# streamlit_app_v2.py

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Clinical Workflow Dashboard", layout="wide")
st.title("🏥 Clinical Workflow Intelligence")

ehr_file = st.file_uploader("📤 Upload EHR/EMR CSV", type="csv")
claims_file = st.file_uploader("📤 Upload Claims CSV", type="csv")

if ehr_file and claims_file:
    ehr = pd.read_csv(ehr_file, parse_dates=["Admission_Date", "Discharge_Date", "DOB"])
    claims = pd.read_csv(claims_file, parse_dates=["Service_Date"])

    ##### 1. Interactive Dashboard ######
    st.header("📊 Interactive Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Patients", len(ehr["Patient_ID"].unique()))

    with col2:
        st.metric("Avg. Length of Stay", round(ehr["Length_of_Stay"].mean(), 2))

    with col3:
        proc_freq = ehr["Procedure_Code"].value_counts().idxmax()
        st.metric("Most Common Procedure", proc_freq)

    with col4:
        approval = (claims["Status"] == "Paid").sum()
        denial = (claims["Status"] == "Denied").sum()
        st.metric("Approval Ratio", f"{approval} / {denial}", help="Paid vs Denied claims count")


    ###### 2. Code Explorer ######
    st.header("📚 Code Explorer")
    code_input = st.text_input("Search ICD or CPT Code:")
    if code_input:
        ehr["Procedure_Code"] = ehr["Procedure_Code"].astype(str)
        ehr["Diagnosis_Code"] = ehr["Diagnosis_Code"].astype(str)

        icd_matches = ehr[ehr["Diagnosis_Code"].str.contains(code_input.upper(), na=False)]
        cpt_matches = ehr[ehr["Procedure_Code"].str.contains(code_input.upper(), na=False)]

        st.subheader("🔍 ICD Code Matches")
        st.dataframe(icd_matches[["Patient_ID", "Diagnosis_Code", "Diagnosis_Description", "Admission_Date"]])

        st.subheader("🔍 CPT Code Matches")
        st.dataframe(cpt_matches[["Patient_ID", "Procedure_Code", "Procedure_Description", "Admission_Date"]])
    
    
    ###### 3. Claims Analyzer ######
    st.header("💰 Claims Analyzer")
    with st.expander("View Summary Charts"):
        st.bar_chart(claims.groupby("Status")[["Billed_Amount", "Paid_Amount"]].mean())

    status_filter = st.selectbox("Filter by Status", ["All"] + list(claims["Status"].unique()))
    provider_filter = st.selectbox("Filter by Provider", ["All"] + list(ehr["Provider"].unique()))
    
    filtered_claims = claims.copy()
    if status_filter != "All":
        filtered_claims = filtered_claims[filtered_claims["Status"] == status_filter]
    if provider_filter != "All":
        patient_ids = ehr[ehr["Provider"] == provider_filter]["Patient_ID"]
        filtered_claims = filtered_claims[filtered_claims["Patient_ID"].isin(patient_ids)]

    st.dataframe(filtered_claims)

    ###### 4. Workflow Efficiency Tracker ######
    # st.header("⏱️ Workflow Efficiency Tracker")
    # ehr["Admission_Date"] = pd.to_datetime(ehr["Admission_Date"], errors="coerce")
    # ehr["Discharge_Date"] = pd.to_datetime(ehr["Discharge_Date"], errors="coerce")

    # ehr["Delay"] = (ehr["Discharge_Date"] - ehr["Admission_Date"]).dt.days - ehr["Length_of_Stay"]
    # st.bar_chart(ehr.set_index("Patient_ID")[["Length_of_Stay", "Delay"]])

    ###### 5. Prompt-Based Insights (Optional) ######
    st.header("💡 Prompt-Based Insights")
    prompt = st.text_input("Ask a question about claims or codes:")

    if prompt:
        date_match = re.findall(r"\d{4}-\d{2}-\d{2}", prompt)
        if len(date_match) == 2:
            start_date, end_date = pd.to_datetime(date_match[0]), pd.to_datetime(date_match[1])
            filtered_claims = claims[(claims["Service_Date"] >= start_date) & (claims["Service_Date"] <= end_date)]
        else:
            filtered_claims = claims

        if "costly" in prompt.lower():
            costly = filtered_claims.groupby("ICD_Code")["Billed_Amount"].sum().sort_values(ascending=False).head(5)
            st.write("💸 Most Costly Diagnoses:")
            st.dataframe(costly)

        elif "denial" in prompt.lower():
            denial_df = filtered_claims[filtered_claims["Status"] == "Denied"]
            denial_rates = denial_df["CPT_Code"].value_counts().head(5)
            st.write("📉 CPT Codes with Highest Denial Rate:")
            st.dataframe(denial_rates)

    ###### 6. Graphs ######
    import plotly.express as px

    st.header("📈 Visual Analytics")

    tab1, tab2, tab3 = st.tabs(["🧑‍⚕️ Diagnoses Overview", "💵 Claims by Provider", "📆 Monthly Trends"])

    with tab1:
        diag_counts = ehr["Diagnosis_Description"].value_counts().nlargest(10).reset_index()
        diag_counts.columns = ["Diagnosis", "Count"]
        fig1 = px.bar(diag_counts, x="Diagnosis", y="Count", title="Top 10 Diagnoses", color="Count", height=400)
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        claims_by_provider = ehr.merge(claims, on="Patient_ID")
        provider_summary = claims_by_provider.groupby("Provider")[["Billed_Amount", "Paid_Amount"]].sum().reset_index()
        fig2 = px.bar(provider_summary, x="Provider", y=["Billed_Amount", "Paid_Amount"],
                      barmode="group", title="Claims Summary by Provider", height=400)
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        claims["Month"] = claims["Service_Date"].dt.to_period("M").astype(str)
        monthly_claims = claims.groupby("Month")[["Billed_Amount", "Paid_Amount"]].sum().reset_index()
        fig3 = px.line(monthly_claims, x="Month", y=["Billed_Amount", "Paid_Amount"],
                       title="Monthly Billed vs Paid Amount", markers=True, height=400)
        st.plotly_chart(fig3, use_container_width=True)

    ###### 7. 🔍 Diagnosis vs Billed Amount Heatmap ######
    st.header("🧠 Top Diagnoses by Cost (Heatmap)")

    import seaborn as sns
    import matplotlib.pyplot as plt

    # Top 10 diagnosis codes by frequency
    top_diag = ehr["Diagnosis_Code"].value_counts().nlargest(10).index
    top_ehr = ehr[ehr["Diagnosis_Code"].isin(top_diag)]

    # Merge with claims to get billing info
    ehr_claims = top_ehr.merge(claims, on="Patient_ID", how="left")

    heatmap_data = ehr_claims.groupby(["Diagnosis_Code", "Status"])["Billed_Amount"].mean().unstack().fillna(0)

    # Create smaller figure for half-width display
    fig, ax = plt.subplots(figsize=(6, 4))  # Adjust size for ~50% width

    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".0f",
        cmap="RdYlGn_r",  # Green-to-red scale
        linewidths=0.5,
        linecolor="gray",
        cbar_kws={"label": "Avg. Billed Amount ($)"}
    )

    ax.set_title("Avg. Billed by Diagnosis & Claim Status", fontsize=12)
    ax.set_xlabel("Claim Status")
    ax.set_ylabel("Diagnosis Code")
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)

    # Render in a smaller column
    left, center, right = st.columns([2, 4, 2])

    with center:
        st.pyplot(fig)


else:
    st.info("Upload both updated CSV files to get started.")