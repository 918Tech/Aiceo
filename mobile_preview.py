"""
AI CEO Mobile App - Main Entry Point for APK
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.animation import Animation
import os
import json
import time
import threading
import random

# Try to import the theme manager
try:
    from theme_manager import theme_manager
except ImportError:
    # Create a minimal theme manager if the full one isn't available
    class ThemeManager:
        def get_theme_color(self, color_type):
            colors = {
                "primary_color": (0, 0.6, 1, 1),
                "background_color": (0.08, 0.08, 0.15, 1),
                "emergency_color": (0.8, 0, 0, 1)
            }
            return colors.get(color_type, (1, 1, 1, 1))

    theme_manager = ThemeManager()

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

        # For command sequence feature
        self.command_sequence = []
        self.expected_sequence = ['up', 'up', 'down', 'down', 'left', 'right', 'left', 'right']
        self.founder_mode = False

        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        # Title
        title = Label(
            text="LOGIN",
            font_size=dp(24),
            size_hint=(1, 0.15),
            color=(0, 0.7, 1, 1),
            bold=True
        )

        # 918 Technologies watermark/button for founder access
        watermark_layout = BoxLayout(
            orientation='vertical', 
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5}
        )

        self.founder_watermark = Button(
            text="918 TECHNOLOGIES",
            font_size=dp(10),
            size_hint=(1, 1),
            background_color=(0.1, 0.1, 0.1, 0.3),
            color=(0.4, 0.4, 0.4, 0.5),
            border=(0, 0, 0, 0)
        )
        self.founder_watermark.bind(on_press=self.on_watermark_press)
        watermark_layout.add_widget(self.founder_watermark)

        # Form layout
        form_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4), spacing=dp(15))

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

        # Founder mode interface (initially hidden)
        self.founder_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.9, 0),  # Zero height to hide initially
            opacity=0,
            spacing=dp(10),
            pos_hint={'center_x': 0.5}
        )

        founder_title = Label(
            text="FOUNDER ACCESS",
            font_size=dp(18),
            color=(0.9, 0.5, 0.1, 1),
            bold=True,
            size_hint=(1, None),
            height=dp(30)
        )

        self.company_email = TextInput(
            hint_text="Company Email (@918tech.com)",
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            disabled=True
        )

        self.otp_input = TextInput(
            hint_text="One-Time Password",
            multiline=False,
            password=True,
            size_hint=(1, None),
            height=dp(50),
            disabled=True
        )

        verify_button = Button(
            text="VERIFY",
            size_hint=(0.8, None),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            background_color=(0.9, 0.5, 0.1, 1),
            disabled=True
        )
        verify_button.bind(on_press=self.verify_founder)
        self.verify_button = verify_button

        self.message_label = Label(
            text="",
            font_size=dp(14),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(30)
        )

        self.founder_layout.add_widget(founder_title)
        self.founder_layout.add_widget(self.company_email)
        self.founder_layout.add_widget(self.otp_input)
        self.founder_layout.add_widget(verify_button)
        self.founder_layout.add_widget(self.message_label)

        # Button layout
        button_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.25), spacing=dp(15))

        login_button = Button(
            text="LOGIN",
            size_hint=(0.8, 0.5),
            pos_hint={'center_x': 0.5},
            background_color=(0.1, 0.6, 0.9, 1)
        )
        login_button.bind(on_press=self.do_login)

        new_user_button = Button(
            text="NEW USER? SIGN UP",
            size_hint=(0.8, 0.5),
            pos_hint={'center_x': 0.5},
            background_color=(0.1, 0.3, 0.5, 1)
        )
        new_user_button.bind(on_press=self.go_to_signup)

        button_layout.add_widget(login_button)
        button_layout.add_widget(new_user_button)

        # Back button
        back_button = Button(
            text="BACK",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5},
            background_color=(0.4, 0.4, 0.4, 1)
        )
        back_button.bind(on_press=self.go_back)

        # ICO Seed Funding Prompt
        self.ico_prompt = Label(
            text="Join our ICO! Get BBGT tokens at early investor rates.",
            font_size=dp(12),
            color=(0.9, 0.7, 0.1, 1),
            size_hint=(1, 0.1),
            halign='center'
        )

        # Add widgets to main layout
        layout.add_widget(title)
        layout.add_widget(self.ico_prompt)
        layout.add_widget(watermark_layout)
        layout.add_widget(form_layout)
        layout.add_widget(self.founder_layout)
        layout.add_widget(button_layout)
        layout.add_widget(back_button)

        # Keyboard binding for command sequence
        Window.bind(on_key_down=self.on_key_down)

        self.add_widget(layout)

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        """Handle keyboard input for the command sequence"""
        if self.founder_mode:
            key_map = {
                273: 'up',     # Up arrow
                274: 'down',   # Down arrow
                276: 'left',   # Left arrow
                275: 'right'   # Right arrow
            }

            if keycode in key_map:
                self.command_sequence.append(key_map[keycode])
                self.message_label.text = f"Sequence: {len(self.command_sequence)}/{len(self.expected_sequence)}"

                # Check if the sequence matches
                if len(self.command_sequence) == len(self.expected_sequence):
                    if self.command_sequence == self.expected_sequence:
                        # Sequence matched, show founder login
                        self.show_founder_login()
                    else:
                        self.message_label.text = "Invalid sequence. Try again."

                    # Reset sequence regardless of match
                    self.command_sequence = []

                return True

        return False

    def on_watermark_press(self, instance):
        """Handle watermark button press to activate founder mode"""
        self.founder_mode = True
        self.founder_watermark.color = (0.9, 0.5, 0.1, 1)  # Highlight the watermark
        self.message_label.text = "Founder mode activated.\nEnter command sequence."

        # Show founder layout
        self.founder_layout.opacity = 1
        self.founder_layout.size_hint = (0.9, 0.3)

    def show_founder_login(self):
        """Show the founder login form"""
        self.message_label.text = "Command verified.\nEnter company email for OTP."
        self.company_email.disabled = False
        self.otp_input.disabled = False
        self.verify_button.disabled = False

    def verify_founder(self, instance):
        """Verify founder credentials and one-time password"""
        email = self.company_email.text
        otp = self.otp_input.text

        # Simulating verification for demo
        if email.endswith('@918tech.com') and otp:
            self.message_label.text = "Verified. Setting up biometric auth..."
            # In a real app, you would trigger biometric setup here

            # For demo, just proceed to dashboard after a delay
            Clock.schedule_once(self.go_to_founder_dashboard, 2)
        else:
            self.message_label.text = "Invalid credentials.\nPlease try again."

    def go_to_founder_dashboard(self, dt):
        """Go to the dashboard as a founder"""
        # Go to special founder dashboard
        self.manager.current = 'founder_dashboard'

    def do_login(self, instance):
        """Handle login button press"""
        email = self.email_input.text
        password = self.password_input.text

        # Here you would normally authenticate the user
        # For demo purposes, we'll just accept any input
        self.manager.current = 'dashboard'

    def go_to_signup(self, instance):
        """Go to signup screen"""
        self.manager.current = 'signup'

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

        # Section labels for organization
        personal_info_label = Label(
            text="PERSONAL INFORMATION",
            font_size=dp(16),
            bold=True,
            size_hint=(0.9, None),
            height=dp(30),
            halign='left',
            pos_hint={'center_x': 0.5}
        )
        form_layout.add_widget(personal_info_label)

        # Personal info fields
        personal_fields = [
            {"hint": "Full Name", "password": False},
            {"hint": "Email", "password": False},
            {"hint": "Password", "password": True},
            {"hint": "Confirm Password", "password": True},
            {"hint": "Phone Number", "password": False}
        ]

        for field in personal_fields:
            input_field = TextInput(
                hint_text=field["hint"],
                multiline=False,
                password=field["password"],
                size_hint=(0.9, None),
                height=dp(50),
                pos_hint={'center_x': 0.5}
            )
            form_layout.add_widget(input_field)

        # Google sign-in option
        google_signin_label = Label(
            text="OR SIGN UP WITH",
            font_size=dp(14),
            size_hint=(0.9, None),
            height=dp(30),
            pos_hint={'center_x': 0.5}
        )
        form_layout.add_widget(google_signin_label)

        google_button = Button(
            text="SIGN UP WITH GOOGLE",
            size_hint=(0.9, None),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            background_color=(0.9, 0.3, 0.3, 1)
        )
        google_button.bind(on_press=self.google_signup)
        form_layout.add_widget(google_button)

        # Payment information section
        payment_label = Label(
            text="PAYMENT INFORMATION (FOR AFTER TRIAL)",
            font_size=dp(16),
            bold=True,
            size_hint=(0.9, None),
            height=dp(30),
            halign='left',
            pos_hint={'center_x': 0.5, 'top': 0.8}  # Adjusted positioning instead of margin
        )
        form_layout.add_widget(payment_label)

        subscription_plan_label = Label(
            text="SUBSCRIPTION: $49.99/month after trial",
            font_size=dp(14),
            size_hint=(0.9, None),
            height=dp(30),
            halign='left',
            color=(0.9, 0.7, 0.1, 1),
            pos_hint={'center_x': 0.5}
        )
        form_layout.add_widget(subscription_plan_label)

        # Payment fields
        payment_fields = [
            {"hint": "Card Number", "password": False},
            {"hint": "Expiration (MM/YY)", "password": False},
            {"hint": "CVC", "password": False},
            {"hint": "Billing Address", "password": False},
            {"hint": "City", "password": False},
            {"hint": "State/Province", "password": False},
            {"hint": "ZIP/Postal Code", "password": False}
        ]

        for field in payment_fields:
            input_field = TextInput(
                hint_text=field["hint"],
                multiline=False,
                password=field["password"],
                size_hint=(0.9, None),
                height=dp(50),
                pos_hint={'center_x': 0.5}
            )
            form_layout.add_widget(input_field)

        # Note about not charging until trial ends
        trial_note = Label(
            text="Your card will not be charged until the 3-hour trial ends",
            font_size=dp(12),
            size_hint=(0.9, None),
            height=dp(30),
            halign='center',
            color=(0.7, 0.7, 0.7, 1),
            pos_hint={'center_x': 0.5}
        )
        form_layout.add_widget(trial_note)

        # Crypto payment option
        crypto_label = Label(
            text="OR PAY WITH CRYPTOCURRENCY",
            font_size=dp(14),
            size_hint=(0.9, None),
            height=dp(30),
            pos_hint={'center_x': 0.5}
        )
        form_layout.add_widget(crypto_label)

        crypto_button = Button(
            text="PAY WITH ETH/BTC",
            size_hint=(0.9, None),
            height=dp(50),
            pos_hint={'center_x': 0.5},
            background_color=(0.3, 0.5, 0.9, 1)
        )
        crypto_button.bind(on_press=self.crypto_payment)
        form_layout.add_widget(crypto_button)

        # Equity agreement checkbox
        equity_label_header = Label(
            text="TERMS & CONDITIONS",
            font_size=dp(16),
            bold=True,
            size_hint=(0.9, None),
            height=dp(30),
            halign='left',
            pos_hint={'center_x': 0.5, 'top': 0.95}  # Use pos_hint instead of margin
        )
        form_layout.add_widget(equity_label_header)

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

        # Auto-renewal agreement
        renewal_layout = BoxLayout(size_hint=(0.9, None), height=dp(70), pos_hint={'center_x': 0.5})
        self.renewal_checkbox = Button(
            text="□",
            size_hint=(0.1, 1),
            background_color=(0.1, 0.6, 0.9, 1)
        )
        self.renewal_checkbox.bind(on_press=self.toggle_renewal_checkbox)
        self.renewal_state = False

        renewal_label = Label(
            text="I agree to auto-renewal of my subscription at $49.99/month after the trial",
            size_hint=(0.9, 1),
            text_size=(Window.width * 0.7, None),
            halign='left',
            valign='center'
        )

        renewal_layout.add_widget(self.renewal_checkbox)
        renewal_layout.add_widget(renewal_label)
        form_layout.add_widget(renewal_layout)

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

    def toggle_renewal_checkbox(self, instance):
        """Toggle renewal checkbox state"""
        self.renewal_state = not self.renewal_state
        instance.text = "☑" if self.renewal_state else "□"

    def google_signup(self, instance):
        """Handle Google sign-up button press"""
        # This would normally initiate OAuth flow with Google
        # For demo, show a message popup
        popup = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        popup.size_hint = (0.8, 0.3)
        popup.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        with popup.canvas.before:
            Color(0.2, 0.2, 0.3, 0.95)
            Rectangle(pos=popup.pos, size=popup.size)
        popup.bind(pos=self._update_popup_rect, size=self._update_popup_rect)

        popup_title = Label(
            text="GOOGLE AUTHENTICATION",
            font_size=dp(18),
            bold=True,
            size_hint=(1, 0.3)
        )

        popup_message = Label(
            text="Redirecting to Google authentication...\nNote: You will still need to provide payment info after login.",
            font_size=dp(14),
            text_size=(Window.width - dp(100), None),
            halign='center',
            size_hint=(1, 0.4)
        )

        close_button = Button(
            text="OK",
            size_hint=(0.5, 0.3),
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

    def crypto_payment(self, instance):
        """Handle crypto payment button press"""
        # This would normally show crypto payment options
        # For demo, show a message popup
        popup = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        popup.size_hint = (0.8, 0.4)
        popup.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        with popup.canvas.before:
            Color(0.2, 0.2, 0.3, 0.95)
            Rectangle(pos=popup.pos, size=popup.size)
        popup.bind(pos=self._update_popup_rect, size=self._update_popup_rect)

        popup_title = Label(
            text="CRYPTO PAYMENT",
            font_size=dp(18),
            bold=True,
            size_hint=(1, 0.2)
        )

        popup_message = Label(
            text="Send 0.01 ETH or 0.0005 BTC to the following address to start your subscription:\n\nETH: 0x1a2b3c4d5e6f...\nBTC: 1A2B3C4D5E6F...",
            font_size=dp(14),
            text_size=(Window.width - dp(100), None),
            halign='center',
            size_hint=(1, 0.5)
        )

        note_label = Label(
            text="Note: Minimum holding of 10 BBGT tokens required for jail insurance",
            font_size=dp(12),
            text_size=(Window.width - dp(100), None),
            halign='center',
            size_hint=(1, 0.1),
            color=(0.9, 0.7, 0.1, 1)
        )

        close_button = Button(
            text="OK",
            size_hint=(0.5, 0.2),
            pos_hint={'center_x': 0.5},
            background_color=(0.1, 0.6, 0.9, 1)
        )

        popup.add_widget(popup_title)
        popup.add_widget(popup_message)
        popup.add_widget(note_label)
        popup.add_widget(close_button)

        # Show popup as an overlay
        self.popup = popup
        self.add_widget(popup)
        close_button.bind(on_press=self.close_popup)

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

class FounderDashboardScreen(BaseScreen):
    """Special dashboard for project founder with administrative capabilities"""
    def __init__(self, **kwargs):
        super(FounderDashboardScreen, self).__init__(**kwargs)
        self.background_color = (0.05, 0.1, 0.2, 1)  # Dark blue background

        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(15))

        # Header with title and logout
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.08))

        title = Label(
            text="FOUNDER CONTROL PANEL",
            font_size=dp(22),
            color=(0.9, 0.5, 0.1, 1),  # Gold color for founder
            bold=True,
            size_hint=(0.8, 1)
        )

        logout_button = Button(
            text="LOGOUT",
            size_hint=(0.2, 0.8),
            pos_hint={'center_y': 0.5},
            background_color=(0.3, 0.3, 0.3, 1)
        )
        logout_button.bind(on_press=self.logout)

        header.add_widget(title)
        header.add_widget(logout_button)

        # Create a tabbed interface for different sections
        tab_panel = TabbedPanel(
            size_hint=(1, 0.92),
            do_default_tab=False,
            tab_pos='top_mid',
            tab_width=dp(150)
        )

        # Project Management Tab
        projects_tab = TabbedPanelItem(text="PROJECTS")
        projects_layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(10))

        # File browser section for selecting local projects
        file_section = BoxLayout(orientation='vertical', size_hint=(1, 0.35), spacing=dp(5))
        file_section_title = Label(
            text="FILE SYSTEM ACCESS",
            font_size=dp(18),
            bold=True,
            size_hint=(1, 0.15),
            halign='left'
        )

        file_path = TextInput(
            hint_text="Project Path",
            multiline=False,
            size_hint=(1, 0.2),
            readonly=True
        )
        self.file_path_input = file_path

        file_buttons = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=dp(10))
        browse_button = Button(
            text="BROWSE",
            size_hint=(0.5, 1),
            background_color=(0.2, 0.5, 0.8, 1)
        )
        browse_button.bind(on_press=self.browse_files)

        create_button = Button(
            text="CREATE NEW",
            size_hint=(0.5, 1),
            background_color=(0.2, 0.5, 0.8, 1)
        )
        create_button.bind(on_press=self.create_project)

        file_buttons.add_widget(browse_button)
        file_buttons.add_widget(create_button)

        file_list = ScrollView(size_hint=(1, 0.45))
        self.file_list_layout = BoxLayout(orientation='vertical', size_hint=(1, None))
        self.file_list_layout.bind(minimum_height=self.file_list_layout.setter('height'))
        file_list.add_widget(self.file_list_layout)

        file_section.add_widget(file_section_title)
        file_section.add_widget(file_path)
        file_section.add_widget(file_buttons)
        file_section.add_widget(file_list)

        # Assimilated Projects section
        projects_section = BoxLayout(orientation='vertical', size_hint=(1, 0.65), spacing=dp(5))
        projects_title = Label(
            text="ASSIMILATED PROJECTS",
            font_size=dp(18),
            bold=True,
            size_hint=(1, 0.1),
            halign='left'
        )

        projects_scroll = ScrollView(size_hint=(1, 0.9))
        projects_list = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(600), spacing=dp(10))

        # Sample projects (in a real app, these would be loaded dynamically)
        project_data = [
            {"name": "AdTV dApp", "progress": 92, "status": "Active"},
            {"name": "Bail Emergency System", "progress": 78, "status": "Active"},
            {"name": "Token Rewards Engine", "progress": 65, "status": "Active"},
            {"name": "Smart Contract Integration", "progress": 45, "status": "In Development"},
            {"name": "Quantum Learning System", "progress": 30, "status": "In Development"}
        ]

        for project in project_data:
            project_card = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(100), padding=dp(10))
            with project_card.canvas.before:
                Color(0.15, 0.2, 0.3, 1)
                Rectangle(pos=project_card.pos, size=project_card.size)
            project_card.bind(pos=self._update_rect, size=self._update_rect)

            project_header = BoxLayout(orientation='horizontal', size_hint=(1, 0.3))
            project_name = Label(
                text=project["name"],
                font_size=dp(16),
                bold=True,
                size_hint=(0.7, 1),
                halign='left',
                text_size=(dp(200), None)
            )

            project_status = Label(
                text=project["status"],
                font_size=dp(14),
                size_hint=(0.3, 1),
                color=(0.2, 0.8, 0.2, 1) if project["status"] == "Active" else (0.8, 0.8, 0.2, 1)
            )

            project_header.add_widget(project_name)
            project_header.add_widget(project_status)

            project_progress_label = Label(
                text=f"Progress: {project['progress']}%",
                font_size=dp(14),
                size_hint=(1, 0.2),
                halign='left',
                text_size=(dp(300), None)
            )

            project_progress = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
            progress_bar_bg = BoxLayout(size_hint=(1, 1))
            with progress_bar_bg.canvas:
                Color(0.2, 0.2, 0.2, 1)
                Rectangle(pos=progress_bar_bg.pos, size=progress_bar_bg.size)
            progress_bar_bg.bind(pos=self._update_rect_progress_bg, size=self._update_rect_progress_bg)

            progress_bar_fg = BoxLayout(size_hint=(project["progress"]/100, 1))
            with progress_bar_fg.canvas:
                Color(0.2, 0.7, 0.3, 1)
                Rectangle(pos=progress_bar_fg.pos, size=progress_bar_fg.size)
            progress_bar_fg.bind(pos=self._update_rect_progress_fg, size=self._update_rect_progress_fg)

            project_progress.add_widget(progress_bar_bg)
            progress_bar_bg.add_widget(progress_bar_fg)

            project_buttons = BoxLayout(orientation='horizontal', size_hint=(1, 0.3), spacing=dp(5))
            view_button = Button(
                text="VIEW DETAILS",
                size_hint=(0.5, 1),
                background_color=(0.2, 0.5, 0.8, 1)
            )
            view_button.bind(on_press=lambda x, name=project["name"]: self.view_project(name))

            update_button = Button(
                text="UPDATE",
                size_hint=(0.5, 1),
                background_color=(0.2, 0.5, 0.8, 1)
            )
            update_button.bind(on_press=lambda x, name=project["name"]: self.update_project(name))

            project_buttons.add_widget(view_button)
            project_buttons.add_widget(update_button)

            project_card.add_widget(project_header)
            project_card.add_widget(project_progress_label)
            project_card.add_widget(project_progress)
            project_card.add_widget(project_buttons)

            projects_list.add_widget(project_card)

        projects_scroll.add_widget(projects_list)
        projects_section.add_widget(projects_title)
        projects_section.add_widget(projects_scroll)

        projects_layout.add_widget(file_section)
        projects_layout.add_widget(projects_section)
        projects_tab.add_widget(projects_layout)

        # Financial Updates Tab
        finance_tab = TabbedPanelItem(text="FINANCIALS")
        finance_layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(10))

        # Revenue section
        revenue_section = BoxLayout(orientation='vertical', size_hint=(1, 0.3), spacing=dp(5))
        revenue_title = Label(
            text="REVENUE OVERVIEW",
            font_size=dp(18),
            bold=True,
            size_hint=(1, 0.2),
            halign='left'
        )

        revenue_grid = GridLayout(cols=3, size_hint=(1, 0.8), spacing=[dp(10), dp(10)])

        # Revenue cards
        revenue_data = [
            {"title": "TOTAL REVENUE", "value": "$127,842.50", "change": "+12.5%"},
            {"title": "SUBSCRIPTIONS", "value": "$98,750.00", "change": "+8.2%"},
            {"title": "TOKEN SALES", "value": "$29,092.50", "change": "+24.7%"},
            {"title": "ACTIVE USERS", "value": "2,541", "change": "+18.3%"},
            {"title": "PREMIUM USERS", "value": "842", "change": "+5.7%"},
            {"title": "AVG REVENUE/USER", "value": "$50.31", "change": "+3.2%"}
        ]

        for item in revenue_data:
            revenue_card = BoxLayout(orientation='vertical', padding=dp(10))
            with revenue_card.canvas.before:
                Color(0.15, 0.2, 0.3, 1)
                Rectangle(pos=revenue_card.pos, size=revenue_card.size)
            revenue_card.bind(pos=self._update_rect, size=self._update_rect)

            title = Label(
                text=item["title"],
                font_size=dp(14),
                size_hint=(1, 0.3),
                halign='center'
            )

            value = Label(
                text=item["value"],
                font_size=dp(20),
                bold=True,
                size_hint=(1, 0.5),
                halign='center'
            )

            change = Label(
                text=item["change"],
                font_size=dp(14),
                size_hint=(1, 0.2),
                halign='center',
                color=(0.2, 0.8, 0.2, 1) if item["change"].startswith("+") else (0.8, 0.2, 0.2, 1)
            )

            revenue_card.add_widget(title)
            revenue_card.add_widget(value)
            revenue_card.add_widget(change)

            revenue_grid.add_widget(revenue_card)

        revenue_section.add_widget(revenue_title)
        revenue_section.add_widget(revenue_grid)

        # Token ecosystem section
        token_section = BoxLayout(orientation='vertical', size_hint=(1, 0.35), spacing=dp(5))
        token_title = Label(
            text="TOKEN ECOSYSTEM",
            font_size=dp(18),
            bold=True,
            size_hint=(1, 0.15),
            halign='left'
        )

        token_grid = GridLayout(cols=2, size_hint=(1, 0.85), spacing=[dp(10), dp(10)])

        # Token stats
        token_data = [
            {"title": "BBGT TOKEN PRICE", "value": "$0.042", "change": "+8.5%", "desc": "24h Change"},
            {"title": "918T TOKEN PRICE", "value": "$0.078", "change": "+12.3%", "desc": "24h Change"},
            {"title": "CIRCULATING SUPPLY", "value": "24.5M BBGT", "change": "70%", "desc": "of Total Supply"},
            {"title": "CIRCULATING SUPPLY", "value": "8.2M 918T", "change": "41%", "desc": "of Total Supply"},
            {"title": "STAKING REWARDS", "value": "2.1M BBGT", "change": "$88,200", "desc": "Value Distributed"},
            {"title": "FOUNDER ALLOCATION", "value": "40%", "change": "$1.25M", "desc": "Current Value"}
        ]

        for item in token_data:
            token_card = BoxLayout(orientation='vertical', padding=dp(10))
            with token_card.canvas.before:
                Color(0.15, 0.2, 0.3, 1)
                Rectangle(pos=token_card.pos, size=token_card.size)
            token_card.bind(pos=self._update_rect, size=self._update_rect)

            title = Label(
                text=item["title"],
                font_size=dp(14),
                size_hint=(1, 0.2),
                halign='left',
                text_size=(dp(200), None)
            )

            value = Label(
                text=item["value"],
                font_size=dp(20),
                bold=True,
                size_hint=(1, 0.4),
                halign='center'
            )

            change = Label(
                text=item["change"],
                font_size=dp(16),
                size_hint=(1, 0.2),
                halign='center',
                color=(0.2, 0.8, 0.2, 1) if item["change"].startswith("+") else (0.9, 0.7, 0.1, 1)
            )

            desc = Label(
                text=item["desc"],
                font_size=dp(12),
                size_hint=(1, 0.2),
                halign='center',
                color=(0.7, 0.7, 0.7, 1)
            )

            token_card.add_widget(title)
            token_card.add_widget(value)
            token_card.add_widget(change)
            token_card.add_widget(desc)

            token_grid.add_widget(token_card)

        token_section.add_widget(token_title)
        token_section.add_widget(token_grid)

        # Ownership section
        ownership_section = BoxLayout(orientation='vertical', size_hint=(1, 0.35), spacing=dp(5))
        ownership_title = Label(
            text="EQUITY & OWNERSHIP",
            font_size=dp(18),
            bold=True,
            size_hint=(1, 0.15),
            halign='left'
        )

        ownership_chart = BoxLayout(orientation='horizontal', size_hint=(1, 0.85))
        with ownership_chart.canvas:
            # This is a simple representation - in a real app, you'd use proper charts
            Color(0.9, 0.5, 0.1, 1)  # Founder color
            Rectangle(pos=(ownership_chart.x, ownership_chart.y), 
                      size=(ownership_chart.width * 0.51, ownership_chart.height))

            Color(0.1, 0.6, 0.9, 1)  # AI CEO color
            Rectangle(pos=(ownership_chart.x + ownership_chart.width * 0.51, ownership_chart.y), 
                      size=(ownership_chart.width * 0.31, ownership_chart.height))

            Color(0.2, 0.7, 0.3, 1)  # Users color
            Rectangle(pos=(ownership_chart.x + ownership_chart.width * 0.82, ownership_chart.y), 
                      size=(ownership_chart.width * 0.18, ownership_chart.height))

        ownership_chart.bind(pos=self._update_ownership_chart, size=self._update_ownership_chart)

        ownership_labels = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        founder_label = Label(
            text="Founder: 51%",
            font_size=dp(14),
            bold=True,
            size_hint=(0.33, 1),
            color=(0.9, 0.5, 0.1, 1)
        )

        ai_ceo_label = Label(
            text="AI CEO: 31%",
            font_size=dp(14),
            bold=True,
            size_hint=(0.33, 1),
            color=(0.1, 0.6, 0.9, 1)
        )

        users_label = Label(
            text="Users: 18%",
            font_size=dp(14),
            bold=True,
            size_hint=(0.33, 1),
            color=(0.2, 0.7, 0.3, 1)
        )

        ownership_labels.add_widget(founder_label)
        ownership_labels.add_widget(ai_ceo_label)
        ownership_labels.add_widget(users_label)

        ownership_info = BoxLayout(orientation='vertical', size_hint=(1, 0.65))

        ownership_actions = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=dp(10))
        update_ownership_button = Button(
            text="UPDATE EQUITY DISTRIBUTION",
            size_hint=(0.5, 1),
            background_color=(0.2, 0.5, 0.8, 1)
        )
        update_ownership_button.bind(on_press=self.update_equity)

        equity_report_button = Button(
            text="GENERATE EQUITY REPORT",
            size_hint=(0.5, 1),
            background_color=(0.2, 0.5, 0.8, 1)
        )
        equity_report_button.bind(on_press=self.generate_equity_report)

        ownership_actions.add_widget(update_ownership_button)
        ownership_actions.add_widget(equity_report_button)

        ownership_info.add_widget(ownership_chart)
        ownership_info.add_widget(ownership_labels)
        ownership_info.add_widget(ownership_actions)

        ownership_section.add_widget(ownership_title)
        ownership_section.add_widget(ownership_info)

        finance_layout.add_widget(revenue_section)
        finance_layout.add_widget(token_section)
        finance_layout.add_widget(ownership_section)
        finance_tab.add_widget(finance_layout)

        # Legal Updates Tab
        legal_tab = TabbedPanelItem(text="LEGAL")
        legal_layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(10))

        # Legal overview section
        legal_overview = BoxLayout(orientation='vertical', size_hint=(1, 0.25), spacing=dp(5))
        legal_title = Label(
            text="LEGAL OVERVIEW",
            font_size=dp(18),
            bold=True,
            size_hint=(1, 0.2),
            halign='left'
        )

        legal_stats = GridLayout(cols=3, size_hint=(1, 0.8), spacing=[dp(10), dp(10)])

        # Legal stats
        legal_data = [
            {"title": "ACTIVE CASES", "value": "12", "status": "8 Pending, 4 Resolved"},
            {"title": "BAIL BONDS ISSUED", "value": "28", "status": "19 Active, 9 Completed"},
            {"title": "LEGAL TEAM", "value": "5 AI Attorneys", "status": "3 Specialized in Bail Law"}
        ]

        for item in legal_data:
            legal_card = BoxLayout(orientation='vertical', padding=dp(10))
            with legal_card.canvas.before:
                Color(0.15, 0.2, 0.3, 1)
                Rectangle(pos=legal_card.pos, size=legal_card.size)
            legal_card.bind(pos=self._update_rect, size=self._update_rect)

            title = Label(
                text=item["title"],
                font_size=dp(14),
                size_hint=(1, 0.3),
                halign='center'
            )

            value = Label(
                text=item["value"],
                font_size=dp(20),
                bold=True,
                size_hint=(1, 0.4),
                halign='center'
            )

            status = Label(
                text=item["status"],
                font_size=dp(12),
                size_hint=(1, 0.3),
                halign='center',
                color=(0.7, 0.7, 0.7, 1)
            )

            legal_card.add_widget(title)
            legal_card.add_widget(value)
            legal_card.add_widget(status)

            legal_stats.add_widget(legal_card)

        legal_overview.add_widget(legal_title)
        legal_overview.add_widget(legal_stats)

        # Recent legal activity section
        legal_activity = BoxLayout(orientation='vertical', size_hint=(1, 0.5), spacing=dp(5))
        activity_title = Label(
            text="RECENT LEGAL ACTIVITY",
            font_size=dp(18),
            bold=True,
            size_hint=(1, 0.1),
            halign='left'
        )

        activity_scroll = ScrollView(size_hint=(1, 0.9))
        activity_list = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(500), spacing=dp(10))

        # Sample legal activities
        activities = [
            {
                "title": "Bail Bond #42874 Successfully Posted",
                "date": "Mar 8, 2025",
                "description": "Bail posted for user John D. in Tulsa County. Bond amount: $5,000. Token collateral: 250 BBGT.",
                "status": "Active"
            },
            {
                "title": "Legal Team Update on Case #38921",
                "date": "Mar 5, 2025",
                "description": "Motion to dismiss filed for charges of minor possession. Hearing scheduled for March 15.",
                "status": "Pending"
            },
            {
                "title": "Token Staking Contract Update",
                "date": "Mar 3, 2025",
                "description": "Smart contract updated to include new staking rewards distribution. 40% to founder, 40% to platform, 20% to users.",
                "status": "Completed"
            },
            {
                "title": "New Legal Jurisdiction Added",
                "date": "Feb 28, 2025",
                "description": "Added support for bail processing in Miami-Dade County. Total supported jurisdictions now at 24 counties.",
                "status": "Completed"
            },
            {
                "title": "Token Distribution Audit",
                "date": "Feb 25, 2025",
                "description": "Annual audit of token distribution completed. All allocations verified according to smart contract specifications.",
                "status": "Completed"
            }
        ]

        for activity in activities:
            activity_card = BoxLayout(orientation='vertical', size_hint=(1, None), height=dp(120), padding=dp(10))
            with activity_card.canvas.before:
                Color(0.15, 0.2, 0.3, 1)
                Rectangle(pos=activity_card.pos, size=activity_card.size)
            activity_card.bind(pos=self._update_rect, size=self._update_rect)

            activity_header = BoxLayout(orientation='horizontal', size_hint=(1, 0.25))
            activity_title_label = Label(
                text=activity["title"],
                font_size=dp(16),
                bold=True,
                size_hint=(0.7, 1),
                halign='left',
                text_size=(dp(250), None)
            )

            status_color = (0.2, 0.8, 0.2, 1) if activity["status"] == "Completed" else \
                          (0.9, 0.7, 0.1, 1) if activity["status"] == "Pending" else \
                          (0.2, 0.6, 0.9, 1)  # Active

            activity_status = Label(
                text=activity["status"],
                font_size=dp(14),
                size_hint=(0.3, 1),
                color=status_color
            )

            activity_header.add_widget(activity_title_label)
            activity_header.add_widget(activity_status)

            activity_date = Label(
                text=activity["date"],
                font_size=dp(12),
                size_hint=(1, 0.15),
                halign='left',
                text_size=(dp(300), None),
                color=(0.7, 0.7, 0.7, 1)
            )

            activity_desc = Label(
                text=activity["description"],
                font_size=dp(14),
                size_hint=(1, 0.4),
                halign='left',
                text_size=(dp(400), None)
            )

            activity_buttons = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=dp(10))
            view_button = Button(
                text="VIEW DETAILS",
                size_hint=(0.5, 1),
                background_color=(0.2, 0.5, 0.8, 1)
            )

            update_button = Button(
                text="UPDATE STATUS",
                size_hint=(0.5, 1),
                background_color=(0.2, 0.5, 0.8, 1)
            )

            activity_buttons.add_widget(view_button)
            activity_buttons.add_widget(update_button)

            activity_card.add_widget(activity_header)
            activity_card.add_widget(activity_date)
            activity_card.add_widget(activity_desc)
            activity_card.add_widget(activity_buttons)

            activity_list.add_widget(activity_card)

        activity_scroll.add_widget(activity_list)
        legal_activity.add_widget(activity_title)
        legal_activity.add_widget(activity_scroll)

        # Compliance section
        compliance_section = BoxLayout(orientation='vertical', size_hint=(1, 0.25), spacing=dp(5))
        compliance_title = Label(
            text="COMPLIANCE STATUS",
            font_size=dp(18),
            bold=True,
            size_hint=(1, 0.2),
            halign='left'
        )

        compliance_status = BoxLayout(orientation='vertical', size_hint=(1, 0.6), padding=dp(10))
        with compliance_status.canvas.before:
            Color(0.15, 0.2, 0.3, 1)
            Rectangle(pos=compliance_status.pos, size=compliance_status.size)
        compliance_status.bind(pos=self._update_rect, size=self._update_rect)

        compliance_status_title = Label(
            text="OVERALL COMPLIANCE: GOOD STANDING",
            font_size=dp(16),
            bold=True,
            size_hint=(1, 0.4),
            color=(0.2, 0.8, 0.2, 1)
        )

        compliance_details = Label(
            text="All required filings up to date. Token contracts audited and verified.\nJurisdictional compliance maintained across 24 counties.\nNext required filing: Annual Report (due in 45 days)",
            font_size=dp(14),
            size_hint=(1, 0.6),
            halign='center',
            text_size=(dp(400), None)
        )

        compliance_status.add_widget(compliance_status_title)
        compliance_status.add_widget(compliance_details)

        compliance_buttons = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=dp(10))
        view_report_button = Button(
            text="VIEW FULL REPORT",
            size_hint=(0.5, 1),
            background_color=(0.2, 0.5, 0.8, 1)
        )

        update_compliance_button = Button(
            text="UPDATE COMPLIANCE",
            size_hint=(0.5, 1),
            background_color=(0.2, 0.5, 0.8, 1)
        )

        compliance_buttons.add_widget(view_report_button)
        compliance_buttons.add_widget(update_compliance_button)

        compliance_section.add_widget(compliance_title)
        compliance_section.add_widget(compliance_status)
        compliance_section.add_widget(compliance_buttons)

        legal_layout.add_widget(legal_overview)
        legal_layout.add_widget(legal_activity)
        legal_layout.add_widget(compliance_section)
        legal_tab.add_widget(legal_layout)

        # Add all tabs to the tab panel
        tab_panel.add_widget(projects_tab)
        tab_panel.add_widget(finance_tab)
        tab_panel.add_widget(legal_tab)
        tab_panel.default_tab = projects_tab

        # Add elements to main layout
        main_layout.add_widget(header)
        main_layout.add_widget(tab_panel)

        self.add_widget(main_layout)

    def _update_rect(self, instance, value):
        """Update rectangle with object's position and size"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.15, 0.2, 0.3, 1)
            Rectangle(pos=instance.pos, size=instance.size)

    def _update_rect_progress_bg(self, instance, value):
        """Update progress bar background rectangle"""
        instance.canvas.clear()
        with instance.canvas:
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(pos=instance.pos, size=instance.size)

    def _update_rect_progress_fg(self, instance, value):
        """Update progress bar foreground rectangle"""
        instance.canvas.clear()
        with instance.canvas:
            Color(0.2, 0.7, 0.3, 1)
            Rectangle(pos=instance.pos, size=instance.size)

    def _update_ownership_chart(self, instance, value):
        """Update ownership chart"""
        instance.canvas.clear()
        with instance.canvas:
            # Founder portion (51%)
            Color(0.9, 0.5, 0.1, 1)
            Rectangle(pos=(instance.x, instance.y), 
                      size=(instance.width * 0.51, instance.height))

            # AI CEO portion (31%)
            Color(0.1, 0.6, 0.9, 1)
            Rectangle(pos=(instance.x + instance.width * 0.51, instance.y), 
                      size=(instance.width * 0.31, instance.height))

            # Users portion (18%)
            Color(0.2, 0.7, 0.3, 1)
            Rectangle(pos=(instance.x + instance.width * 0.82, instance.y), 
                      size=(instance.width * 0.18, instance.height))

    def browse_files(self, instance):
        """Open file browser to select project directory"""
        # In a real app, this would open a file browser dialog
        # For this demo, just simulate selecting a file
        self.file_path_input.text = "/home/user/projects/new_crypto_app"

        # Clear existing files
        self.file_list_layout.clear_widgets()

        # Add sample files
        sample_files = [
            "main.py", "token_rewards.py", "smart_contracts/", 
            "user_auth.py", "wallet_integration.py"
        ]

        for file in sample_files:
            file_button = Button(
                text=file,
                size_hint=(1, None),
                height=dp(40),
                background_color=(0.2, 0.2, 0.3, 1),
                halign='left'
            )
            self.file_list_layout.add_widget(file_button)

    def create_project(self, instance):
        """Create a new project"""
        # In a real app, this would open a dialog to create a new project
        # For this demo, just show a popup message
        popup = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        popup.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        popup.size_hint = (0.8, 0.3)
        with popup.canvas.before:
            Color(0.2, 0.2, 0.3, 0.95)
            Rectangle(pos=popup.pos, size=popup.size)
        popup.bind(pos=self._update_rect, size=self._update_rect)

        popup_title = Label(
            text="CREATE NEW PROJECT",
            font_size=dp(18),
            bold=True,
            size_hint=(1, 0.3)
        )

        popup_message = Label(
            text="New project template created at /home/user/projects/new_project",
            font_size=dp(14),
            size_hint=(1, 0.4),
            halign='center',
            text_size=(Window.width - dp(100), None)
        )

        close_button = Button(
            text="OK",
            size_hint=(0.5, 0.3),
            pos_hint={'center_x': 0.5},
            background_color=(0.2, 0.5, 0.8, 1)
        )

        popup.add_widget(popup_title)
        popup.add_widget(popup_message)
        popup.add_widget(close_button)

        # Show popup as an overlay
        self.popup = popup
        self.add_widget(popup)
        close_button.bind(on_press=self.close_popup)

    def view_project(self, project_name):
        """View project details"""
        print(f"Viewing project: {project_name}")
        # This would open a detailed view of the project

    def update_project(self, project_name):
        """Update project status"""
        print(f"Updating project: {project_name}")
        # This would open project update options

    def update_equity(self, instance):
        """Update equity distribution"""
        print("Updating equity distribution")
        # This would open equity distribution settings

    def generate_equity_report(self, instance):
        """Generate equity report"""
        print("Generating equity report")
        # This would generate a detailed equity report

    def close_popup(self, instance):
        """Close any active popup"""
        if hasattr(self, 'popup') and self.popup in self.children:
            self.remove_widget(self.popup)

    def logout(self, instance):
        """Log out of the founder dashboard"""
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
        sm.add_widget(FounderDashboardScreen(name='founder_dashboard'))

        return sm

if __name__ == '__main__':
    try:
        print("Starting AI CEO Mobile App...")
        AICEOMobileApp().run()
    except Exception as e:
        print(f"Error starting app: {str(e)}")
        import traceback
        traceback.print_exc()