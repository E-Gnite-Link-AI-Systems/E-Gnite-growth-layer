from qualify import qualify_leads
from score import score_leads
from outreach import generate_outreach
from email_sender import send_email
import time

def run_system():
    # your existing logic here
    pass

leads = [
    {"name": "John", "company": "ABC", "revenue": 2000},
    {"name": "Sarah", "company": "XYZ", "revenue": 500}
]


qualified = qualify_leads(leads)
scored = score_leads(qualified)

best = max(scored, key=lambda x: x["score"])

message = generate_outreach(best)

send_email(best["email"], "Growth Opportunity", message)

print("Lead:", best["name"])
print("Score:", best["score"])
print("Message:", message)


