
# 📊 Bond Portfolio Optimization & Immunization

A professional Streamlit dashboard developed as part of a project on **bond portfolio optimization and immunization**, combining **quantitative finance theory** with practical implementation. The dashboard integrates **duration** and **convexity analysis** into an interactive environment for evaluating fixed-income portfolios.

---

## 📌 Motivation

Interest rate risk is one of the most significant challenges in fixed-income portfolio management. Bond prices are highly sensitive to changes in interest rates, and small shifts in the yield curve can cause large fluctuations in portfolio value.

This project addresses these challenges by:

* Quantifying **interest rate sensitivity** via **key rate durations** and **convexity**
* Building a framework for **portfolio immunization**
* Delivering an **interactive dashboard** that enables investors and analysts to monitor, analyze, and export risk-adjusted insights

---

## 📐 Mathematical Framework

### 1. Duration

Duration measures the sensitivity of a bond’s price to changes in interest rates:

$$
D = - \frac{1}{P} \cdot \frac{\partial P}{\partial y}
$$

Where:

* $P$ = bond price
* $y$ = yield

**Portfolio Duration** is the weighted average:

$$
D_p = \sum_{i=1}^{n} w_i D_i
$$

### 2. Convexity

Convexity refines the duration measure by accounting for the curvature in the price-yield relationship:

$$
C = \frac{1}{P} \cdot \frac{\partial^2 P}{\partial y^2}
$$

Portfolio convexity is similarly the weighted sum:

$$
C_p = \sum_{i=1}^{n} w_i C_i
$$

### 3. Price Change Approximation

For small yield changes $\Delta y$:

$$
\frac{\Delta P}{P} \approx -D \cdot \Delta y + \frac{1}{2}C \cdot (\Delta y)^2
$$

This forms the basis for **duration-convexity immunization**, ensuring portfolio value is stable under yield shifts.

---

## 🔬 Methodology

### Step 1: Data Collection

* **Interest rates**: `KeyRates.xlsx`
* **Asset prices**: `Assets.xlsx`
* **Duration matrix**: `durations.xlsx`
* **Convexity matrix**: `convexity.xlsx`

### Step 2: Risk Factor Construction

* Calculated **key rate returns**:

$$
r_t = \frac{kr_t - kr_{t-1}}{kr_{t-1}}
$$

* Built **loadings matrix**:

$$
L = [-D, \tfrac{1}{2}C]
$$

* Constructed **risk factors matrix** $X$:
  Combining $\Delta kr$ and $(\Delta kr)^2$

### Step 3: Asset Return Matrix

For each bond/equity:

$$
R_{i,t} = \frac{P_{i,t} - P_{i,t-1}}{P_{i,t-1}}
$$

Filtered and aligned with risk factors for analysis.

### Step 4: Analytics & Visualization

* Average returns, volatility, correlations
* Cumulative performance analysis
* Risk-return scatter plots
* Correlation heatmaps

---

## 📊 Key Results

* **Duration & Convexity Exposure**: Computed matrices clearly show interest rate sensitivity.
* **Volatility vs Return Trade-off**: Scatter plots highlight asset positioning.
* **Correlation Heatmap**: Identifies diversification potential.
* **Cumulative Returns**: Demonstrated long-term portfolio growth under selected assets.

---

## 🖥️ Dashboard Features

* 📂 **Excel Integration**: Automatic ingestion of bond & equity data
* 🧭 **Interactive Sidebar**: Select assets & date ranges dynamically
* 📈 **Performance Metrics**: Returns, volatility, and portfolio size
* 📊 **Visual Analytics**:

  * Cumulative returns line charts
  * Risk-return scatter plots
  * Correlation heatmaps
  * Average return bar charts
* ⬇️ **Export Functionality**: Download filtered datasets

---


## ⚙️ Installation & Setup

1. Clone Repository

```bash
git clone https://github.com/yourusername/bond-portfolio-optimization.git
cd bond-portfolio-optimization
```

2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Run Streamlit App

```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
bond-portfolio-optimization/
│── app.py                 # Streamlit dashboard
│── requirements.txt       # Dependencies
│── KeyRates.xlsx          # Interest rate data
│── Assets.xlsx            # Asset prices
│── durations.xlsx         # Duration matrix
│── convexity.xlsx         # Convexity matrix
│── screenshots/           # Dashboard screenshots
│── README.md              # Project documentation
```

---

## 🌱 Future Enhancements

* Add **mean-variance portfolio optimization** with immunization constraints
* Introduce **stress testing** under parallel and non-parallel rate shifts
* Integrate **live financial data APIs** for real-time analytics

---

## 👤 Author

**MD Amir Khan**
🎓 MS in Financial Engineering | Stevens Institute of Technology
💡 Quantitative Finance | Portfolio Optimization | Risk Management

---

⚡ Amir, would you like me to also prepare a **separate “Mathematical Appendix” section** (with equations in LaTeX + derivations for immunization constraints) so your README looks research-grade rather than just technical documentation?
