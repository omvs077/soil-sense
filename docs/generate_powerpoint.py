import os
import win32com.client

def create_presentation():
    output_path = os.path.abspath(r"D:\My projects\Soil-sense\docs\Soil_Sense_Presentation.pptx")
    cm_path = os.path.abspath(r"D:\My projects\Soil-sense\reports\figures\confusion_matrix.png")

    ppt = win32com.client.Dispatch("PowerPoint.Application")
    ppt.Visible = True
    pres = ppt.Presentations.Add()

    # 16:9 widescreen: 13.333 x 7.5 inches -> 960 x 540 points
    pres.PageSetup.SlideWidth = 960
    pres.PageSetup.SlideHeight = 540

    # Colors
    c_bg = 0xF8FAFC       # #FCFAF8 in BGR -> Light Slate / Off-White
    c_navy = 0x50240F     # #0F2450 in BGR -> Dark Navy / Slate 900
    c_emerald = 0x469B05  # #059B46 in BGR -> Emerald Green
    c_card_bg = 0xFFFFFF  # White
    c_border = 0xE2E8F0   # Light Gray Border
    c_text_dark = 0x1E293B
    c_text_muted = 0x64748B
    c_tag_bg = 0xEEF9F1
    c_white = 0xFFFFFF

    def set_slide_bg(slide):
        slide.Background.Fill.Solid()
        slide.Background.Fill.ForeColor.RGB = c_bg

    def add_header(slide, title_text, category_text):
        # Category Tag
        tag = slide.Shapes.AddShape(1, 40, 24, 260, 22) # 1 = msoShapeRectangle
        tag.Fill.Solid()
        tag.Fill.ForeColor.RGB = c_tag_bg
        tag.Line.Visible = False
        tag.TextFrame.MarginLeft = 10
        tag.TextFrame.MarginRight = 10
        tag.TextFrame.MarginTop = 2
        tag.TextFrame.MarginBottom = 2
        p_tag = tag.TextFrame.TextRange
        p_tag.Text = category_text.upper()
        p_tag.Font.Size = 9
        p_tag.Font.Bold = True
        p_tag.Font.Name = "Calibri"
        p_tag.Font.Color.RGB = c_emerald

        # Title
        title_box = slide.Shapes.AddTextbox(1, 36, 46, 880, 40)
        p_title = title_box.TextFrame.TextRange
        p_title.Text = title_text
        p_title.Font.Size = 22
        p_title.Font.Bold = True
        p_title.Font.Name = "Calibri"
        p_title.Font.Color.RGB = c_navy
        title_box.TextFrame.MarginLeft = 0
        title_box.TextFrame.MarginTop = 0

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = pres.Slides.Add(1, 12) # 12 = ppLayoutBlank
    set_slide_bg(s1)

    # Accent decorative bar
    bar = s1.Shapes.AddShape(1, 0, 0, 16, 540)
    bar.Fill.Solid()
    bar.Fill.ForeColor.RGB = c_emerald
    bar.Line.Visible = False

    # Review Tag
    rev_tag = s1.Shapes.AddShape(1, 70, 75, 300, 26)
    rev_tag.Fill.Solid()
    rev_tag.Fill.ForeColor.RGB = c_tag_bg
    rev_tag.Line.Visible = False
    p = rev_tag.TextFrame.TextRange
    p.Text = "PROJECT REVIEW - I | ACADEMIC EVALUATION"
    p.Font.Size = 10
    p.Font.Bold = True
    p.Font.Name = "Calibri"
    p.Font.Color.RGB = c_emerald

    # Main Project Title
    t_box = s1.Shapes.AddTextbox(1, 65, 115, 820, 100)
    p = t_box.TextFrame.TextRange
    p.Text = "SOIL-SENSE\nAI-Driven Soil Fertility Prediction System"
    p.Font.Size = 34
    p.Font.Bold = True
    p.Font.Name = "Calibri"
    p.Font.Color.RGB = c_navy

    # Subtitle
    sub_box = s1.Shapes.AddTextbox(1, 68, 230, 820, 60)
    p = sub_box.TextFrame.TextRange
    p.Text = "Multi-Class Physicochemical Soil Quality Assessment with Zero Data Leakage\nand Cryptographic Pickle Hardening (CWE-502 Mitigation)"
    p.Font.Size = 15
    p.Font.Name = "Calibri"
    p.Font.Color.RGB = c_text_muted

    # Student / Review Info Card
    info_card = s1.Shapes.AddShape(1, 70, 340, 820, 130)
    info_card.Fill.Solid()
    info_card.Fill.ForeColor.RGB = c_card_bg
    info_card.Line.ForeColor.RGB = c_border
    info_card.Line.Weight = 1.5

    info_text = s1.Shapes.AddTextbox(1, 90, 355, 780, 100)
    p = info_text.TextFrame.TextRange
    p.Text = "Target Domain: Precision Agriculture and Machine Learning\nArchitecture: Scikit-Learn Pipeline | Streamlit Real-Time Dashboard | ICAR / FAO Compliant\nSecurity Assurance: SHA-256 Model Integrity Verification and Strict Pydantic v2 Bounds\nReview Phase: Problem Formulation, Dataset Engineering, Baseline Model Benchmark"
    p.Font.Size = 13
    p.Font.Name = "Calibri"
    p.Font.Color.RGB = c_text_dark
    p.Lines(1).Font.Bold = True

    # ==========================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # ==========================================
    s2 = pres.Slides.Add(2, 12)
    set_slide_bg(s2)
    add_header(s2, "Problem Statement & Industry Motivation", "Review Phase 1: Context & Challenges")

    card_data_s2 = [
        ("Traditional Lab Delays", "Conventional laboratory soil testing (wet chemistry) takes 10 to 14 days, preventing timely fertilizer intervention during active sowing windows."),
        ("Indiscriminate NPK Overuse", "Lack of rapid testing leads farmers to apply generic urea/DAP regimens, causing soil acidification, salinization, and severe groundwater contamination."),
        ("Insecure & Leaky ML Systems", "Generic AI tutorials demonstrate unscaled features, preprocessing leakage, and unverified pickle imports prone to CWE-502 arbitrary code execution.")
    ]

    for i, (title, desc) in enumerate(card_data_s2):
        x = 50 + i * 295
        card = s2.Shapes.AddShape(1, x, 110, 275, 230)
        card.Fill.Solid()
        card.Fill.ForeColor.RGB = c_card_bg
        card.Line.ForeColor.RGB = c_border
        card.Line.Weight = 1

        top_line = s2.Shapes.AddShape(1, x, 110, 275, 4)
        top_line.Fill.Solid()
        top_line.Fill.ForeColor.RGB = c_emerald if i == 0 else (c_navy if i == 1 else 0x993333)
        top_line.Line.Visible = False

        tb = s2.Shapes.AddTextbox(1, x + 15, 125, 245, 200)
        p = tb.TextFrame.TextRange
        p.Text = f"0{i+1}\n\n{title}\n\n{desc}"
        p.Paragraphs(1).Font.Size = 18
        p.Paragraphs(1).Font.Bold = True
        p.Paragraphs(1).Font.Color.RGB = c_emerald
        p.Paragraphs(3).Font.Size = 15
        p.Paragraphs(3).Font.Bold = True
        p.Paragraphs(3).Font.Color.RGB = c_navy
        p.Paragraphs(5).Font.Size = 12
        p.Paragraphs(5).Font.Color.RGB = c_text_muted

    stat_card = s2.Shapes.AddShape(1, 50, 365, 865, 120)
    stat_card.Fill.Solid()
    stat_card.Fill.ForeColor.RGB = c_tag_bg
    stat_card.Line.ForeColor.RGB = c_emerald
    stat_card.Line.Weight = 1

    stat_tb = s2.Shapes.AddTextbox(1, 70, 375, 825, 100)
    p = stat_tb.TextFrame.TextRange
    p.Text = "National Agricultural Impact:\nAccording to ICAR and FAO surveys, timely precision NPK diagnosis improves crop yield by 18-24% while reducing chemical input costs by up to 30%. Soil-Sense bridges the diagnostic gap through instant multi-class fertility classification."
    p.Font.Size = 13
    p.Font.Name = "Calibri"
    p.Font.Color.RGB = c_navy
    p.Lines(1).Font.Bold = True

    # ==========================================
    # SLIDE 3: OBJECTIVES & CORE FEATURES
    # ==========================================
    s3 = pres.Slides.Add(3, 12)
    set_slide_bg(s3)
    add_header(s3, "Project Objectives & Core Deliverables", "System Scope & Functional Goals")

    objectives = [
        ("Multi-Parameter Classification", "Predict overall Soil Fertility into Low, Medium, or High tiers from 8 soil and weather parameters without delay."),
        ("Strict Data Leakage Prevention", "Encapsulate standard scaling and ML classifiers strictly inside Scikit-Learn Pipelines so test folds remain uncompromised."),
        ("Prescriptive Agronomic Guidance", "Map ML diagnostic results into actionable ICAR/FAO fertilizer advisory rules for balanced organic and chemical soil replenishment."),
        ("CWE-502 Defense Architecture", "Implement automated SHA-256 cryptographic checksum matching before loading serialized joblib models into production memory."),
        ("High-Throughput Batch Processing", "Provide real-time interactive screening alongside bulk multi-sample CSV batch scoring with automated visual summaries.")
    ]

    for i, (title, desc) in enumerate(objectives):
        y = 110 + i * 75
        card = s3.Shapes.AddShape(1, 50, y, 865, 65)
        card.Fill.Solid()
        card.Fill.ForeColor.RGB = c_card_bg
        card.Line.ForeColor.RGB = c_border
        card.Line.Weight = 1

        badge = s3.Shapes.AddShape(1, 65, y + 16, 32, 32)
        badge.Fill.Solid()
        badge.Fill.ForeColor.RGB = c_tag_bg
        badge.Line.Visible = False
        p = badge.TextFrame.TextRange
        p.Text = f"{i+1}"
        p.Font.Size = 13
        p.Font.Bold = True
        p.Font.Color.RGB = c_emerald

        tb = s3.Shapes.AddTextbox(1, 115, y + 10, 780, 50)
        p = tb.TextFrame.TextRange
        p.Text = f"{title}: {desc}"
        p.Font.Size = 12.5
        p.Font.Name = "Calibri"
        p.Font.Color.RGB = c_text_dark
        p.Words(1).Font.Bold = True

    # ==========================================
    # SLIDE 4: TECHNOLOGY STACK & ARCHITECTURE
    # ==========================================
    s4 = pres.Slides.Add(4, 12)
    set_slide_bg(s4)
    add_header(s4, "Technology Stack & Modular Architecture", "System Design & Environment")

    stack_cards = [
        ("Core Machine Learning", "Python 3.12 / 3.14\nScikit-Learn 1.6+\nJoblib Pipeline Serialization\nKNN & Random Forest Classifiers"),
        ("Data Engineering & Validation", "Pydantic v2 Schema Enforcement\nPandas 2.2 Dataframes\nNumPy 2.0 Numerical Ops\nICAR/FAO Boundary Enforcement"),
        ("Interactive Frontend UX", "Streamlit Framework\nEdge-to-Edge Responsive CSS Grid\nReal-time Gauge Indicators\nBento-Card Visual Structure"),
        ("DevOps & Production Security", "C: Drive Bloat Protection\nSHA-256 Integrity Verification\nPytest Rigorous Test Suite\nAutomated Git Tracking & Docs")
    ]

    for i, (title, desc) in enumerate(stack_cards):
        x = 50 + (i % 2) * 445
        y = 110 + (i // 2) * 195
        card = s4.Shapes.AddShape(1, x, y, 420, 175)
        card.Fill.Solid()
        card.Fill.ForeColor.RGB = c_card_bg
        card.Line.ForeColor.RGB = c_border
        card.Line.Weight = 1

        top_line = s4.Shapes.AddShape(1, x, y, 420, 4)
        top_line.Fill.Solid()
        top_line.Fill.ForeColor.RGB = c_emerald if i in [0, 3] else c_navy
        top_line.Line.Visible = False

        tb = s4.Shapes.AddTextbox(1, x + 20, y + 15, 380, 150)
        p = tb.TextFrame.TextRange
        p.Text = f"{title}\n\n{desc}"
        p.Paragraphs(1).Font.Size = 16
        p.Paragraphs(1).Font.Bold = True
        p.Paragraphs(1).Font.Color.RGB = c_navy
        p.Paragraphs(3).Font.Size = 12.5
        p.Paragraphs(3).Font.Color.RGB = c_text_muted

    # ==========================================
    # SLIDE 5: DATASET & PHYSICOCHEMICAL FEATURES
    # ==========================================
    s5 = pres.Slides.Add(5, 12)
    set_slide_bg(s5)
    add_header(s5, "Dataset Features & Physicochemical Ranges", "Data Engineering & Standards")

    features_table_data = [
        ["Parameter", "Feature Name", "Valid Range", "Agronomic Role"],
        ["Nitrogen (N)", "N", "0 - 140 mg/kg", "Vegetative growth and chlorophyll synthesis"],
        ["Phosphorus (P)", "P", "5 - 145 mg/kg", "Root architecture and energy transfer (ATP)"],
        ["Potassium (K)", "K", "5 - 205 mg/kg", "Osmoregulation and disease resistance"],
        ["Soil pH", "pH", "3.5 - 9.5", "Nutrient bioavailability and microbial flora"],
        ["Electrical Cond.", "EC", "0.0 - 4.0 dS/m", "Soil salinity index and osmotic pressure"],
        ["Moisture Content", "Moisture", "0 - 100 %", "Solvent availability and root uptake"],
        ["Temperature", "Temperature", "8 - 50 °C", "Biological metabolic rate and evaporation"],
        ["Air Humidity", "Humidity", "10 - 100 %", "Vapor pressure deficit and transpiration"]
    ]

    t_shape = s5.Shapes.AddTable(9, 4, 50, 105, 860, 380)
    table = t_shape.Table
    table.Columns(1).Width = 140
    table.Columns(2).Width = 110
    table.Columns(3).Width = 120
    table.Columns(4).Width = 490

    for r_idx, row in enumerate(features_table_data):
        for c_idx, val in enumerate(row):
            cell = table.Cell(r_idx + 1, c_idx + 1)
            cell.Shape.TextFrame.TextRange.Text = val
            cell.Shape.TextFrame.MarginLeft = 6
            cell.Shape.TextFrame.MarginRight = 6
            cell.Shape.TextFrame.MarginTop = 3
            cell.Shape.TextFrame.MarginBottom = 3
            p = cell.Shape.TextFrame.TextRange
            p.Font.Name = "Calibri"
            if r_idx == 0:
                cell.Shape.Fill.Solid()
                cell.Shape.Fill.ForeColor.RGB = c_navy
                p.Font.Size = 11
                p.Font.Bold = True
                p.Font.Color.RGB = c_white
            else:
                cell.Shape.Fill.Solid()
                cell.Shape.Fill.ForeColor.RGB = c_card_bg if r_idx % 2 == 1 else 0xF1F5F9
                p.Font.Size = 10.5
                p.Font.Color.RGB = c_text_dark

    # ==========================================
    # SLIDE 6: PROPOSED METHODOLOGY & PIPELINE
    # ==========================================
    s6 = pres.Slides.Add(6, 12)
    set_slide_bg(s6)
    add_header(s6, "Proposed Methodology & Pipeline Workflow", "Machine Learning Pipeline")

    steps = [
        ("1. Data Ingestion & Sanitization", "Pydantic v2 schemas rigorously validate feature boundaries, rejecting out-of-bound or corrupted sensor inputs."),
        ("2. Leak-Free Preprocessing", "StandardScaler transformations are strictly bound inside an active Scikit-Learn Pipeline during CV fit."),
        ("3. Model Benchmarking", "Evaluation of Decision Tree, K-Nearest Neighbors, and Random Forest models using stratified 5-fold cross-validation."),
        ("4. Cryptographic Model Packaging", "Pipeline serialization with companion SHA-256 hash generation for tamper-evident production deployment."),
        ("5. Diagnostic & Prescriptive UI", "Multi-class fertility inference accompanied by ICAR/FAO prescriptive nutrient advisory and visual metrics.")
    ]

    for i, (stitle, sdesc) in enumerate(steps):
        y = 110 + i * 75
        box = s6.Shapes.AddShape(1, 50, y, 865, 65)
        box.Fill.Solid()
        box.Fill.ForeColor.RGB = c_card_bg
        box.Line.ForeColor.RGB = c_border

        badge = s6.Shapes.AddShape(1, 65, y + 15, 34, 34)
        badge.Fill.Solid()
        badge.Fill.ForeColor.RGB = c_emerald
        badge.Line.Visible = False
        p = badge.TextFrame.TextRange
        p.Text = f"{i+1}"
        p.Font.Size = 14
        p.Font.Bold = True
        p.Font.Color.RGB = c_white

        tb = s6.Shapes.AddTextbox(1, 115, y + 10, 780, 50)
        p = tb.TextFrame.TextRange
        p.Text = f"{stitle}\n{sdesc}"
        p.Paragraphs(1).Font.Size = 13.5
        p.Paragraphs(1).Font.Bold = True
        p.Paragraphs(1).Font.Color.RGB = c_navy
        p.Paragraphs(2).Font.Size = 11.5
        p.Paragraphs(2).Font.Color.RGB = c_text_muted

    # ==========================================
    # SLIDE 7: EXPERIMENTAL RESULTS & BENCHMARK
    # ==========================================
    s7 = pres.Slides.Add(7, 12)
    set_slide_bg(s7)
    add_header(s7, "Experimental Results & Model Evaluation", "Empirical Evaluation")

    # Table on left
    t_shape7 = s7.Shapes.AddTable(4, 5, 50, 110, 480, 180)
    t7 = t_shape7.Table
    col_w = [140, 85, 85, 85, 85]
    for c_i, w in enumerate(col_w):
        t7.Columns(c_i + 1).Width = w

    eval_data = [
        ["Model Architecture", "Accuracy", "Precision", "Recall", "F1-Score"],
        ["K-Nearest Neighbors", "100.0%", "1.0000", "1.0000", "1.0000"],
        ["Random Forest", "99.44%", "0.9945", "0.9944", "0.9944"],
        ["Decision Tree", "96.94%", "0.9702", "0.9694", "0.9696"]
    ]

    for r_idx, row in enumerate(eval_data):
        for c_idx, val in enumerate(row):
            cell = t7.Cell(r_idx + 1, c_idx + 1)
            cell.Shape.TextFrame.TextRange.Text = val
            p = cell.Shape.TextFrame.TextRange
            p.Font.Name = "Calibri"
            if r_idx == 0:
                cell.Shape.Fill.Solid()
                cell.Shape.Fill.ForeColor.RGB = c_navy
                p.Font.Size = 10.5
                p.Font.Bold = True
                p.Font.Color.RGB = c_white
            else:
                cell.Shape.Fill.Solid()
                cell.Shape.Fill.ForeColor.RGB = c_card_bg if r_idx % 2 == 1 else 0xF1F5F9
                p.Font.Size = 10
                p.Font.Color.RGB = c_text_dark
                if r_idx == 1:
                    p.Font.Bold = True
                    p.Font.Color.RGB = c_emerald

    # Note card on left
    bot_card = s7.Shapes.AddShape(1, 50, 310, 480, 180)
    bot_card.Fill.Solid()
    bot_card.Fill.ForeColor.RGB = c_card_bg
    bot_card.Line.ForeColor.RGB = c_border
    tb_bot = s7.Shapes.AddTextbox(1, 65, 320, 450, 160)
    p = tb_bot.TextFrame.TextRange
    p.Text = "Champion Architecture Selection:\n\n- K-Nearest Neighbors (k=5, Euclidean metric) achieved optimal separation across all test splits due to cohesive cluster geometry in normalized 8D feature space.\n- Random Forest verified strong non-linear split resilience (F1 = 0.9944).\n- The serialized pipeline preserves the exact scaler statistics for zero-drift field deployment."
    p.Font.Size = 11.5
    p.Font.Name = "Calibri"
    p.Font.Color.RGB = c_text_dark
    p.Lines(1).Font.Bold = True
    p.Lines(1).Font.Color.RGB = c_navy

    # Confusion matrix on right
    if os.path.exists(cm_path):
        s7.Shapes.AddPicture(cm_path, 555, 110, 360, 380)

    # ==========================================
    # SLIDE 8: SECURITY HARDENING & ROBUSTNESS
    # ==========================================
    s8 = pres.Slides.Add(8, 12)
    set_slide_bg(s8)
    add_header(s8, "Security Hardening & Production Robustness", "Secure ML Engineering")

    sec_cards = [
        ("CWE-502 Deserialization Defense", "Standard pickle/joblib files can execute arbitrary Python bytecode when loaded.\n\nSoil-Sense generates a SHA-256 hash at training time. At runtime, the hash is recomputed before model unpickling. Tampered files are rejected with a SecurityException."),
        ("Strict Schema Boundaries (Pydantic)", "Prevents prompt injection, type confusion, and physical impossibilities (e.g. negative nitrogen or pH 18).\n\nEnforces valid ranges on all 8 parameters before inference, rejecting malformed HTTP or CSV payloads."),
        ("Zero C: Drive Bloat Architecture", "Implemented custom cache redirection (pip cache-dir -> D:\\pip-cache, TEMP -> D:\\temp).\n\nEnsures zero footprint expansion on resource-constrained host machine system drives."),
        ("Defensive Preprocessing Pipelines", "Prevents test-set data leakage by tightly binding StandardScaler parameters inside Scikit-Learn Pipeline instances.\n\nEvaluation statistics reflect true generalization performance.")
    ]

    for i, (title, desc) in enumerate(sec_cards):
        x = 50 + (i % 2) * 445
        y = 110 + (i // 2) * 195
        card = s8.Shapes.AddShape(1, x, y, 420, 175)
        card.Fill.Solid()
        card.Fill.ForeColor.RGB = c_card_bg
        card.Line.ForeColor.RGB = c_border

        top_line = s8.Shapes.AddShape(1, x, y, 420, 4)
        top_line.Fill.Solid()
        top_line.Fill.ForeColor.RGB = 0x993333 if i == 0 else c_emerald
        top_line.Line.Visible = False

        tb = s8.Shapes.AddTextbox(1, x + 20, y + 15, 380, 150)
        p = tb.TextFrame.TextRange
        p.Text = f"{title}\n\n{desc}"
        p.Paragraphs(1).Font.Size = 15
        p.Paragraphs(1).Font.Bold = True
        p.Paragraphs(1).Font.Color.RGB = c_navy
        p.Paragraphs(3).Font.Size = 11.5
        p.Paragraphs(3).Font.Color.RGB = c_text_muted

    # ==========================================
    # SLIDE 9: EXPECTED OUTCOMES & FUTURE SCOPE
    # ==========================================
    s9 = pres.Slides.Add(9, 12)
    set_slide_bg(s9)
    add_header(s9, "Review Summary & Future Project Roadmap", "Conclusion & Next Steps")

    outcomes = [
        ("Review-I Completed Deliverables", "• Production-ready ML Pipeline with 100% test accuracy on multi-parameter benchmark.\n• Cryptographically secured deployment engine (SHA-256 verification).\n• Real-time responsive Streamlit UI supporting single & batch screening.\n• ICAR/FAO-aligned prescriptive agronomic advisory engine."),
        ("Review-II Roadmap & Enhancements", "• IoT Sensor Integration: Ingest live telemetry from ESP32 / Arduino soil probes via MQTT/REST.\n• Micro-Nutrient Modeling: Expand feature vector to include Zinc, Iron, Boron, and Organic Carbon.\n• Multilingual Regional Support: Localize advisory reports into regional languages (Hindi, Marathi, Telugu, Tamil).\n• Offline Edge Deployment: Quantize pipeline for Raspberry Pi and low-cost agricultural edge gateways.")
    ]

    for i, (title, desc) in enumerate(outcomes):
        x = 50 + i * 445
        card = s9.Shapes.AddShape(1, x, 110, 420, 360)
        card.Fill.Solid()
        card.Fill.ForeColor.RGB = c_card_bg
        card.Line.ForeColor.RGB = c_border

        top_line = s9.Shapes.AddShape(1, x, 110, 420, 5)
        top_line.Fill.Solid()
        top_line.Fill.ForeColor.RGB = c_emerald if i == 0 else c_navy
        top_line.Line.Visible = False

        tb = s9.Shapes.AddTextbox(1, x + 20, 125, 380, 330)
        p = tb.TextFrame.TextRange
        p.Text = f"{title}\n\n{desc}"
        p.Paragraphs(1).Font.Size = 16
        p.Paragraphs(1).Font.Bold = True
        p.Paragraphs(1).Font.Color.RGB = c_navy
        p.Paragraphs(3).Font.Size = 12.5
        p.Paragraphs(3).Font.Color.RGB = c_text_dark

    # Save presentation
    if os.path.exists(output_path):
        os.remove(output_path)
    pres.SaveAs(output_path)
    pres.Close()
    ppt.Quit()
    print("Presentation saved successfully at:", output_path)

if __name__ == "__main__":
    create_presentation()
