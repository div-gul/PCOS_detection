from flask import Flask, request, jsonify
import pickle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file
import os

app = Flask(__name__)

# LOAD MODEL
basic_model = pickle.load(open("basic_model.pkl", "rb"))
adv_model = pickle.load(open("adv_model.pkl", "rb"))
#PDF Generator
def generate_pdf(data, prediction, probability):
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet

    file_path = "report.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    content = []

    # NAME
    name = data.get("name", "Patient")
    content.append(Paragraph(f"<b>{name}</b>", styles['Title']))
    content.append(Spacer(1, 10))

    # BASIC DETAILS
    basic_info = [
        f"Age: {data.get('age','-')}",
        f"Weight: {data.get('weight','-')} kg",
        f"Height: {data.get('height','-')} cm",
        f"BMI: {data.get('bmi','-')}"
    ]

    content.append(Paragraph(" | ".join(basic_info), styles['Normal']))
    content.append(Spacer(1, 10))

    # LINE
    content.append(Paragraph("------------------------------------------------------------", styles['Normal']))
    content.append(Spacer(1, 10))

    # NORMAL RANGES (you can tweak)
    normal_ranges = {
        "cycle": "0 = Regular, 1 = Irregular",
        "cycle_length": "21-35 days",
        "weight_gain": "0 (No), 1 (Yes)",
        "hair_growth": "0 (No), 1 (Yes)",
        "skin_darkening": "0 (No), 1 (Yes)",
        "amh": "1.0 - 4.0 ng/mL",
        "lh": "1.9 - 12.5 IU/L",
        "fsh_lh": "< 2",
        "tsh": "0.4 - 4.0 mIU/L",
        "follicle_r": "1 - 10",
        "follicle_l": "1 - 10",
        "hip": "Varies",
        "weight": "Varies",
        "age": "Varies",
        "bmi": "18.5 - 24.9"
    }

    # LABEL MAP
    label_map = {
        "name": "Name",
        "age": "Age",
        "weight": "Weight",
        "height": "Height",
        "bmi": "BMI",
        "cycle": "Cycle Type",
        "cycle_length": "Cycle Length",
        "weight_gain": "Weight Gain",
        "hair_growth": "Hair Growth",
        "skin_darkening": "Skin Darkening",
        "hip": "Hip Size",
        "amh": "AMH",
        "lh": "LH",
        "fsh_lh": "FSH/LH Ratio",
        "tsh": "TSH",
        "follicle_r": "Follicle (Right)",
        "follicle_l": "Follicle (Left)"
    }

    # TABLE DATA
    table_data = [["Parameter", "Value", "Normal Range"]]

    for key, value in data.items():
        # skip name because already shown at top
        if key == "name":
            continue

        label = label_map.get(key, key)
        normal = normal_ranges.get(key, "-")

        table_data.append([label, str(value), normal])

    table = Table(table_data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
    ]))

    content.append(table)
    content.append(Spacer(1, 15))

    # 🟣 LINE
    content.append(Paragraph("------------------------------------------------------------", styles['Normal']))
    content.append(Spacer(1, 10))

    # 🟣 RESULT
    result = " PCOS Detected " if prediction == 1 else "No PCOS Detected "

    content.append(Paragraph("<b>Result:</b>", styles['Heading2']))
    content.append(Paragraph(result, styles['Normal']))
    content.append(Paragraph(f"Confidence: {round(probability*100,2)}%", styles['Normal']))

    content.append(Spacer(1, 15))

    # 🟣 DISCLAIMER
    content.append(Paragraph(
        "<i>Disclaimer: This is not a medical diagnosis. Please consult a doctor for professional advice.</i>",
        styles['Normal']
    ))

    doc.build(content)
    return file_path
# HOME ROUTE
@app.route('/')
def home():
    return "PCOS Prediction API Running"

# PREDICTION ROUTE
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    try:
        features = [
            float(data['age']),
            float(data['weight']),
            float(data['bmi']),
            float(data['cycle']),
            float(data['cycle_length']),
            float(data['weight_gain']),
            float(data['hair_growth']),
            float(data['skin_darkening']),
            float(data['hip'])
        ]

        prediction = basic_model.predict([features])[0]
        probability = basic_model.predict_proba([features])[0][1]

        
        pdf_path = generate_pdf(data, prediction, probability)
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/predict_adv', methods=['POST'])
def predict_adv():
    data = request.json

    try:
        features = [
            float(data['follicle_r']),
            float(data['follicle_l']),
            float(data['skin_darkening']),
            float(data['hair_growth']),
            float(data['weight_gain']),
            float(data['amh']),
            float(data['cycle_length']),
            float(data['cycle']),
            float(data['weight']),
            float(data['age']),
            float(data['fsh_lh']),
            float(data['bmi']),
            float(data['lh']),
            float(data['hip']),
            float(data['tsh'])
        ]

        prediction = adv_model.predict([features])[0]
        probability = adv_model.predict_proba([features])[0][1]

       
        pdf_path = generate_pdf(data, prediction, probability)
        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)})

# RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)