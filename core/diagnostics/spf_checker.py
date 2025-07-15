# diagnostics/spf_checker.py

import dns.resolver
from rich import print

def get_spf_record(domain: str) -> str:
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                decoded = txt_string.decode("utf-8")
                if decoded.startswith("v=spf1"):
                    return decoded
        return "No SPF record found"
    except Exception as e:
        return f"[red]Error fetching SPF for {domain}: {e}[/red]"

if __name__ == "__main__":
    domain = input("Enter domain to check SPF for: ").strip()
    spf = get_spf_record(domain)
    print(f"[bold green]SPF Record for {domain}:[/bold green] {spf}")
