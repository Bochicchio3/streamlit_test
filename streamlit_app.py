import streamlit as st
import json
import pandas as pd

# Load tickets
with open('disagreements.json', 'r') as file:
    tickets = json.load(file)

st.title("📝 Abstract Screening - Disagreement Review")

if 'comments' not in st.session_state:
    st.session_state['comments'] = {}

for idx, ticket in enumerate(tickets, 1):
    with st.expander(f"Ticket {idx}: {ticket['Title']}"):
        st.write(f"**Abstract:** {ticket['Abstract']}")
        st.write(f"**Human Result:** {ticket['Human_Result']}")
        st.write(f"**LLM Result:** {ticket['LLM_Result']}")
        st.write(f"**Summary:** {ticket['Disagreement_Summary']}")

        comment = st.text_area(
            f"🗒️ **Comment / Correction for Ticket {idx}:**",
            value=st.session_state['comments'].get(idx, ""),
            key=f"comment_{idx}"
        )

        st.session_state['comments'][idx] = comment

# Save comments button
if st.button("💾 Save all comments"):
    comments_df = pd.DataFrame([
        {
            "Title": t["Title"],
            "Human_Result": t["Human_Result"],
            "LLM_Result": t["LLM_Result"],
            "Disagreement_Summary": t["Disagreement_Summary"],
            "Comment": st.session_state['comments'].get(idx + 1, "")
        } for idx, t in enumerate(tickets)
    ])

    comments_df.to_csv("ticket_comments.csv", index=False)
    st.success("✅ Comments saved successfully!")
