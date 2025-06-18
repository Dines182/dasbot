import streamlit as st
import pandas as pd

def statis():
    # Load your data
    df = pd.read_excel("Yay All.xlsx")

    # Check required columns
    required_cols = ["Year", "Region Name", "School Name", "Enrolments", "Attendance", "Teacher Retention", "Non-Teacher Retention"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        st.error(f"Dataset is missing required columns: {missing}")
        return

    st.markdown("## 📊 Summary Statistics by Year")

    # --- Year filter with “All Years” option ---
    years = sorted(df["Year"].unique())
    year_options = ["All Years"] + years
    selected_year = st.selectbox("Select Year", year_options, index=0)

    # Filter data
    if selected_year == "All Years":
        filtered_df = df.copy()
    else:
        filtered_df = df[df["Year"] == selected_year].copy()

    # Calculate retention gap
    filtered_df["Retention Gap"] = filtered_df["Teacher Retention"] - filtered_df["Non-Teacher Retention"]

    # Columns for numeric stats
    numeric_cols = [
        "Enrolments", "Attendance", "Teacher Retention", "Non-Teacher Retention"
    ]

    # Calculate means
    numeric_means = filtered_df[numeric_cols].mean().round(2)
    retention_gap_mean = filtered_df["Retention Gap"].mean().round(2)

    # Combine stats using pd.concat instead of append
    summary = pd.concat([numeric_means, pd.Series({"Retention Gap": retention_gap_mean})])

    # Rename for readability
    summary = summary.rename({
        "Enrolments": "Average Enrolments",
        "Attendance": "Average Attendance (%)",
        "Teacher Retention": "Average Teacher Retention (%)",
        "Non-Teacher Retention": "Average Non-Teacher Retention (%)",
        "Retention Gap": "Average Retention Gap (Teacher - Non-Teacher %)"
    })

    # Display summary
    summary_df = pd.DataFrame(summary).reset_index()
    summary_df.columns = ["Metric", "Value"]
    summary_df.index = summary_df.index + 1

    with st.container():
        st.dataframe(summary_df, use_container_width=True, height=210)

    # Detailed descriptive stats
    st.markdown("### Detailed Descriptive Statistics")
    st.dataframe(filtered_df[numeric_cols + ["Retention Gap"]].describe().T)

    # Download filtered data
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "Download Filtered Data as CSV",
        convert_df(filtered_df),
        f"education_data_{selected_year}.csv",
        "text/csv"
    )

if __name__ == "__main__":
    st.set_page_config(page_title="Education Summary Stats", layout="wide")
    statis()
