"""
Provisional configuration thresholds for image-processing-based disease severity estimation.

IMPORTANT DISCLAIMER:
These thresholds are PROVISIONAL values for a research prototype.
They are NOT scientifically established or expert-validated agricultural standards.
Modify these values after domain-expert validation with annotated field data.
"""

# Provisional severity category upper bounds (percentage of segmented leaf area)
SEVERITY_THRESHOLDS = {
    "negligible_max": 1.0,   # <= 1.0% visible discolouration -> Healthy / No Visible Damage
    "mild_max": 10.0,        # > 1.0% to <= 10.0% -> Mild
    "moderate_max": 30.0,    # > 10.0% to <= 30.0% -> Moderate
    # > 30.0% -> Severe
}

# Tolerance for minor shadows/edge variation when the classifier predicts a healthy class
HEALTHY_CLASS_TOLERANCE_PERCENT = 5.0

# Leaf segmentation reliability guards
MIN_LEAF_AREA_RATIO = 0.03   # Minimum 3% of image area must be segmented as leaf
MAX_LEAF_AREA_RATIO = 1.00   # Allow close-up / full-frame foliage photos up to 100% if plant colour check passes
MIN_PLANT_COLOR_RATIO = 0.35 # At least 35% of segmented region must show plant-like hues (green/yellow/brown)
MIN_CONTOUR_AREA_RATIO = 0.015  # Ignore tiny background artifacts smaller than 1.5% of image

# Processing resolution cap (keeps detail while ensuring fast execution)
MAX_ANALYSIS_DIMENSION = 768
