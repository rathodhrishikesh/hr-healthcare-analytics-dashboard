## 🚀 How to Run / Use This App

### 🔧 Option 1: Run Locally

1. **Generate Sample Data (Optional):**
   Run the following to create dummy EHR and Claims CSV files:

   ```bash
   python generate_dummy.py
   ```

   You can modify the script to change the number of records.

2. **Launch the Streamlit App:**

   ```bash
   streamlit run ehr_claims.py
   ```

3. **Use the App:**

   * A local URL will open in your browser (e.g., `http://localhost:8501`)
   * Upload your CSV files when prompted:

     * **EHR/EMR CSV:** Patient & diagnosis data
     * **Claims CSV:** Claims & billing data

4. **Explore and Interact Freely:**
   Use all built-in features to analyze data and extract insights.

---

### 🌐 Option 2: Use on Streamlit Cloud (No Setup)

1. **Visit the App Online:**
   👉 [Open App on Streamlit](https://hr-healthcare-analytics-dashboard.streamlit.app/)

2. **Upload Required CSV Files:**

   * **EHR/EMR CSV:** Patient & diagnosis data
   * **Claims CSV:** Claims & billing data (both available in this repo)

3. **Explore and Interact Freely:**
   Use all built-in features to analyze data and extract insights.
