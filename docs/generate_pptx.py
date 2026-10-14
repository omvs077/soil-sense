"""Script to generate a modern 8-slide PowerPoint presentation (.pptx) for Soil-Sense."""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "Soil_Sense_Presentation.pptx")

# Color Palette (Modern Agritech Dark Theme)
COLOR_BG = RGBColor(10, 17, 32)         # Deep Navy #0A1120
COLOR_CARD = RGBColor(17, 26, 46)       # Surface #111A2E
COLOR_ACCENT = RGBColor(16, 185, 129)   # Emerald Green #10B981
COLOR_CYAN = RGBColor(56, 189, 248)     # Accent Cyan #38BDF8
COLOR_AMBER = RGBColor(245, 158, 11)    # Amber #F59E0B
COLOR_WHITE = RGBColor(248, 250, 252)   # Title Text #F8FAFC
COLOR_MUTED = RGBColor(148, 163, 184)   # Body Muted #94A3B8
COLOR_CARD_BORDER = RGBColor(30, 41, 59)


def set_slide_background(slide):
    """Set dark slate background for slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG


def add_header(slide, title_text, category_text="SOIL-SENSE ML PLATFORM"):
    """Add standard header across slides."""
    # Category pill
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.35))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_ACCENT

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11), Inches(0.8))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE


def add_card(slide, left, top, width, height, title, items, border_color=COLOR_CARD_BORDER):
    """Add a sleek card with title and bulleted text."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = COLOR_CARD
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)

    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(15)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_CYAN

    for item in items:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_WHITE
        p.space_before = Pt(6)


def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "🌱 MACHINE LEARNING & PRECISION AGRICULTURE"
    p_badge.font.size = Pt(13)
    p_badge.font.bold = True
    p_badge.font.color.rgb = COLOR_ACCENT

    p_title = tf1.add_paragraph()
    p_title.text = "Soil-Sense: Precision Soil Fertility Diagnostics"
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE
    p_title.space_before = Pt(12)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Explainable Multiclass Classification • Security-Hardened (CWE-502) • Zero C: Drive Bloat"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = COLOR_CYAN
    p_sub.space_before = Pt(10)

    p_foot = tf1.add_paragraph()
    p_foot.text = "Supervised Classification (Low / Medium / High) | Scikit-learn & Streamlit Cloud"
    p_foot.font.size = Pt(13)
    p_foot.font.color.rgb = COLOR_MUTED
    p_foot.space_before = Pt(28)

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Statement & Project Motivation", "THE CHALLENGE")

    add_card(
        s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
        "⚠️ Traditional Soil Testing Bottlenecks",
        [
            "High Costs & Latency: Certified wet-lab soil chemical testing takes 2–4 weeks and requires specialized instruments.",
            "Multidimensional Complexity: Interpreting NPK, pH, EC, moisture, and temperature simultaneously is difficult for non-specialists.",
            "Blind Fertilizer Over-Application: Misjudging soil requirements leads to nutrient imbalances, soil acidification, and ground runoff.",
            "Accessibility Barrier: Smallholder farmers lack instant decision-support mechanisms in remote field areas."
        ]
    )

    add_card(
        s2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
        "💡 Proposed Soil-Sense Solution",
        [
            "Instant Supervised Inference: Fast, consistent multiclass classification into High, Medium, or Low fertility tiers.",
            "Actionable Agronomic Guidance: Maps specific parameter deficits to ICAR/FAO corrective fertilizer prescriptions.",
            "Accessible Bento-Grid UI: Clean web and mobile-responsive interface for single-sample and batch CSV screening.",
            "Zero Cloud Lock-in: Fully reproducible open-source software running locally or on serverless cloud."
        ],
        border_color=COLOR_ACCENT
    )

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE & STORAGE INTEGRITY
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "System Architecture & Zero C: Drive Bloat Sandbox", "ENGINEERING DESIGN")

    add_card(
        s3, Inches(0.8), Inches(1.8), Inches(3.7), Inches(5.0),
        "1. Core Tech Stack",
        [
            "Language: Python 3.12 / 3.14",
            "ML Framework: Scikit-learn (Pipeline, Ensembles, Scalers)",
            "Data Engine: Pandas & NumPy",
            "Validation: Pydantic v2",
            "UI Framework: Streamlit with bespoke CSS Grid design system"
        ]
    )

    add_card(
        s3, Inches(4.8), Inches(1.8), Inches(3.7), Inches(5.0),
        "2. Pipeline Execution",
        [
            "Data Validation: Pydantic schema sanitization before inference.",
            "Zero Data Leakage: Scalers encapsulated in Scikit-Learn Pipeline.",
            "Ensemble Inference: Probabilistic confidence scores per class.",
            "Advisory Engine: Rule-based heuristics for targeted treatments."
        ]
    )

    add_card(
        s3, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
        "3. C: Drive Protection",
        [
            "Storage Sandbox: Virtual environment and models reside 100% on D:.",
            "Cache Redirection: Pip cache mapped to D:\\pip-cache and build temp to D:\\temp.",
            "Ultra-Lightweight: Total disk footprint < 400 MB (vs > 3.5 GB for Deep Learning alternatives)."
        ],
        border_color=COLOR_ACCENT
    )

    # =========================================================================
    # SLIDE 4: DATASET & AGRONOMIC BENCHMARKS
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Dataset Specification & Agronomic Reference Bands", "DATA ENGINEERING")

    add_card(
        s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
        "🧪 8 Core Physicochemical Features",
        [
            "Primary Macronutrients: Nitrogen (N), Phosphorus (P), Potassium (K) measured in mg/kg.",
            "Soil Reaction (pH): Acidity vs alkalinity on 0–14 scale (Neutral band: 6.2 – 7.5).",
            "Electrical Conductivity (EC): Salinity index in dS/m (< 1.0 dS/m is non-saline).",
            "Moisture Content (%): Available water content in the root zone (Optimal: 25 – 60%).",
            "Microclimate Factors: Ambient Temperature (°C) and Relative Humidity (%)."
        ]
    )

    add_card(
        s4, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
        "🌾 ICAR & FAO Soil Quality Tiers",
        [
            "High Fertility (🟢): Balanced NPK within optimal bands, neutral pH, low EC, adequate soil moisture.",
            "Medium Fertility (🟡): Moderate nutrient levels, mild pH deviation, or minor moisture stress; easily correctable.",
            "Low Fertility (🔴): Severe depletion in multiple macronutrients, extreme acidity (< 5.5) or alkalinity (> 8.5), or salinity stress.",
            "Target Classes: Low (0), Medium (1), High (2)."
        ]
    )

    # =========================================================================
    # SLIDE 5: ML METHODOLOGY & EXPERIMENTAL RESULTS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Supervised Machine Learning Comparison", "MODELING & EVALUATION")

    add_card(
        s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
        "📊 5-Fold Stratified Cross-Validation",
        [
            "Decision Tree Classifier: Baseline interpretable model. CV Macro F1: 97.23% | Test F1: 96.96%.",
            "Random Forest Classifier: Bagging ensemble with 120 trees. CV Macro F1: 99.79% | Test F1: 99.44%.",
            "K-Nearest Neighbors (Champion): Distance-weighted classifier with feature normalization. CV Macro F1: 99.72% | Test F1: 100.0%.",
            "Metric Focus: Evaluated using Macro-averaged F1-Score to guarantee balanced sensitivity across all fertility classes."
        ]
    )

    add_card(
        s5, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
        "🏆 Champion Pipeline Highlights",
        [
            "Encapsulation: SimpleImputer (median) + StandardScaler + Estimator.",
            "Test Set Evaluation: Evaluated on 360 untouched test samples with zero confusion between Low and High classes.",
            "Feature Importances: Primary drivers of fertility classification are Nitrogen, Phosphorus, and Electrical Conductivity.",
            "Reproducibility: Random state fixed across all training splits."
        ],
        border_color=COLOR_ACCENT
    )

    # =========================================================================
    # SLIDE 6: SECURITY HARDENING & DEFENSE IN DEPTH
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Security Hardening & Vulnerability Remediation", "CYBERSECURITY & ROBUSTNESS")

    add_card(
        s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
        "🛡️ Deserialization Protection (CWE-502)",
        [
            "Vulnerability: Python pickle / joblib allows arbitrary code execution via untrusted serialized bytecode.",
            "Cryptographic Verification: A SHA-256 digest is generated during training and stored in models/model_checksum.json.",
            "Integrity Check at Load: SoilPredictor computes the file hash and blocks unpickling if any tampering or mismatch is detected.",
            "Scoped Paths: File loading restricted exclusively to internal directories."
        ],
        border_color=COLOR_ACCENT
    )

    add_card(
        s6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
        "🔒 Input Sanitization & Automated Testing",
        [
            "Pydantic Schema Validation: Enforces biological boundary rules (0 ≤ pH ≤ 14, non-negative nutrients, bounded moisture).",
            "Injection Rejection: Strictly rejects non-numeric text strings, NaNs, and infinite float values.",
            "Pytest Automated Test Suite: 8 automated unit tests covering input sanitization, batch schema errors, and cryptographic tamper detection.",
            "Zero Data Leakage: Transforms fitted strictly on X_train."
        ]
    )

    # =========================================================================
    # SLIDE 7: UI/UX DESIGN & BENTO-GRID DASHBOARD
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Modern Agritech Bento-Grid Interface", "FRONTEND ARCHITECTURE")

    add_card(
        s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
        "✨ UI/UX Design System",
        [
            "Non-Generic Aesthetic: Bespoke dark theme with vibrant emerald, amber, and coral fertility status banners.",
            "Full-Page Edge-to-Edge: Responsive 98% width layout eliminating narrow margins on wide displays.",
            "Mobile-Ready CSS Grid: Parameter Health Matrix dynamically flexes from 4/8 columns on desktop to 2 columns on phones.",
            "Synced Dual Controls: Dual slider + numeric inputs with real-time validation badges."
        ]
    )

    add_card(
        s7, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
        "🌾 Core Application Features",
        [
            "Regional Archetype Presets: Instant 1-click loading for Alluvial Loam, Black Cotton, Acidic Sand, and Saline Sodic.",
            "Class Probability Stack: Animated progress bars showing exact confidence breakdown per class.",
            "Prescriptive Advisory Feed: Specific agronomic recommendations (e.g. lime for acidity, gypsum for sodicity, FYM for N).",
            "Batch CSV Screening: Drag-and-drop multiple field samples with summary metrics and exportable CSV reports."
        ],
        border_color=COLOR_CYAN
    )

    # =========================================================================
    # SLIDE 8: CONCLUSION, LIMITATIONS & FUTURE SCOPE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Summary, Limitations & Future Roadmap", "PROJECT CONCLUSION")

    add_card(
        s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
        "📌 Key Project Deliverables",
        [
            "Complete Supervised Classification Pipeline with 100% test accuracy on held-out benchmark data.",
            "Security Hardened ML Engine with SHA-256 checksums and Pydantic validation.",
            "Production Cloud Deployment on Streamlit Community Cloud (omvs077/soil-sense).",
            "Comprehensive Documentation: Architectural blueprints, agronomic reference guides, and viva defense FAQ in docs/."
        ]
    )

    add_card(
        s8, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0),
        "🚀 Future Research Directions",
        [
            "IoT Wireless Ingestion: Direct real-time sensor integration via ESP32 / LoRaWAN soil probes.",
            "Satellite Earth Observation: Fusing Sentinel-2 multispectral surface reflectance and NDVI vegetation index data.",
            "Crop-Specific Recommendation Engine: Mapping fertility classes to tailored crop-specific nutrient demand curves.",
            "Micronutrient Assay Expansion: Integrating Zinc, Boron, and organic carbon assay variables."
        ],
        border_color=COLOR_ACCENT
    )

    prs.save(OUTPUT_FILE)
    print(f"[SUCCESS] PowerPoint presentation generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_presentation()
