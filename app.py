import streamlit as st
import streamlit.components.v1 as components

# Set up clean mobile layout parameters
st.set_page_config(
    page_title="Expert Analysis V4.0",
    page_icon="📊",
    layout="centered"
)

# Style overrides to remove default page padding
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0px; margin: 0px;}
    iframe {border: none; border-radius: 20px;}
    </style>
""", unsafe_allow_html=True)

# Fixed Web App Frame Layout
ui_frame = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0;
            padding: 10px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #fff0f3;
            display: flex;
            justify-content: center;
        }
        .container {
            width: 100%;
            max-width: 350px;
            background: #ffffff;
            border-radius: 24px;
            padding: 15px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.05);
            text-align: center;
            box-sizing: border-box;
        }
        h2 {
            font-size: 1.2rem;
            margin: 5px 0 15px 0;
            color: #2b2d42;
        }
        .selector-group {
            margin-bottom: 12px;
            text-align: left;
        }
        label {
            font-size: 0.75rem;
            font-weight: 600;
            color: #4a4e69;
            display: block;
            margin-bottom: 3px;
        }
        select {
            width: 100%;
            padding: 8px;
            border-radius: 8px;
            border: 1px solid #ced4da;
            background-color: #f8f9fa;
            font-size: 0.85rem;
            color: #2b2d42;
            margin-bottom: 8px;
        }
        .live-price-box {
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: 1px;
            color: #2b2d42;
            margin: 12px 0;
        }
        .last-digit {
            color: #f72585;
            border-bottom: 3px solid #f72585;
        }
        .control-panel {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 15px 0;
        }
        .side-btn {
            background-color: #4cc9f0;
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.8rem;
        }
        .side-btn.differ {
            background-color: #4361ee;
        }
        .center-circle {
            width: 70px;
            height: 70px;
            background-color: #7209b7;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            font-weight: 800;
        }
        .timer-container {
            margin-top: 5px;
            font-size: 0.8rem;
            color: #4a4e69;
            font-weight: 600;
            background: #f8f9fa;
            padding: 5px 12px;
            border-radius: 15px;
            display: inline-block;
        }
        #countdown-number {
            color: #f72585;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 4px;
            margin-top: 15px;
        }
        .stat-bar-container {
            font-size: 0.7rem;
            font-weight: bold;
            background: #f1f3f5;
            padding: 4px 0;
            border-radius: 6px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .stat-fill {
            width: 6px;
            height: 25px;
            background: #dee2e6;
            margin-top: 3px;
            border-radius: 2px;
            position: relative;
            overflow: hidden;
        }
        .stat-progress {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            background: #7209b7;
            height: 0%;
            transition: height 0.2s ease;
        }
    </style>
</head>
<body>

    <div class="container">
        <h2>Expert Analysis V4.0</h2>
        
        <div class="selector-group">
            <label>Select Market Index</label>
            <select id="market-select">
                <option value="1HZ10V">Volatility 10 (1s) Index</option>
                <option value="1HZ25V">Volatility 25 (1s) Index</option>
                <option value="1HZ50V">Volatility 50 (1s) Index</option>
                <option value="1HZ75V">Volatility 75 (1s) Index</option>
                <option value="1HZ100V" selected>Volatility 100 (1s) Index</option>
                <option value="R_10">Volatility 10 Index</option>
                <option value="R_25">Volatility 25 Index</option>
                <option value="R_50">Volatility 50 Index</option>
                <option value="R_75">Volatility 75 Index</option>
                <option value="R_100">Volatility 100 Index</option>
            </select>

            <label>Trade Type</label>
            <select id="trade-select">
                <option value="matches_differs" selected>Digits Matches/Differs</option>
                <option value="even_odd">Digits Even/Odd</option>
                <option value="over_under">Digits Over/Under</option>
            </select>
        </div>
        
        <div class="live-price-box" id="price-display">0.00</div>

        <div class="control-panel">
            <button class="side-btn">MATCH</button>
            <div class="center-circle" id="predicted-digit">-</div>
            <button class="side-btn differ">DIFFER</button>
        </div>

        <div class="timer-container">
            Next update in: <span id="countdown-number">5s</span>
        </div>

        <div class="stats-grid" id="stats-output"></div>
    </div>

    <script>
        let ws;
        let digitCounts = Array(10).fill(0);
        let totalTicks = 0;
        let timeLeft = 5;
        let currentSymbol = "1HZ100V";

        const statsOutput = document.getElementById('stats-output');
        for (let i = 0; i < 10; i++) {
            statsOutput.innerHTML += `
                <div class="stat-bar-container">
                    <div>${i}</div>
                    <div class="stat-fill"><div class="stat-progress" id="bar-${i}"></div></div>
                </div>
            `;
        }

        function connectWebSocket(symbol) {
            if (ws) ws.close();
            digitCounts = Array(10).fill(0);
            totalTicks = 0;

            ws = new WebSocket('wss://://derivws.com');

            ws.onopen = () => {
                ws.send(JSON.stringify({ "ticks": symbol }));
            };

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.tick) {
                    const quote = data.tick.quote.toFixed(data.tick.pip_size);
                    const lastDigit = quote.slice(-1);
                    
                    document.getElementById('price-display').innerHTML = 
                        `${quote.slice(0, -1)}<span class="last-digit">${lastDigit}</span>`;

                    digitCounts[parseInt(lastDigit)]++;
                    totalTicks++;
                    
                    for (let i = 0; i < 10; i++) {
                        const percentage = (digitCounts[i] / totalTicks) * 100;
                        document.getElementById(`bar-${i}`).style.height = `${Math.min(percentage * 4, 100)}%`;
                    }
                }
            };
        }

        document.getElementById('market-select').addEventListener('change', (e) => {
            currentSymbol = e.target.value;
            connectWebSocket(currentSymbol);
        });

        connectWebSocket(currentSymbol);

        setInterval(() => {
            if (timeLeft <= 0) {
                timeLeft = 5;
                document.getElementById('predicted-digit').innerText = Math.floor(Math.random() * 10);
            } else {
                timeLeft--;
            }
            document.getElementById('countdown-number').innerText = timeLeft + "s";
        }, 1000);
    </script>

</body>
</html>
"""

# Render with safe explicit sizing for small smartphone browsers
components.html(ui_frame, height=580, scrolling=True)
