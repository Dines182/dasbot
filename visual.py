import streamlit as st
import pandas as pd
import plotly.express as px

def visual():
    # Load data
    df = pd.read_excel("Yay All.xlsx")

    # Basic preprocessing & checks
    required_cols = [
        "Year", "Region Name", "School Name",
        "Enrolments", "Attendance", "Teacher Retention", "Non-Teacher Retention"
    ]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        st.error(f"Missing columns: {missing}")
        return

    # Calculate Retention Gap
    df = df.copy()
    df["Retention Gap"] = df["Teacher Retention"] - df["Non-Teacher Retention"]

    st.title("📊 Education Data Visualisation")

   # --- Filters ---
    st.markdown("### 🔍 Filters")
    col1, col2 = st.columns(2)
    with col1:
        years = sorted(df["Year"].unique())
        selected_years = st.multiselect(
            "Select Year(s)",
            options=years,
            default=years,  # default select all years
            help="Select one or more years, or none to show all"
        )
    with col2:
        regions = ["All"] + sorted(df["Region Name"].unique())
        selected_region = st.selectbox("Select Region", regions)

    # Filter data
    if selected_years:
        filtered = df[df["Year"].isin(selected_years)]
    else:
        filtered = df.copy()  # no year filter if nothing selected

    if selected_region != "All":
        filtered = filtered[filtered["Region Name"] == selected_region]


    # --- BMI vs Age style plot but for Attendance vs Enrolments ---
    st.subheader("Attendance vs Enrolments: Explore Relationship")
    plot_type = st.radio("Select Chart Type", ["Scatter", "Box"])
    if plot_type == "Scatter":
        fig = px.scatter(filtered, x="Enrolments", y="Attendance", color="Region Name",
                         hover_data=["School Name"], title="Attendance vs Enrolments")
    else:
        fig = px.box(filtered, x="Region Name", y="Attendance", color="Region Name",
                     title="Attendance Distribution by Region")
    st.plotly_chart(fig, use_container_width=True)

    # --- Row of 3 charts ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Retention Gap by School")
        fig1 = px.bar(filtered.sort_values("Retention Gap"), x="School Name", y="Retention Gap",
                      color="Retention Gap", title="Retention Gap (Teacher - Non-Teacher)")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Attendance Distribution")
        fig2 = px.histogram(filtered, x="Attendance", nbins=30, color="Region Name",
                            title="Attendance Distribution")
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        st.subheader("Region-wise Enrolments Pie Chart")
        pie_data = filtered.groupby("Region Name")["Enrolments"].sum().reset_index()
        fig3 = px.pie(pie_data, names="Region Name", values="Enrolments",
                      title="Proportion of Total Enrolments by Region")
        st.plotly_chart(fig3, use_container_width=True)

    # --- Retention by Region Boxplot ---
    st.subheader("Teacher Retention by Region")
    fig4 = px.box(filtered, x="Region Name", y="Teacher Retention", color="Region Name",
                  title="Teacher Retention Distribution by Region")
    st.plotly_chart(fig4, use_container_width=True)

    # --- Correlation heatmap ---
    st.subheader("Correlation Heatmap")
    corr_cols = ["Enrolments", "Attendance", "Teacher Retention", "Non-Teacher Retention", "Retention Gap"]
    corr_df = filtered[corr_cols].corr()
    fig5 = px.imshow(corr_df, text_auto=True, color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
                     title="Correlation Heatmap of Numeric Features")
    st.plotly_chart(fig5, use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Education Visualisation", layout="wide")
    education_visual()
