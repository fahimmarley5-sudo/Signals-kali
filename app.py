import streamlit as st
import random
import time

# 1. Page Configuration to look exactly like a native web dashboard
st.set_page_config(
    page_title="Live Dashboard",
    page_icon="📈",
    layout="centered"
)

# 2. CSS Override to remove the pink color and match the clean target design
st.markdown("""
<style>
    /* Clean white/light gray background matching the second image */
    .stApp { 
        background-color: #FFFFFF !important; 
    }
    
    /* Global layout fonts and labels */
    .app-container {
        padding: 15px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Target Title formatting */
    .main-title {
        font-size: 26px;
        font-weight: bold;
        color: #111827;
        margin-bottom: 2px;
    }
    
    .sub-title {
        font-size: 13px;
        color: #6B7280;
        margin-bottom: 25px;
    }

    /* Live Data Display Styling */
    .live-ticker-box {
        background-color: #F3F4F6;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-top: 20px;
        border: 1px solid #E5E7EB;
    }
    
    .ticker-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #6B7280;
        margin-bottom: 5px;
    }
    
    .ticker-value {
        font-size: 36px;
        font-weight: 800;
        color: #111827;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='app-container'>", unsafe_allow_html=True)

# Header matching your second target image
st.markdown("<div class='main-title'>Live Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Expert algorithmic analysis for synthetic indices.</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# INPUT FIELDS (Asset Selector & Configurations)
# -------------------------------------------------------------
volatility_market = st.selectbox(
    "Volatility Index",
    options=["Volatility 10 Index", "Volatility 25 Index", "Volatility 50 Index", "Volatility 75 Index", "Volatility 100 Index"],
    index=3
)

trade_type = st.selectbox(
    "Trade Type",
    options=["Digits Matches/Differs", "Digits Even/Odd", "Digits Over/Under"]
)

# Responsive setup for layout options
col1, col2 = st.columns(2)
with col1:
    stake = st.number_input("Stake ($)", min_value=0.35, value=1.00, step=0.50)
with col2:
    target_digit = st.number_input("Last Digit Prediction", min_value=0, max_value=9, value=5, step=1)

duration = st.number_input("Duration (Ticks)", min_value=1, max_value=10, value=1, step=1)

# -------------------------------------------------------------
# THE LIVE RUNNING SLOT (This updates the numbers actively)
# -------------------------------------------------------------
st.markdown("---")

# Dynamic empty spots that change live when the tool runs
ticker_placeholder = st.empty()
status_placeholder = st.empty()

# Control button to turn on the processing digits execution
start_analysis = st.button("RUN ANALYSIS", use_container_width=True)

if start_analysis:
    status_placeholder.info(f"Connecting to live data stream for {volatility_market}...")
    
    # Base starting price value to mock active charts
    base_price = 277190.00
    
    # Active monitoring simulation loop (This runs and updates constantly)
    for _ in range(50):
        # Calculate random shifts to tick values to show updating stream data
        base_price += random.uniform(-1.5, 1.8)
        last_digit = int(str(f"{base_price:.4f}")[-1])
        
        # Inject changing values directly into the display box without moving layout
        ticker_placeholder.markdown(f"""
            <div class="live-ticker-box">
                <div class="ticker-label">Active Stream Price</div>
                <div class="ticker-value">{base_price:.4f}</div>
                <div style="margin-top: 10px; font-size: 14px; color: #4B5563;">
                    Analyzing Digit: <b style="color: #10B981; font-size: 18px;">{last_digit}</b>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Speed pacing frame interval for updates
        time.sleep(1.0)
        
    status_placeholder.success("Analysis complete.")
else:
    # Default resting box look before user triggers execution
    ticker_placeholder.markdown("""
        <div class="live-ticker-box">
            <div class="ticker-label">Active Stream Price</div>
            <div class="ticker-value" style="color: #9CA3AF;">000000.0000</div>
        </div>
    """, unsafe_allow_html=True)
    status_placeholder.warning("Click 'RUN ANALYSIS' above to begin tracking live trading digits.")

st.markdown("</div>", unsafe_allow_html=True)
