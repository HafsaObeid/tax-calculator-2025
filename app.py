import streamlit as st

# Set up the web page title and wide layout
st.set_page_config(page_title="India Tax Calculator FY 25-26", layout="centered")

st.title("📊 India Tax Calculator FY 2025-26")
st.write("Compare your tax liabilities between the Old and New Tax Regimes with the latest slab adjustments.")

# ----------------------------------------------------------------
# SIDEBAR: USER INPUT CONTROLS
# ----------------------------------------------------------------
st.sidebar.header("💰 Income & Deductions")

gross_salary = st.sidebar.number_input("Gross Annual Salary (₹)", min_value=0, value=1200000, step=10000)

st.sidebar.subheader("Old Regime Deductions Only")
exemptions_old_only = st.sidebar.number_input("Exemptions (HRA, LTA, PTax) (₹)", min_value=0, value=0, step=5000)
deductions_80c = st.sidebar.number_input("Section 80C (PPF, EPF, ELSS) (₹)", min_value=0, value=150000, step=5000)
sec_24b_home_loan = st.sidebar.number_input("Section 24b (Home Loan Interest) (₹)", min_value=0, value=0, step=5000)
sec_80d_medical = st.sidebar.number_input("Section 80D (Medical Insurance) (₹)", min_value=0, value=0, step=1000)
other_deductions_old = st.sidebar.number_input("Other Custom Old Deductions (₹)", min_value=0, value=0, step=5000)

st.sidebar.subheader("Deductions Allowed In Both Regimes")
sec_80ccd2_nps_employer = st.sidebar.number_input("Section 80CCD(2) (Employer NPS) (₹)", min_value=0, value=0, step=5000)

# ----------------------------------------------------------------
# CALCULATIONS LOGIC
# ----------------------------------------------------------------
# 1. OLD REGIME
old_std_deduction = 50000
eligible_80c = min(deductions_80c, 150000)
eligible_24b = min(sec_24b_home_loan, 200000)

total_old_deductions = (old_std_deduction + exemptions_old_only + eligible_80c + eligible_24b + sec_80d_medical + other_deductions_old + sec_80ccd2_nps_employer)
old_taxable_income = max(0, gross_salary - total_old_deductions)

old_base_tax = 0
if old_taxable_income <= 250000:
    old_base_tax = 0
elif old_taxable_income <= 500000:
    old_base_tax = (old_taxable_income - 250000) * 0.05
elif old_taxable_income <= 1000000:
    old_base_tax = 12500 + (old_taxable_income - 500000) * 0.20
else:
    old_base_tax = 12500 + 100000 + (old_taxable_income - 1000000) * 0.30

if old_taxable_income <= 500000:
    old_base_tax = 0
old_total_tax = round(old_base_tax * 1.04)

# 2. NEW REGIME
new_std_deduction = 75000
total_new_deductions = new_std_deduction + sec_80ccd2_nps_employer
new_taxable_income = max(0, gross_salary - total_new_deductions)

new_base_tax = 0
if new_taxable_income <= 400000:
    new_base_tax = 0
elif new_taxable_income <= 800000:
    new_base_tax = (new_taxable_income - 400000) * 0.05
elif new_taxable_income <= 1200000:
    new_base_tax = 20000 + (new_taxable_income - 800000) * 0.10
elif new_taxable_income <= 1600000:
    new_base_tax = 20000 + 40000 + (new_taxable_income - 1200000) * 0.15
else:
    new_base_tax = 20000 + 40000 + 60000 + (new_taxable_income - 1600000) * 0.20

if new_taxable_income <= 700000:
    new_base_tax = 0
new_total_tax = round(new_base_tax * 1.04)

# ----------------------------------------------------------------
# RENDER VISUAL OUTPUTS
# ----------------------------------------------------------------
# Highlights Section
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Old Regime Payable Tax", value=f"₹{old_total_tax:,}")
with col2:
    st.metric(label="New Regime Payable Tax", value=f"₹{new_total_tax:,}")

# Final Verdict Banner
tax_diff = abs(old_total_tax - new_total_tax)
if old_total_tax < new_total_tax:
    st.success(f"🟢 **Verdict:** The **Old Regime** saves you **₹{tax_diff:,}**!")
elif new_total_tax < old_total_tax:
    st.success(f"🟢 **Verdict:** The **New Regime** saves you **₹{tax_diff:,}**!")
else:
    st.info("🟢 **Verdict:** Both regimes lead to the exact same tax payment.")

# Breakdown Comparison Table
st.subheader("📋 Step-by-Step Breakdown Comparison")
st.markdown(f"""

| Calculation Metric | Old Regime | New Regime |
| :--- | :---: | :---: |
| **Gross Salary** | ₹{gross_salary:,} | ₹{gross_salary:,} |
| Standard Deduction | ₹{old_std_deduction:,} | ₹{new_std_deduction:,} |
| Section 80C Limit Applied | ₹{eligible_80c:,} | ₹0 |
| Housing Loan Int. (Sec 24b) | ₹{eligible_24b:,} | ₹0 |
| Medical Premium (Sec 80D) | ₹{sec_80d_medical:,} | ₹0 |
| Corporate NPS (Sec 80CCD) | ₹{sec_80ccd2_nps_employer:,} | ₹{sec_80ccd2_nps_employer:,} |
| **Net Taxable Income** | **₹{old_taxable_income:,}** | **₹{new_taxable_income:,}** |
| **Final Tax (Including 4% Cess)** | **₹{old_total_tax:,}** | **₹{new_total_tax:,}** |
""")
