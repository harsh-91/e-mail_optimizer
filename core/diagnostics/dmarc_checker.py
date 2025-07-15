# diagnostics/dmarc_checker.py

import dns.resolver
from rich import print

def get_dmarc_record(domain: str) -> str:
    try:
        record_name = f"_dmarc.{domain}"
        answers = dns.resolver.resolve(record_name, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                decoded = txt_string.decode("utf-8")
                if decoded.startswith("v=DMARC1"):
                    return f"[green]✓ DMARC record for {domain}:[/green]\n{decoded}"
        return f"[yellow]No DMARC record found for {domain}[/yellow]"
    except dns.resolver.NXDOMAIN:
        return f"[red]✗ No DMARC record found for {domain} (NXDOMAIN)[/red]"
    except Exception as e:
        return f"[red]✗ Error fetching DMARC for {domain}: {e}[/red]"

if __name__ == "__main__":
    domain = input("Enter domain to check DMARC: ").strip()
    result = get_dmarc_record(domain)
    print(result)
