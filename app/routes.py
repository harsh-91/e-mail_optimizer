# app/routes.py

from flask import Blueprint, render_template, request, redirect, session
from core.diagnostics import spf_checker, dkim_checker, dmarc_checker
from core.formatter import email_template_formatter, send_email as se
from core.imap.analyzer import fetch_latest_email

main = Blueprint('main', __name__)
client_bp = Blueprint('client', __name__)

# Homepage: Diagnostic Checks
@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        domain = session.get("domain") or request.form.get("domain")
        selector = session.get("selector") or request.form.get("selector")

        spf = spf_checker.get_spf_record(domain)
        dkim = dkim_checker.get_dkim_record(domain, selector)
        dmarc = dmarc_checker.get_dmarc_record(domain)

        return render_template("results.html", domain=domain, spf=spf, dkim=dkim, dmarc=dmarc)
    
    return render_template("index.html")

# Client Setup
@client_bp.route("/setup", methods=["GET", "POST"])
def setup():
    if request.method == "POST":
        session["domain"] = request.form["domain"]
        session["selector"] = request.form["selector"]
        session["gmail"] = request.form["gmail"]
        session["password"] = request.form["password"]
        return redirect("/")
    return render_template("client_setup.html")

# Analyze Received Email Headers
@main.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        gmail = request.form.get("email") or session.get("gmail")
        password = request.form.get("password") or session.get("password")
        subject = request.form.get("subject")

        result = fetch_latest_email(gmail, password, subject)
        return render_template("analyze_result.html", result=result)

    return render_template("analyze_form.html")

# Send Authenticated Email
@main.route("/email", methods=["GET", "POST"])
def email():
    if request.method == "POST":
        name = request.form.get("name")
        itinerary = request.form.get("itinerary")
        price = request.form.get("price")
        to_email = request.form.get("to")
        subject = request.form.get("subject")

        sender_email = request.form.get("sender_email") or session.get("gmail")
        app_password = request.form.get("app_password") or session.get("password")

        html = email_template_formatter.generate_email_html(name, itinerary, price)
        se.send_email(to_email, subject, html, sender_email, app_password)

        return render_template("email_preview.html", html=html)

    return render_template("email_preview.html")
