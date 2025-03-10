
"""
Asset Generator for AI CEO Mobile App
Generates necessary assets for the application
"""

import os
import json

def ensure_directories():
    """Ensure all necessary directories exist"""
    directories = [
        'assets',
        'bin',
        'static',
        'static/images',
        'templates'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def generate_default_assets():
    """Generate default assets if they don't exist"""
    # Default app logo SVG
    app_logo_svg = """
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="180" height="180" rx="20" fill="#162447" stroke="#00a8ff" stroke-width="5"/>
  <text x="100" y="80" font-family="Arial" font-size="40" fill="#00a8ff" text-anchor="middle">AI CEO</text>
  <text x="100" y="130" font-family="Arial" font-size="20" fill="#ffffff" text-anchor="middle">MANAGEMENT</text>
  <text x="100" y="160" font-family="Arial" font-size="20" fill="#ffffff" text-anchor="middle">SYSTEM</text>
</svg>
"""
    
    # BBGT token logo SVG
    bbgt_logo_svg = """
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <circle cx="100" cy="100" r="90" fill="#1c2e4a" stroke="#ffa500" stroke-width="5"/>
  <text x="100" y="90" font-family="Arial" font-size="50" fill="#ffa500" text-anchor="middle">BBGT</text>
  <text x="100" y="130" font-family="Arial" font-size="20" fill="#ffffff" text-anchor="middle">Bail Bonds</text>
</svg>
"""
    
    # 918T token logo SVG
    token_918_logo_svg = """
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <circle cx="100" cy="100" r="90" fill="#2a193b" stroke="#00ff9d" stroke-width="5"/>
  <text x="100" y="90" font-family="Arial" font-size="50" fill="#00ff9d" text-anchor="middle">918T</text>
  <text x="100" y="130" font-family="Arial" font-size="20" fill="#ffffff" text-anchor="middle">Technology</text>
</svg>
"""
    
    # Default emergency button SVG
    emergency_button_svg = """
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <circle cx="100" cy="100" r="90" fill="#8b0000" stroke="#ff0000" stroke-width="5"/>
  <text x="100" y="80" font-family="Arial" font-size="20" fill="#ffffff" text-anchor="middle">EMERGENCY</text>
  <text x="100" y="110" font-family="Arial" font-size="20" fill="#ffffff" text-anchor="middle">BAIL</text>
  <text x="100" y="140" font-family="Arial" font-size="20" fill="#ffffff" text-anchor="middle">BUTTON</text>
</svg>
"""
    
    # Write SVG files
    assets = [
        ('app_logo.svg', app_logo_svg),
        ('bbgt_logo.svg', bbgt_logo_svg),
        ('918t_logo.svg', token_918_logo_svg),
        ('emergency_button.svg', emergency_button_svg)
    ]
    
    for filename, content in assets:
        filepath = os.path.join('assets', filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"Created asset: {filepath}")

def generate_dummy_data():
    """Generate dummy data files for testing"""
    # Token balances
    token_balances = {
        "users": {
            "founder": {"BBGT": 1000000, "918T": 5000000},
            "user1@example.com": {"BBGT": 500, "918T": 20},
            "user2@example.com": {"BBGT": 1200, "918T": 50},
            "user3@example.com": {"BBGT": 300, "918T": 10}
        }
    }
    
    # Subscription data
    subscriptions = {
        "plans": {
            "free_trial": {"price": 0, "duration_hours": 3, "features": ["basic_access", "emergency_button"]},
            "standard": {"price": 49.99, "duration_days": 30, "features": ["basic_access", "emergency_button", "legal_team"]},
            "premium": {"price": 99.99, "duration_days": 30, "features": ["basic_access", "emergency_button", "legal_team", "priority_support"]}
        },
        "active_subscriptions": {
            "user1@example.com": {
                "plan": "free_trial",
                "start_time": "2025-03-10T12:00:00",
                "end_time": "2025-03-10T15:00:00"
            },
            "user2@example.com": {
                "plan": "standard",
                "start_time": "2025-03-01T00:00:00",
                "end_time": "2025-03-31T00:00:00"
            }
        }
    }
    
    # Write JSON files
    data_files = [
        ('token_balances.json', token_balances),
        ('subscriptions.json', subscriptions)
    ]
    
    for filename, data in data_files:
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Created data file: {filename}")

def generate_all_assets():
    """Generate all necessary assets"""
    ensure_directories()
    generate_default_assets()
    generate_dummy_data()
    print("Asset generation complete!")

if __name__ == "__main__":
    generate_all_assets()
