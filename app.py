import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="AeroRent UK - Financial Calculator",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #4f46e5;
    }
    .break-even-highlight {
        background-color: #eef2ff;
        border-left: 4px solid #4f46e5;
    }
    .profit-positive {
        color: #059669;
    }
    .profit-negative {
        color: #dc2626;
    }
    .download-section {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px dashed #cbd5e1;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🚁 AeroRent UK - Financial Calculator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Interactive financial projections for your drone rental business</p>', unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.header("📊 Business Configuration")
    
    # Capital Expenditure
    st.subheader("1. Initial Capital Expenditure")
    
    col1, col2 = st.columns(2)
    with col1:
        flip_qty = st.number_input("DJI Flips (Qty)", min_value=0.0, value=3.0, step=1.0)
        mini4_qty = st.number_input("DJI Mini 4 Pros (Qty)", min_value=0.0, value=1.0, step=1.0)
        case_cost = st.number_input("Hard Cases Cost (£)", min_value=0.0, value=0.0, step=10.0)
        battery_cost = st.number_input("Extra Batteries Cost (£)", min_value=0.0, value=0.0, step=10.0)
        filter_cost = st.number_input("ND Filters Cost (£)", min_value=0.0, value=0.0, step=10.0)
    
    with col2:
        flip_cost = st.number_input("DJI Flip Cost (£)", min_value=0.0, value=587.95, step=10.0)
        mini4_cost = st.number_input("DJI Mini 4 Pro Cost (£)", min_value=0.0, value=899.0, step=10.0)
        web_cost = st.number_input("Website Setup Cost (£)", min_value=0.0, value=0.0, step=100.0)
        legal_cost = st.number_input("Legal Fees (£)", min_value=0.0, value=100.0, step=50.0)
    
    # SD Cards (1 per drone)
    total_drones_for_sd = flip_qty + mini4_qty
    sd_card_cost_per_unit = 38.99
    total_sd_card_cost = total_drones_for_sd * sd_card_cost_per_unit
    
    if total_drones_for_sd > 0:
        st.markdown(f"**SD Cards**: {total_drones_for_sd} × £{sd_card_cost_per_unit} = £{total_sd_card_cost:.2f}**")
    
    # Operational Expenditure
    st.subheader("2. Annual Operational Costs")
    
    col1, col2 = st.columns(2)
    with col1:
        platform_cost = st.number_input("E-commerce Platform (£)", min_value=0.0, value=228.0, step=10.0)
        insurance_cost = st.number_input("Corporate Insurance (£)", min_value=0.0, value=750.0, step=50.0)
        marketing_cost = st.number_input("Digital Marketing (£)", min_value=0.0, value=6000.0, step=500.0)
        shipping_supplies_cost = st.number_input("Shipping Supplies (£)", min_value=0.0, value=1200.0, step=100.0)
    
    with col2:
        domain_cost = st.number_input("Domain & Hosting (£)", min_value=0.0, value=30.0, step=5.0)
        caa_cost = st.number_input("CAA Renewal (£)", min_value=0.0, value=11.79, step=1.0)
        repairs_cost = st.number_input("Repairs & Maintenance (£)", min_value=0.0, value=295.60, step=10.0)
        shipping_cost = st.number_input("Shipping Cost per Rental (£)", min_value=0.0, value=32.0, step=1.0)
    
    processing_fee = st.number_input("Payment Processing Fee (%)", min_value=0.0, value=1.5, step=0.1)

    # Additional Costs Section
    st.subheader("3. Additional Costs")
    st.markdown("Add any additional costs with notes")
    
    # Initialize session state for additional costs if it doesn't exist
    if 'additional_costs' not in st.session_state:
        st.session_state.additional_costs = []
    
    # Add new cost button
    if st.button("➕ Add Additional Cost"):
        st.session_state.additional_costs.append({"amount": 0.0, "note": ""})
    
    # Display existing additional costs
    additional_costs_total = 0.0
    costs_to_remove = []
    
    for i, cost in enumerate(st.session_state.additional_costs):
        col1, col2, col3 = st.columns([1, 2, 0.5])
        with col1:
            new_amount = st.number_input(f"Amount (£)", min_value=0.0, value=cost["amount"], step=10.0, key=f"cost_amount_{i}")
            st.session_state.additional_costs[i]["amount"] = new_amount
        with col2:
            new_note = st.text_input(f"Description", value=cost["note"], key=f"cost_note_{i}")
            st.session_state.additional_costs[i]["note"] = new_note
        with col3:
            if st.button("🗑️", key=f"remove_cost_{i}"):
                costs_to_remove.append(i)
        
        additional_costs_total += new_amount
    
    # Remove costs that were marked for deletion
    for index in reversed(costs_to_remove):
        st.session_state.additional_costs.pop(index)
        st.rerun()
    
    # Display total additional costs
    if additional_costs_total > 0:
        st.markdown(f"**Total Additional Costs: £{additional_costs_total:,.2f}**")
    
    # Display additional costs breakdown
    if st.session_state.additional_costs:
        st.markdown("**Additional Costs Breakdown:**")
        for i, cost in enumerate(st.session_state.additional_costs):
            if cost["amount"] > 0:
                note_display = cost["note"] if cost["note"] else "No description"
                st.markdown(f"- £{cost['amount']:,.2f}: {note_display}")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Pricing Strategy
    st.subheader("4. Pricing & Revenue Strategy")
    
    pricing_col1, pricing_col2 = st.columns(2)
    
    with pricing_col1:
        st.markdown("**DJI Flip Pricing (£)**")
        flip_daily = st.number_input("Daily Hire", min_value=0.0, value=49.0, step=1.0, key="flip_daily")
        flip_weekend = st.number_input("Weekend Hire", min_value=0.0, value=85.0, step=1.0, key="flip_weekend")
        flip_weekly = st.number_input("Weekly Hire", min_value=0.0, value=165.0, step=5.0, key="flip_weekly")
    
    with pricing_col2:
        st.markdown("**DJI Mini 4 Pro Pricing (£)**")
        mini4_daily = st.number_input("Daily Hire", min_value=0.0, value=65.0, step=1.0, key="mini4_daily")
        mini4_weekend = st.number_input("Weekend Hire", min_value=0.0, value=109.0, step=1.0, key="mini4_weekend")
        mini4_weekly = st.number_input("Weekly Hire", min_value=0.0, value=210.0, step=5.0, key="mini4_weekly")
    
    # Rental Mix
    st.markdown("**Rental Mix Assumption (%)**")
    mix_col1, mix_col2, mix_col3 = st.columns(3)
    
    with mix_col1:
        mix_daily = st.number_input("Daily", min_value=0.0, max_value=100.0, value=20.0, step=5.0, key="mix_daily")
    with mix_col2:
        mix_weekend = st.number_input("Weekend", min_value=0.0, max_value=100.0, value=60.0, step=5.0, key="mix_weekend")
    with mix_col3:
        mix_weekly = st.number_input("Weekly", min_value=0.0, max_value=100.0, value=20.0, step=5.0, key="mix_weekly")
    
    # Validate rental mix
    mix_total = mix_daily + mix_weekend + mix_weekly
    if mix_total != 100.0:
        st.error(f"⚠️ Rental mix percentages add up to {mix_total}%. Must equal 100%.")
    else:
        st.success("✅ Rental mix percentages are valid!")

# Calculations
def calculate_financials():
    # Capital Expenditure
    total_drones = flip_qty + mini4_qty
    capex = (flip_qty * flip_cost) + (mini4_qty * mini4_cost) + case_cost + battery_cost + filter_cost + web_cost + legal_cost
    
    # SD Cards (1 per drone)
    sd_card_cost_per_unit = 38.99
    total_sd_card_cost = total_drones * sd_card_cost_per_unit
    capex += total_sd_card_cost
    
    # Additional Costs
    additional_costs_total = sum(cost["amount"] for cost in st.session_state.get('additional_costs', []))
    
    # Operational Expenditure
    opex = platform_cost + domain_cost + insurance_cost + caa_cost + marketing_cost + repairs_cost + shipping_supplies_cost
    total_first_year_costs = capex + opex + additional_costs_total
    
    # Revenue & Margin
    mix_daily_pct = mix_daily / 100.0
    mix_weekend_pct = mix_weekend / 100.0
    mix_weekly_pct = mix_weekly / 100.0
    
    flip_avg_rev = (flip_daily * mix_daily_pct) + (flip_weekend * mix_weekend_pct) + (flip_weekly * mix_weekly_pct)
    mini4_avg_rev = (mini4_daily * mix_daily_pct) + (mini4_weekend * mix_weekend_pct) + (mini4_weekly * mix_weekly_pct)
    
    flip_ratio = flip_qty / total_drones if total_drones > 0 else 0
    mini4_ratio = mini4_qty / total_drones if total_drones > 0 else 0
    
    weighted_avg_revenue = (flip_avg_rev * flip_ratio) + (mini4_avg_rev * mini4_ratio)
    
    processing_cost = weighted_avg_revenue * (processing_fee / 100.0)
    variable_cost_per_rental = shipping_cost + processing_cost
    contribution_margin = weighted_avg_revenue - variable_cost_per_rental
    
    # Break-Even Analysis
    break_even_days = total_first_year_costs / contribution_margin if contribution_margin > 0 else 0
    total_available_days = total_drones * 365
    break_even_utilisation = (break_even_days / total_available_days * 100.0) if total_available_days > 0 else 0
    
    return {
        'total_first_year_costs': total_first_year_costs,
        'weighted_avg_revenue': weighted_avg_revenue,
        'contribution_margin': contribution_margin,
        'break_even_days': break_even_days,
        'break_even_utilisation': break_even_utilisation,
        'total_drones': total_drones,
        'total_available_days': total_available_days,
        'variable_cost_per_rental': variable_cost_per_rental,
        'opex': opex,
        'capex': capex
    }

# Function to create comprehensive data export
def create_export_data(results):
    # Get additional costs
    additional_costs = st.session_state.get('additional_costs', [])
    additional_costs_total = sum(cost["amount"] for cost in additional_costs)
    
    # Create multiple dataframes for different sections
    
    # 1. Input Parameters
    inputs_data = {
        'Category': [
            'Capital Expenditure', 'Capital Expenditure', 'Capital Expenditure', 'Capital Expenditure',
            'Capital Expenditure', 'Capital Expenditure', 'Capital Expenditure', 'Capital Expenditure',
            'Capital Expenditure', 'Operational Costs', 'Operational Costs', 'Operational Costs', 'Operational Costs',
            'Operational Costs', 'Operational Costs', 'Operational Costs', 'Operational Costs',
            'Pricing Strategy', 'Pricing Strategy', 'Pricing Strategy', 'Pricing Strategy',
            'Pricing Strategy', 'Pricing Strategy', 'Pricing Strategy', 'Pricing Strategy',
            'Pricing Strategy', 'Pricing Strategy', 'Pricing Strategy'
        ],
        'Parameter': [
            'DJI Flips Quantity', 'DJI Flip Cost per Unit', 'DJI Mini 4 Pros Quantity', 'DJI Mini 4 Pro Cost per Unit',
            'Hard Cases Cost', 'Extra Batteries Cost', 'ND Filters Cost', 'Website Setup Cost',
            'SD Cards Cost', 'E-commerce Platform', 'Domain & Hosting', 'Corporate Insurance', 'CAA Renewal',
            'Digital Marketing', 'Repairs & Maintenance', 'Shipping Supplies', 'Shipping Cost per Rental',
            'DJI Flip Daily Price', 'DJI Flip Weekend Price', 'DJI Flip Weekly Price',
            'DJI Mini 4 Pro Daily Price', 'DJI Mini 4 Pro Weekend Price', 'DJI Mini 4 Pro Weekly Price',
            'Rental Mix Daily %', 'Rental Mix Weekend %', 'Rental Mix Weekly %', 'Payment Processing Fee %',
            'Legal Fees'
        ],
        'Value': [
            flip_qty, flip_cost, mini4_qty, mini4_cost,
            case_cost, battery_cost, filter_cost, web_cost,
            (flip_qty + mini4_qty) * 38.99, platform_cost, domain_cost, insurance_cost, caa_cost,
            marketing_cost, repairs_cost, shipping_supplies_cost, shipping_cost,
            flip_daily, flip_weekend, flip_weekly,
            mini4_daily, mini4_weekend, mini4_weekly,
            mix_daily, mix_weekend, mix_weekly, processing_fee,
            legal_cost
        ],
        'Unit': [
            'units', '£', 'units', '£',
            '£', '£', '£', '£',
            '£', '£', '£', '£',
            '£', '£', '£', '£',
            '£', '£', '£',
            '£', '£', '£',
            '%', '%', '%', '%',
            '£'
        ]
    }
    
    # Add additional costs to inputs data
    for i, cost in enumerate(additional_costs):
        if cost["amount"] > 0:
            inputs_data['Category'].append('Additional Costs')
            inputs_data['Parameter'].append(f"Additional Cost {i+1}: {cost['note']}" if cost['note'] else f"Additional Cost {i+1}")
            inputs_data['Value'].append(cost["amount"])
            inputs_data['Unit'].append('£')
    
    # Ensure all arrays have the same length by adding empty entries if needed
    base_length = len(inputs_data['Category'])
    for key in inputs_data:
        while len(inputs_data[key]) < base_length:
            if key == 'Category':
                inputs_data[key].append('Additional Costs')
            elif key == 'Parameter':
                inputs_data[key].append('')
            elif key == 'Value':
                inputs_data[key].append(0.0)
            elif key == 'Unit':
                inputs_data[key].append('£')
    
    # 2. Key Metrics
    metrics_data = {
        'Metric': [
            'Total First-Year Costs', 'Weighted Average Revenue per Day', 'Contribution Margin per Day',
            'Break-Even Days', 'Break-Even Utilisation Rate', 'Total Drones', 'Total Available Days',
            'Variable Cost per Rental', 'Annual Operational Costs', 'Capital Expenditure'
        ],
        'Value': [
            results['total_first_year_costs'], results['weighted_avg_revenue'], results['contribution_margin'],
            results['break_even_days'], results['break_even_utilisation'], results['total_drones'],
            results['total_available_days'], results['variable_cost_per_rental'], results['opex'], results['capex']
        ],
        'Unit': [
            '£', '£', '£', 'days', '%', 'units', 'days', '£', '£', '£'
        ]
    }
    
    # 3. Detailed Projections
    def calculate_projection(utilisation):
        rental_days = results['total_available_days'] * (utilisation / 100.0)
        total_revenue = rental_days * results['weighted_avg_revenue']
        total_variable_costs = rental_days * results['variable_cost_per_rental']
        profit = total_revenue - results['opex'] - total_variable_costs - results['capex']
        return {'revenue': total_revenue, 'profit': profit, 'rental_days': rental_days}
    
    utilisation_rates = [10, 15, 20, 25, 30, 35, 40, 45, 50]
    projections_data = []
    
    for util in utilisation_rates:
        proj = calculate_projection(util)
        projections_data.append({
            'Utilisation Rate (%)': util,
            'Rental Days': proj['rental_days'],
            'Annual Revenue (£)': proj['revenue'],
            'Annual Profit (£)': proj['profit'],
            'Profit Margin (%)': (proj['profit'] / proj['revenue'] * 100.0) if proj['revenue'] > 0 else 0
        })
    
    # 4. Cost Breakdown
    cost_breakdown_data = {
        'Cost Category': [
            'DJI Flips', 'DJI Mini 4 Pros', 'SD Cards', 'Accessories (Cases, Batteries, Filters)',
            'Website & Legal', 'E-commerce Platform', 'Domain & Hosting', 'Insurance & CAA',
            'Marketing', 'Repairs & Maintenance', 'Shipping Supplies'
        ],
        'Amount (£)': [
            flip_qty * flip_cost, mini4_qty * mini4_cost, (flip_qty + mini4_qty) * 38.99, case_cost + battery_cost + filter_cost,
            web_cost + legal_cost, platform_cost, domain_cost, insurance_cost + caa_cost,
            marketing_cost, repairs_cost, shipping_supplies_cost
        ],
        'Type': [
            'Capital', 'Capital', 'Capital', 'Capital', 'Capital',
            'Operational', 'Operational', 'Operational', 'Operational', 'Operational', 'Operational'
        ]
    }
    
    # Add additional costs to cost breakdown
    for i, cost in enumerate(additional_costs):
        if cost["amount"] > 0:
            cost_breakdown_data['Cost Category'].append(f"Additional Cost {i+1}: {cost['note']}" if cost['note'] else f"Additional Cost {i+1}")
            cost_breakdown_data['Amount (£)'].append(cost["amount"])
            cost_breakdown_data['Type'].append('Additional')
    
    return {
        'inputs': pd.DataFrame(inputs_data),
        'metrics': pd.DataFrame(metrics_data),
        'projections': pd.DataFrame(projections_data),
        'cost_breakdown': pd.DataFrame(cost_breakdown_data)
    }

if mix_total == 100.0:
    results = calculate_financials()
    
    # Download section
    st.markdown("---")
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    st.subheader("📥 Download Financial Data")
    st.markdown("Export all pricing, inputs, and financial projections for analysis")
    
    # Create export data
    export_data = create_export_data(results)
    
    # Create a comprehensive CSV with all data
    def create_comprehensive_csv():
        output = io.StringIO()
        
        # Write header
        output.write("AERORENT UK - FINANCIAL CALCULATOR EXPORT\n")
        output.write(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
        output.write("=" * 50 + "\n\n")
        
        # Write inputs
        output.write("INPUT PARAMETERS\n")
        output.write("-" * 20 + "\n")
        export_data['inputs'].to_csv(output, index=False)
        output.write("\n\n")
        
        # Write key metrics
        output.write("KEY METRICS\n")
        output.write("-" * 12 + "\n")
        export_data['metrics'].to_csv(output, index=False)
        output.write("\n\n")
        
        # Write projections
        output.write("ANNUAL PROJECTIONS\n")
        output.write("-" * 18 + "\n")
        export_data['projections'].to_csv(output, index=False)
        output.write("\n\n")
        
        # Write cost breakdown
        output.write("COST BREAKDOWN\n")
        output.write("-" * 14 + "\n")
        export_data['cost_breakdown'].to_csv(output, index=False)
        
        return output.getvalue()
    
    csv_data = create_comprehensive_csv()
    
    # Download button
    st.download_button(
        label="📊 Download Complete Financial Report (CSV)",
        data=csv_data,
        file_name=f"aerorent_financial_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        help="Download all pricing, inputs, and financial projections as a comprehensive CSV file"
    )
    
    # Individual section downloads
    download_col1, download_col2 = st.columns(2)
    
    with download_col1:
        st.download_button(
            label="📋 Download Input Parameters",
            data=export_data['inputs'].to_csv(index=False),
            file_name=f"aerorent_inputs_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
        
        st.download_button(
            label="📈 Download Projections",
            data=export_data['projections'].to_csv(index=False),
            file_name=f"aerorent_projections_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with download_col2:
        st.download_button(
            label="🎯 Download Key Metrics",
            data=export_data['metrics'].to_csv(index=False),
            file_name=f"aerorent_metrics_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
        
        st.download_button(
            label="💰 Download Cost Breakdown",
            data=export_data['cost_breakdown'].to_csv(index=False),
            file_name=f"aerorent_costs_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Key Metrics Section
    st.subheader("5. Key Metrics")
    
    # First row of metrics (3 boxes)
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Total First-Year Costs</h4>
            <h2>£{results['total_first_year_costs']:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Avg. Revenue per Day</h4>
            <h2>£{results['weighted_avg_revenue']:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Contribution Margin</h4>
            <h2>£{results['contribution_margin']:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Second row of metrics (3 boxes)
    metric_col4, metric_col5, metric_col6 = st.columns(3)
    
    with metric_col4:
        st.markdown(f"""
        <div class="metric-card break-even-highlight">
            <h4>Break-Even Days</h4>
            <h2>{results['break_even_days']:.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col5:
        st.markdown(f"""
        <div class="metric-card break-even-highlight">
            <h4>Break-Even Utilisation</h4>
            <h2>{results['break_even_utilisation']:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col6:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Total Available Days</h4>
            <h2>{results['total_available_days']:,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Projections table
    st.subheader("6. Annual Projections")
    
    def calculate_projection(utilisation):
        rental_days = results['total_available_days'] * (utilisation / 100.0)
        total_revenue = rental_days * results['weighted_avg_revenue']
        total_variable_costs = rental_days * results['variable_cost_per_rental']
        profit = total_revenue - results['opex'] - total_variable_costs - results['capex']
        return {'revenue': total_revenue, 'profit': profit}
    
    projections_data = []
    utilisation_rates = [20, results['break_even_utilisation'], 30, 40]
    
    for util in utilisation_rates:
        if util > 0:
            proj = calculate_projection(util)
            projections_data.append({
                'Utilisation': f"{util:.1f}%",
                'Annual Revenue': f"£{proj['revenue']:,.0f}",
                'Annual Profit': f"£{proj['profit']:,.0f}",
                'Profit_Margin': proj['profit']
            })
    
    df_projections = pd.DataFrame(projections_data)
    
    # Style the dataframe
    def color_profit(val):
        try:
            profit = float(val.replace('£', '').replace(',', ''))
            return 'color: #059669' if profit >= 0 else 'color: #dc2626'
        except:
            return ''
    
    styled_df = df_projections.style.applymap(color_profit, subset=['Annual Profit'])
    st.dataframe(styled_df, use_container_width=True)
    
    # Monthly Revenue Projections Section
    st.subheader("7. Monthly Revenue Projections")
    
    def calculate_monthly_projection(utilisation):
        rental_days = results['total_available_days'] * (utilisation / 100.0)
        total_revenue = rental_days * results['weighted_avg_revenue']
        total_variable_costs = rental_days * results['variable_cost_per_rental']
        
        # Calculate monthly values
        monthly_revenue = total_revenue / 12.0
        monthly_variable_costs = total_variable_costs / 12.0
        monthly_operational_costs = results['opex'] / 12.0
        
        # Monthly profit EXCLUDES capital expenditure (one-time cost)
        monthly_profit = monthly_revenue - monthly_variable_costs - monthly_operational_costs
        monthly_rental_days = rental_days / 12.0
        
        return {
            'monthly_revenue': monthly_revenue,
            'monthly_profit': monthly_profit,
            'monthly_rental_days': monthly_rental_days,
            'monthly_variable_costs': monthly_variable_costs,
            'monthly_operational_costs': monthly_operational_costs,
            'annual_revenue': total_revenue,
            'annual_profit': monthly_profit * 12  # Annual profit excluding capex
        }
    
    # Calculate projections for specified utilisation rates
    monthly_projections_data = []
    target_utilisation_rates = [15, 20, 30]
    
    for util in target_utilisation_rates:
        proj = calculate_monthly_projection(util)
        monthly_projections_data.append({
            'Utilisation Rate': f"{util}%",
            'Monthly Revenue': f"£{proj['monthly_revenue']:,.0f}",
            'Monthly Profit': f"£{proj['monthly_profit']:,.0f}",
            'Monthly Rental Days': f"{proj['monthly_rental_days']:.1f}",
            'Annual Revenue': f"£{proj['annual_revenue']:,.0f}",
            'Annual Profit': f"£{proj['annual_profit']:,.0f}",
            'Profit_Margin': proj['monthly_profit']
        })
    
    df_monthly_projections = pd.DataFrame(monthly_projections_data)
    
    # Style the monthly projections dataframe
    styled_monthly_df = df_monthly_projections.style.applymap(color_profit, subset=['Monthly Profit'])
    st.dataframe(styled_monthly_df, use_container_width=True)
    
    # Add explanatory text
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #4f46e5;">
        <h4>📊 Monthly Revenue Insights:</h4>
        <ul>
            <li><strong>15% Utilisation:</strong> Conservative estimate for initial market entry</li>
            <li><strong>20% Utilisation:</strong> Realistic target for established operations</li>
            <li><strong>30% Utilisation:</strong> Optimistic scenario with strong market demand</li>
        </ul>
        <p><strong>Monthly Profit Calculation:</strong></p>
        <p>Monthly Revenue - Monthly Variable Costs - Monthly Operational Costs</p>
        <p><em>Note: Monthly profit excludes the initial capital expenditure (£2,918.81) as this is a one-time startup cost.</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cost Breakdown Section
    st.subheader("8. Cost Breakdown")
    
    # Calculate costs
    capex = results['capex']
    opex = results['opex']
    additional_costs = sum(cost["amount"] for cost in st.session_state.get('additional_costs', []))
    
    # Initial Expenditure (One-time costs)
    initial_expenditure = capex + additional_costs
    
    # Monthly costs (Annual operational costs / 12)
    monthly_costs = opex / 12.0
    annual_monthly_costs = opex
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Initial Expenditure</h4>
            <h3>£{initial_expenditure:,.2f}</h3>
            <p style="font-size: 0.8rem; color: #6b7280;">One-time startup costs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Monthly Costs</h4>
            <h3>£{monthly_costs:,.2f}</h3>
            <p style="font-size: 0.8rem; color: #6b7280;">£{annual_monthly_costs:,.2f} annually</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Initial Expenditure Details:**")
        st.markdown(f"- Drones & Equipment: £{capex - web_cost - legal_cost:,.2f}")
        st.markdown(f"- Website & Legal: £{web_cost + legal_cost:,.2f}")
        if additional_costs > 0:
            st.markdown(f"- Additional Costs: £{additional_costs:,.2f}")
    
    with col2:
        st.markdown("**Monthly Operational Costs:**")
        st.markdown(f"- Platform & Hosting: £{(platform_cost + domain_cost) / 12:,.2f}")
        st.markdown(f"- Insurance & CAA: £{(insurance_cost + caa_cost) / 12:,.2f}")
        st.markdown(f"- Marketing: £{marketing_cost / 12:,.2f}")
        st.markdown(f"- Repairs & Supplies: £{(repairs_cost + shipping_supplies_cost) / 12:,.2f}")
    
    # Charts
    st.subheader("9. Visual Analysis")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Revenue vs Utilisation chart
        utilisation_range = list(range(10, 51, 5))
        revenue_data = []
        profit_data = []
        
        for util in utilisation_range:
            proj = calculate_projection(util)
            revenue_data.append(proj['revenue'])
            profit_data.append(proj['profit'])
        
        fig_revenue = go.Figure()
        fig_revenue.add_trace(go.Scatter(
            x=utilisation_range,
            y=revenue_data,
            mode='lines+markers',
            name='Annual Revenue',
            line=dict(color='#4f46e5', width=3)
        ))
        fig_revenue.add_trace(go.Scatter(
            x=utilisation_range,
            y=profit_data,
            mode='lines+markers',
            name='Annual Profit',
            line=dict(color='#059669', width=3)
        ))
        
        fig_revenue.update_layout(
            title='Revenue & Profit vs Utilisation Rate',
            xaxis_title='Utilisation Rate (%)',
            yaxis_title='Amount (£)',
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with chart_col2:
        # Cost breakdown pie chart
        cost_data = {
            'DJI Flips': flip_qty * flip_cost,
            'DJI Mini 4 Pros': mini4_qty * mini4_cost,
            'Accessories': case_cost + battery_cost + filter_cost,
            'Website & Legal': web_cost + legal_cost,
            'Annual Opex': results['opex']
        }
        
        fig_costs = px.pie(
            values=list(cost_data.values()),
            names=list(cost_data.keys()),
            title='Cost Breakdown',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_costs.update_layout(height=400)
        
        st.plotly_chart(fig_costs, use_container_width=True)

else:
    st.warning("Please adjust the rental mix percentages to equal 100% to see calculations.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 1rem;'>
    <p>🚁 AeroRent UK Financial Calculator | Built with Streamlit</p>
    <p>Last updated: """ + datetime.now().strftime("%B %d, %Y") + """</p>
</div>
""", unsafe_allow_html=True) 
