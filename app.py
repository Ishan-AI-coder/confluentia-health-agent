import streamlit as st
import pandas as pd
from io import StringIO, BytesIO
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Import functions from main.py
from main import route_input, report_analyzer, chart_generator, final_workflow,table_generator

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="Health AI", page_icon="🩺")
st.title("🩺 Health AI Assistant")

# -----------------------------
# Sidebar File Upload
# -----------------------------
st.sidebar.header("📂 Upload Medical Report")
uploaded_file = st.sidebar.file_uploader("Upload a report file", type=["csv", "xlsx", "pdf","webp"])

if uploaded_file:
    st.sidebar.success("✅ File uploaded!")

    # Read file contents
    bytes_data = uploaded_file.getvalue()
    media_type = uploaded_file.type

    table_response=table_generator(bytes_data,media_type)
    st.markdown(table_response)
    
    
    # # Report analysis
    # st.subheader("📑 Report Analysis")
    # report_analyzer_result = report_analyzer(bytes_data, media_type)
    # st.write(report_analyzer_result)

    # Final workflow
    st.subheader("🩺 Final Workflow Result")
    response = final_workflow(bytes_data,media_type)
    st.markdown(response)

    # # -----------------------------
    # # PDF Download Section
    # # -----------------------------
    # def generate_pdf(text: str) -> BytesIO:
    #     buffer = BytesIO()
    #     doc = SimpleDocTemplate(buffer, pagesize=letter)
    #     styles = getSampleStyleSheet()
    #     story = []

    #     for line in text.split("\n"):
    #         if line.strip() == "":
    #             story.append(Spacer(1, 12))
    #         else:
    #             story.append(Paragraph(line, styles["Normal"]))

    #     doc.build(story)
    #     buffer.seek(0)
    #     return buffer

    # pdf_buffer = generate_pdf(response)

    # st.download_button(
    #     label="⬇️ Download Full Report as PDF",
    #     data=pdf_buffer,
    #     file_name="health_report.pdf",
    #     mime="application/pdf"
    # )

    # # Charts (only for CSV/Excel)
    st.subheader("📊 Report Charts")
    chart_code = chart_generator(bytes_data,media_type)
    # st.code(chart_code, language='python')
    chart_lines = chart_code.splitlines()
    if len(chart_lines) > 2:
        chart_code = "\n".join(chart_lines[1:-1])
    else:
        chart_code = ""
    exec(chart_code, {}, {'st': st})


# -----------------------------
# Chat Section
# -----------------------------
st.subheader("💬 Chat with Health AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar", None)):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "🧑"})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    placeholder = st.empty()
    placeholder.chat_message("assistant", avatar="🤖").markdown("_typing..._")

    result, agent_name = route_input(prompt, return_agent=True)

    placeholder.empty()

    agent_avatars = {
        "RachelAgent": "💪",
        "WarrenAgent": "🩺",
        "CarlaAgent": "🥗",
        "AdvikAgent": "📊",
        "NeelAgent": "🧩",
        "RubyAgent": "📌",
    }
    avatar = agent_avatars.get(agent_name, "🤖")

    st.session_state.messages.append({"role": "assistant", "content": result, "avatar": avatar})
    with st.chat_message("assistant", avatar=avatar):
        st.markdown(f"**{agent_name} says:** {result}")
