import os
import json
import threading
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.switch import Switch
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ListProperty
from kivy.uix.popup import Popup

class LogDisplay(ScrollView):
    """Scrollable log display for AI CEO system activity."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)
        
    def add_log(self, message):
        """Add a new log entry to the display."""
        log_label = Label(
            text=f"[{time.strftime('%H:%M:%S')}] {message}",
            size_hint_y=None,
            height=30,
            text_size=(self.width, None),
            halign='left'
        )
        self.layout.add_widget(log_label)
        # Scroll to the bottom to show the newest log
        self.scroll_y = 0

class SettingsPopup(Popup):
    """Settings popup for AI CEO system configuration."""
    
    def __init__(self, ai_ceo_system, **kwargs):
        super().__init__(**kwargs)
        self.ai_ceo_system = ai_ceo_system
        self.title = "AI CEO Settings"
        self.size_hint = (0.8, 0.8)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Debug mode toggle
        debug_layout = BoxLayout(size_hint_y=None, height=40)
        debug_layout.add_widget(Label(text="Debug Mode:"))
        self.debug_switch = Switch(active=ai_ceo_system.debug_mode)
        debug_layout.add_widget(self.debug_switch)
        layout.add_widget(debug_layout)
        
        # Number of AI engineers
        engineers_layout = BoxLayout(size_hint_y=None, height=40)
        engineers_layout.add_widget(Label(text="AI Engineers:"))
        self.engineers_input = TextInput(
            text=str(ai_ceo_system.ai_engineers),
            input_filter='int',
            multiline=False,
            size_hint_x=0.7
        )
        engineers_layout.add_widget(self.engineers_input)
        layout.add_widget(engineers_layout)
        
        # Analysis depth
        depth_layout = BoxLayout(size_hint_y=None, height=40)
        depth_layout.add_widget(Label(text="Analysis Depth:"))
        self.depth_spinner = Spinner(
            text=ai_ceo_system.analysis_depth,
            values=('Basic', 'Standard', 'Deep'),
            size_hint_x=0.7
        )
        depth_layout.add_widget(self.depth_spinner)
        layout.add_widget(depth_layout)
        
        # Save button
        save_button = Button(text="Save Settings", size_hint_y=None, height=50)
        save_button.bind(on_press=self.save_settings)
        layout.add_widget(save_button)
        
        self.content = layout
    
    def save_settings(self, instance):
        """Save the updated settings to the main system."""
        self.ai_ceo_system.debug_mode = self.debug_switch.active
        try:
            self.ai_ceo_system.ai_engineers = int(self.engineers_input.text)
        except ValueError:
            self.ai_ceo_system.ai_engineers = 5  # Default if invalid input
        self.ai_ceo_system.analysis_depth = self.depth_spinner.text
        self.ai_ceo_system.save_config()
        self.ai_ceo_system.log_display.add_log(f"Settings updated")
        self.dismiss()

class AICEOSystem(BoxLayout):
    """Main AI CEO management system application."""
    
    CONFIG_FILE = "ai_ceo_config.json"
    
    # Properties for binding in Kivy
    status = StringProperty("Idle")
    is_running = BooleanProperty(False)
    ai_engineers = NumericProperty(5)
    debug_mode = BooleanProperty(True)
    analysis_depth = StringProperty("Standard")
    task_queue = ListProperty([])
    
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        Window.size = (800, 600)
        Window.minimum_width, Window.minimum_height = 600, 500
        
        # Initialize system variables
        self.project_path = None
        self.ceo_logic = {}
        self.active_thread = None
        
        # Load configuration
        self.load_config()
        
        # Initialize UI
        self.init_ui()
    
    def load_config(self):
        """Load AI CEO system configuration from JSON."""
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.project_path = config.get("last_project", "")
                    self.ai_engineers = config.get("ai_engineers", 5)
                    self.task_queue = config.get("task_queue", [])
                    self.debug_mode = config.get("debug_mode", True)
                    self.ceo_logic = config.get("ceo_logic", {})
                    self.analysis_depth = config.get("analysis_depth", "Standard")
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            # Use defaults if config can't be loaded

    def save_config(self):
        """Save updated AI CEO system configuration to JSON."""
        try:
            config_data = {
                "last_project": self.project_path,
                "ai_engineers": self.ai_engineers,
                "task_queue": self.task_queue,
                "debug_mode": self.debug_mode,
                "ceo_logic": self.ceo_logic,
                "analysis_depth": self.analysis_depth
            }
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config_data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {str(e)}")

    def init_ui(self):
        """Initialize the user interface for AI CEO System."""
        # Title
        title_label = Label(
            text='AI CEO Management Suite',
            font_size=24,
            size_hint_y=None,
            height=50
        )
        self.add_widget(title_label)
        
        # Input area
        input_layout = GridLayout(cols=2, spacing=5, size_hint_y=None, height=40)
        input_layout.add_widget(Label(text='Project Path:'))
        self.project_input = TextInput(
            text=self.project_path or "",
            multiline=False,
            size_hint_x=0.7
        )
        input_layout.add_widget(self.project_input)
        self.add_widget(input_layout)
        
        # Buttons row
        buttons_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        self.start_button = Button(
            text='Start AI CEO',
            background_color=(0.2, 0.7, 0.2, 1) 
        )
        self.start_button.bind(on_press=self.start_ai_ceo)
        buttons_layout.add_widget(self.start_button)
        
        self.stop_button = Button(
            text='Stop',
            background_color=(0.7, 0.2, 0.2, 1),
            disabled=True
        )
        self.stop_button.bind(on_press=self.stop_ai_ceo)
        buttons_layout.add_widget(self.stop_button)
        
        settings_button = Button(text='Settings')
        settings_button.bind(on_press=self.show_settings)
        buttons_layout.add_widget(settings_button)
        
        self.add_widget(buttons_layout)
        
        # Status bar
        status_layout = BoxLayout(size_hint_y=None, height=30)
        status_layout.add_widget(Label(text='Status:'))
        self.status_label = Label(text=self.status)
        self.bind(status=self.status_label.setter('text'))
        status_layout.add_widget(self.status_label)
        self.add_widget(status_layout)
        
        # Log display
        log_label = Label(
            text='Activity Log:',
            size_hint_y=None,
            height=30,
            halign='left'
        )
        self.add_widget(log_label)
        
        self.log_display = LogDisplay()
        self.add_widget(self.log_display)

    def show_settings(self, instance):
        """Display the settings popup."""
        settings_popup = SettingsPopup(self)
        settings_popup.open()

    def start_ai_ceo(self, instance):
        """Start AI CEO logic in a separate thread to avoid UI freezing."""
        if self.is_running:
            return
            
        self.project_path = self.project_input.text.strip()
        if not self.project_path:
            self.status = "Error: Project path is empty"
            self.log_display.add_log("Error: Please enter a project path")
            return
            
        if not os.path.exists(self.project_path):
            try:
                os.makedirs(self.project_path)
                self.log_display.add_log(f"Created project directory: {self.project_path}")
            except Exception as e:
                self.status = "Error: Unable to create project directory"
                self.log_display.add_log(f"Error creating directory: {str(e)}")
                return
                
        self.save_config()
        self.is_running = True
        self.status = "AI CEO Running..."
        self.start_button.disabled = True
        self.stop_button.disabled = False
        
        self.log_display.add_log(f"Starting AI CEO with {self.ai_engineers} engineers")
        self.log_display.add_log(f"Analysis depth: {self.analysis_depth}")
        
        # Start the AI logic in a separate thread
        self.active_thread = threading.Thread(target=self.run_ai_logic, daemon=True)
        self.active_thread.start()

    def stop_ai_ceo(self, instance):
        """Stop the running AI CEO thread."""
        if not self.is_running:
            return
            
        self.is_running = False
        self.status = "Stopping..."
        self.log_display.add_log("Stopping AI CEO operations")
        
        # The thread will check self.is_running and terminate
        Clock.schedule_once(self.update_ui_after_stop, 1)

    def update_ui_after_stop(self, dt):
        """Update UI components after stopping the AI CEO."""
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.status = "Idle"
        self.log_display.add_log("AI CEO stopped")

    def run_ai_logic(self):
        """
        Core AI CEO Logic:
        - Analyzes the project for missing logic.
        - Deploys AI Engineers to generate real, working code.
        - Follows a decision-making strategy for continuous project improvement.
        """
        try:
            iterations = 0
            while self.is_running:
                iterations += 1
                
                # Update UI from thread using Clock (thread-safe)
                Clock.schedule_once(lambda dt: setattr(self, 'status', "Analyzing project..."), 0)
                Clock.schedule_once(lambda dt: self.log_display.add_log(f"Running project analysis (iteration {iterations})"), 0)
                
                # Analyze project to find missing components
                missing_components = self.analyze_project()
                
                if not self.is_running:
                    break
                
                # If missing components found, deploy AI engineers
                if missing_components:
                    components_str = ", ".join(missing_components)
                    Clock.schedule_once(lambda dt, s=components_str: self.log_display.add_log(f"Missing components: {s}"), 0)
                    
                    for component in missing_components:
                        if not self.is_running:
                            break
                        Clock.schedule_once(lambda dt, c=component: self.log_display.add_log(f"Deploying AI engineers for: {c}"), 0)
                        Clock.schedule_once(lambda dt: setattr(self, 'status', f"Generating code..."), 0)
                        
                        # Simulate AI engineer working time based on analysis depth
                        work_time = {"Basic": 1, "Standard": 2, "Deep": 3}.get(self.analysis_depth, 2)
                        time.sleep(work_time)
                        
                        if self.is_running:
                            self.deploy_ai_engineers([component])
                            Clock.schedule_once(lambda dt, c=component: self.log_display.add_log(f"Generated: {c}"), 0)
                
                # No more missing components
                else:
                    Clock.schedule_once(lambda dt: self.log_display.add_log("All required components are present"), 0)
                    Clock.schedule_once(lambda dt: setattr(self, 'status', "Project is complete"), 0)
                    break
                
                # Prevent CPU overload
                time.sleep(1)
                
        except Exception as e:
            error_msg = f"Error in AI CEO thread: {str(e)}"
            print(error_msg)
            Clock.schedule_once(lambda dt, msg=error_msg: self.log_display.add_log(msg), 0)
            Clock.schedule_once(lambda dt, msg=error_msg: setattr(self, 'status', "Error"), 0)
        
        finally:
            # Always make sure UI is updated when thread ends
            if self.is_running:  # Only auto-update if not manually stopped
                Clock.schedule_once(self.update_ui_after_stop, 0)

    def analyze_project(self):
        """
        Analyzes the project directory to identify missing logic or files.
        Returns a list of missing components.
        """
        # Define required files for the AI CEO project
        required_files = ['ai_ceo.py', 'ai_engineers.py']
        
        # Check if files exist
        missing = [f for f in required_files if not os.path.exists(os.path.join(self.project_path, f))]
        
        # Add debug information if debug mode is enabled
        if self.debug_mode:
            print(f"Project path: {self.project_path}")
            print(f"Missing components: {missing}")
        
        return missing

    def deploy_ai_engineers(self, missing_components):
        """
        Deploys AI Engineers to generate missing components in real-time.
        
        Args:
            missing_components: List of file names to be generated
        """
        for component in missing_components:
            file_path = os.path.join(self.project_path, component)
            
            # Generate content based on the component type
            content = ""
            if component == "ai_ceo.py":
                content = self.generate_ai_ceo_content()
            elif component == "ai_engineers.py":
                content = self.generate_ai_engineers_content()
            else:
                content = f"# AI-generated component: {component}\n# Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n# This file would contain implementation for {component}"
            
            # Create the file with generated content
            try:
                with open(file_path, 'w') as f:
                    f.write(content)
                
                if self.debug_mode:
                    print(f"Created file: {file_path}")
            except Exception as e:
                print(f"Error creating file {file_path}: {str(e)}")

    def generate_ai_ceo_content(self):
        """Generate the content for ai_ceo.py."""
        return """# AI CEO Implementation
# Generated by AI CEO Management Suite

import os
import json
import time

class AICEO:
    def __init__(self, project_path):
        self.project_path = project_path
        self.config = {}
        self.load_config()
        
    def load_config(self):
        \"\"\"Load configuration from the project directory.\"\"\"
        config_path = os.path.join(self.project_path, "ceo_config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "project_name": os.path.basename(self.project_path),
                "creation_date": time.strftime("%Y-%m-%d"),
                "last_analysis": None,
                "components": []
            }
            self.save_config()
    
    def save_config(self):
        \"\"\"Save current configuration to the project directory.\"\"\"
        config_path = os.path.join(self.project_path, "ceo_config.json")
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def analyze_project(self):
        \"\"\"Analyze the project structure and identify requirements.\"\"\"
        self.config["last_analysis"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Scan directories
        components = []
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.endswith('.py'):
                    components.append({
                        "name": file,
                        "path": os.path.relpath(os.path.join(root, file), self.project_path),
                        "type": "Python module",
                        "last_modified": time.ctime(os.path.getmtime(os.path.join(root, file)))
                    })
        
        self.config["components"] = components
        self.save_config()
        return components
    
    def make_decision(self, component_status):
        \"\"\"Make strategic decisions about project development.\"\"\"
        decisions = []
        
        # Check for missing core components
        core_components = ["ai_engineers.py", "ai_ceo.py"]
        for component in core_components:
            if not any(c["name"] == component for c in component_status):
                decisions.append({
                    "action": "create",
                    "component": component,
                    "priority": "high",
                    "reason": "Core component missing"
                })
        
        # Add timestamp to decisions
        for decision in decisions:
            decision["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            
        return decisions

if __name__ == "__main__":
    # This allows the file to be run directly for testing
    ceo = AICEO("./test_project")
    components = ceo.analyze_project()
    decisions = ceo.make_decision(components)
    print(f"Project analysis complete. Found {len(components)} components.")
    print(f"Decisions: {len(decisions)}")
"""

    def generate_ai_engineers_content(self):
        """Generate the content for ai_engineers.py."""
        return """# AI Engineers Implementation
# Generated by AI CEO Management Suite

import os
import time
import random

class AIEngineer:
    def __init__(self, name, specialization):
        self.name = name
        self.specialization = specialization
        self.tasks_completed = 0
        self.active = True
    
    def work_on_task(self, task):
        \"\"\"Simulate working on a development task.\"\"\"
        print(f"Engineer {self.name} working on: {task}")
        # Simulate work with a small delay
        time.sleep(0.5)
        self.tasks_completed += 1
        return {
            "task": task,
            "status": "completed",
            "engineer": self.name,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def generate_code(self, specification):
        \"\"\"Generate code based on a specification.\"\"\"
        if self.specialization == "Frontend":
            return self._generate_frontend_code(specification)
        elif self.specialization == "Backend":
            return self._generate_backend_code(specification)
        else:
            return self._generate_generic_code(specification)
    
    def _generate_frontend_code(self, specification):
        \"\"\"Generate frontend-related code.\"\"\"
        return f'''
# Frontend component: {specification.get('name', 'UI Component')}
# Generated by AI Engineer: {self.name}
# Created on: {time.strftime("%Y-%m-%d %H:%M:%S")}

class UserInterface:
    def __init__(self):
        self.components = []
        self.initialize()
    
    def initialize(self):
        # Set up the user interface components
        print("Initializing user interface...")
        
    def add_component(self, component):
        self.components.append(component)
        
    def render(self):
        # Render the user interface
        print("Rendering user interface with", len(self.components), "components")

# Initialize the UI
ui = UserInterface()
'''
    
    def _generate_backend_code(self, specification):
        \"\"\"Generate backend-related code.\"\"\"
        return f'''
# Backend component: {specification.get('name', 'Service')}
# Generated by AI Engineer: {self.name}
# Created on: {time.strftime("%Y-%m-%d %H:%M:%S")}

class DataService:
    def __init__(self):
        self.data = {}
        self.initialize()
    
    def initialize(self):
        # Initialize the data service
        print("Initializing data service...")
        
    def store_data(self, key, value):
        self.data[key] = value
        
    def retrieve_data(self, key):
        return self.data.get(key)

# Initialize the service
service = DataService()
'''
    
    def _generate_generic_code(self, specification):
        \"\"\"Generate generic utility code.\"\"\"
        return f'''
# Utility component: {specification.get('name', 'Utility')}
# Generated by AI Engineer: {self.name}
# Created on: {time.strftime("%Y-%m-%d %H:%M:%S")}

class Utility:
    @staticmethod
    def process_data(data):
        # Process the input data
        return data
    
    @staticmethod
    def validate_input(input_value):
        # Validate the input
        return len(input_value) > 0

# Example usage
result = Utility.process_data("test data")
'''

class EngineeringTeam:
    def __init__(self, team_size=5):
        self.engineers = self._create_team(team_size)
    
    def _create_team(self, size):
        \"\"\"Create a team of AI Engineers with different specializations.\"\"\"
        specializations = ["Frontend", "Backend", "Database", "DevOps", "Testing"]
        names = ["Alex", "Bailey", "Casey", "Dana", "Ellis", "Finley", "Gale", "Harper"]
        
        team = []
        for i in range(size):
            spec = specializations[i % len(specializations)]
            name = f"{random.choice(names)}-{i+1}"
            team.append(AIEngineer(name, spec))
        
        return team
    
    def assign_tasks(self, tasks):
        \"\"\"Assign tasks to engineers based on their specialization.\"\"\"
        results = []
        for task in tasks:
            # Find an appropriate engineer
            for engineer in self.engineers:
                if engineer.active and (engineer.specialization in task.get("requires", ["any"])):
                    result = engineer.work_on_task(task["description"])
                    results.append(result)
                    break
            else:
                # If no specific engineer found, assign to first available
                if self.engineers:
                    result = self.engineers[0].work_on_task(task["description"])
                    results.append(result)
        
        return results
    
    def generate_project_component(self, component_spec):
        \"\"\"Generate a project component based on specifications.\"\"\"
        component_type = component_spec.get("type", "unknown")
        
        # Find engineer with matching specialization if possible
        for engineer in self.engineers:
            if engineer.active and engineer.specialization.lower() in component_type.lower():
                return engineer.generate_code(component_spec)
        
        # Otherwise use any available engineer
        if self.engineers:
            return self.engineers[0].generate_code(component_spec)
        
        return "# No engineers available to generate code"

if __name__ == "__main__":
    # This allows the file to be run directly for testing
    team = EngineeringTeam(3)
    print(f"Created engineering team with {len(team.engineers)} engineers")
    
    # Example task
    tasks = [
        {"description": "Create login form", "requires": ["Frontend"]},
        {"description": "Set up database connection", "requires": ["Backend", "Database"]}
    ]
    
    results = team.assign_tasks(tasks)
    print(f"Completed {len(results)} tasks")
    
    # Example component generation
    component = team.generate_project_component({"name": "UserService", "type": "Backend"})
    print("Generated component with", len(component.split('\\n')), "lines of code")
"""

class AICEOApp(App):
    def build(self):
        return AICEOSystem()

if __name__ == '__main__':
    AICEOApp().run()
