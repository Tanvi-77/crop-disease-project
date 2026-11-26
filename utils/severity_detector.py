import cv2
import numpy as np

from utils.severity_config import (
    HEALTHY_CLASS_TOLERANCE_PERCENT,
    MAX_ANALYSIS_DIMENSION,
    MAX_LEAF_AREA_RATIO,
    MIN_CONTOUR_AREA_RATIO,
    MIN_LEAF_AREA_RATIO,
    MIN_PLANT_COLOR_RATIO,
    SEVERITY_THRESHOLDS,
)


def _resize_for_analysis(image_bgr, max_dim=MAX_ANALYSIS_DIMENSION):
    """Resize only if larger than max_dim to preserve lesion detail at reasonable speed."""
    h, w = image_bgr.shape[:2]
    largest = max(h, w)
    if largest <= max_dim:
        return image_bgr
    scale = max_dim / float(largest)
    new_w = max(1, int(round(w * scale)))
    new_h = max(1, int(round(h * scale)))
    return cv2.resize(image_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)


def _segment_leaf(image_bgr):
    """
    Segment the leaf region from background while preserving yellow, brown,
    and dark necrotic areas inside the leaf contour.
    """
    h, w = image_bgr.shape[:2]
    img_area = float(h * w)

    # Light smoothing to reduce sensor noise without blurring small lesions
    smoothed = cv2.GaussianBlur(image_bgr, (5, 5), 0)

    hsv = cv2.cvtColor(smoothed, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(smoothed, cv2.COLOR_BGR2LAB)

    hue = hsv[:, :, 0]
    sat = hsv[:, :, 1]
    val = hsv[:, :, 2]

    lab_a = lab[:, :, 1].astype(np.float32)
    lab_b = lab[:, :, 2].astype(np.float32)

    # Lab chroma distance from neutral gray (128, 128)
    chroma = np.sqrt((lab_a - 128.0) ** 2 + (lab_b - 128.0) ** 2)

    # Excess Green index helps retain green leaf tissue even under low saturation
    b_ch, g_ch, r_ch = cv2.split(smoothed.astype(np.float32))
    exg = 2.0 * g_ch - r_ch - b_ch

    # Plant-colour cue: covers green, yellow, orange, and brown leaf tissue
    plant_hue_mask = (hue >= 4) & (hue <= 96) & (sat >= 22) & (val >= 20)
    # Exclude clearly non-plant cool/blue/purple backgrounds from chroma cue
    non_plant_chroma = (hue >= 98) & (hue <= 155) & (sat >= 35)
    chroma_mask = (chroma >= 14.0) & (val >= 20) & (val <= 248) & (~non_plant_chroma)
    green_mask = exg >= 14.0

    fg_mask = np.where(plant_hue_mask | chroma_mask | green_mask, 255, 0).astype(np.uint8)

    # Close small gaps inside leaves and open small isolated background specks
    close_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    open_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, close_kernel)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, open_kernel)

    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, 0.0

    # Keep only substantial contours relative to image and largest leaf component
    max_contour_area = max(cv2.contourArea(c) for c in contours)
    min_abs_area = img_area * MIN_CONTOUR_AREA_RATIO
    kept_contours = [
        c
        for c in contours
        if cv2.contourArea(c) >= min_abs_area and cv2.contourArea(c) >= 0.15 * max_contour_area
    ]

    if not kept_contours:
        return None, 0.0

    # Fill external contours so dark internal necrotic spots are never dropped
    leaf_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.drawContours(leaf_mask, kept_contours, -1, 255, thickness=cv2.FILLED)

    leaf_pixels = int(np.count_nonzero(leaf_mask))
    leaf_ratio = leaf_pixels / img_area

    if leaf_pixels == 0 or leaf_ratio < MIN_LEAF_AREA_RATIO or leaf_ratio > MAX_LEAF_AREA_RATIO:
        return None, leaf_ratio

    # Verify the segmented region actually contains plant-like colours (not a blue/red wall)
    plant_like = (plant_hue_mask | green_mask) & (leaf_mask > 0)
    plant_fraction = int(np.count_nonzero(plant_like)) / float(leaf_pixels)
    if plant_fraction < MIN_PLANT_COLOR_RATIO:
        return None, leaf_ratio

    return leaf_mask, leaf_ratio


def _detect_damaged_regions(image_bgr, leaf_mask):
    """
    Detect visible discoloured/damaged regions (chlorosis, brown lesions, dark necrosis)
    strictly inside the segmented leaf mask, guarding against shadows and leaf-edge halos.
    """
    smoothed = cv2.GaussianBlur(image_bgr, (3, 3), 0)
    hsv = cv2.cvtColor(smoothed, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(smoothed, cv2.COLOR_BGR2LAB)

    hue = hsv[:, :, 0]
    sat = hsv[:, :, 1]
    val = hsv[:, :, 2]

    lab_l = lab[:, :, 0].astype(np.float32)
    lab_a = lab[:, :, 1].astype(np.float32)
    lab_b = lab[:, :, 2].astype(np.float32)

    b_ch, g_ch, r_ch = cv2.split(smoothed.astype(np.float32))
    exg = 2.0 * g_ch - r_ch - b_ch

    leaf_bool = leaf_mask > 0
    leaf_l_values = lab_l[leaf_bool]
    if leaf_l_values.size == 0:
        return np.zeros_like(leaf_mask)

    median_l = float(np.median(leaf_l_values))

    # 1. Yellow / chlorotic patches (exclude healthy bright green using Lab a* >= 116)
    yellow_mask = (
        (hue >= 18)
        & (hue < 36)
        & (sat >= 40)
        & (val >= 50)
        & (lab_b >= 136.0)
        & (lab_a >= 116.0)
    )

    # 2. Brown / tan / rust / blight lesions (shifted away from green on Lab a*)
    brown_mask = (
        ((hue <= 24) | (hue >= 165))
        & (sat >= 25)
        & (val >= 20)
        & (lab_a >= 125.0)
    )

    # 3. Dark necrotic regions (significantly darker than leaf median AND lacking green ExG)
    dark_threshold = max(45.0, median_l - 35.0)
    necrotic_mask = (
        (lab_l < dark_threshold)
        & (val < 110)
        & ((lab_a >= 122.0) | (exg <= 10.0))
    )

    candidate = np.where(yellow_mask | brown_mask | necrotic_mask, 255, 0).astype(np.uint8)

    # Suppress 1-2px outer leaf boundary halos from background bleed
    erode_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    interior_mask = cv2.erode(leaf_mask, erode_kernel, iterations=1)
    candidate = cv2.bitwise_and(candidate, interior_mask)

    # Remove isolated 1-2px sensor noise and thin vein speckles, then consolidate spots
    clean_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    candidate = cv2.morphologyEx(candidate, cv2.MORPH_OPEN, clean_kernel)
    candidate = cv2.morphologyEx(candidate, cv2.MORPH_CLOSE, clean_kernel)

    # Strictly restrict final mask to the segmented leaf
    damage_mask = cv2.bitwise_and(candidate, leaf_mask)
    return damage_mask


def _categorize_severity(damaged_percentage, predicted_disease=None):
    """Map damaged percentage to a category key and human-readable label."""
    is_healthy_pred = bool(predicted_disease and "healthy" in predicted_disease.lower())

    if is_healthy_pred and damaged_percentage <= HEALTHY_CLASS_TOLERANCE_PERCENT:
        return "healthy", "Healthy / No Visible Damage"

    if damaged_percentage <= SEVERITY_THRESHOLDS["negligible_max"]:
        return "healthy", "Healthy / No Visible Damage"
    if damaged_percentage <= SEVERITY_THRESHOLDS["mild_max"]:
        return "mild", "Mild"
    if damaged_percentage <= SEVERITY_THRESHOLDS["moderate_max"]:
        return "moderate", "Moderate"
    return "severe", "Severe"


def estimate_severity(image_path, predicted_disease=None):
    """
    Estimate visible leaf damage percentage and severity category using OpenCV.

    Returns a dict with:
        success (bool), status (str: 'ok'|'unreliable'|'error'),
        damaged_percentage (float|None), category_key (str), category_label (str),
        leaf_pixels (int), damaged_pixels (int),
        original_rgb (ndarray|None), leaf_mask_rgb (ndarray|None),
        damage_overlay_rgb (ndarray|None), error (str|None)
    """
    try:
        orig_bgr = cv2.imread(image_path)
        if orig_bgr is None or orig_bgr.size == 0:
            return {
                "success": False,
                "status": "error",
                "damaged_percentage": None,
                "category_key": "unreliable",
                "category_label": "Unable to Estimate Reliably",
                "leaf_pixels": 0,
                "damaged_pixels": 0,
                "original_rgb": None,
                "leaf_mask_rgb": None,
                "damage_overlay_rgb": None,
                "error": "Unable to read image for severity estimation.",
            }

        work_bgr = _resize_for_analysis(orig_bgr)
        original_rgb = cv2.cvtColor(work_bgr, cv2.COLOR_BGR2RGB)

        leaf_mask, _ = _segment_leaf(work_bgr)
        if leaf_mask is None:
            return {
                "success": False,
                "status": "unreliable",
                "damaged_percentage": None,
                "category_key": "unreliable",
                "category_label": "Unable to Estimate Reliably",
                "leaf_pixels": 0,
                "damaged_pixels": 0,
                "original_rgb": original_rgb,
                "leaf_mask_rgb": None,
                "damage_overlay_rgb": None,
                "error": "Leaf segmentation was unreliable for this image.",
            }

        leaf_pixels = int(np.count_nonzero(leaf_mask))
        if leaf_pixels == 0:
            return {
                "success": False,
                "status": "unreliable",
                "damaged_percentage": None,
                "category_key": "unreliable",
                "category_label": "Unable to Estimate Reliably",
                "leaf_pixels": 0,
                "damaged_pixels": 0,
                "original_rgb": original_rgb,
                "leaf_mask_rgb": None,
                "damage_overlay_rgb": None,
                "error": "Segmented leaf mask is empty.",
            }

        damage_mask = _detect_damaged_regions(work_bgr, leaf_mask)
        damaged_pixels = int(np.count_nonzero(damage_mask))

        raw_pct = (damaged_pixels / float(leaf_pixels)) * 100.0
        damaged_percentage = round(float(np.clip(raw_pct, 0.0, 100.0)), 2)

        category_key, category_label = _categorize_severity(
            damaged_percentage, predicted_disease=predicted_disease
        )

        # Build segmented-leaf visualization (leaf in colour on dark slate background + green outline)
        dark_bg = np.full_like(original_rgb, (15, 23, 42))
        leaf_mask_rgb = np.where(leaf_mask[:, :, None] > 0, original_rgb, dark_bg)
        leaf_contours, _ = cv2.findContours(leaf_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(leaf_mask_rgb, leaf_contours, -1, (34, 197, 94), 2)

        # Build damage-region visualization (distinct red-orange highlight + cyan leaf boundary)
        damage_overlay_rgb = original_rgb.copy()
        if damaged_pixels > 0:
            highlight = damage_overlay_rgb.copy()
            highlight[damage_mask > 0] = (239, 68, 68)
            damage_overlay_rgb = cv2.addWeighted(damage_overlay_rgb, 0.45, highlight, 0.55, 0)
        cv2.drawContours(damage_overlay_rgb, leaf_contours, -1, (56, 189, 248), 2)

        return {
            "success": True,
            "status": "ok",
            "damaged_percentage": damaged_percentage,
            "category_key": category_key,
            "category_label": category_label,
            "leaf_pixels": leaf_pixels,
            "damaged_pixels": damaged_pixels,
            "original_rgb": original_rgb,
            "leaf_mask_rgb": leaf_mask_rgb,
            "damage_overlay_rgb": damage_overlay_rgb,
            "error": None,
        }
    except Exception as exc:
        return {
            "success": False,
            "status": "error",
            "damaged_percentage": None,
            "category_key": "unreliable",
            "category_label": "Unable to Estimate Reliably",
            "leaf_pixels": 0,
            "damaged_pixels": 0,
            "original_rgb": None,
            "leaf_mask_rgb": None,
            "damage_overlay_rgb": None,
            "error": str(exc),
        }
