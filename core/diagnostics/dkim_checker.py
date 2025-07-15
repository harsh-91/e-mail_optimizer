# diagnostics/dkim_checker.py

import dns.resolver
from rich import print

def get_dkim_record(domain: str, selector: str) -> str:
    record_name = f"{selector}._domainkey.{domain}"
    try:
        answers = dns.resolver.resolve(record_name, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                decoded = txt_string.decode("utf-8")
                return f"[bold green]DKIM Record:[/bold green] {decoded}"
        return f"[yellow]No DKIM record found for {record_name}[/yellow]"
    except dns.resolver.NXDOMAIN:
        return f"[red]NXDOMAIN: {record_name} not found[/red]"
    except Exception as e:
        return f"[red]Error fetching DKIM: {e}[/red]"

if __name__ == "__main__":
    domain = input("Enter domain (e.g., google.com): ").strip()
    selector = input("Enter DKIM selector (e.g., google, default): ").strip()
    result = get_dkim_record(domain, selector)
    print(result)
