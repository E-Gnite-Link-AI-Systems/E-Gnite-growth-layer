import streamlit as st
import json

st.title("🚀 E-Gnite Growth Dashboard")

with open("data/leads.json") as f:
    leads = json.load(f)

st.subheader("📊 Leads Data")
st.write(leads)

st.subheader("📈 Summary")

total_leads = len(leads)
high_value = len([l for l in leads if l["revenue"] > 1000])

st.metric("Total Leads", total_leads)
st.metric("Qualified Leads", high_value)
