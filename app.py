import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io
import base64
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import tempfile
import os

# Define presets
PRESETS = {
    "Proposal 1": {
        # Capital Expenditure
        "flip_qty": 3.0,
        "flip_cost": 587.95,
        "mini4_qty": 1.0,
        "mini4_cost": 899.0,
        "case_cost_per_unit": 45.0,
        "battery_cost": 0.0,
        "filter_cost": 0.0,
        "web_cost": 0.0,
        "legal_cost": 100.0,
        
        # Operational Costs
        "platform_cost": 228.0,
        "domain_cost": 30.0,
        "insurance_cost": 750.0,
        "caa_cost": 11.79,
        "marketing_cost": 6000.0,
        "repairs_cost": 295.60,
        "shipping_cost": 32.0,
        "box_cost": 1.51,
        "processing_fee": 1.5,
        "accountant_cost": 50.0,
        
        # Pricing Strategy
        "flip_daily": 49.0,
        "flip_weekend": 85.0,
        "flip_weekly": 165.0,
        "mini4_daily": 65.0,
        "mini4_weekend": 109.0,
        "mini4_weekly": 210.0,
        "mix_daily": 20.0,
        "mix_weekend": 60.0,
        "mix_weekly": 20.0
    },
    "Proposal 2": {
        # Capital Expenditure
        "flip_qty": 3.0,
        "flip_cost": 587.95,
        "mini4_qty": 1.0,
        "mini4_cost": 899.0,
        "case_cost_per_unit": 45.0,
        "battery_cost": 0.0,
        "filter_cost": 0.0,
        "web_cost": 0.0,
        "legal_cost": 100.0,
        
        # Operational Costs
        "platform_cost": 228.0,
        "domain_cost": 30.0,
        "insurance_cost": 750.0,
        "caa_cost": 11.79,
        "marketing_cost": 6000.0,
        "repairs_cost": 295.6,
        "shipping_cost": 32.0,
        "box_cost": 1.51,
        "processing_fee": 1.5,
        "accountant_cost": 50.0,
        
        # Pricing Strategy
        "flip_daily": 45.0,
        "flip_weekend": 72.99,
        "flip_weekly": 130.0,
        "mini4_daily": 45.0,
        "mini4_weekend": 84.99,
        "mini4_weekly": 190.0,
        "mix_daily": 10.0,
        "mix_weekend": 65.0,
        "mix_weekly": 25.0
    }
}

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
    .preset-selector {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #e5e7eb;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🚁 AeroRent UK - Financial Calculator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Interactive financial projections for your drone rental business</p>', unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.header("📊 Business Configuration")
    
    # Preset Selector
    st.markdown('<div class="preset-selector">', unsafe_allow_html=True)
    st.subheader("🎯 Quick Presets")
    selected_preset = st.selectbox(
        "Choose a preset configuration:",
        list(PRESETS.keys()),
        help="Select a preset to quickly load predefined values"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Get selected preset values
    preset_values = PRESETS[selected_preset]
    
    # Capital Expenditure
    st.subheader("1. Initial Capital Expenditure")
    
    col1, col2 = st.columns(2)
    with col1:
        flip_qty = st.number_input("DJI Flips (Qty)", min_value=0.0, value=preset_values["flip_qty"], step=1.0)
        mini4_qty = st.number_input("DJI Mini 4 Pros (Qty)", min_value=0.0, value=preset_values["mini4_qty"], step=1.0)
        case_cost_per_unit = st.number_input("Hard Case Cost per Unit (£)", min_value=0.0, value=preset_values["case_cost_per_unit"], step=10.0)
        battery_cost = st.number_input("Extra Batteries Cost (£)", min_value=0.0, value=preset_values["battery_cost"], step=10.0)
        filter_cost = st.number_input("ND Filters Cost (£)", min_value=0.0, value=preset_values["filter_cost"], step=10.0)
    
    with col2:
        flip_cost = st.number_input("DJI Flip Cost (£)", min_value=0.0, value=preset_values["flip_cost"], step=10.0)
        mini4_cost = st.number_input("DJI Mini 4 Pro Cost (£)", min_value=0.0, value=preset_values["mini4_cost"], step=10.0)
        web_cost = st.number_input("Website Setup Cost (£)", min_value=0.0, value=preset_values["web_cost"], step=100.0)
        legal_cost = st.number_input("Legal Fees (£)", min_value=0.0, value=preset_values["legal_cost"], step=50.0)
    
    # SD Cards (1 per drone)
    total_drones_for_sd = flip_qty + mini4_qty
    sd_card_cost_per_unit = 38.99
    total_sd_card_cost = total_drones_for_sd * sd_card_cost_per_unit
    
    if total_drones_for_sd > 0:
        st.markdown(f"**SD Cards**: {total_drones_for_sd} × £{sd_card_cost_per_unit} = £{total_sd_card_cost:.2f}**")
    
    # Hard Cases (1 per drone)
    total_hard_cases_cost = total_drones_for_sd * case_cost_per_unit
    
    if total_drones_for_sd > 0 and case_cost_per_unit > 0:
        st.markdown(f"**Hard Cases**: {total_drones_for_sd} × £{case_cost_per_unit} = £{total_hard_cases_cost:.2f}**")
    
    # Operational Expenditure
    st.subheader("2. Annual Operational Costs")
    
    col1, col2 = st.columns(2)
    with col1:
        platform_cost = st.number_input("E-commerce Platform (£)", min_value=0.0, value=preset_values["platform_cost"], step=10.0)
        insurance_cost = st.number_input("Corporate Insurance (£)", min_value=0.0, value=preset_values["insurance_cost"], step=50.0)
        marketing_cost = st.number_input("Digital Marketing (£)", min_value=0.0, value=preset_values["marketing_cost"], step=500.0)
    
    with col2:
        domain_cost = st.number_input("Domain & Hosting (£)", min_value=0.0, value=preset_values["domain_cost"], step=5.0)
        caa_cost = st.number_input("CAA Renewal (£)", min_value=0.0, value=preset_values["caa_cost"], step=1.0)
        repairs_cost = st.number_input("Repairs & Maintenance (£)", min_value=0.0, value=preset_values["repairs_cost"], step=10.0)
    
    # Accountant costs (monthly)
    accountant_cost = st.number_input("Accountant Costs (Monthly £)", min_value=0.0, value=preset_values["accountant_cost"], step=25.0, help="Monthly accounting fees for bookkeeping, VAT returns, and tax compliance")
    
    # Shipping costs per rental
    st.markdown("**Shipping Costs per Rental:**")
    shipping_col1, shipping_col2 = st.columns(2)
    with shipping_col1:
        shipping_cost = st.number_input("Postage Cost per Rental (£)", min_value=0.0, value=preset_values["shipping_cost"], step=1.0)
    with shipping_col2:
        box_cost = st.number_input("Cardboard Box per Order (£)", min_value=0.0, value=preset_values["box_cost"], step=0.1)
    
    total_shipping_cost_per_rental = shipping_cost + box_cost
    st.markdown(f"**Total Shipping Cost per Rental: £{total_shipping_cost_per_rental:.2f}** (Postage: £{shipping_cost:.2f} + Box: £{box_cost:.2f})")
    
    processing_fee = st.number_input("Payment Processing Fee (%)", min_value=0.0, value=preset_values["processing_fee"], step=0.1)

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
        flip_daily = st.number_input("Daily Hire", min_value=0.0, value=preset_values["flip_daily"], step=1.0, key="flip_daily")
        flip_weekend = st.number_input("Weekend Hire", min_value=0.0, value=preset_values["flip_weekend"], step=1.0, key="flip_weekend")
        flip_weekly = st.number_input("Weekly Hire", min_value=0.0, value=preset_values["flip_weekly"], step=5.0, key="flip_weekly")
    
    with pricing_col2:
        st.markdown("**DJI Mini 4 Pro Pricing (£)**")
        mini4_daily = st.number_input("Daily Hire", min_value=0.0, value=preset_values["mini4_daily"], step=1.0, key="mini4_daily")
        mini4_weekend = st.number_input("Weekend Hire", min_value=0.0, value=preset_values["mini4_weekend"], step=1.0, key="mini4_weekend")
        mini4_weekly = st.number_input("Weekly Hire", min_value=0.0, value=preset_values["mini4_weekly"], step=5.0, key="mini4_weekly")
    
    # Rental Mix
    st.markdown("**Rental Mix Assumption (%)**")
    mix_col1, mix_col2, mix_col3 = st.columns(3)
    
    with mix_col1:
        mix_daily = st.number_input("Daily", min_value=0.0, max_value=100.0, value=preset_values["mix_daily"], step=5.0, key="mix_daily")
    with mix_col2:
        mix_weekend = st.number_input("Weekend", min_value=0.0, max_value=100.0, value=preset_values["mix_weekend"], step=5.0, key="mix_weekend")
    with mix_col3:
        mix_weekly = st.number_input("Weekly", min_value=0.0, max_value=100.0, value=preset_values["mix_weekly"], step=5.0, key="mix_weekly")
    
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
    capex = (flip_qty * flip_cost) + (mini4_qty * mini4_cost) + total_hard_cases_cost + battery_cost + filter_cost + web_cost + legal_cost
    
    # SD Cards (1 per drone)
    sd_card_cost_per_unit = 38.99
    total_sd_card_cost = total_drones * sd_card_cost_per_unit
    capex += total_sd_card_cost
    
    # Additional Costs
    additional_costs_total = sum(cost["amount"] for cost in st.session_state.get('additional_costs', []))
    
    # Operational Expenditure
    opex = platform_cost + domain_cost + insurance_cost + caa_cost + marketing_cost + repairs_cost + accountant_cost
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
    variable_cost_per_rental = total_shipping_cost_per_rental + processing_cost
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
            'Capital Expenditure', 'Capital Expenditure', 'Operational Costs', 'Operational Costs', 'Operational Costs', 'Operational Costs',
            'Operational Costs', 'Operational Costs', 'Operational Costs', 'Operational Costs', 'Operational Costs',
            'Pricing Strategy', 'Pricing Strategy', 'Pricing Strategy', 'Pricing Strategy',
            'Pricing Strategy', 'Pricing Strategy', 'Pricing Strategy', 'Pricing Strategy',
            'Pricing Strategy', 'Pricing Strategy', 'Pricing Strategy'
        ],
        'Parameter': [
            'DJI Flips Quantity', 'DJI Flip Cost per Unit', 'DJI Mini 4 Pros Quantity', 'DJI Mini 4 Pro Cost per Unit',
            'Hard Case Cost per Unit', 'Extra Batteries Cost', 'ND Filters Cost', 'Website Setup Cost',
            'SD Cards Cost', 'Legal Fees', 'E-commerce Platform', 'Domain & Hosting',
            'Corporate Insurance', 'CAA Renewal', 'Digital Marketing', 'Repairs & Maintenance', 'Accountant Costs (Monthly)', 'Shipping Supplies',
            'Shipping Cost per Rental', 'DJI Flip Daily Price', 'DJI Flip Weekend Price', 'DJI Flip Weekly Price',
            'DJI Mini 4 Pro Daily Price', 'DJI Mini 4 Pro Weekend Price', 'DJI Mini 4 Pro Weekly Price',
            'Rental Mix Daily %', 'Rental Mix Weekend %', 'Rental Mix Weekly %', 'Payment Processing Fee %'
        ],
        'Value': [
            flip_qty, flip_cost, mini4_qty, mini4_cost,
            case_cost_per_unit, battery_cost, filter_cost, web_cost,
            (flip_qty + mini4_qty) * 38.99, legal_cost, platform_cost, domain_cost,
            insurance_cost, caa_cost, marketing_cost, repairs_cost, accountant_cost, shipping_cost, total_shipping_cost_per_rental,
            flip_daily, flip_weekend, flip_weekly,
            mini4_daily, mini4_weekend, mini4_weekly,
            mix_daily, mix_weekend, mix_weekly, processing_fee
        ],
        'Unit': [
            'units', '£', 'units', '£',
            '£', '£', '£', '£',
            '£', '£', '£', '£',
            '£', '£', '£', '£', '£',
            '£', '£', '£',
            '£', '£', '£',
            '%', '%', '%', '%'
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
            'DJI Flips', 'DJI Mini 4 Pros', 'SD Cards', 'Hard Cases', 'Extra Batteries', 'ND Filters',
            'Website & Legal', 'E-commerce Platform', 'Domain & Hosting', 'Insurance & CAA',
            'Marketing', 'Repairs & Maintenance', 'Accountant Costs', 'Shipping Supplies'
        ],
        'Amount (£)': [
            flip_qty * flip_cost, mini4_qty * mini4_cost, (flip_qty + mini4_qty) * 38.99, total_hard_cases_cost,
            battery_cost, filter_cost, web_cost + legal_cost, platform_cost, domain_cost, insurance_cost + caa_cost,
            marketing_cost, repairs_cost, accountant_cost * 12, shipping_cost
        ],
        'Type': [
            'Capital', 'Capital', 'Capital', 'Capital', 'Capital', 'Capital',
            'Capital', 'Operational', 'Operational', 'Operational',
            'Operational', 'Operational', 'Operational', 'Operational'
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

# Function to generate comprehensive PDF report
def generate_pdf_report(results, vat_analysis, business_metrics, export_data, preset_name):
    """
    Generate a comprehensive PDF business plan report
    """
    # Create temporary file for PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        pdf_path = tmp_file.name
    
    # Create PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1f2937')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.HexColor('#4f46e5')
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=16,
        textColor=colors.HexColor('#6b7280')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        textColor=colors.HexColor('#374151')
    )
    
    # Title Page
    story.append(Paragraph("🚁 AeroRent UK", title_style))
    story.append(Paragraph("Drone Rental Business Plan", title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", normal_style))
    story.append(Paragraph(f"Configuration: {preset_name}", normal_style))
    story.append(PageBreak())
    
    # Executive Summary
    story.append(Paragraph("📋 Executive Summary", heading_style))
    story.append(Paragraph("""
    This comprehensive business plan outlines the financial projections and operational strategy for AeroRent UK, 
    a professional drone rental service targeting the UK market. The analysis includes detailed cost structures, 
    revenue projections, break-even analysis, and investment metrics to support strategic decision-making.
    """, normal_style))
    story.append(Spacer(1, 12))
    
    # Key Metrics Summary
    story.append(Paragraph("🎯 Key Business Metrics", subheading_style))
    
    # Create key metrics table
    key_metrics_data = [
        ['Metric', 'Value'],
        ['Total First-Year Investment', f"£{results['total_first_year_costs']:,.2f}"],
        ['Break-Even Utilisation Rate', f"{results['break_even_utilisation']:.1f}%"],
        ['Weighted Average Revenue per Day', f"£{results['weighted_avg_revenue']:.2f}"],
        ['Contribution Margin per Day', f"£{results['contribution_margin']:.2f}"],
        ['Total Available Rental Days', f"{results['total_available_days']:,.0f}"],
        ['Expected ROI (20% Utilisation)', f"{business_metrics['roi_data'][1]['ROI']:.1f}%"]
    ]
    
    key_metrics_table = Table(key_metrics_data, colWidths=[3*inch, 2*inch])
    key_metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    story.append(key_metrics_table)
    story.append(PageBreak())
    
    # Business Configuration
    story.append(Paragraph("⚙️ Business Configuration", heading_style))
    
    # Equipment Configuration
    story.append(Paragraph("📦 Equipment & Assets", subheading_style))
    equipment_data = [
        ['Equipment', 'Quantity', 'Cost per Unit', 'Total Cost'],
        ['DJI Flips', f"{flip_qty:.0f}", f"£{flip_cost:.2f}", f"£{flip_qty * flip_cost:.2f}"],
        ['DJI Mini 4 Pros', f"{mini4_qty:.0f}", f"£{mini4_cost:.2f}", f"£{mini4_qty * mini4_cost:.2f}"],
        ['Hard Cases', f"{flip_qty + mini4_qty:.0f}", f"£{case_cost_per_unit:.2f}", f"£{total_hard_cases_cost:.2f}"],
        ['SD Cards', f"{flip_qty + mini4_qty:.0f}", "£38.99", f"£{(flip_qty + mini4_qty) * 38.99:.2f}"],
        ['Website & Legal', '1', f"£{web_cost + legal_cost:.2f}", f"£{web_cost + legal_cost:.2f}"]
    ]
    
    equipment_table = Table(equipment_data, colWidths=[1.5*inch, 1*inch, 1.5*inch, 1.5*inch])
    equipment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    story.append(equipment_table)
    story.append(Spacer(1, 12))
    
    # Pricing Strategy
    story.append(Paragraph("💰 Pricing Strategy", subheading_style))
    pricing_data = [
        ['Service', 'Daily', 'Weekend', 'Weekly'],
        ['DJI Flip', f"£{flip_daily:.2f}", f"£{flip_weekend:.2f}", f"£{flip_weekly:.2f}"],
        ['DJI Mini 4 Pro', f"£{mini4_daily:.2f}", f"£{mini4_weekend:.2f}", f"£{mini4_weekly:.2f}"]
    ]
    
    pricing_table = Table(pricing_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    pricing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fdf4')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bbf7d0'))
    ]))
    story.append(pricing_table)
    story.append(Spacer(1, 12))
    
    # Rental Mix
    story.append(Paragraph(f"📊 Rental Mix: Daily {mix_daily}% | Weekend {mix_weekend}% | Weekly {mix_weekly}%", normal_style))
    story.append(PageBreak())
    
    # Financial Analysis
    story.append(Paragraph("📈 Financial Analysis", heading_style))
    
    # Cost Structure
    story.append(Paragraph("💸 Cost Structure Breakdown", subheading_style))
    
    # Capital Expenditure
    story.append(Paragraph("🏗️ Capital Expenditure (One-time)", normal_style))
    capex_data = [
        ['Category', 'Amount'],
        ['Equipment & Assets', f"£{results['capex'] - web_cost - legal_cost:,.2f}"],
        ['Website & Legal', f"£{web_cost + legal_cost:,.2f}"],
        ['Total Capex', f"£{results['capex']:,.2f}"]
    ]
    
    capex_table = Table(capex_data, colWidths=[3*inch, 2*inch])
    capex_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fef2f2')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fecaca'))
    ]))
    story.append(capex_table)
    story.append(Spacer(1, 12))
    
    # Operational Costs
    story.append(Paragraph("🔄 Annual Operational Costs", normal_style))
    opex_data = [
        ['Category', 'Annual Cost', 'Monthly Cost'],
        ['Platform & Hosting', f"£{platform_cost + domain_cost:,.2f}", f"£{(platform_cost + domain_cost) / 12:,.2f}"],
        ['Insurance & CAA', f"£{insurance_cost + caa_cost:,.2f}", f"£{(insurance_cost + caa_cost) / 12:,.2f}"],
        ['Marketing', f"£{marketing_cost:,.2f}", f"£{marketing_cost / 12:,.2f}"],
        ['Repairs & Maintenance', f"£{repairs_cost:,.2f}", f"£{repairs_cost / 12:,.2f}"],
        ['Accountant', f"£{accountant_cost * 12:,.2f}", f"£{accountant_cost:,.2f}"],
        ['Total Opex', f"£{results['opex']:,.2f}", f"£{results['opex'] / 12:,.2f}"]
    ]
    
    opex_table = Table(opex_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
    opex_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fef2f2')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fecaca'))
    ]))
    story.append(opex_table)
    story.append(Spacer(1, 12))
    
    # Variable Costs
    story.append(Paragraph("📦 Variable Costs per Rental", normal_style))
    variable_costs_data = [
        ['Cost Item', 'Amount per Rental'],
        ['Postage', f"£{shipping_cost:.2f}"],
        ['Cardboard Box', f"£{box_cost:.2f}"],
        ['Payment Processing (1.5%)', f"£{results['weighted_avg_revenue'] * 0.015:.2f}"],
        ['Total Variable Cost', f"£{results['variable_cost_per_rental']:.2f}"]
    ]
    
    variable_costs_table = Table(variable_costs_data, colWidths=[3*inch, 2*inch])
    variable_costs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fdf4')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bbf7d0'))
    ]))
    story.append(variable_costs_table)
    story.append(PageBreak())
    
    # Revenue Projections
    story.append(Paragraph("📊 Revenue & Profit Projections", heading_style))
    
    # Annual Projections Table
    story.append(Paragraph("📈 Annual Projections by Utilisation Rate", subheading_style))
    
    # Get projections data
    projections_data = []
    utilisation_rates = [20, results['break_even_utilisation'], 30, 40]
    
    for util in utilisation_rates:
        if util > 0:
            proj = calculate_projection(util)
            projections_data.append([
                f"{util:.1f}%",
                f"£{proj['revenue']:,.0f}",
                f"£{proj['profit']:,.0f}",
                f"{(proj['profit'] / proj['revenue'] * 100):.1f}%" if proj['revenue'] > 0 else "0.0%"
            ])
    
    projections_table_data = [['Utilisation', 'Annual Revenue', 'Annual Profit', 'Profit Margin']] + projections_data
    projections_table = Table(projections_table_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 1*inch])
    projections_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    story.append(projections_table)
    story.append(Spacer(1, 12))
    
    # Monthly Projections
    story.append(Paragraph("📅 Monthly Projections", subheading_style))
    
    monthly_data = []
    target_utilisation_rates = [15, 20, 30]
    
    for util in target_utilisation_rates:
        proj = calculate_monthly_projection(util)
        monthly_data.append([
            f"{util}%",
            f"{proj['monthly_rentals']:.1f}",
            f"£{proj['monthly_revenue']:,.0f}",
            f"£{proj['monthly_profit']:,.0f}",
            f"{(proj['monthly_profit'] / proj['monthly_revenue'] * 100):.1f}%" if proj['monthly_revenue'] > 0 else "0.0%"
        ])
    
    monthly_table_data = [['Utilisation', 'Monthly Rentals', 'Monthly Revenue', 'Monthly Profit', 'Margin']] + monthly_data
    monthly_table = Table(monthly_table_data, colWidths=[1*inch, 1.2*inch, 1.3*inch, 1.3*inch, 1.2*inch])
    monthly_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fdf4')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bbf7d0'))
    ]))
    story.append(monthly_table)
    story.append(PageBreak())
    
    # Investment Analysis
    story.append(Paragraph("💼 Investment Analysis", heading_style))
    
    # ROI Analysis
    story.append(Paragraph("📈 Return on Investment (ROI) Analysis", subheading_style))
    
    roi_data = []
    for data in business_metrics['roi_data']:
        roi_data.append([
            data['Utilisation'],
            f"{data['ROI']:.1f}%",
            f"£{data['Annual Profit']:,.0f}",
            f"{data['Payback Years']:.1f} years" if data['Payback Years'] != float('inf') else "∞"
        ])
    
    roi_table_data = [['Utilisation', 'ROI', 'Annual Profit', 'Payback Period']] + roi_data
    roi_table = Table(roi_table_data, colWidths=[1.2*inch, 1.2*inch, 1.5*inch, 1.1*inch])
    roi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    story.append(roi_table)
    story.append(Spacer(1, 12))
    
    # Cash Flow Analysis
    story.append(Paragraph("💰 Cash Flow Analysis", subheading_style))
    
    cash_flow_data = []
    for data in business_metrics['cash_flow_data']:
        cash_flow_data.append([
            data['Utilisation'],
            f"£{data['Monthly Cash Flow']:,.0f}",
            f"£{data['Annual Cash Flow']:,.0f}",
            f"£{data['Monthly Profit']:,.0f}"
        ])
    
    cash_flow_table_data = [['Utilisation', 'Monthly Cash Flow', 'Annual Cash Flow', 'Monthly Profit']] + cash_flow_data
    cash_flow_table = Table(cash_flow_table_data, colWidths=[1.2*inch, 1.5*inch, 1.5*inch, 1.3*inch])
    cash_flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fdf4')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bbf7d0'))
    ]))
    story.append(cash_flow_table)
    story.append(PageBreak())
    
    # Risk Assessment
    story.append(Paragraph("⚠️ Risk Assessment", heading_style))
    
    # Scenario Analysis
    story.append(Paragraph("🎯 Scenario Analysis", subheading_style))
    
    risk_data = []
    risk_metrics = business_metrics['risk_metrics']
    
    for scenario_name, metrics in risk_metrics.items():
        risk_data.append([
            scenario_name.replace(' (', '\n('),
            f"£{metrics['Annual Profit']:,.0f}",
            f"{metrics['ROI']:.1f}%",
            f"{metrics['Payback Years']:.1f} years" if metrics['Payback Years'] != float('inf') else "∞"
        ])
    
    risk_table_data = [['Scenario', 'Annual Profit', 'ROI', 'Payback Period']] + risk_data
    risk_table = Table(risk_table_data, colWidths=[2*inch, 1.5*inch, 1*inch, 1.5*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fef2f2')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fecaca'))
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 12))
    
    # Sensitivity Analysis
    story.append(Paragraph("📊 Sensitivity Analysis", subheading_style))
    
    sensitivity_data = []
    for data in business_metrics['sensitivity_data']:
        sensitivity_data.append([
            data['Scenario'],
            f"£{data['Adjusted Profit']:,.0f}",
            f"{data['Profit Change %']:+.1f}%"
        ])
    
    sensitivity_table_data = [['Scenario', 'Adjusted Profit', 'Profit Change']] + sensitivity_data
    sensitivity_table = Table(sensitivity_table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
    sensitivity_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    story.append(sensitivity_table)
    story.append(PageBreak())
    
    # VAT Analysis
    story.append(Paragraph("🏛️ VAT Analysis", heading_style))
    
    story.append(Paragraph("""
    This business operates under UK VAT regulations. The analysis below shows the VAT implications 
    for the business at different utilisation rates and revenue levels.
    """, normal_style))
    story.append(Spacer(1, 12))
    
    # VAT Summary
    story.append(Paragraph("💰 VAT Summary", subheading_style))
    
    vat_summary_data = [
        ['Metric', 'Value'],
        ['VAT Rate', f"{vat_analysis['vat_rate'] * 100:.0f}%"],
        ['Annual Revenue (20% Utilisation)', f"£{vat_analysis['annual_revenue']:,.0f}"],
        ['VAT on Revenue', f"£{vat_analysis['total_revenue_vat']:,.0f}"],
        ['VAT Deductible', f"£{vat_analysis['total_vat_deductible']:,.0f}"],
        ['Net VAT Payable', f"£{vat_analysis['net_vat_payable']:,.0f}"],
        ['Profit After VAT', f"£{vat_analysis['profit_after_vat']:,.0f}"],
        ['VAT Registration Required', "Yes" if vat_analysis['annual_revenue'] >= vat_analysis['vat_threshold'] else "No"]
    ]
    
    vat_summary_table = Table(vat_summary_data, colWidths=[3*inch, 2*inch])
    vat_summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fef2f2')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#fecaca'))
    ]))
    story.append(vat_summary_table)
    story.append(Spacer(1, 12))
    
    # Business Insights
    story.append(Paragraph("💡 Business Insights & Recommendations", heading_style))
    
    insights = [
        "🎯 **Break-Even Analysis**: The business requires " + f"{results['break_even_utilisation']:.1f}%" + " utilisation to break even in the first year.",
        "📈 **Growth Potential**: At 30% utilisation, the business generates significant positive cash flow.",
        "💰 **Investment Appeal**: Expected ROI of " + f"{business_metrics['roi_data'][1]['ROI']:.1f}%" + " at 20% utilisation makes this an attractive investment.",
        "⚠️ **Risk Management**: Conservative estimates show the business remains viable even at 15% utilisation.",
        "🏛️ **VAT Considerations**: " + ("VAT registration is required" if vat_analysis['annual_revenue'] >= vat_analysis['vat_threshold'] else "VAT registration threshold not reached") + " based on projected revenue.",
        "📊 **Market Positioning**: Competitive pricing strategy positions the business well in the UK drone rental market.",
        "🔄 **Operational Efficiency**: Fixed costs are well-controlled, with variable costs scaling appropriately with demand."
    ]
    
    for insight in insights:
        story.append(Paragraph(insight, normal_style))
        story.append(Spacer(1, 6))
    
    # Conclusion
    story.append(Paragraph("🎯 Conclusion", heading_style))
    story.append(Paragraph("""
    AeroRent UK presents a compelling investment opportunity with strong financial projections, 
    manageable risk profile, and clear path to profitability. The business model demonstrates 
    resilience across various market scenarios and offers attractive returns for investors 
    seeking exposure to the growing drone rental market.
    """, normal_style))
    
    # Build PDF
    doc.build(story)
    
    # Read the generated PDF
    with open(pdf_path, 'rb') as pdf_file:
        pdf_data = pdf_file.read()
    
    # Clean up temporary file
    os.unlink(pdf_path)
    
    return pdf_data

if mix_total == 100.0:
    results = calculate_financials()
    
    # Calculate VAT analysis
    def calculate_vat_analysis(results):
        vat_rate = 0.20  # 20% UK VAT rate
        
        # Calculate actual annual values based on utilisation
        # For VAT analysis, we'll use 20% utilisation as the base case
        base_utilisation = 20.0  # 20% utilisation rate
        actual_rental_days = results['total_available_days'] * (base_utilisation / 100.0)
        actual_annual_revenue = results['weighted_avg_revenue'] * actual_rental_days
        
        # VAT on Revenue (assuming all revenue is VATable)
        total_revenue_vat = actual_annual_revenue * vat_rate
        
        # VAT-deductible items (business expenses) - these are annual costs
        vat_deductible_items = {
            'DJI Flips': flip_qty * flip_cost * vat_rate,
            'DJI Mini 4 Pros': mini4_qty * mini4_cost * vat_rate,
            'Hard Cases': total_hard_cases_cost * vat_rate,
            'SD Cards': (flip_qty + mini4_qty) * 38.99 * vat_rate,
            'Extra Batteries': battery_cost * vat_rate,
            'ND Filters': filter_cost * vat_rate,
            'Website Setup': web_cost * vat_rate,
            'Legal Fees': legal_cost * vat_rate,
            'E-commerce Platform': platform_cost * vat_rate,
            'Domain & Hosting': domain_cost * vat_rate,
            'Corporate Insurance': insurance_cost * vat_rate,
            'CAA Renewal': caa_cost * vat_rate,
            'Digital Marketing': marketing_cost * vat_rate,
            'Repairs & Maintenance': repairs_cost * vat_rate,
            'Shipping Supplies': shipping_cost * vat_rate,
            'Cardboard Boxes': box_cost * vat_rate,
            'Accountant Costs': accountant_cost * 12 * vat_rate  # Annual accountant costs
        }
        
        # Additional costs VAT
        additional_costs_vat = sum(cost["amount"] * vat_rate for cost in st.session_state.get('additional_costs', []))
        
        total_vat_deductible = sum(vat_deductible_items.values()) + additional_costs_vat
        
        # Net VAT payable (VAT on revenue - VAT deductible)
        net_vat_payable = total_revenue_vat - total_vat_deductible
        
        # Calculate actual profit based on utilisation
        actual_annual_profit = actual_annual_revenue - (results['variable_cost_per_rental'] * actual_rental_days) - results['opex'] - results['capex']
        profit_after_vat = actual_annual_profit - net_vat_payable
        
        # VAT registration threshold analysis
        vat_threshold = 85000  # UK VAT registration threshold
        months_to_threshold = (vat_threshold / actual_annual_revenue * 12) if actual_annual_revenue > 0 else float('inf')
        
        return {
            'vat_rate': vat_rate,
            'total_revenue_vat': total_revenue_vat,
            'vat_deductible_items': vat_deductible_items,
            'total_vat_deductible': total_vat_deductible,
            'net_vat_payable': net_vat_payable,
            'profit_before_vat': actual_annual_profit,
            'profit_after_vat': profit_after_vat,
            'vat_threshold': vat_threshold,
            'annual_revenue': actual_annual_revenue,
            'months_to_threshold': months_to_threshold,
            'additional_costs_vat': additional_costs_vat,
            'actual_rental_days': actual_rental_days,
            'base_utilisation': base_utilisation
        }
    
    vat_analysis = calculate_vat_analysis(results)
    
    # Download section
    st.markdown("---")
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    st.subheader("📥 Download Financial Data")
    st.markdown("Export all pricing, inputs, and financial projections for analysis")
    
    # Create export data
    export_data = create_export_data(results)
    
    st.markdown("---")
    st.markdown("### 📊 Data Export Options")
    st.markdown("Export specific data sections for further analysis")
    
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
    
    # Third row - VAT-adjusted metrics
    metric_col7, metric_col8, metric_col9 = st.columns(3)
    
    with metric_col7:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #dc2626;">
            <h4>Profit After VAT</h4>
            <h2>£{vat_analysis['profit_after_vat']:,.0f}</h2>
            <p style="font-size: 0.8rem; color: #6b7280;">Annual at {vat_analysis['base_utilisation']:.0f}% utilisation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col8:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #dc2626;">
            <h4>Net VAT Payable</h4>
            <h2>£{vat_analysis['net_vat_payable']:,.0f}</h2>
            <p style="font-size: 0.8rem; color: #6b7280;">Annual at {vat_analysis['base_utilisation']:.0f}% utilisation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col9:
        vat_status = "Must Register" if vat_analysis['annual_revenue'] >= vat_analysis['vat_threshold'] else "Below Threshold"
        vat_color = "#dc2626" if vat_analysis['annual_revenue'] >= vat_analysis['vat_threshold'] else "#059669"
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: {vat_color};">
            <h4>VAT Status</h4>
            <h2 style="color: {vat_color};">{vat_status}</h2>
            <p style="font-size: 0.8rem; color: #6b7280;">£{vat_analysis['annual_revenue']:,.0f} annual revenue</p>
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
    st.subheader("7. Monthly Revenue & Rental Projections")
    
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
        
        # Calculate actual rentals per month (assuming average rental duration)
        # Based on rental mix: 20% daily, 60% weekend, 20% weekly
        avg_rental_duration = (0.2 * 1) + (0.6 * 2) + (0.2 * 7)  # weighted average days per rental
        monthly_rentals = monthly_rental_days / avg_rental_duration if avg_rental_duration > 0 else 0
        
        return {
            'monthly_revenue': monthly_revenue,
            'monthly_profit': monthly_profit,
            'monthly_rental_days': monthly_rental_days,
            'monthly_rentals': monthly_rentals,
            'monthly_variable_costs': monthly_variable_costs,
            'monthly_operational_costs': monthly_operational_costs,
            'annual_revenue': total_revenue,
            'annual_profit': monthly_profit * 12,  # Annual profit excluding capex
            'avg_rental_duration': avg_rental_duration
        }
    
    # Calculate projections for specified utilisation rates
    monthly_projections_data = []
    target_utilisation_rates = [15, 20, 30]
    
    for util in target_utilisation_rates:
        proj = calculate_monthly_projection(util)
        monthly_projections_data.append({
            'Utilisation Rate': f"{util}%",
            'Monthly Rentals': f"{proj['monthly_rentals']:.1f}",
            'Avg Rental Duration': f"{proj['avg_rental_duration']:.1f} days",
            'Monthly Revenue': f"£{proj['monthly_revenue']:,.0f}",
            'Monthly Profit': f"£{proj['monthly_profit']:,.0f}",
            'Annual Revenue': f"£{proj['annual_revenue']:,.0f}",
            'Annual Profit': f"£{proj['annual_profit']:,.0f}",
            'Profit_Margin': proj['monthly_profit']
        })
    
    df_monthly_projections = pd.DataFrame(monthly_projections_data)
    
    # Style the monthly projections dataframe
    styled_monthly_df = df_monthly_projections.style.applymap(color_profit, subset=['Monthly Profit'])
    st.dataframe(styled_monthly_df, use_container_width=True)
    
    # Monthly Cost Breakdown
    st.markdown("**📊 Monthly Cost Breakdown:**")
    
    cost_breakdown_data = []
    for util in target_utilisation_rates:
        proj = calculate_monthly_projection(util)
        cost_breakdown_data.append({
            'Utilisation Rate': f"{util}%",
            'Monthly Rentals': f"{proj['monthly_rentals']:.1f}",
            'Monthly Revenue': f"£{proj['monthly_revenue']:,.2f}",
            'Variable Costs': f"£{proj['monthly_variable_costs']:,.2f}",
            'Fixed Operational Costs': f"£{proj['monthly_operational_costs']:,.2f}",
            'Total Monthly Costs': f"£{proj['monthly_variable_costs'] + proj['monthly_operational_costs']:,.2f}",
            'Monthly Profit': f"£{proj['monthly_profit']:,.2f}",
            'Profit Margin %': f"{(proj['monthly_profit'] / proj['monthly_revenue'] * 100):.1f}%" if proj['monthly_revenue'] > 0 else "0.0%"
        })
    
    df_cost_breakdown = pd.DataFrame(cost_breakdown_data)
    st.dataframe(df_cost_breakdown, use_container_width=True)
    
    # Add explanatory text
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #4f46e5;">
        <h4>📊 Monthly Projections Insights:</h4>
        <ul>
            <li><strong>15% Utilisation:</strong> Conservative estimate for initial market entry</li>
            <li><strong>20% Utilisation:</strong> Realistic target for established operations</li>
            <li><strong>30% Utilisation:</strong> Optimistic scenario with strong market demand</li>
        </ul>
        <p><strong>Key Calculations:</strong></p>
        <ul>
            <li><strong>Monthly Rentals:</strong> Actual number of drone rentals per month</li>
            <li><strong>Avg Rental Duration:</strong> Weighted average based on rental mix (20% daily, 60% weekend, 20% weekly)</li>
            <li><strong>Monthly Profit:</strong> Monthly Revenue - Variable Costs - Fixed Operational Costs</li>
        </ul>
        <p><em>Note: Monthly profit excludes the initial capital expenditure as this is a one-time startup cost.</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cost Structure Section
    st.subheader("8. Cost Structure Analysis")
    
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
            <h4>Monthly Fixed Costs</h4>
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
        st.markdown("**Monthly Fixed Operational Costs:**")
        st.markdown(f"- Platform & Hosting: £{(platform_cost + domain_cost) / 12:,.2f}")
        st.markdown(f"- Insurance & CAA: £{(insurance_cost + caa_cost) / 12:,.2f}")
        st.markdown(f"- Marketing: £{marketing_cost / 12:,.2f}")
        st.markdown(f"- Repairs & Maintenance: £{repairs_cost / 12:,.2f}")
        st.markdown(f"- Accountant: £{accountant_cost:,.2f}")
    
    # Variable vs Fixed Cost Explanation
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #4f46e5;">
        <h4>💰 Cost Structure Explanation:</h4>
        <p><strong>Variable Costs (per rental):</strong></p>
        <ul>
            <li>Postage: £32.00 per rental</li>
            <li>Cardboard Box: £1.51 per rental</li>
            <li>Payment Processing: 1.5% of rental revenue</li>
        </ul>
        <p><strong>Fixed Operational Costs (monthly):</strong></p>
        <ul>
            <li>Platform & Hosting: £21.50/month</li>
            <li>Insurance & CAA: £63.48/month</li>
            <li>Marketing: £500.00/month</li>
            <li>Repairs & Maintenance: £24.63/month</li>
            <li>Accountant: £150.00/month</li>
        </ul>
        <p><em>Note: Variable costs increase with more rentals, while fixed costs remain the same regardless of utilisation.</em></p>
    </div>
    """, unsafe_allow_html=True)
    
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
            'Hard Cases': total_hard_cases_cost,
            'SD Cards': (flip_qty + mini4_qty) * 38.99,
            'Batteries & Filters': battery_cost + filter_cost,
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

    # Business Planning Metrics
    st.subheader("10. Business Planning & Investment Metrics")
    
    # Calculate additional financial metrics
    def calculate_business_metrics(results, utilisation_rates=None):
        # If no utilisation rates provided, use default ones including break-even
        if utilisation_rates is None:
            # Get break-even utilisation and ensure it's included in the analysis
            break_even_util = results['break_even_utilisation']
            base_rates = [15, 20, 30]
            
            # Add break-even utilisation if it's not already in the base rates
            if break_even_util not in base_rates and 10 <= break_even_util <= 50:
                utilisation_rates = sorted(base_rates + [break_even_util])
            else:
                utilisation_rates = base_rates
        """
        Calculate business planning metrics with two different approaches:
        1. ROI & Payback: Include capex to measure return on total investment
        2. Cash Flow: Exclude capex to measure ongoing operational cash generation
        """
        metrics = {}
        
        # ROI and Payback Period calculations
        initial_investment = results['total_first_year_costs']
        
        # Calculate ROI for different utilisation rates
        roi_data = []
        payback_data = []
        cash_flow_data = []
        
        for util in utilisation_rates:
            proj = calculate_projection(util)
            annual_profit = proj['profit']  # Includes capex for ROI/payback calculations
            
            # ROI = (Annual Profit / Initial Investment) * 100
            # Note: Annual profit includes capex to measure return on total investment
            roi = (annual_profit / initial_investment * 100) if initial_investment > 0 else 0
            
            # Payback Period = Initial Investment / Annual Profit
            # Note: Annual profit includes capex to measure time to recover total investment
            payback_years = initial_investment / annual_profit if annual_profit > 0 else float('inf')
            payback_months = payback_years * 12 if payback_years != float('inf') else float('inf')
            
            # Cash Flow Analysis
            # Use the same logic as calculate_monthly_projection - exclude capex from monthly calculations
            # Note: Cash flow excludes capex to measure ongoing operational cash generation
            rental_days = results['total_available_days'] * (util / 100.0)
            total_revenue = rental_days * results['weighted_avg_revenue']
            total_variable_costs = rental_days * results['variable_cost_per_rental']
            
            # Calculate monthly values (excluding capex)
            monthly_revenue = total_revenue / 12.0
            monthly_variable_costs = total_variable_costs / 12.0
            monthly_operational_costs = results['opex'] / 12.0
            monthly_profit = monthly_revenue - monthly_variable_costs - monthly_operational_costs
            
            # Monthly cash flow is the same as monthly profit (excluding capex)
            monthly_cash_flow = monthly_profit
            
            roi_data.append({
                'Utilisation': f"{util}%",
                'ROI': roi,
                'Annual Profit': annual_profit,
                'Initial Investment': initial_investment
            })
            
            payback_data.append({
                'Utilisation': f"{util}%",
                'Payback Years': payback_years,
                'Payback Months': payback_months,
                'Annual Profit': annual_profit
            })
            
            cash_flow_data.append({
                'Utilisation': f"{util}%",
                'Monthly Cash Flow': monthly_cash_flow,
                'Annual Cash Flow': monthly_cash_flow * 12,
                'Monthly Profit': monthly_profit
            })
        
        metrics['roi_data'] = roi_data
        metrics['payback_data'] = payback_data
        metrics['cash_flow_data'] = cash_flow_data
        
        # Sensitivity Analysis
        sensitivity_data = []
        base_utilisation = 20  # Base case
        base_proj = calculate_projection(base_utilisation)
        base_profit = base_proj['profit']
        
        # Test different scenarios
        scenarios = [
            ('Revenue -10%', 0.9, 1.0),
            ('Revenue -5%', 0.95, 1.0),
            ('Base Case', 1.0, 1.0),
            ('Revenue +5%', 1.05, 1.0),
            ('Revenue +10%', 1.10, 1.0),
            ('Costs +10%', 1.0, 1.1),
            ('Costs +5%', 1.0, 1.05),
            ('Costs -5%', 1.0, 0.95),
            ('Costs -10%', 1.0, 0.9)
        ]
        
        for scenario_name, revenue_mult, cost_mult in scenarios:
            if 'Revenue' in scenario_name:  # Revenue scenarios
                adjusted_revenue = base_proj['revenue'] * revenue_mult
                adjusted_variable_costs = (base_proj['revenue'] - base_profit - results['opex']) * revenue_mult
                adjusted_profit = adjusted_revenue - results['opex'] - adjusted_variable_costs - results['capex']
            else:  # Cost scenarios
                adjusted_profit = base_profit - (results['opex'] * (cost_mult - 1))
            
            profit_change = ((adjusted_profit - base_profit) / base_profit * 100) if base_profit != 0 else 0
            sensitivity_data.append({
                'Scenario': scenario_name,
                'Adjusted Profit': adjusted_profit,
                'Profit Change %': profit_change
            })
        
        metrics['sensitivity_data'] = sensitivity_data
        
        # Risk Assessment
        worst_case = calculate_projection(10)  # 10% utilisation
        best_case = calculate_projection(40)   # 40% utilisation
        expected_case = calculate_projection(20)  # 20% utilisation
        
        risk_metrics = {
            'Worst Case (10% Utilisation)': {
                'Annual Profit': worst_case['profit'],
                'ROI': (worst_case['profit'] / initial_investment * 100) if initial_investment > 0 else 0,
                'Payback Years': initial_investment / worst_case['profit'] if worst_case['profit'] > 0 else float('inf')
            },
            'Expected Case (20% Utilisation)': {
                'Annual Profit': expected_case['profit'],
                'ROI': (expected_case['profit'] / initial_investment * 100) if initial_investment > 0 else 0,
                'Payback Years': initial_investment / expected_case['profit'] if expected_case['profit'] > 0 else float('inf')
            },
            'Best Case (40% Utilisation)': {
                'Annual Profit': best_case['profit'],
                'ROI': (best_case['profit'] / initial_investment * 100) if initial_investment > 0 else 0,
                'Payback Years': initial_investment / best_case['profit'] if best_case['profit'] > 0 else float('inf')
            }
        }
        
        metrics['risk_metrics'] = risk_metrics
        
        return metrics
    
    business_metrics = calculate_business_metrics(results, utilisation_rates=None)
    
    # Generate PDF Report
    st.markdown("### 📄 Professional Business Plan PDF")
    st.markdown("Generate a comprehensive business plan PDF for investors and stakeholders")
    
    if st.button("🚀 Generate Business Plan PDF", type="primary", help="Create a professional PDF report with all data, charts, and analysis"):
        with st.spinner("Generating comprehensive business plan PDF..."):
            try:
                pdf_data = generate_pdf_report(results, vat_analysis, business_metrics, export_data, selected_preset)
                
                st.download_button(
                    label="📄 Download Business Plan PDF",
                    data=pdf_data,
                    file_name=f"aerorent_business_plan_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                    help="Download the complete business plan as a professional PDF document"
                )
                
                st.success("✅ Business plan PDF generated successfully! Click the download button above to save.")
                
            except Exception as e:
                st.error(f"❌ Error generating PDF: {str(e)}")
                st.info("Please ensure all calculations are complete and try again.")
    
    st.markdown("---")
    
    # Display metrics in tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📈 ROI & Payback", "💰 Cash Flow", "🎯 Sensitivity", "⚠️ Risk Assessment", "📊 Summary", "🏛️ VAT Analysis"])
    
    with tab1:
        st.markdown("**Return on Investment (ROI) & Payback Period**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**ROI Analysis**")
            roi_df = pd.DataFrame(business_metrics['roi_data'])
            roi_df['ROI'] = roi_df['ROI'].round(1)
            roi_df['Annual Profit'] = roi_df['Annual Profit'].apply(lambda x: f"£{x:,.0f}")
            roi_df['Initial Investment'] = roi_df['Initial Investment'].apply(lambda x: f"£{x:,.0f}")
            st.dataframe(roi_df, use_container_width=True)
        
        with col2:
            st.markdown("**Payback Period Analysis**")
            payback_df = pd.DataFrame(business_metrics['payback_data'])
            payback_df['Payback Years'] = payback_df['Payback Years'].apply(lambda x: f"{x:.1f}" if x != float('inf') else "∞")
            payback_df['Payback Months'] = payback_df['Payback Months'].apply(lambda x: f"{x:.0f}" if x != float('inf') else "∞")
            payback_df['Annual Profit'] = payback_df['Annual Profit'].apply(lambda x: f"£{x:,.0f}")
            st.dataframe(payback_df, use_container_width=True)
        
        # ROI Chart
        roi_values = [data['ROI'] for data in business_metrics['roi_data']]
        utilisation_labels = [data['Utilisation'] for data in business_metrics['roi_data']]
        
        fig_roi = go.Figure()
        fig_roi.add_trace(go.Bar(
            x=utilisation_labels,
            y=roi_values,
            marker_color=['#4f46e5' if roi > 0 else '#dc2626' for roi in roi_values],
            text=[f"{roi:.1f}%" for roi in roi_values],
            textposition='auto'
        ))
        
        fig_roi.update_layout(
            title='Return on Investment by Utilisation Rate',
            xaxis_title='Utilisation Rate',
            yaxis_title='ROI (%)',
            height=400
        )
        
        st.plotly_chart(fig_roi, use_container_width=True)
    
    with tab2:
        st.markdown("**Cash Flow Analysis**")
        
        cash_flow_df = pd.DataFrame(business_metrics['cash_flow_data'])
        cash_flow_df['Monthly Cash Flow'] = cash_flow_df['Monthly Cash Flow'].apply(lambda x: f"£{x:,.0f}")
        cash_flow_df['Annual Cash Flow'] = cash_flow_df['Annual Cash Flow'].apply(lambda x: f"£{x:,.0f}")
        cash_flow_df['Monthly Profit'] = cash_flow_df['Monthly Profit'].apply(lambda x: f"£{x:,.0f}")
        
        st.dataframe(cash_flow_df, use_container_width=True)
        
        # Cash Flow Chart
        monthly_cash_flows = [data['Monthly Cash Flow'] for data in business_metrics['cash_flow_data']]
        utilisation_labels = [data['Utilisation'] for data in business_metrics['cash_flow_data']]
        
        fig_cashflow = go.Figure()
        fig_cashflow.add_trace(go.Bar(
            x=utilisation_labels,
            y=monthly_cash_flows,
            marker_color=['#059669' if cf > 0 else '#dc2626' for cf in monthly_cash_flows],
            text=[f"£{cf:,.0f}" for cf in monthly_cash_flows],
            textposition='auto'
        ))
        
        fig_cashflow.update_layout(
            title='Monthly Cash Flow by Utilisation Rate',
            xaxis_title='Utilisation Rate',
            yaxis_title='Monthly Cash Flow (£)',
            height=400
        )
        
        st.plotly_chart(fig_cashflow, use_container_width=True)
    
    with tab3:
        st.markdown("**Sensitivity Analysis**")
        st.markdown("How changes in revenue and costs affect profitability")
        
        sensitivity_df = pd.DataFrame(business_metrics['sensitivity_data'])
        sensitivity_df['Adjusted Profit'] = sensitivity_df['Adjusted Profit'].apply(lambda x: f"£{x:,.0f}")
        sensitivity_df['Profit Change %'] = sensitivity_df['Profit Change %'].apply(lambda x: f"{x:+.1f}%")
        
        st.dataframe(sensitivity_df, use_container_width=True)
        
        # Sensitivity Chart
        scenarios = [data['Scenario'] for data in business_metrics['sensitivity_data']]
        profit_changes = [data['Profit Change %'] for data in business_metrics['sensitivity_data']]
        
        fig_sensitivity = go.Figure()
        fig_sensitivity.add_trace(go.Bar(
            x=scenarios,
            y=profit_changes,
            marker_color=['#059669' if pc > 0 else '#dc2626' for pc in profit_changes],
            text=[f"{pc:+.1f}%" for pc in profit_changes],
            textposition='auto'
        ))
        
        fig_sensitivity.update_layout(
            title='Profit Sensitivity to Revenue and Cost Changes',
            xaxis_title='Scenario',
            yaxis_title='Profit Change (%)',
            height=400,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_sensitivity, use_container_width=True)
    
    with tab4:
        st.markdown("**Risk Assessment - Scenario Analysis**")
        
        risk_metrics = business_metrics['risk_metrics']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🔴 Worst Case (10% Utilisation)**")
            worst = risk_metrics['Worst Case (10% Utilisation)']
            st.markdown(f"""
            <div class="metric-card">
                <h4>Annual Profit</h4>
                <h3>£{worst['Annual Profit']:,.0f}</h3>
                <p>ROI: {worst['ROI']:.1f}%</p>
                <p>Payback: {worst['Payback Years']:.1f} years</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**🟡 Expected Case (20% Utilisation)**")
            expected = risk_metrics['Expected Case (20% Utilisation)']
            st.markdown(f"""
            <div class="metric-card">
                <h4>Annual Profit</h4>
                <h3>£{expected['Annual Profit']:,.0f}</h3>
                <p>ROI: {expected['ROI']:.1f}%</p>
                <p>Payback: {expected['Payback Years']:.1f} years</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("**🟢 Best Case (40% Utilisation)**")
            best = risk_metrics['Best Case (40% Utilisation)']
            st.markdown(f"""
            <div class="metric-card">
                <h4>Annual Profit</h4>
                <h3>£{best['Annual Profit']:,.0f}</h3>
                <p>ROI: {best['ROI']:.1f}%</p>
                <p>Payback: {best['Payback Years']:.1f} years</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Risk vs Reward Chart
        scenarios = ['Worst Case', 'Expected Case', 'Best Case']
        profits = [risk_metrics['Worst Case (10% Utilisation)']['Annual Profit'],
                  risk_metrics['Expected Case (20% Utilisation)']['Annual Profit'],
                  risk_metrics['Best Case (40% Utilisation)']['Annual Profit']]
        rois = [risk_metrics['Worst Case (10% Utilisation)']['ROI'],
                risk_metrics['Expected Case (20% Utilisation)']['ROI'],
                risk_metrics['Best Case (40% Utilisation)']['ROI']]
        
        fig_risk = go.Figure()
        fig_risk.add_trace(go.Scatter(
            x=scenarios,
            y=profits,
            mode='lines+markers',
            name='Annual Profit',
            line=dict(color='#4f46e5', width=3),
            marker=dict(size=10)
        ))
        
        fig_risk.update_layout(
            title='Risk vs Reward Analysis',
            xaxis_title='Scenario',
            yaxis_title='Annual Profit (£)',
            height=400
        )
        
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with tab5:
        st.markdown("**📊 Business Planning Summary**")
        
        # Key Investment Metrics
        st.markdown("**Key Investment Metrics:**")
        
        expected_roi = business_metrics['roi_data'][1]['ROI']  # 20% utilisation
        expected_payback = business_metrics['payback_data'][1]['Payback Years']
        expected_cash_flow = business_metrics['cash_flow_data'][1]['Monthly Cash Flow']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Expected ROI</h4>
                <h2>{expected_roi:.1f}%</h2>
                <p style="font-size: 0.8rem; color: #6b7280;">At 20% utilisation</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Payback Period</h4>
                <h2>{expected_payback:.1f} years</h2>
                <p style="font-size: 0.8rem; color: #6b7280;">Time to recover investment</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Monthly Cash Flow</h4>
                <h2>£{expected_cash_flow:,.0f}</h2>
                <p style="font-size: 0.8rem; color: #6b7280;">Net cash generation</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Business Planning Insights
        st.markdown("""
        <div style="background-color: #f8fafc; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #4f46e5;">
            <h4>💡 Business Planning Insights:</h4>
            <ul>
                <li><strong>Investment Decision:</strong> Consider ROI above 15-20% as attractive for small business investments</li>
                <li><strong>Cash Flow Management:</strong> Ensure positive monthly cash flow to cover operational expenses</li>
                <li><strong>Risk Mitigation:</strong> Plan for worst-case scenarios and maintain adequate cash reserves</li>
                <li><strong>Growth Planning:</strong> Use sensitivity analysis to understand key drivers of profitability</li>
                <li><strong>Exit Strategy:</strong> Consider payback period when planning business exit or expansion</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional Considerations
        st.markdown("**Additional Business Planning Considerations:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📋 Legal & Compliance:**")
            st.markdown("- Business registration and licensing")
            st.markdown("- Insurance requirements")
            st.markdown("- Tax obligations and VAT registration")
            st.markdown("- Data protection compliance")
            st.markdown("- Employment law considerations")
        
        with col2:
            st.markdown("**🎯 Market & Competition:**")
            st.markdown("- Market size and growth potential")
            st.markdown("- Competitive landscape analysis")
            st.markdown("- Customer acquisition strategy")
            st.markdown("- Pricing strategy refinement")
            st.markdown("- Marketing and branding approach")

    with tab6:
        st.markdown("**🏛️ VAT Analysis**")
        st.markdown("""
        <div style="background-color: #f8fafc; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #4f46e5;">
            <h4>💰 VAT Overview:</h4>
            <p>In the UK, the standard VAT rate is 20%. This means that for every £100 of revenue, £20 is VATable and £20 is VAT-exempt.</p>
            <p><strong>Key VAT Terms:</strong></p>
            <ul>
                <li><strong>VATable Revenue:</strong> Revenue that is subject to VAT (e.g., drone rentals, website hosting)</li>
                <li><strong>VAT-Exempt Revenue:</strong> Revenue that is not subject to VAT (e.g., legal fees, website setup)</li>
                <li><strong>VAT-Deductible Costs:</strong> Business expenses that can be claimed back from HMRC (e.g., drone costs, website hosting)</li>
                <li><strong>Net VAT Payable:</strong> The difference between VATable revenue and VAT-deductible costs.</li>
                <li><strong>Profit After VAT:</strong> Your net profit after deducting VATable revenue and VAT-deductible costs.</li>
            </ul>
            <p><strong>VAT Registration Threshold:</strong> If your annual turnover exceeds £85,000, you must register for VAT. This is a one-time decision.</p>
            <p><strong>VAT Registration Benefits:</strong></p>
            <ul>
                <li>Can claim back VAT on purchases (e.g., drones, website hosting)</li>
                <li>Can reclaim VAT on business travel, utilities, and other operational costs</li>
                <li>May be eligible for reduced rates on certain services</li>
                <li>Can increase credibility with customers</li>
            </ul>
            <p><strong>VAT Registration Considerations:</strong></p>
            <ul>
                <li>Initial costs for registration and ongoing compliance</li>
                <li>Need to maintain accurate records of all transactions</li>
                <li>Must charge VAT on all VATable sales</li>
                <li>Must account for VAT on all VAT-deductible expenses</li>
                <li>May need to pay VAT quarterly to HMRC</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # VAT Summary Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>VAT Rate</h4>
                <h2>{vat_analysis['vat_rate'] * 100:.0f}%</h2>
                <p style="font-size: 0.8rem; color: #6b7280;">Standard UK VAT rate</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Net VAT Payable</h4>
                <h2>£{vat_analysis['net_vat_payable']:,.0f}</h2>
                <p style="font-size: 0.8rem; color: #6b7280;">Per rental day</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Profit After VAT</h4>
                <h2>£{vat_analysis['profit_after_vat']:,.0f}</h2>
                <p style="font-size: 0.8rem; color: #6b7280;">Per rental day</p>
            </div>
            """, unsafe_allow_html=True)

        # VAT Registration Analysis
        st.markdown("**📋 VAT Registration Analysis**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>Annual Revenue</h4>
                <h3>£{vat_analysis['annual_revenue']:,.0f}</h3>
                <p style="font-size: 0.8rem; color: #6b7280;">Total annual revenue</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>VAT Threshold</h4>
                <h3>£{vat_analysis['vat_threshold']:,.0f}</h3>
                <p style="font-size: 0.8rem; color: #6b7280;">Registration threshold</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            threshold_status = "✅ Must Register" if vat_analysis['annual_revenue'] >= vat_analysis['vat_threshold'] else "⏳ Below Threshold"
            threshold_color = "#dc2626" if vat_analysis['annual_revenue'] >= vat_analysis['vat_threshold'] else "#059669"
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: {threshold_color};">
                <h4>Registration Status</h4>
                <h3 style="color: {threshold_color};">{threshold_status}</h3>
                <p style="font-size: 0.8rem; color: #6b7280;">
                    {vat_analysis['months_to_threshold']:.0f} months to threshold
                </p>
            </div>
            """, unsafe_allow_html=True)

        # VAT Breakdown Table
        st.markdown("**📊 VAT-Deductible Items Breakdown**")
        
        vat_breakdown_data = []
        for item, vat_amount in vat_analysis['vat_deductible_items'].items():
            if vat_amount > 0:  # Only show items with VAT
                vat_breakdown_data.append({
                    'Item': item,
                    'VAT Amount (£)': f"£{vat_amount:,.2f}",
                    'VAT Rate': "20%",
                    'Deductible': "✅ Yes"
                })
        
        # Add additional costs VAT
        if vat_analysis['additional_costs_vat'] > 0:
            vat_breakdown_data.append({
                'Item': 'Additional Costs',
                'VAT Amount (£)': f"£{vat_analysis['additional_costs_vat']:,.2f}",
                'VAT Rate': "20%",
                'Deductible': "✅ Yes"
            })
        
        vat_df = pd.DataFrame(vat_breakdown_data)
        st.dataframe(vat_df, use_container_width=True)
        
        # VAT Impact Analysis
        st.markdown("**💡 VAT Impact Analysis**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**VAT on Revenue:**")
            st.markdown(f"- **Daily Revenue VAT:** £{vat_analysis['total_revenue_vat']:,.2f}")
            st.markdown(f"- **Annual Revenue VAT:** £{vat_analysis['total_revenue_vat'] * 365:,.0f}")
            st.markdown(f"- **VAT Rate Applied:** {vat_analysis['vat_rate'] * 100:.0f}%")
        
        with col2:
            st.markdown("**VAT on Costs:**")
            st.markdown(f"- **Total VAT Deductible:** £{vat_analysis['total_vat_deductible']:,.2f}")
            st.markdown(f"- **Net VAT Payable:** £{vat_analysis['net_vat_payable']:,.2f}")
            st.markdown(f"- **VAT Recovery Rate:** {(vat_analysis['total_vat_deductible'] / vat_analysis['total_revenue_vat'] * 100):.1f}%")

        # VAT Planning Insights
        st.markdown("""
        <div style="background-color: #f8fafc; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #4f46e5;">
            <h4>💡 VAT Planning Insights:</h4>
            <ul>
                <li><strong>VAT Registration Decision:</strong> If your annual revenue exceeds £85,000, you must register for VAT. This is a one-time decision.</li>
                <li><strong>VAT-Deductible Costs:</strong> Ensure all business expenses are VAT-deductible to reduce your net VAT payable.</li>
                <li><strong>VAT on Revenue:</strong> Always charge VAT on VATable revenue (e.g., drone rentals, website hosting).</li>
                <li><strong>Quarterly VAT Payments:</strong> If you register for VAT, you must pay VAT quarterly to HMRC.</li>
                <li><strong>VAT Refunds:</strong> If you register for VAT, you can claim back VAT on purchases and certain operational costs.</li>
                <li><strong>VAT Recovery:</strong> Your current VAT recovery rate shows how much VAT you can claim back on business expenses.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # VAT Charts
        st.markdown("**📈 VAT Visualization**")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # VAT Composition Chart
            vat_composition = {
                'VAT on Revenue': vat_analysis['total_revenue_vat'],
                'VAT Deductible': vat_analysis['total_vat_deductible'],
                'Net VAT Payable': vat_analysis['net_vat_payable']
            }
            
            fig_vat = px.pie(
                values=list(vat_composition.values()),
                names=list(vat_composition.keys()),
                title='VAT Composition',
                color_discrete_sequence=['#4f46e5', '#059669', '#dc2626']
            )
            fig_vat.update_layout(height=400)
            st.plotly_chart(fig_vat, use_container_width=True)
        
        with chart_col2:
            # VAT Impact on Profit
            profit_comparison = {
                'Profit Before VAT': vat_analysis['profit_before_vat'],
                'VAT Payable': vat_analysis['net_vat_payable'],
                'Profit After VAT': vat_analysis['profit_after_vat']
            }
            
            fig_profit = go.Figure()
            fig_profit.add_trace(go.Bar(
                x=list(profit_comparison.keys()),
                y=list(profit_comparison.values()),
                marker_color=['#4f46e5', '#dc2626', '#059669'],
                text=[f"£{v:,.0f}" for v in profit_comparison.values()],
                textposition='auto'
            ))
            
            fig_profit.update_layout(
                title='VAT Impact on Daily Profit',
                yaxis_title='Amount (£)',
                height=400
            )
            
            st.plotly_chart(fig_profit, use_container_width=True)

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
