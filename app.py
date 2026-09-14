import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# 1. Page Configuration for Mobile Views
st.set_page_config(page_title="VIX Expert Board", page_icon="📈", layout="wide")

st.markdown("""
<style>
    .title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; }
    .card { background-color: #F8FAFC; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-bottom: 10px; }
    .signal-buy { color: #16A34A; font-weight: bold; font-size: 20px; }
    .signal-sell { color: #DC2626; font-weight: bold; font-size: 20px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">📊 Volatility Index & Digit Matching Board</div>', unsafe_allow_html=True)
st.write("---")

# 2. Sidebar Configuration
with st.sidebar:
    st.header("⚡ Index Controls")
    selected_index = st.selectbox("Choose Volatility Index", ["VIX (Standard)", "Vol Index 75 (V75)", "Vol Index 100 (V100)"])
    sample_ticks = st.slider("Tick Analysis Depth", 50, 500, 100)
    refresh_button = st.button("🔄 Recalculate Live Matching Data")

# 3. Simulated Live Stream Data Generation
# In production, connect this to a WebSocket API like Deriv or Binance
np.random.seed(int(time.time()))
base_price = {"VIX (Standard)": 18.50, "Vol Index 75 (V75)": 245000.00, "Vol Index 100 (V100)": 4200.00}[selected_index]
volatility = {"VIX (Standard)": 0.05, "Vol Index 75 (V75)": 15.00, "Vol Index 100 (V100)": 1.20)[selected_index]

prices = [base_price]
for _ in range(sample_ticks - 1):
    prices.append(prices[-1] + np.random.normal(0, volatility))

df = pd.DataFrame({"Tick": range(1, sample_ticks + 1), "Price": prices})
df["Price"] = df["Price"].round(4)

# Extract Last Digit for Digit Matching Analysis
df["Last_Digit"] = df["Price"].apply(lambda x: int(str(x)[-1]) if str(x)[-1].isdigit() else 0)

# 4. Expert Analytics Calculations
last_price = df["Price"].iloc[-1]
price_change = last_price - df["Price"].iloc[-2]
digit_counts = df["Last_Digit"].value_index().reindex(range(10), fill_value=0)
most_frequent_digit = digit_counts.idxmax()
digit_match_percentage = (digit_counts.max() / sample_ticks) * 100

# Simple Expert AI Signal Logic
rsi_sim = np.random.uniform(30, 70)
if rsi_sim > 60:
    signal = "🔴 STRONG OVERBOUGHT (SELLER MATCH)"
    class_name = "signal-sell"
elif rsi_sim < 40:
    signal = "🟢 STRONG OVERSOLD (BUYER MATCH)"
    class_name = "signal-buy"
else:
    signal = "🟡 NEUTRAL RANGE"
    class_name = "text-align:center;"

# 5. Dashboard Grid Setup (Mobile Stack View)
st.subheader("🎯 Real-Time Board Metrics")
col1, col2 = st.columns(2)

with col1:
    st.metric(label=f"Current {selected_index} Price", value=f"{last_price:,.4f}", delta=f"{price_change:,.4f}")
with col2:
    st.markdown(f'<div class="card">Current Engine Signal:<br><span class="{class_name}">{signal}</span></div>', unsafe_allow_html=True)

st.write("---")
st.subheader("🔢 Digit Match Frequency Array")
st.write("Tracks the mathematical repeating probability of trailing decimal numbers across ticks:")

# Create a clean responsive bar chart for matching digits
fig_digits = px.bar(
    x=digit_counts.index, 
    y=digit_counts.values, 
    labels={'x': 'Decimal Digit (0-9)', 'y': 'Occurrences Count'},
    color=digit_counts.values,
    color_continuous_scale="Viridis"
)
fig_digits.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig_digits, use_container_width=True)

st.info(f"💡 **Expert Board Insight:** Digit **{most_frequent_digit}** currently shows the highest matching cluster density, appearing in **{digit_match_percentage:.1f}%** of parsed tick trends.")

st.write("### 📈 Visual Micro-Trend Stream")
fig_trend = px.line(df, x="Tick", y="Price", title=f"{selected_index} Live Analytical Velocity")
fig_trend.update_layout(height=300)
st.plotly_chart(fig_trend, use_container_width=True)


