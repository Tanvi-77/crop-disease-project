translations = {

    # =========================================================
    # ENGLISH
    # =========================================================

    "English": {

        "home": "Home",

        "detection": "Disease Detection",

        "history": "Prediction History",

        "title": "Crop Disease Detection System",

        "subtitle": "Smart Farming Dashboard",

        "select_crop": "Select Crop",

        "upload_image": "Upload Leaf Image",

        "predict_button": "Predict Disease",

        "prediction_result": "Prediction Result",

        "disease": "Disease",

        "confidence": "Confidence",

        "solution": "Solution",

        "history_empty": "No prediction history found.",

        "camera": "📷 Capture Leaf Image",

        "upload_text": "Upload or capture a leaf image for disease detection.",

        "explainable_ai": "Explainable AI – Grad-CAM Visualization",
        "gradcam_heatmap": "Grad-CAM Heatmap",
        "original_leaf_image": "Original Leaf Image",
        "heatmap_overlay": "Heatmap Overlay",
        "gradcam_explanation": "Grad-CAM highlights the image regions that contributed most to the model's prediction. It helps users understand where the model focused when identifying a disease.",
        "gradcam_colour_legend": "Red/yellow: relatively strong positive activation. Blue/green: relatively weaker activation.",
        "gradcam_limitation": "Highlighted regions represent model activation, not verified disease locations. A heatmap does not prove that the model has identified the actual infected tissue.",
        "gradcam_warning": "Grad-CAM heatmap could not be generated for this image. The disease prediction above remains valid.",

        "severity_estimation": "Disease Severity Estimation",
        "estimated_damaged_area": "Estimated Visible Damage",
        "severity_label": "Severity",
        "severity_calculation": "Damaged area / Total leaf area × 100",
        "leaf_segmentation_mask": "Leaf Segmentation",
        "detected_damage_regions": "Detected Damaged Regions",
        "severity_explanation": "Visible discolouration inside the segmented leaf is estimated using OpenCV colour and luminance analysis with provisional thresholds.",
        "severity_limitation": "Severity is estimated from visible leaf discolouration using image processing. Lighting, shadows, leaf segmentation and natural leaf variations may affect the result. This estimate is preliminary and should not replace an agricultural expert's assessment.",
        "severity_unreliable_msg": "Unable to estimate severity reliably.",
        "severity_warning": "Severity estimation could not be completed reliably for this image.",
        "explanation_heading": "Explanation",
        "methodology_heading": "Methodology",
        "limitation_heading": "Limitation",
        "severity_mild": "Mild",
        "severity_moderate": "Moderate",
        "severity_severe": "Severe",
        "severity_healthy": "Healthy / No Visible Damage",
        "severity_unreliable": "Unable to Estimate Reliably"
    },

    # =========================================================
    # HINDI
    # =========================================================

    "Hindi": {

        "home": "होम",

        "detection": "रोग पहचान",

        "history": "पूर्वानुमान इतिहास",

        "title": "फसल रोग पहचान प्रणाली",

        "subtitle": "स्मार्ट खेती डैशबोर्ड",

        "select_crop": "फसल चुनें",

        "upload_image": "पत्ते की छवि अपलोड करें",

        "predict_button": "रोग पहचानें",

        "prediction_result": "परिणाम",

        "disease": "रोग",

        "confidence": "विश्वास स्तर",

        "solution": "समाधान",

        "history_empty": "कोई इतिहास उपलब्ध नहीं है।",

        "camera": "📷 पत्ते की फोटो लें",

        "upload_text": "रोग पहचान के लिए पत्ते की छवि अपलोड करें या कैमरा उपयोग करें।",

        "explainable_ai": "व्याख्यात्मक AI – Grad-CAM विज़ुअलाइज़ेशन",
        "gradcam_heatmap": "Grad-CAM हीटमैप",
        "original_leaf_image": "मूल पत्ते की छवि",
        "heatmap_overlay": "हीटमैप ओवरले",
        "gradcam_explanation": "Grad-CAM उन छवि क्षेत्रों को उजागर करता है जिन्होंने मॉडल के पूर्वानुमान में सबसे अधिक योगदान दिया। यह समझने में मदद करता है कि रोग पहचानते समय मॉडल ने कहाँ ध्यान केंद्रित किया।",
        "gradcam_colour_legend": "लाल/पीला: अपेक्षाकृत अधिक सक्रियण। नीला/हरा: अपेक्षाकृत कम सक्रियण।",
        "gradcam_limitation": "हाइलाइट किए गए क्षेत्र मॉडल की सक्रियता दर्शाते हैं, प्रमाणित रोग स्थान नहीं। हीटमैप यह सिद्ध नहीं करता कि मॉडल ने वास्तविक संक्रमित ऊतक की पहचान की है।",
        "gradcam_warning": "इस छवि के लिए Grad-CAM हीटमैप तैयार नहीं किया जा सका। ऊपर दिया गया रोग पूर्वानुमान मान्य है।",

        "severity_estimation": "रोग गंभीरता अनुमान",
        "estimated_damaged_area": "अनुमानित दृश्य क्षति",
        "severity_label": "गंभीरता",
        "severity_calculation": "क्षतिग्रस्त क्षेत्र / कुल पत्ते का क्षेत्र × 100",
        "leaf_segmentation_mask": "पत्ते का विभाजन",
        "detected_damage_regions": "पहचाने गए क्षतिग्रस्त क्षेत्र",
        "severity_explanation": "विभाजित पत्ते के भीतर दिखाई देने वाले रंग-परिवर्तन का अनुमान OpenCV रंग और चमक विश्लेषण तथा अस्थायी सीमाओं के आधार पर लगाया जाता है।",
        "severity_limitation": "गंभीरता का अनुमान इमेज प्रोसेसिंग द्वारा पत्ते के रंग-परिवर्तन से लगाया गया है। प्रकाश, छाया, पत्ते के विभाजन और प्राकृतिक भिन्नताओं से परिणाम प्रभावित हो सकते हैं। यह प्रारंभिक अनुमान है और कृषि विशेषज्ञ की सलाह का विकल्प नहीं है।",
        "severity_unreliable_msg": "गंभीरता का विश्वसनीय अनुमान नहीं लगाया जा सका।",
        "severity_warning": "इस छवि के लिए रोग गंभीरता का विश्वसनीय अनुमान नहीं लगाया जा सका।",
        "explanation_heading": "व्याख्या",
        "methodology_heading": "कार्यप्रणाली",
        "limitation_heading": "सीमाएं",
        "severity_mild": "हल्का (Mild)",
        "severity_moderate": "मध्यम (Moderate)",
        "severity_severe": "गंभीर (Severe)",
        "severity_healthy": "स्वस्थ / कोई दृश्य क्षति नहीं",
        "severity_unreliable": "विश्वसनीय अनुमान संभव नहीं"
    },

    # =========================================================
    # MARATHI
    # =========================================================

    "Marathi": {

        "home": "मुख्यपृष्ठ",

        "detection": "पीक रोग ओळख",

        "history": "पूर्वीचा इतिहास",

        "title": "पीक रोग ओळख प्रणाली",

        "subtitle": "स्मार्ट शेती डॅशबोर्ड",

        "select_crop": "पीक निवडा",

        "upload_image": "पानाचा फोटो अपलोड करा",

        "predict_button": "रोग ओळखा",

        "prediction_result": "निकाल",

        "disease": "रोग",

        "confidence": "विश्वास पातळी",

        "solution": "उपाय",

        "history_empty": "कोणताही इतिहास उपलब्ध नाही.",

        "camera": "📷 पानाचा फोटो काढा",

        "upload_text": "रोग ओळखण्यासाठी पानाचा फोटो अपलोड करा किंवा कॅमेरा वापरा.",

        "explainable_ai": "स्पष्टीकरणात्मक AI – Grad-CAM व्हिज्युअलायझेशन",
        "gradcam_heatmap": "Grad-CAM हीटमॅप",
        "original_leaf_image": "मूळ पानाची प्रतिमा",
        "heatmap_overlay": "हीटमॅप ओव्हरले",
        "gradcam_explanation": "Grad-CAM मॉडेलच्या अंदाजात सर्वाधिक योगदान देणारे प्रतिमेचे भाग ठळक करते. रोग ओळखताना मॉडेलने कोठे लक्ष केंद्रित केले हे समजण्यास यामुळे मदत होते.",
        "gradcam_colour_legend": "लाल/पिवळा: तुलनेने जास्त सक्रियता. निळा/हिरवा: तुलनेने कमी सक्रियता.",
        "gradcam_limitation": "ठळक केलेले भाग मॉडेलची सक्रियता दर्शवतात, प्रमाणित रोगग्रस्त भाग नाहीत. हीटमॅपमुळे मॉडेलने प्रत्यक्ष संक्रमित भाग ओळखला हे सिद्ध होत नाही.",
        "gradcam_warning": "या प्रतिमेसाठी Grad-CAM हीटमॅप तयार करता आला नाही. वरील रोग अंदाज वैध आहे.",

        "severity_estimation": "रोग तीव्रता अंदाज",
        "estimated_damaged_area": "अंदाजित दृश्य नुकसान",
        "severity_label": "तीव्रता",
        "severity_calculation": "नुकसान झालेला भाग / एकूण पानाचे क्षेत्र × 100",
        "leaf_segmentation_mask": "पानाचे विभाजन",
        "detected_damage_regions": "ओळखलेले नुकसानग्रस्त भाग",
        "severity_explanation": "विभागलेल्या पानातील दृश्य रंगबदलाचा अंदाज OpenCV रंग व प्रकाश विश्लेषणाद्वारे तात्पुरत्या मर्यादा वापरून काढला जातो.",
        "severity_limitation": "तीव्रतेचा अंदाज इमेज प्रोसेसिंगद्वारे पानाच्या दृश्य रंगबदलावरून काढला आहे. प्रकाश, सावली, पानाचे विभाजन आणि नैसर्गिक फरक यांचा निकालावर परिणाम होऊ शकतो. हा प्राथमिक अंदाज असून कृषी तज्ज्ञांच्या तपासणीला पर्याय नाही.",
        "severity_unreliable_msg": "तीव्रतेचा विश्वासार्ह अंदाज काढता आला नाही.",
        "severity_warning": "या प्रतिमेसाठी तीव्रतेचा विश्वासार्ह अंदाज काढता आला नाही.",
        "explanation_heading": "स्पष्टीकरण",
        "methodology_heading": "कार्यपद्धती",
        "limitation_heading": "मर्यादा",
        "severity_mild": "सौम्य (Mild)",
        "severity_moderate": "मध्यम (Moderate)",
        "severity_severe": "तीव्र (Severe)",
        "severity_healthy": "निरोगी / दृश्य नुकसान नाही",
        "severity_unreliable": "विश्वसनीय अंदाज शक्य नाही"
    }
}