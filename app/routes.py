# app/routes.py

from flask import Blueprint, render_template, request
from core.diagnostics import spf_checker, dkim_checker, dmarc_checker
from core.formatter import email_template_formatter, send_email as se

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        domain = request.form.get("domain")
        selector = request.form.get("selector")

        spf = spf_checker.get_spf_record(domain)
        dkim = dkim_checker.get_dkim_record(domain, selector)
        dmarc = dmarc_checker.get_dmarc_record(domain)

        return render_template("results.html", domain=domain, spf=spf, dkim=dkim, dmarc=dmarc)
    return render_template("index.html")

from core.imap.analyzer import fetch_latest_email

@main.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        gmail = request.form.get("email")
        password = request.form.get("password")
        subject = request.form.get("subject")

        result = fetch_latest_email(gmail, password, subject)
        return render_template("analyze_result.html", result=result)

    return render_template("analyze_form.html")

@main.route("/email", methods=["GET", "POST"])
def email():
    if request.method == "POST":
        name = request.form.get("name")
        itinerary = request.form.get("itinerary")
        price = request.form.get("price")
        to_email = request.form.get("to")
        subject = request.form.get("subject")

        # New fields
        sender_email = request.form.get("sender_email")
        app_password = request.form.get("app_password")

        html = email_template_formatter.generate_email_html(name, itinerary, price)

        # Use temporary credentials
        se.send_email(to_email, subject, html, sender_email, app_password)

        return render_template("email_preview.html", html=html)

    return render_template("email_preview.html")
