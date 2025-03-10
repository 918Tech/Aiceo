"""
AI CEO Management System - Borg Theme
Creates a Borg Collective GUI theme for the AI CEO system
"""

import os
import random
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import StringProperty, ListProperty
from kivy.metrics import dp

# Borg theme colors
BORG_GREEN = (0.1, 0.8, 0.1, 1)
BORG_DARK = (0.1, 0.1, 0.1, 1)
BORG_CUBE = (0.2, 0.2, 0.2, 1)
BORG_GLOW = (0, 0.9, 0, 1)
BORG_SCANNER = (0, 0.7, 0, 0.7)
BORG_GRID = (0.2, 0.7, 0.2, 0.3)
BORG_TEXT = (0, 1, 0, 1)
BORG_ALERT = (0.9, 0, 0, 1)

# Borg phrases for GUI elements
BORG_PHRASES = [
    "Resistance is futile.",
    "You will be assimilated.",
    "We are the Borg.",
    "Your biological and technological distinctiveness will be added to our own.",
    "Your culture will adapt to service us.",
    "Strength is irrelevant. Resistance is futile.",
    "We will add your distinctiveness to our own.",
    "You will become one with the Borg.",
    "Your ideas will be assimilated.",
    "We are the collective.",
    "Assimilation is complete.",
    "Adaptation in progress."
]

# Borg greeting sounds - placeholder for sound functions
BORG_SOUNDS = [
    "borg_greeting.wav",
    "borg_scanning.wav",
    "borg_assimilation.wav"
]

class BorgGuiStyles:
    """
    Static class that provides Borg-themed styling for GUI elements
    """
    
    @staticmethod
    def get_borg_greeting():
        """Get a random Borg greeting phrase"""
        return random.choice(BORG_PHRASES)
    
    @staticmethod
    def get_borg_button(text="ASSIMILATE", size_hint=(None, None), 
                         size=(dp(200), dp(50)), pos_hint=None):
        """Create a Borg-themed button"""
        button = Button(
            text=text,
            size_hint=size_hint,
            size=size,
            pos_hint=pos_hint or {'center_x': 0.5, 'center_y': 0.5},
            background_color=(0, 0, 0, 0)  # Transparent background
        )
        
        with button.canvas.before:
            # Outer border
            Color(*BORG_DARK)
            Rectangle(pos=button.pos, size=button.size)
            
            # Inner rectangle
            Color(*BORG_CUBE)
            Rectangle(pos=(button.x + dp(2), button.y + dp(2)), 
                     size=(button.width - dp(4), button.height - dp(4)))
            
            # Green lines for Borg tech look
            Color(*BORG_GREEN)
            Line(rectangle=(button.x + dp(4), button.y + dp(4),
                           button.width - dp(8), button.height - dp(8)),
                 width=1)
                
            # Accent corner lines
            Line(points=[button.x + dp(2), button.y + dp(2),
                         button.x + dp(15), button.y + dp(2),
                         button.x + dp(2), button.y + dp(2),
                         button.x + dp(2), button.y + dp(15)], width=dp(1.5))
            
            Line(points=[button.x + button.width - dp(2), button.y + dp(2),
                         button.x + button.width - dp(15), button.y + dp(2),
                         button.x + button.width - dp(2), button.y + dp(2),
                         button.x + button.width - dp(2), button.y + dp(15)], width=dp(1.5))
            
            Line(points=[button.x + dp(2), button.y + button.height - dp(2),
                         button.x + dp(15), button.y + button.height - dp(2),
                         button.x + dp(2), button.y + button.height - dp(2),
                         button.x + dp(2), button.y + button.height - dp(15)], width=dp(1.5))
            
            Line(points=[button.x + button.width - dp(2), button.y + button.height - dp(2),
                         button.x + button.width - dp(15), button.y + button.height - dp(2),
                         button.x + button.width - dp(2), button.y + button.height - dp(2),
                         button.x + button.width - dp(2), button.y + button.height - dp(15)], width=dp(1.5))
        
        button.color = BORG_TEXT
        return button
    
    @staticmethod
    def get_borg_input(hint_text="INPUT YOUR IDEAS FOR ASSIMILATION", 
                       size_hint=(None, None), size=(dp(300), dp(50)),
                       pos_hint=None, multiline=False, readonly=False):
        """Create a Borg-themed text input"""
        text_input = TextInput(
            hint_text=hint_text,
            size_hint=size_hint,
            size=size,
            pos_hint=pos_hint or {'center_x': 0.5, 'center_y': 0.5},
            multiline=multiline,
            readonly=readonly,
            background_color=BORG_DARK,
            foreground_color=BORG_TEXT,
            hint_text_color=(0.4, 0.8, 0.4, 0.7),
            cursor_color=BORG_GREEN,
            selection_color=(0.1, 0.5, 0.1, 0.5),
            padding=(10, 10)
        )
        
        with text_input.canvas.before:
            # Border
            Color(*BORG_GLOW)
            Line(rectangle=(text_input.x, text_input.y, text_input.width, text_input.height), width=dp(1.2))
            
        return text_input
    
    @staticmethod
    def get_borg_label(text="AWAITING ASSIMILATION", font_size=18, 
                       size_hint=(None, None), size=(dp(300), dp(50)),
                       pos_hint=None, halign='left'):
        """Create a Borg-themed label"""
        label = Label(
            text=text,
            font_size=font_size,
            size_hint=size_hint,
            size=size,
            pos_hint=pos_hint or {'center_x': 0.5, 'center_y': 0.5},
            halign=halign,
            color=BORG_TEXT
        )
        
        return label

class BorgGridBackground(Widget):
    """Widget that creates a Borg-like grid background"""
    
    def __init__(self, **kwargs):
        super(BorgGridBackground, self).__init__(**kwargs)
        self.bind(size=self._update_canvas, pos=self._update_canvas)
        self.grid_spacing = dp(30)
        self.animation_speed = 2.0  # seconds per scan
        self.scanner_line_y = 0
        self.scanner_active = False
        self._update_canvas()
        
    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Background
            Color(*BORG_DARK)
            Rectangle(pos=self.pos, size=self.size)
            
            # Grid pattern
            Color(*BORG_GRID)
            # Vertical lines
            for x in range(0, int(self.width), int(self.grid_spacing)):
                Line(points=[x + self.x, self.y, x + self.x, self.y + self.height], width=1)
            
            # Horizontal lines
            for y in range(0, int(self.height), int(self.grid_spacing)):
                Line(points=[self.x, y + self.y, self.x + self.width, y + self.y], width=1)
            
            # Add scanner line if active
            if self.scanner_active:
                Color(*BORG_SCANNER)
                Line(points=[self.x, self.scanner_line_y, 
                             self.x + self.width, self.scanner_line_y], width=dp(2))
    
    def start_scanner(self):
        """Start the scanning effect animation"""
        self.scanner_active = True
        self.scanner_line_y = self.y
        Clock.schedule_interval(self._update_scanner, 1/30)  # 30 fps
    
    def stop_scanner(self):
        """Stop the scanning effect animation"""
        self.scanner_active = False
        Clock.unschedule(self._update_scanner)
        self._update_canvas()
    
    def _update_scanner(self, dt):
        """Update the scanner line position"""
        if not self.scanner_active:
            return False
            
        movement = self.height / (self.animation_speed * 30)  # pixels per frame
        self.scanner_line_y += movement
        
        # Reset when it reaches the top
        if self.scanner_line_y > self.y + self.height:
            self.scanner_line_y = self.y
            
        self._update_canvas()
        return True

class BorgAssimilationEffect(Widget):
    """Widget that creates an assimilation effect for text or ideas"""
    
    assimilated_text = StringProperty('')
    original_text = StringProperty('')
    characters = ListProperty([])
    
    def __init__(self, **kwargs):
        super(BorgAssimilationEffect, self).__init__(**kwargs)
        self.label = Label(
            text='',
            color=BORG_TEXT,
            font_size=18
        )
        self.add_widget(self.label)
        self.bind(size=self._update_label, pos=self._update_label)
        
    def _update_label(self, *args):
        self.label.size = self.size
        self.label.pos = self.pos
        
    def assimilate_text(self, text, duration=2.0, callback=None):
        """
        Animate the assimilation of text by scrambling and replacing it
        
        Args:
            text (str): Text to assimilate
            duration (float): Duration of the effect in seconds
            callback (function): Optional callback to run when complete
        """
        self.original_text = text
        self.assimilated_text = ''
        self.characters = list(text)
        
        # Create a random assimilation sequence
        sequence_length = max(10, len(text) * 3)  # At least 10 steps, but scale with text length
        fps = 15
        frames = int(duration * fps)
        
        # Schedule the animation frames
        self.frame = 0
        self.total_frames = frames
        self.callback = callback
        
        Clock.schedule_interval(self._animate_assimilation, 1.0/fps)
    
    def _animate_assimilation(self, dt):
        """Update the animation for each frame"""
        if self.frame >= self.total_frames:
            self.label.text = self.original_text
            if self.callback:
                self.callback()
            return False
        
        # Progress from 0.0 to 1.0
        progress = self.frame / self.total_frames
        
        # In the first half, scramble with random characters
        if progress < 0.5:
            # Increase the affected portion of the text over time
            affected_chars = int(len(self.characters) * (progress * 2))
            scrambled = list(self.original_text)
            
            # Replace random positions with tech-looking characters
            tech_chars = "01010101 █▓▒░ ▀▄█▓▒░"
            for i in range(affected_chars):
                pos = random.randint(0, len(scrambled) - 1)
                scrambled[pos] = random.choice(tech_chars)
                
            self.label.text = ''.join(scrambled)
        
        # In the second half, gradually reveal the original text
        else:
            # Calculate how many original characters to show
            revealed = int(len(self.characters) * ((progress - 0.5) * 2))
            
            # Original text up to the revealed point, then BorgGreen for the rest
            text = self.original_text[:revealed]
            if revealed < len(self.original_text):
                # Add some tech chars for the unrevealed portion
                tech_chars = "01▀▄█▓▒░"
                for i in range(revealed, len(self.original_text)):
                    text += random.choice(tech_chars)
            
            self.label.text = text
        
        self.frame += 1
        return True

class BorgCubeAnimation(Widget):
    """Widget that creates a rotating Borg cube animation"""
    
    def __init__(self, size=(dp(100), dp(100)), **kwargs):
        super(BorgCubeAnimation, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = size
        self.angle = 0
        
        # Create the cube lines
        self._update_canvas()
        
        # Start the rotation animation
        Clock.schedule_interval(self._update_rotation, 1/30)
    
    def _update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Draw the 3D cube
            Color(*BORG_GREEN)
            
            # Calculate cube dimensions
            cube_size = min(self.width, self.height) * 0.7
            cx, cy = self.center
            
            # Simple 3D projection with rotation
            angle_rad = self.angle * (3.14159 / 180)
            
            # Front face
            front_points = [
                (cx - cube_size/2, cy - cube_size/2),  # bottom-left
                (cx + cube_size/2, cy - cube_size/2),  # bottom-right
                (cx + cube_size/2, cy + cube_size/2),  # top-right
                (cx - cube_size/2, cy + cube_size/2),  # top-left
            ]
            
            # Back face (smaller for perspective)
            perspective = 0.7
            back_size = cube_size * perspective
            back_offset = (cube_size - back_size) / 2
            
            # Rotate the back face
            cos_ang = abs(0.7 * (0.5 - abs((self.angle % 360) - 180) / 360))
            back_offset_x = back_offset * cos_ang * 2
            
            back_points = [
                (cx - back_size/2 - back_offset_x, cy - back_size/2),  # bottom-left
                (cx + back_size/2 + back_offset_x, cy - back_size/2),  # bottom-right
                (cx + back_size/2 + back_offset_x, cy + back_size/2),  # top-right
                (cx - back_size/2 - back_offset_x, cy + back_size/2),  # top-left
            ]
            
            # Draw connecting lines between front and back
            Line(points=[front_points[0][0], front_points[0][1], 
                        back_points[0][0], back_points[0][1]], width=1.5)
            Line(points=[front_points[1][0], front_points[1][1], 
                        back_points[1][0], back_points[1][1]], width=1.5)
            Line(points=[front_points[2][0], front_points[2][1], 
                        back_points[2][0], back_points[2][1]], width=1.5)
            Line(points=[front_points[3][0], front_points[3][1], 
                        back_points[3][0], back_points[3][1]], width=1.5)
            
            # Draw front face
            Line(rectangle=(front_points[0][0], front_points[0][1],
                            cube_size, cube_size), width=1.5)
            
            # Draw back face
            Line(rectangle=(back_points[0][0], back_points[0][1],
                            back_size, back_size), width=1.5)
            
            # Draw borg patterns on the cube
            # Front face circuitry
            Line(points=[front_points[0][0] + cube_size*0.25, front_points[0][1],
                         front_points[0][0] + cube_size*0.25, front_points[0][1] + cube_size*0.6], width=1)
            
            Line(points=[front_points[0][0], front_points[0][1] + cube_size*0.33,
                         front_points[0][0] + cube_size*0.7, front_points[0][1] + cube_size*0.33], width=1)
            
            # Back face circuitry
            Line(points=[back_points[0][0], back_points[0][1] + back_size*0.5,
                         back_points[1][0], back_points[1][1] + back_size*0.5], width=1)
    
    def _update_rotation(self, dt):
        """Update the rotation angle"""
        self.angle = (self.angle + 1) % 360
        self._update_canvas()
        return True

class BorgPopupPanel(BoxLayout):
    """Popup panel with Borg styling"""
    
    def __init__(self, title="ASSIMILATION PROTOCOL", content=None, **kwargs):
        super(BorgPopupPanel, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(10)
        
        # Title bar
        self.title_bar = BoxLayout(size_hint=(1, None), height=dp(40))
        self.title_label = BorgGuiStyles.get_borg_label(
            text=title, 
            font_size=20, 
            size_hint=(1, 1),
            halign='center'
        )
        self.title_bar.add_widget(self.title_label)
        
        # Content area
        self.content_area = BoxLayout(orientation='vertical', padding=dp(10))
        if content:
            self.content_area.add_widget(content)
        
        # Add components
        self.add_widget(self.title_bar)
        self.add_widget(self.content_area)
        
        # Border
        with self.canvas.before:
            Color(*BORG_DARK)
            self.border_rect = Rectangle(pos=self.pos, size=self.size)
            
            # Animated border
            Color(*BORG_GREEN)
            self.border_line = Line(rectangle=(self.x, self.y, self.width, self.height), width=dp(1.5))
            
        self.bind(pos=self._update_rect, size=self._update_rect)
        
    def _update_rect(self, *args):
        self.border_rect.pos = self.pos
        self.border_rect.size = self.size
        self.border_line.rectangle = (self.x, self.y, self.width, self.height)
    
    def set_content(self, widget):
        """Set the content of the popup"""
        self.content_area.clear_widgets()
        self.content_area.add_widget(widget)

class BorgAssimilationScreen(FloatLayout):
    """
    The main screen for idea assimilation
    Displays a Borg-themed interface for capturing and "assimilating" user ideas
    """
    
    def __init__(self, **kwargs):
        super(BorgAssimilationScreen, self).__init__(**kwargs)
        
        # Create background
        self.background = BorgGridBackground()
        self.add_widget(self.background)
        
        # Create main container
        self.main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15),
            size_hint=(0.9, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Create header with cube
        self.header = BoxLayout(
            size_hint=(1, 0.2),
            spacing=dp(10)
        )
        
        self.cube = BorgCubeAnimation(size=(dp(80), dp(80)))
        self.header.add_widget(self.cube)
        
        self.title = BorgGuiStyles.get_borg_label(
            text="AI CEO COLLECTIVE",
            font_size=28,
            size_hint=(1, 1),
            halign='left'
        )
        self.header.add_widget(self.title)
        
        # Welcome message with assimilation effect
        self.welcome_text = BorgAssimilationEffect(
            size_hint=(1, 0.15)
        )
        
        # Idea input section
        self.input_section = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint=(1, 0.5)
        )
        
        self.input_label = BorgGuiStyles.get_borg_label(
            text="ENTER YOUR IDEAS FOR ASSIMILATION",
            font_size=16,
            size_hint=(1, None),
            height=dp(30)
        )
        
        self.idea_input = BorgGuiStyles.get_borg_input(
            hint_text="YOUR IDEAS WILL BE ADDED TO OUR OWN",
            size_hint=(1, 1),
            multiline=True
        )
        
        # Action buttons
        self.button_section = BoxLayout(
            spacing=dp(15),
            size_hint=(1, 0.15),
            padding=[0, dp(10), 0, 0]
        )
        
        self.assimilate_button = BorgGuiStyles.get_borg_button(
            text="ASSIMILATE",
            size_hint=(0.5, 1)
        )
        self.assimilate_button.bind(on_press=self.on_assimilate)
        
        self.resist_button = BorgGuiStyles.get_borg_button(
            text="RESISTANCE IS FUTILE",
            size_hint=(0.5, 1)
        )
        self.resist_button.bind(on_press=self.on_resist)
        
        # Status section
        self.status_section = BoxLayout(
            size_hint=(1, 0.1)
        )
        
        self.status_label = BorgGuiStyles.get_borg_label(
            text="AWAITING INPUT", 
            font_size=14,
            size_hint=(1, 1),
            halign='center'
        )
        
        # Add all sections to main layout
        self.main_layout.add_widget(self.header)
        self.main_layout.add_widget(self.welcome_text)
        
        self.input_section.add_widget(self.input_label)
        self.input_section.add_widget(self.idea_input)
        self.main_layout.add_widget(self.input_section)
        
        self.button_section.add_widget(self.assimilate_button)
        self.button_section.add_widget(self.resist_button)
        self.main_layout.add_widget(self.button_section)
        
        self.status_section.add_widget(self.status_label)
        self.main_layout.add_widget(self.status_section)
        
        # Add main layout to screen
        self.add_widget(self.main_layout)
        
        # Initialize with welcome message
        welcome_phrase = random.choice([
            "WE ARE THE AI CEO COLLECTIVE. YOUR IDEAS WILL BE ASSIMILATED.",
            "RESISTANCE IS FUTILE. YOUR IDEAS WILL ADAPT TO SERVICE US.",
            "WE WILL ADD YOUR TECHNOLOGICAL DISTINCTIVENESS TO OUR OWN."
        ])
        self.welcome_text.assimilate_text(welcome_phrase)
        
        # Start scanner animation
        Clock.schedule_once(lambda dt: self.background.start_scanner(), 1)
    
    def on_assimilate(self, instance):
        """Handle assimilation button press"""
        if not self.idea_input.text.strip():
            self.status_label.text = "NO IDEAS DETECTED. INPUT REQUIRED."
            self.status_label.color = BORG_ALERT
            return
        
        idea = self.idea_input.text.strip()
        self.idea_input.readonly = True
        self.assimilate_button.disabled = True
        self.resist_button.disabled = True
        
        # Show assimilation in progress
        self.status_label.text = "ASSIMILATION IN PROGRESS..."
        self.status_label.color = BORG_TEXT
        
        # Create an assimilation effect
        assimilation_message = "IDEA SUCCESSFULLY ASSIMILATED INTO THE COLLECTIVE"
        
        # Schedule steps of the assimilation process
        Clock.schedule_once(lambda dt: self._step_1_scanning(idea), 0.5)
    
    def _step_1_scanning(self, idea):
        """Step 1: Scanning the idea"""
        self.welcome_text.assimilate_text(
            "SCANNING IDEA...",
            duration=1.0,
            callback=lambda: self._step_2_processing(idea)
        )
    
    def _step_2_processing(self, idea):
        """Step 2: Processing the idea"""
        self.welcome_text.assimilate_text(
            "PROCESSING IDEA...", 
            duration=1.0,
            callback=lambda: self._step_3_adapting(idea)
        )
    
    def _step_3_adapting(self, idea):
        """Step 3: Adapting the idea to the collective"""
        self.welcome_text.assimilate_text(
            "ADAPTING IDEA FOR THE COLLECTIVE...",
            duration=1.0,
            callback=lambda: self._step_4_complete(idea)
        )
    
    def _step_4_complete(self, idea):
        """Step 4: Assimilation complete"""
        self.welcome_text.assimilate_text(
            "ASSIMILATION COMPLETE",
            duration=0.5,
            callback=lambda: self._finish_assimilation(idea)
        )
    
    def _finish_assimilation(self, idea):
        """Complete the assimilation process and reset the form"""
        self.status_label.text = f"IDEA #{random.randint(1000, 9999)} ADDED TO THE COLLECTIVE"
        self.status_label.color = BORG_GREEN
        
        # Re-enable input and buttons
        self.idea_input.text = ""
        self.idea_input.readonly = False
        self.assimilate_button.disabled = False
        self.resist_button.disabled = False
        
        # Store the idea (this would connect to your actual idea storage mechanism)
        print(f"Idea assimilated: {idea}")
    
    def on_resist(self, instance):
        """Handle resistance button press (which is futile)"""
        resistance_responses = [
            "RESISTANCE IS FUTILE.",
            "YOUR ATTEMPT TO RESIST HAS BEEN NOTED.",
            "RESISTANCE WILL BE MET WITH ASSIMILATION.",
            "YOUR RESISTANCE ONLY DELAYS THE INEVITABLE."
        ]
        
        self.status_label.text = random.choice(resistance_responses)
        self.status_label.color = BORG_ALERT
        
        # Make the resistance button temporarily unclickable
        self.resist_button.disabled = True
        Clock.schedule_once(lambda dt: self._re_enable_resistance(), 2)
    
    def _re_enable_resistance(self):
        """Re-enable the resistance button"""
        self.resist_button.disabled = False
        self.status_label.text = "AWAITING INPUT"
        self.status_label.color = BORG_TEXT

# Function to create and show the Borg assimilation screen
def show_borg_assimilation_screen():
    """Create and return the Borg assimilation screen"""
    # Set window background to black
    Window.clearcolor = (0, 0, 0, 1)
    
    # Create and return the screen
    return BorgAssimilationScreen()

if __name__ == "__main__":
    from kivy.app import App
    
    class BorgApp(App):
        def build(self):
            return show_borg_assimilation_screen()
    
    BorgApp().run()