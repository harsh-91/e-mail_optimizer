# core/imap/analyzer.py

from imapclient import IMAPClient
import pyzmail
from rich import print
import os

def fetch_latest_email(email, app_password, subject_filter=None):
    try:
        with IMAPClient('imap.gmail.com', ssl=True) as client:
            client.login(email, app_password)
            client.select_folder('INBOX', readonly=True)

            messages = client.search(['FROM', email] if not subject_filter else ['SUBJECT', subject_filter])
            if not messages:
                return "[red]✗ No matching emails found[/red]"

            latest_uid = messages[-1]
            raw_msg = client.fetch([latest_uid], ['BODY[]', 'FLAGS'])[latest_uid][b'BODY[]']
            msg = pyzmail.PyzMessage.factory(raw_msg)

            headers = msg.get_decoded_header('Authentication-Results')
            received_spf = msg.get_decoded_header('Received-SPF')
            return_path = msg.get_decoded_header('Return-Path')
            dkim = msg.get_decoded_header('DKIM-Signature')
            subject = msg.get_subject()
            sender = msg.get_addresses('from')[0][1]

            result = f"""
[bold]Subject:[/bold] {subject}
[bold]From:[/bold] {sender}
[bold]Return-Path:[/bold] {return_path}

[bold]Received-SPF:[/bold]
{received_spf}

[bold]Authentication-Results:[/bold]
{headers}

[bold]DKIM-Signature:[/bold]
{dkim[:100]}...""" if dkim else "No DKIM signature found."

            return result.strip()

    except Exception as e:
        return f"[red]✗ Error reading inbox: {e}[/red]"
