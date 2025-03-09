"""
AdTV Mobile App - MTV-style Retro TV Experience with Learn & Earn
"""

import os
import random
import json
import time
from datetime import datetime
import threading

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.video import Video
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.progressbar import ProgressBar
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

# Import the AdTV System
from adtv_project import AdTVSystem, AdTVChannel, Advertisement, UserProfile

# Set app size for desktop testing - mobile will use full screen
Window.size = (400, 700)

# Define the assets directory
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')

class StaticNoiseEffect:
    """Class to handle TV static noise effects"""
    
    def __init__(self):
        sound_path = os.path.join(ASSETS_DIR, 'static_noise.wav')
        self.static_sound = SoundLoader.load(sound_path) 
        self.static_duration = 1.5  # Duration in seconds
        
    def play_static(self, callback=None):
        """Play static noise effect and execute callback when done"""
        if self.static_sound:
            self.static_sound.play()
            # Schedule the callback after static duration
            if callback:
                Clock.schedule_once(lambda dt: self._finish_static(callback), self.static_duration)
    
    def _finish_static(self, callback):
        """Stop static sound and execute callback"""
        if self.static_sound:
            self.static_sound.stop()
        if callback:
            callback()


class TVStaticImage(Image):
    """Widget to display TV static image/animation"""
    
    def __init__(self, **kwargs):
        super(TVStaticImage, self).__init__(**kwargs)
        self.source = os.path.join(ASSETS_DIR, 'tv_static.png')  # Static image
        self.static_frames = []
        self.current_frame = 0
        self.is_playing = False
        
        # Try to load static frames if available
        for i in range(1, 11):  # Assuming 10 frames
            frame_path = os.path.join(ASSETS_DIR, f'static_frame_{i}.png')
            if os.path.exists(frame_path):
                self.static_frames.append(frame_path)
        
    def play(self, duration=1.5):
        """Play static animation for a given duration"""
        if not self.static_frames:
            # Just show static image if no frames available
            return
            
        self.is_playing = True
        Clock.schedule_interval(self._update_frame, 0.05)  # 50ms per frame
        Clock.schedule_once(self.stop, duration)
    
    def stop(self, dt=None):
        """Stop static animation"""
        self.is_playing = False
        Clock.unschedule(self._update_frame)
        self.source = os.path.join(ASSETS_DIR, 'tv_static.png')  # Return to static image
    
    def _update_frame(self, dt):
        """Update to next frame of static animation"""
        if not self.is_playing or not self.static_frames:
            return
            
        self.current_frame = (self.current_frame + 1) % len(self.static_frames)
        self.source = self.static_frames[self.current_frame]


class RetroTVScreen(BoxLayout):
    """Base layout for the retro TV screen effect"""
    
    def __init__(self, **kwargs):
        super(RetroTVScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.static_effect = StaticNoiseEffect()
        
        # TV Frame
        self.tv_frame = Image(source=os.path.join(ASSETS_DIR, 'tv_frame.png'), size_hint=(1, 1))
        
        # TV Content area (where channel content displays)
        self.content_area = BoxLayout(orientation='vertical', size_hint=(0.8, 0.7), pos_hint={'center_x': 0.5})
        
        # Add static image on top that can be shown during transitions
        self.static_image = TVStaticImage(opacity=0)
        
        self.add_widget(self.tv_frame)
        self.add_widget(self.content_area)
        self.add_widget(self.static_image)
    
    def show_static(self, duration=1.5, callback=None):
        """Show static effect for channel change"""
        # Make static visible
        self.static_image.opacity = 1
        self.static_image.play(duration)
        
        # Play static sound 
        self.static_effect.play_static()
        
        # Schedule end of static
        Clock.schedule_once(lambda dt: self._end_static(callback), duration)
    
    def _end_static(self, callback=None):
        """End static effect"""
        # Fade out static
        anim = Animation(opacity=0, duration=0.3)
        anim.start(self.static_image)
        
        # Execute callback
        if callback:
            callback()


class LoginScreen(Screen):
    """Login screen for the app"""
    
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Logo
        self.logo = Image(source=os.path.join(ASSETS_DIR, 'adtv_logo.png'), size_hint=(1, 0.3))
        
        # Retro TV heading
        self.heading = Label(
            text="ADTV RETRO", 
            font_size=32, 
            size_hint=(1, 0.1),
            color=(0.8, 0.8, 1, 1)
        )
        
        # Login form
        self.form = BoxLayout(orientation='vertical', spacing=15, size_hint=(1, 0.5))
        
        self.username_input = TextInput(
            hint_text="Username",
            multiline=False,
            size_hint=(1, None),
            height=50
        )
        
        self.password_input = TextInput(
            hint_text="Password",
            password=True,
            multiline=False,
            size_hint=(1, None),
            height=50
        )
        
        self.login_button = Button(
            text="LOG IN",
            size_hint=(1, None),
            height=60,
            background_color=(0.2, 0.6, 1, 1)
        )
        self.login_button.bind(on_press=self.do_login)
        
        self.register_button = Button(
            text="REGISTER NEW ACCOUNT",
            size_hint=(1, None),
            height=40,
            background_color=(0.2, 0.2, 0.2, 1)
        )
        
        self.status_label = Label(
            text="",
            size_hint=(1, None),
            height=30
        )
        
        # Add widgets to form
        self.form.add_widget(self.username_input)
        self.form.add_widget(self.password_input)
        self.form.add_widget(self.login_button)
        self.form.add_widget(self.register_button)
        self.form.add_widget(self.status_label)
        
        # Add all components to main layout
        self.layout.add_widget(self.logo)
        self.layout.add_widget(self.heading)
        self.layout.add_widget(self.form)
        
        self.add_widget(self.layout)
        
        # Reference to the app
        self.app = None
    
    def set_app(self, app_instance):
        """Set reference to main app"""
        self.app = app_instance
    
    def do_login(self, instance):
        """Handle login button press"""
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        # Basic validation
        if not username:
            self.status_label.text = "Please enter a username"
            return
            
        # For demo, just check if a user with this name exists
        user = self._find_user(username)
        
        if user:
            # Set the current user
            self.app.set_current_user(user)
            
            # Show static TV effect then switch to main screen
            self.app.root.transition = FadeTransition(duration=0.5)
            self.app.switch_to_main_screen()
        else:
            # Create a new user if it doesn't exist
            user = self.app.adtv_system.create_user(username)
            self.app.set_current_user(user)
            self.status_label.text = "New account created!"
            
            # Schedule transition to main screen
            Clock.schedule_once(lambda dt: self.app.switch_to_main_screen(), 1.5)
    
    def _find_user(self, username):
        """Find a user by username"""
        # Check if username exists in users
        for user_id, user in self.app.adtv_system.users.items():
            if user.username.lower() == username.lower():
                return user
        return None


class ChannelButton(Button):
    """Custom button for TV channels with retro look"""
    
    channel_id = StringProperty('')
    channel_name = StringProperty('')
    
    def __init__(self, **kwargs):
        super(ChannelButton, self).__init__(**kwargs)
        self.background_normal = os.path.join(ASSETS_DIR, 'channel_button.png')
        self.background_down = os.path.join(ASSETS_DIR, 'channel_button_down.png')
        self.size_hint = (1, None)
        self.height = 70
        self.halign = 'left'
        self.valign = 'middle'
        self.text_size = (self.width - 20, None)
        self.font_size = 18


class MainScreen(Screen):
    """Main screen with channel selection"""
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        
        # Main layout
        self.layout = BoxLayout(orientation='vertical')
        
        # Header with user info
        self.header = BoxLayout(
            orientation='horizontal', 
            size_hint=(1, 0.1), 
            padding=10,
            spacing=10
        )
        
        self.username_label = Label(
            text="Guest",
            size_hint=(0.7, 1),
            halign='left',
            valign='middle'
        )
        self.username_label.bind(size=self._update_text_size)
        
        self.points_label = Label(
            text="Points: 0",
            size_hint=(0.3, 1),
            halign='right',
            valign='middle'
        )
        self.points_label.bind(size=self._update_text_size)
        
        self.header.add_widget(self.username_label)
        self.header.add_widget(self.points_label)
        
        # TV Display area
        self.tv_display = RetroTVScreen(size_hint=(1, 0.4))
        
        # Channel list with scroll
        self.scroll_view = ScrollView(size_hint=(1, 0.5))
        self.channel_grid = GridLayout(
            cols=1, 
            spacing=10, 
            size_hint_y=None,
            padding=10
        )
        self.channel_grid.bind(minimum_height=self.channel_grid.setter('height'))
        
        self.scroll_view.add_widget(self.channel_grid)
        
        # Add all components to main layout
        self.layout.add_widget(self.header)
        self.layout.add_widget(self.tv_display)
        self.layout.add_widget(self.scroll_view)
        
        self.add_widget(self.layout)
        
        # Reference to app
        self.app = None
    
    def _update_text_size(self, instance, value):
        """Update text size when widget size changes"""
        instance.text_size = (instance.width, instance.height)
    
    def set_app(self, app_instance):
        """Set reference to main app"""
        self.app = app_instance
    
    def update_user_info(self, username, points):
        """Update the display of user information"""
        self.username_label.text = f"User: {username}"
        self.points_label.text = f"Points: {points}"
    
    def load_channels(self, channels):
        """Load available channels into the grid"""
        self.channel_grid.clear_widgets()
        
        for channel_id, channel in channels.items():
            btn = ChannelButton(
                text=f"{channel.name}",
                channel_id=channel_id,
                channel_name=channel.name
            )
            btn.bind(on_press=self.on_channel_select)
            self.channel_grid.add_widget(btn)
    
    def on_channel_select(self, instance):
        """Handle channel selection"""
        # Show static effect
        self.tv_display.show_static(callback=lambda: self._change_to_channel(instance.channel_id))
    
    def _change_to_channel(self, channel_id):
        """Change to selected channel after static effect"""
        # Tell the app to switch to this channel
        self.app.switch_to_channel(channel_id)


class ChannelScreen(Screen):
    """Screen showing content for a specific channel"""
    
    current_channel_id = StringProperty('')
    
    def __init__(self, **kwargs):
        super(ChannelScreen, self).__init__(**kwargs)
        
        # Main layout
        self.layout = BoxLayout(orientation='vertical')
        
        # Header with back button and channel info
        self.header = BoxLayout(
            orientation='horizontal', 
            size_hint=(1, 0.1),
            padding=10,
            spacing=10
        )
        
        self.back_button = Button(
            text="BACK",
            size_hint=(0.25, 1),
            background_color=(0.5, 0.5, 0.5, 1)
        )
        self.back_button.bind(on_press=self.go_back)
        
        self.channel_name_label = Label(
            text="Channel",
            size_hint=(0.5, 1),
            halign='center',
            valign='middle'
        )
        self.channel_name_label.bind(size=self._update_text_size)
        
        self.ad_mode_button = Button(
            text="WATCH ADS",
            size_hint=(0.25, 1),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        self.ad_mode_button.bind(on_press=self.start_ad_mode)
        
        self.header.add_widget(self.back_button)
        self.header.add_widget(self.channel_name_label)
        self.header.add_widget(self.ad_mode_button)
        
        # TV Display area
        self.tv_display = RetroTVScreen(size_hint=(1, 0.5))
        
        # Content area
        self.content_area = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.4),
            padding=15,
            spacing=10
        )
        
        self.content_title = Label(
            text="Now Playing",
            size_hint=(1, 0.2),
            font_size=20,
            halign='left',
            valign='middle'
        )
        self.content_title.bind(size=self._update_text_size)
        
        self.content_description = Label(
            text="",
            size_hint=(1, 0.6),
            halign='left',
            valign='top',
            text_size=(Window.width - 30, None)
        )
        
        self.next_button = Button(
            text="NEXT PROGRAM",
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        self.next_button.bind(on_press=self.next_program)
        
        self.content_area.add_widget(self.content_title)
        self.content_area.add_widget(self.content_description)
        self.content_area.add_widget(self.next_button)
        
        # Add components to main layout
        self.layout.add_widget(self.header)
        self.layout.add_widget(self.tv_display)
        self.layout.add_widget(self.content_area)
        
        self.add_widget(self.layout)
        
        # Channel content references
        self.current_channel = None
        self.current_content = None
        
        # Reference to app
        self.app = None
    
    def _update_text_size(self, instance, value):
        """Update text size when widget size changes"""
        instance.text_size = (instance.width, instance.height)
    
    def set_app(self, app_instance):
        """Set reference to main app"""
        self.app = app_instance
    
    def set_channel(self, channel_id):
        """Set the current channel being displayed"""
        self.current_channel_id = channel_id
        self.current_channel = self.app.adtv_system.channels.get(channel_id)
        
        if self.current_channel:
            self.channel_name_label.text = self.current_channel.name
            self.load_content()
        else:
            self.channel_name_label.text = "Unknown Channel"
    
    def load_content(self):
        """Load random content from the channel"""
        if not self.current_channel or not self.current_channel.content_blocks:
            self.content_title.text = "No Content Available"
            self.content_description.text = "This channel has no content yet."
            return
            
        # Get random content
        self.current_content = self.current_channel.get_random_content()
        
        if self.current_content:
            self.content_title.text = self.current_content["title"]
            self.content_description.text = self.current_content["content"]
            
            # Record that user is watching this content
            duration = self.current_content["duration"]
            if self.app.current_user:
                self.app.adtv_system.record_watch(
                    self.app.current_user.user_id,
                    self.current_channel_id,
                    duration
                )
    
    def next_program(self, instance):
        """Switch to next program with static effect"""
        self.tv_display.show_static(callback=self.load_content)
    
    def go_back(self, instance):
        """Go back to main channel selection"""
        self.tv_display.show_static(callback=self.app.switch_to_main_screen)
    
    def start_ad_mode(self, instance):
        """Start the ad-watching mode"""
        self.tv_display.show_static(callback=self.app.start_ad_mode)


class AdScreen(Screen):
    """Screen showing advertisements and quizzes"""
    
    def __init__(self, **kwargs):
        super(AdScreen, self).__init__(**kwargs)
        
        # Main layout
        self.layout = BoxLayout(orientation='vertical')
        
        # Header
        self.header = BoxLayout(
            orientation='horizontal', 
            size_hint=(1, 0.1),
            padding=10,
            spacing=10
        )
        
        self.back_button = Button(
            text="EXIT",
            size_hint=(0.2, 1),
            background_color=(0.5, 0.5, 0.5, 1)
        )
        self.back_button.bind(on_press=self.exit_ad_mode)
        
        self.ad_label = Label(
            text="ADVERTISEMENT",
            size_hint=(0.6, 1),
            halign='center',
            valign='middle',
            color=(1, 0.3, 0.3, 1)
        )
        self.ad_label.bind(size=self._update_text_size)
        
        self.points_label = Label(
            text="Points: 0",
            size_hint=(0.2, 1),
            halign='right',
            valign='middle'
        )
        self.points_label.bind(size=self._update_text_size)
        
        self.header.add_widget(self.back_button)
        self.header.add_widget(self.ad_label)
        self.header.add_widget(self.points_label)
        
        # TV Display area
        self.tv_display = RetroTVScreen(size_hint=(1, 0.5))
        
        # Ad content area
        self.ad_content_area = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.4),
            padding=15,
            spacing=10
        )
        
        self.ad_brand = Label(
            text="",
            size_hint=(1, 0.2),
            font_size=24,
            halign='center',
            valign='middle',
            bold=True
        )
        self.ad_brand.bind(size=self._update_text_size)
        
        self.ad_slogan = Label(
            text="",
            size_hint=(1, 0.2),
            font_size=18,
            halign='center',
            valign='middle',
            italic=True
        )
        self.ad_slogan.bind(size=self._update_text_size)
        
        self.ad_content = Label(
            text="",
            size_hint=(1, 0.4),
            halign='center',
            valign='top'
        )
        self.ad_content.bind(size=self._update_text_size)
        
        self.next_ad_button = Button(
            text="NEXT AD (1/5)",
            size_hint=(1, 0.2),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        self.next_ad_button.bind(on_press=self.next_ad)
        
        self.ad_content_area.add_widget(self.ad_brand)
        self.ad_content_area.add_widget(self.ad_slogan)
        self.ad_content_area.add_widget(self.ad_content)
        self.ad_content_area.add_widget(self.next_ad_button)
        
        # Add components to main layout
        self.layout.add_widget(self.header)
        self.layout.add_widget(self.tv_display)
        self.layout.add_widget(self.ad_content_area)
        
        self.add_widget(self.layout)
        
        # Ad block references
        self.current_ads = []
        self.current_ad_index = 0
        self.ads_watched = 0
        self.ad_block_size = 5  # Watch 5 ads before quiz
        
        # Reference to app
        self.app = None
    
    def _update_text_size(self, instance, value):
        """Update text size when widget size changes"""
        instance.text_size = (instance.width, instance.height)
    
    def set_app(self, app_instance):
        """Set reference to main app"""
        self.app = app_instance
    
    def update_points(self, points):
        """Update displayed points"""
        self.points_label.text = f"Points: {points}"
    
    def start_ad_block(self, channel_id=None):
        """Start a new block of advertisements"""
        # Get ads from current channel or general pool
        self.current_ads = self.app.adtv_system.generate_ad_block(
            channel_id,
            self.ad_block_size
        )
        
        # Reset counters
        self.current_ad_index = 0
        self.ads_watched = 0
        
        # Show first ad
        self.show_current_ad()
    
    def show_current_ad(self):
        """Display the current advertisement"""
        if not self.current_ads or self.current_ad_index >= len(self.current_ads):
            # No more ads to show
            self.exit_ad_mode(None)
            return
            
        # Get current ad
        ad = self.current_ads[self.current_ad_index]
        
        # Update display
        self.ad_brand.text = ad.get("brand", "")
        self.ad_slogan.text = ad.get("slogan", "")
        self.ad_content.text = ad.get("content", "")
        
        # Update button
        self.next_ad_button.text = f"NEXT AD ({self.current_ad_index + 1}/{self.ad_block_size})"
        
        # If this is the last ad, change button text
        if self.current_ad_index == self.ad_block_size - 1:
            self.next_ad_button.text = "START QUIZ"
    
    def next_ad(self, instance):
        """Move to next ad or start quiz if all ads watched"""
        # Increase counters
        self.current_ad_index += 1
        self.ads_watched += 1
        
        # Show static effect
        self.tv_display.show_static(callback=self._after_static)
    
    def _after_static(self):
        """Called after static effect"""
        if self.current_ad_index >= self.ad_block_size:
            # All ads watched, start quiz
            self.app.start_quiz_mode()
        else:
            # Show next ad
            self.show_current_ad()
    
    def exit_ad_mode(self, instance):
        """Exit ad mode and return to channel"""
        self.tv_display.show_static(callback=self.app.return_to_channel)


class QuizScreen(Screen):
    """Screen showing ad quiz questions"""
    
    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)
        
        # Main layout
        self.layout = BoxLayout(orientation='vertical')
        
        # Header
        self.header = BoxLayout(
            orientation='horizontal', 
            size_hint=(1, 0.1),
            padding=10,
            spacing=10
        )
        
        self.quiz_label = Label(
            text="AD QUIZ",
            size_hint=(0.7, 1),
            halign='center',
            valign='middle',
            color=(0.3, 0.7, 1, 1)
        )
        self.quiz_label.bind(size=self._update_text_size)
        
        self.streak_label = Label(
            text="Streak: 0",
            size_hint=(0.3, 1),
            halign='right',
            valign='middle'
        )
        self.streak_label.bind(size=self._update_text_size)
        
        self.header.add_widget(self.quiz_label)
        self.header.add_widget(self.streak_label)
        
        # Question area
        self.question_area = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.3),
            padding=15
        )
        
        self.question_label = Label(
            text="Question will appear here",
            size_hint=(1, 1),
            halign='center',
            valign='middle',
            font_size=20
        )
        self.question_label.bind(size=self._update_text_size)
        
        self.question_area.add_widget(self.question_label)
        
        # Answers area
        self.answers_area = GridLayout(
            cols=1,
            size_hint=(1, 0.5),
            padding=15,
            spacing=10
        )
        
        # Results area
        self.results_area = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.1),
            padding=10
        )
        
        self.result_label = Label(
            text="",
            size_hint=(1, 1),
            halign='center',
            valign='middle',
            font_size=18
        )
        self.result_label.bind(size=self._update_text_size)
        
        self.results_area.add_widget(self.result_label)
        
        # Add components to main layout
        self.layout.add_widget(self.header)
        self.layout.add_widget(self.question_area)
        self.layout.add_widget(self.answers_area)
        self.layout.add_widget(self.results_area)
        
        self.add_widget(self.layout)
        
        # Quiz references
        self.current_quiz = []
        self.current_question_index = 0
        self.current_question = None
        self.option_buttons = []
        
        # Reference to app
        self.app = None
    
    def _update_text_size(self, instance, value):
        """Update text size when widget size changes"""
        instance.text_size = (instance.width, instance.height)
    
    def set_app(self, app_instance):
        """Set reference to main app"""
        self.app = app_instance
    
    def update_streak(self, streak):
        """Update displayed streak"""
        self.streak_label.text = f"Streak: {streak}"
    
    def start_quiz(self, ads):
        """Start a quiz based on the ads watched"""
        # Generate quiz questions from the ads
        self.current_quiz = self.app.adtv_system.generate_quiz_for_ads(ads)
        self.current_question_index = 0
        
        # Show first question
        self.show_current_question()
    
    def show_current_question(self):
        """Display the current question"""
        if not self.current_quiz or self.current_question_index >= len(self.current_quiz):
            # No more questions, go back to channel
            self.finish_quiz()
            return
            
        # Get current question
        self.current_question = self.current_quiz[self.current_question_index]
        
        # Update question text
        self.question_label.text = self.current_question["question"]
        
        # Clear previous answer buttons
        self.answers_area.clear_widgets()
        self.option_buttons = []
        
        # Create answer option buttons
        for option in self.current_question["options"]:
            btn = Button(
                text=option,
                size_hint=(1, None),
                height=60,
                background_color=(0.2, 0.2, 0.8, 1)
            )
            btn.bind(on_press=self.on_answer_selected)
            self.answers_area.add_widget(btn)
            self.option_buttons.append(btn)
        
        # Clear previous result
        self.result_label.text = ""
    
    def on_answer_selected(self, instance):
        """Handle when user selects an answer"""
        selected_answer = instance.text
        
        # Process the answer
        result = self.app.answer_question(self.current_question, selected_answer)
        
        # Highlight correct/incorrect
        for btn in self.option_buttons:
            if btn.text == self.current_question["correct_answer"]:
                # Correct answer
                btn.background_color = (0.2, 0.8, 0.2, 1)
            elif btn.text == selected_answer and not result["correct"]:
                # Wrong answer
                btn.background_color = (0.8, 0.2, 0.2, 1)
        
        # Show result
        if result["correct"]:
            self.result_label.text = f"Correct! +{result['points']} points"
            self.result_label.color = (0.2, 0.8, 0.2, 1)
        else:
            self.result_label.text = "Incorrect! Try to remember the ad details."
            self.result_label.color = (0.8, 0.2, 0.2, 1)
        
        # Update streak display
        self.update_streak(result["streak"])
        
        # Schedule next question
        Clock.schedule_once(self.next_question, 2)
    
    def next_question(self, dt):
        """Move to the next question"""
        self.current_question_index += 1
        self.show_current_question()
    
    def finish_quiz(self):
        """Finish the quiz and show results"""
        # Switch back to main screen or channel
        self.app.quiz_completed()


class RewardsScreen(Screen):
    """Screen for viewing and redeeming rewards"""
    
    def __init__(self, **kwargs):
        super(RewardsScreen, self).__init__(**kwargs)
        
        # Main layout
        self.layout = BoxLayout(orientation='vertical')
        
        # Header
        self.header = BoxLayout(
            orientation='horizontal', 
            size_hint=(1, 0.1),
            padding=10,
            spacing=10
        )
        
        self.back_button = Button(
            text="BACK",
            size_hint=(0.2, 1),
            background_color=(0.5, 0.5, 0.5, 1)
        )
        self.back_button.bind(on_press=self.go_back)
        
        self.reward_label = Label(
            text="REWARDS",
            size_hint=(0.6, 1),
            halign='center',
            valign='middle',
            color=(1, 0.8, 0.2, 1)
        )
        self.reward_label.bind(size=self._update_text_size)
        
        self.points_label = Label(
            text="Points: 0",
            size_hint=(0.2, 1),
            halign='right',
            valign='middle'
        )
        self.points_label.bind(size=self._update_text_size)
        
        self.header.add_widget(self.back_button)
        self.header.add_widget(self.reward_label)
        self.header.add_widget(self.points_label)
        
        # Rewards list with scroll
        self.scroll_view = ScrollView(size_hint=(1, 0.9))
        self.rewards_grid = GridLayout(
            cols=1, 
            spacing=15, 
            size_hint_y=None,
            padding=15
        )
        self.rewards_grid.bind(minimum_height=self.rewards_grid.setter('height'))
        
        self.scroll_view.add_widget(self.rewards_grid)
        
        # Add components to main layout
        self.layout.add_widget(self.header)
        self.layout.add_widget(self.scroll_view)
        
        self.add_widget(self.layout)
        
        # Reference to app
        self.app = None
    
    def _update_text_size(self, instance, value):
        """Update text size when widget size changes"""
        instance.text_size = (instance.width, instance.height)
    
    def set_app(self, app_instance):
        """Set reference to main app"""
        self.app = app_instance
    
    def update_points(self, points):
        """Update displayed points"""
        self.points_label.text = f"Points: {points}"
    
    def load_rewards(self):
        """Load available rewards"""
        self.rewards_grid.clear_widgets()
        
        if not self.app.adtv_system.rewards:
            # No rewards available
            label = Label(
                text="No rewards available yet.",
                size_hint=(1, None),
                height=60
            )
            self.rewards_grid.add_widget(label)
            return
            
        # Add each reward as a button
        for reward_id, reward_data in self.app.adtv_system.rewards.items():
            # Create reward panel
            panel = BoxLayout(
                orientation='vertical',
                size_hint=(1, None),
                height=150,
                padding=10,
                spacing=5
            )
            panel.canvas.before.add(Color(0.2, 0.2, 0.2, 1))
            panel.canvas.before.add(Rectangle(pos=panel.pos, size=panel.size))
            
            # Reward name
            name_label = Label(
                text=reward_data["name"],
                size_hint=(1, 0.3),
                font_size=18,
                bold=True,
                halign='left',
                valign='middle'
            )
            name_label.bind(size=self._update_text_size)
            
            # Description
            desc_label = Label(
                text=reward_data["description"],
                size_hint=(1, 0.4),
                halign='left',
                valign='top'
            )
            desc_label.bind(size=self._update_text_size)
            
            # Points and redeem button in horizontal layout
            bottom_layout = BoxLayout(
                orientation='horizontal',
                size_hint=(1, 0.3),
                spacing=10
            )
            
            # Points cost
            cost_label = Label(
                text=f"{reward_data['points_cost']} points",
                size_hint=(0.4, 1),
                color=(1, 0.8, 0.2, 1)
            )
            
            # Inventory (if applicable)
            if reward_data.get("inventory") is not None:
                inventory_text = f"Stock: {reward_data['inventory']}"
                inventory_label = Label(
                    text=inventory_text,
                    size_hint=(0.2, 1)
                )
                bottom_layout.add_widget(inventory_label)
            
            # Redeem button
            redeem_button = Button(
                text="REDEEM",
                size_hint=(0.4, 1),
                background_color=(0.8, 0.4, 0.1, 1)
            )
            redeem_button.reward_id = reward_id
            redeem_button.bind(on_press=self.redeem_reward)
            
            # Disable button if inventory is 0
            if reward_data.get("inventory") == 0:
                redeem_button.disabled = True
            
            # Disable button if user doesn't have enough points
            if self.app.current_user and self.app.current_user.points < reward_data["points_cost"]:
                redeem_button.disabled = True
            
            bottom_layout.add_widget(cost_label)
            bottom_layout.add_widget(redeem_button)
            
            # Add all components to panel
            panel.add_widget(name_label)
            panel.add_widget(desc_label)
            panel.add_widget(bottom_layout)
            
            # Add panel to grid
            self.rewards_grid.add_widget(panel)
    
    def redeem_reward(self, instance):
        """Redeem a reward"""
        reward_id = instance.reward_id
        
        # Try to redeem
        if self.app.redeem_reward(reward_id):
            # Success
            # Refresh the rewards list
            self.load_rewards()
        else:
            # Failed
            pass
    
    def go_back(self, instance):
        """Return to main screen"""
        self.app.switch_to_main_screen()


class ProfileScreen(Screen):
    """Screen for viewing user profile and statistics"""
    
    def __init__(self, **kwargs):
        super(ProfileScreen, self).__init__(**kwargs)
        
        # Main layout
        self.layout = BoxLayout(orientation='vertical')
        
        # Header
        self.header = BoxLayout(
            orientation='horizontal', 
            size_hint=(1, 0.1),
            padding=10,
            spacing=10
        )
        
        self.back_button = Button(
            text="BACK",
            size_hint=(0.2, 1),
            background_color=(0.5, 0.5, 0.5, 1)
        )
        self.back_button.bind(on_press=self.go_back)
        
        self.profile_label = Label(
            text="PROFILE",
            size_hint=(0.8, 1),
            halign='center',
            valign='middle'
        )
        self.profile_label.bind(size=self._update_text_size)
        
        self.header.add_widget(self.back_button)
        self.header.add_widget(self.profile_label)
        
        # User info area
        self.user_info = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.9),
            padding=15,
            spacing=10
        )
        
        # Profile icon and username
        self.top_section = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.2),
            spacing=10
        )
        
        self.profile_icon = Image(
            source='profile_icon.png',
            size_hint=(0.3, 1)
        )
        
        self.username_box = BoxLayout(
            orientation='vertical',
            size_hint=(0.7, 1),
            spacing=5
        )
        
        self.username_label = Label(
            text="Username",
            size_hint=(1, 0.6),
            font_size=24,
            halign='left',
            valign='bottom',
            bold=True
        )
        self.username_label.bind(size=self._update_text_size)
        
        self.joined_label = Label(
            text="Joined: Unknown",
            size_hint=(1, 0.4),
            halign='left',
            valign='top',
            font_size=14
        )
        self.joined_label.bind(size=self._update_text_size)
        
        self.username_box.add_widget(self.username_label)
        self.username_box.add_widget(self.joined_label)
        
        self.top_section.add_widget(self.profile_icon)
        self.top_section.add_widget(self.username_box)
        
        # Stats grid
        self.stats_grid = GridLayout(
            cols=2,
            size_hint=(1, 0.8),
            padding=10,
            spacing=15
        )
        
        # Stats will be added dynamically
        
        # Add components to main layout
        self.user_info.add_widget(self.top_section)
        self.user_info.add_widget(self.stats_grid)
        
        self.layout.add_widget(self.header)
        self.layout.add_widget(self.user_info)
        
        self.add_widget(self.layout)
        
        # Reference to app
        self.app = None
    
    def _update_text_size(self, instance, value):
        """Update text size when widget size changes"""
        instance.text_size = (instance.width, instance.height)
    
    def set_app(self, app_instance):
        """Set reference to main app"""
        self.app = app_instance
    
    def load_profile(self):
        """Load and display user profile data"""
        if not self.app.current_user:
            return
            
        user = self.app.current_user
        
        # Update username and join date
        self.username_label.text = user.username
        
        # Format join date
        try:
            joined_date = datetime.fromisoformat(user.created_at)
            self.joined_label.text = f"Joined: {joined_date.strftime('%B %d, %Y')}"
        except:
            self.joined_label.text = "Joined: Unknown"
        
        # Get user stats
        stats = self.app.adtv_system.get_user_stats(user.user_id)
        
        if not stats:
            return
            
        # Clear stats grid
        self.stats_grid.clear_widgets()
        
        # Add stats to grid
        self._add_stat("Total Points", str(stats["points"]))
        self._add_stat("Current Streak", str(stats["current_streak"]))
        self._add_stat("Best Streak", str(stats["max_streak"]))
        
        # Format watch time in hours and minutes
        watch_time_mins = stats["total_watch_time"] // 60
        hours = watch_time_mins // 60
        minutes = watch_time_mins % 60
        watch_time_str = f"{hours}h {minutes}m"
        self._add_stat("Watch Time", watch_time_str)
        
        self._add_stat("Questions Answered", str(stats["questions_answered"]))
        
        # Format answer rate as percentage
        answer_rate = int(stats["correct_answer_rate"] * 100)
        self._add_stat("Correct Answer Rate", f"{answer_rate}%")
        
        self._add_stat("Rewards Redeemed", str(stats["rewards_redeemed"]))
        
        # Most watched channel
        most_watched = stats["most_watched_channel"] or "None yet"
        self._add_stat("Favorite Channel", most_watched)
    
    def _add_stat(self, label_text, value_text):
        """Add a stat item to the grid"""
        # Label
        label = Label(
            text=label_text,
            size_hint=(0.6, None),
            height=40,
            halign='left',
            valign='middle'
        )
        label.bind(size=self._update_text_size)
        
        # Value
        value = Label(
            text=value_text,
            size_hint=(0.4, None),
            height=40,
            halign='right',
            valign='middle',
            bold=True
        )
        value.bind(size=self._update_text_size)
        
        # Add to grid
        self.stats_grid.add_widget(label)
        self.stats_grid.add_widget(value)
    
    def go_back(self, instance):
        """Return to main screen"""
        self.app.switch_to_main_screen()


class SettingsScreen(Screen):
    """Screen for app settings"""
    
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        
        # Main layout
        self.layout = BoxLayout(orientation='vertical')
        
        # Header
        self.header = BoxLayout(
            orientation='horizontal', 
            size_hint=(1, 0.1),
            padding=10,
            spacing=10
        )
        
        self.back_button = Button(
            text="BACK",
            size_hint=(0.2, 1),
            background_color=(0.5, 0.5, 0.5, 1)
        )
        self.back_button.bind(on_press=self.go_back)
        
        self.settings_label = Label(
            text="SETTINGS",
            size_hint=(0.8, 1),
            halign='center',
            valign='middle'
        )
        self.settings_label.bind(size=self._update_text_size)
        
        self.header.add_widget(self.back_button)
        self.header.add_widget(self.settings_label)
        
        # Settings area
        self.settings_area = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.9),
            padding=15,
            spacing=20
        )
        
        # Bluetooth detection setting
        self.bluetooth_box = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.15),
            spacing=10
        )
        
        self.bluetooth_label = Label(
            text="Bluetooth Detection",
            size_hint=(0.7, 1),
            halign='left',
            valign='middle'
        )
        self.bluetooth_label.bind(size=self._update_text_size)
        
        self.bluetooth_toggle = Button(
            text="ON",
            size_hint=(0.3, 1),
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.bluetooth_toggle.bind(on_press=self.toggle_bluetooth)
        
        self.bluetooth_box.add_widget(self.bluetooth_label)
        self.bluetooth_box.add_widget(self.bluetooth_toggle)
        
        # Notifications setting
        self.notifications_box = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.15),
            spacing=10
        )
        
        self.notifications_label = Label(
            text="Notifications",
            size_hint=(0.7, 1),
            halign='left',
            valign='middle'
        )
        self.notifications_label.bind(size=self._update_text_size)
        
        self.notifications_toggle = Button(
            text="ON",
            size_hint=(0.3, 1),
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.notifications_toggle.bind(on_press=self.toggle_notifications)
        
        self.notifications_box.add_widget(self.notifications_label)
        self.notifications_box.add_widget(self.notifications_toggle)
        
        # Static effect setting
        self.static_box = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.15),
            spacing=10
        )
        
        self.static_label = Label(
            text="Channel Static Effect",
            size_hint=(0.7, 1),
            halign='left',
            valign='middle'
        )
        self.static_label.bind(size=self._update_text_size)
        
        self.static_toggle = Button(
            text="ON",
            size_hint=(0.3, 1),
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.static_toggle.bind(on_press=self.toggle_static)
        
        self.static_box.add_widget(self.static_label)
        self.static_box.add_widget(self.static_toggle)
        
        # Account actions
        self.account_buttons = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.3),
            spacing=15
        )
        
        self.edit_profile_button = Button(
            text="EDIT PROFILE",
            size_hint=(1, 0.5),
            background_color=(0.3, 0.5, 0.8, 1)
        )
        
        self.logout_button = Button(
            text="LOGOUT",
            size_hint=(1, 0.5),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        self.logout_button.bind(on_press=self.logout)
        
        self.account_buttons.add_widget(self.edit_profile_button)
        self.account_buttons.add_widget(self.logout_button)
        
        # Add all setting components
        self.settings_area.add_widget(self.bluetooth_box)
        self.settings_area.add_widget(self.notifications_box)
        self.settings_area.add_widget(self.static_box)
        self.settings_area.add_widget(Label(size_hint=(1, 0.25)))  # Spacer
        self.settings_area.add_widget(self.account_buttons)
        
        # Add components to main layout
        self.layout.add_widget(self.header)
        self.layout.add_widget(self.settings_area)
        
        self.add_widget(self.layout)
        
        # Setting states
        self.bluetooth_enabled = True
        self.notifications_enabled = True
        self.static_enabled = True
        
        # Reference to app
        self.app = None
    
    def _update_text_size(self, instance, value):
        """Update text size when widget size changes"""
        instance.text_size = (instance.width, instance.height)
    
    def set_app(self, app_instance):
        """Set reference to main app"""
        self.app = app_instance
    
    def toggle_bluetooth(self, instance):
        """Toggle Bluetooth detection setting"""
        self.bluetooth_enabled = not self.bluetooth_enabled
        
        if self.bluetooth_enabled:
            instance.text = "ON"
            instance.background_color = (0.2, 0.8, 0.2, 1)
        else:
            instance.text = "OFF"
            instance.background_color = (0.8, 0.2, 0.2, 1)
    
    def toggle_notifications(self, instance):
        """Toggle notifications setting"""
        self.notifications_enabled = not self.notifications_enabled
        
        if self.notifications_enabled:
            instance.text = "ON"
            instance.background_color = (0.2, 0.8, 0.2, 1)
        else:
            instance.text = "OFF"
            instance.background_color = (0.8, 0.2, 0.2, 1)
    
    def toggle_static(self, instance):
        """Toggle static effect setting"""
        self.static_enabled = not self.static_enabled
        
        if self.static_enabled:
            instance.text = "ON"
            instance.background_color = (0.2, 0.8, 0.2, 1)
        else:
            instance.text = "OFF"
            instance.background_color = (0.8, 0.2, 0.2, 1)
            
        # Update app setting
        if self.app:
            self.app.static_enabled = self.static_enabled
    
    def logout(self, instance):
        """Log out the current user"""
        if self.app:
            self.app.logout()
    
    def go_back(self, instance):
        """Return to main screen"""
        self.app.switch_to_main_screen()


class AdTVApp(App):
    """Main AdTV Application"""
    
    def __init__(self, **kwargs):
        super(AdTVApp, self).__init__(**kwargs)
        self.adtv_system = None
        self.current_user = None
        self.current_channel_id = None
        self.current_ad_block = []
        self.static_enabled = True
    
    def build(self):
        """Build the app UI"""
        # Initialize the AdTV system
        self.adtv_system = AdTVSystem()
        
        # Check if we need to create sample data
        if not self.adtv_system.channels:
            from adtv_project import create_sample_adtv
            self.adtv_system = create_sample_adtv()
        
        # Create screen manager
        self.sm = ScreenManager(transition=SlideTransition())
        
        # Create screens
        self.login_screen = LoginScreen(name='login')
        self.main_screen = MainScreen(name='main')
        self.channel_screen = ChannelScreen(name='channel')
        self.ad_screen = AdScreen(name='ad')
        self.quiz_screen = QuizScreen(name='quiz')
        self.rewards_screen = RewardsScreen(name='rewards')
        self.profile_screen = ProfileScreen(name='profile')
        self.settings_screen = SettingsScreen(name='settings')
        
        # Pass app reference to screens
        self.login_screen.set_app(self)
        self.main_screen.set_app(self)
        self.channel_screen.set_app(self)
        self.ad_screen.set_app(self)
        self.quiz_screen.set_app(self)
        self.rewards_screen.set_app(self)
        self.profile_screen.set_app(self)
        self.settings_screen.set_app(self)
        
        # Add screens to manager
        self.sm.add_widget(self.login_screen)
        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.channel_screen)
        self.sm.add_widget(self.ad_screen)
        self.sm.add_widget(self.quiz_screen)
        self.sm.add_widget(self.rewards_screen)
        self.sm.add_widget(self.profile_screen)
        self.sm.add_widget(self.settings_screen)
        
        # Start at login screen
        self.sm.current = 'login'
        
        return self.sm
    
    def set_current_user(self, user):
        """Set the current user and update relevant screens"""
        self.current_user = user
        
        # Update main screen
        self.main_screen.update_user_info(user.username, user.points)
        
        # Load channels
        self.main_screen.load_channels(self.adtv_system.channels)
    
    def switch_to_main_screen(self):
        """Switch to the main channel selection screen"""
        # Update screens with latest data
        if self.current_user:
            self.main_screen.update_user_info(
                self.current_user.username, 
                self.current_user.points
            )
        
        self.sm.current = 'main'
    
    def switch_to_channel(self, channel_id):
        """Switch to view a specific channel"""
        self.current_channel_id = channel_id
        self.channel_screen.set_channel(channel_id)
        self.sm.current = 'channel'
    
    def return_to_channel(self):
        """Return to the current channel after ads or quiz"""
        if self.current_channel_id:
            self.channel_screen.set_channel(self.current_channel_id)
            self.sm.current = 'channel'
        else:
            self.switch_to_main_screen()
    
    def start_ad_mode(self):
        """Start ad-watching mode"""
        # Get ads for current channel
        self.current_ad_block = self.adtv_system.generate_ad_block(
            self.current_channel_id, 
            5  # Block size
        )
        
        # Update points display
        if self.current_user:
            self.ad_screen.update_points(self.current_user.points)
        
        # Start showing ads
        self.ad_screen.start_ad_block(self.current_channel_id)
        self.sm.current = 'ad'
    
    def start_quiz_mode(self):
        """Start quiz mode after watching ads"""
        # Update streak display
        if self.current_user:
            self.quiz_screen.update_streak(self.current_user.streak)
        
        # Start quiz with the ads that were watched
        self.quiz_screen.start_quiz(self.current_ad_block)
        self.sm.current = 'quiz'
    
    def answer_question(self, question, answer):
        """Process a user's answer to a quiz question"""
        if not self.current_user:
            return {"correct": False, "points": 0, "streak": 0, "total_points": 0}
            
        # Process answer through AdTV system
        result = self.adtv_system.answer_question(
            self.current_user.user_id,
            question,
            answer
        )
        
        return result
    
    def quiz_completed(self):
        """Handle completion of a quiz"""
        # Show a short message or reward animation
        # For now, just return to channel
        self.return_to_channel()
    
    def show_rewards(self):
        """Show the rewards screen"""
        # Update points display
        if self.current_user:
            self.rewards_screen.update_points(self.current_user.points)
        
        # Load available rewards
        self.rewards_screen.load_rewards()
        self.sm.current = 'rewards'
    
    def redeem_reward(self, reward_id):
        """Redeem a reward for the current user"""
        if not self.current_user:
            return False
            
        # Try to redeem the reward
        success = self.adtv_system.redeem_reward(
            self.current_user.user_id,
            reward_id
        )
        
        if success and self.current_user:
            # Update points display
            self.rewards_screen.update_points(self.current_user.points)
            
        return success
    
    def show_profile(self):
        """Show the user profile screen"""
        self.profile_screen.load_profile()
        self.sm.current = 'profile'
    
    def show_settings(self):
        """Show the settings screen"""
        self.sm.current = 'settings'
    
    def logout(self):
        """Log out the current user"""
        self.current_user = None
        self.current_channel_id = None
        self.current_ad_block = []
        
        # Return to login screen
        self.sm.current = 'login'


if __name__ == '__main__':
    AdTVApp().run()