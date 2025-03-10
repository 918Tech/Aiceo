
"""
App Configurator - Manage configuration for the AI CEO Mobile App
"""
import os
import json
import time

# Default configuration
DEFAULT_CONFIG = {
    "theme": "default",
    "debug_mode": False,
    "emergency_contact": "",
    "subscription_tier": "trial",
    "token_balance": {
        "BBGT": 500,
        "918T": 20
    },
    "emergency_bail_limit": 7000,
    "trial_expiry": int(time.time()) + (3 * 60 * 60),  # 3 hours from now
    "founder_mode": False,
    "active_subscriptions": {},  # Add this to fix the error
    "user_preferences": {
        "notifications": True,
        "emergency_alerts": True,
        "auto_login": False
    },
    "version": "1.0.0",  # Production version
    "last_update": int(time.time())
}

CONFIG_FILE = "ai_ceo_config.json"

class AppConfigurator:
    """Manages the application configuration"""
    
    def __init__(self):
        """Initialize with current config"""
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    # Update with any missing default values
                    for key, value in DEFAULT_CONFIG.items():
                        if key not in config:
                            config[key] = value
                    return config
            except (json.JSONDecodeError, IOError):
                print("Error loading configuration, using defaults")
        
        # If file doesn't exist or there was an error, use defaults
        return DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            # Update the last_update timestamp
            self.config["last_update"] = int(time.time())
            
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except IOError:
            print("Error saving configuration")
            return False
    
    def get(self, key, default=None):
        """Get a configuration value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value"""
        self.config[key] = value
        return self.save_config()
    
    def update(self, updates):
        """Update multiple configuration values"""
        self.config.update(updates)
        return self.save_config()
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = DEFAULT_CONFIG.copy()
        return self.save_config()
    
    def is_trial_expired(self):
        """Check if the trial period has expired"""
        return time.time() > self.config.get("trial_expiry", 0)
    
    def get_remaining_trial_time(self):
        """Get remaining trial time in seconds"""
        expiry = self.config.get("trial_expiry", 0)
        remaining = expiry - time.time()
        return max(0, remaining)
    
    def get_formatted_trial_time(self):
        """Get formatted remaining trial time"""
        seconds = self.get_remaining_trial_time()
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}:{minutes:02d}:{secs:02d}"
    
    def add_tokens(self, token_type, amount):
        """Add tokens to the user's balance"""
        current = self.config.get("token_balance", {}).get(token_type, 0)
        self.config.setdefault("token_balance", {})
        self.config["token_balance"][token_type] = current + amount
        return self.save_config()
    
    def get_token_balance(self, token_type):
        """Get token balance for a specific token type"""
        return self.config.get("token_balance", {}).get(token_type, 0)

# Create a global instance
app_config = AppConfigurator()

def get_config():
    """Helper function to get the global config"""
    return app_config

if __name__ == "__main__":
    # If run directly, print the current configuration
    config = AppConfigurator()
    print("Current Configuration:")
    print(json.dumps(config.config, indent=2))
    
    # Check trial status
    if config.is_trial_expired():
        print("Trial Status: Expired")
    else:
        print(f"Trial Status: Active - {config.get_formatted_trial_time()} remaining")
