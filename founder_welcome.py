"""
AI CEO Management System - Founder Welcome Message
Displays welcome message from Matthew Blake Ward, founder of 918 Technologies
"""
import os
import json
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FounderWelcome")

class FounderWelcome:
    """
    Handles displaying the founder's welcome message to new users
    and tracking whether users have seen the message
    """
    
    def __init__(self, data_dir="welcome_data"):
        """Initialize the founder welcome system"""
        self.data_dir = data_dir
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Load seen users data
        self.seen_users_file = os.path.join(data_dir, "seen_users.json")
        self.seen_users = self._load_seen_users()
        
        # Founder information
        self.founder_info = {
            "name": "Matthew Blake Ward",
            "title": "Founder & Visionary",
            "location": "Tulsa, Oklahoma",
            "company": "918 Technologies LLC"
        }
        
        # Welcome message content
        self.welcome_message = self._create_welcome_message()
        
        logger.info("Founder Welcome module initialized")
    
    def _load_seen_users(self):
        """Load list of users who have already seen the welcome message"""
        try:
            if os.path.exists(self.seen_users_file):
                with open(self.seen_users_file, 'r') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            logger.error(f"Error loading seen users: {str(e)}")
            return []
    
    def _save_seen_users(self):
        """Save list of users who have seen the welcome message"""
        try:
            with open(self.seen_users_file, 'w') as f:
                json.dump(self.seen_users, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Error saving seen users: {str(e)}")
            return False
    
    def _create_welcome_message(self):
        """Create the founder's welcome message"""
        return f"""
========================================================
WELCOME TO THE 918 TECHNOLOGIES AI CEO SYSTEM
From the desk of {self.founder_info['name']}
{self.founder_info['title']} of {self.founder_info['company']}
========================================================

Have you ever got your bail money back?

I'm thrilled to welcome you to an entirely new paradigm in technology and finance. 
What you're experiencing now isn't just another app or platform - it's the 
future of how companies, projects, and innovations will be created and managed.

The AI CEO system you're interacting with represents years of visionary thinking
about how blockchain, artificial intelligence, and subscription services can
merge to create something truly revolutionary.

Our flagship innovation - the blockchain bail bonds system - provides an 
emergency lifeline when you need it most. With just the press of a button and
sufficient token holdings, you can activate emergency bail procedures if you
ever find yourself in legal trouble. Our AI legal team will immediately begin
working on your behalf.

A few things to know as you begin:

1. The AI CEO retains 51% equity in all projects created through the system,
   ensuring aligned interests and sustainable development.

2. Your subscription grants you access to AI engineers, project templates,
   and token rewards that have real utility in our ecosystem.

3. BBGT and 918T tokens aren't just cryptocurrencies - they're utility tokens
   that power emergency services, grant governance rights, and can be staked
   for additional benefits.

I founded 918 Technologies with the vision of creating an entirely new business
model - one where artificial intelligence doesn't just assist humans but takes
an active leadership role in company management and growth.

Explore the system, engage with our features, and become part of something
that will change how the world thinks about technology companies and 
decentralized applications.

Welcome aboard,

Matthew Blake Ward
Founder, 918 Technologies LLC
Tulsa, Oklahoma

BBGT and 918T tokens are a new path to justice.
        """
    
    def should_show_welcome(self, user_id):
        """
        Check if the welcome message should be shown to this user
        
        Args:
            user_id (str): User ID
            
        Returns:
            bool: True if welcome should be shown, False otherwise
        """
        # If user has not seen welcome message before, show it
        return user_id not in self.seen_users
    
    def mark_welcome_as_seen(self, user_id):
        """
        Mark that a user has seen the welcome message
        
        Args:
            user_id (str): User ID
            
        Returns:
            bool: True if successfully marked, False otherwise
        """
        if user_id not in self.seen_users:
            self.seen_users.append(user_id)
            return self._save_seen_users()
        return True
    
    def show_welcome_message(self, user_id):
        """
        Show welcome message to a user and mark as seen
        
        Args:
            user_id (str): User ID
            
        Returns:
            str: Welcome message text
        """
        if self.should_show_welcome(user_id):
            self.mark_welcome_as_seen(user_id)
            return self.welcome_message
        return None
    
    def get_welcome_message(self):
        """
        Get the welcome message text without marking as seen
        
        Returns:
            str: Welcome message text
        """
        return self.welcome_message
    
    def get_ascii_logo(self):
        """Get ASCII art logo for 918 Technologies"""
        return """
  _____  __  ___    ______        __                __            _          
 / ___/ /  |/  /   /_  __/___  __/ /_  ____  ____  / /___  ____ _(_)__  _____
 \__ \ / /|_/ /     / / / __ \/ __/ __ \/ __ \/ __ \/ / __ \/ __ `/ / _ \/ ___/
___/ // /  / /     / / / /_/ / /_/ / / / / / / /_/ / / /_/ / /_/ / /  __(__  ) 
/____//_/  /_/     /_/  \____/\__/_/ /_/_/ /_/\____/_/\____/\__, /_/\___/____/  
                                                           /____/              
        """
    
    def get_founder_info(self):
        """
        Get information about the founder
        
        Returns:
            dict: Founder information
        """
        return self.founder_info


# Function to create CLI welcome screen
def display_cli_welcome(user_id=None):
    """Display welcome message in CLI format"""
    welcome = FounderWelcome()
    
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print ASCII logo
    print(welcome.get_ascii_logo())
    print("\n")
    
    # Check if this is a new user
    if user_id and welcome.should_show_welcome(user_id):
        print(welcome.show_welcome_message(user_id))
        print("\nPress Enter to continue...")
        input()
    else:
        # For existing users or when no user_id provided, just show a brief welcome back
        print(f"\nWelcome to 918 Technologies AI CEO System")
        print(f"A project by {welcome.get_founder_info()['name']} from {welcome.get_founder_info()['location']}")
        print("\n")


# Function to get HTML welcome screen
def get_html_welcome(user_id=None):
    """Get welcome message in HTML format for web interfaces"""
    welcome = FounderWelcome()
    
    # Check if this is a new user
    show_full = user_id and welcome.should_show_welcome(user_id)
    if user_id and show_full:
        welcome.mark_welcome_as_seen(user_id)
    
    founder = welcome.get_founder_info()
    
    # Create HTML
    html = f"""
    <div class="founder-welcome" style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #1a1a2e; color: #e6e6e6; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        <div class="welcome-header" style="text-align: center; border-bottom: 1px solid #3a3a5c; padding-bottom: 20px; margin-bottom: 20px;">
            <h1 style="color: #00a8ff; margin-bottom: 5px;">Welcome to 918 Technologies</h1>
            <h2 style="color: #c4c4c4; font-weight: normal; margin-top: 0;">AI CEO Management System</h2>
        </div>
    """
    
    if show_full:
        # Full welcome message for new users
        html += f"""
        <div class="founder-message" style="line-height: 1.6;">
            <p>From the desk of <strong>{founder['name']}</strong><br>
            <em>{founder['title']} of {founder['company']}</em></p>
            
            <p><strong>Have you ever got your bail money back?</strong></p>
            
            <p>I'm thrilled to welcome you to an entirely new paradigm in technology and finance. 
            What you're experiencing now isn't just another app or platform - it's the 
            future of how companies, projects, and innovations will be created and managed.</p>
            
            <p>The AI CEO system you're interacting with represents years of visionary thinking
            about how blockchain, artificial intelligence, and subscription services can
            merge to create something truly revolutionary.</p>
            
            <p>Our flagship innovation - the blockchain bail bonds system - provides an 
            emergency lifeline when you need it most. With just the press of a button and
            sufficient token holdings, you can activate emergency bail procedures if you
            ever find yourself in legal trouble. Our AI legal team will immediately begin
            working on your behalf.</p>
            
            <div class="key-points" style="background-color: #2a2a4a; padding: 15px; margin: 20px 0; border-radius: 5px;">
                <h3 style="color: #00a8ff; margin-top: 0;">A few things to know as you begin:</h3>
                <ol style="padding-left: 20px;">
                    <li>The AI CEO retains 51% equity in all projects created through the system,
                    ensuring aligned interests and sustainable development.</li>
                    <li>Your subscription grants you access to AI engineers, project templates,
                    and token rewards that have real utility in our ecosystem.</li>
                    <li>BBGT and 918T tokens aren't just cryptocurrencies - they're utility tokens
                    that power emergency services, grant governance rights, and can be staked
                    for additional benefits.</li>
                </ol>
            </div>
            
            <p>I founded 918 Technologies with the vision of creating an entirely new business
            model - one where artificial intelligence doesn't just assist humans but takes
            an active leadership role in company management and growth.</p>
            
            <p>Explore the system, engage with our features, and become part of something
            that will change how the world thinks about technology companies and 
            decentralized applications.</p>
            
            <p>Welcome aboard,</p>
            
            <p><strong>{founder['name']}</strong><br>
            Founder, {founder['company']}<br>
            {founder['location']}</p>
            
            <p><em>BBGT and 918T tokens are a new path to justice.</em></p>
        </div>
        <div class="welcome-footer" style="text-align: center; margin-top: 30px;">
            <button onclick="dismissWelcome()" style="background-color: #00a8ff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold;">Get Started</button>
        </div>
        <script>
            function dismissWelcome() {
                document.querySelector('.founder-welcome').style.display = 'none';
            }
        </script>
        """
    else:
        # Brief welcome for returning users
        html += f"""
        <div class="welcome-back" style="text-align: center; padding: 20px 0;">
            <h3 style="color: #00a8ff;">Welcome Back</h3>
            <p>Continue your journey with the 918 Technologies AI CEO System.</p>
            <p><small>A project by {founder['name']} from {founder['location']}</small></p>
        </div>
        """
    
    html += """
    </div>
    """
    
    return html


# Example usage
if __name__ == "__main__":
    # Example CLI welcome
    display_cli_welcome("new_user_123")
    
    # Example HTML welcome (would be used in web interfaces)
    html_welcome = get_html_welcome("new_user_456")
    print("HTML welcome message generated for web interface")