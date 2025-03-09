"""
AI CEO Management System - Kivy GUI Interface
Provides a graphical user interface for the AI CEO system
"""

import os
import threading
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.metrics import dp

# Import the core AI CEO system
from main import AICEOSystem

class ConsoleOutput(ScrollView):
    """A scrollable console output widget"""
    
    def __init__(self, **kwargs):
        super(ConsoleOutput, self).__init__(**kwargs)
        self.layout = GridLayout(cols=1, spacing=dp(2), size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)
        
    def add_message(self, message, is_system=False):
        """Add a message to the console output"""
        label = Label(
            text=message,
            size_hint_y=None,
            height=dp(30),
            halign='left',
            text_size=(self.width, None),
            font_name="RobotoMono-Regular",
            color=(0.8, 1, 0.8, 1) if is_system else (1, 1, 1, 1)
        )
        self.layout.add_widget(label)
        # Scroll to the bottom
        self.scroll_y = 0

class ProjectPanel(TabbedPanelItem):
    """Panel for project management"""
    
    def __init__(self, ai_ceo_app, **kwargs):
        super(ProjectPanel, self).__init__(**kwargs)
        self.text = 'Project'
        self.ai_ceo_app = ai_ceo_app
        
        # Create layout
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # Project path section
        path_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        path_layout.add_widget(Label(text='Project Path:', size_hint_x=0.3))
        
        self.path_input = TextInput(
            text=self.ai_ceo_app.system.project_path,
            multiline=False,
            size_hint_x=0.7
        )
        path_layout.add_widget(self.path_input)
        content.add_widget(path_layout)
        
        # Buttons for project management
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
        
        self.set_path_btn = Button(text='Set Path', size_hint_x=0.33)
        self.set_path_btn.bind(on_press=self.on_set_path)
        
        self.browse_btn = Button(text='Browse', size_hint_x=0.33)
        self.browse_btn.bind(on_press=self.on_browse)
        
        self.analyze_btn = Button(text='Analyze', size_hint_x=0.33)
        self.analyze_btn.bind(on_press=self.on_analyze)
        
        btn_layout.add_widget(self.set_path_btn)
        btn_layout.add_widget(self.browse_btn)
        btn_layout.add_widget(self.analyze_btn)
        content.add_widget(btn_layout)
        
        # Project status display
        status_layout = BoxLayout(orientation='vertical', spacing=dp(5), padding=[0, dp(10)])
        self.status_label = Label(
            text='Status: Loading...',
            size_hint_y=None,
            height=dp(30),
            halign='left'
        )
        self.components_label = Label(
            text='Components: Loading...',
            size_hint_y=None,
            height=dp(30),
            halign='left'
        )
        status_layout.add_widget(self.status_label)
        status_layout.add_widget(self.components_label)
        content.add_widget(status_layout)
        
        self.add_widget(content)
        
        # Update status periodically
        Clock.schedule_interval(self.update_status, 2)
        
    def on_set_path(self, instance):
        """Handle set path button press"""
        new_path = self.path_input.text.strip()
        if self.ai_ceo_app.system.set_project_path(new_path):
            self.ai_ceo_app.console.add_message(f"Project path set to: {new_path}", True)
            self.ai_ceo_app.system.save_config()
            self.update_status(None)
        else:
            self.ai_ceo_app.console.add_message(f"Error: Invalid project path: {new_path}", True)
            # Reset to current valid path
            self.path_input.text = self.ai_ceo_app.system.project_path
    
    def on_browse(self, instance):
        """Handle browse button press"""
        # We can't use the console browse directly, so we'll just open the file dialog
        self.ai_ceo_app.console.add_message("Opening file dialog...", True)
        if hasattr(self.ai_ceo_app.system, "_open_file_dialog"):
            try:
                self.ai_ceo_app.system._open_file_dialog()
                # Update the path input
                self.path_input.text = self.ai_ceo_app.system.project_path
                self.update_status(None)
            except Exception as e:
                self.ai_ceo_app.console.add_message(f"Error browsing: {str(e)}", True)
        else:
            self.ai_ceo_app.console.add_message("Browse functionality not available", True)
    
    def on_analyze(self, instance):
        """Handle analyze button press"""
        self.ai_ceo_app.console.add_message("Analyzing project...", True)
        missing = self.ai_ceo_app.system.analyze_project()
        if missing:
            self.ai_ceo_app.console.add_message(f"Missing components: {', '.join(missing)}", True)
            # Ask if user wants to generate missing components
            self.show_generate_dialog(missing)
        else:
            self.ai_ceo_app.console.add_message("All core components are present", True)
        self.update_status(None)
    
    def show_generate_dialog(self, missing):
        """Show dialog to generate missing components"""
        # For simplicity, just add a message and generate immediately in this version
        self.ai_ceo_app.console.add_message("Generating missing components...", True)
        self.ai_ceo_app.system.deploy_ai_engineers(missing)
        self.update_status(None)
    
    def update_status(self, dt):
        """Update the project status display"""
        if hasattr(self.ai_ceo_app, 'system'):
            # Update path field with current path
            self.path_input.text = self.ai_ceo_app.system.project_path
            
            # Update status labels
            if self.ai_ceo_app.system.running_thread and self.ai_ceo_app.system.running_thread.is_alive():
                status = "Running"
            else:
                status = "Stopped"
            
            self.status_label.text = f"Status: {status} | Debug: {'Enabled' if self.ai_ceo_app.system.debug_mode else 'Disabled'} | Engineers: {self.ai_ceo_app.system.ai_engineers}"
            
            # Check for missing components
            missing = self.ai_ceo_app.system.analyze_project()
            if missing:
                self.components_label.text = f"Missing Components: {', '.join(missing)}"
            else:
                self.components_label.text = "All core components are present"

class ClonePanel(TabbedPanelItem):
    """Panel for cloning and integrating repositories"""
    
    def __init__(self, ai_ceo_app, **kwargs):
        super(ClonePanel, self).__init__(**kwargs)
        self.text = 'Clone dApp'
        self.ai_ceo_app = ai_ceo_app
        
        # Create layout
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # Repository URL input
        repo_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        repo_layout.add_widget(Label(text='Repository URL:', size_hint_x=0.3))
        
        self.repo_input = TextInput(
            hint_text='https://github.com/username/repo.git',
            multiline=False,
            size_hint_x=0.7
        )
        repo_layout.add_widget(self.repo_input)
        content.add_widget(repo_layout)
        
        # Target directory input
        target_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        target_layout.add_widget(Label(text='Target Directory:', size_hint_x=0.3))
        
        self.target_input = TextInput(
            hint_text='Leave empty for default',
            multiline=False,
            size_hint_x=0.7
        )
        target_layout.add_widget(self.target_input)
        content.add_widget(target_layout)
        
        # Clone and Integrate buttons
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
        
        self.clone_btn = Button(text='Clone Repository', size_hint_x=0.5)
        self.clone_btn.bind(on_press=self.on_clone)
        
        self.integrate_btn = Button(text='Integrate AI CEO', size_hint_x=0.5)
        self.integrate_btn.bind(on_press=self.on_integrate)
        
        btn_layout.add_widget(self.clone_btn)
        btn_layout.add_widget(self.integrate_btn)
        content.add_widget(btn_layout)
        
        # Clone status
        self.status_label = Label(
            text='Ready to clone',
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(self.status_label)
        
        # Help text
        help_text = (
            "Use this panel to clone external repositories and integrate the AI CEO system into them.\n\n"
            "1. Enter the Git repository URL you want to clone\n"
            "2. Optionally specify a target directory\n"
            "3. Click 'Clone Repository' to clone the repository\n"
            "4. Click 'Integrate AI CEO' to add AI CEO functionality to the current project"
        )
        help_label = Label(
            text=help_text,
            size_hint_y=1,
            halign='left',
            valign='top',
            text_size=(Window.width - dp(40), None)
        )
        content.add_widget(help_label)
        
        self.add_widget(content)
    
    def on_clone(self, instance):
        """Handle clone button press"""
        repo_url = self.repo_input.text.strip()
        if not repo_url:
            self.status_label.text = "Error: Please enter a repository URL"
            self.ai_ceo_app.console.add_message("Error: No repository URL provided", True)
            return
        
        target_dir = self.target_input.text.strip()
        if not target_dir:
            target_dir = None
        
        self.status_label.text = f"Cloning repository: {repo_url}..."
        self.ai_ceo_app.console.add_message(f"Cloning repository: {repo_url}", True)
        
        # Clone in a separate thread to avoid blocking the UI
        threading.Thread(
            target=self._clone_thread,
            args=(repo_url, target_dir),
            daemon=True
        ).start()
    
    def _clone_thread(self, repo_url, target_dir):
        """Clone repository in a separate thread"""
        try:
            result = self.ai_ceo_app.system.clone_project(repo_url, target_dir)
            
            # Update UI from the main thread
            Clock.schedule_once(lambda dt: self._update_clone_status(result, repo_url), 0)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self._update_clone_status(False, str(e)), 0)
    
    def _update_clone_status(self, success, message):
        """Update clone status"""
        if success:
            self.status_label.text = f"Repository cloned successfully"
            self.ai_ceo_app.console.add_message("Clone operation completed successfully", True)
        else:
            self.status_label.text = f"Clone failed: {message}"
            self.ai_ceo_app.console.add_message(f"Clone operation failed: {message}", True)
    
    def on_integrate(self, instance):
        """Handle integrate button press"""
        self.status_label.text = "Integrating AI CEO..."
        self.ai_ceo_app.console.add_message("Integrating AI CEO into current project...", True)
        
        # Integrate in a separate thread
        threading.Thread(
            target=self._integrate_thread,
            daemon=True
        ).start()
    
    def _integrate_thread(self):
        """Integrate AI CEO in a separate thread"""
        try:
            missing_components = self.ai_ceo_app.system.analyze_project()
            result = self.ai_ceo_app.system.integrate_ai_ceo(
                self.ai_ceo_app.system.project_path, 
                missing_components
            )
            
            # Update UI from the main thread
            Clock.schedule_once(lambda dt: self._update_integrate_status(result), 0)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self._update_integrate_status(False, str(e)), 0)
    
    def _update_integrate_status(self, success, error=None):
        """Update integration status"""
        if success:
            self.status_label.text = "AI CEO integrated successfully"
            self.ai_ceo_app.console.add_message("Integration completed successfully", True)
        else:
            self.status_label.text = f"Integration failed: {error}"
            self.ai_ceo_app.console.add_message(f"Integration failed: {error}", True)

class SettingsPanel(TabbedPanelItem):
    """Panel for system settings"""
    
    def __init__(self, ai_ceo_app, **kwargs):
        super(SettingsPanel, self).__init__(**kwargs)
        self.text = 'Settings'
        self.ai_ceo_app = ai_ceo_app
        
        # Create layout
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # Debug mode toggle
        debug_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        debug_layout.add_widget(Label(text='Debug Mode:', size_hint_x=0.7))
        
        self.debug_btn = Button(
            text='Enabled' if self.ai_ceo_app.system.debug_mode else 'Disabled',
            size_hint_x=0.3
        )
        self.debug_btn.bind(on_press=self.toggle_debug)
        debug_layout.add_widget(self.debug_btn)
        content.add_widget(debug_layout)
        
        # Engineers count
        engineers_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        engineers_layout.add_widget(Label(text='AI Engineers:', size_hint_x=0.7))
        
        self.engineers_input = TextInput(
            text=str(self.ai_ceo_app.system.ai_engineers),
            multiline=False,
            input_filter='int',
            size_hint_x=0.3
        )
        engineers_layout.add_widget(self.engineers_input)
        content.add_widget(engineers_layout)
        
        # System control buttons
        control_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(10))
        
        self.start_btn = Button(text='Start AI CEO', size_hint_x=0.5)
        self.start_btn.bind(on_press=self.on_start)
        
        self.stop_btn = Button(text='Stop AI CEO', size_hint_x=0.5)
        self.stop_btn.bind(on_press=self.on_stop)
        
        control_layout.add_widget(self.start_btn)
        control_layout.add_widget(self.stop_btn)
        content.add_widget(control_layout)
        
        # Save settings button
        self.save_btn = Button(
            text='Save Settings',
            size_hint_y=None,
            height=dp(40)
        )
        self.save_btn.bind(on_press=self.on_save)
        content.add_widget(self.save_btn)
        
        # Add some spacing
        content.add_widget(Label(size_hint_y=0.1))
        
        # Help text
        help_text = (
            "AI CEO Management System Settings\n\n"
            "- Debug Mode: Enables detailed logging\n"
            "- AI Engineers: Number of virtual engineers to deploy (1-10)\n"
            "- Start/Stop: Control the AI CEO background monitoring\n"
            "- Save Settings: Save current configuration to disk"
        )
        help_label = Label(
            text=help_text,
            size_hint_y=0.9,
            halign='left',
            valign='top',
            text_size=(Window.width - dp(40), None)
        )
        content.add_widget(help_label)
        
        self.add_widget(content)
        
        # Update status periodically
        Clock.schedule_interval(self.update_status, 1)
    
    def toggle_debug(self, instance):
        """Toggle debug mode"""
        self.ai_ceo_app.system.debug_mode = not self.ai_ceo_app.system.debug_mode
        self.debug_btn.text = 'Enabled' if self.ai_ceo_app.system.debug_mode else 'Disabled'
        self.ai_ceo_app.console.add_message(
            f"Debug mode {'enabled' if self.ai_ceo_app.system.debug_mode else 'disabled'}",
            True
        )
    
    def on_start(self, instance):
        """Start AI CEO system"""
        if self.ai_ceo_app.system.running_thread and self.ai_ceo_app.system.running_thread.is_alive():
            self.ai_ceo_app.console.add_message("AI CEO is already running", True)
        else:
            self.ai_ceo_app.system.stop_requested = False
            self.ai_ceo_app.console.add_message("Starting AI CEO system...", True)
            self.ai_ceo_app.system.running_thread = threading.Thread(
                target=self.ai_ceo_app.system.run_ai_ceo
            )
            self.ai_ceo_app.system.running_thread.daemon = True
            self.ai_ceo_app.system.running_thread.start()
    
    def on_stop(self, instance):
        """Stop AI CEO system"""
        if not self.ai_ceo_app.system.running_thread or not self.ai_ceo_app.system.running_thread.is_alive():
            self.ai_ceo_app.console.add_message("AI CEO is not running", True)
        else:
            self.ai_ceo_app.console.add_message("Stopping AI CEO system...", True)
            self.ai_ceo_app.system.stop_requested = True
            # No need to join, as we're updating status dynamically
    
    def on_save(self, instance):
        """Save settings"""
        try:
            # Update engineers count
            try:
                engineers = int(self.engineers_input.text)
                self.ai_ceo_app.system.ai_engineers = max(1, min(10, engineers))
                self.engineers_input.text = str(self.ai_ceo_app.system.ai_engineers)
            except ValueError:
                self.ai_ceo_app.console.add_message("Error: Invalid engineer count. Using previous value.", True)
                self.engineers_input.text = str(self.ai_ceo_app.system.ai_engineers)
            
            # Save configuration
            self.ai_ceo_app.system.save_config()
            self.ai_ceo_app.console.add_message("Settings saved successfully", True)
        except Exception as e:
            self.ai_ceo_app.console.add_message(f"Error saving settings: {str(e)}", True)
    
    def update_status(self, dt):
        """Update UI with current system status"""
        if hasattr(self.ai_ceo_app, 'system'):
            is_running = (self.ai_ceo_app.system.running_thread and 
                         self.ai_ceo_app.system.running_thread.is_alive())
            self.start_btn.disabled = is_running
            self.stop_btn.disabled = not is_running
            
            # Ensure debug button matches current state
            self.debug_btn.text = 'Enabled' if self.ai_ceo_app.system.debug_mode else 'Disabled'
            
            # Ensure engineers input matches current state
            if self.engineers_input.text != str(self.ai_ceo_app.system.ai_engineers):
                self.engineers_input.text = str(self.ai_ceo_app.system.ai_engineers)

class AICEOApp(App):
    """Main Kivy application for the AI CEO Management System"""
    
    def __init__(self, **kwargs):
        super(AICEOApp, self).__init__(**kwargs)
        self.title = 'AI CEO Management System'
        
        # Initialize the system
        self.system = AICEOSystem()
        
        # Log capture
        self.log_capture_thread = None
        self.stop_log_capture = False
    
    def build(self):
        """Build the UI"""
        # Main layout
        main_layout = BoxLayout(orientation='vertical')
        
        # Header
        header = Label(
            text='AI CEO Management System',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(24)
        )
        main_layout.add_widget(header)
        
        # Tabbed layout for different functions
        self.tabs = TabbedPanel(do_default_tab=False, size_hint_y=0.7)
        
        # Add tabs
        self.project_panel = ProjectPanel(self)
        self.clone_panel = ClonePanel(self)
        self.settings_panel = SettingsPanel(self)
        
        self.tabs.add_widget(self.project_panel)
        self.tabs.add_widget(self.clone_panel)
        self.tabs.add_widget(self.settings_panel)
        
        # Set default tab
        self.tabs.default_tab = self.project_panel
        self.tabs.switch_to(self.project_panel)
        
        main_layout.add_widget(self.tabs)
        
        # Console output
        console_header = Label(
            text='Console Output',
            size_hint_y=None,
            height=dp(30),
            halign='left',
            font_size=dp(14)
        )
        main_layout.add_widget(console_header)
        
        self.console = ConsoleOutput(size_hint_y=0.3)
        main_layout.add_widget(self.console)
        
        # Add initial welcome message
        self.console.add_message("AI CEO Management System started", True)
        self.console.add_message(f"Project path: {self.system.project_path}", True)
        
        # Start the AI CEO system
        self.console.add_message("Starting AI CEO background monitoring...", True)
        self.system.stop_requested = False
        self.system.running_thread = threading.Thread(target=self.system.run_ai_ceo)
        self.system.running_thread.daemon = True
        self.system.running_thread.start()
        
        # Start log capture thread
        self.start_log_capture()
        
        return main_layout
    
    def start_log_capture(self):
        """Start capturing logs in a separate thread"""
        self.stop_log_capture = False
        self.log_capture_thread = threading.Thread(target=self.capture_logs)
        self.log_capture_thread.daemon = True
        self.log_capture_thread.start()
    
    def capture_logs(self):
        """Capture system logs"""
        # In a real implementation, this would tail a log file
        # or use a pipe to capture stdout/stderr
        # For our demonstration, we'll simulate log messages
        while not self.stop_log_capture:
            # This would be replaced with actual log reading
            time.sleep(0.1)
    
    def on_stop(self):
        """When the app is closed"""
        # Stop log capture
        self.stop_log_capture = True
        if self.log_capture_thread:
            self.log_capture_thread.join(timeout=1)
        
        # Stop AI CEO system
        if self.system.running_thread and self.system.running_thread.is_alive():
            self.system.stop()
        
        return super(AICEOApp, self).on_stop()

if __name__ == '__main__':
    AICEOApp().run()