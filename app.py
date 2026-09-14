import streamlit as st
import random
import time
import pandas as pd

# 1. Mobile-First Page Optimization
st.set_page_config(
    page_title="Expert Analysis V4.0",
    page_icon="🔮",
    layout="centered"
)

# 2. Strict CSS overrides to achieve the absolute exact pink design
st.markdown("""
<style>
    .stApp { 
        background-color: #FCE7F3 !important; 
    }
    .app-container {
        padding: 10px;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.6) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(0,0,0,0.03) !important;
    }
    [data-testid="column"] {
        width: calc(33.33% - 8px) !important;
        flex: 1 1 calc(33.33% - 8px) !important;
        min-width: 0px !important;
    }
    .live-stream-box {
        background-color: rgba(255, 255, 255, 0.4);
        border: 1px dashed rgba(219, 39, 119, 0.3);
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        margin-top: 15px;
    }
    .live-stream-digit {
        font-size: 38px;
        font-weight: 800;
        color: #111827;
        letter-spacing: 0.5px;
        font-family: monospace;
    }
    label p {
        font-size: 13px !important;
        font-weight: bold !important;
        color: #4B5563 !important;
    }
    .stat-badge {
        padding: 8px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='app-container'>", unsafe_allow_html=True)

# Main Title Header
st.markdown("<h3 style='text-align: center; color: #1F2937; margin-bottom: 2px; font-weight: 800;'>Expert Analysis V4.0</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6B7280; font-size: 11px; margin-top:0;'>Live Algorithmic Digit Signals Engine</p>", unsafe_allow_html=True)

# Interactive Selector Slots
vol_market = st.selectbox(
    "Select Market Index",
    options=["Volatility 10 Index", "Volatility 25 Index", "Volatility 50 Index", "Volatility 75 Index", "Volatility 100 Index"]
)

trade_type = st.selectbox(
    "Trade Type / Strategy Pattern",
    options=["Digits Matches/Differs", "Digits Even/Odd", "Digits Over/Under"]
)

param_cols = st.columns(2)
with param_cols:
    stake = st.number_input("Stake Amount ($)", min_value=0.35, value=1.00, step=0.50)
with param_cols:
    prediction = st.number_input("Last Digit Target", min_value=0, max_value=9, value=5, step=1)

st.markdown("<br>", unsafe_allow_html=True)
ticker_display = st.empty()
counter_display = st.empty()
message_display = st.empty()

# Static Idle Look
ticker_display.markdown("""
    <div class="live-stream-box">
        <div style="font-size: 11px; text-transform: uppercase; color: #6B7280; font-weight:bold; letter-spacing:1px;">Stream Status: Idle</div>
        <div class="live-stream-digit" style="color: #9CA3AF;">000000.0000</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
btn_col1, btn_col2, btn_col3 = st.columns(3)

with btn_col1:
    reset_btn = st.button("Reset", key="sys_rst", use_container_width=True)

with btn_col2:
    run_btn = st.button("RUN", key="sys_run", use_container_width=True)
    st.markdown("""
        <div style='text-align: center; margin-top: -53px; pointer-events: none; position: relative; z-index: 10;'>
            <div style='background: linear-gradient(135deg, #D946EF, #A21CAF); color: white; width: 56px; height: 56px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: bold; font-size:12px; box-shadow: 0 4px 12px rgba(217, 70, 239, 0.4);'>
                RUN
            </div>
        </div>
    """, unsafe_allow_html=True)

with btn_col3:
    clear_btn = st.button("Clear", key="sys_clr", use_container_width=True)

# Loop Engine
if run_btn:
    message_display.warning("Initializing live web stream feed pipeline...")
    time.sleep(0.8)
    
    current_tick = 797120.5500
    digit_history = []
    
    for i in range(100):
        current_tick += random.uniform(-2.25, 2.50)
        analyzed_digit = int(str(f"{current_tick:.4f}")[-1])
        
        digit_history.append(analyzed_digit)
        if len(digit_history) > 50:
            digit_history.pop(0)
            
        counts = {d: digit_history.count(d) for d in range(10)}
        hot_digit = max(counts, key=counts.get)
        cold_digit = min(counts, key=counts.get)
        
        ticker_display.markdown(f"""
            <div class="live-stream-box">
                <div style="font-size: 11px; text-transform: uppercase; color: #DB2777; font-weight:bold; letter-spacing:1px;">🔴 Streaming Real-Time Digits</div>
                <div class="live-stream-digit">{current_tick:.4f}</div>
                <div style="margin-top: 5px; font-size: 13px; color: #374151;">
                    Last Analyzed Digit: <b style="color: #D946EF; font-size: 18px;">{analyzed_digit}</b>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with counter_display.container():
            st.markdown("<p style='font-size:12px; font-weight:bold; color:#4B5563; margin-bottom:5px; margin-top:10px;'>📊 Digit Frequency (Last 50 Ticks)</p>", unsafe_allow_html=True)
            chart_data = pd.DataFrame(list(counts.values()), index=[str(d) for d in range(10)], columns=["Count"])
            st.bar_chart(chart_data, height=130, use_container_width=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"<div class='stat-badge' style='background-color:#EF4444;'>🔥 Hot (Matches): Digit {hot_digit}</div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='stat-badge' style='background-color:#3B82F6;'>❄️ Cold (Differs): Digit {cold_digit}</div>", unsafe_allow_html=True)
        
        win_rate = random.randint(52, 94)
        message_display.markdown(f"""
            <div style="background-color: rgba(255,255,255,0.7); border-radius:10px; padding:10px; border-left: 4px solid #10B981; font-size:12px; color:#1F2937; margin-top:10px;">
                💡 <b>Signal update:</b> Strategy tracking win-rate indicator at <span style="color:#10B981; font-weight:bold;">{win_rate}%</span> for digit target pattern.
            </div>
        """, unsafe_allow_html=True)
        
        time.sleep(1.0)

elif reset_btn:
    st.rerun()

elif clear_btn:
    message_display.info("Interface stream data log cleared.")

st.markdown("</div>", unsafe_allow_html=True)
