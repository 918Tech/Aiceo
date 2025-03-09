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
from continuous_improvement import ContinuousImprovement

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
        self.improvement_thread = None
        # Platform compatibility information
        self.os_info = {}
        self.ui_info = {}
        self.network_info = {}
        self.performance_info = {}
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
                        
                    # Load platform compatibility information
                    self.os_info = config.get("os_info", {})
                    self.ui_info = config.get("ui_info", {})
                    self.network_info = config.get("network_info", {})
                    self.performance_info = config.get("performance_info", {})
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
                "project_path": self.project_path,  # Save the project path
                # Save compatibility information
                "os_info": self.os_info,
                "ui_info": self.ui_info,
                "network_info": self.network_info,
                "performance_info": self.performance_info
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

    def _continuous_improvement(self):
        """Continuously works on improving the AI CEO system for cross-platform compatibility"""
        # Use the dedicated ContinuousImprovement class
        improvement_system = ContinuousImprovement(self.CONFIG_FILE, self.debug_mode)
        improvement_system.start()
        
        # Keep the thread alive until stop is requested
        while not self.stop_requested:
            time.sleep(5)
            
        # Stop the improvement system when main thread stops
        improvement_system.stop()
    
    def run_ai_ceo(self):
        """Runs the AI CEO system in a loop with continuous self-improvement"""
        iterations = 0
        
        # Start the self-improvement thread
        self.improvement_thread = threading.Thread(target=self._continuous_improvement)
        self.improvement_thread.daemon = True
        self.improvement_thread.start()
        
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
            print("\n========== GIT REPOSITORY CLONING ==========")
            # Validate repository URL
            if not repo_url:
                print("[ERROR] No repository URL provided.")
                return False
                
            # Support different Git URL formats
            if not (repo_url.startswith('http') or 
                   repo_url.startswith('https') or 
                   repo_url.startswith('git@') or 
                   repo_url.startswith('ssh:')):
                print("[WARNING] URL format may not be valid. Supported formats:")
                print("  • https://github.com/username/repo.git")
                print("  • git@github.com:username/repo.git")
                print("  • ssh://git@github.com/username/repo.git")
                confirm = input("Continue anyway? (y/n): ").lower()
                if confirm != 'y':
                    print("[INFO] Clone operation cancelled.")
                    return False
            
            # If no target directory provided, extract name from the repo URL
            if not target_dir:
                # Extract repository name from URL
                try:
                    if '/' in repo_url:
                        repo_name = repo_url.split('/')[-1]
                    elif ':' in repo_url:
                        repo_name = repo_url.split(':')[-1].split('/')[-1]
                    else:
                        repo_name = "cloned_repo"
                        
                    if repo_name.endswith('.git'):
                        repo_name = repo_name[:-4]  # Remove .git extension
                    
                    target_dir = os.path.join(os.getcwd(), repo_name)
                except Exception as e:
                    print(f"[WARNING] Could not extract repo name from URL: {str(e)}")
                    target_dir = os.path.join(os.getcwd(), "cloned_repo")
                    
                print(f"Default target directory: {target_dir}")
                change_target = input("Use a different target directory? (y/n): ").lower()
                if change_target == 'y':
                    new_target = input("Enter target directory path: ").strip()
                    if new_target:
                        target_dir = os.path.abspath(new_target)
            else:
                target_dir = os.path.abspath(target_dir)
            
            # Validate target directory
            if os.path.exists(target_dir):
                print(f"\n[WARNING] Target directory already exists: {target_dir}")
                
                # Check if it's already a Git repository
                is_git_repo = False
                try:
                    git_check = subprocess.run(
                        ['git', '-C', target_dir, 'rev-parse', '--is-inside-work-tree'],
                        capture_output=True, text=True, check=False
                    )
                    is_git_repo = (git_check.returncode == 0 and git_check.stdout.strip() == 'true')
                except Exception:
                    is_git_repo = False
                
                if is_git_repo:
                    print("[INFO] The target directory is already a Git repository.")
                    
                    # Compare with the remote URL
                    try:
                        remote_check = subprocess.run(
                            ['git', '-C', target_dir, 'config', '--get', 'remote.origin.url'],
                            capture_output=True, text=True, check=False
                        )
                        
                        if remote_check.returncode == 0:
                            current_remote = remote_check.stdout.strip()
                            print(f"Current remote URL: {current_remote}")
                            
                            if current_remote == repo_url or repo_url in current_remote or current_remote in repo_url:
                                print("[INFO] This appears to be the same repository.")
                                action = input("What would you like to do? (pull/overwrite/cancel): ").lower()
                                
                                if action == 'pull':
                                    print("\n--------- Pulling Latest Changes ---------")
                                    pull_result = subprocess.run(
                                        ['git', '-C', target_dir, 'pull', 'origin', 'main'],
                                        capture_output=True, text=True, check=False
                                    )
                                    
                                    if pull_result.returncode == 0:
                                        print("[SUCCESS] Repository updated successfully.")
                                        
                                        # Set this as the current project
                                        self.set_project_path(target_dir)
                                        self.save_config()
                                        
                                        # Continue with analysis/integration
                                        print("\n--------- Repository Information ---------")
                                        self._print_repo_info(target_dir)
                                        
                                        self._offer_integration(target_dir)
                                        return True
                                    else:
                                        print(f"[ERROR] Failed to pull changes: {pull_result.stderr}")
                                        retry = input("Would you like to overwrite instead? (y/n): ").lower()
                                        if retry != 'y':
                                            return False
                                        # Fall through to overwrite
                                elif action == 'overwrite':
                                    # Continue to overwrite code below
                                    pass
                                else:
                                    print("[INFO] Clone operation cancelled.")
                                    return False
                    except Exception as e:
                        if self.debug_mode:
                            print(f"[DEBUG] Error checking remotes: {str(e)}")
                
                # Overwrite existing directory
                overwrite = input("Overwrite existing directory? (y/n): ").lower()
                if overwrite != 'y':
                    print("[INFO] Clone operation cancelled.")
                    return False
                
                print("\n--------- Removing Existing Directory ---------")
                print(f"Deleting {target_dir}...")
                
                try:
                    shutil.rmtree(target_dir)
                    print("[SUCCESS] Directory removed.")
                except Exception as e:
                    print(f"[ERROR] Failed to remove directory: {str(e)}")
                    return False
            
            # Clone the repository with progress indicator
            print("\n--------- Cloning Repository ---------")
            print(f"Source: {repo_url}")
            print(f"Target: {target_dir}")
            print("This may take a moment depending on repository size...")
            
            # Prepare the spinning progress indicator
            spinner = "|/-\\"
            idx = 0
            
            # Start the git clone process
            process = subprocess.Popen(
                ['git', 'clone', repo_url, target_dir],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Show a spinning progress indicator while waiting
            while process.poll() is None:
                print(f"\r[{spinner[idx % len(spinner)]}] Cloning repository...", end="")
                idx += 1
                time.sleep(0.1)
            
            # Get results
            _, stderr = process.communicate()
            
            # Check for errors
            if process.returncode != 0:
                print(f"\n[ERROR] Git clone failed: {stderr}")
                return False
            
            print("\n[SUCCESS] Repository cloned successfully!")
            
            # Set the project path to the cloned repository
            self.set_project_path(target_dir)
            self.save_config()
            
            # Display repository information
            print("\n--------- Repository Information ---------")
            self._print_repo_info(target_dir)
            
            # Offer AI CEO integration
            return self._offer_integration(target_dir)
                
        except Exception as e:
            print(f"\n[ERROR] Failed to clone repository: {str(e)}")
            if self.debug_mode:
                import traceback
                traceback.print_exc()
            return False
    
    def _print_repo_info(self, repo_dir):
        """Print detailed information about a Git repository"""
        try:
            # Get repository statistics
            stats = {}
            
            # Count files by type
            py_files = json_files = 0
            total_files = 0
            
            for root, _, files in os.walk(repo_dir):
                if '.git' in root:  # Skip .git directory
                    continue
                for file in files:
                    total_files += 1
                    if file.endswith('.py'):
                        py_files += 1
                    elif file.endswith('.json'):
                        json_files += 1
            
            # Get commit count
            try:
                commit_count = subprocess.run(
                    ['git', '-C', repo_dir, 'rev-list', '--count', 'HEAD'],
                    capture_output=True, text=True, check=False
                )
                if commit_count.returncode == 0:
                    stats['commits'] = commit_count.stdout.strip()
                else:
                    stats['commits'] = "Unknown"
            except Exception:
                stats['commits'] = "Unknown"
                
            # Get current branch
            try:
                branch = subprocess.run(
                    ['git', '-C', repo_dir, 'rev-parse', '--abbrev-ref', 'HEAD'],
                    capture_output=True, text=True, check=False
                )
                if branch.returncode == 0:
                    stats['branch'] = branch.stdout.strip()
                else:
                    stats['branch'] = "Unknown"
            except Exception:
                stats['branch'] = "Unknown"
                
            # Get last commit info
            try:
                last_commit = subprocess.run(
                    ['git', '-C', repo_dir, 'log', '-1', '--pretty=format:%h - %an, %ar: %s'],
                    capture_output=True, text=True, check=False
                )
                if last_commit.returncode == 0:
                    stats['last_commit'] = last_commit.stdout.strip()
                else:
                    stats['last_commit'] = "Unknown"
            except Exception:
                stats['last_commit'] = "Unknown"
            
            # Print repository statistics
            print(f"Repository directory: {repo_dir}")
            print(f"Total files: {total_files}")
            print(f"Python files: {py_files}")
            print(f"JSON files: {json_files}")
            print(f"Other files: {total_files - py_files - json_files}")
            print(f"Commit count: {stats['commits']}")
            print(f"Current branch: {stats['branch']}")
            print(f"Latest commit: {stats['last_commit']}")
            print("-------------------------------------------")
            
        except Exception as e:
            print(f"[WARNING] Error getting repository info: {str(e)}")
    
    def _offer_integration(self, target_dir):
        """Offer to integrate AI CEO with a repository"""
        # Analyze the repository
        print("\n--------- AI CEO Integration ---------")
        print("Analyzing repository structure...")
        missing_components = self.analyze_project()
        
        if missing_components:
            print("\nThis repository needs the following AI CEO components:")
            for component in missing_components:
                print(f"  • {component}")
        else:
            print("\nThis repository already has all required AI CEO components.")
            
        # Ask if user wants to integrate
        integrate = input("\nIntegrate AI CEO functionality? (y/n): ").lower()
        if integrate == 'y':
            self.integrate_ai_ceo(target_dir, missing_components)
            return True
        else:
            print("\n[INFO] Integration skipped. You can run 'integrate' later if needed.")
            return True
            
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
            print("\n========== AI CEO INTEGRATION ==========")
            print(f"Target directory: {target_dir}")
            
            # Validate target directory
            if not os.path.exists(target_dir):
                print(f"[ERROR] Target directory does not exist: {target_dir}")
                print("Please specify a valid project directory.")
                return False
                
            # If missing_components is None, analyze the project
            if missing_components is None:
                print("Analyzing project structure...")
                missing_components = self.analyze_project()
            
            # Print integration plan
            print("\n--------- Integration Plan ---------")
            if missing_components:
                print(f"The following components will be generated:")
                for component in missing_components:
                    print(f"  • {component}")
            else:
                print("All required components are already present.")
                print("Only documentation will be added.")
            print("-----------------------------------")
            
            # Confirm integration
            confirm = input("\nProceed with integration? (y/n): ").lower()
            if confirm != 'y':
                print("Integration cancelled.")
                return False
                
            # Deploy AI engineers to generate missing components
            if missing_components:
                print("\n--------- Deploying AI Engineers ---------")
                print(f"Generating {len(missing_components)} missing components...")
                
                # Create a progress bar
                for i, component in enumerate(missing_components):
                    progress = int((i / len(missing_components)) * 20)
                    progress_bar = "█" * progress + "░" * (20 - progress)
                    print(f"\r[{progress_bar}] Deploying for: {component}", end="")
                    
                    # Actually generate the component
                    self.deploy_ai_engineers([component])
                    
                    # Complete this component
                    progress_bar = "█" * 20
                    print(f"\r[{progress_bar}] Completed: {component}   ")
                
                print("\n--------------------------------------")
            
            # Create integration documentation
            print("\n--------- Creating Documentation ---------")
            integration_file = os.path.join(target_dir, "ai_ceo_integration.md")
            
            # Prepare the components list
            if missing_components:
                components_text = "- " + "\n- ".join(missing_components)
            else:
                components_text = "- None (All required components were already present)"
            
            # Get project statistics
            py_files = 0
            total_files = 0
            
            for root, _, files in os.walk(target_dir):
                for file in files:
                    total_files += 1
                    if file.endswith('.py'):
                        py_files += 1
            
            # Write the integration document
            with open(integration_file, 'w') as f:
                f.write(f"""# AI CEO Integration

This project has been integrated with the AI CEO Management System, providing intelligent project analysis and management capabilities.

## Project Overview

- Integration date: {time.strftime("%Y-%m-%d %H:%M:%S")}
- Python files: {py_files}
- Total files: {total_files}
- AI CEO version: 1.0.0

## Generated Components

The following components were added to your project:

{components_text}

## Features Added

- **Continuous Project Analysis**: AI CEO monitors your project structure and identifies missing components
- **Virtual AI Engineering Team**: Deploy AI engineers to generate code based on project requirements
- **Project Management**: Get insights into your project's status and structure
- **Command-line Interface**: Interact with the AI CEO system through a comprehensive CLI

## Getting Started

1. Run the AI CEO system to analyze and optimize your project:
   ```
   python main.py
   ```

2. Use the following commands to interact with AI CEO:
   - `status` - View the current project status
   - `analyze` - Run an analysis cycle
   - `help` - See all available commands

## Documentation

For more information on how to use the AI CEO system, refer to the generated
AI CEO components in your project directory.

---
*Integration completed on: {time.strftime("%Y-%m-%d %H:%M:%S")}*
""")
            
            # Create a .aiceo configuration file
            config_file = os.path.join(target_dir, ".aiceo")
            with open(config_file, 'w') as f:
                f.write(f"""# AI CEO Configuration
integration_date={time.strftime("%Y-%m-%d %H:%M:%S")}
integration_version=1.0.0
components_added={len(missing_components)}
project_dir={target_dir}
""")
            
            print(f"Created documentation: {integration_file}")
            print(f"Added configuration: {config_file}")
            print("--------------------------------------")
            
            print("\n========= INTEGRATION COMPLETE =========")
            print(f"✓ Added {len(missing_components)} AI CEO components")
            print(f"✓ Generated documentation")
            print(f"✓ Project is now AI CEO compatible")
            print("\nUse 'python main.py' to start managing your project with AI CEO")
            print("==========================================")
            
            return True
            
        except Exception as e:
            print(f"\n[ERROR] Failed to integrate AI CEO: {str(e)}")
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
                    print("\nAI CEO Management System - Command Reference")
                    print("=================================================")
                    print("\nSystem Control:")
                    print("  start      - Start AI CEO system background monitoring")
                    print("  stop       - Stop AI CEO system monitoring")
                    print("  status     - Check system status and project components")
                    print("  compat     - Display platform compatibility information")
                    print("  debug      - Toggle debug mode for verbose logging")
                    print("  engineers  - Set number of AI engineers (1-10)")
                    print("  exit       - Exit the application")
                    
                    print("\nProject Management:")
                    print("  project    - Set or view current project path")
                    print("  browse     - Browse directories to select a project folder")
                    print("  dialog     - Open a file dialog to select a project folder")
                    print("  analyze    - Run a single analysis cycle on current project")
                    
                    print("\nDApp Integration:")
                    print("  clone      - Clone a Git repository and integrate AI CEO")
                    print("  integrate  - Integrate AI CEO into current project")
                    
                    print("\nExamples:")
                    print("  > clone                   - Interactive clone of a repository")
                    print("  > integrate               - Add AI CEO to current project")
                    print("  > analyze                 - Check for missing components")
                    print("  > project set /path/to/project - Change project directory")
                    print("  > status                  - Show system and project status")
                    print("")
                
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
                    print("\n-------- AI CEO System Status --------")
                    if self.running_thread and self.running_thread.is_alive():
                        print("Status: 🟢 Running")
                    else:
                        print("Status: 🔴 Stopped")
                    print(f"Debug mode: {'Enabled ✓' if self.debug_mode else 'Disabled ✗'}")
                    print(f"AI Engineers: {self.ai_engineers}")
                    print(f"Last config save: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    print("\n-------- Project Information --------")
                    print(f"Project path: {self.project_path}")
                    print(f"Path exists: {'Yes ✓' if os.path.exists(self.project_path) else 'No ✗'}")
                    
                    # Count files by type
                    py_files = 0
                    json_files = 0
                    other_files = 0
                    
                    if os.path.exists(self.project_path):
                        for root, dirs, files in os.walk(self.project_path):
                            for file in files:
                                if file.endswith('.py'):
                                    py_files += 1
                                elif file.endswith('.json'):
                                    json_files += 1
                                else:
                                    other_files += 1
                    
                    print(f"Python files: {py_files}")
                    print(f"JSON files: {json_files}")
                    print(f"Other files: {other_files}")
                    
                    # Check for missing components
                    print("\n-------- Component Analysis --------")
                    missing = self.analyze_project()
                    if missing:
                        print(f"Missing components: {', '.join(missing)}")
                        print("\nRecommendation: Run the 'integrate' command to add missing components")
                    else:
                        print("All core components are present ✓")
                        
                    # Git repository information
                    print("\n-------- Git Repository Info --------")
                    try:
                        # Check if it's a git repository
                        result = subprocess.run(
                            ['git', '-C', self.project_path, 'rev-parse', '--is-inside-work-tree'],
                            capture_output=True, text=True, check=False
                        )
                        
                        if result.returncode == 0 and result.stdout.strip() == 'true':
                            # Get remote URL
                            remote_result = subprocess.run(
                                ['git', '-C', self.project_path, 'config', '--get', 'remote.origin.url'],
                                capture_output=True, text=True, check=False
                            )
                            remote_url = remote_result.stdout.strip() if remote_result.returncode == 0 else "Not set"
                            
                            # Get current branch
                            branch_result = subprocess.run(
                                ['git', '-C', self.project_path, 'rev-parse', '--abbrev-ref', 'HEAD'],
                                capture_output=True, text=True, check=False
                            )
                            branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "Unknown"
                            
                            print(f"Git repository: Yes ✓")
                            print(f"Remote origin: {remote_url}")
                            print(f"Current branch: {branch}")
                        else:
                            print("Git repository: No ✗")
                            print("Note: Initialize a Git repository to enable version control")
                    except Exception as e:
                        print("Git repository: Error checking")
                        if self.debug_mode:
                            print(f"Error details: {str(e)}")
                    print("-----------------------------------")
                
                elif command == 'compat':
                    print("\n-------- Platform Compatibility Information --------")
                    
                    # Operating System Information
                    print("Operating System:")
                    if self.os_info:
                        system = self.os_info.get('system', 'Unknown')
                        release = self.os_info.get('release', 'Unknown')
                        machine = self.os_info.get('machine', 'Unknown')
                        last_check = self.os_info.get('last_check', 'Never')
                        print(f"  System: {system} {release}")
                        print(f"  Architecture: {machine}")
                        print(f"  Last check: {last_check}")
                    else:
                        print("  No OS information available. Start AI CEO to gather data.")
                    
                    # UI Toolkit Information
                    print("\nUI Toolkit Compatibility:")
                    if self.ui_info:
                        toolkits = self.ui_info.get('available_toolkits', {})
                        preferred = self.ui_info.get('preferred_toolkit', 'Unknown')
                        
                        print(f"  Kivy: {'Available ✓' if toolkits.get('kivy', False) else 'Not available ✗'}")
                        print(f"  Tkinter: {'Available ✓' if toolkits.get('tkinter', False) else 'Not available ✗'}")
                        print(f"  Terminal: {'Available ✓' if toolkits.get('terminal', True) else 'Not available ✗'}")
                        print(f"  Preferred toolkit: {preferred}")
                    else:
                        print("  No UI information available. Start AI CEO to gather data.")
                    
                    # Networking Information
                    print("\nNetwork Compatibility:")
                    if self.network_info:
                        internet = 'Available ✓' if self.network_info.get('internet_available', False) else 'Limited ✗'
                        print(f"  Internet connectivity: {internet}")
                    else:
                        print("  No network information available. Start AI CEO to gather data.")
                    
                    # Performance Information
                    print("\nPerformance Optimization:")
                    if self.performance_info:
                        cpu_count = self.performance_info.get('cpu_count', 'Unknown')
                        recommended = self.performance_info.get('recommended_engineers', 5)
                        print(f"  CPU cores: {cpu_count}")
                        print(f"  Recommended engineers: {recommended}")
                        print(f"  Current engineers: {self.ai_engineers}")
                        
                        if self.ai_engineers < recommended:
                            print(f"  Recommendation: Increase engineers to {recommended} for optimal performance")
                    else:
                        print("  No performance information available. Start AI CEO to gather data.")
                    
                    print("---------------------------------------------------")
                
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

def run_gui_mode():
    """Run the AI CEO System in GUI mode using Kivy"""
    try:
        # We import here to avoid Kivy initialization when running in CLI mode
        from ai_ceo_ui import AICEOApp
        app = AICEOApp()
        app.run()
    except ImportError as e:
        print(f"Error loading GUI: {str(e)}")
        print("Make sure Kivy is installed correctly.")
        print("Falling back to command-line interface.")
        run_cli_mode()
    except Exception as e:
        print(f"Error starting GUI: {str(e)}")
        print("Falling back to command-line interface.")
        run_cli_mode()

def run_cli_mode():
    """Run the AI CEO System in command-line interface mode"""
    ai_ceo_system = AICEOSystem()
    ai_ceo_system.start()

def show_compatibility_info():
    """Display system compatibility information non-interactively"""
    system = AICEOSystem()
    
    # Run a single improvement cycle to gather data
    improvement = ContinuousImprovement(system.CONFIG_FILE, system.debug_mode)
    improvement.check_platform_compatibility()
    improvement.check_ui_compatibility()
    improvement.check_networking_compatibility()
    improvement.check_performance_optimization()
    improvement.check_security_enhancements()
    improvement.save_config()  # Save the gathered data
    
    # Copy the gathered data directly to system
    system.os_info = improvement.os_info
    system.ui_info = improvement.ui_info
    system.network_info = improvement.network_info 
    system.performance_info = improvement.performance_info
    
    # Display compatibility information
    print("\n-------- Platform Compatibility Information --------")
    
    # Operating System Information
    print("Operating System:")
    if system.os_info:
        system_name = system.os_info.get('system', 'Unknown')
        release = system.os_info.get('release', 'Unknown')
        machine = system.os_info.get('machine', 'Unknown')
        last_check = system.os_info.get('last_check', 'Never')
        print(f"  System: {system_name} {release}")
        print(f"  Architecture: {machine}")
        print(f"  Last check: {last_check}")
    else:
        print("  No OS information available.")
    
    # UI Toolkit Information
    print("\nUI Toolkit Compatibility:")
    if system.ui_info:
        toolkits = system.ui_info.get('available_toolkits', {})
        preferred = system.ui_info.get('preferred_toolkit', 'Unknown')
        
        print(f"  Kivy: {'Available ✓' if toolkits.get('kivy', False) else 'Not available ✗'}")
        print(f"  Tkinter: {'Available ✓' if toolkits.get('tkinter', False) else 'Not available ✗'}")
        print(f"  Terminal: {'Available ✓' if toolkits.get('terminal', True) else 'Not available ✗'}")
        print(f"  Preferred toolkit: {preferred}")
    else:
        print("  No UI information available.")
    
    # Networking Information
    print("\nNetwork Compatibility:")
    if system.network_info:
        internet = 'Available ✓' if system.network_info.get('internet_available', False) else 'Limited ✗'
        print(f"  Internet connectivity: {internet}")
    else:
        print("  No network information available.")
    
    # Performance Information
    print("\nPerformance Optimization:")
    if system.performance_info:
        cpu_count = system.performance_info.get('cpu_count', 'Unknown')
        recommended = system.performance_info.get('recommended_engineers', 5)
        print(f"  CPU cores: {cpu_count}")
        print(f"  Recommended engineers: {recommended}")
        print(f"  Current engineers: {system.ai_engineers}")
        
        if system.ai_engineers < recommended:
            print(f"  Recommendation: Increase engineers to {recommended} for optimal performance")
    else:
        print("  No performance information available.")
    
    print("---------------------------------------------------")

if __name__ == '__main__':
    # Check if command-line args specify a mode
    import sys
    
    # We need to handle Kivy's command line arguments
    # Set KIVY_NO_ARGS=1 in the environment to disable Kivy's argument parser
    os.environ['KIVY_NO_ARGS'] = '1'
    
    # Now check for our own arguments
    use_cli = False
    use_gui = False
    test_compat = False
    
    # Process command line arguments
    for arg in sys.argv[1:]:
        if arg.lower() == 'cli':
            use_cli = True
        elif arg.lower() == 'gui':
            use_gui = True
        elif arg.lower() == 'compat':
            test_compat = True
    
    if test_compat:
        # Just run the compatibility check and exit
        show_compatibility_info()
    elif use_cli:
        # Explicitly requested CLI mode
        print("Starting AI CEO in command-line mode")
        run_cli_mode()
    elif use_gui:
        # Explicitly requested GUI mode
        print("Starting AI CEO in graphical mode")
        run_gui_mode()
    else:
        # Try GUI mode by default, fallback to CLI
        try:
            # Test if Kivy is available
            import kivy
            print("Starting AI CEO in graphical mode (default)")
            run_gui_mode()
        except ImportError:
            print("Kivy not available. Starting in command-line mode")
            run_cli_mode()