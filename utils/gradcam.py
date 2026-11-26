import cv2
import numpy as np
import tensorflow as tf

from utils.predictor import get_model, preprocess_image

# Cache gradient models keyed by (id(model), layer_name) to avoid rebuilding on every call.
_GRAD_MODEL_CACHE = {}


def _is_4d_spatial_layer(layer):
    """Return True if layer produces a 4D feature map with spatial dimensions > 1."""
    try:
        shape = layer.output.shape
    except Exception:
        shape = getattr(layer, "output_shape", None)

    if not shape or len(shape) != 4:
        return False

    h, w = shape[1], shape[2]
    return (h is None or h > 1) and (w is None or w > 1)


def find_target_conv_layer(model):
    """
    Identify the final spatial convolutional/activation layer in the saved model.
    Supports both flat MobileNetV2 models and models with a nested MobileNetV2 backbone.
    """
    # Prefer 'out_relu' if present directly on the top-level model.
    for layer in reversed(model.layers):
        if layer.name == "out_relu" and _is_4d_spatial_layer(layer):
            return layer, None

    # Check if there is a nested sub-model (e.g. a nested MobileNetV2 functional layer).
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.Model):
            for sub_layer in reversed(layer.layers):
                if sub_layer.name == "out_relu" and _is_4d_spatial_layer(sub_layer):
                    return sub_layer, layer
            for sub_layer in reversed(layer.layers):
                if isinstance(
                    sub_layer,
                    (tf.keras.layers.Conv2D, tf.keras.layers.DepthwiseConv2D, tf.keras.layers.ReLU),
                ) and _is_4d_spatial_layer(sub_layer):
                    return sub_layer, layer

    # Fallback: last 4D spatial conv/activation layer on the top-level model.
    for layer in reversed(model.layers):
        if isinstance(
            layer,
            (tf.keras.layers.Conv2D, tf.keras.layers.DepthwiseConv2D, tf.keras.layers.ReLU),
        ) and _is_4d_spatial_layer(layer):
            return layer, None

    raise ValueError("No suitable 4D spatial convolutional layer found for Grad-CAM.")


def _get_grad_model(model, target_layer, nested_backbone):
    """Build or retrieve a cached model returning (conv_outputs, predictions)."""
    cache_key = (id(model), target_layer.name, id(nested_backbone) if nested_backbone else None)
    if cache_key in _GRAD_MODEL_CACHE:
        return _GRAD_MODEL_CACHE[cache_key]

    if nested_backbone is None:
        grad_model = tf.keras.Model(
            inputs=model.inputs,
            outputs=[target_layer.output, model.output],
        )
        _GRAD_MODEL_CACHE[cache_key] = ("flat", grad_model)
    else:
        backbone_idx = model.layers.index(nested_backbone)
        tail_layers = model.layers[backbone_idx + 1 :]
        backbone_probe = tf.keras.Model(
            inputs=nested_backbone.inputs,
            outputs=[target_layer.output, nested_backbone.output],
        )
        _GRAD_MODEL_CACHE[cache_key] = ("nested", (backbone_probe, tail_layers))

    return _GRAD_MODEL_CACHE[cache_key]


def generate_gradcam(image_path, class_index=None, alpha=0.45):
    """
    Generate a genuine gradient-based Grad-CAM heatmap overlay for the given image.

    Reuses the already-loaded MobileNetV2 model and exact classifier preprocessing.
    Returns a dict with:
        success (bool), original_rgb (ndarray|None), overlay_rgb (ndarray|None),
        heatmap (ndarray|None), target_layer (str|None), class_index (int|None),
        error (str|None)
    """
    try:
        model = get_model()
        input_tensor, orig_bgr = preprocess_image(image_path)
        if orig_bgr is None or orig_bgr.size == 0:
            return {"success": False, "error": "Invalid or empty image."}

        target_layer, nested_backbone = find_target_conv_layer(model)
        mode, model_ref = _get_grad_model(model, target_layer, nested_backbone)

        input_tf = tf.convert_to_tensor(input_tensor, dtype=tf.float32)

        with tf.GradientTape() as tape:
            if mode == "flat":
                conv_outputs, predictions = model_ref(input_tf, training=False)
            else:
                backbone_probe, tail_layers = model_ref
                conv_outputs, x = backbone_probe(input_tf, training=False)
                for layer in tail_layers:
                    x = layer(x, training=False)
                predictions = x

            if isinstance(predictions, (list, tuple)):
                predictions = predictions[0]

            if class_index is None:
                class_index = int(tf.argmax(predictions[0]).numpy())

            class_score = predictions[:, class_index]

        grads = tape.gradient(class_score, conv_outputs)
        if grads is None:
            return {
                "success": False,
                "error": f"Gradients did not flow to layer '{target_layer.name}'.",
            }

        grads_np = grads.numpy()
        conv_np = conv_outputs[0].numpy()

        if not np.all(np.isfinite(grads_np)) or not np.all(np.isfinite(conv_np)):
            return {
                "success": False,
                "error": "Non-finite activations or gradients encountered during Grad-CAM.",
            }

        # Global average pooling of gradients across spatial dimensions (H, W)
        pooled_grads = np.mean(grads_np, axis=(0, 1, 2))
        heatmap = np.sum(conv_np * pooled_grads, axis=-1)

        # Apply ReLU to keep only positive contributions
        heatmap = np.maximum(heatmap, 0.0)
        max_val = float(np.max(heatmap))
        if max_val <= 1e-8:
            return {
                "success": False,
                "error": "Grad-CAM produced an empty activation map for this image.",
            }

        heatmap = heatmap / max_val

        orig_h, orig_w = orig_bgr.shape[:2]
        heatmap_resized = cv2.resize(heatmap.astype(np.float32), (orig_w, orig_h))
        heatmap_uint8 = np.uint8(np.clip(heatmap_resized * 255.0, 0, 255))

        colored_heatmap_bgr = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        alpha = float(np.clip(alpha, 0.4, 0.5))
        overlay_bgr = cv2.addWeighted(orig_bgr, 1.0 - alpha, colored_heatmap_bgr, alpha, 0)

        original_rgb = cv2.cvtColor(orig_bgr, cv2.COLOR_BGR2RGB)
        overlay_rgb = cv2.cvtColor(overlay_bgr, cv2.COLOR_BGR2RGB)

        return {
            "success": True,
            "original_rgb": original_rgb,
            "overlay_rgb": overlay_rgb,
            "heatmap": heatmap_resized,
            "target_layer": target_layer.name,
            "class_index": class_index,
            "error": None,
        }
    except Exception as exc:
        return {
            "success": False,
            "original_rgb": None,
            "overlay_rgb": None,
            "heatmap": None,
            "target_layer": None,
            "class_index": class_index,
            "error": str(exc),
        }
