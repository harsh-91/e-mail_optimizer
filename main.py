# main.py

import argparse
from diagnostics import spf_checker, dkim_checker, dmarc_checker
from formatter import email_template_formatter, send_email
from pathlib import Path
from rich import print

def run_checks(domain, selector=None):
    print(f"[bold cyan]\nRunning Email Authentication Checks for [u]{domain}[/u][/bold cyan]")

    print("\n[bold]SPF Check:[/bold]")
    print(spf_checker.get_spf_record(domain))

    print("\n[bold]DKIM Check:[/bold]")
    if selector:
        print(dkim_checker.get_dkim_record(domain, selector))
    else:
        print("[yellow]No DKIM selector provided. Skipping DKIM check.[/yellow]")

    print("\n[bold]DMARC Check:[/bold]")
    print(dmarc_checker.get_dmarc_record(domain))

def generate_email(customer, itinerary, price):
    html = email_template_formatter.generate_email_html(customer, itinerary, price)
    file_path = email_template_formatter.save_email_to_file(html)
    print(f"[green]✓ HTML email saved to {file_path.absolute()}[/green]")
    return html

def send(html, to, subject):
    plain = "This is a travel itinerary. Please view this in an HTML-enabled email client."
    success = send_email.send_email(to, subject, html, plain)
    if not success:
        print("[red]Email sending failed.[/red]")

def main():
    parser = argparse.ArgumentParser(description="Email Delivery Optimizer Tool")
    parser.add_argument("--domain", help="Domain to check SPF/DKIM/DMARC")
    parser.add_argument("--selector", help="DKIM selector (optional)")
    parser.add_argument("--check", action="store_true", help="Run SPF/DKIM/DMARC checks")
    parser.add_argument("--generate-email", action="store_true", help="Generate HTML email")
    parser.add_argument("--send-email", action="store_true", help="Send the generated email")
    parser.add_argument("--to", help="Recipient email")
    parser.add_argument("--subject", help="Email subject line")

    args = parser.parse_args()

    if args.check and args.domain:
        run_checks(args.domain, args.selector)

    if args.generate_email:
        name = input("Customer Name: ")
        itinerary = input("Itinerary: ")
        price = input("Total Price (e.g., ₹4999): ")
        html = generate_email(name, itinerary, price)
    else:
        html = Path("email_preview.html").read_text(encoding="utf-8") if Path("email_preview.html").exists() else None

    if args.send_email and args.to and args.subject:
        if html:
            send(html, args.to, args.subject)
        else:
            print("[red]No HTML email found to send. Generate first using --generate-email[/red]")

if __name__ == "__main__":
    main()
