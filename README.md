# perfusioncalc-App
Got it. Here's a clean version of your `README.md` file **without emojis** and formatted for professional use:

---

# Perfusion Report Generator

This is a web-based application built using Flask to generate detailed perfusion reports. The app allows perfusionists to input patient data, complete a pre-bypass safety checklist, and generate a clean, printable summary report combining all submitted information.

---

## Features

* Patient demographics and clinical input form
* Pre-Bypass Checklist with critical safety and procedure fields
* Automatic calculations (e.g., BSA, EBV, flow rate)
* Displays adult or pediatric circuit diagram based on selection
* Combined final report page with all relevant details
* Clean, print-ready layout
* Data stored locally in SQLite database

---

## Technologies Used

* Flask (Python web framework)
* HTML5 / CSS3 (Frontend design)
* Jinja2 (Template rendering)
* SQLite (Data storage)
* Python session management

---

## Project Structure

```
project/
│
├── templates/
│   ├── intro.html
│   ├── login.html
│   ├── form.html
│   ├── pre_bypass_checklist.html
│   └── result.html
│
├── static/
│   ├── css/
│   └── images/          # circuit diagrams and logo
│
├── app.py               # main Flask application
├── reports.db           # SQLite database
└── README.md
```

---

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/yourusername/perfusion-report.git
cd perfusion-report
```

2. Install Flask:

```bash
pip install flask
```

3. Run the application:

```bash
python app.py
```

4. Open your browser and go to:

```
http://127.0.0.1:5000
```

---

## Notes

* Ensure all fields in the form and checklist are completed before submission.
* The app uses session-based transitions to pass data across multiple steps.
* Circuit diagram changes based on whether the patient is adult or pediatric.
* The final report is generated based on actual submitted data only.

---

## Future Improvements

* PDF generation for printed reports
* Email integration for sending reports
* User authentication with roles (perfusionist, admin)
* Export to Excel or CSV formats

---

## License

This project is open-source and available under the MIT License.

---


