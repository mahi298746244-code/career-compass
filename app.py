from flask import Flask, render_template, request, redirect,session
print("Starting the application...")
from models.db import get_db_connection
import sqlite3

app = Flask(__name__)

app.secret_key = "career_compass_secret"

def init_db():
    conn = sqlite3.connect("career_portal.db")

    with open("database/schema.sql") as f:
        conn.executescript(f.read())

    conn.close()

#init_db()

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        print("register button clicked")

        full_name = request.form['full_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        if password != confirm_password:
            return "Passwords do not match!"

        conn = get_db_connection()

        conn.execute(
            '''
            INSERT INTO users
            (full_name, email, phone_number, password, role)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (full_name, email, phone_number, password, role)
        )

        conn.commit()
        conn.close()

        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        ).fetchone()

        conn.close()

        if user:
            session['user_name'] = user['full_name']
            session['email'] = user['email']
            session['role'] = user['role']
            return redirect('/dashboard')

        return "Invalid Email or Password"

    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if 'user_name' not in session:
        return redirect('/login')

    return render_template(
        'dashboard.html',
        name=session['user_name']
    )

@app.route('/recommendation')
def recommendation_page():
    return render_template('recommendation.html')


@app.route('/recommendation/<interest>')
def recommendation(interest):

    recommendations = {

        "ai": [
            "AI Engineer",
            "Machine Learning Engineer",
            "Data Scientist"
        ],

        "data-science": [
            "Data Scientist",
            "Data Analyst",
            "Business Analyst"
        ],

        "web-development": [
            "Frontend Developer",
            "Backend Developer",
            "Full Stack Developer"
        ],

        "cyber-security": [
            "Cyber Security Analyst",
            "SOC Analyst",
            "Ethical Hacker"
        ],

        "ui-ux": [
            "UI Designer",
            "UX Designer",
            "Product Designer"
        ],

        "digital-marketing": [
            "SEO Specialist",
            "Digital Marketer",
            "Content Strategist"
        ]
    }

    careers = recommendations.get(interest, [])

    return render_template(
        "recommendation.html",
        careers=careers,
        interest=interest
    )

@app.route('/profile')
def profile():

    if 'user_name' not in session:
        return redirect('/login')

    return render_template(
        'profile.html',
        name=session['user_name'],
        email=session['email'],
        role=session['role']
    )

@app.route('/career/<career_name>')
def career_details(career_name):
    career_data = {
        "AI Engineer": {
            "salary": "₹10 - 25 LPA",
            "skills": "Python, TensorFlow, Machine Learning",
            "companies": "Google, Microsoft, Amazon"
        },
        "Machine Learning Engineer": {
            "salary": "₹12 - 30 LPA",
            "skills": "Python, Deep Learning, PyTorch",
            "companies": "Meta, Google, NVIDIA"
        },
        "Data Scientist": {
            "salary": "₹8 - 20 LPA",
            "skills": "Python, SQL, Statistics",
            "companies": "Netflix, Microsoft, IBM"
        },
        "Frontend Developer": {
            "salary": "₹5 - 15 LPA",
            "skills": "HTML, CSS, JavaScript, React",
            "companies": "Google, Infosys, TCS"
        },
        "Backend Developer": {
            "salary": "₹6 - 18 LPA",
            "skills": "Python, Flask, SQL",
            "companies": "Amazon, IBM, Accenture"
        },
        "Full Stack Developer": {
            "salary": "₹8 - 20 LPA",
            "skills": "HTML, CSS, JavaScript, Flask",
            "companies": "Microsoft, Zoho, Oracle"
        },
        "Cyber Security Analyst": {
            "salary": "₹6 - 15 LPA",
            "skills": "Network Security, Linux, SIEM",
            "companies": "Cisco, Wipro, Deloitte"
        },
        "SOC Analyst": {
            "salary": "₹5 - 12 LPA",
            "skills": "Incident Response, Splunk, Monitoring",
            "companies": "IBM, EY, KPMG"
        },
        "Ethical Hacker": {
            "salary": "₹8 - 20 LPA",
            "skills": "Penetration Testing, Kali Linux, Networking",
            "companies": "Infosys, Deloitte, TCS"
        },
        "Data Analyst": {
            "salary": "₹5 - 12 LPA",
            "skills": "Excel, SQL, Power BI",
            "companies": "Amazon, Flipkart, Accenture"
        },
        "Business Analyst": {
            "salary": "₹6 - 15 LPA",
            "skills": "SQL, Excel, Communication",
            "companies": "Deloitte, Capgemini, IBM"
        },
        "UI Designer": {
            "salary": "₹4 - 12 LPA",
            "skills": "Figma, Adobe XD, Design Systems",
            "companies": "Adobe, Swiggy, Zomato"
        },
        "UX Designer": {
            "salary": "₹6 - 18 LPA",
            "skills": "User Research, Wireframing, Figma",
            "companies": "Google, Adobe, Microsoft"
        },
        "Product Designer": {
            "salary": "₹8 - 22 LPA",
            "skills": "Figma, UX Research, Prototyping",
            "companies": "Meta, Google, Airbnb"
        },
        "SEO Specialist": {
            "salary": "₹4 - 10 LPA",
            "skills": "SEO, Google Analytics, Content Marketing",
            "companies": "HubSpot, WebFX, Neil Patel Digital"
        },
        "Digital Marketer": {
            "salary": "₹5 - 15 LPA",
            "skills": "SEO, Social Media, Ads",
            "companies": "Google, Amazon, Flipkart"
        },
        "Content Strategist": {
            "salary": "₹5 - 12 LPA",
            "skills": "Content Writing, SEO, Analytics",
            "companies": "HubSpot, Adobe, Canva"
        }
    }

    career = career_data.get(career_name)

    if not career:
        career = {
            "salary": "Coming Soon",
            "skills": "Coming Soon",
            "companies": "Coming Soon"
        }

    return render_template(
        "career_details.html",
        career_name=career_name,
        career=career
    )


@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

@app.route('/')
def home():
    return render_template('index.html')

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
