import streamlit as st
import json
import pandas as pd
import os

st.title("📝 Abstract Screening - Disagreement Review")

# Load CSV from local path
csv_path = os.path.join("data", "articles_output.csv")  # Adjust if needed

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df = df[df['Agreement'] == 'Disagree']  # Only show disagreements

    tickets = []
    for _, row in df.iterrows():
        tickets.append({
            "Title": row.get("title", ""),
            "Abstract": row.get("abstract", ""),
            "Human_Result": row.get("Benedetta_Result", ""),
            "LLM_Result": row.get("LLM_Result", ""),
            "Disagreement_Summary": row.get("LLM_Notes", ""),
            "LLM_Reasoning": row.get("LLM_Reasoning", ""),
            "Agreement": row.get("Agreement", "")
        })
else:
    st.error(f"CSV file not found at {csv_path}")
    st.stop()

if 'comments' not in st.session_state:
    st.session_state['comments'] = {}

for idx, ticket in enumerate(tickets, 1):
    with st.expander(f"Ticket {idx}: {ticket['Title']}"):
        show_abstract = st.checkbox(f"🔍 Show Abstract for Ticket {idx}", key=f"show_abstract_{idx}")
        if show_abstract:
            st.write(f"**Abstract:** {ticket['Abstract']}")

        st.write(f"**Human Decision (Benedetta):** {ticket['Human_Result']}")
        st.write(f"**LLM Result:** {ticket['LLM_Result']}")
        st.write(f"**Agreement:** {ticket['Agreement']}")
        st.write(f"**Summary / Notes:** {ticket['Disagreement_Summary']}")
        st.write(f"**LLM Reasoning:** {ticket['LLM_Reasoning']}")

        comment = st.text_area(
            f"🗒️ **Comment / Correction for Ticket {idx}:**",
            value=st.session_state['comments'].get(idx, ""),
            key=f"comment_{idx}"
        )

        st.session_state['comments'][idx] = comment

# Save comments
comments_json = [
    {
        "Title": t["Title"],
        "Human_Result": t["Human_Result"],
        "LLM_Result": t["LLM_Result"],
        "Agreement": t["Agreement"],
        "Disagreement_Summary": t["Disagreement_Summary"],
        "LLM_Reasoning": t["LLM_Reasoning"],
        "Comment": st.session_state['comments'].get(idx + 1, "")
    } for idx, t in enumerate(tickets)
]

st.download_button(
    label="⬇️ Download Comments as JSON",
    data=json.dumps(comments_json, indent=2),
    file_name="ticket_comments.json",
    mime="application/json"
)
