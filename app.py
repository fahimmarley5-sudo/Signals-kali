import streamlit as st
import asyncio
import json
import websockets
import pandas as pd
import numpy as np
import time

# 1. Page Configuration for Mobile and Web Views
st.set_page_config(
    page_title="Expert Analysis Tool", 
    page_icon="📈", 
    layout="centered"
)

# 2. Embedded Custom Styling matching the Mobile App UI
st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC;
    }
    .title { 
        font-size: 28px; 
        font-weight: 800; 
        color: #0F172A; 
        text-align: center;
        line-height: 1.3;
        margin-bottom: 5px;
    }
    .highlight-text {
        color: #10B981;
    }
    .description {
        color: #64748B;
        font-size: 14px;
        text-align: center;
        margin-bottom: 25px;
        line-height: 1.5;
    }
    .hud-card { 
        background-color: #0F172A; 
        padding: 24px; 
        border-radius: 20px; 
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        color: #FFFFFF;
        margin-bottom: 20px;
    }
    .hud-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #1E293B;
        padding-bottom: 12px;
        margin-bottom: 12px;
    }
    .hud-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94A3B8;
        font-weight: 600;
    }
    .hud-value-price {
        font-family: monospace;
        font-size: 20px;
        color: #34D399;
        font-weight: 700;
    }
    .hud-value-digit {
        font-size: 24px;
        color: #F59E0B;
        font-weight: 900;
    }
    .win-rate-container {
        text-align: center;
        padding-top: 8px;
    }
    .win-rate-pct {
        font-size: 52px;
        font-weight: 900;
        letter-spacing: -0.05em;
    }
    .win-rate-sign {
        font-size: 30px;
        color: #34D399;
    }
    .signal-badge-call {
        background-color: #10B981;
        color: white;
        padding: 10px;
        border-radius: 12px;
        font-weight: 700;
        text-align: center;
        letter-spacing: 0.05em;
        font-size: 14px;
        margin-top: 15px;
    }
    .signal-badge-put {
        background-color: #EF4444;
        color: white;
        padding: 10px;
        border-radius: 12px;
        font-weight: 700;
        text-align: center;
        letter-spacing: 0.05em;
        font-size: 14px;
        margin-top: 15px;
    }
    .signal-badge-neutral {
        background-color: #334155;
        color: #94A3B8;
        padding: 10px;
        border-radius: 12px;
        font-weight: 700;
        text-align: center;
        font-size: 14px;
        margin-top: 15px;
    }
    .btn-primary {
        background-color: #10B981;
        color: white;
        text-align: center;
        padding: 14px;
        border-radius: 12px;
        font-weight: 700;
        margin-top: 20px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    .btn-secondary {
        color: #64748B;
        text-align: center;
        padding: 10px;
        font-weight: 600;
        font-size: 14px;
        margin-top: 5px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# 3. Micro-Window Calculation Algorithm
def process_expert_signals(ticks_list):
    if len(ticks_list) < 5:
        return {"win_rate": 50, "signal": "NEUTRAL", "last_digit": 0, "bias": "NEUTRAL"}
    
    last_ticks = ticks_list[-5:]
    gains = sum(1 for i in range(1, len(last_ticks)) if last_ticks[i] > last_ticks[i-1])
    
    win_rate = 50 + (gains * 11) - ((4 - gains) * 9)
    win_rate = max(35, min(94, win_rate))
    
    last_price_str = str(last_ticks[-1])
    last_digit = int(last_price_str[-1]) if last_price_str else 0
    
    bias = "OVER" if last_digit > 4 else "UNDER"
    if win_rate > 65:
        signal = "CALL"
    elif win_rate < 45:
        signal = "PUT"
        win_rate = 100 - win_rate
    else:
        signal = "NEUTRAL"
        
    return {"win_rate": win_rate, "signal": signal, "last_digit": last_digit, "bias": bias}

# 4. Asynchronous Deriv WebSocket Feed Bridge
async def fetch_deriv_tick():
    uri = "wss://://derivws.com" 
    try:
        async with websockets.connect(uri) as websocket:
            subscribe_query = {"ticks": "R_100"}
            await websocket.send(json.dumps(subscribe_query))
            
            response = await websocket.recv()
            data = json.loads(response)
            if "tick" in data:
                return data["tick"]["quote"]
    except Exception:
        pass
    return None

if "price_history" not in st.session_state:
    st.session_state.price_history = [1000.00]

# 5. Core Interface Layout Structure
st.markdown('<div class="title">Trade binary digits with <span class="highlight-text">live win-rate signals</span></div>', unsafe_allow_html=True)
st.markdown('<div class="description">Expert Analysis Tool tracking deep real-time synthetic data indices and algorithmic match parameters.</div>', unsafe_allow_html=True)

hud_placeholder = st.empty()

st.markdown('<div class="btn-primary">Get Started</div>', unsafe_allow_html=True)
st.markdown('<div class="btn-secondary">View Pricing</div>', unsafe_allow_html=True)

# 6. Real-Time High Frequency Live Update Loop
while True:
    current_tick = asyncio.run(fetch_deriv_tick())
    
    if current_tick is not None:
        st.session_state.price_history.append(current_tick)
        if len(st.session_state.price_history) > 30:
            st.session_state.price_history.pop(0)
            
        metrics = process_expert_signals(st.session_state.price_history)
        
        badge_class = "signal-badge-neutral"
        if metrics["signal"] == "CALL":
            badge_class = "signal-badge-call"
        elif metrics["signal"] == "PUT":
            badge_class = "signal-badge-put"
            
        hud_placeholder.markdown(f"""
        <div class="hud-card">
            <div class="hud-row">
                <div class="hud-label">Active Market Price</div>
                <div class="hud-value-price">{current_tick:.2f}</div>
            </div>
            <div class="hud-row">
                <div class="hud-label">Last Digit Analyzed</div>
                <div class="hud-value-digit">{metrics["last_digit"]}</div>
            </div>
            <div class="win-rate-container">
                <div class="hud-label" style="margin-bottom: 5px;">Algorithmic Win Probability</div>
                <div class="win-rate-pct">{metrics["win_rate"]}<span class="win-rate-sign">%</span></div>
            </div>
            <div class="{badge_class}">
                EXECUTION SIGNAL: {metrics["signal"]} ({metrics["bias"]})
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    time.sleep(0.3)
