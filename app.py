import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

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
        flip_qty = st.number_input("DJI Flips (Qty)", min_value=0, value=3, step=1)
        mini4_qty = st.number_input("DJI Mini 4 Pros (Qty)", min_value=0, value=1, step=1)
        case_cost = st.number_input("Hard Cases Cost (£)", min_value=0, value=200, step=10)
        battery_cost = st.number_input("Extra Batteries Cost (£)", min_value=0, value=236, step=10)
        filter_cost = st.number_input("ND Filters Cost (£)", min_value=0, value=180, step=10)
    
    with col2:
        flip_cost = st.number_input("DJI Flip Cost (£)", min_value=0, value=659, step=10)
        mini4_cost = st.number_input("DJI Mini 4 Pro Cost (£)", min_value=0, value=979, step=10)
        web_cost = st.number_input("Website Setup Cost (£)", min_value=0, value=2500, step=100)
        legal_cost = st.number_input("Legal Fees (£)", min_value=0, value=500, step=50)
    
    # Operational Expenditure
    st.subheader("2. Annual Operational Costs")
    
    col1, col2 = st.columns(2)
    with col1:
        platform_cost = st.number_input("E-commerce Platform (£)", min_value=0, value=228, step=10)
        insurance_cost = st.number_input("Corporate Insurance (£)", min_value=0, value=750, step=50)
        marketing_cost = st.number_input("Digital Marketing (£)", min_value=0, value=6000, step=500)
        shipping_supplies_cost = st.number_input("Shipping Supplies (£)", min_value=0, value=1200, step=100)
    
    with col2:
        domain_cost = st.number_input("Domain & Hosting (£)", min_value=0, value=30, step=5)
        caa_cost = st.number_input("CAA Renewal (£)", min_value=0.0, value=11.79, step=1.0)
        repairs_cost = st.number_input("Repairs & Maintenance (£)", min_value=0, value=295.60, step=10)
        shipping_cost = st.number_input("Shipping Cost per Rental (£)", min_value=0, value=32, step=1)
    
    processing_fee = st.number_input("Payment Processing Fee (%)", min_value=0.0, value=1.5, step=0.1)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Pricing Strategy
    st.subheader("3. Pricing & Revenue Strategy")
    
    pricing_col1, pricing_col2 = st.columns(2)
    
    with pricing_col1:
        st.markdown("**DJI Flip Pricing (£)**")
        flip_daily = st.number_input("Daily Hire", min_value=0, value=49, step=1, key="flip_daily")
        flip_weekend = st.number_input("Weekend Hire", min_value=0, value=85, step=1, key="flip_weekend")
        flip_weekly = st.number_input("Weekly Hire", min_value=0, value=165, step=5, key="flip_weekly")
    
    with pricing_col2:
        st.markdown("**DJI Mini 4 Pro Pricing (£)**")
        mini4_daily = st.number_input("Daily Hire", min_value=0, value=65, step=1, key="mini4_daily")
        mini4_weekend = st.number_input("Weekend Hire", min_value=0, value=109, step=1, key="mini4_weekend")
        mini4_weekly = st.number_input("Weekly Hire", min_value=0, value=210, step=5, key="mini4_weekly")
    
    # Rental Mix
    st.markdown("**Rental Mix Assumption (%)**")
    mix_col1, mix_col2, mix_col3 = st.columns(3)
    
    with mix_col1:
        mix_daily = st.number_input("Daily", min_value=0, max_value=100, value=40, step=5, key="mix_daily")
    with mix_col2:
        mix_weekend = st.number_input("Weekend", min_value=0, max_value=100, value=40, step=5, key="mix_weekend")
    with mix_col3:
        mix_weekly = st.number_input("Weekly", min_value=0, max_value=100, value=20, step=5, key="mix_weekly")
    
    # Validate rental mix
    mix_total = mix_daily + mix_weekend + mix_weekly
    if mix_total != 100:
        st.error(f"⚠️ Rental mix percentages add up to {mix_total}%. Must equal 100%.")
    else:
        st.success("✅ Rental mix percentages are valid!")

# Calculations
def calculate_financials():
    # Capital Expenditure
    total_drones = flip_qty + mini4_qty
    capex = (flip_qty * flip_cost) + (mini4_qty * mini4_cost) + case_cost + battery_cost + filter_cost + web_cost + legal_cost
    
    # Operational Expenditure
    opex = platform_cost + domain_cost + insurance_cost + caa_cost + marketing_cost + repairs_cost + shipping_supplies_cost
    total_first_year_costs = capex + opex
    
    # Revenue & Margin
    mix_daily_pct = mix_daily / 100
    mix_weekend_pct = mix_weekend / 100
    mix_weekly_pct = mix_weekly / 100
    
    flip_avg_rev = (flip_daily * mix_daily_pct) + (flip_weekend * mix_weekend_pct) + (flip_weekly * mix_weekly_pct)
    mini4_avg_rev = (mini4_daily * mix_daily_pct) + (mini4_weekend * mix_weekend_pct) + (mini4_weekly * mix_weekly_pct)
    
    flip_ratio = flip_qty / total_drones if total_drones > 0 else 0
    mini4_ratio = mini4_qty / total_drones if total_drones > 0 else 0
    
    weighted_avg_revenue = (flip_avg_rev * flip_ratio) + (mini4_avg_rev * mini4_ratio)
    
    processing_cost = weighted_avg_revenue * (processing_fee / 100)
    variable_cost_per_rental = shipping_cost + processing_cost
    contribution_margin = weighted_avg_revenue - variable_cost_per_rental
    
    # Break-Even Analysis
    break_even_days = total_first_year_costs / contribution_margin if contribution_margin > 0 else 0
    total_available_days = total_drones * 365
    break_even_utilisation = (break_even_days / total_available_days * 100) if total_available_days > 0 else 0
    
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

# Calculate and display results
if mix_total == 100:
    results = calculate_financials()
    
    with col2:
        st.subheader("4. Key Metrics")
        
        # Key metrics cards
        st.markdown(f"""
        <div class="metric-card">
            <h4>Total First-Year Costs</h4>
            <h2>£{results['total_first_year_costs']:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>Avg. Revenue per Day</h4>
            <h2>£{results['weighted_avg_revenue']:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>Contribution Margin</h4>
            <h2>£{results['contribution_margin']:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card break-even-highlight">
            <h4>Break-Even Days</h4>
            <h2>{results['break_even_days']:.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card break-even-highlight">
            <h4>Break-Even Utilisation</h4>
            <h2>{results['break_even_utilisation']:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)

    # Projections table
    st.subheader("5. Annual Projections")
    
    def calculate_projection(utilisation):
        rental_days = results['total_available_days'] * (utilisation / 100)
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
    
    # Charts
    st.subheader("6. Visual Analysis")
    
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
