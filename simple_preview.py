"""
AI CEO Management System - Simple Web Preview
A dedicated web server that works with Replit's webview
"""
from flask import Flask, render_template_string, jsonify
import os
import json
import time

app = Flask(__name__)

# HTML template for the home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI CEO Management System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #1a1a2e;
            color: #e6e6e6;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 1px solid #00a8ff;
            padding-bottom: 15px;
        }
        .card {
            background-color: #16213e;
            border-radius: 10px;
            margin-bottom: 20px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .card-header {
            background-color: #0f3460;
            padding: 15px;
            border-bottom: 1px solid #00a8ff;
        }
        .card-body {
            padding: 20px;
        }
        h1, h2, h3 {
            color: #00a8ff;
        }
        .btn {
            display: inline-block;
            background-color: #e94560;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            margin: 5px;
            border: none;
            cursor: pointer;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        .btn:hover {
            background-color: #c73a54;
        }
        .btn-emergency {
            background-color: #ff0000;
        }
        .btn-emergency:hover {
            background-color: #cc0000;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            border-top: 1px solid #00a8ff;
            padding-top: 15px;
            font-size: 0.8em;
        }
        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: bold;
        }
        .badge-premium {
            background-color: #ffd700;
            color: #000;
        }
        .token-info {
            display: flex;
            justify-content: space-between;
        }
        .token-box {
            flex: 1;
            margin: 5px;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        .token-bbgt {
            background-color: #3a6ea5;
        }
        .token-918t {
            background-color: #6b3a75;
        }
        .equity {
            text-align: center;
            font-size: 1.2em;
            font-weight: bold;
            margin: 20px 0;
        }
        .blink {
            animation: blink-animation 1s steps(5, start) infinite;
        }
        @keyframes blink-animation {
            to {
                visibility: hidden;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI CEO Management System</h1>
            <p>Founded by Matthew Blake Ward, Tulsa, Oklahoma</p>
        </div>
        
        <div class="card">
            <div class="card-header">
                <h2>Founder's Welcome</h2>
            </div>
            <div class="card-body">
                <p><em>"Have you ever got your bail money back?"</em></p>
                <p>Welcome to an entirely new paradigm in technology and finance. The AI CEO system represents years of visionary thinking about how blockchain, artificial intelligence, and subscription services can merge to create something truly revolutionary.</p>
                <p>Our 51% equity retention model ensures we're invested in your success, while our automated emergency bail procedures provide real-world utility for token holders.</p>
                <p><strong><em>BBGT and 918T tokens are a new path to justice.</em></strong></p>
                <div class="equity">
                    AI CEO maintains 51% equity in all projects
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">
                <h2>System Features</h2>
            </div>
            <div class="card-body">
                <h3>Core Components</h3>
                <ul>
                    <li><strong>AI Legal Team:</strong> Comprehensive legal assistance and compliance monitoring</li>
                    <li><strong>Emergency Bail Button:</strong> Automated mugshot scraping and bail processing</li>
                    <li><strong>Carmen Sandiego-style Game:</strong> Educational bail bonds game with dual modes</li>
                    <li><strong>Quantum Learning:</strong> Advanced AI-powered decision making</li>
                </ul>
                
                <h3>Token Economy</h3>
                <div class="token-info">
                    <div class="token-box token-bbgt">
                        <h3>BBGT Token</h3>
                        <p>0.001 ETH</p>
                        <p>Basic Bail Guarantor Token</p>
                        <p>10% stake rewards</p>
                    </div>
                    <div class="token-box token-918t">
                        <h3>918T Token</h3>
                        <p>0.01 ETH</p>
                        <p>918 Technologies Token</p>
                        <p>40% to founders</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">
                <h2>Bail Emergency System</h2>
            </div>
            <div class="card-body" style="text-align: center;">
                <p>Requires 10% of total bond amount in BBGT/918T tokens for automatic bail-out</p>
                <button class="btn btn-emergency"><span class="blink">⚠</span> I'M GOING TO JAIL <span class="blink">⚠</span></button>
                <p><small>Press only in case of imminent arrest</small></p>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">
                <h2>Subscription Options</h2>
            </div>
            <div class="card-body">
                <h3>Multi-tiered Subscription Model</h3>
                <p>Starting at $49.99/month with 3-hour free trial</p>
                <p>All plans include:</p>
                <ul>
                    <li>Access to emergency bail system</li>
                    <li>AI legal assistance</li>
                    <li>Token rewards</li>
                    <li>Carmen Sandiego-style game</li>
                </ul>
                <div style="text-align: center; margin-top: 20px;">
                    <button class="btn">Start Free Trial</button>
                    <button class="btn">View Premium Plans <span class="badge badge-premium">PREMIUM</span></button>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2024 918 Technologies LLC - All rights reserved</p>
            <p>Port status: Active on port 5000</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Display the home page"""
    return render_template_string(HOME_TEMPLATE)

@app.route('/api/status')
def status():
    """Return the system status as JSON"""
    return jsonify({
        'status': 'online',
        'system_name': 'AI CEO Management System',
        'founder': 'Matthew Blake Ward',
        'location': 'Tulsa, Oklahoma',
        'features': [
            'AI Legal Team',
            'Emergency Bail Button',
            'Carmen Sandiego-style Game',
            'Token Rewards System'
        ],
        'token_prices': {
            'BBGT': '0.001 ETH',
            '918T': '0.01 ETH'
        },
        'subscription': {
            'base_price': '$49.99/month',
            'trial_period': '3 hours'
        },
        'timestamp': time.time()
    })

@app.route('/emergency')
def emergency():
    """Emergency bail button page"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI CEO - Emergency Bail System</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #1a1a2e;
                color: #e6e6e6;
                text-align: center;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1, h2 {
                color: #ff0000;
            }
            .emergency-panel {
                background-color: #16213e;
                border: 2px solid #ff0000;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
                70% { box-shadow: 0 0 0 15px rgba(255, 0, 0, 0); }
                100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
            }
            .btn {
                display: inline-block;
                background-color: #ff0000;
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 5px;
                margin: 10px;
                border: none;
                cursor: pointer;
                font-weight: bold;
                font-size: 1.2em;
                transition: background-color 0.3s;
            }
            .btn:hover {
                background-color: #cc0000;
            }
            .token-status {
                background-color: #0f3460;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .back-link {
                margin-top: 30px;
            }
            .back-link a {
                color: #00a8ff;
                text-decoration: none;
            }
            .back-link a:hover {
                text-decoration: underline;
            }
            .blink {
                animation: blink-animation 1s steps(5, start) infinite;
            }
            @keyframes blink-animation {
                to {
                    visibility: hidden;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1><span class="blink">⚠</span> EMERGENCY BAIL SYSTEM <span class="blink">⚠</span></h1>
            
            <div class="emergency-panel">
                <h2>I'M GOING TO JAIL</h2>
                <p>This emergency system will automatically process bail using your token holdings.</p>
                <button class="btn">ACTIVATE EMERGENCY BAIL</button>
            </div>
            
            <div class="token-status">
                <h3>Your Token Status</h3>
                <p>BBGT Balance: 500 tokens (0.5 ETH equivalent)</p>
                <p>918T Balance: 20 tokens (0.2 ETH equivalent)</p>
                <p>Maximum Bail Amount: $7,000</p>
                <p><small>Based on current token holdings and 10% requirement</small></p>
            </div>
            
            <div class="back-link">
                <a href="/">← Return to Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    # Run the application on port 5000, which is the Replit standard
    print("Starting AI CEO Web Preview on port 5000...")
    app.run(host='0.0.0.0', port=5000)