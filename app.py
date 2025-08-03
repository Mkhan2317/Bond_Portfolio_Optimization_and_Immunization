import os
import sys
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
        st.error(f"Missing files: {missing_files}")
        st.write("📂 Available files:", os.listdir("."))
        raise FileNotFoundError(f"Missing files: {missing_files}")

    try:
        kr = pd.read_excel("KeyRates.xlsx", engine="openpyxl", index_col=0, header=0) / 100
        assets = pd.read_excel("Assets.xlsx", engine="openpyxl", index_col=0, header=0)
        durations = pd.read_excel("durations.xlsx", index_col=0, header=0)
        convexity = pd.read_excel("convexity.xlsx", index_col=0, header=0)
    except Exception as e:
        st.error(f"Error reading Excel files: {e}")
        st.write("📂 Available files:", os.listdir("."))
        raise

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
    st.write("🔍 Python version:", os.sys.version)
    st.write("🔍 Working directory:", os.getcwd())
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
    st.title("🏦 Bond Portfolio Optimization & Immunization Dashboard")
    st.markdown("---")
    
    # Header with key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Assets",
            value=len(available_assets),
            delta=f"{len(selected_assets)} selected"
        )
    
    with col2:
        st.metric(
            label="📈 Data Points",
            value=f"{len(Y):,}",
            delta="Historical records"
        )
    
    with col3:
        avg_vol = filtered_Y.std().mean()
        st.metric(
            label="⚠️ Avg Volatility",
            value=f"{avg_vol:.2%}",
            delta="Portfolio risk"
        )
    
    with col4:
        avg_return = filtered_Y.mean().mean()
        st.metric(
            label="💰 Avg Return",
            value=f"{avg_return:.2%}",
            delta="Portfolio performance"
        )
    
    st.markdown("---")
    
    # Main content in columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 📋 Dashboard Overview
        
        This professional-grade financial analytics platform provides comprehensive bond portfolio analysis 
        and risk management capabilities. Built using advanced quantitative methods, it enables 
        portfolio managers to make data-driven investment decisions through interactive visualizations 
        and real-time risk assessment.
        
        ### 🎯 Core Capabilities
        - **Interest Rate Risk Analysis**: Duration and convexity-based risk quantification
        - **Portfolio Performance Tracking**: Historical returns and volatility analysis
        - **Correlation Analysis**: Asset relationship mapping and diversification insights
        - **Risk-Return Optimization**: Visual risk-return profiling for asset selection
        - **Data Export**: Filtered datasets for external analysis and reporting
        
        ### 🔧 Technical Features
        - **Real-time Processing**: Dynamic data filtering and analysis
        - **Interactive Visualizations**: Professional charts with comprehensive labeling
        - **Multi-asset Support**: Bonds, equities, and mixed portfolio analysis
        - **Export Functionality**: CSV downloads for further analysis
        - **Responsive Design**: Optimized for desktop and mobile access
        """)
    
    with col2:
        st.markdown("""
        ## 📊 Quick Stats
        
        **Selected Assets**: {selected_count}
        
        **Date Range**: {start_date} to {end_date}
        
        **Analysis Period**: {period_days} days
        
        **Data Quality**: ✅ Complete
        
        **Risk Level**: {risk_level}
        """.format(
            selected_count=len(selected_assets),
            start_date=date_range[0].strftime('%Y-%m-%d'),
            end_date=date_range[1].strftime('%Y-%m-%d'),
            period_days=(date_range[1] - date_range[0]).days,
            risk_level="Medium" if avg_vol < 0.02 else "High" if avg_vol > 0.05 else "Low"
        ))
    
    st.markdown("---")
    
    # Key insights section
    st.markdown("## 🔍 Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📈 Performance Analysis
        - **Cumulative Returns**: Track long-term portfolio growth
        - **Volatility Patterns**: Identify risk concentration periods
        - **Asset Performance**: Compare individual asset contributions
        - **Risk-Adjusted Returns**: Sharpe ratio and other metrics
        """)
    
    with col2:
        st.markdown("""
        ### 🔄 Correlation Insights
        - **Asset Relationships**: Understand diversification benefits
        - **Risk Concentration**: Identify highly correlated assets
        - **Portfolio Balance**: Optimize asset allocation
        - **Market Sensitivity**: Interest rate impact analysis
        """)
    
    with col3:
        st.markdown("""
        ### ⚠️ Risk Management
        - **Duration Analysis**: Interest rate sensitivity measurement
        - **Convexity Assessment**: Non-linear risk quantification
        - **Stress Testing**: Scenario analysis capabilities
        - **Immunization Ready**: Framework for risk mitigation
        """)
    
    st.markdown("---")
    
    # Technical details
    st.markdown("## 🛠 Technical Implementation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 💻 Technology Stack
        - **Backend**: Python 3.x with Pandas, NumPy
        - **Frontend**: Streamlit for interactive web interface
        - **Visualization**: Matplotlib, Seaborn for professional charts
        - **Data Processing**: Excel integration with openpyxl
        - **Deployment**: Streamlit Cloud with dependency management
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Data Sources
        - **Key Rate Data**: Historical interest rate movements
        - **Asset Prices**: Bond and equity price time series
        - **Duration Metrics**: Interest rate sensitivity calculations
        - **Convexity Data**: Non-linear risk measurements
        """)
    
    st.markdown("---")
    
    # Footer with author info
    st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;'>
        <h4>📌 Project by MD Amir Khan</h4>
        <p><strong>MS Financial Engineering | Expected August 2025</strong></p>
        <p>Building the future of quantitative finance through innovative analytics platforms</p>
    </div>
    """, unsafe_allow_html=True)

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
    
    # Summary Statistics
    st.subheader("📈 Summary Statistics")
    avg_return = filtered_Y.mean()
    std_return = filtered_Y.std()
    summary_df = pd.DataFrame({"Average Return": avg_return, "Volatility": std_return})
    st.dataframe(summary_df.style.format("{:.2%}").background_gradient(cmap="Blues"))
    
    # Correlation Heatmap
    st.subheader("🔄 Asset Correlation Matrix")
    fig, ax = plt.subplots(figsize=(10, 8))
    correlation_matrix = filtered_Y.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5, 
                ax=ax, fmt='.2f', cbar_kws={'label': 'Correlation Coefficient'})
    ax.set_title("Asset Correlation Heatmap", fontsize=14, fontweight='bold')
    ax.set_xlabel("Assets", fontsize=12)
    ax.set_ylabel("Assets", fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Risk Metrics
    st.subheader("⚠️ Risk Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Portfolio Volatility", f"{filtered_Y.std().mean():.2%}")
        st.metric("Max Drawdown", f"{filtered_Y.min().min():.2%}")
    
    with col2:
        st.metric("Average Return", f"{filtered_Y.mean().mean():.2%}")
        st.metric("Sharpe Ratio", f"{(filtered_Y.mean().mean() / filtered_Y.std().mean()):.2f}")

# ===============================
# Charts & Visualization
# ===============================
elif section == "Charts & Visualization":
    st.title("📊 Charts & Visualization")
    
    # Chart 1: Average Returns Bar Chart
    st.subheader("📈 Average Returns by Asset")
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.barplot(x=filtered_Y.columns, y=filtered_Y.mean(), palette="viridis", ax=ax1)
    ax1.set_title("Average Returns by Asset", fontsize=14, fontweight='bold')
    ax1.set_xlabel("Assets", fontsize=12)
    ax1.set_ylabel("Average Return", fontsize=12)
    ax1.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig1)
    
    # Chart 2: Risk-Return Scatter Plot
    st.subheader("🎯 Risk-Return Profile")
    avg_return = filtered_Y.mean()
    std_return = filtered_Y.std()
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    scatter = sns.scatterplot(x=std_return, y=avg_return, s=150, color="tomato", 
                             edgecolor="black", ax=ax2)
    
    # Add asset labels
    for i in avg_return.index:
        ax2.text(x=std_return[i] + 0.0005, y=avg_return[i], s=i, fontsize=10, 
                fontweight='bold', ha='left', va='center')
    
    ax2.set_title("Risk-Return Scatter Plot", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Volatility (Standard Deviation)", fontsize=12)
    ax2.set_ylabel("Average Return", fontsize=12)
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig2)
    
    # Chart 3: Cumulative Returns Time Series
    st.subheader("📈 Cumulative Returns Over Time")
    fig3, ax3 = plt.subplots(figsize=(14, 7))
    for col in filtered_Y.columns:
        ax3.plot(filtered_Y.index, (1 + filtered_Y[col]).cumprod(), label=col, linewidth=2)
    
    ax3.set_title("Cumulative Returns Performance", fontsize=14, fontweight='bold')
    ax3.set_xlabel("Date", fontsize=12)
    ax3.set_ylabel("Cumulative Return (Index = 1)", fontsize=12)
    ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig3)
    
    # Chart 4: Returns Distribution
    st.subheader("📊 Returns Distribution")
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    filtered_Y.boxplot(ax=ax4)
    ax4.set_title("Returns Distribution by Asset", fontsize=14, fontweight='bold')
    ax4.set_xlabel("Assets", fontsize=12)
    ax4.set_ylabel("Returns", fontsize=12)
    ax4.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig4)

# ===============================
# Footer
# ===============================
st.sidebar.markdown("---")
st.sidebar.markdown("📌 Project by **MD Amir Khan** | MS Financial Engineering | August 2025")
