import streamlit as st
import pandas as pd
import plotly.express as px

def about_us():
    # Load full dataset
    df = pd.read_excel("Fulles_Data_with_2024.xlsx")
    
    # Filter 2024 data and compute gap
    df_2024 = df[df["Year"] == 2024].copy()
    df_2024["Retention Gap"] = df_2024["Teacher Retention"] - df_2024["Non-Teacher Retention"]

    # --- 2024 Summary and Visualizations ---
    st.title("📊 Retention Summary & Visualization for Year 2024")

    st.subheader("Summary Statistics for 2024")
    summary_cols = ["Teacher Retention", "Non-Teacher Retention", "Retention Gap"]
    summary_df = df_2024[summary_cols].describe().T
    st.dataframe(summary_df.style.format("{:.2f}"))

    st.subheader("Retention Visualizations for 2024")
    st.subheader("NOTE : 2024 values are predicted using Random Forest model trained on 2023 data")



    fig1 = px.box(df_2024.melt(id_vars=["Region Name"],
                               value_vars=["Teacher Retention", "Non-Teacher Retention"],
                               var_name="Retention Type", value_name="Retention Value"),
                  x="Region Name", y="Retention Value", color="Retention Type",
                  title="Teacher vs Non-Teacher Retention by Region (2024)")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.scatter(df_2024, x="Teacher Retention", y="Non-Teacher Retention", color="Region Name",
                      hover_data=["School Name"],
                      title="Teacher Retention vs Non-Teacher Retention (2024)")
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.histogram(df_2024, x="Retention Gap", nbins=30, title="Distribution of Retention Gap (Teacher - Non-Teacher) in 2024")
    st.plotly_chart(fig3, use_container_width=True)

    # --- Multi-year (2019-2024) Visualizations ---
    st.header("📈 Multi-Year (2019 - 2024) Retention Visualizations")
    df_multi = df[(df["Year"] >= 2019) & (df["Year"] <= 2024)].copy()
    df_multi["Retention Gap"] = df_multi["Teacher Retention"] - df_multi["Non-Teacher Retention"]

    # Average retention over years line chart
    avg_retention = df_multi.groupby("Year")[["Teacher Retention", "Non-Teacher Retention"]].mean().reset_index()
    fig_line = px.line(avg_retention, x="Year", y=["Teacher Retention", "Non-Teacher Retention"],
                       markers=True, title="Average Teacher and Non-Teacher Retention Over Years")
    st.plotly_chart(fig_line, use_container_width=True)

    # Box plot retention distribution by year
    fig_box = px.box(df_multi.melt(id_vars=["Year"],
                                  value_vars=["Teacher Retention", "Non-Teacher Retention"],
                                  var_name="Retention Type", value_name="Retention Value"),
                     x="Year", y="Retention Value", color="Retention Type",
                     title="Teacher vs Non-Teacher Retention Distribution by Year")
    st.plotly_chart(fig_box, use_container_width=True)

    st.title(" Retention Summary & Visualization (2019–2024)")

    # Calculate retention gap for all years
    df["Retention Gap"] = df["Teacher Retention"] - df["Non-Teacher Retention"]

    yearly_stats = df.groupby("Year")[["Teacher Retention", "Non-Teacher Retention", "Retention Gap"]].mean().reset_index()
    st.subheader("Retention Gap Over the Years")
    fig_line_gap = px.line(yearly_stats, x="Year", y="Retention Gap", markers=True,
                           title="Average Retention Gap (Teacher - Non-Teacher) by Year")
    st.plotly_chart(fig_line_gap, use_container_width=True)

    st.subheader("Teacher vs Non-Teacher Retention Trends")
    fig_line_retention = px.line(yearly_stats, x="Year",
                                 y=["Teacher Retention", "Non-Teacher Retention"],
                                 markers=True, title="Teacher and Non-Teacher Retention Over Years")
    st.plotly_chart(fig_line_retention, use_container_width=True)

    st.subheader("Region-wise Retention Gap Over Years")
    region_year_gap = df.groupby(["Region Name", "Year"])["Retention Gap"].mean().reset_index()
    fig_region_gap = px.line(region_year_gap, x="Year", y="Retention Gap", color="Region Name",
                             markers=True, title="Region-wise Retention Gap Over Time")
    st.plotly_chart(fig_region_gap, use_container_width=True)

    st.subheader("Boxplot: Teacher vs Non-Teacher Retention by Year")
    melted = df.melt(id_vars=["Year"], value_vars=["Teacher Retention", "Non-Teacher Retention"],
                     var_name="Retention Type", value_name="Retention Value")
    fig_box_years = px.box(melted, x="Year", y="Retention Value", color="Retention Type",
                           title="Retention Distribution by Year")
    st.plotly_chart(fig_box_years, use_container_width=True)
    
    # Calculate retention gap
    df["Retention Gap"] = df["Teacher Retention"] - df["Non-Teacher Retention"]

    st.subheader("Yearly Averages: Retention & Enrolments")
    yearly_stats = df.groupby("Year")[["Teacher Retention", "Non-Teacher Retention", "Retention Gap", "Enrolments"]].mean().reset_index()
    st.dataframe(yearly_stats.style.format("{:.2f}"))

    st.subheader("Enrolments Over Time")
    fig_enrol = px.line(yearly_stats, x="Year", y="Enrolments", markers=True, title="Average Enrolments by Year")
    st.plotly_chart(fig_enrol, use_container_width=True)

    st.subheader("Region-wise Enrolment Trends")
    region_enrol = df.groupby(["Region Name", "Year"])["Enrolments"].mean().reset_index()
    fig_region_enrol = px.line(region_enrol, x="Year", y="Enrolments", color="Region Name",
                               markers=True, title="Average Enrolments per Region (2019–2024)")
    st.plotly_chart(fig_region_enrol, use_container_width=True)

    st.subheader("Correlation Heatmap (All Years)")
    numeric_cols = df.select_dtypes(include="number")[["Enrolments", "Teacher Retention", "Non-Teacher Retention", "Retention Gap"]]
    corr_matrix = numeric_cols.corr()

    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        title="Correlation Heatmap: Enrolments vs Retention"
    )
    st.plotly_chart(fig_corr, use_container_width=True)
