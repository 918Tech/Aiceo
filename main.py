import os
import json
import time
import threading
import sys

class AICEOSystem:
    CONFIG_FILE = "ai_ceo_config.json"

    def __init__(self):
        self.project_path = os.getcwd()
        self.ai_engineers = 5
        self.debug_mode = True
        self.stop_requested = False
        self.load_config()
        self.print_welcome()
        self.running_thread = None
        
    def print_welcome(self):
        """Print a welcome message for the AI CEO system."""
        print("\n" + "="*50)
        print("     AI CEO MANAGEMENT SYSTEM")
        print("     Command Line Interface")
        print("="*50)
        print(f"Project Path: {self.project_path}")
        print(f"Debug Mode: {'Enabled' if self.debug_mode else 'Disabled'}")
        print(f"AI Engineers: {self.ai_engineers}")
        print("="*50 + "\n")

    def load_config(self):
        """Loads AI CEO system configuration."""
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.task_queue = config.get("task_queue", [])
                    self.debug_mode = config.get("debug_mode", True)
                    self.ceo_logic = config.get("ceo_logic", {})
                    self.ai_engineers = config.get("ai_engineers", 5)
            else:
                self.task_queue = []
                self.debug_mode = True
                self.ceo_logic = {}
                self.save_config()
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
            self.task_queue = []
            self.debug_mode = True
            self.ceo_logic = {}

    def save_config(self):
        """Saves updated configuration."""
        try:
            config_data = {
                "task_queue": self.task_queue,
                "debug_mode": self.debug_mode,
                "ceo_logic": self.ceo_logic,
                "ai_engineers": self.ai_engineers
            }
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config_data, f, indent=4)
            if self.debug_mode:
                print("[DEBUG] Configuration saved successfully.")
        except Exception as e:
            print(f"Error saving configuration: {str(e)}")

    def start(self):
        """Start the AI CEO system in a separate thread."""
        if self.running_thread and self.running_thread.is_alive():
            print("AI CEO is already running.")
            return
        
        self.stop_requested = False
        print("[AI CEO] System starting...")
        self.running_thread = threading.Thread(target=self.run_ai_ceo)
        self.running_thread.daemon = True
        self.running_thread.start()
        
        # Start interactive command loop
        self.command_loop()

    def stop(self):
        """Stop the AI CEO system."""
        if not self.running_thread or not self.running_thread.is_alive():
            print("AI CEO is not running.")
            return
        
        print("[AI CEO] Stopping system...")
        self.stop_requested = True
        self.running_thread.join(timeout=5)
        if self.running_thread.is_alive():
            print("[WARNING] AI CEO thread did not terminate gracefully.")
        else:
            print("[AI CEO] System stopped successfully.")

    def run_ai_ceo(self):
        """Runs the AI CEO system in a loop."""
        iterations = 0
        while not self.stop_requested:
            iterations += 1
            try:
                print(f"\n[AI CEO] Starting analysis iteration {iterations}...")
                missing_logic = self.analyze_project()
                
                if missing_logic:
                    component_list = ", ".join(missing_logic)
                    print(f"[AI CEO] Missing components detected: {component_list}")
                    self.deploy_ai_engineers(missing_logic)
                else:
                    print("[AI CEO] No missing logic. System is stable.")
                    # Check if we should continue running or exit after all components are present
                    if iterations > 1:
                        print("[AI CEO] All required components are now present. System ready.")
                        break
                
                # Add some delay between iterations
                for _ in range(5):  # 5-second delay broken into smaller chunks for responsiveness
                    if self.stop_requested:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                print(f"[ERROR] AI CEO encountered an error: {str(e)}")
                if self.debug_mode:
                    import traceback
                    traceback.print_exc()
                # Short delay before retrying after error
                time.sleep(3)
                
        print("[AI CEO] System thread terminated.")

    def analyze_project(self):
        """Checks for missing logic or files."""
        required_files = ['ai_ceo.py', 'ai_engineers.py']
        missing = [f for f in required_files if not os.path.exists(f)]
        
        if self.debug_mode:
            print(f"[DEBUG] Analyzing project at {self.project_path}")
            print(f"[DEBUG] Missing components: {missing}")
            
        return missing

    def deploy_ai_engineers(self, missing_logic):
        """Generates missing components dynamically."""
        for component in missing_logic:
            print(f"[AI CEO] Deploying AI engineers for: {component}")
            
            # Simulate work being done
            engineer_count = min(self.ai_engineers, 5)  # Cap at 5 for simulation
            for i in range(engineer_count):
                print(f"[Engineer {i+1}] Working on {component}...")
                time.sleep(0.5)  # Simulate work time
            
            # Generate appropriate content based on the component
            content = ""
            if component == "ai_ceo.py":
                content = self.generate_ai_ceo_content()
            elif component == "ai_engineers.py":
                content = self.generate_ai_engineers_content()
            else:
                content = f"# AI-generated logic for {component}\n# Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # Write the file
            try:
                with open(component, 'w') as f:
                    f.write(content)
                print(f"[AI CEO] Successfully generated {component}")
            except Exception as e:
                print(f"[ERROR] Failed to create {component}: {str(e)}")
        
        print(f"[AI CEO] AI Engineers deployed for: {', '.join(missing_logic)}")

    def generate_ai_ceo_content(self):
        """Generate content for the AI CEO module."""
        return '''# AI CEO Implementation
# Generated by AI CEO Management Suite

import os
import json
import time
import random
from datetime import datetime

class AICEO:
    """
    AI CEO class that manages the strategic direction of the project
    by analyzing the codebase and making development decisions.
    """
    
    def __init__(self, project_path):
        self.project_path = project_path
        self.config = {}
        self.components = []
        self.decisions = []
        self.last_analysis = None
        self.load_config()
'''
        
    def load_config(self):
        """Load configuration from the project directory."""
        config_path = os.path.join(self.project_path, "ceo_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    self.config = json.load(f)
                    self.components = self.config.get("components", [])
                    self.decisions = self.config.get("decisions", [])
                    self.last_analysis = self.config.get("last_analysis")
            except Exception as e:
                print(f"Error loading config: {str(e)}")
                self._initialize_default_config()
        else:
            self._initialize_default_config()
    
    def _initialize_default_config(self):
        """Set up default configuration when no existing config is found."""
        self.config = {
            "project_name": os.path.basename(self.project_path),
            "creation_date": time.strftime("%Y-%m-%d"),
            "last_analysis": None,
            "components": [],
            "decisions": [],
            "version": "1.0.0"
        }
        self.save_config()
    
    def save_config(self):
        """Save current configuration to the project directory."""
        config_path = os.path.join(self.project_path, "ceo_config.json")
        try:
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {str(e)}")
    
    def analyze_project(self):
        """
        Analyze the project structure and identify requirements.
        Returns a list of components found in the project.
        """
        self.last_analysis = time.strftime("%Y-%m-%d %H:%M:%S")
        self.config["last_analysis"] = self.last_analysis
        
        # Scan directories
        components = []
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(('.py', '.json', '.txt')):
                    file_path = os.path.join(root, file)
                    # Skip the config file itself
                    if file == "ceo_config.json":
                        continue
                        
                    # Get file metadata
                    rel_path = os.path.relpath(file_path, self.project_path)
                    try:
                        stats = os.stat(file_path)
                        file_size = stats.st_size
                        last_modified = time.ctime(stats.st_mtime)
                    except:
                        file_size = 0
                        last_modified = "Unknown"
                    
                    # Determine component type
                    component_type = "Unknown"
                    if file.endswith('.py'):
                        component_type = "Python module"
                    elif file.endswith('.json'):
                        component_type = "JSON data"
                    elif file.endswith('.txt'):
                        component_type = "Text data"
                    
                    # Add to components list
                    components.append({
                        "name": file,
                        "path": rel_path,
                        "type": component_type,
                        "size": file_size,
                        "last_modified": last_modified
                    })
        
        self.components = components
        self.config["components"] = components
        self.save_config()
        return components
    
    def make_decision(self):
        """
        Make strategic decisions about project development.
        Returns a list of decisions for the project.
        """
        decisions = []
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Check for missing core components
        core_components = ["ai_engineers.py", "ai_ceo.py"]
        for component in core_components:
            if not any(c["name"] == component for c in self.components):
                decisions.append({
                    "action": "create",
                    "component": component,
                    "priority": "high",
                    "reason": "Core component missing",
                    "timestamp": timestamp
                })
        
        # Store decisions
        self.decisions = decisions
        self.config["decisions"] = decisions
        self.save_config()
        return decisions
    
    def execute_decision(self, decision):
        """
        Execute a specific decision made by the AI CEO.
        Returns the status of the execution.
        """
        action = decision.get("action")
        component = decision.get("component")
        
        if action == "create":
            # Create component would be handled by AI engineers
            return {
                "status": "pending",
                "message": f"Requested creation of {component}",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        return {
            "status": "error",
            "message": f"Unknown action: {action}",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_project_status(self):
        """
        Get a summary of the current project status.
        Returns a dictionary with project stats.
        """
        total_components = len(self.components)
        py_components = len([c for c in self.components if c["type"] == "Python module"])
        json_components = len([c for c in self.components if c["type"] == "JSON data"])
        other_components = total_components - py_components - json_components
        
        pending_decisions = len([d for d in self.decisions if d.get("status", "") != "completed"])
        
        return {
            "project_name": self.config.get("project_name", "Unknown"),
            "total_components": total_components,
            "python_modules": py_components,
            "json_files": json_components,
            "other_files": other_components,
            "pending_decisions": pending_decisions,
            "last_analysis": self.last_analysis,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
"""

    def generate_ai_engineers_content(self):
        """Generate content for the AI Engineers module."""
        return """# AI Engineers Implementation
# Generated by AI CEO Management Suite

import os
import time
import random
import json
from datetime import datetime

class AIEngineer:
    """
    Represents a virtual AI Engineer that can generate code
    based on specifications and complete assigned tasks.
    """
    
    def __init__(self, name, specialization, efficiency=0.8):
        self.name = name
        self.specialization = specialization
        self.efficiency = efficiency  # 0.0 to 1.0 scale
        self.tasks_completed = 0
        self.code_generated = 0
        self.active = True
        self.started_at = datetime.now()
    
    def work_on_task(self, task):
        """
        Simulate working on a development task.
        Returns the result of the task.
        """
        # Log task start
        print(f"Engineer {self.name} working on: {task}")
        
        # Simulate work with a small delay based on efficiency
        delay = 1.0 - (self.efficiency * 0.5)  # 0.5 to 1.0 seconds
        time.sleep(delay)
        
        # Calculate success probability based on efficiency
        success = random.random() < self.efficiency
        
        self.tasks_completed += 1
        status = "completed" if success else "needs_review"
        
        return {
            "task": task,
            "status": status,
            "engineer": self.name,
            "specialization": self.specialization,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def generate_code(self, specification):
        """
        Generate code based on a specification.
        Returns the generated code as a string.
        """
        # Track code generation
        self.code_generated += 1
        
        # Generate the appropriate code based on specialization
        if self.specialization == "Frontend":
            code = self._generate_frontend_code(specification)
        elif self.specialization == "Backend":
            code = self._generate_backend_code(specification)
        elif self.specialization == "Database":
            code = self._generate_database_code(specification)
        elif self.specialization == "Testing":
            code = self._generate_testing_code(specification)
        elif self.specialization == "DevOps":
            code = self._generate_devops_code(specification)
        else:
            code = self._generate_generic_code(specification)
            
        return code
    
    def _generate_frontend_code(self, specification):
        """Generate frontend-related code."""
        component_name = specification.get('name', 'UIComponent')
        return f"# Frontend component: {component_name}\\n# Generated by AI Engineer: {self.name}\\n"
    
    def _generate_backend_code(self, specification):
        """Generate backend-related code."""
        component_name = specification.get('name', 'Service')
        return f"# Backend component: {component_name}\\n# Generated by AI Engineer: {self.name}\\n"
    
    def _generate_database_code(self, specification):
        """Generate database-related code."""
        component_name = specification.get('name', 'Database')
        return f"# Database component: {component_name}\\n# Generated by AI Engineer: {self.name}\\n"
    
    def _generate_testing_code(self, specification):
        """Generate testing-related code."""
        component_name = specification.get('name', 'TestSuite')
        return f"# Testing component: {component_name}\\n# Generated by AI Engineer: {self.name}\\n"
    
    def _generate_devops_code(self, specification):
        """Generate DevOps-related code."""
        component_name = specification.get('name', 'Pipeline')
        return f"# DevOps component: {component_name}\\n# Generated by AI Engineer: {self.name}\\n"
    
    def _generate_generic_code(self, specification):
        """Generate generic utility code."""
        component_name = specification.get('name', 'Utility')
        return f"# Utility component: {component_name}\\n# Generated by AI Engineer: {self.name}\\n"
    
    def get_stats(self):
        """
        Get statistics about this AI Engineer.
        Returns a dictionary with engineer statistics.
        """
        time_active = datetime.now() - self.started_at
        hours_active = time_active.total_seconds() / 3600
        
        return {
            "name": self.name,
            "specialization": self.specialization,
            "efficiency": self.efficiency,
            "tasks_completed": self.tasks_completed,
            "code_generated": self.code_generated,
            "active": self.active,
            "hours_active": round(hours_active, 2),
            "productivity": round(self.tasks_completed / max(1, hours_active), 2)
        }

class EngineeringTeam:
    """
    Represents a team of AI Engineers that can work on tasks
    and generate code components for a project.
    """
    
    def __init__(self, team_size=5):
        self.team = self._create_team(team_size)
        self.log = []
        self.created_at = datetime.now()
        self.log_event("Engineering team created")
    
    def _create_team(self, size):
        """
        Create a team of AI Engineers with different specializations.
        Returns a list of AIEngineer objects.
        """
        specializations = [
            "Frontend", "Backend", "Database", 
            "Testing", "DevOps", "Security", 
            "Mobile", "AI/ML", "Infrastructure"
        ]
        
        engineers = []
        for i in range(size):
            # Assign a specialization, looping through the list as needed
            spec = specializations[i % len(specializations)]
            
            # Random engineer name
            name = f"Engineer-{i+1:02d}"
            
            # Random efficiency between 0.7 and 0.95
            efficiency = 0.7 + (random.random() * 0.25)
            
            engineers.append(AIEngineer(name, spec, efficiency))
            
        return engineers
    
    def log_event(self, message, event_type="info"):
        """
        Log a team event.
        Adds an event to the team log and prints to console.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "type": event_type,
            "message": message
        }
        self.log.append(log_entry)
        print(f"[{timestamp}] [{event_type.upper()}] {message}")
    
    def assign_tasks(self, tasks):
        """
        Assign tasks to engineers based on their specialization.
        Returns a list of completed task results.
        
        Each task should be a dictionary with:
        - description: description of the task
        - requires: list of specializations needed
        - priority: optional priority level (high, medium, low)
        """
        results = []
        for task in tasks:
            description = task.get("description", "Unknown task")
            required_specs = task.get("requires", [])
            
            # Find suitable engineers
            suitable_engineers = []
            for engineer in self.team:
                if not required_specs or engineer.specialization in required_specs:
                    suitable_engineers.append(engineer)
            
            if suitable_engineers:
                # Assign to the most efficient suitable engineer
                chosen_engineer = max(suitable_engineers, key=lambda e: e.efficiency)
                self.log_event(f"Assigning '{description}' to {chosen_engineer.name} ({chosen_engineer.specialization})")
                
                # Engineer works on the task
                result = chosen_engineer.work_on_task(description)
                results.append(result)
                
                self.log_event(f"Task '{description}' {result['status']}", 
                              "success" if result["status"] == "completed" else "warning")
            else:
                self.log_event(f"No suitable engineer found for task: {description}", "error")
                results.append({
                    "task": description,
                    "status": "unassigned",
                    "reason": "No suitable engineer",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
        
        return results
    
    def generate_project_component(self, component_spec):
        """
        Generate a project component based on specifications.
        Returns the generated code.
        
        Component spec should be a dictionary with:
        - name: component name
        - type: component type (Frontend, Backend, etc.)
        - description: optional description
        """
        component_name = component_spec.get("name", "Component")
        component_type = component_spec.get("type", "Generic")
        description = component_spec.get("description", f"A {component_type} component")
        
        self.log_event(f"Generating {component_type} component: {component_name}")
        
        # Find engineer with matching specialization or the most efficient one
        suitable_engineers = [e for e in self.team if e.specialization == component_type]
        if not suitable_engineers:
            self.log_event(f"No {component_type} specialist available, using best available engineer", "warning")
            chosen_engineer = max(self.team, key=lambda e: e.efficiency)
        else:
            chosen_engineer = max(suitable_engineers, key=lambda e: e.efficiency)
        
        # Generate the code
        code = chosen_engineer.generate_code({
            "name": component_name,
            "description": description
        })
        
        self.log_event(f"Component {component_name} generated by {chosen_engineer.name}")
        return code
    
    def get_team_status(self):
        """
        Get current status of the engineering team.
        Returns a dictionary with team statistics.
        """
        team_age = datetime.now() - self.created_at
        days_active = team_age.total_seconds() / (60 * 60 * 24)
        
        total_tasks = sum(e.tasks_completed for e in self.team)
        total_code = sum(e.code_generated for e in self.team)
        
        engineer_stats = [e.get_stats() for e in self.team]
        
        return {
            "team_size": len(self.team),
            "days_active": round(days_active, 1),
            "total_tasks_completed": total_tasks,
            "total_code_generated": total_code,
            "productivity": round(total_tasks / max(1, days_active), 2),
            "engineers": engineer_stats,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
"""

    def command_loop(self):
        """Interactive command loop for the AI CEO system."""
        print("\nAI CEO Management System - Command Line Interface")
        print("Type 'help' for a list of commands")
        
        while not self.stop_requested:
            try:
                command = input("\nEnter command (or 'help'): ").strip().lower()
                
                if command == 'help':
                    print("\nAvailable commands:")
                    print("  start      - Start AI CEO system")
                    print("  stop       - Stop AI CEO system")
                    print("  status     - Check system status")
                    print("  debug      - Toggle debug mode")
                    print("  engineers  - Set number of AI engineers")
                    print("  analyze    - Run a single analysis cycle")
                    print("  exit       - Exit the application")
                
                elif command == 'start':
                    if self.running_thread and self.running_thread.is_alive():
                        print("AI CEO is already running.")
                    else:
                        print("Starting AI CEO system...")
                        self.stop_requested = False
                        self.running_thread = threading.Thread(target=self.run_ai_ceo)
                        self.running_thread.daemon = True
                        self.running_thread.start()
                
                elif command == 'stop':
                    self.stop()
                    
                elif command == 'status':
                    if self.running_thread and self.running_thread.is_alive():
                        print("AI CEO is running")
                    else:
                        print("AI CEO is stopped")
                    print(f"Project path: {self.project_path}")
                    print(f"Debug mode: {'Enabled' if self.debug_mode else 'Disabled'}")
                    print(f"AI Engineers: {self.ai_engineers}")
                    missing = self.analyze_project()
                    if missing:
                        print(f"Missing components: {', '.join(missing)}")
                    else:
                        print("All core components are present")
                
                elif command == 'debug':
                    self.debug_mode = not self.debug_mode
                    print(f"Debug mode {'enabled' if self.debug_mode else 'disabled'}")
                    self.save_config()
                
                elif command == 'engineers':
                    try:
                        num = int(input("Enter number of AI engineers (1-10): "))
                        self.ai_engineers = max(1, min(10, num))  # Clamp between 1 and 10
                        print(f"Number of AI engineers set to {self.ai_engineers}")
                        self.save_config()
                    except ValueError:
                        print("Please enter a valid number")
                
                elif command == 'analyze':
                    print("Running analysis cycle...")
                    missing_logic = self.analyze_project()
                    if missing_logic:
                        print(f"Missing components: {', '.join(missing_logic)}")
                        confirm = input("Generate these components? (y/n): ").lower()
                        if confirm == 'y':
                            self.deploy_ai_engineers(missing_logic)
                    else:
                        print("All core components are present")
                
                elif command == 'exit':
                    if self.running_thread and self.running_thread.is_alive():
                        print("Stopping AI CEO before exit...")
                        self.stop()
                    print("Exiting AI CEO Management System")
                    break
                
                else:
                    print(f"Unknown command: '{command}'. Type 'help' for a list of commands.")
            
            except KeyboardInterrupt:
                print("\nOperation interrupted. Type 'exit' to quit.")
            except Exception as e:
                print(f"Error executing command: {str(e)}")
                if self.debug_mode:
                    import traceback
                    traceback.print_exc()

if __name__ == '__main__':
    ai_ceo_system = AICEOSystem()
    ai_ceo_system.start()