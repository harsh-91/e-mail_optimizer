import tkinter as tk
from tkinter import messagebox
from diagnostics import spf_checker, dkim_checker, dmarc_checker
from formatter import email_template_formatter, send_email

def check_all():
    domain = domain_entry.get()
    selector = selector_entry.get()

    spf_result = spf_checker.get_spf_record(domain)
    dkim_result = dkim_checker.get_dkim_record(domain, selector)
    dmarc_result = dmarc_checker.get_dmarc_record(domain)

    results = f"""
--- SPF Result ---
{spf_result}

--- DKIM Result ---
{dkim_result}

--- DMARC Result ---
{dmarc_result}
"""
    messagebox.showinfo("Authentication Results", results)

def create_email():
    name = name_entry.get()
    itinerary = itinerary_entry.get("1.0", tk.END).strip()
    price = price_entry.get()

    html = email_template_formatter.generate_email_html(name, itinerary, price)
    email_template_formatter.save_email_to_file(html)
    messagebox.showinfo("Email Generated", "Email preview saved as 'email_preview.html'.")

def send_it():
    recipient = to_entry.get()
    subject = subject_entry.get()
    try:
        html = open("email_preview.html", "r", encoding="utf-8").read()
        send_email.send_email(recipient, subject, html)
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("Email Delivery Optimizer")
app.geometry("600x600")

# ========== Instructions ==========
instructions = tk.Label(app, text="🧠 Email Setup Instructions", font=("Helvetica", 12, "bold"))
instructions.grid(row=0, column=0, columnspan=2, pady=4)

inst_text = tk.Label(app, justify="left", anchor="w", wraplength=580, text="""
1. Enter the domain and DKIM selector to check SPF, DKIM, and DMARC.
   - SPF ensures your domain is allowed to send emails.
   - DKIM ensures emails are signed and not tampered with.
   - DMARC tells mail providers how to handle failures.
2. Use the lower section to generate a quote/itinerary email.
3. You must create an App Password in Gmail if 2FA is enabled.
""", fg="gray")
inst_text.grid(row=1, column=0, columnspan=2)

# ========== Auth Section ==========
tk.Label(app, text="Domain (e.g. example.com):").grid(row=2, column=0, sticky="e")
domain_entry = tk.Entry(app, width=40)
domain_entry.grid(row=2, column=1)

tk.Label(app, text="DKIM Selector (e.g. default, google, 20230601):").grid(row=3, column=0, sticky="e")
selector_entry = tk.Entry(app, width=40)
selector_entry.grid(row=3, column=1)

tk.Button(app, text="Check SPF / DKIM / DMARC", command=check_all, bg="#cce5ff").grid(row=4, column=0, columnspan=2, pady=10)

# ========== Email Generator ==========
tk.Label(app, text="Customer Name:").grid(row=5, column=0, sticky="e")
name_entry = tk.Entry(app, width=40)
name_entry.grid(row=5, column=1)

tk.Label(app, text="Itinerary Details (flight/train info, etc.):").grid(row=6, column=0, sticky="e")
itinerary_entry = tk.Text(app, height=4, width=30)
itinerary_entry.grid(row=6, column=1)

tk.Label(app, text="Total Price (INR):").grid(row=7, column=0, sticky="e")
price_entry = tk.Entry(app, width=40)
price_entry.grid(row=7, column=1)

tk.Button(app, text="Generate Email HTML", command=create_email, bg="#d4edda").grid(row=8, column=0, columnspan=2, pady=10)

# ========== Send Email ==========
tk.Label(app, text="Recipient Email:").grid(row=9, column=0, sticky="e")
to_entry = tk.Entry(app, width=40)
to_entry.grid(row=9, column=1)

tk.Label(app, text="Subject Line:").grid(row=10, column=0, sticky="e")
subject_entry = tk.Entry(app, width=40)
subject_entry.grid(row=10, column=1)

tk.Button(app, text="Send Email", command=send_it, bg="#f8d7da").grid(row=11, column=0, columnspan=2, pady=10)

app.mainloop()
