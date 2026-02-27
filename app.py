# ----------------------------------------------------------
# 🚀 AI Data Cleaning, Visualization & Report Generator
# Author: Aadhi Kesavan
# ----------------------------------------------------------

import streamlit as st
import pandas as pd
import os, sys
import altair as alt

# ----------------------------------------------------------
# 🔧 Page Configuration
# ----------------------------------------------------------
st.set_page_config(
    page_title="AI Data Analysis Tool",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------------------------
# 🔗 Backend Path
# ----------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from cleaning import clean_data
from visualization import generate_chart
from groq_ai import generate_ai_insights
from report_gen import generate_report

# ----------------------------------------------------------
# 🎨 Sidebar
# ----------------------------------------------------------
st.sidebar.title("📊 AI Data Tool")
st.sidebar.markdown("""
- Upload Dataset  
- Clean Data  
- Visualize  
- Generate AI Report  
""")

# ----------------------------------------------------------
# 🧠 Header
# ----------------------------------------------------------
st.markdown(
    "<h1 style='text-align:center;'>🧠 AI-Powered Data Cleaning & Reporting</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;'>Upload → Clean → Visualize → AI Report</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ----------------------------------------------------------
# 📁 File Upload
# ----------------------------------------------------------
uploaded_file = st.file_uploader(
    "📤 Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
    except:
        df = pd.read_excel(uploaded_file)

    st.subheader("🔍 Raw Dataset Preview")
    st.dataframe(df.head())

    # ------------------------------------------------------
    # 🧼 Clean Data
    # ------------------------------------------------------
    if st.button("🧼 Clean Data"):
        cleaned_df, cleaning_summary = clean_data(df)

        st.success("✅ Data cleaned successfully!")
        st.subheader("📋 Cleaned Data Preview")
        st.dataframe(cleaned_df.head())

        st.session_state["cleaned_df"] = cleaned_df
        st.session_state["summary"] = cleaning_summary

# ----------------------------------------------------------
# 📊 Visualization Section
# ----------------------------------------------------------
if "cleaned_df" in st.session_state:
    st.markdown("---")
    st.subheader("📊 Visualization")

    cleaned_df = st.session_state["cleaned_df"]
    numeric_cols = cleaned_df.select_dtypes(include="number").columns.tolist()

    chart_type = st.selectbox(
        "Select Chart Type",
        ["Histogram", "Scatter", "Bar", "Box"]
    )

    x_col = st.selectbox("Select X-axis column", numeric_cols)
    y_col = None

    if chart_type in ["Scatter", "Bar"]:
        y_col = st.selectbox("Select Y-axis column", numeric_cols)

    if st.button("📈 Visualize"):
        chart = generate_chart(cleaned_df, chart_type, x_col, y_col)
        st.altair_chart(chart, use_container_width=True)

# ----------------------------------------------------------
# 🤖 AI Report Generation
# ----------------------------------------------------------
if "cleaned_df" in st.session_state:
    st.markdown("---")
    st.subheader("🧾 Generate AI Report")

    if st.button("🤖 Generate AI PDF Report"):
        with st.spinner("Analyzing data using Groq AI..."):
            ai_insights = generate_ai_insights(
                st.session_state["summary"],
                st.session_state["cleaned_df"]
            )

            os.makedirs("reports", exist_ok=True)
            report_path = generate_report(
                st.session_state["summary"],
                ai_insights,
                output_file="reports/ai_data_report.pdf"
            )

        st.success("🎉 Report generated successfully!")

        with open(report_path, "rb") as f:
            st.download_button(
                "📄 Download PDF Report",
                f,
                file_name="AI_Data_Report.pdf",
                mime="application/pdf"
            )

# ----------------------------------------------------------
# 👣 Footer
# ----------------------------------------------------------
st.markdown("---")
st.markdown(
    "<center style='color:gray;'>Built by Aadhi Kesavan | Powered by Streamlit & Groq AI</center>",
    unsafe_allow_html=True
)
