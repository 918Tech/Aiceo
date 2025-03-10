
"""
Theme Manager - Integrates all visual styles for the AI CEO system
"""
import os
import json
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

# Define all available themes
THEMES = {
    "default": {
        "primary_color": "#0097FB",
        "secondary_color": "#97fb00",
        "background_color": "#080815",
        "text_color": "#FFFFFF",
        "accent_color": "#FF2266",
        "emergency_color": "#FF0000",
        "button_color": "#0097FB",
        "founder_color": "#FFA500"
    },
    "borg": {
        "primary_color": "#1AFF1A",
        "secondary_color": "#000000",
        "background_color": "#0A0A0A",
        "text_color": "#1AFF1A",
        "accent_color": "#1AFF1A",
        "emergency_color": "#FF0000",
        "button_color": "#222222",
        "founder_color": "#1AFF1A"
    },
    "terminator": {
        "primary_color": "#FF0000",
        "secondary_color": "#191919",
        "background_color": "#000000",
        "text_color": "#FFFFFF",
        "accent_color": "#FF0000",
        "emergency_color": "#FF0000",
        "button_color": "#333333",
        "founder_color": "#FF6600"
    },
    "mtv": {
        "primary_color": "#FF00FF",
        "secondary_color": "#00FFFF",
        "background_color": "#000000",
        "text_color": "#FFFFFF",
        "accent_color": "#FFFF00",
        "emergency_color": "#FF0000",
        "button_color": "#FF00FF",
        "founder_color": "#FFFF00"
    }
}

# Config file location
CONFIG_FILE = "ai_ceo_config.json"

class ThemeManager:
    """
    Manages the visual themes for the AI CEO system
    """
    def __init__(self):
        self.current_theme = "default"
        self.load_theme_from_config()
    
    def load_theme_from_config(self):
        """Load theme setting from config file"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    if 'theme' in config and config['theme'] in THEMES:
                        self.current_theme = config['theme']
            except (json.JSONDecodeError, IOError):
                print("Error loading theme from config, using default")
    
    def save_theme_to_config(self):
        """Save current theme to config file"""
        config = {}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        config['theme'] = self.current_theme
        
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
        except IOError:
            print("Error saving theme to config")
    
    def set_theme(self, theme_name):
        """Set the current theme"""
        if theme_name in THEMES:
            self.current_theme = theme_name
            self.save_theme_to_config()
            return True
        return False
    
    def get_theme(self):
        """Get the current theme"""
        return THEMES.get(self.current_theme, THEMES["default"])
    
    def apply_theme_to_widget(self, widget, theme_type="background"):
        """Apply the current theme to a widget"""
        theme = self.get_theme()
        
        if theme_type == "background":
            color = get_color_from_hex(theme["background_color"])
        elif theme_type == "button":
            color = get_color_from_hex(theme["button_color"])
        elif theme_type == "accent":
            color = get_color_from_hex(theme["accent_color"])
        elif theme_type == "emergency":
            color = get_color_from_hex(theme["emergency_color"])
        elif theme_type == "founder":
            color = get_color_from_hex(theme["founder_color"])
        else:
            color = get_color_from_hex(theme["primary_color"])
        
        with widget.canvas.before:
            Color(*color)
            Rectangle(pos=widget.pos, size=widget.size)
        
        widget.bind(pos=self._update_rect, size=self._update_rect)
    
    def _update_rect(self, instance, value):
        """Update the rectangle with the widget's position and size"""
        instance.canvas.before.clear()
        self.apply_theme_to_widget(instance)
    
    def get_theme_button(self, text, theme_type="button"):
        """Create a themed button"""
        from kivy.uix.button import Button
        
        theme = self.get_theme()
        
        if theme_type == "emergency":
            bg_color = get_color_from_hex(theme["emergency_color"])
            text_color = get_color_from_hex(theme["text_color"])
        elif theme_type == "accent":
            bg_color = get_color_from_hex(theme["accent_color"])
            text_color = get_color_from_hex(theme["text_color"])
        elif theme_type == "founder":
            bg_color = get_color_from_hex(theme["founder_color"])
            text_color = get_color_from_hex(theme["text_color"])
        else:
            bg_color = get_color_from_hex(theme["button_color"])
            text_color = get_color_from_hex(theme["text_color"])
        
        button = Button(
            text=text,
            background_color=bg_color,
            color=text_color
        )
        
        return button
    
    def get_theme_color(self, color_type):
        """Get a specific color from the current theme"""
        theme = self.get_theme()
        return get_color_from_hex(theme.get(color_type, theme["primary_color"]))

# Create a global instance for use throughout the app
theme_manager = ThemeManager()

def apply_borg_theme(widget):
    """Shortcut for applying the Borg theme to a widget"""
    theme_manager.set_theme("borg")
    theme_manager.apply_theme_to_widget(widget)

def apply_terminator_theme(widget):
    """Shortcut for applying the Terminator theme to a widget"""
    theme_manager.set_theme("terminator")
    theme_manager.apply_theme_to_widget(widget)

def apply_mtv_theme(widget):
    """Shortcut for applying the MTV theme to a widget"""
    theme_manager.set_theme("mtv")
    theme_manager.apply_theme_to_widget(widget)

def reset_to_default_theme(widget):
    """Reset to default theme"""
    theme_manager.set_theme("default")
    theme_manager.apply_theme_to_widget(widget)
