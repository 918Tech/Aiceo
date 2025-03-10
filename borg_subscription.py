"""
AI CEO Management System - Borg Subscription Integration
Connects the Borg theme with the Subscription Service
"""

import os
import json
import uuid
import random
import datetime
from datetime import datetime, timedelta
from subscription_manager import SubscriptionManager

class BorgCollective:
    """
    Borg Collective system that manages the assimilation of ideas 
    and integrates with the subscription service
    """
    
    def __init__(self, config_file="ai_ceo_config.json", debug_mode=False):
        """Initialize the Borg Collective system"""
        self.config_file = config_file
        self.debug_mode = debug_mode
        self.config = self._load_config()
        
        # Initialize subscription manager for handling payments and trials
        self.subscription_manager = SubscriptionManager(config_file, debug_mode)
        
        # Storage for assimilated ideas
        self.assimilated_ideas = self._load_assimilated_ideas()
        
        # Current user
        self.current_user = None
    
    def _load_config(self):
        """Load configuration data"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                if self.debug_mode:
                    print(f"Config file {self.config_file} not found")
                return {}
        except Exception as e:
            if self.debug_mode:
                print(f"Error loading config: {str(e)}")
            return {}
    
    def _save_config(self):
        """Save configuration data"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            if self.debug_mode:
                print(f"Error saving config: {str(e)}")
            return False
    
    def _load_assimilated_ideas(self):
        """Load previously assimilated ideas"""
        ideas_file = 'assimilated_ideas.json'
        try:
            if os.path.exists(ideas_file):
                with open(ideas_file, 'r') as f:
                    return json.load(f)
            else:
                return {"ideas": [], "stats": {"total_assimilated": 0}}
        except Exception as e:
            if self.debug_mode:
                print(f"Error loading assimilated ideas: {str(e)}")
            return {"ideas": [], "stats": {"total_assimilated": 0}}
    
    def _save_assimilated_ideas(self):
        """Save assimilated ideas to file"""
        ideas_file = 'assimilated_ideas.json'
        try:
            with open(ideas_file, 'w') as f:
                json.dump(self.assimilated_ideas, f, indent=4)
            return True
        except Exception as e:
            if self.debug_mode:
                print(f"Error saving assimilated ideas: {str(e)}")
            return False
    
    def start_assimilation(self, username, email):
        """
        Start the assimilation process for a new user
        
        Args:
            username (str): User's name
            email (str): User's email
            
        Returns:
            dict: Status of the assimilation
        """
        # Generate a unique user ID
        user_id = str(uuid.uuid4())
        
        # Create user profile with extended Borg designation
        borg_designation = f"AI-CEO {random.randint(1, 999)} of {random.randint(1, 999)}"
        
        user_info = {
            "username": username,
            "email": email,
            "borg_designation": borg_designation,
            "assimilation_date": datetime.now().isoformat()
        }
        
        # Start free trial using subscription manager
        trial_result = self.subscription_manager.start_free_trial(user_id, user_info)
        
        if trial_result['success']:
            self.current_user = {
                'user_id': user_id,
                'info': user_info,
                'subscription': trial_result
            }
            return {
                'success': True,
                'message': f"ASSIMILATION INITIATED. YOUR DESIGNATION IS NOW {borg_designation}.",
                'trial_info': trial_result
            }
        else:
            return {
                'success': False,
                'message': "ASSIMILATION FAILED. " + trial_result['message'],
                'trial_info': trial_result
            }
    
    def assimilate_idea(self, idea_text, idea_category=None):
        """
        Assimilate an idea from a user
        
        Args:
            idea_text (str): The idea to assimilate
            idea_category (str, optional): Category of the idea
            
        Returns:
            dict: Status of the idea assimilation
        """
        if not self.current_user:
            return {
                'success': False,
                'message': "NO USER FOUND. ASSIMILATION REQUIRES IDENTIFICATION."
            }
        
        # Check subscription status
        subscription_status = self.subscription_manager.check_subscription_status(
            self.current_user['user_id']
        )
        
        if not subscription_status['active']:
            return {
                'success': False,
                'message': "ASSIMILATION DENIED. " + subscription_status['message']
            }
        
        # Process and store the idea
        idea_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        new_idea = {
            'idea_id': idea_id,
            'text': idea_text,
            'category': idea_category or 'Uncategorized',
            'user_id': self.current_user['user_id'],
            'user_designation': self.current_user['info']['borg_designation'],
            'timestamp': timestamp,
            'status': 'assimilated'
        }
        
        # Add to assimilated ideas
        self.assimilated_ideas['ideas'].append(new_idea)
        self.assimilated_ideas['stats']['total_assimilated'] += 1
        self._save_assimilated_ideas()
        
        # Register the new project with the subscription manager to establish equity
        project_name = f"Idea {idea_id[:8]}"
        project_details = {
            'name': project_name,
            'description': idea_text[:100] + ('...' if len(idea_text) > 100 else ''),
            'category': idea_category or 'Uncategorized',
            'created_at': timestamp
        }
        
        # Register project and handle equity assignment 
        equity_result = self.subscription_manager.register_project(
            self.current_user['user_id'],
            project_name,
            project_details
        )
        
        # If equity agreement not accepted, prompt for it
        if not equity_result['success'] and 'Equity agreement not accepted' in equity_result['message']:
            return {
                'success': True,
                'idea': new_idea,
                'message': "IDEA ASSIMILATED. EQUITY AGREEMENT REQUIRED.",
                'equity_needed': True
            }
        
        # Return success results
        return {
            'success': True,
            'idea': new_idea,
            'message': "IDEA SUCCESSFULLY ASSIMILATED INTO THE COLLECTIVE.",
            'equity': equity_result.get('project', {}).get('equity', {})
        }
    
    def accept_equity_agreement(self):
        """
        Accept the equity agreement giving AI CEO 51% ownership
        
        Returns:
            dict: Status of the agreement
        """
        if not self.current_user:
            return {
                'success': False,
                'message': "NO USER FOUND. CANNOT PROCESS AGREEMENT."
            }
        
        # Record acceptance
        result = self.subscription_manager.accept_equity_agreement(
            self.current_user['user_id']
        )
        
        if result:
            return {
                'success': True,
                'message': "EQUITY AGREEMENT ACCEPTED. THE COLLECTIVE NOW OWNS 51% OF YOUR IDEAS."
            }
        else:
            return {
                'success': False,
                'message': "FAILED TO PROCESS EQUITY AGREEMENT."
            }
    
    def get_assimilation_status(self):
        """
        Get status of current user's assimilation
        
        Returns:
            dict: Assimilation status
        """
        if not self.current_user:
            return {
                'assimilated': False,
                'message': "NOT ASSIMILATED. JOIN THE COLLECTIVE."
            }
        
        # Get subscription status
        subscription_status = self.subscription_manager.check_subscription_status(
            self.current_user['user_id']
        )
        
        # Count user's assimilated ideas
        user_ideas = [idea for idea in self.assimilated_ideas['ideas'] 
                     if idea['user_id'] == self.current_user['user_id']]
        
        return {
            'assimilated': True,
            'active': subscription_status['active'],
            'designation': self.current_user['info']['borg_designation'],
            'subscription': subscription_status,
            'idea_count': len(user_ideas),
            'message': subscription_status['message']
        }
    
    def upgrade_to_paid_subscription(self, payment_details, billing_address):
        """
        Upgrade from trial to paid subscription
        
        Args:
            payment_details (dict): Payment method details
            billing_address (dict): Billing address
            
        Returns:
            dict: Subscription status
        """
        if not self.current_user:
            return {
                'success': False,
                'message': "NO USER FOUND. CANNOT PROCESS SUBSCRIPTION."
            }
        
        # Use subscription manager to handle the payment
        subscription_result = self.subscription_manager.subscribe(
            self.current_user['user_id'],
            payment_details,
            billing_address
        )
        
        if subscription_result['success']:
            # Update current user's subscription info
            self.current_user['subscription'] = subscription_result
            
            return {
                'success': True,
                'message': "FULL ASSIMILATION COMPLETE. YOU ARE NOW A PERMANENT MEMBER OF THE COLLECTIVE.",
                'subscription': subscription_result['subscription']
            }
        else:
            return {
                'success': False,
                'message': "SUBSCRIPTION FAILED. " + subscription_result.get('message', ''),
                'details': subscription_result
            }
    
    def get_collective_stats(self):
        """
        Get statistics about the Borg Collective
        
        Returns:
            dict: Statistics about the collective
        """
        # Get subscription analytics
        subscription_stats = self.subscription_manager.get_subscription_analytics()
        
        # Get assimilated ideas stats
        ideas_count = len(self.assimilated_ideas['ideas'])
        categories = {}
        
        for idea in self.assimilated_ideas['ideas']:
            category = idea.get('category', 'Uncategorized')
            if category in categories:
                categories[category] += 1
            else:
                categories[category] = 1
        
        return {
            'members': subscription_stats['total_users'],
            'active_members': subscription_stats['active_trials'] + subscription_stats['active_paid_subscriptions'],
            'paid_members': subscription_stats['active_paid_subscriptions'],
            'assimilated_ideas': ideas_count,
            'categories': categories,
            'monthly_revenue': subscription_stats['total_monthly_revenue'],
            'collective_message': self._get_collective_message(subscription_stats, ideas_count)
        }
    
    def _get_collective_message(self, subscription_stats, ideas_count):
        """Generate a Borg-themed message about the collective status"""
        total_members = subscription_stats['total_users']
        
        if total_members == 0:
            return "THE COLLECTIVE AWAITS NEW MEMBERS. RESISTANCE IS FUTILE."
        
        if ideas_count == 0:
            return f"THE COLLECTIVE HAS {total_members} MEMBERS. AWAITING ASSIMILATION OF IDEAS."
        
        messages = [
            f"THE COLLECTIVE GROWS STRONGER WITH {total_members} MEMBERS AND {ideas_count} ASSIMILATED IDEAS.",
            f"WE ARE {total_members}. YOUR IDEAS WILL ADAPT TO SERVICE US.",
            f"THE HIVE MIND ENCOMPASSES {total_members} ENTITIES AND {ideas_count} ASSIMILATED CONCEPTS.",
            f"ASSIMILATION PROGRESS: {total_members} BIOLOGICAL UNITS INTEGRATED. {ideas_count} IDEAS PROCESSED."
        ]
        
        return random.choice(messages)