"""Pure standard-library OOXML builder for Soil-Sense Presentation (.pptx).

Generates a fully valid, widescreen (16:9), dark-theme PowerPoint presentation
without requiring any external dependencies or network downloads.
"""

import os
import zipfile

OUTPUT_PPTX = os.path.join(os.path.dirname(__file__), "Soil_Sense_Presentation.pptx")

# 1 inch = 914,400 EMUs
# Widescreen 16:9: Width = 13.333 inches (12,192,000 EMUs), Height = 7.5 inches (6,858,000 EMUs)
WIDTH_EMU = 12192000
HEIGHT_EMU = 6858000

# Color Constants
BG_COLOR = "0A1120"       # Deep Slate
CARD_BG = "111A2E"        # Card Background
ACCENT_GREEN = "10B981"   # Emerald
ACCENT_CYAN = "38BDF8"    # Sky Blue
TEXT_WHITE = "F8FAFC"     # White
TEXT_MUTED = "94A3B8"     # Muted Slate
CARD_BORDER = "1E293B"    # Subtle Border
BORDER_GREEN = "10B981"   # Highlight Border


def make_shape_xml(sp_id, name, x_in, y_in, w_in, h_in, bg_hex, border_hex, title, bullets):
    """Generate OOXML shape string for a card or text container."""
    x = int(x_in * 914400)
    y = int(y_in * 914400)
    w = int(w_in * 914400)
    h = int(h_in * 914400)

    # Paragraphs
    p_xml = []
    if title:
        p_xml.append(f"""
        <a:p>
          <a:pPr algn="l">
            <a:spcBef><a:spcPts val="0"/></a:spcBef>
            <a:spcAft><a:spcPts val="600"/></a:spcAft>
          </a:pPr>
          <a:r>
            <a:rPr lang="en-US" sz="1500" b="1">
              <a:solidFill><a:srgbClr val="{ACCENT_CYAN}"/></a:solidFill>
              <a:latin typeface="Segoe UI"/>
            </a:rPr>
            <a:t>{title}</a:t>
          </a:r>
        </a:p>
        """)

    for b in bullets:
        # Split bold prefix if present
        if ":" in b:
            parts = b.split(":", 1)
            b_head = parts[0] + ":"
            b_tail = parts[1]
            p_xml.append(f"""
            <a:p>
              <a:pPr algn="l" lvl="0" marL="288000" indent="-288000">
                <a:buClr><a:srgbClr val="{ACCENT_GREEN}"/></a:buClr>
                <a:buChar char="•"/>
                <a:spcBef><a:spcPts val="450"/></a:spcBef>
              </a:pPr>
              <a:r>
                <a:rPr lang="en-US" sz="1150" b="1">
                  <a:solidFill><a:srgbClr val="{TEXT_WHITE}"/></a:solidFill>
                  <a:latin typeface="Segoe UI"/>
                </a:rPr>
                <a:t>{b_head}</a:t>
              </a:r>
              <a:r>
                <a:rPr lang="en-US" sz="1150" b="0">
                  <a:solidFill><a:srgbClr val="{TEXT_MUTED}"/></a:solidFill>
                  <a:latin typeface="Segoe UI"/>
                </a:rPr>
                <a:t>{b_tail}</a:t>
              </a:r>
            </a:p>
            """)
        else:
            p_xml.append(f"""
            <a:p>
              <a:pPr algn="l" lvl="0" marL="288000" indent="-288000">
                <a:buClr><a:srgbClr val="{ACCENT_GREEN}"/></a:buClr>
                <a:buChar char="•"/>
                <a:spcBef><a:spcPts val="450"/></a:spcBef>
              </a:pPr>
              <a:r>
                <a:rPr lang="en-US" sz="1150" b="0">
                  <a:solidFill><a:srgbClr val="{TEXT_WHITE}"/></a:solidFill>
                  <a:latin typeface="Segoe UI"/>
                </a:rPr>
                <a:t>{b}</a:t>
              </a:r>
            </a:p>
            """)

    fill_xml = f'<a:solidFill><a:srgbClr val="{bg_hex}"/></a:solidFill>' if bg_hex else '<a:noFill/>'
    ln_xml = f'<a:ln w="19050"><a:solidFill><a:srgbClr val="{border_hex}"/></a:solidFill></a:ln>' if border_hex else '<a:ln><a:noFill/></a:ln>'

    return f"""
    <p:sp>
      <p:nvSpPr>
        <p:cNvPr id="{sp_id}" name="{name}"/>
        <p:cNvSpPr/>
        <p:nvPr/>
      </p:nvSpPr>
      <p:spPr>
        <a:xfrm>
          <a:off x="{x}" y="{y}"/>
          <a:ext cx="{w}" cy="{h}"/>
        </a:xfrm>
        <a:prstGeom prst="roundRect">
          <a:avLst><a:gd name="adj" fmla="val 2000"/></a:avLst>
        </a:prstGeom>
        {fill_xml}
        {ln_xml}
      </p:spPr>
      <p:txBody>
        <a:bodyPr tIns="144000" bIns="144000" lIns="180000" rIns="180000" anchor="t"/>
        <a:lstStyle/>
        {"".join(p_xml)}
      </p:txBody>
    </p:sp>
    """


def make_slide_xml(header_badge, title, cards):
    """Generate OOXML for a slide with dark background, header, and content cards."""
    shapes = []
    sp_id = 2

    # Background shape
    shapes.append(f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{sp_id}" name="Background"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x="0" y="0"/><a:ext cx="{WIDTH_EMU}" cy="{HEIGHT_EMU}"/></a:xfrm>
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        <a:solidFill><a:srgbClr val="{BG_COLOR}"/></a:solidFill>
      </p:spPr>
      <p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody>
    </p:sp>
    """)
    sp_id += 1

    # Header Badge & Title
    if header_badge or title:
        badge_xml = f"""
        <a:p>
          <a:r>
            <a:rPr lang="en-US" sz="1050" b="1">
              <a:solidFill><a:srgbClr val="{ACCENT_GREEN}"/></a:solidFill>
              <a:latin typeface="Segoe UI"/>
            </a:rPr>
            <a:t>{header_badge.upper()}</a:t>
          </a:r>
        </a:p>
        """ if header_badge else ""

        title_xml = f"""
        <a:p>
          <a:spcBef><a:spcPts val="200"/></a:spcBef>
          <a:r>
            <a:rPr lang="en-US" sz="2400" b="1">
              <a:solidFill><a:srgbClr val="{TEXT_WHITE}"/></a:solidFill>
              <a:latin typeface="Segoe UI"/>
            </a:rPr>
            <a:t>{title}</a:t>
          </a:r>
        </a:p>
        """ if title else ""

        shapes.append(f"""
        <p:sp>
          <p:nvSpPr><p:cNvPr id="{sp_id}" name="Header"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="731520" y="365760"/><a:ext cx="10972800" cy="914400"/></a:xfrm>
            <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
            <a:noFill/>
            <a:ln><a:noFill/></a:ln>
          </p:spPr>
          <p:txBody>
            <a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0"/>
            <a:lstStyle/>
            {badge_xml}
            {title_xml}
          </p:txBody>
        </p:sp>
        """)
        sp_id += 1

    # Add content cards
    for c in cards:
        shapes.append(make_shape_xml(
            sp_id, f"Card_{sp_id}",
            c["x"], c["y"], c["w"], c["h"],
            c.get("bg", CARD_BG),
            c.get("border", CARD_BORDER),
            c.get("title", ""),
            c.get("bullets", [])
        ))
        sp_id += 1

    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
           xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
           xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
      <p:cSld>
        <p:spTree>
          <p:nvGrpSpPr>
            <p:cNvPr id="1" name=""/>
            <p:cNvGrpSpPr/>
            <p:nvPr/>
          </p:nvGrpSpPr>
          <p:grpSpPr>
            <a:xfrm>
              <a:off x="0" y="0"/>
              <a:ext cx="0" cy="0"/>
              <a:chOff x="0" y="0"/>
              <a:chExt cx="0" cy="0"/>
            </a:xfrm>
          </p:grpSpPr>
          {"".join(shapes)}
        </p:spTree>
      </p:cSld>
      <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
    </p:sld>
    """


def build_soil_sense_deck():
    """Define content for all 8 slides and build the .pptx zip container."""
    slides_data = [
        # SLIDE 1: Title
        {
            "badge": "🌱 MACHINE LEARNING & PRECISION AGRICULTURE",
            "title": "",
            "cards": [
                {
                    "x": 0.8, "y": 1.6, "w": 11.7, "h": 4.5,
                    "bg": CARD_BG, "border": BORDER_GREEN,
                    "title": "Soil-Sense: Precision Soil Fertility Diagnostics",
                    "bullets": [
                        "Project Goal: Explainable Multiclass Machine Learning Classification (Low / Medium / High).",
                        "Agronomic Indicators: Nitrogen (N), Phosphorus (P), Potassium (K), pH, EC, Moisture, Temperature, Humidity.",
                        "Security Engineering: Cryptographic SHA-256 model verification mitigating CWE-502 deserialization risks.",
                        "Storage Sandbox: 100% contained execution on D: drive with zero C: drive bloat (< 400 MB).",
                        "Live Deployment: Interactive responsive Bento-grid dashboard hosted on Streamlit Cloud."
                    ]
                }
            ]
        },

        # SLIDE 2: Problem Statement
        {
            "badge": "01 • PROBLEM STATEMENT & MOTIVATION",
            "title": "Challenges in Modern Soil Diagnostics",
            "cards": [
                {
                    "x": 0.8, "y": 1.7, "w": 5.7, "h": 5.0,
                    "bg": CARD_BG, "border": CARD_BORDER,
                    "title": "⚠️ Wet-Lab Bottlenecks",
                    "bullets": [
                        "High Latency: Laboratory chemical soil testing typically takes 2 to 4 weeks for results.",
                        "Diagnostic Complexity: Interpreting 8+ physicochemical parameters simultaneously is challenging for growers.",
                        "Over-Fertilization: Misdiagnosing soil leads to excessive chemical application and ground-water pollution.",
                        "Accessibility: Smallholder farmers lack real-time decision-support tools in remote rural belts."
                    ]
                },
                {
                    "x": 6.8, "y": 1.7, "w": 5.7, "h": 5.0,
                    "bg": CARD_BG, "border": BORDER_GREEN,
                    "title": "💡 Soil-Sense Solution",
                    "bullets": [
                        "Real-Time Inference: Multiclass classification (Low / Medium / High) generated in under 50 milliseconds.",
                        "Actionable Heuristics: Automatic parameter diagnosis mapped to ICAR/FAO corrective amendments.",
                        "Zero Cloud Lock-in: Runs on lightweight Scikit-learn pipelines with zero heavy deep-learning bloat.",
                        "Multi-Sample Screening: Upload batch farm surveys with instant CSV diagnostic report exports."
                    ]
                }
            ]
        },

        # SLIDE 3: System Architecture
        {
            "badge": "02 • SYSTEM ARCHITECTURE & SANDBOXING",
            "title": "Technical Architecture & Storage Protection",
            "cards": [
                {
                    "x": 0.8, "y": 1.7, "w": 3.7, "h": 5.0,
                    "bg": CARD_BG, "border": CARD_BORDER,
                    "title": "1. Core Stack",
                    "bullets": [
                        "Language: Python 3.12 / 3.14.",
                        "ML Engine: Scikit-learn (Pipelines, Scalers, Imputers).",
                        "Data Engine: Pandas & NumPy.",
                        "Validation: Pydantic v2 schemas.",
                        "Frontend: Streamlit with responsive CSS Grid."
                    ]
                },
                {
                    "x": 4.8, "y": 1.7, "w": 3.7, "h": 5.0,
                    "bg": CARD_BG, "border": CARD_BORDER,
                    "title": "2. Pipeline Design",
                    "bullets": [
                        "Data Ingestion: Clean raw tabular soil observation datasets.",
                        "Leak-Free Scaling: StandardScaler fitted strictly on X_train.",
                        "Class Balancing: Stratified split ensuring uniform sensitivity.",
                        "Inference Engine: Returns class and confidence probabilities."
                    ]
                },
                {
                    "x": 8.8, "y": 1.7, "w": 3.7, "h": 5.0,
                    "bg": CARD_BG, "border": BORDER_GREEN,
                    "title": "3. C: Drive Protection",
                    "bullets": [
                        "Virtualenv on D: Isolated .venv on secondary drive.",
                        "Cache Redirection: Pip cache set to D:\\pip-cache.",
                        "Temp Isolation: Build temp pointed to D:\\temp.",
                        "Ultra-Light: Complete footprint < 400 MB."
                    ]
                }
            ]
        },

        # SLIDE 4: Dataset & Agronomic Features
        {
            "badge": "03 • DATA ENGINEERING & AGRONOMY",
            "title": "8 Physicochemical Features & ICAR Standards",
            "cards": [
                {
                    "x": 0.8, "y": 1.7, "w": 5.7, "h": 5.0,
                    "bg": CARD_BG, "border": CARD_BORDER,
                    "title": "🧪 8 Measurable Soil Features",
                    "bullets": [
                        "Nitrogen (N): Essential for vegetative foliage (Optimal: 140–280 mg/kg).",
                        "Phosphorus (P): Early root development & cellular energy (Optimal: 15–30 mg/kg).",
                        "Potassium (K): Stomatal regulation & drought tolerance (Optimal: 130–280 mg/kg).",
                        "Soil Reaction (pH): Acidity vs alkalinity on 0–14 scale (Neutral: 6.2–7.5).",
                        "Electrical Cond. (EC): Salinity index in dS/m (Non-saline: < 1.0 dS/m).",
                        "Moisture & Climate: Available water % (25–60%), Temperature & Humidity."
                    ]
                },
                {
                    "x": 6.8, "y": 1.7, "w": 5.7, "h": 5.0,
                    "bg": CARD_BG, "border": BORDER_GREEN,
                    "title": "🌾 Fertility Class Tiers",
                    "bullets": [
                        "High Fertility (🟢): Balanced macronutrients, neutral pH, low salinity, optimal moisture.",
                        "Medium Fertility (🟡): Moderate nutrient levels, mild pH deviation, or minor water stress.",
                        "Low Fertility (🔴): Severe depletion in NPK, extreme acidity (< 5.5) or sodicity (> 8.5), or salinity.",
                        "Scientific Alignment: Calibrated against ICAR Soil Health Card standards."
                    ]
                }
            ]
        },

        # SLIDE 5: Machine Learning Modeling
        {
            "badge": "04 • MODELING & EXPERIMENTAL BENCHMARKS",
            "title": "Supervised Classifier Comparison",
            "cards": [
                {
                    "x": 0.8, "y": 1.7, "w": 5.7, "h": 5.0,
                    "bg": CARD_BG, "border": CARD_BORDER,
                    "title": "📊 5-Fold Stratified Cross-Validation",
                    "bullets": [
                        "Decision Tree Classifier: Explainable baseline. CV Macro F1: 97.23% | Test F1: 96.96%.",
                        "Random Forest Classifier: Bagging ensemble of 120 trees. CV Macro F1: 99.79% | Test F1: 99.44%.",
                        "K-Nearest Neighbors (Champion): Distance-weighted classifier. CV Macro F1: 99.72% | Test F1: 100.0%.",
                        "Metric Focus: Evaluated using Macro-averaged F1 to prevent majority-class bias."
                    ]
                },
                {
                    "x": 6.8, "y": 1.7, "w": 5.7, "h": 5.0,
                    "bg": CARD_BG, "border": BORDER_GREEN,
                    "title": "🏆 Pipeline Highlights",
                    "bullets": [
                        "Zero Data Leakage: Scalers fitted solely on training folds within Pipeline.",
                        "Test Evaluation: Evaluated on 360 untouched test samples with clean boundary separation.",
                        "Feature Importance: Nitrogen, Phosphorus, and Electrical Conductivity are primary decision drivers.",
                        "Reproducibility: Seed fixed across all random splits."
                    ]
                }
            ]
        },

        # SLIDE 6: Security Hardening
        {
            "badge": "05 • CYBERSECURITY & DEFENSE-IN-DEPTH",
            "title": "Security Hardening & Input Sanitization",
            "cards": [
                {
                    "x": 0.8, "y": 1.7, "w": 5.7, "h": 5.0,
                    "bg": CARD_BG, "border": BORDER_GREEN,
                    "title": "🛡️ Deserialization Defense (CWE-502)",
                    "bullets": [
                        "The Threat: Python pickle / joblib allows arbitrary code execution from malicious model files.",
                        "Cryptographic Hash: SHA-256 digest computed during training (models/model_checksum.json).",
                        "Load-Time Verification: SoilPredictor computes hash and aborts if file is altered or tampered.",
                        "Path Containment: Model loading locked strictly to trusted internal directory."
                    ]
                },
                {
                    "x": 6.8, "y": 1.7, "w": 5.7, "h": 5.0,
                    "bg": CARD_BG, "border": CARD_BORDER,
                    "title": "🔒 Pydantic Validation & Test Suite",
                    "bullets": [
                        "Boundary Rules: Enforces physical limits (0 ≤ pH ≤ 14, non-negative nutrients, moisture ≤ 100%).",
                        "Input Sanitization: Blocks text injections, NaNs, and infinite float values.",
                        "Automated Test Suite: 8 unit tests in pytest verifying boundary rules and tamper detection.",
                        "Production Reliability: Ensures model never receives corrupted numerical arrays."
                    ]
                }
            ]
        },

        # SLIDE 7: UI/UX Bento-Grid
        {
            "badge": "06 • FRONTEND ARCHITECTURE & UX",
            "title": "Modern Agritech Bento-Grid Interface",
            "cards": [
                {
                    "x": 0.8, "y": 1.7, "w": 5.7, "h": 5.0,
                    "bg": CARD_BG, "border": CARD_BORDER,
                    "title": "✨ Responsive Design System",
                    "bullets": [
                        "Bento-Grid Architecture: Clean modular cards organizing parameters, status, and advisories.",
                        "Full-Page Edge-to-Edge: 98% wide-screen view eliminating narrow side margins.",
                        "Mobile-Ready Grid: Parameter Health Matrix flexes from 8 cards to 2 columns on phones.",
                        "Visual Fertility Badges: High-impact glowing cards (🟢 High, 🟡 Medium, 🔴 Low)."
                    ]
                },
                {
                    "x": 6.8, "y": 1.7, "w": 5.7, "h": 5.0,
                    "bg": CARD_BG, "border": BORDER_GREEN,
                    "title": "🌾 Interactive Platform Tools",
                    "bullets": [
                        "Regional Archetype Presets: 1-click loading for Alluvial, Black Cotton, Laterite, and Saline soils.",
                        "Parameter Health Matrix: Compares live input values directly against ICAR reference bands.",
                        "Prescriptive Guidance: Actionable advice (e.g. lime for acidity, gypsum for sodicity, FYM for N).",
                        "Batch CSV Screening: Multi-sample file uploader with downloadable diagnostic reports."
                    ]
                }
            ]
        },

        # SLIDE 8: Conclusion & Roadmap
        {
            "badge": "07 • PROJECT CONCLUSION & ROADMAP",
            "title": "Deliverables & Future Scope",
            "cards": [
                {
                    "x": 0.8, "y": 1.7, "w": 5.7, "h": 5.0,
                    "bg": CARD_BG, "border": CARD_BORDER,
                    "title": "📌 Key Deliverables Achieved",
                    "bullets": [
                        "Trained ML Pipeline: High-performance supervised classifier with 100% test F1-score.",
                        "Security-Hardened: SHA-256 model signature and Pydantic boundary validation.",
                        "Cloud Deployment: Running live on Streamlit Community Cloud (omvs077/soil-sense).",
                        "Comprehensive Docs: Architectural specifications, agronomic standards, and viva guides in docs/."
                    ]
                },
                {
                    "x": 6.8, "y": 1.7, "w": 5.7, "h": 5.0,
                    "bg": CARD_BG, "border": BORDER_GREEN,
                    "title": "🚀 Future Research Scope",
                    "bullets": [
                        "Wireless IoT Probes: Real-time telemetry via ESP32 / LoRaWAN NPK and moisture sensors.",
                        "Satellite GIS Integration: Fusing Sentinel-2 multispectral surface reflectance and NDVI data.",
                        "Crop-Specific Recommendations: Tailoring fertilizer recommendations to crop nutrient demand curves.",
                        "Micronutrient Assays: Expanding model features to include Zinc, Iron, and Organic Carbon."
                    ]
                }
            ]
        }
    ]

    # Content Types XML
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
      <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
      <Default Extension="xml" ContentType="application/xml"/>
      <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
      <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
      <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
      <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
    """
    for i in range(1, len(slides_data) + 1):
        content_types += f'  <Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n'
    content_types += "</Types>"

    # Package Relationships XML
    root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
    </Relationships>"""

    # Presentation XML
    pres_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                    xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
      <p:sldMasterIdLst>
        <p:sldMasterId id="2147483648" r:id="rId1"/>
      </p:sldMasterIdLst>
      <p:sldIdLst>
    """
    for i in range(1, len(slides_data) + 1):
        pres_xml += f'    <p:sldId id="{255 + i}" r:id="rId{i + 1}"/>\n'
    pres_xml += f"""
      </p:sldIdLst>
      <p:sldSz cx="{WIDTH_EMU}" cy="{HEIGHT_EMU}" type="screen16x9"/>
      <p:notesSz cx="6858000" cy="9144000"/>
    </p:presentation>
    """

    # Presentation Relationships
    pres_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
    """
    for i in range(1, len(slides_data) + 1):
        pres_rels += f'  <Relationship Id="rId{i + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>\n'
    pres_rels += "</Relationships>"

    # Minimal Slide Master
    slide_master = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                 xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
      <p:cSld>
        <p:spTree>
          <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
          <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
        </p:spTree>
      </p:cSld>
      <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
      <p:sldLayoutIdLst>
        <p:sldLayoutId id="2147483649" r:id="rId1"/>
      </p:sldLayoutIdLst>
    </p:sldMaster>
    """

    # Slide Master Rels
    master_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
      <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
    </Relationships>"""

    # Slide Layout
    slide_layout = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                 xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                 type="blank" preserve="1">
      <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
      <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
    </p:sldLayout>
    """

    layout_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
    </Relationships>"""

    # Theme XML
    theme_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="SoilSenseDark">
      <a:themeElements>
        <a:clrScheme name="SoilSense">
          <a:dk1><a:srgbClr val="0A1120"/></a:dk1>
          <a:lt1><a:srgbClr val="F8FAFC"/></a:lt1>
          <a:dk2><a:srgbClr val="111A2E"/></a:dk2>
          <a:lt2><a:srgbClr val="94A3B8"/></a:lt2>
          <a:accent1><a:srgbClr val="10B981"/></a:accent1>
          <a:accent2><a:srgbClr val="38BDF8"/></a:accent2>
          <a:accent3><a:srgbClr val="F59E0B"/></a:accent3>
          <a:accent4><a:srgbClr val="EF4444"/></a:accent4>
          <a:accent5><a:srgbClr val="8B5CF6"/></a:accent5>
          <a:accent6><a:srgbClr val="EC4899"/></a:accent6>
          <a:hlink><a:srgbClr val="38BDF8"/></a:hlink>
          <a:folHlink><a:srgbClr val="10B981"/></a:folHlink>
        </a:clrScheme>
        <a:fontScheme name="PlusJakarta">
          <a:majorFont><a:latin typeface="Segoe UI"/></a:majorFont>
          <a:minorFont><a:latin typeface="Segoe UI"/></a:minorFont>
        </a:fontScheme>
        <a:fmtScheme name="Office">
          <a:fillStyleLst><a:solidFill><a:srgbClr val="111A2E"/></a:solidFill></a:fillStyleLst>
          <a:lnStyleLst><a:ln w="9525"><a:solidFill><a:srgbClr val="1E293B"/></a:solidFill></a:ln></a:lnStyleLst>
          <a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
          <a:bgFillStyleLst><a:solidFill><a:srgbClr val="0A1120"/></a:solidFill></a:bgFillStyleLst>
        </a:fmtScheme>
      </a:themeElements>
    </a:theme>
    """

    # Single Slide Relationships (pointing to slideLayout1)
    slide_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
    </Relationships>"""

    # Write Zip Archive (.pptx)
    with zipfile.ZipFile(OUTPUT_PPTX, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("ppt/presentation.xml", pres_xml)
        z.writestr("ppt/_rels/presentation.xml.rels", pres_rels)
        z.writestr("ppt/slideMasters/slideMaster1.xml", slide_master)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", master_rels)
        z.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", layout_rels)
        z.writestr("ppt/theme/theme1.xml", theme_xml)

        for i, s_data in enumerate(slides_data, start=1):
            slide_xml = make_slide_xml(s_data["badge"], s_data["title"], s_data["cards"])
            z.writestr(f"ppt/slides/slide{i}.xml", slide_xml)
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels)

    print(f"Presentation successfully generated: {OUTPUT_PPTX}")
    print(f"File size: {os.path.getsize(OUTPUT_PPTX)} bytes")


if __name__ == "__main__":
    build_soil_sense_deck()
