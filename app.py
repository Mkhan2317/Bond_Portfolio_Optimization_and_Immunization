import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bond Portfolio Dashboard", layout="wide")

# ===============================
# Sidebar
# ===============================
st.sidebar.title("📊 Bond Portfolio Dashboard")
st.sidebar.markdown("Interactive dashboard showcasing the outcome of my project on bond portfolio optimization & immunization.")

section = st.sidebar.radio("Navigation", ["Overview", "Data Explorer", "Analytics & Risk", "Charts & Visualization"])

# ===============================
# Load Data with Safety Checks
# ===============================
@st.cache_data
def load_data():
    required_files = ["KeyRates.xlsx", "Assets.xlsx", "durations.xlsx", "convexity.xlsx"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        raise FileNotFoundError(f"Missing files: {missing_files}")

    kr = pd.read_excel("KeyRates.xlsx", engine="openpyxl", index_col=0, header=0) / 100
    assets = pd.read_excel("Assets.xlsx", engine="openpyxl", index_col=0, header=0)
    durations = pd.read_excel("durations.xlsx", index_col=0, header=0)
    convexity = pd.read_excel("convexity.xlsx", index_col=0, header=0)

    merged = pd.merge(left=assets, right=kr, how="inner", on="Date")
    dates = merged.index

    kr_returns = kr.loc[dates, :].sort_index().diff().dropna()
    kr_returns.sort_index(ascending=False, inplace=True)

    assets_returns = assets.loc[dates].sort_index().pct_change().dropna()
    assets_returns.sort_index(ascending=False, inplace=True)

    loadings = pd.concat([-1.0 * durations, 0.5 * convexity], axis=1)
    kr_returns_sq = kr_returns ** 2
    X = pd.concat([kr_returns, kr_returns_sq], axis=1)
    X.columns = loadings.columns
    Y = assets_returns[loadings.index]

    return kr_returns, assets_returns, durations, convexity, loadings, X, Y

try:
    kr_returns, assets_returns, durations, convexity, loadings, X, Y = load_data()
except Exception as e:
    st.error(f"❌ App initialization failed: {e}")
    st.write("📂 Current repo files:", os.listdir("."))
    st.stop()

# ===============================
# Sidebar Filters
# ===============================
available_assets = list(Y.columns)
selected_assets = st.sidebar.multiselect("Select Assets", available_assets, default=available_assets[:5])

# Convert Pandas Timestamps safely
dates_list = Y.index.to_pydatetime()
min_date, max_date = dates_list.min().date(), dates_list.max().date()

date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Filter returns
mask = (Y.index.date >= date_range[0]) & (Y.index.date <= date_range[1])
filtered_Y = Y.loc[mask, selected_assets]

# ===============================
# Overview
# ===============================
if section == "Overview":
    st.title("📌 Project Outcome: Bond Portfolio Optimization & Immunization")
    
    st.markdown("""
    ## Project Overview

    This dashboard is the **final outcome of my project on bond portfolio optimization and immunization**.  
    It demonstrates how interest rate risk can be measured and managed using **duration and convexity analysis**, 
    and how these concepts can be embedded into an interactive, professional-grade financial dashboard.

    ---
    ### 🎯 Objectives
    - Analyze a mixed portfolio of bonds and equities using historical price and interest rate data  
    - Quantify exposures using **key rate durations** and **convexity**  
    - Provide an interactive dashboard to visualize **returns, risk factors, and correlations**  
    - Establish a foundation for **immunization strategies** to mitigate interest rate risk  

    ---
    ### 🔑 Key Insights
    - **Interest Rate Sensitivity**: Captured via duration and convexity matrices  
    - **Portfolio Risk Profile**: Highlighted volatility, average returns, and asset correlations  
    - **Performance Tracking**: Cumulative returns analysis revealed growth trends across assets  
    - **Immunization Readiness**: Framework prepared for duration-matching optimization  

    ---
    ### 📊 Deliverables
    - Interactive **Streamlit dashboard** for portfolio analytics  
    - **Risk-return analysis** with volatility, correlations, and scatter plots  
    - **Visual outcomes**:  
        - Cumulative returns time-series  
        - Correlation heatmap  
        - Risk-return scatter plots  
        - Average return bar charts  
    - Exportable **filtered datasets** for further study  

    ---
    ### 🌱 Future Scope
    - Implement **duration-matched portfolio optimization**  
    - Add **scenario analysis under rate shocks**  
    - Integrate **live bond market data** for real-time monitoring  

    ---
    """)

    col1, col2, col3 = st.columns(3)
    col1.metric("Number of Assets", len(available_assets))
    col2.metric("Data Points", len(Y))
    col3.metric("Selected Assets", len(selected_assets))

# ===============================
# Data Explorer
# ===============================
elif section == "Data Explorer":
    st.title("📁 Data Explorer")
    st.dataframe(kr_returns.head(15).style.format("{:.4%}"))
    st.dataframe(filtered_Y.head(15).style.format("{:.4%}"))
    st.dataframe(durations.style.format("{:.4f}"))
    st.dataframe(convexity.style.format("{:.4f}"))
    st.dataframe(loadings.style.format("{:.4f}"))
    st.download_button("⬇️ Download Filtered Asset Returns CSV",
                       filtered_Y.to_csv().encode("utf-8"),
                       "filtered_returns.csv",
                       "text/csv")

# ===============================
# Analytics & Risk
# ===============================
elif section == "Analytics & Risk":
    st.title("📊 Analytics & Risk")
    avg_return = filtered_Y.mean()
    std_return = filtered_Y.std()
    summary_df = pd.DataFrame({"Average Return": avg_return, "Volatility": std_return})
    st.dataframe(summary_df.style.format("{:.2%}").background_gradient(cmap="Blues"))
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(filtered_Y.corr(), annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
    st.pyplot(fig)

# ===============================
# Charts & Visualization
# ===============================
elif section == "Charts & Visualization":
    st.title("📊 Charts & Visualization")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=filtered_Y.columns, y=filtered_Y.mean(), palette="viridis", ax=ax1)
    st.pyplot(fig1)
    avg_return = filtered_Y.mean()
    std_return = filtered_Y.std()
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x=std_return, y=avg_return, s=120, color="tomato", edgecolor="black", ax=ax2)
    for i in avg_return.index:
        ax2.text(x=std_return[i] + 0.0005, y=avg_return[i], s=i, fontsize=9)
    st.pyplot(fig2)
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    for col in filtered_Y.columns:
        ax3.plot(filtered_Y.index, (1 + filtered_Y[col]).cumprod(), label=col)
    ax3.legend()
    st.pyplot(fig3)

# ===============================
# Footer
# ===============================
st.sidebar.markdown("---")
st.sidebar.markdown("📌 Project by **MD Amir Khan** | MS Financial Engineering | August 2025")
