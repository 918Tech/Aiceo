import os
import json
import time
import threading
import sys
import tkinter as tk
from tkinter import filedialog
import subprocess
import re
import shutil
from task_manager import task_manager

class AICEOSystem:
    """AI CEO Management System - Command Line Interface"""
    
    CONFIG_FILE = "ai_ceo_config.json"

    def __init__(self):
        """Initialize the AI CEO system"""
        self.project_path = os.getcwd()  # Default to current directory
        self.ai_engineers = 5
        self.debug_mode = True
        self.stop_requested = False
        self.task_queue = []
        self.ceo_logic = {}
        self.running_thread = None
        self.load_config()
        self.print_welcome()
        
    def print_welcome(self):
        """Print a welcome message for the AI CEO system"""
        print("\n" + "="*50)
        print("     AI CEO MANAGEMENT SYSTEM")
        print("     Command Line Interface")
        print("="*50)
        print(f"Project Path: {self.project_path}")
        print(f"Debug Mode: {'Enabled' if self.debug_mode else 'Disabled'}")
        print(f"AI Engineers: {self.ai_engineers}")
        print("="*50 + "\n")

    def load_config(self):
        """Loads AI CEO system configuration"""
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.task_queue = config.get("task_queue", [])
                    self.debug_mode = config.get("debug_mode", True)
                    self.ceo_logic = config.get("ceo_logic", {})
                    self.ai_engineers = config.get("ai_engineers", 5)
                    
                    # Load project path if it exists in the config
                    saved_path = config.get("project_path", "")
                    if saved_path and os.path.exists(saved_path):
                        self.project_path = saved_path
            else:
                self.save_config()
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")

    def save_config(self):
        """Saves updated configuration"""
        try:
            config_data = {
                "task_queue": self.task_queue,
                "debug_mode": self.debug_mode,
                "ceo_logic": self.ceo_logic,
                "ai_engineers": self.ai_engineers,
                "project_path": self.project_path  # Save the project path
            }
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config_data, f, indent=4)
            if self.debug_mode:
                print("[DEBUG] Configuration saved successfully.")
        except Exception as e:
            print(f"Error saving configuration: {str(e)}")

    def start(self):
        """Start the AI CEO system in a separate thread"""
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
        """Stop the AI CEO system"""
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
        """Runs the AI CEO system in a loop"""
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
                    # Notify when all components are present but DON'T break the loop
                    if iterations > 1:
                        print("[AI CEO] All required components are present. System ready.")
                        # Continue monitoring instead of exiting
                        print("[AI CEO] Continuing to monitor project...")
                
                # Add some delay between iterations (increased from 5 to 10 seconds)
                for _ in range(10):  # 10-second delay broken into smaller chunks for responsiveness
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

    def set_project_path(self, path):
        """Set a new project path"""
        # Normalize and validate path
        path = os.path.abspath(os.path.expanduser(path))
        
        if not os.path.exists(path):
            print(f"[ERROR] Path does not exist: {path}")
            return False
            
        old_path = self.project_path
        self.project_path = path
        print(f"[AI CEO] Project path changed: {old_path} -> {self.project_path}")
        return True
        
    def clone_project(self, repo_url, target_dir=None):
        """
        Clone a Git repository to a target directory and integrate AI CEO system.
        
        Args:
            repo_url (str): URL of the Git repository to clone
            target_dir (str): Optional target directory name, if not provided,
                              will use the repository name
                              
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # If no target directory provided, extract name from the repo URL
            if not target_dir:
                # Extract repository name from URL
                repo_name = repo_url.split('/')[-1]
                if repo_name.endswith('.git'):
                    repo_name = repo_name[:-4]  # Remove .git extension
                target_dir = os.path.join(os.getcwd(), repo_name)
            
            # Validate target directory
            if os.path.exists(target_dir):
                print(f"[WARNING] Target directory already exists: {target_dir}")
                confirm = input("Overwrite existing directory? (y/n): ").lower()
                if confirm != 'y':
                    print("[INFO] Clone operation cancelled.")
                    return False
                # Delete existing directory
                shutil.rmtree(target_dir)
            
            # Clone the repository
            print(f"[AI CEO] Cloning repository: {repo_url}")
            print(f"[AI CEO] Target directory: {target_dir}")
            
            # Execute git clone command
            result = subprocess.run(
                ['git', 'clone', repo_url, target_dir],
                capture_output=True,
                text=True,
                check=False
            )
            
            # Check for errors
            if result.returncode != 0:
                print(f"[ERROR] Git clone failed: {result.stderr}")
                return False
            
            print(f"[AI CEO] Repository cloned successfully to: {target_dir}")
            
            # Set the project path to the cloned repository
            self.set_project_path(target_dir)
            self.save_config()
            
            # Analyze the newly cloned repository
            print(f"[AI CEO] Analyzing cloned repository...")
            missing_components = self.analyze_project()
            
            # Ask if user wants to integrate AI CEO
            print("\n[AI CEO] Would you like to integrate AI CEO functionality into this project?")
            confirm = input("Deploy AI engineers to add AI CEO capabilities? (y/n): ").lower()
            
            if confirm == 'y':
                self.integrate_ai_ceo(target_dir, missing_components)
                return True
            else:
                print("[INFO] Integration skipped.")
                return True
                
        except Exception as e:
            print(f"[ERROR] Failed to clone repository: {str(e)}")
            if self.debug_mode:
                import traceback
                traceback.print_exc()
            return False
            
    def integrate_ai_ceo(self, target_dir, missing_components=None):
        """
        Integrate AI CEO functionality into a project
        
        Args:
            target_dir (str): Target directory containing the project
            missing_components (list): Optional list of missing components
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"[AI CEO] Integrating AI CEO system into: {target_dir}")
            
            # If missing_components is None, analyze the project
            if missing_components is None:
                missing_components = self.analyze_project()
            
            if missing_components:
                print(f"[AI CEO] Deploying AI engineers to generate: {', '.join(missing_components)}")
                self.deploy_ai_engineers(missing_components)
            
            # Create integration file that explains the AI CEO system
            integration_file = os.path.join(target_dir, "ai_ceo_integration.md")
            
            # Prepare the components list outside the f-string
            if missing_components:
                components_text = "- " + "\n- ".join(missing_components)
            else:
                components_text = "- None (All required components were already present)"
                
            with open(integration_file, 'w') as f:
                f.write(f"""# AI CEO Integration

This project has been integrated with the AI CEO Management System.

## Generated Components

The following components were added to your project:

{components_text}

## Next Steps

1. Run the AI CEO system to analyze and optimize your project
2. Use `python main.py` to start the AI CEO command-line interface
3. Use the 'status' command to see the current project state

Integration completed on: {time.strftime("%Y-%m-%d %H:%M:%S")}
""")
            
            print(f"[AI CEO] Integration completed successfully!")
            print(f"[AI CEO] Created integration documentation: {integration_file}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to integrate AI CEO: {str(e)}")
            if self.debug_mode:
                import traceback
                traceback.print_exc()
            return False
        
    def analyze_project(self):
        """Checks for missing logic or files"""
        # First check if the path exists
        if not os.path.exists(self.project_path):
            print(f"[ERROR] Project path doesn't exist: {self.project_path}")
            return []
            
        # Check for missing required files
        required_files = ['ai_ceo.py', 'ai_engineers.py']
        missing = []
        
        for file in required_files:
            file_path = os.path.join(self.project_path, file)
            if not os.path.exists(file_path):
                missing.append(file)
        
        if self.debug_mode:
            print(f"[DEBUG] Analyzing project at {self.project_path}")
            print(f"[DEBUG] Missing components: {missing}")
            
        return missing

    def deploy_ai_engineers(self, missing_logic):
        """Generates missing components dynamically"""
        # Determine if we should use background tasks
        use_background = len(missing_logic) > 1
        
        if use_background:
            print(f"[AI CEO] Deploying AI engineers for {len(missing_logic)} components in the background")
            task_id = task_manager.submit_task(
                "Deploy AI Engineers",
                self._background_deploy_engineers,
                missing_logic,
                self.project_path,
                self.ai_engineers
            )
            print(f"[AI CEO] Background deployment started (Task ID: {task_id[:8]})")
            print(f"[AI CEO] Use 'tasks info {task_id}' to check progress")
            return
            
        # Synchronous deployment for a single component
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
            
            # Write the file to the correct project path
            file_path = os.path.join(self.project_path, component)
            try:
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f"[AI CEO] Successfully generated {file_path}")
            except Exception as e:
                print(f"[ERROR] Failed to create {file_path}: {str(e)}")
        
        print(f"[AI CEO] AI Engineers deployed for: {', '.join(missing_logic)}")
        
    def _background_deploy_engineers(self, missing_logic, project_path, num_engineers):
        """Background task to deploy AI engineers"""
        results = {}
        
        for component in missing_logic:
            print(f"[Background Task] Deploying AI engineers for: {component}")
            
            # Simulate work being done
            engineer_count = min(num_engineers, 5)  # Cap at 5 for simulation
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
            
            # Write the file to the correct project path
            file_path = os.path.join(project_path, component)
            try:
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f"[AI CEO] Successfully generated {file_path}")
                results[component] = "success"
            except Exception as e:
                error_msg = f"Failed to create {file_path}: {str(e)}"
                print(f"[ERROR] {error_msg}")
                results[component] = f"error: {error_msg}"
        
        print(f"[AI CEO] Background deployment completed for: {', '.join(missing_logic)}")
        return results

    def generate_ai_ceo_content(self):
        """Generate content for the AI CEO module"""
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
'''

    def generate_ai_engineers_content(self):
        """Generate content for the AI Engineers module"""
        return '''# AI Engineers Implementation
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
'''

    def command_loop(self):
        """Interactive command loop for the AI CEO system"""
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
                    print("  project    - Set or view project path")
                    print("  browse     - Browse directories and select a project folder")
                    print("  dialog     - Open a file dialog to select a project folder")
                    print("  clone      - Clone a Git repository and integrate AI CEO")
                    print("  integrate  - Integrate AI CEO into current project")
                    print("  tasks      - Manage background tasks")
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
                
                elif command == 'project':
                    action = input("Enter 'set' to change project path or 'view' to see current path: ").strip().lower()
                    
                    if action == 'view':
                        print(f"Current project path: {self.project_path}")
                        
                    elif action == 'set':
                        new_path = input("Enter the full path to the project folder: ").strip()

    def _handle_tasks_command(self):
        """Handle task management commands"""
        print("\nTask Management")
        print("Commands: status, list, run, info <task_id>")
        
        action = input("Enter task command: ").strip().lower()
        
        if action == 'status':
            status = task_manager.get_status()
            print(f"\nTask Manager Status:")
            print(f"  Running: {status['running']}")
            print(f"  Active Workers: {status['active_workers']}/{status['max_workers']}")
            print(f"  Pending Tasks: {status['pending_tasks']}")
            print(f"  Total Tasks: {status['total_tasks']}")
            print("\nTask Status Counts:")
            for status_name, count in status['task_statuses'].items():
                print(f"  {status_name}: {count}")
                
        elif action == 'list':
            tasks = task_manager.get_all_tasks()
            if not tasks:
                print("No tasks found.")
                return
                
            print(f"\nTotal Tasks: {len(tasks)}")
            print(f"{'ID':<8} {'Name':<20} {'Status':<10} {'Runtime':<10}")
            print("-" * 50)
            
            for task in tasks:
                task_info = task.get_info()
                print(f"{task_info['id'][:8]:<8} {task_info['name'][:20]:<20} {task_info['status']:<10} {task_info['runtime']:.2f}s")
                
        elif action == 'info':
            task_id = input("Enter task ID: ").strip()
            task_info = task_manager.get_task_info(task_id)
            
            if not task_info:
                print(f"Task with ID {task_id} not found.")
                return
                
            print(f"\nTask Information:")
            print(f"  ID: {task_info['id']}")
            print(f"  Name: {task_info['name']}")
            print(f"  Status: {task_info['status']}")
            print(f"  Created: {task_info['created_at']}")
            print(f"  Started: {task_info['started_at'] or 'Not started'}")
            print(f"  Completed: {task_info['completed_at'] or 'Not completed'}")
            print(f"  Runtime: {task_info['runtime']:.2f} seconds")
            
            if task_info['error']:
                print(f"\nError: {task_info['error']}")
                
        elif action == 'run':
            task_name = input("Enter task name: ").strip()
            
            # Define some example tasks
            if task_name == 'scan_project':
                # Submit a background task to scan the project
                def scan_project_task(project_path):
                    print(f"[Task] Scanning project at {project_path}")
                    file_count = 0
                    for root, dirs, files in os.walk(project_path):
                        file_count += len(files)
                        time.sleep(0.01)  # Simulate work
                    return {"file_count": file_count}
                
                task_id = task_manager.submit_task(
                    "Project Scan", 
                    scan_project_task, 
                    self.project_path
                )
                print(f"Task submitted with ID: {task_id}")
                
            elif task_name == 'backup':
                # Submit a task to backup the project
                def backup_task(project_path):
                    print(f"[Task] Backing up project at {project_path}")
                    backup_dir = os.path.join(os.path.dirname(project_path), "backup_" + time.strftime("%Y%m%d_%H%M%S"))
                    os.makedirs(backup_dir, exist_ok=True)
                    
                    # Simple backup - just copy .py files
                    for root, dirs, files in os.walk(project_path):
                        for file in files:
                            if file.endswith('.py'):
                                src_path = os.path.join(root, file)
                                rel_path = os.path.relpath(src_path, project_path)
                                dst_path = os.path.join(backup_dir, rel_path)
                                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                                shutil.copy2(src_path, dst_path)
                                time.sleep(0.05)  # Simulate work
                                
                    return {"backup_dir": backup_dir}
                
                task_id = task_manager.submit_task(
                    "Project Backup", 
                    backup_task, 
                    self.project_path
                )
                print(f"Backup task submitted with ID: {task_id}")
                
            elif task_name == 'analyze':
                # Submit a task to analyze the project in the background
                def analyze_task(project_path):
                    print(f"[Task] Analyzing project at {project_path}")
                    # Perform a more detailed analysis than the regular analyze_project
                    components = []
                    for root, dirs, files in os.walk(project_path):
                        for file in files:
                            if file.endswith(('.py', '.json', '.txt', '.md')):
                                file_path = os.path.join(root, file)
                                rel_path = os.path.relpath(file_path, project_path)
                                
                                # Read file to count lines
                                try:
                                    with open(file_path, 'r') as f:
                                        lines = f.readlines()
                                        line_count = len(lines)
                                except:
                                    line_count = 0
                                
                                # Get file stats
                                try:
                                    stats = os.stat(file_path)
                                    file_size = stats.st_size
                                    modified = time.ctime(stats.st_mtime)
                                except:
                                    file_size = 0
                                    modified = "Unknown"
                                
                                components.append({
                                    "name": file,
                                    "path": rel_path,
                                    "size": file_size,
                                    "lines": line_count,
                                    "modified": modified
                                })
                                time.sleep(0.02)  # Simulate work
                                
                    return {
                        "components": components,
                        "total_files": len(components),
                        "total_lines": sum(c["lines"] for c in components)
                    }
                
                task_id = task_manager.submit_task(
                    "Deep Project Analysis", 
                    analyze_task, 
                    self.project_path
                )
                print(f"Analysis task submitted with ID: {task_id}")
                
            else:
                print(f"Unknown task: {task_name}")
                print("Available tasks: scan_project, backup, analyze")
        
        else:
            print(f"Unknown action: {action}")
            print("Use: status, list, run, info <task_id>")

                        if new_path:
                            if self.set_project_path(new_path):
                                print(f"Project path updated to: {self.project_path}")
                                self.save_config()
                        else:
                            print("No path provided. Project path not changed.")
                    else:
                        print(f"Unknown action: '{action}'. Use 'set' or 'view'.")
                
                elif command == 'browse':
                    self._browse_directories()
                
                elif command == 'dialog':
                    self._open_file_dialog()
                
                elif command == 'clone':
                    repo_url = input("Enter Git repository URL to clone: ").strip()
                    if not repo_url:
                        print("No repository URL provided. Operation cancelled.")
                    else:
                        # Optional target directory
                        target_dir = input("Enter target directory (leave empty for default): ").strip()
                        if not target_dir:
                            target_dir = None
                        
                        # Execute the clone operation
                        self.clone_project(repo_url, target_dir)
                
                elif command == 'integrate':
                    print(f"Current project path: {self.project_path}")
                    confirm = input("Do you want to integrate AI CEO into this project? (y/n): ").lower()
                    if confirm == 'y':
                        missing_components = self.analyze_project()
                        self.integrate_ai_ceo(self.project_path, missing_components)
                    else:
                        print("Integration cancelled.")
                
                elif command == 'tasks':
                    self._handle_tasks_command()
                    
                elif command == 'exit':
                    if self.running_thread and self.running_thread.is_alive():
                        print("Stopping AI CEO before exit...")
                        self.stop()
                    # Also stop the task manager
                    task_manager.stop()
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
    
    def _browse_directories(self):
        """Interactive directory browser to select a project folder"""
        current_dir = os.getcwd()
        
        while True:
            print(f"\nCurrent directory: {current_dir}")
            print("\nContents:")
            
            try:
                # Get directories and files
                items = os.listdir(current_dir)
                dirs = [d for d in items if os.path.isdir(os.path.join(current_dir, d))]
                files = [f for f in items if os.path.isfile(os.path.join(current_dir, f))]
                
                # Display directories
                print("\nDirectories:")
                for i, d in enumerate(dirs):
                    print(f"  {i+1}. {d}/")
                
                # Display files (only Python, JSON, and text files)
                py_files = [f for f in files if f.endswith(('.py', '.json', '.txt'))]
                if py_files:
                    print("\nRelevant Files:")
                    for i, f in enumerate(py_files):
                        print(f"  {len(dirs)+i+1}. {f}")
                
                # Show options
                print("\nOptions:")
                print("  0. Select current directory as project")
                print("  p. Go to parent directory")
                print("  d. Use file dialog for selection")
                print("  c. Cancel browsing")
                
                # Get user choice
                choice = input("\nEnter your choice: ").strip()
                
                if choice == '0':
                    # Select current directory
                    if self.set_project_path(current_dir):
                        print(f"Project path set to: {current_dir}")
                        self.save_config()
                    return
                
                elif choice == 'p':
                    # Go to parent directory
                    parent = os.path.dirname(current_dir)
                    if parent != current_dir:  # Avoid getting stuck at root
                        current_dir = parent
                    else:
                        print("Already at root directory.")
                
                elif choice == 'd':
                    # Switch to file dialog
                    self._open_file_dialog()
                    return
                
                elif choice == 'c':
                    # Cancel browsing
                    print("Directory browsing cancelled.")
                    return
                
                elif choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(dirs):
                        # Navigate to subdirectory
                        current_dir = os.path.join(current_dir, dirs[idx])
                    elif len(dirs) <= idx < len(dirs) + len(py_files):
                        # Selected a file - treat its directory as the project
                        file_dir = os.path.dirname(os.path.join(current_dir, py_files[idx - len(dirs)]))
                        if self.set_project_path(file_dir):
                            print(f"Project path set to: {file_dir}")
                            self.save_config()
                        return
                    else:
                        print("Invalid selection.")
                
                else:
                    print("Invalid choice.")
            
            except Exception as e:
                print(f"Error browsing directory: {str(e)}")
                if self.debug_mode:
                    import traceback
                    traceback.print_exc()
                return
                
    def _open_file_dialog(self):
        """Open a graphical file dialog to select a project folder"""
        try:
            print("Opening file dialog window...")
            
            # Hide the main tkinter window
            root = tk.Tk()
            root.withdraw()
            
            # Request a directory from the user
            directory = filedialog.askdirectory(
                title="Select Project Directory",
                initialdir=self.project_path,
                mustexist=True
            )
            
            # Process the selected directory
            if directory:
                if self.set_project_path(directory):
                    print(f"Project path set to: {directory}")
                    self.save_config()
            else:
                print("No directory selected. Project path not changed.")
                
            # Clean up the tkinter instance
            root.destroy()
            
        except Exception as e:
            print(f"Error opening file dialog: {str(e)}")
            print("Note: GUI dialogs may not work in all environments.")
            print("Try using the 'browse' or 'project' commands instead.")
            if self.debug_mode:
                import traceback
                traceback.print_exc()

if __name__ == '__main__':
    ai_ceo_system = AICEOSystem()
    ai_ceo_system.start()