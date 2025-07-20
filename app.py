from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
# IMPORTANT: Change this to a strong, random key in production!
# You can generate a good key with: import os; os.urandom(24)
app.secret_key = 'your_secret_key_here'

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    patient_name = db.Column(db.String(50))
    patient_id = db.Column(db.String(50))
    age = db.Column(db.String(10))
    sex = db.Column(db.String(10))
    perfusionist_name = db.Column(db.String(50))
    patient_type = db.Column(db.String(20))
    height = db.Column(db.String(10))
    weight = db.Column(db.String(10))
    hemoglobin = db.Column(db.String(10))
    diagnosis = db.Column(db.String(100))
    surgery_type = db.Column(db.String(100))
    nyha_class = db.Column(db.String(10))
    comorbidities = db.Column(db.String(100))
    preop_creatinine = db.Column(db.String(10))
    preop_inr = db.Column(db.String(10))
    preop_hematocrit = db.Column(db.String(10))
    notes = db.Column(db.Text)
    # This column will store a JSON string of all combined inputs, calculated values, and checklist data
    all_report_data = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('intro'))

@app.route('/intro')
def intro():
    return render_template('intro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # IMPORTANT: In a real application, never hardcode credentials like this.
        # Use a proper user management system with hashed passwords.
        if request.form['username'] == 'vasudha' and request.form['password'] == '7995315749':
            session['logged_in'] = True
            return redirect(url_for('form'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/form')
def form():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('form.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    form_data = request.form.to_dict()
    patient_type = form_data.get("patient_type", "").lower()

    # Initialize all calculated values to 0.0 or sensible defaults
    bsa = ebv = avg_blood_flow = flow_rate = rbc_volume = cardioplegia_dosage = 0.0

    try:
        height = float(form_data.get("height", 0))
        weight = float(form_data.get("weight", 0))
        # hemoglobin = float(form_data.get("hemoglobin", 0)) # Not used in these specific calculations
        hematocrit = float(form_data.get("preop_hematocrit", 0))
        sex = form_data.get("sex", "male").lower()

        bsa = round(0.007184 * (height ** 0.725) * (weight ** 0.425), 2)
        ebv = round(weight * (70 if sex == 'male' else 65), 2)
        avg_blood_flow = round(bsa * 2.6, 2)
        # Convert L/min to ml/min for flow_rate display if needed
        flow_rate = round(avg_blood_flow * 1000 * 1.2, 2)
        rbc_volume = round((hematocrit / 100) * ebv, 2)
        cardioplegia_dosage = round(weight * 4, 2)
    except ValueError as e:
        # Log the error for debugging purposes
        print(f"Calculation error in submit_form: {e}. Some numeric fields might be empty or invalid.")
        # bsa, ebv, etc. remain 0.0 as initialized

    calculated = {
        "BSA": f"{bsa} m²", # Use proper Unicode for m²
        "EBV": f"{ebv} ml",
        "AvgBloodFlow": f"{avg_blood_flow} L/min",
        "FlowRate": f"{flow_rate} ml/min",
        "Hematocrit": f"{form_data.get('preop_hematocrit', 0)} %", # Display original hematocrit
        "RBCVolume": f"{rbc_volume} ml",
        "CardioplegiaDosage": f"{cardioplegia_dosage} ml"
    }

    circuit_image_filename = "adult_circuit.png" if patient_type == "adult" else "pediatric_circuit.png"
    # Store the full URL for the circuit image for easy use in templates
    session['circuit_image_path'] = url_for('static', filename=circuit_image_filename)

    # Combine all data from the initial form and calculated values into a single dictionary
    all_data_for_session = {
        **form_data, # Unpack all data from the initial form
        **calculated, # Unpack all calculated results
        "circuit_image_filename": circuit_image_filename, # Store just the filename if needed
        "date": datetime.now().strftime("%Y-%m-%d"), # Add current date
        "perfusionist_name": "Vasudha" # Add perfusionist name
    }

    # Store this comprehensive dictionary in the session
    session['all_report_data'] = all_data_for_session

    # Redirect to the pre-bypass checklist page
    return redirect(url_for('pre_bypass_checklist'))

@app.route('/pre_bypass_checklist', methods=['GET', 'POST'])
def pre_bypass_checklist():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Retrieve the comprehensive data from session to pre-populate the form on GET request
    initial_form_data = session.get('all_report_data', {})

    if request.method == 'POST':
        # Get checklist and other pre-bypass specific data from the submitted form
        checklist_and_prebypass_data = request.form.to_dict()

        # Update the comprehensive session data with the new checklist and pre-bypass info
        # This merges the new data into the existing patient and calculated data
        session['all_report_data'].update(checklist_and_prebypass_data)

        # Now, create and save the complete report to the database
        final_report_data = session['all_report_data']

        report = Report(
            date=final_report_data.get("date"), # Use the date set in submit_form
            patient_name=final_report_data.get("patient_name"),
            patient_id=final_report_data.get("patient_id"),
            age=final_report_data.get("age"),
            sex=final_report_data.get("sex"),
            perfusionist_name=final_report_data.get("perfusionist_name"),
            patient_type=final_report_data.get("patient_type"),
            height=final_report_data.get("height"),
            weight=final_report_data.get("weight"),
            hemoglobin=final_report_data.get("hemoglobin"),
            diagnosis=final_report_data.get("diagnosis"),
            surgery_type=final_report_data.get("surgery_type"),
            nyha_class=final_report_data.get("nyha_class"),
            comorbidities=final_report_data.get("comorbidities"),
            preop_creatinine=final_report_data.get("preop_creatinine"),
            preop_inr=final_report_data.get("preop_inr"),
            preop_hematocrit=final_report_data.get("preop_hematocrit"),
            notes=final_report_data.get("notes"),
            # Store all combined data as JSON in the database's all_report_data column
            all_report_data=json.dumps(final_report_data)
        )
        db.session.add(report)
        db.session.commit()

        # Store the ID of the newly created report (optional, but useful for direct access)
        session['last_report_id'] = report.id

        # Redirect to the final result page
        return redirect(url_for('final_result'))

    # For GET request, render the checklist form and pass initial patient data for display
    return render_template('pre_bypass_checklist.html', initial_form_data=initial_form_data)


@app.route('/final_result', methods=['GET']) # Changed to GET, as it's a display page after a POST redirect
def final_result():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Retrieve the comprehensive data from the session
    # This dictionary now contains all patient, calculated, and checklist data
    final_report_data = session.get('all_report_data', {})
    circuit_image_path = session.get('circuit_image_path', "")

    # Pass the single comprehensive dictionary and the image path to the template
    return render_template(
        'result.html',
        report_data=final_report_data, # This now holds all patient, calculated, and checklist data
        circuit_image_path=circuit_image_path
    )

if __name__ == '__main__':
    app.run(debug=True)
