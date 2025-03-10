
"""
AI CEO System - Theme Manager
Provides consistent styling across the application
"""
import json
import os

# Default theme colors
DEFAULT_THEME = {
    "primary_color": (0, 0.6, 1, 1),         # Blue
    "secondary_color": (0.1, 0.3, 0.6, 1),   # Dark blue
    "accent_color": (0.9, 0.5, 0.1, 1),      # Orange/gold for founder
    "background_color": (0.08, 0.08, 0.15, 1), # Dark background
    "surface_color": (0.12, 0.12, 0.2, 1),   # Slightly lighter background
    "error_color": (0.8, 0.0, 0.0, 1),       # Red for errors
    "warning_color": (0.9, 0.7, 0.1, 1),     # Yellow/gold for warnings
    "success_color": (0.2, 0.7, 0.2, 1),     # Green for success
    "text_color": (1, 1, 1, 1),              # White text
    "text_secondary_color": (0.7, 0.7, 0.7, 1), # Gray text
    "emergency_color": (0.8, 0, 0, 1),       # Emergency red
    "disabled_color": (0.5, 0.5, 0.5, 0.5),  # Disabled gray
    "border_color": (0.2, 0.2, 0.3, 1)       # Border color
}

# Theme presets
THEME_PRESETS = {
    "default": DEFAULT_THEME,
    "dark": {
        "primary_color": (0, 0.5, 0.9, 1),
        "secondary_color": (0.1, 0.2, 0.4, 1),
        "accent_color": (0.9, 0.5, 0.1, 1),
        "background_color": (0.05, 0.05, 0.1, 1),
        "surface_color": (0.1, 0.1, 0.15, 1),
        "error_color": (0.8, 0.0, 0.0, 1),
        "warning_color": (0.9, 0.7, 0.0, 1),
        "success_color": (0.2, 0.7, 0.2, 1),
        "text_color": (1, 1, 1, 1),
        "text_secondary_color": (0.7, 0.7, 0.7, 1),
        "emergency_color": (0.8, 0, 0, 1),
        "disabled_color": (0.5, 0.5, 0.5, 0.5),
        "border_color": (0.2, 0.2, 0.3, 1)
    },
    "light": {
        "primary_color": (0, 0.5, 0.9, 1),
        "secondary_color": (0.3, 0.6, 0.9, 1),
        "accent_color": (1, 0.6, 0, 1),
        "background_color": (0.95, 0.95, 0.97, 1),
        "surface_color": (1, 1, 1, 1),
        "error_color": (0.9, 0.1, 0.1, 1),
        "warning_color": (0.9, 0.7, 0.0, 1),
        "success_color": (0.2, 0.8, 0.2, 1),
        "text_color": (0.1, 0.1, 0.1, 1),
        "text_secondary_color": (0.4, 0.4, 0.4, 1),
        "emergency_color": (0.9, 0, 0, 1),
        "disabled_color": (0.7, 0.7, 0.7, 0.5),
        "border_color": (0.8, 0.8, 0.8, 1)
    },
    "borg": {
        "primary_color": (0.1, 0.8, 0.1, 1),  # Borg green
        "secondary_color": (0.05, 0.2, 0.05, 1),
        "accent_color": (0.6, 1, 0.6, 1),
        "background_color": (0.05, 0.1, 0.05, 1),
        "surface_color": (0.1, 0.15, 0.1, 1),
        "error_color": (0.8, 0.0, 0.0, 1),
        "warning_color": (0.9, 0.7, 0.0, 1),
        "success_color": (0.3, 1, 0.3, 1),
        "text_color": (0.8, 1, 0.8, 1),
        "text_secondary_color": (0.6, 0.8, 0.6, 1),
        "emergency_color": (0.8, 0, 0, 1),
        "disabled_color": (0.3, 0.5, 0.3, 0.5),
        "border_color": (0.3, 0.5, 0.3, 1)
    },
    "founder": {
        "primary_color": (0.9, 0.5, 0.1, 1),  # Founder gold
        "secondary_color": (0.4, 0.2, 0.05, 1),
        "accent_color": (0, 0.6, 1, 1),
        "background_color": (0.1, 0.05, 0, 1),
        "surface_color": (0.15, 0.1, 0.05, 1),
        "error_color": (0.8, 0.0, 0.0, 1),
        "warning_color": (1, 0.8, 0.2, 1),
        "success_color": (0.2, 0.7, 0.2, 1),
        "text_color": (1, 0.9, 0.7, 1),
        "text_secondary_color": (0.8, 0.7, 0.5, 1),
        "emergency_color": (0.8, 0, 0, 1),
        "disabled_color": (0.5, 0.4, 0.3, 0.5),
        "border_color": (0.3, 0.2, 0.1, 1)
    }
}

class ThemeManager:
    """Manages application theming"""
    
    def __init__(self, config_path="ai_ceo_config.json"):
        """Initialize with default theme"""
        self.config_path = config_path
        self.current_theme_name = "default"
        self.current_theme = DEFAULT_THEME.copy()
        self.custom_themes = {}
        self.load_theme_settings()
    
    def load_theme_settings(self):
        """Load theme settings from config file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    
                    # Load current theme name
                    if 'theme' in config:
                        self.current_theme_name = config['theme']
                    
                    # Load custom themes if available
                    if 'custom_themes' in config:
                        self.custom_themes = config['custom_themes']
                    
                    # Set current theme
                    self.set_theme(self.current_theme_name)
            except (json.JSONDecodeError, IOError):
                # Use default theme if config can't be loaded
                print("Error loading theme settings, using default")
        else:
            # If no config exists, save the default theme
            self.save_theme_settings()
    
    def save_theme_settings(self):
        """Save theme settings to config file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
            except (json.JSONDecodeError, IOError):
                config = {}
        else:
            config = {}
        
        # Update theme settings
        config['theme'] = self.current_theme_name
        config['custom_themes'] = self.custom_themes
        
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
        except IOError:
            print("Error saving theme settings")
    
    def get_theme_color(self, color_name):
        """Get a specific color from current theme"""
        if color_name in self.current_theme:
            return self.current_theme[color_name]
        return (1, 1, 1, 1)  # Default white if color not found
    
    def set_theme(self, theme_name):
        """Set active theme by name"""
        self.current_theme_name = theme_name
        
        # Check if it's a preset theme
        if theme_name in THEME_PRESETS:
            self.current_theme = THEME_PRESETS[theme_name].copy()
        # Check if it's a custom theme
        elif theme_name in self.custom_themes:
            self.current_theme = self.custom_themes[theme_name].copy()
        else:
            # Fall back to default if theme not found
            self.current_theme_name = "default"
            self.current_theme = DEFAULT_THEME.copy()
        
        self.save_theme_settings()
        return True
    
    def create_custom_theme(self, theme_name, colors):
        """Create a new custom theme"""
        # Start with default theme
        new_theme = DEFAULT_THEME.copy()
        
        # Update with provided colors
        for color_name, color_value in colors.items():
            if color_name in new_theme:
                new_theme[color_name] = color_value
        
        # Save the custom theme
        self.custom_themes[theme_name] = new_theme
        self.save_theme_settings()
        return True
    
    def delete_custom_theme(self, theme_name):
        """Delete a custom theme"""
        if theme_name in self.custom_themes:
            del self.custom_themes[theme_name]
            
            # If current theme was deleted, switch to default
            if self.current_theme_name == theme_name:
                self.set_theme("default")
            
            self.save_theme_settings()
            return True
        return False
    
    def get_available_themes(self):
        """Get list of all available themes"""
        available_themes = list(THEME_PRESETS.keys())
        available_themes.extend(list(self.custom_themes.keys()))
        return available_themes

    def get_kivy_colors(self):
        """Get theme colors formatted for Kivy"""
        colors = {}
        for name, color in self.current_theme.items():
            colors[name] = color
        return colors

# Create a singleton instance
theme_manager = ThemeManager()

def get_theme_manager():
    """Helper function to get the global theme manager"""
    return theme_manager

if __name__ == "__main__":
    # If run directly, print available themes
    tm = ThemeManager()
    print("AI CEO Theme Manager")
    print("===================")
    print(f"Current theme: {tm.current_theme_name}")
    print("\nAvailable themes:")
    for theme in tm.get_available_themes():
        print(f"- {theme}")
    
    # Print current theme colors
    print("\nCurrent theme colors:")
    for name, color in tm.current_theme.items():
        r, g, b, a = color
        print(f"- {name}: rgba({r:.2f}, {g:.2f}, {b:.2f}, {a:.2f})")
