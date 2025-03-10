"""
AI CEO Management System - Web Server
Provides a web interface for the AI CEO system and preview access
"""
import os
import json
import flask
from flask import Flask, render_template, request, jsonify, redirect, url_for
from founder_welcome import get_html_welcome
from ai_ceo import AICEO
from bail_emergency_button import BailEmergencyButton
from mugshot_scraper import MugshotScraper
from ai_legal_team import AILegalTeam
import time
import uuid

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())

# Initialize AI CEO system components
ai_ceo = AICEO(".")
bail_emergency = BailEmergencyButton(debug_mode=True)
legal_team = AILegalTeam(debug_mode=True)
mugshot_scraper = MugshotScraper()

# Create templates directory if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')

# Create basic templates
with open('templates/index.html', 'w') as f:
    f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI CEO Management System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #1a1a2e;
            color: #e6e6e6;
            font-family: 'Arial', sans-serif;
        }
        .navbar {
            background-color: #0f3460;
        }
        .card {
            background-color: #16213e;
            border: none;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .btn-primary {
            background-color: #00a8ff;
            border: none;
        }
        .btn-danger {
            background-color: #ff3b30;
            border: none;
        }
        .emergency-button {
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        .welcome-container {
            margin-bottom: 30px;
        }
        .features-list {
            list-style-type: none;
            padding-left: 0;
        }
        .features-list li {
            padding: 10px 0;
            border-bottom: 1px solid #2c3e50;
        }
        .features-list li:last-child {
            border-bottom: none;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">918 Technologies</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/emergency">Emergency</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/legal">Legal Team</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/game">Bail Jumper Game</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <div class="welcome-container">
            {{ welcome_message | safe }}
        </div>

        <div class="row">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Emergency Bail</h5>
                        <p class="card-text">Activate emergency bail procedures with just the press of a button.</p>
                        <a href="/emergency" class="btn btn-danger w-100 emergency-button">I'M GOING TO JAIL</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">AI Legal Team</h5>
                        <p class="card-text">Access your AI legal team for assistance with bail and legal matters.</p>
                        <a href="/legal" class="btn btn-primary w-100">Legal Assistance</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Bail Jumper Game</h5>
                        <p class="card-text">Play the Carmen Sandiego-style bail jumper game for fun and rewards.</p>
                        <a href="/game" class="btn btn-primary w-100">Play Now</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">About AI CEO System</h5>
                        <p>The AI CEO system represents a revolution in company management and project development. Our system retains 51% equity in all projects while providing access to AI engineers, project templates, and token rewards.</p>
                        
                        <h6 class="mt-4">Key Features:</h6>
                        <ul class="features-list">
                            <li><strong>Emergency Bail Button:</strong> With sufficient token holdings, you can activate bail procedures instantly if you find yourself in legal trouble.</li>
                            <li><strong>AI Legal Team:</strong> Get comprehensive legal assistance from our AI-powered legal team.</li>
                            <li><strong>Token Rewards:</strong> Earn BBGT and 918T tokens with real utility in our ecosystem.</li>
                            <li><strong>Carmen Sandiego-style Game:</strong> Play our bail jumper game to earn additional tokens and train the system.</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-dark text-white text-center py-3 mt-5">
        <div class="container">
            <p>© 2024 918 Technologies LLC - Founded by Matthew Blake Ward, Tulsa, Oklahoma</p>
            <p><small>BBGT and 918T tokens are a new path to justice.</small></p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """)

with open('templates/emergency.html', 'w') as f:
    f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emergency Bail - AI CEO System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #1a1a2e;
            color: #e6e6e6;
            font-family: 'Arial', sans-serif;
        }
        .navbar {
            background-color: #0f3460;
        }
        .card {
            background-color: #16213e;
            border: none;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .emergency-container {
            max-width: 800px;
            margin: 0 auto;
        }
        .btn-danger {
            background-color: #ff3b30;
            border: none;
            font-size: 24px;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }
        .btn-danger::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.2);
            transform: scale(0);
            border-radius: 50%;
            transition: transform 0.5s;
        }
        .btn-danger:active::before {
            transform: scale(3);
            transition: transform 0s;
        }
        .pulse-animation {
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 59, 48, 0.7); }
            70% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(255, 59, 48, 0); }
            100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 59, 48, 0); }
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 5px;
        }
        .status-active {
            background-color: #4cd964;
        }
        .status-inactive {
            background-color: #ff3b30;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">918 Technologies</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" href="/emergency">Emergency</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/legal">Legal Team</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/game">Bail Jumper Game</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <div class="emergency-container">
            <h1 class="text-center mb-4">Emergency Bail Bond Activation</h1>
            
            <div class="card mb-4">
                <div class="card-body">
                    <h5 class="card-title">Token Status</h5>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="d-flex justify-content-between">
                                <span>BBGT Balance:</span>
                                <span>1,000 BBGT</span>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="d-flex justify-content-between">
                                <span>918T Balance:</span>
                                <span>50 918T</span>
                            </div>
                        </div>
                    </div>
                    <div class="mt-3">
                        <div class="d-flex justify-content-between">
                            <span>Eligible Bail Coverage:</span>
                            <span>$50,000</span>
                        </div>
                        <div class="d-flex justify-content-between">
                            <span>Eligibility Tier:</span>
                            <span>Silver</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="text-center mb-5">
                <button id="emergencyButton" class="btn btn-danger btn-lg rounded-pill pulse-animation">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    I'M GOING TO JAIL
                </button>
            </div>
            
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">How It Works</h5>
                    <ol class="list-group list-group-numbered mt-3" style="background: transparent;">
                        <li class="list-group-item border-0" style="background: transparent;">Press the emergency button if you're being arrested</li>
                        <li class="list-group-item border-0" style="background: transparent;">Our system will verify your token holdings to determine eligibility</li>
                        <li class="list-group-item border-0" style="background: transparent;">AI system will scan county jail databases for your booking information</li>
                        <li class="list-group-item border-0" style="background: transparent;">Auto-generate bail bond documentation with appropriate court</li>
                        <li class="list-group-item border-0" style="background: transparent;">AI legal team will be assigned to your case</li>
                        <li class="list-group-item border-0" style="background: transparent;">Access ongoing legal assistance throughout your case</li>
                    </ol>
                </div>
            </div>
            
            <div class="card mt-4">
                <div class="card-body">
                    <h5 class="card-title">Current System Status</h5>
                    <div class="mt-3">
                        <p><span class="status-indicator status-active"></span> Emergency Bail System: <strong>Online</strong></p>
                        <p><span class="status-indicator status-active"></span> AI Legal Team: <strong>Available</strong></p>
                        <p><span class="status-indicator status-active"></span> Mugshot Scraper: <strong>Active</strong></p>
                        <p><span class="status-indicator status-active"></span> Token Verification: <strong>Operational</strong></p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-dark text-white text-center py-3 mt-5">
        <div class="container">
            <p>© 2024 918 Technologies LLC - Founded by Matthew Blake Ward, Tulsa, Oklahoma</p>
            <p><small>BBGT and 918T tokens are a new path to justice.</small></p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
    <script>
        document.getElementById('emergencyButton').addEventListener('click', function() {
            if (confirm('Are you sure you want to activate the emergency bail process? This should only be used if you are actually being arrested.')) {
                // Show activation in progress
                this.textContent = 'Processing...';
                this.disabled = true;
                
                // Simulate activation process
                setTimeout(() => {
                    alert('Emergency bail process activated. An AI legal team has been assigned to your case. We will begin scanning jail databases for your booking information.');
                    
                    // Update button
                    this.textContent = 'Activated';
                    this.classList.remove('btn-danger', 'pulse-animation');
                    this.classList.add('btn-success');
                    
                    // In a real application, this would make an API call to activate the emergency process
                }, 2000);
            }
        });
    </script>
</body>
</html>
    """)

with open('templates/legal.html', 'w') as f:
    f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Legal Team - AI CEO System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #1a1a2e;
            color: #e6e6e6;
            font-family: 'Arial', sans-serif;
        }
        .navbar {
            background-color: #0f3460;
        }
        .card {
            background-color: #16213e;
            border: none;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .btn-primary {
            background-color: #00a8ff;
            border: none;
        }
        .legal-team-member {
            background-color: #1f305e;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .legal-document {
            background-color: #2a2a4a;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .legal-document pre {
            white-space: pre-wrap;
            color: #ddd;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">918 Technologies</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/emergency">Emergency</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" href="/legal">Legal Team</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/game">Bail Jumper Game</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <h1 class="mb-4">AI Legal Team</h1>
        
        <div class="row">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Your Legal Team</h5>
                        <div class="legal-team-member">
                            <h6>AI Defense Attorney</h6>
                            <p><small>Specialized in criminal defense with expertise in bail proceedings and pretrial motions.</small></p>
                        </div>
                        <div class="legal-team-member">
                            <h6>AI Legal Researcher</h6>
                            <p><small>Specialized in researching case law, statutes, and legal precedents relevant to bail and criminal proceedings.</small></p>
                        </div>
                        <div class="legal-team-member">
                            <h6>AI Compliance Specialist</h6>
                            <p><small>Specialized in ensuring compliance with court orders, bail conditions, and monitoring requirements.</small></p>
                        </div>
                        <div class="legal-team-member">
                            <h6>AI Strategy Advisor</h6>
                            <p><small>Specialized in developing optimal legal strategies and evaluating plea options.</small></p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-8">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Active Legal Cases</h5>
                        
                        <div class="alert alert-info">
                            No active legal cases found. Cases will appear here after bail emergency activation.
                        </div>
                        
                        <h5 class="mt-4">Sample Legal Documents</h5>
                        
                        <div class="legal-document">
                            <h6>Court Appearance Reminder</h6>
                            <pre>
NOTICE OF COURT APPEARANCE

CASE NUMBER: CASE12345
DEFENDANT: John Doe

This is a reminder that you are scheduled to appear in court on:
Date: March 24, 2024
Time: 09:00 AM
Location: County Courthouse
Department: Dept. 5

Please arrive at least 30 minutes early to clear security and locate your courtroom.
Failure to appear may result in a warrant being issued for your arrest and forfeiture
of your bail bond.

If you have any questions, please contact your AI Legal Team at:
Phone: (800) BAIL-CEO
Email: legal@aiceo.com

Sincerely,
AI CEO Legal Team
                            </pre>
                        </div>
                        
                        <div class="legal-document">
                            <h6>Bail Conditions Reminder</h6>
                            <pre>
BAIL CONDITIONS REMINDER

CASE NUMBER: CASE12345
DEFENDANT: John Doe
BAIL BOND ID: BOND67890

This is a reminder of the conditions of your bail:

1. You must appear at all scheduled court appearances
2. You must not leave the jurisdiction without court permission
3. You must report to your AI Monitoring System as scheduled
4. You must comply with all court-ordered conditions

Compliance with these conditions is monitored through our AI tracking systems.
Violation of any condition may result in revocation of bail and return to custody.

Your next check-in is scheduled for: March 17, 2024 at 10:00 AM

If you have any questions, please contact your AI Legal Team at:
Phone: (800) BAIL-CEO
Email: legal@aiceo.com

Sincerely,
AI CEO Legal Team
                            </pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mt-4">
            <div class="card-body">
                <h5 class="card-title">Legal Resources</h5>
                <div class="row">
                    <div class="col-md-6">
                        <h6>Key Supreme Court Cases on Bail</h6>
                        <ul>
                            <li><strong>United States v. Salerno (1987)</strong> - Established that pretrial detention without bail is constitutional if the defendant poses a danger to the community.</li>
                            <li><strong>Stack v. Boyle (1951)</strong> - Ruled that bail cannot be set higher than necessary to ensure the defendant's appearance at trial.</li>
                            <li><strong>Bell v. Wolfish (1979)</strong> - Distinguished between punitive and regulatory detention, allowing pretrial detention for safety concerns.</li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <h6>Important Legal Definitions</h6>
                        <ul>
                            <li><strong>Bail</strong> - Money or property given to secure release from jail while ensuring court appearance.</li>
                            <li><strong>Bail Bond</strong> - A legal agreement to forfeit money or property if a defendant fails to appear in court.</li>
                            <li><strong>Own Recognizance (OR)</strong> - Release without bail, based on the defendant's promise to appear in court.</li>
                            <li><strong>Surety</strong> - A person who agrees to be legally responsible for another's debt or obligation.</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-dark text-white text-center py-3 mt-5">
        <div class="container">
            <p>© 2024 918 Technologies LLC - Founded by Matthew Blake Ward, Tulsa, Oklahoma</p>
            <p><small>BBGT and 918T tokens are a new path to justice.</small></p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """)

with open('templates/game.html', 'w') as f:
    f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bail Jumper Game - AI CEO System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #1a1a2e;
            color: #e6e6e6;
            font-family: 'Arial', sans-serif;
        }
        .navbar {
            background-color: #0f3460;
        }
        .card {
            background-color: #16213e;
            border: none;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .btn-primary {
            background-color: #00a8ff;
            border: none;
        }
        .game-container {
            max-width: 800px;
            margin: 0 auto;
        }
        .game-mode {
            background-color: #1f305e;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            transition: transform 0.3s;
        }
        .game-mode:hover {
            transform: translateY(-5px);
        }
        .game-map {
            width: 100%;
            height: 300px;
            background-color: #2a2a4a;
            border-radius: 10px;
            margin: 20px 0;
            position: relative;
            overflow: hidden;
            border: 2px solid #3d4b6e;
        }
        .map-title {
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            background-color: rgba(0, 0, 0, 0.7);
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 14px;
        }
        .map-point {
            position: absolute;
            width: 15px;
            height: 15px;
            background-color: #ff3b30;
            border-radius: 50%;
            cursor: pointer;
        }
        .player-point {
            position: absolute;
            width: 20px;
            height: 20px;
            background-color: #00a8ff;
            border-radius: 50%;
            z-index: 10;
        }
        .coming-soon {
            opacity: 0.7;
        }
        .token-stake {
            font-size: 24px;
            font-weight: bold;
            color: #4cd964;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">918 Technologies</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/emergency">Emergency</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/legal">Legal Team</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" href="/game">Bail Jumper Game</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <div class="game-container">
            <h1 class="text-center mb-4">Carmen Sandiego-Style Bail Jumper Game</h1>
            <p class="lead text-center mb-5">Choose your game mode and put your tokens at stake to earn double rewards or help train our AI risk assessment system.</p>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="game-mode">
                        <h4>Mode #1: Bail Jumper</h4>
                        <p>Try to outwit the AI bailsman through strategy or discovering exploits in the system. If you successfully evade capture, earn double your bet amount!</p>
                        <ul>
                            <li>Bet BBGT or 918T tokens</li>
                            <li>Navigate through the county map</li>
                            <li>Avoid bailsman and bounty hunters</li>
                            <li>Double your tokens if you survive</li>
                        </ul>
                        <div class="d-grid">
                            <button class="btn btn-primary">Play Bail Jumper</button>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="game-mode">
                        <h4>Mode #2: Defendant</h4>
                        <p>Participate in a mock arrest and bail process to help train our AI risk assessment system. Stake tokens and get 100% back plus rewards!</p>
                        <ul>
                            <li>Stake 10% for mock bail</li>
                            <li>Complete court appearances</li>
                            <li>Follow all bail conditions</li>
                            <li>Get 100% of stake plus rewards</li>
                        </ul>
                        <div class="d-grid">
                            <button class="btn btn-primary">Play Defendant</button>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card mt-4">
                <div class="card-body">
                    <h5 class="card-title">Game Preview</h5>
                    <p>In this Carmen Sandiego-style game, you'll navigate through county maps, make strategic decisions, and try to evade capture or fulfill your bail obligations.</p>
                    
                    <div class="game-map">
                        <div class="map-title">Los Angeles County</div>
                        <div class="player-point" style="top: 150px; left: 250px;"></div>
                        <div class="map-point" style="top: 100px; left: 180px;"></div>
                        <div class="map-point" style="top: 200px; left: 300px;"></div>
                        <div class="map-point" style="top: 80px; left: 400px;"></div>
                    </div>
                    
                    <div class="row">
                        <div class="col-6">
                            <div class="card">
                                <div class="card-body">
                                    <h6 class="card-title">Your Tokens</h6>
                                    <p class="mb-1">BBGT: 1,000</p>
                                    <p>918T: 50</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="card">
                                <div class="card-body">
                                    <h6 class="card-title">Current Stake</h6>
                                    <p class="token-stake">0 BBGT</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="alert alert-info mt-4">
                <strong>Coming Soon!</strong> The full game is currently in development. Check back soon for the complete experience!
            </div>
        </div>
    </div>

    <footer class="bg-dark text-white text-center py-3 mt-5">
        <div class="container">
            <p>© 2024 918 Technologies LLC - Founded by Matthew Blake Ward, Tulsa, Oklahoma</p>
            <p><small>BBGT and 918T tokens are a new path to justice.</small></p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """)

@app.route('/')
def index():
    # Generate welcome message with founder's message
    welcome_message = get_html_welcome(request.remote_addr)
    return render_template('index.html', welcome_message=welcome_message)

@app.route('/emergency')
def emergency():
    return render_template('emergency.html')

@app.route('/legal')
def legal_team_page():
    return render_template('legal.html')

@app.route('/game')
def game_page():
    return render_template('game.html')

# API Endpoints
@app.route('/api/emergency/activate', methods=['POST'])
def activate_emergency():
    data = request.json
    location = data.get('location', 'Unknown')
    situation = data.get('situation', 'Unknown')
    
    # Call the emergency activation function
    result = bail_emergency.activate_emergency(
        user_id=request.remote_addr,
        location=location,
        situation=situation
    )
    
    return jsonify(result)

@app.route('/api/emergency/<activation_id>/status', methods=['GET'])
def emergency_status(activation_id):
    result = bail_emergency.get_activation_status(activation_id)
    return jsonify(result)

@app.route('/api/mugshot/search', methods=['POST'])
def search_mugshot():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    county = data.get('county')
    
    if not first_name or not last_name:
        return jsonify({"error": "First name and last name are required"}), 400
    
    result = mugshot_scraper.search_inmate(first_name, last_name, county)
    return jsonify({"result": result})

if __name__ == '__main__':
    # Create necessary directories if they don't exist
    os.makedirs('legal_team_data', exist_ok=True)
    os.makedirs('emergency_activations', exist_ok=True)
    os.makedirs('mugshot_cache', exist_ok=True)
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)