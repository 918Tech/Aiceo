"""
AI CEO Mobile App - Main Entry Point for APK
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.clock import Clock
import os
import json
import time
import threading

# Set default window size for desktop testing
Window.size = (400, 700)

class BaseScreen(Screen):
    """Base screen with common functionality"""
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.background_color = (0.08, 0.08, 0.15, 1)
        
    def on_pre_enter(self):
        """Called before the screen is displayed"""
        with self.canvas.before:
            Color(*self.background_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
    def _update_rect(self, instance, value):
        """Update the background rectangle when size changes"""
        if hasattr(self, 'rect'):
            self.rect.size = instance.size
            self.rect.pos = instance.pos

class WelcomeScreen(BaseScreen):
    """Welcome screen with logo and introduction"""
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Logo and title
        title_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4))
        title = Label(
            text="AI CEO\nMANAGEMENT SYSTEM",
            font_size=dp(28),
            halign='center',
            color=(0, 0.7, 1, 1),
            bold=True,
            size_hint=(1, 0.7)
        )
        subtitle = Label(
            text="Founded by Matthew Blake Ward\nTulsa, Oklahoma",
            font_size=dp(16),
            halign='center',
            size_hint=(1, 0.3)
        )
        title_layout.add_widget(title)
        title_layout.add_widget(subtitle)
        
        # Welcome message
        welcome_box = BoxLayout(orientation='vertical', 
                             size_hint=(1, 0.4),
                             padding=[dp(15), dp(15)],
                             spacing=dp(10))
        with welcome_box.canvas.before:
            Color(0.06, 0.13, 0.24, 1)
            Rectangle(pos=welcome_box.pos, size=welcome_box.size)
        welcome_box.bind(pos=self._update_welcome_rect, size=self._update_welcome_rect)
        
        welcome_title = Label(
            text="HAVE YOU EVER GOT YOUR BAIL MONEY BACK?",
            font_size=dp(16),
            halign='center',
            color=(0.9, 0.9, 0.9, 1),
            bold=True,
            size_hint=(1, 0.2)
        )
        
        welcome_text = Label(
            text=("Welcome to an entirely new paradigm in technology and finance. "
                  "The AI CEO system represents years of visionary thinking about how "
                  "blockchain, artificial intelligence, and subscription services "
                  "can merge to create something truly revolutionary.\n\n"
                  "BBGT and 918T tokens are a new path to justice."),
            font_size=dp(14),
            halign='center',
            valign='top',
            text_size=(Window.width - dp(80), None),
            size_hint=(1, 0.8)
        )
        
        welcome_box.add_widget(welcome_title)
        welcome_box.add_widget(welcome_text)
        
        # Button layout
        button_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3), spacing=dp(15))
        
        login_button = Button(
            text="LOGIN",
            size_hint=(0.8, 0.4),
            pos_hint={'center_x': 0.5},
            background_color=(0.9, 0.1, 0.3, 1)
        )
        login_button.bind(on_press=self.login)
        
        signup_button = Button(
            text="START FREE TRIAL",
            size_hint=(0.8, 0.4),
            pos_hint={'center_x': 0.5},
            background_color=(0.1, 0.6, 0.9, 1)
        )
        signup_button.bind(on_press=self.signup)
        
        emergency_button = Button(
            text="I'M GOING TO JAIL",
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5},
            background_color=(0.8, 0, 0, 1)
        )
        emergency_button.bind(on_press=self.emergency)
        
        button_layout.add_widget(login_button)
        button_layout.add_widget(signup_button)
        button_layout.add_widget(emergency_button)
        
        # Add widgets to main layout
        layout.add_widget(title_layout)
        layout.add_widget(welcome_box)
        layout.add_widget(button_layout)
        
        self.add_widget(layout)
    
    def _update_welcome_rect(self, instance, value):
        """Update welcome box background"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.06, 0.13, 0.24, 1)
            Rectangle(pos=instance.pos, size=instance.size)
    
    def login(self, instance):
        """Handle login button press"""
        self.manager.current = 'login'
    
    def signup(self, instance):
        """Handle signup button press"""
        self.manager.current = 'signup'
    
    def emergency(self, instance):
        """Handle emergency button press"""
        self.manager.current = 'emergency'

class LoginScreen(BaseScreen):
    """Login screen for the application"""
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Title
        title = Label(
            text="LOGIN",
            font_size=dp(24),
            size_hint=(1, 0.2),
            color=(0, 0.7, 1, 1),
            bold=True
        )
        
        # Form layout
        form_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.5), spacing=dp(15))
        
        email_input = TextInput(
            hint_text="Email",
            multiline=False,
            size_hint=(0.9, None),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        self.email_input = email_input
        
        password_input = TextInput(
            hint_text="Password",
            multiline=False,
            password=True,
            size_hint=(0.9, None),
            height=dp(50),
            pos_hint={'center_x': 0.5}
        )
        self.password_input = password_input
        
        form_layout.add_widget(email_input)
        form_layout.add_widget(password_input)
        
        # Button layout
        button_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3), spacing=dp(15))
        
        login_button = Button(
            text="LOGIN",
            size_hint=(0.8, 0.5),
            pos_hint={'center_x': 0.5},
            background_color=(0.1, 0.6, 0.9, 1)
        )
        login_button.bind(on_press=self.do_login)
        
        back_button = Button(
            text="BACK",
            size_hint=(0.8, 0.5),
            pos_hint={'center_x': 0.5},
            background_color=(0.4, 0.4, 0.4, 1)
        )
        back_button.bind(on_press=self.go_back)
        
        button_layout.add_widget(login_button)
        button_layout.add_widget(back_button)
        
        # Add widgets to main layout
        layout.add_widget(title)
        layout.add_widget(form_layout)
        layout.add_widget(button_layout)
        
        self.add_widget(layout)
    
    def do_login(self, instance):
        """Handle login button press"""
        email = self.email_input.text
        password = self.password_input.text
        
        # Here you would normally authenticate the user
        # For demo purposes, we'll just accept any input
        self.manager.current = 'dashboard'
    
    def go_back(self, instance):
        """Go back to welcome screen"""
        self.manager.current = 'welcome'

class SignupScreen(BaseScreen):
    """Signup screen for new users"""
    def __init__(self, **kwargs):
        super(SignupScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Title
        title = Label(
            text="START FREE TRIAL",
            font_size=dp(24),
            size_hint=(1, 0.1),
            color=(0, 0.7, 1, 1),
            bold=True
        )
        
        # Trial info
        trial_info = Label(
            text="3-HOUR FREE TRIAL",
            font_size=dp(16),
            size_hint=(1, 0.1)
        )
        
        # Form layout in a scroll view
        scroll_view = ScrollView(size_hint=(1, 0.6), do_scroll_x=False, do_scroll_y=True)
        form_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint=(1, None), height=dp(400))
        
        # Form fields
        fields = [
            {"hint": "Full Name", "password": False},
            {"hint": "Email", "password": False},
            {"hint": "Password", "password": True},
            {"hint": "Confirm Password", "password": True},
            {"hint": "Phone Number", "password": False}
        ]
        
        for field in fields:
            input_field = TextInput(
                hint_text=field["hint"],
                multiline=False,
                password=field["password"],
                size_hint=(0.9, None),
                height=dp(50),
                pos_hint={'center_x': 0.5}
            )
            form_layout.add_widget(input_field)
        
        # Equity agreement checkbox
        equity_layout = BoxLayout(size_hint=(0.9, None), height=dp(70), pos_hint={'center_x': 0.5})
        self.equity_checkbox = Button(
            text="□",
            size_hint=(0.1, 1),
            background_color=(0.1, 0.6, 0.9, 1)
        )
        self.equity_checkbox.bind(on_press=self.toggle_checkbox)
        self.checkbox_state = False
        
        equity_label = Label(
            text="I agree to give AI CEO 51% equity in all my projects",
            size_hint=(0.9, 1),
            text_size=(Window.width * 0.7, None),
            halign='left',
            valign='center'
        )
        
        equity_layout.add_widget(self.equity_checkbox)
        equity_layout.add_widget(equity_label)
        form_layout.add_widget(equity_layout)
        
        scroll_view.add_widget(form_layout)
        
        # Button layout
        button_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.2), spacing=dp(15))
        
        signup_button = Button(
            text="START FREE TRIAL",
            size_hint=(0.8, 0.5),
            pos_hint={'center_x': 0.5},
            background_color=(0.1, 0.6, 0.9, 1)
        )
        signup_button.bind(on_press=self.do_signup)
        
        back_button = Button(
            text="BACK",
            size_hint=(0.8, 0.5),
            pos_hint={'center_x': 0.5},
            background_color=(0.4, 0.4, 0.4, 1)
        )
        back_button.bind(on_press=self.go_back)
        
        button_layout.add_widget(signup_button)
        button_layout.add_widget(back_button)
        
        # Add widgets to main layout
        layout.add_widget(title)
        layout.add_widget(trial_info)
        layout.add_widget(scroll_view)
        layout.add_widget(button_layout)
        
        self.add_widget(layout)
    
    def toggle_checkbox(self, instance):
        """Toggle checkbox state"""
        self.checkbox_state = not self.checkbox_state
        instance.text = "☑" if self.checkbox_state else "□"
    
    def do_signup(self, instance):
        """Handle signup button press"""
        if not self.checkbox_state:
            # Show error message for equity agreement
            popup = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
            with popup.canvas.before:
                Color(0.8, 0, 0, 0.9)
                Rectangle(pos=popup.pos, size=popup.size)
            popup.bind(pos=self._update_popup_rect, size=self._update_popup_rect)
            
            error_title = Label(
                text="ERROR",
                font_size=dp(18),
                bold=True,
                size_hint=(1, 0.3)
            )
            
            error_message = Label(
                text="You must agree to give AI CEO 51% equity to continue.",
                font_size=dp(14),
                text_size=(Window.width - dp(80), None),
                halign='center',
                size_hint=(1, 0.4)
            )
            
            close_button = Button(
                text="OK",
                size_hint=(0.5, 0.3),
                pos_hint={'center_x': 0.5},
                background_color=(0.1, 0.6, 0.9, 1)
            )
            
            popup.add_widget(error_title)
            popup.add_widget(error_message)
            popup.add_widget(close_button)
            
            # Show popup as an overlay
            self.popup = popup
            self.add_widget(popup)
            close_button.bind(on_press=self.close_popup)
            return
        
        # For demo purposes, we'll just proceed to dashboard
        self.manager.current = 'dashboard'
    
    def _update_popup_rect(self, instance, value):
        """Update popup background"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.8, 0, 0, 0.9)
            Rectangle(pos=instance.pos, size=instance.size)
    
    def close_popup(self, instance):
        """Close the error popup"""
        if hasattr(self, 'popup') and self.popup in self.children:
            self.remove_widget(self.popup)
    
    def go_back(self, instance):
        """Go back to welcome screen"""
        self.manager.current = 'welcome'

class EmergencyScreen(BaseScreen):
    """Emergency screen for the 'I'm going to jail' functionality"""
    def __init__(self, **kwargs):
        super(EmergencyScreen, self).__init__(**kwargs)
        self.background_color = (0.15, 0.05, 0.05, 1)  # Darker red for emergency
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # Title with warning icon
        title = Label(
            text="⚠ EMERGENCY BAIL SYSTEM ⚠",
            font_size=dp(22),
            size_hint=(1, 0.1),
            color=(1, 0.3, 0.3, 1),
            bold=True
        )
        
        # Emergency box
        emergency_box = BoxLayout(orientation='vertical', 
                             size_hint=(1, 0.4),
                             padding=[dp(15), dp(15)],
                             spacing=dp(10))
        with emergency_box.canvas.before:
            Color(0.2, 0.05, 0.05, 1)
            Rectangle(pos=emergency_box.pos, size=emergency_box.size)
        emergency_box.bind(pos=self._update_emergency_rect, size=self._update_emergency_rect)
        
        emergency_title = Label(
            text="I'M GOING TO JAIL",
            font_size=dp(20),
            halign='center',
            color=(1, 0.3, 0.3, 1),
            bold=True,
            size_hint=(1, 0.3)
        )
        
        emergency_text = Label(
            text=("This emergency system will automatically process bail "
                  "using your token holdings. Press only in case of imminent arrest."),
            font_size=dp(14),
            halign='center',
            text_size=(Window.width - dp(80), None),
            size_hint=(1, 0.4)
        )
        
        emergency_button = Button(
            text="ACTIVATE EMERGENCY BAIL",
            size_hint=(0.9, 0.3),
            pos_hint={'center_x': 0.5},
            background_color=(1, 0, 0, 1)
        )
        emergency_button.bind(on_press=self.activate_emergency)
        
        emergency_box.add_widget(emergency_title)
        emergency_box.add_widget(emergency_text)
        emergency_box.add_widget(emergency_button)
        
        # Token status box
        token_box = BoxLayout(orientation='vertical', 
                         size_hint=(1, 0.3),
                         padding=[dp(15), dp(15)],
                         spacing=dp(5))
        with token_box.canvas.before:
            Color(0.05, 0.13, 0.24, 1)
            Rectangle(pos=token_box.pos, size=token_box.size)
        token_box.bind(pos=self._update_token_rect, size=self._update_token_rect)
        
        token_title = Label(
            text="YOUR TOKEN STATUS",
            font_size=dp(16),
            halign='center',
            bold=True,
            size_hint=(1, 0.2)
        )
        
        token_info = Label(
            text=("BBGT Balance: 500 tokens (0.5 ETH equivalent)\n"
                  "918T Balance: 20 tokens (0.2 ETH equivalent)\n"
                  "Maximum Bail Amount: $7,000\n"
                  "Based on current token holdings and 10% requirement"),
            font_size=dp(14),
            halign='center',
            text_size=(Window.width - dp(60), None),
            size_hint=(1, 0.8)
        )
        
        token_box.add_widget(token_title)
        token_box.add_widget(token_info)
        
        # Back button
        back_button = Button(
            text="BACK TO DASHBOARD",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5},
            background_color=(0.1, 0.6, 0.9, 1)
        )
        back_button.bind(on_press=self.go_back)
        
        # Add widgets to main layout
        layout.add_widget(title)
        layout.add_widget(emergency_box)
        layout.add_widget(token_box)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
    def _update_emergency_rect(self, instance, value):
        """Update emergency box background"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.2, 0.05, 0.05, 1)
            Rectangle(pos=instance.pos, size=instance.size)
    
    def _update_token_rect(self, instance, value):
        """Update token box background"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.05, 0.13, 0.24, 1)
            Rectangle(pos=instance.pos, size=instance.size)
    
    def activate_emergency(self, instance):
        """Handle emergency activation button press"""
        # This would normally initiate the emergency bail process
        # For demo, show a confirmation popup
        popup = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10), size_hint=(0.9, 0.4))
        popup.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        with popup.canvas.before:
            Color(0.3, 0.05, 0.05, 0.95)
            Rectangle(pos=popup.pos, size=popup.size)
        popup.bind(pos=self._update_popup_rect, size=self._update_popup_rect)
        
        popup_title = Label(
            text="EMERGENCY ACTIVATED",
            font_size=dp(18),
            bold=True,
            size_hint=(1, 0.3)
        )
        
        popup_message = Label(
            text=("Your emergency bail process has been initiated.\n"
                  "Your location is being tracked and jail databases will be monitored.\n"
                  "Bail will be posted automatically upon booking."),
            font_size=dp(14),
            text_size=(Window.width - dp(100), None),
            halign='center',
            size_hint=(1, 0.5)
        )
        
        close_button = Button(
            text="OK",
            size_hint=(0.5, 0.2),
            pos_hint={'center_x': 0.5},
            background_color=(0.1, 0.6, 0.9, 1)
        )
        
        popup.add_widget(popup_title)
        popup.add_widget(popup_message)
        popup.add_widget(close_button)
        
        # Show popup as an overlay
        self.popup = popup
        self.add_widget(popup)
        close_button.bind(on_press=self.close_popup)
    
    def _update_popup_rect(self, instance, value):
        """Update popup background"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.3, 0.05, 0.05, 0.95)
            Rectangle(pos=instance.pos, size=instance.size)
    
    def close_popup(self, instance):
        """Close the confirmation popup"""
        if hasattr(self, 'popup') and self.popup in self.children:
            self.remove_widget(self.popup)
    
    def go_back(self, instance):
        """Go back to dashboard or welcome screen"""
        if self.manager.has_screen('dashboard'):
            self.manager.current = 'dashboard'
        else:
            self.manager.current = 'welcome'

class DashboardScreen(BaseScreen):
    """Main dashboard screen"""
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(15))
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        
        title = Label(
            text="AI CEO DASHBOARD",
            font_size=dp(20),
            color=(0, 0.7, 1, 1),
            bold=True,
            size_hint=(0.7, 1)
        )
        
        profile_button = Button(
            text="👤",
            font_size=dp(20),
            size_hint=(0.15, 0.8),
            pos_hint={'center_y': 0.5},
            background_color=(0.2, 0.2, 0.3, 1)
        )
        profile_button.bind(on_press=self.show_profile)
        
        settings_button = Button(
            text="⚙",
            font_size=dp(20),
            size_hint=(0.15, 0.8),
            pos_hint={'center_y': 0.5},
            background_color=(0.2, 0.2, 0.3, 1)
        )
        settings_button.bind(on_press=self.show_settings)
        
        header.add_widget(title)
        header.add_widget(profile_button)
        header.add_widget(settings_button)
        
        # Subscription info
        subscription_box = BoxLayout(orientation='vertical', 
                               size_hint=(1, 0.15),
                               padding=[dp(15), dp(15)])
        with subscription_box.canvas.before:
            Color(0.15, 0.3, 0.5, 1)
            Rectangle(pos=subscription_box.pos, size=subscription_box.size)
        subscription_box.bind(pos=self._update_sub_rect, size=self._update_sub_rect)
        
        plan_info = Label(
            text="TRIAL PLAN",
            font_size=dp(18),
            bold=True,
            halign='center',
            size_hint=(1, 0.4)
        )
        
        time_left = Label(
            text="Time Remaining: 2:45:22",
            font_size=dp(14),
            halign='center',
            size_hint=(1, 0.3)
        )
        
        upgrade_button = Button(
            text="UPGRADE TO PREMIUM",
            size_hint=(0.8, 0.3),
            pos_hint={'center_x': 0.5},
            background_color=(0.9, 0.7, 0.2, 1)
        )
        upgrade_button.bind(on_press=self.upgrade_plan)
        
        subscription_box.add_widget(plan_info)
        subscription_box.add_widget(time_left)
        subscription_box.add_widget(upgrade_button)
        
        # Token information
        token_info = BoxLayout(orientation='horizontal', 
                         size_hint=(1, 0.15),
                         spacing=dp(10))
        
        bbgt_box = BoxLayout(orientation='vertical')
        with bbgt_box.canvas.before:
            Color(0.15, 0.3, 0.5, 1)
            Rectangle(pos=bbgt_box.pos, size=bbgt_box.size)
        bbgt_box.bind(pos=self._update_bbgt_rect, size=self._update_bbgt_rect)
        
        bbgt_title = Label(
            text="BBGT TOKEN",
            font_size=dp(16),
            bold=True,
            halign='center',
            size_hint=(1, 0.3)
        )
        
        bbgt_balance = Label(
            text="500",
            font_size=dp(20),
            halign='center',
            size_hint=(1, 0.4)
        )
        
        bbgt_value = Label(
            text="0.5 ETH",
            font_size=dp(14),
            halign='center',
            size_hint=(1, 0.3)
        )
        
        bbgt_box.add_widget(bbgt_title)
        bbgt_box.add_widget(bbgt_balance)
        bbgt_box.add_widget(bbgt_value)
        
        token918_box = BoxLayout(orientation='vertical')
        with token918_box.canvas.before:
            Color(0.25, 0.15, 0.35, 1)
            Rectangle(pos=token918_box.pos, size=token918_box.size)
        token918_box.bind(pos=self._update_918_rect, size=self._update_918_rect)
        
        token918_title = Label(
            text="918T TOKEN",
            font_size=dp(16),
            bold=True,
            halign='center',
            size_hint=(1, 0.3)
        )
        
        token918_balance = Label(
            text="20",
            font_size=dp(20),
            halign='center',
            size_hint=(1, 0.4)
        )
        
        token918_value = Label(
            text="0.2 ETH",
            font_size=dp(14),
            halign='center',
            size_hint=(1, 0.3)
        )
        
        token918_box.add_widget(token918_title)
        token918_box.add_widget(token918_balance)
        token918_box.add_widget(token918_value)
        
        token_info.add_widget(bbgt_box)
        token_info.add_widget(token918_box)
        
        # Main options menu in a scrollview
        scroll_view = ScrollView(size_hint=(1, 0.5), do_scroll_x=False, do_scroll_y=True)
        options_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint=(1, None), height=dp(650))
        
        options = [
            {"text": "EMERGENCY BAIL BUTTON", "color": (0.8, 0, 0, 1), "action": self.show_emergency},
            {"text": "AI LEGAL TEAM", "color": (0.1, 0.5, 0.9, 1), "action": self.show_legal},
            {"text": "CARMEN SANDIEGO GAME", "color": (0.6, 0.1, 0.6, 1), "action": self.show_game},
            {"text": "TOKEN STAKING", "color": (0.1, 0.6, 0.1, 1), "action": self.show_staking},
            {"text": "PROJECT EQUITY", "color": (0.8, 0.6, 0.1, 1), "action": self.show_equity},
            {"text": "QUANTUM LEARNING", "color": (0.3, 0.3, 0.8, 1), "action": self.show_emergency},
            {"text": "NETWORK MANAGER", "color": (0.5, 0.2, 0.5, 1), "action": self.show_emergency},
            {"text": "SMART CONTRACTS", "color": (0.7, 0.4, 0.1, 1), "action": self.show_emergency}
        ]
        
        for option in options:
            button = Button(
                text=option["text"],
                size_hint=(0.9, None),
                height=dp(60),
                pos_hint={'center_x': 0.5},
                background_color=option["color"],
                font_size=dp(16)
            )
            button.bind(on_press=option["action"])
            options_layout.add_widget(button)
        
        # Make sure the layout is tall enough for scrolling
        options_layout.height = len(options) * dp(75)
        scroll_view.add_widget(options_layout)
        
        # Logout button
        logout_button = Button(
            text="LOGOUT",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5},
            background_color=(0.4, 0.4, 0.4, 1)
        )
        logout_button.bind(on_press=self.logout)
        
        # Add widgets to main layout
        layout.add_widget(header)
        layout.add_widget(subscription_box)
        layout.add_widget(token_info)
        layout.add_widget(scroll_view)
        layout.add_widget(logout_button)
        
        self.add_widget(layout)
    
    def _update_sub_rect(self, instance, value):
        """Update subscription box background"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.15, 0.3, 0.5, 1)
            Rectangle(pos=instance.pos, size=instance.size)
    
    def _update_bbgt_rect(self, instance, value):
        """Update BBGT box background"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.15, 0.3, 0.5, 1)
            Rectangle(pos=instance.pos, size=instance.size)
    
    def _update_918_rect(self, instance, value):
        """Update 918T box background"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.25, 0.15, 0.35, 1)
            Rectangle(pos=instance.pos, size=instance.size)
    
    def show_profile(self, instance):
        """Show user profile screen"""
        # In a real app, you would create and switch to a profile screen
        pass
    
    def show_settings(self, instance):
        """Show settings screen"""
        # In a real app, you would create and switch to a settings screen
        pass
    
    def upgrade_plan(self, instance):
        """Upgrade subscription plan"""
        # In a real app, you would show payment options
        pass
    
    def show_emergency(self, instance):
        """Show emergency bail button screen"""
        self.manager.current = 'emergency'
    
    def show_legal(self, instance):
        """Show AI legal team screen"""
        # In a real app, you would create and switch to a legal screen
        pass
    
    def show_game(self, instance):
        """Show Carmen Sandiego game screen"""
        # In a real app, you would create and switch to a game screen
        pass
    
    def show_staking(self, instance):
        """Show token staking screen"""
        # In a real app, you would create and switch to a staking screen
        pass
    
    def show_equity(self, instance):
        """Show project equity screen"""
        # In a real app, you would create and switch to an equity screen
        pass
    
    def logout(self, instance):
        """Log out and return to welcome screen"""
        self.manager.current = 'welcome'

class AICEOMobileApp(App):
    """Main application class"""
    def build(self):
        """Build the UI"""
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(EmergencyScreen(name='emergency'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        
        return sm

if __name__ == '__main__':
    AICEOMobileApp().run()