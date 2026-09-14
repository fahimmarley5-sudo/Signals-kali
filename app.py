import streamlit as st
import random
import time

# 1. Page Configuration for Mobile Views
st.set_page_config(
    page_title="Expert Analysis Tool",
    page_icon="🔮",
    layout="centered"
)

# 2. Advanced CSS Override to force mobile layout elements inline
st.markdown("""
<style>
    /* Force background color of the phone layout */
    .stApp { 
        background-color: #FCE7F3 !important; 
    }
    
    /* Global container styling */
    .app-container {
        padding: 10px;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* Make input background blend seamlessly with page */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.4) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
    }
    
    /* FORCE Streamlit columns to stay horizontal on mobile phones */
    [data-testid="column"] {
        width: calc(33.33% - 10px) !important;
        flex: 1 1 calc(33.33% - 10px) !important;
        min-width: 0px !important;
    }
    
    /* Make sure form columns sit side by side too */
    .form-grid {
        display: flex;
        gap: 10px;
    }
    
    /* Custom style definitions for the button container row */
    .mobile-button-row {
        display: flex;
        justify-content: space-around;
        align-items: center;
        width: 100%;
        margin: 25px 0;
        gap: 8px;
    }
    
    /* Small Utility Action buttons (Reset / Clear) */
    .utility-btn {
        background-color: #06B6D4 !important; /* Teal/Cyan color matching video */
        color: white !important;
        border-radius: 20px !important;
        padding: 6px 15px !important;
        font-size: 13px !important;
        font-weight: bold;
        text-align: center;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Central Circular Execution Trigger Button */
    .center-run-circle {
        background-color: #D946EF !important; /* Bold Fuchsia/Pink matching video */
        color: white !important;
        width: 65px !important;
        height: 65px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: bold !important;
        font-size: 15px !important;
        box-shadow: 0 4px 10px rgba(217, 70, 239, 0.4) !important;
        border: none !important;
        text-align: center;
    }
    
    /* Label Adjustments */
    label p {
        font-size: 13px !important;
        font-weight: bold !important;
        color: #4B5563 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='app-container'>", unsafe_allow_html=True)

# App Header
st.markdown("<h3 style='text-align: center; color: #1F2937; margin-bottom: 0px; font-weight: 800;'>EXPERT ANALYSIS</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B7280; font-size: 11px; margin-top:0;'>Volatility & Digit Statistics</p>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. THE VOLATILITY MARKET CHANGING CONFIG SLOT
# -------------------------------------------------------------
volatility_market = st.selectbox(
    "Market Asset Selector",
    options=["Volatility 10 Index", "Volatility 25 Index", "Volatility 50 Index", "Volatility 75 Index", "Volatility 100 Index"]
)

trade_type = st.selectbox(
    "Trade Type / Strategy Pattern",
    options=["Digits Matches/Differs", "Digits Even/Odd", "Digits Over/Under"]
)

# 2. Side-by-side Form Inputs for Stake and Target Digit
col_inputs = st.columns(2)
with col_inputs[0]:
    stake = st.number_input("Stake Amount ($)", min_value=0.35, value=1.00, step=0.50)
with col_inputs[1]:
    target_digit = st.number_input("Target Run Digit", min_value=0, max_value=9, value=5, step=1)

# -------------------------------------------------------------
# 2. THE THREE BUTTONS IN A PERFECT HORIZONTAL ROW
# -------------------------------------------------------------
st.write("") # Micro spacer

# Create 3 strict horizontal column slots
btn_col1, btn_col2, btn_col3 = st.columns(3)

with btn_col1:
    # Use HTML markup to design beautiful horizontal flow blocks
    reset_clicked = st.button("Reset", key="rs_btn", use_container_width=True)

with btn_col2:
    run_clicked = st.button("RUN", key="rn_btn", use_container_width=True)
    # Visual circle overlay to completely match the circular look of the video button
    st.markdown("""
        <div style='text-align: center; margin-top: -53px; pointer-events: none; position: relative; z-index: 10;'>
            <div style='background: linear-gradient(135deg, #D946EF, #C084FC); color: white; width: 55px; height: 55px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: bold; font-size:12px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);'>
                RUN
            </div>
        </div>
    """, unsafe_allow_html=True)

with btn_col3:
    clear_clicked = st.button("Clear", key="cl_btn", use_container_width=True)


# -------------------------------------------------------------
# 3. STATS OUTPUT DISPLAYS
# -------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
output_block = st.empty()

if run_clicked:
    output_block.success(f"Connecting to live ticker stream for {volatility_market}...")
    # Add your websockets code inside this block to show active trading digits!
else:
    output_block.info("Adjust the parameter configurations above and press RUN to analyze digits.")

st.markdown("</div>", unsafe_allow_html=True)
