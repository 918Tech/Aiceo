"""
Theme Manager for AI CEO Mobile App
Provides consistent styling across the application
"""

class ThemeManager:
    """Theme manager for providing consistent colors and styles"""

    def __init__(self):
        """Initialize theme manager with default theme"""
        self.current_theme = "default"
        self.themes = {
            "default": {
                "primary_color": (0, 0.6, 1, 1),
                "background_color": (0.08, 0.08, 0.15, 1),
                "secondary_color": (0.1, 0.3, 0.5, 1),
                "emergency_color": (0.8, 0, 0, 1),
                "success_color": (0.2, 0.8, 0.2, 1),
                "warning_color": (0.9, 0.7, 0.1, 1),
                "text_color": (1, 1, 1, 1),
                "text_secondary_color": (0.7, 0.7, 0.7, 1),
                "button_color": (0.1, 0.6, 0.9, 1),
                "button_secondary_color": (0.4, 0.4, 0.4, 1)
            },
            "dark": {
                "primary_color": (0, 0.5, 0.9, 1),
                "background_color": (0.05, 0.05, 0.1, 1),
                "secondary_color": (0.08, 0.2, 0.4, 1),
                "emergency_color": (0.7, 0, 0, 1),
                "success_color": (0.1, 0.7, 0.1, 1),
                "warning_color": (0.8, 0.6, 0.1, 1),
                "text_color": (0.9, 0.9, 0.9, 1),
                "text_secondary_color": (0.6, 0.6, 0.6, 1),
                "button_color": (0.1, 0.5, 0.8, 1),
                "button_secondary_color": (0.3, 0.3, 0.3, 1)
            },
            "borg": {
                "primary_color": (0.2, 0.8, 0.2, 1),
                "background_color": (0.1, 0.1, 0.1, 1),
                "secondary_color": (0.15, 0.25, 0.15, 1),
                "emergency_color": (0.7, 0, 0, 1),
                "success_color": (0.2, 0.9, 0.2, 1),
                "warning_color": (0.8, 0.8, 0, 1),
                "text_color": (0.2, 0.9, 0.2, 1),
                "text_secondary_color": (0.5, 0.7, 0.5, 1),
                "button_color": (0.1, 0.4, 0.1, 1),
                "button_secondary_color": (0.2, 0.2, 0.2, 1)
            },
            "founder": {
                "primary_color": (0.9, 0.5, 0.1, 1),
                "background_color": (0.15, 0.15, 0.2, 1),
                "secondary_color": (0.25, 0.2, 0.1, 1),
                "emergency_color": (0.8, 0, 0, 1),
                "success_color": (0.2, 0.8, 0.2, 1),
                "warning_color": (0.9, 0.7, 0.1, 1),
                "text_color": (1, 0.9, 0.7, 1),
                "text_secondary_color": (0.8, 0.7, 0.6, 1),
                "button_color": (0.8, 0.4, 0, 1),
                "button_secondary_color": (0.4, 0.3, 0.2, 1)
            }
        }

    def get_theme_color(self, color_type):
        """Get color for the current theme"""
        if color_type in self.themes[self.current_theme]:
            return self.themes[self.current_theme][color_type]
        return (1, 1, 1, 1)  # Default to white if color not found

    def set_theme(self, theme_name):
        """Set current theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False

    def get_available_themes(self):
        """Get list of available themes"""
        return list(self.themes.keys())

    def generate_font_styles(self):
        """Generate font styles for current theme"""
        return {
            "heading": {
                "font_size": 24,
                "bold": True,
                "color": self.get_theme_color("primary_color")
            },
            "subheading": {
                "font_size": 18,
                "bold": True,
                "color": self.get_theme_color("text_color")
            },
            "body": {
                "font_size": 14,
                "color": self.get_theme_color("text_color")
            },
            "caption": {
                "font_size": 12,
                "color": self.get_theme_color("text_secondary_color")
            }
        }

# Create a singleton instance
theme_manager = ThemeManager()