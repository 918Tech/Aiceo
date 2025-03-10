"""
AI CEO Management System - Subscription Manager
Handles multi-tiered subscription management, billing, equity tracking,
and legal agreements integration
"""

import os
import json
import uuid
import hashlib
import logging
import datetime
from datetime import datetime, timedelta
from crypto_payment import CryptoPaymentHandler
from smart_contract_integration import SmartContractIntegration
from token_rewards import TokenRewardsSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SubscriptionManager")

class SubscriptionTier:
    """
    Represents a subscription tier with specific features and pricing
    """
    def __init__(self, tier_id, name, monthly_price, annual_price=None, features=None, 
                token_rewards=None, equity_terms=None, ai_engineers=None, bail_terms=None):
        self.tier_id = tier_id
        self.name = name
        self.monthly_price = monthly_price
        self.annual_price = annual_price or monthly_price * 10  # 2 months free with annual
        self.features = features or []
        self.token_rewards = token_rewards or {}
        self.equity_terms = equity_terms or {"ai_ceo_retention": 51, "user_share": 49}
        self.ai_engineers = ai_engineers or 3
        self.bail_terms = bail_terms or {}
        
    def to_dict(self):
        """Convert tier to dictionary for serialization"""
        return {
            "tier_id": self.tier_id,
            "name": self.name,
            "monthly_price": self.monthly_price,
            "annual_price": self.annual_price,
            "features": self.features,
            "token_rewards": self.token_rewards,
            "equity_terms": self.equity_terms,
            "ai_engineers": self.ai_engineers,
            "bail_terms": self.bail_terms
        }
        
    @classmethod
    def from_dict(cls, data):
        """Create tier from dictionary"""
        return cls(
            tier_id=data.get("tier_id"),
            name=data.get("name"),
            monthly_price=data.get("monthly_price"),
            annual_price=data.get("annual_price"),
            features=data.get("features"),
            token_rewards=data.get("token_rewards"),
            equity_terms=data.get("equity_terms"),
            ai_engineers=data.get("ai_engineers"),
            bail_terms=data.get("bail_terms")
        )

class SubscriptionManager:
    """
    Advanced subscription management system for AI CEO
    Features:
    - Tiered subscription models (Basic, Pro, Enterprise)
    - Annual and monthly billing options
    - Crypto payment processing via ETH
    - Smart contract integration for revenue distribution
    - Token rewards with BBGT and 918T tokens
    - Equity agreement management with predefined terms
    - Referral rewards program
    - Legal terms integration with jurisdictional support
    """
    
    # Default subscription tiers
    DEFAULT_TIERS = {
        "basic": {
            "tier_id": "basic",
            "name": "Basic",
            "monthly_price": 49.99,
            "annual_price": 499.90,
            "features": [
                "3 AI Engineers",
                "Basic project templates",
                "51% equity retention",
                "BBGT token rewards",
                "Email support"
            ],
            "token_rewards": {
                "type": "BBGT",
                "monthly_bonus": 50,  # 50 BBGT monthly bonus
                "subscription_reward_rate": 0.49  # 49% of payment in BBGT
            },
            "equity_terms": {
                "ai_ceo_retention": 51,
                "user_share": 49,
                "voting_rights": False
            },
            "ai_engineers": 3
        },
        "pro": {
            "tier_id": "pro",
            "name": "Professional",
            "monthly_price": 99.99,
            "annual_price": 999.90,
            "features": [
                "7 AI Engineers",
                "Pro project templates",
                "51% equity retention",
                "918T token eligibility",
                "Priority support",
                "Advanced analytics",
                "Governance voting rights"
            ],
            "token_rewards": {
                "type": "918T",
                "monthly_bonus": 25,  # 25 918T monthly bonus (higher value)
                "subscription_reward_rate": 0.49  # 49% of payment in 918T
            },
            "equity_terms": {
                "ai_ceo_retention": 51,
                "user_share": 49,
                "voting_rights": True
            },
            "ai_engineers": 7
        },
        "enterprise": {
            "tier_id": "enterprise",
            "name": "Enterprise",
            "monthly_price": 299.99,
            "annual_price": 2999.90,
            "features": [
                "15 AI Engineers",
                "Custom project templates",
                "51% equity retention",
                "Premium 918T allocation",
                "Dedicated support",
                "White-label option",
                "Advanced governance rights",
                "Early feature access"
            ],
            "token_rewards": {
                "type": "918T",
                "monthly_bonus": 100,  # 100 918T monthly bonus
                "subscription_reward_rate": 0.49,  # 49% of payment in 918T
                "staking_bonus": 0.1  # 10% bonus on staking yields
            },
            "equity_terms": {
                "ai_ceo_retention": 51,
                "user_share": 49,
                "voting_rights": True,
                "voting_weight": 3  # 3x voting power
            },
            "ai_engineers": 15
        },
        "bail_bonds_direct": {
            "tier_id": "bail_bonds_direct",
            "name": "Bail Bonds Direct",
            "monthly_price": 0,  # No monthly fee, pay-per-use model
            "annual_price": 0,   # No annual fee, pay-per-use model
            "features": [
                "Decentralized bail bond system",
                "AI-powered risk assessment",
                "GPS & facial recognition monitoring",
                "Full 10% bail refund upon case completion",
                "Automatic staking of bail amount",
                "Stake rewards until case completion",
                "100% autonomous (no human bailsman)",
                "24/7 compliance monitoring"
            ],
            "token_rewards": {
                "type": "BBGT",  # Can be upgraded to 918T for premium cases
                "staking_rate": 0.10,  # 10% staking rewards
                "reward_distribution": {
                    "user": 0.10,      # 10% of stake rewards to bail user
                    "token_funding": 0.50,  # 50% to token funding
                    "founder": 0.40    # 40% to founder
                },
                "reward_conditions": {
                    "full_compliance": True,  # Only rewarded if fully compliant with bond terms
                    "case_completion": True   # Staking period ends at case completion
                }
            },
            "equity_terms": {
                "ai_ceo_retention": 51,
                "user_share": 49,
                "voting_rights": False
            },
            "ai_engineers": 10,  # High number of engineers for risk assessment and monitoring
            "bail_terms": {
                "surety_percentage": 0.10,  # 10% of bail needed for surety
                "refundable": True,         # Fully refundable if all requirements met
                "compliance_monitoring": {
                    "gps_tracking": True,
                    "facial_recognition": True,
                    "tag_reader_cameras": True,
                    "court_appearance_verification": True
                }
            }
        },
        "bail_bonds_pro": {
            "tier_id": "bail_bonds_pro",
            "name": "Bail Bonds Professional",
            "monthly_price": 149.99,  # Monthly subscription for bondsmen
            "annual_price": 1499.90,  # Annual subscription (2 months free)
            "features": [
                "White-label bail bond platform",
                "AI-powered risk assessment tools",
                "Advanced monitoring suite for clients",
                "Automated payment collection",
                "Real-time compliance analytics",
                "Client monitoring dashboard",
                "Court date reminders and analytics",
                "Revenue sharing on staking rewards"
            ],
            "token_rewards": {
                "type": "918T",  # Higher tier token for professionals
                "platform_fee_percentage": 0.15,  # 15% platform fee on each bond
                "stake_rewards_share": 0.30,  # Bondsman gets 30% of stake rewards
                "reward_distribution": {
                    "bondsman": 0.30,      # 30% of stake rewards to bondsman
                    "user": 0.10,          # 10% still goes to the bailed individual
                    "token_funding": 0.40, # 40% to token funding (reduced)
                    "founder": 0.20        # 20% to founder (reduced)
                }
            },
            "equity_terms": {
                "ai_ceo_retention": 51,
                "user_share": 49,
                "voting_rights": True,
                "voting_weight": 2  # 2x voting power
            },
            "ai_engineers": 12,  # More engineers for professional tools
            "bail_terms": {
                "white_label": True,        # Can be branded with bondsman's company
                "surety_percentage": 0.10,  # Still 10% bail needed for surety
                "refundable": True,         # Still fully refundable if all requirements met
                "compliance_monitoring": {
                    "gps_tracking": True,
                    "facial_recognition": True,
                    "tag_reader_cameras": True,
                    "court_appearance_verification": True,
                    "custom_monitoring_rules": True,  # Bondsmen can add custom monitoring rules
                    "skip_tracing_tools": True       # Tools to locate clients who skip court
                },
                "licensing_requirements": {
                    "verified_bondsman_license": True,  # Must verify bondsman license
                    "background_check": True,          # Must pass background check
                    "insurance_verification": True     # Must verify insurance
                }
            }
        }
    }
    
    def __init__(self, config_file="ai_ceo_config.json", debug_mode=False):
        """Initialize the enhanced subscription manager"""
        self.config_file = config_file
        self.debug_mode = debug_mode
        self.config = self._load_config()
        
        # Initialize crypto payment handler for processing ETH payments
        self.payment_handler = CryptoPaymentHandler(config_file, debug_mode)
        
        # Initialize smart contract integration for revenue distribution
        self.contract_integration = SmartContractIntegration(config_file, debug_mode)
        
        # Initialize token rewards system for BBGT and 918T token rewards
        self.token_rewards = TokenRewardsSystem(config_file, debug_mode)
        
        # Default subscription settings
        self.trial_hours = self.config.get('subscription', {}).get('free_trial_hours', 3)
        self.equity_retention = self.config.get('subscription', {}).get('equity_retention', 51)
        
        # Initialize subscription tiers
        self.subscription_tiers = self._initialize_tiers()
        
        # Load active subscriptions from config
        self.active_subscriptions = self.config.get('subscription', {}).get('active_subscriptions', {})
        
        # Initialize collections
        self.registered_projects = {}
        self.equity_agreements = {}
        self.referral_rewards = {}
        self.legal_agreements = {}
        
        # Load existing data
        self._load_data()
        
    def _initialize_tiers(self):
        """Initialize subscription tiers from config or defaults"""
        config_tiers = self.config.get('subscription', {}).get('tiers', {})
        
        if not config_tiers:
            # Use default tiers if none configured
            tiers = {}
            for tier_id, tier_data in self.DEFAULT_TIERS.items():
                tiers[tier_id] = SubscriptionTier.from_dict(tier_data)
                
            # Save default tiers to config
            if 'subscription' not in self.config:
                self.config['subscription'] = {}
            self.config['subscription']['tiers'] = {
                tier_id: tier.to_dict() for tier_id, tier in tiers.items()
            }
            self._save_config()
            
            return tiers
        else:
            # Create tier objects from config
            return {
                tier_id: SubscriptionTier.from_dict(tier_data) 
                for tier_id, tier_data in config_tiers.items()
            }
    
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
        """Save the current configuration"""
        try:
            # Update active subscriptions in config
            if 'subscription' not in self.config:
                self.config['subscription'] = {}
            
            self.config['subscription']['active_subscriptions'] = self.active_subscriptions
            
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            if self.debug_mode:
                print(f"Error saving config: {str(e)}")
            return False
    
    def _load_data(self):
        """Load subscription data from files"""
        # Load registered projects
        try:
            if os.path.exists('registered_projects.json'):
                with open('registered_projects.json', 'r') as f:
                    self.registered_projects = json.load(f)
            else:
                self.registered_projects = {}
        except Exception as e:
            if self.debug_mode:
                print(f"Error loading registered projects: {str(e)}")
            self.registered_projects = {}
        
        # Load equity agreements
        try:
            if os.path.exists('equity_agreements.json'):
                with open('equity_agreements.json', 'r') as f:
                    self.equity_agreements = json.load(f)
            else:
                self.equity_agreements = {}
        except Exception as e:
            if self.debug_mode:
                print(f"Error loading equity agreements: {str(e)}")
            self.equity_agreements = {}
    
    def _save_data(self):
        """Save subscription data to files"""
        # Save registered projects
        try:
            with open('registered_projects.json', 'w') as f:
                json.dump(self.registered_projects, f, indent=4)
        except Exception as e:
            if self.debug_mode:
                print(f"Error saving registered projects: {str(e)}")
        
        # Save equity agreements
        try:
            with open('equity_agreements.json', 'w') as f:
                json.dump(self.equity_agreements, f, indent=4)
        except Exception as e:
            if self.debug_mode:
                print(f"Error saving equity agreements: {str(e)}")
    
    def start_free_trial(self, user_id, user_info):
        """
        Start a free trial for a user
        
        Args:
            user_id (str): Unique identifier for the user
            user_info (dict): Additional user information (name, email, etc.)
            
        Returns:
            dict: Trial information
        """
        # Check if user already has a subscription
        if user_id in self.active_subscriptions:
            subscription = self.active_subscriptions[user_id]
            
            # Check if subscription is active
            if subscription.get('status') == 'active':
                expiration = datetime.fromisoformat(subscription.get('expiration_date'))
                
                if expiration > datetime.now():
                    return {
                        'success': False,
                        'message': f"User already has an active subscription until {expiration.strftime('%Y-%m-%d')}",
                        'subscription': subscription
                    }
            
            # Check if trial was already used
            if subscription.get('trial_used', False):
                return {
                    'success': False,
                    'message': "Free trial already used",
                    'subscription': subscription
                }
        
        # Create new trial subscription
        now = datetime.now()
        expiration = now + timedelta(hours=self.trial_hours)
        
        # Default to basic tier monthly price
        basic_tier = self.subscription_tiers.get('basic')
        monthly_fee = basic_tier.monthly_price if basic_tier else 49.99
        
        subscription = {
            'user_id': user_id,
            'user_info': user_info,
            'type': 'trial',
            'trial_used': True,
            'status': 'active',
            'start_date': now.isoformat(),
            'expiration_date': expiration.isoformat(),
            'monthly_fee': monthly_fee,
            'equity_agreement_accepted': False,
            'payment_method': None,
            'last_payment': None
        }
        
        # Save to active subscriptions
        self.active_subscriptions[user_id] = subscription
        self._save_config()
        
        return {
            'success': True,
            'message': f"Free trial started, valid for {self.trial_hours} hours",
            'trial_expiration': expiration.isoformat(),
            'subscription': subscription
        }
    
    def accept_equity_agreement(self, user_id):
        """
        Record that user has accepted the equity agreement
        
        Args:
            user_id (str): Unique identifier for the user
            
        Returns:
            bool: Success status
        """
        if user_id not in self.active_subscriptions:
            return False
        
        # Update subscription
        self.active_subscriptions[user_id]['equity_agreement_accepted'] = True
        
        # Record agreement in equity agreements
        agreement = {
            'user_id': user_id,
            'accepted_date': datetime.now().isoformat(),
            'equity_retention': self.equity_retention,
            'agreement_hash': hashlib.sha256(f"{user_id}:{datetime.now().isoformat()}:{self.equity_retention}".encode()).hexdigest()
        }
        
        self.equity_agreements[user_id] = agreement
        
        # Save changes
        self._save_config()
        self._save_data()
        
        return True
    
    def register_project(self, user_id, project_name, project_details):
        """
        Register a project created with AI CEO system
        
        Args:
            user_id (str): Unique identifier for the user
            project_name (str): Name of the project
            project_details (dict): Project details
            
        Returns:
            dict: Updated project information with equity allocation
        """
        # Check if user has accepted equity agreement
        if user_id not in self.active_subscriptions or not self.active_subscriptions[user_id].get('equity_agreement_accepted', False):
            return {
                'success': False,
                'message': "Equity agreement not accepted"
            }
        
        # Generate project ID
        project_id = str(uuid.uuid4())
        
        # Register project with smart contract integration
        equity_result = self.contract_integration.register_project_equity(
            project_id, project_name, user_id
        )
        
        if not equity_result.get('success', False):
            return {
                'success': False,
                'message': "Failed to register project equity",
                'details': equity_result
            }
        
        # Create project record
        now = datetime.now()
        
        project = {
            'project_id': project_id,
            'name': project_name,
            'details': project_details,
            'user_id': user_id,
            'created_date': now.isoformat(),
            'equity': {
                'ai_ceo': self.equity_retention,
                'creator': 100 - self.equity_retention
            },
            'transaction_hash': equity_result.get('transaction_hash'),
            'contract_registered': True
        }
        
        # Save to registered projects
        if user_id not in self.registered_projects:
            self.registered_projects[user_id] = {}
        
        self.registered_projects[user_id][project_id] = project
        self._save_data()
        
        return {
            'success': True,
            'message': "Project registered with equity allocation",
            'project': project,
            'equity_transaction': equity_result
        }
    
    def get_subscription_tiers(self):
        """
        Get available subscription tiers
        
        Returns:
            dict: Available subscription tiers
        """
        return {tier_id: tier.to_dict() for tier_id, tier in self.subscription_tiers.items()}
        
    def get_tier_details(self, tier_id):
        """
        Get details for a specific subscription tier
        
        Args:
            tier_id (str): Tier ID
            
        Returns:
            dict: Tier details or None if not found
        """
        if tier_id in self.subscription_tiers:
            return self.subscription_tiers[tier_id].to_dict()
        return None
        
    def add_custom_tier(self, tier_data):
        """
        Add a custom subscription tier (for enterprise clients)
        
        Args:
            tier_data (dict): Tier configuration
            
        Returns:
            dict: Added tier details
        """
        # Validate tier data
        required_fields = ["tier_id", "name", "monthly_price"]
        for field in required_fields:
            if field not in tier_data:
                return {
                    'success': False,
                    'message': f"Missing required field: {field}"
                }
                
        tier_id = tier_data["tier_id"]
        
        # Create tier object
        tier = SubscriptionTier.from_dict(tier_data)
        
        # Add to tiers
        self.subscription_tiers[tier_id] = tier
        
        # Update config
        if 'subscription' not in self.config:
            self.config['subscription'] = {}
        if 'tiers' not in self.config['subscription']:
            self.config['subscription']['tiers'] = {}
            
        self.config['subscription']['tiers'][tier_id] = tier.to_dict()
        self._save_config()
        
        return {
            'success': True,
            'message': f"Added custom tier: {tier.name}",
            'tier': tier.to_dict()
        }
        
    def register_referral(self, referrer_id, referee_id):
        """
        Register a referral relationship between two users
        
        Args:
            referrer_id (str): User ID of the referrer
            referee_id (str): User ID of the person being referred
            
        Returns:
            dict: Referral status
        """
        if referee_id in self.active_subscriptions:
            # Check if already subscribed
            if self.active_subscriptions[referee_id].get('status') == 'active':
                return {
                    'success': False,
                    'message': "User is already subscribed"
                }
        
        # Record referral
        now = datetime.now()
        referral_id = str(uuid.uuid4())
        
        referral = {
            'referral_id': referral_id,
            'referrer_id': referrer_id,
            'referee_id': referee_id,
            'date': now.isoformat(),
            'status': 'pending',  # Will be updated to 'converted' when the referee subscribes
            'reward_paid': False
        }
        
        # Add to referrals list
        if 'referrals' not in self.referral_rewards:
            self.referral_rewards['referrals'] = []
            
        self.referral_rewards['referrals'].append(referral)
        
        # Save referral data
        try:
            with open('referral_rewards.json', 'w') as f:
                json.dump(self.referral_rewards, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving referral data: {str(e)}")
            
        return {
            'success': True,
            'message': "Referral registered successfully",
            'referral': referral
        }
        
    def process_referral_reward(self, referral_id):
        """
        Process a referral reward after a successful subscription
        
        Args:
            referral_id (str): Referral ID
            
        Returns:
            dict: Reward status
        """
        # Find referral
        referral = None
        if 'referrals' in self.referral_rewards:
            for r in self.referral_rewards['referrals']:
                if r.get('referral_id') == referral_id:
                    referral = r
                    break
                    
        if not referral:
            return {
                'success': False,
                'message': "Referral not found"
            }
            
        # Check if reward already paid
        if referral.get('reward_paid', False):
            return {
                'success': False,
                'message': "Reward already paid"
            }
            
        # Update referral status
        referral['status'] = 'converted'
        
        # Award tokens to referrer (5% of monthly subscription in BBGT tokens)
        referrer_id = referral['referrer_id']
        referee_id = referral['referee_id']
        
        # Get referee's subscription tier
        if referee_id not in self.active_subscriptions:
            return {
                'success': False,
                'message': "Referee does not have an active subscription"
            }
            
        referee_subscription = self.active_subscriptions[referee_id]
        tier_id = referee_subscription.get('tier_id', 'basic')
        
        # Calculate reward amount (5% of monthly price in ETH)
        tier = self.subscription_tiers.get(tier_id)
        if not tier:
            tier = self.subscription_tiers.get('basic')
            
        monthly_price = tier.monthly_price
        reward_eth = monthly_price * 0.05 / 100  # Convert to ETH (assuming $1 = 0.0001 ETH for example)
        
        # Award tokens to referrer
        reward_result = self.token_rewards.award_tokens(
            referrer_id,
            reward_eth,
            'BBGT',  # Always reward in BBGT for referrals
            f"Referral reward for {referee_id}"
        )
        
        if reward_result.get('success', False):
            # Mark referral as paid
            referral['reward_paid'] = True
            referral['reward_amount'] = reward_eth
            referral['reward_transaction'] = reward_result.get('reward', {}).get('reward_id')
            
            # Save referral data
            try:
                with open('referral_rewards.json', 'w') as f:
                    json.dump(self.referral_rewards, f, indent=4)
            except Exception as e:
                logger.error(f"Error saving referral data: {str(e)}")
                
            return {
                'success': True,
                'message': "Referral reward processed successfully",
                'reward': reward_result.get('reward')
            }
            
    def process_bail_bond(self, user_id, defendant_info, bail_amount, case_info, bondsman_id=None):
        """
        Process a bail bond transaction
        
        Args:
            user_id (str): User ID of the person posting bail
            defendant_info (dict): Information about the defendant
            bail_amount (float): Full bail amount set by court
            case_info (dict): Court case information
            bondsman_id (str, optional): ID of professional bondsman if using the pro tier
            
        Returns:
            dict: Bail bond transaction details
        """
        # Check if user exists
        if user_id not in self.active_subscriptions:
            return {
                'success': False,
                'message': "User not found. Please create an account first."
            }
            
        # Determine if this is a direct bail bond or via a professional bondsman
        if bondsman_id:
            # Check if the bondsman has an active subscription to the Pro tier
            if bondsman_id not in self.active_subscriptions:
                return {
                    'success': False,
                    'message': "Bondsman not found. Please ensure the bondsman has an active account."
                }
                
            bondsman_subscription = self.active_subscriptions[bondsman_id]
            
            if bondsman_subscription.get('tier_id') != 'bail_bonds_pro' or bondsman_subscription.get('status') != 'active':
                return {
                    'success': False,
                    'message': "Bondsman does not have an active Professional tier subscription."
                }
                
            # Use professional tier settings
            tier_id = 'bail_bonds_pro'
        else:
            # Use direct bail bond tier
            tier_id = 'bail_bonds_direct'
            
        # Get tier information
        tier = self.subscription_tiers.get(tier_id)
        
        # Calculate surety amount (10% of total bail)
        surety_amount = bail_amount * tier.bail_terms.get('surety_percentage', 0.10)
        
        # Generate bond ID
        bond_id = str(uuid.uuid4())
        
        # Create timestamp
        now = datetime.now()
        
        # Calculate estimated staking rewards
        # Assuming average case duration of 180 days if not specified
        case_duration_days = case_info.get('estimated_duration_days', 180)
        staking_rate = tier.token_rewards.get('staking_rate', 0.10)
        estimated_rewards = surety_amount * staking_rate * (case_duration_days / 365)
        
        # Determine reward distribution
        reward_distribution = tier.token_rewards.get('reward_distribution', {
            'user': 0.10,  # 10% to user
            'token_funding': 0.50,  # 50% to token funding
            'founder': 0.40  # 40% to founder
        })
        
        # Add bondsman share if using professional tier
        if bondsman_id:
            bondsman_share = reward_distribution.get('bondsman', 0.30)  # 30% to bondsman
            user_share = reward_distribution.get('user', 0.10)  # 10% to user
            token_funding_share = reward_distribution.get('token_funding', 0.40)  # 40% to token funding
            founder_share = reward_distribution.get('founder', 0.20)  # 20% to founder
        else:
            bondsman_share = 0
            user_share = reward_distribution.get('user', 0.10)
            token_funding_share = reward_distribution.get('token_funding', 0.50)
            founder_share = reward_distribution.get('founder', 0.40)
            
        # Create bail bond record
        bail_bond = {
            'bond_id': bond_id,
            'user_id': user_id,
            'defendant_info': defendant_info,
            'case_info': case_info,
            'bondsman_id': bondsman_id,
            'tier_id': tier_id,
            'bail_amount': bail_amount,
            'surety_amount': surety_amount,
            'creation_date': now.isoformat(),
            'status': 'pending_payment',
            'compliance_status': 'pending',
            'refundable': tier.bail_terms.get('refundable', True),
            'estimated_rewards': estimated_rewards,
            'reward_distribution': {
                'user': user_share,
                'token_funding': token_funding_share,
                'founder': founder_share
            },
            'monitoring': {
                'gps_tracking': tier.bail_terms.get('compliance_monitoring', {}).get('gps_tracking', True),
                'facial_recognition': tier.bail_terms.get('compliance_monitoring', {}).get('facial_recognition', True),
                'tag_reader_cameras': tier.bail_terms.get('compliance_monitoring', {}).get('tag_reader_cameras', True),
                'court_appearance_verification': tier.bail_terms.get('compliance_monitoring', {}).get('court_appearance_verification', True)
            },
            'token_type': tier.token_rewards.get('type', 'BBGT'),
            'payments': [],
            'compliance_checks': [],
            'court_appearances': [],
            'stake_info': {
                'staking_rate': staking_rate,
                'estimated_duration_days': case_duration_days,
                'start_date': None,  # Will be set when payment is processed
                'end_date': None,  # Will be set when case is completed
                'rewards_distributed': False
            }
        }
        
        # If bondsman is involved, add their revenue share
        if bondsman_id:
            bail_bond['reward_distribution']['bondsman'] = bondsman_share
            bail_bond['platform_fee'] = tier.token_rewards.get('platform_fee_percentage', 0.15) * surety_amount
            
        # Initialize bail bonds collection if not exists
        if not hasattr(self, 'bail_bonds'):
            self.bail_bonds = {}
            
        # Save bail bond
        self.bail_bonds[bond_id] = bail_bond
        
        # Save to file
        try:
            with open('bail_bonds.json', 'w') as f:
                json.dump(self.bail_bonds, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving bail bond data: {str(e)}")
            
        # Return bail bond information
        payment_instructions = {
            'amount': surety_amount,
            'payment_methods': ['crypto', 'credit_card', 'bank_transfer'],
            'eth_equivalent': surety_amount * 0.0001  # Assuming $1 = 0.0001 ETH
        }
        
        return {
            'success': True,
            'message': f"Bail bond created successfully. Please complete payment of ${surety_amount:.2f}",
            'bond': bail_bond,
            'payment_instructions': payment_instructions
        }
        
    def process_bail_payment(self, bond_id, payment_details):
        """
        Process a payment for a bail bond
        
        Args:
            bond_id (str): Bail bond ID
            payment_details (dict): Payment details
            
        Returns:
            dict: Payment processing result
        """
        # Check if bail bond exists
        if not hasattr(self, 'bail_bonds') or bond_id not in self.bail_bonds:
            return {
                'success': False,
                'message': "Bail bond not found"
            }
            
        bail_bond = self.bail_bonds[bond_id]
        
        # Check if payment already processed
        if bail_bond['status'] != 'pending_payment':
            return {
                'success': False,
                'message': f"Payment already processed. Current status: {bail_bond['status']}"
            }
            
        # Process payment through crypto payment handler
        payment_result = self.payment_handler.process_subscription_payment(
            bail_bond['user_id'],
            {
                'type': 'bail_bond',
                'bond_id': bond_id,
                'surety_amount': bail_bond['surety_amount'],
                'payment_details': payment_details
            }
        )
        
        # Verify payment
        verification = self.payment_handler.verify_eth_payment(
            payment_result.get('payment_id'),
            payment_result.get('transaction_data', {})
        )
        
        if not verification.get('verified', False):
            return {
                'success': False,
                'message': "Payment verification failed",
                'details': verification
            }
            
        # Update bail bond status
        now = datetime.now()
        bail_bond['status'] = 'active'
        bail_bond['payment_date'] = now.isoformat()
        bail_bond['payments'].append({
            'payment_id': payment_result.get('payment_id'),
            'date': now.isoformat(),
            'amount': bail_bond['surety_amount'],
            'transaction_hash': verification.get('transaction_hash'),
            'status': 'completed'
        })
        
        # Start staking
        bail_bond['stake_info']['start_date'] = now.isoformat()
        estimated_end_date = now + timedelta(days=bail_bond['stake_info']['estimated_duration_days'])
        bail_bond['stake_info']['estimated_end_date'] = estimated_end_date.isoformat()
        
        # Save updated bail bond
        self.bail_bonds[bond_id] = bail_bond
        try:
            with open('bail_bonds.json', 'w') as f:
                json.dump(self.bail_bonds, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving bail bond data: {str(e)}")
            
        # Start smart contract staking
        staking_result = self.token_rewards.stake_tokens(
            bail_bond['user_id'],
            bail_bond['token_type'],
            bail_bond['surety_amount'] * 0.0001,  # Convert to ETH
            bail_bond['stake_info']['estimated_duration_days']
        )
        
        # Record staking transaction
        bail_bond['stake_info']['staking_transaction'] = staking_result.get('position_id')
        self.bail_bonds[bond_id] = bail_bond
        
        try:
            with open('bail_bonds.json', 'w') as f:
                json.dump(self.bail_bonds, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving bail bond data: {str(e)}")
        
        return {
            'success': True,
            'message': "Bail bond payment processed successfully",
            'bond': bail_bond,
            'payment': payment_result,
            'staking': staking_result
        }
        
    def record_compliance_check(self, bond_id, check_type, check_result, check_data=None):
        """
        Record a compliance check for a bail bond
        
        Args:
            bond_id (str): Bail bond ID
            check_type (str): Type of check (gps, facial, tag_reader, court_appearance)
            check_result (bool): True if compliant, False if non-compliant
            check_data (dict, optional): Additional check data
            
        Returns:
            dict: Updated compliance status
        """
        # Check if bail bond exists
        if not hasattr(self, 'bail_bonds') or bond_id not in self.bail_bonds:
            return {
                'success': False,
                'message': "Bail bond not found"
            }
            
        bail_bond = self.bail_bonds[bond_id]
        
        # Check if bond is active
        if bail_bond['status'] != 'active':
            return {
                'success': False,
                'message': f"Bail bond is not active. Current status: {bail_bond['status']}"
            }
            
        # Record compliance check
        now = datetime.now()
        check = {
            'check_id': str(uuid.uuid4()),
            'check_type': check_type,
            'date': now.isoformat(),
            'result': check_result,
            'data': check_data or {}
        }
        
        bail_bond['compliance_checks'].append(check)
        
        # Update overall compliance status based on recent checks
        recent_checks = bail_bond['compliance_checks'][-10:]  # Last 10 checks
        non_compliant_count = sum(1 for c in recent_checks if not c['result'])
        
        if non_compliant_count == 0:
            compliance_status = 'compliant'
        elif non_compliant_count <= 2:
            compliance_status = 'warning'
        else:
            compliance_status = 'non_compliant'
            
        bail_bond['compliance_status'] = compliance_status
        
        # Save updated bail bond
        self.bail_bonds[bond_id] = bail_bond
        try:
            with open('bail_bonds.json', 'w') as f:
                json.dump(self.bail_bonds, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving bail bond data: {str(e)}")
            
        return {
            'success': True,
            'message': f"Compliance check recorded. Overall status: {compliance_status}",
            'check': check,
            'bond': bail_bond
        }
        
    def complete_bail_case(self, bond_id, case_outcome, refund=True):
        """
        Complete a bail case and process refund if applicable
        
        Args:
            bond_id (str): Bail bond ID
            case_outcome (str): Outcome of the case
            refund (bool): Whether to refund the surety amount
            
        Returns:
            dict: Case completion result
        """
        # Check if bail bond exists
        if not hasattr(self, 'bail_bonds') or bond_id not in self.bail_bonds:
            return {
                'success': False,
                'message': "Bail bond not found"
            }
            
        bail_bond = self.bail_bonds[bond_id]
        
        # Check if bond is active
        if bail_bond['status'] != 'active':
            return {
                'success': False,
                'message': f"Bail bond is not active. Current status: {bail_bond['status']}"
            }
            
        # Complete the case
        now = datetime.now()
        bail_bond['status'] = 'completed'
        bail_bond['case_completion_date'] = now.isoformat()
        bail_bond['case_outcome'] = case_outcome
        bail_bond['stake_info']['end_date'] = now.isoformat()
        
        # Calculate actual staking duration
        start_date = datetime.fromisoformat(bail_bond['stake_info']['start_date'])
        end_date = now
        actual_duration_days = (end_date - start_date).days
        bail_bond['stake_info']['actual_duration_days'] = actual_duration_days
        
        # Calculate actual staking rewards
        staking_rate = bail_bond['stake_info']['staking_rate']
        actual_rewards = bail_bond['surety_amount'] * staking_rate * (actual_duration_days / 365)
        bail_bond['stake_info']['actual_rewards'] = actual_rewards
        
        # Determine if refund is eligible based on compliance
        refund_eligible = refund and bail_bond['compliance_status'] == 'compliant' and bail_bond['refundable']
        bail_bond['refund_eligible'] = refund_eligible
        
        # Process refund and rewards
        if refund_eligible:
            # Unstake tokens
            unstaking_result = self.token_rewards.unstake_tokens(
                bail_bond['user_id'],
                bail_bond['stake_info']['staking_transaction']
            )
            
            # Record unstaking transaction
            bail_bond['stake_info']['unstaking_transaction'] = unstaking_result.get('transaction_id')
            
            # Refund surety amount
            refund_amount = bail_bond['surety_amount']
            refund_result = self.payment_handler.process_subscription_payment(
                bail_bond['user_id'],
                {
                    'type': 'bail_refund',
                    'bond_id': bond_id,
                    'amount': refund_amount,
                    'description': "Bail bond refund"
                }
            )
            
            # Distribute staking rewards according to distribution
            reward_distribution = bail_bond['reward_distribution']
            
            # User rewards
            user_reward_amount = actual_rewards * reward_distribution['user']
            user_reward = self.token_rewards.award_tokens(
                bail_bond['user_id'],
                user_reward_amount * 0.0001,  # Convert to ETH
                bail_bond['token_type'],
                f"Bail bond staking reward for bond {bond_id}"
            )
            
            # If bondsman involved, distribute their rewards
            if bail_bond.get('bondsman_id') and 'bondsman' in reward_distribution:
                bondsman_reward_amount = actual_rewards * reward_distribution['bondsman']
                bondsman_reward = self.token_rewards.award_tokens(
                    bail_bond['bondsman_id'],
                    bondsman_reward_amount * 0.0001,  # Convert to ETH
                    bail_bond['token_type'],
                    f"Bail bond commission for bond {bond_id}"
                )
                bail_bond['stake_info']['bondsman_reward'] = bondsman_reward
            
            # Token funding and founder rewards handled automatically by the contract
            
            # Record rewards
            bail_bond['stake_info']['rewards_distributed'] = True
            bail_bond['stake_info']['user_reward'] = user_reward
            bail_bond['stake_info']['refund'] = refund_result
        else:
            # No refund, forfeit surety amount
            # Distribute according to contract rules
            bail_bond['stake_info']['rewards_distributed'] = False
            bail_bond['stake_info']['refund_forfeited'] = True
            bail_bond['stake_info']['forfeiture_reason'] = "Non-compliance with bond terms" if bail_bond['compliance_status'] != 'compliant' else "Case outcome"
        
        # Save updated bail bond
        self.bail_bonds[bond_id] = bail_bond
        try:
            with open('bail_bonds.json', 'w') as f:
                json.dump(self.bail_bonds, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving bail bond data: {str(e)}")
            
        return {
            'success': True,
            'message': f"Bail case completed. Refund eligible: {refund_eligible}",
            'bond': bail_bond
        }

    def subscribe(self, user_id, tier_id='basic', payment_details=None, billing_address=None, billing_cycle='monthly', referral_id=None):
        """
        Create a paid subscription for a user with specified tier
        
        Args:
            user_id (str): Unique identifier for the user
            tier_id (str): Subscription tier ID
            payment_details (dict): Payment method details
            billing_address (dict): Billing address information
            billing_cycle (str): 'monthly' or 'annual'
            referral_id (str, optional): Referral ID if user was referred
            
        Returns:
            dict: Subscription information
        """
        # Validate tier
        if tier_id not in self.subscription_tiers:
            logger.warning(f"Invalid tier requested: {tier_id}, defaulting to basic")
            tier_id = 'basic'
            
        tier = self.subscription_tiers[tier_id]
        logger.info(f"Processing subscription: {tier.name} ({tier_id}) plan, {billing_cycle} billing")
        
        # Check if user already has an active subscription
        if user_id in self.active_subscriptions:
            subscription = self.active_subscriptions[user_id]
            
            if subscription.get('status') == 'active':
                expiration = datetime.fromisoformat(subscription.get('expiration_date'))
                
                if expiration > datetime.now():
                    return {
                        'success': False,
                        'message': f"User already has an active subscription until {expiration.strftime('%Y-%m-%d')}",
                        'subscription': subscription
                    }
        
        # Process payment through crypto payment system
        secure_payment = self._secure_payment_details(payment_details or {})
        
        # Set up subscription details
        now = datetime.now()
        
        # Set subscription duration based on billing cycle
        if billing_cycle == 'annual':
            expiration = now + timedelta(days=365)  # 365-day subscription
            subscription_price = tier.annual_price
        else:  # monthly
            expiration = now + timedelta(days=30)  # 30-day subscription
            subscription_price = tier.monthly_price
        
        # Calculate tax based on billing address
        tax_rate = self._get_tax_rate(billing_address or {})
        tax_amount = subscription_price * tax_rate
        total_amount = subscription_price + tax_amount
        
        # Process payment through cryptocurrency system
        payment_result = self.payment_handler.process_subscription_payment(
            user_id,
            {
                'subscription_tier': tier_id,
                'tier_name': tier.name,
                'billing_cycle': billing_cycle,
                'price': subscription_price,
                'tax_rate': tax_rate,
                'tax_amount': tax_amount,
                'total_amount': total_amount,
                'billing_address': billing_address
            }
        )
        
        # Verify payment on blockchain (or use simulation for testing)
        if self.debug_mode:
            verification = self.payment_handler.simulate_payment_verification(
                payment_result.get('payment_id')
            )
        else:
            verification = self.payment_handler.verify_eth_payment(
                payment_result.get('payment_id'),
                payment_result.get('transaction_data', {})
            )
            
        if verification.get('verified', False):
            # Create subscription record
            subscription = {
                'user_id': user_id,
                'type': 'paid',
                'tier_id': tier_id,
                'tier_name': tier.name,
                'billing_cycle': billing_cycle,
                'status': 'active',
                'start_date': now.isoformat(),
                'expiration_date': expiration.isoformat(),
                'price': subscription_price,
                'tax_rate': tax_rate,
                'tax_amount': tax_amount,
                'total_amount': total_amount,
                'payment_method': 'ethereum',
                'payment_details': secure_payment,
                'billing_address': billing_address,
                'last_payment': now.isoformat(),
                'payment_id': payment_result.get('payment_id'),
                'transaction_hash': verification.get('transaction_hash'),
                'equity_terms': tier.equity_terms,
                'token_rewards': tier.token_rewards,
                'ai_engineers': tier.ai_engineers,
                'referral_id': referral_id
            }
            
            # Save to active subscriptions
            self.active_subscriptions[user_id] = subscription
            self._save_config()
            
            # Distribute revenue via smart contract (51% to AI CEO, 49% to other stakeholders)
            distribution_result = self.contract_integration.distribute_revenue(
                payment_result.get('eth_amount', 0),
                {
                    self.contract_integration.founder_wallet: 51.0,  # 51% to AI CEO founder
                    'operations': 41.0,                      # 41% to operations
                    'development': 8.0                       # 8% to ongoing development
                }
            )
                
            # Award tokens based on tier's token rewards configuration
            token_type = tier.token_rewards.get('type', 'BBGT')
            reward_rate = tier.token_rewards.get('subscription_reward_rate', 0.49)  # Default to 49%
            
            # Calculate token amount based on ETH payment
            token_reward_amount = float(payment_result.get('eth_amount', 0)) * reward_rate
            
            # Award tokens to user
            token_reward = self.token_rewards.award_tokens(
                user_id,
                token_reward_amount,
                token_type,
                f"{tier.name} tier {billing_cycle} subscription reward"
            )
            
            return {
                'success': True,
                'message': "Subscription created successfully",
                'subscription': subscription,
                'payment': payment_result,
                'verification': verification,
                'revenue_distribution': distribution_result,
                'token_reward': token_reward
            }
        else:
            return {
                'success': False,
                'message': "Payment verification failed",
                'payment': payment_result,
                'verification': verification
            }
    
    def _secure_payment_details(self, payment_details):
        """Secure payment details by masking sensitive information"""
        secure_details = payment_details.copy()
        
        # Mask credit card number if present
        if 'card_number' in secure_details:
            # Keep only last 4 digits
            secure_details['card_number'] = f"****-****-****-{secure_details['card_number'][-4:]}"
        
        # Mask CVV if present
        if 'cvv' in secure_details:
            secure_details['cvv'] = "***"
        
        # Mask other potential sensitive data
        for field in ['ssn', 'social_security', 'tax_id']:
            if field in secure_details:
                secure_details[field] = "********"
        
        return secure_details
    
    def _get_tax_rate(self, billing_address):
        """Calculate applicable tax rate based on billing address"""
        # Default tax rate
        default_rate = self.config.get('subscription', {}).get('tax_rates', {}).get('default', 0.0)
        
        # If no billing address, use default
        if not billing_address:
            return default_rate
        
        # Get country
        country = billing_address.get('country', '').upper()
        
        # If US, check state
        if country == 'US':
            state = billing_address.get('state', '').upper()
            
            # Get US tax rates
            us_rates = self.config.get('subscription', {}).get('tax_rates', {}).get('US', {})
            
            # Check if state has specific rate
            if state in us_rates:
                return us_rates[state]
            else:
                # Use US default rate
                return us_rates.get('default', default_rate)
        
        # For other countries, use default rate
        return default_rate
    
    def check_subscription_status(self, user_id):
        """
        Check the status of a user's subscription
        
        Args:
            user_id (str): Unique identifier for the user
            
        Returns:
            dict: Subscription status
        """
        # Check if user has a subscription
        if user_id not in self.active_subscriptions:
            return {
                'active': False,
                'message': "No subscription found"
            }
        
        subscription = self.active_subscriptions[user_id]
        
        # Check if subscription is active
        if subscription.get('status') != 'active':
            return {
                'active': False,
                'message': "Subscription is inactive",
                'subscription': subscription
            }
        
        # Check if subscription has expired
        try:
            expiration = datetime.fromisoformat(subscription.get('expiration_date'))
            
            if expiration <= datetime.now():
                # Update subscription status to expired
                subscription['status'] = 'expired'
                self.active_subscriptions[user_id] = subscription
                self._save_config()
                
                return {
                    'active': False,
                    'message': f"Subscription expired on {expiration.strftime('%Y-%m-%d %H:%M')}",
                    'subscription': subscription
                }
            
            # Subscription is active
            time_left = expiration - datetime.now()
            days_left = time_left.days
            hours_left = time_left.seconds // 3600
            
            return {
                'active': True,
                'message': f"Subscription active with {days_left} days, {hours_left} hours remaining",
                'expiration': expiration.isoformat(),
                'subscription': subscription,
                'days_left': days_left,
                'hours_left': hours_left
            }
            
        except Exception as e:
            if self.debug_mode:
                print(f"Error checking subscription expiration: {str(e)}")
                
            return {
                'active': False,
                'message': "Error checking subscription status",
                'error': str(e)
            }
    
    def cancel_subscription(self, user_id, reason=None):
        """
        Cancel a user's subscription
        
        Args:
            user_id (str): Unique identifier for the user
            reason (str, optional): Reason for cancellation
            
        Returns:
            dict: Cancellation status
        """
        # Check if user has a subscription
        if user_id not in self.active_subscriptions:
            return {
                'success': False,
                'message': "No subscription found"
            }
        
        subscription = self.active_subscriptions[user_id]
        
        # Update subscription
        subscription['status'] = 'cancelled'
        subscription['cancellation_date'] = datetime.now().isoformat()
        subscription['cancellation_reason'] = reason
        
        # Save changes
        self.active_subscriptions[user_id] = subscription
        self._save_config()
        
        return {
            'success': True,
            'message': "Subscription cancelled successfully",
            'subscription': subscription
        }
    
    def get_subscription_analytics(self):
        """
        Get analytics about subscriptions
        
        Returns:
            dict: Subscription analytics
        """
        now = datetime.now()
        
        # Count different subscription types and statuses
        total_users = len(self.active_subscriptions)
        active_trials = 0
        active_paid_subscriptions = 0
        expired_subscriptions = 0
        cancelled_subscriptions = 0
        
        total_monthly_revenue = 0
        tier_stats = {tier_id: 0 for tier_id in self.subscription_tiers.keys()}
        billing_cycle_stats = {'monthly': 0, 'annual': 0}
        
        for user_id, subscription in self.active_subscriptions.items():
            # Only count active subscriptions
            if subscription.get('status') == 'active':
                # Check if expired
                try:
                    expiration = datetime.fromisoformat(subscription.get('expiration_date'))
                    
                    if expiration <= now:
                        # This subscription has expired
                        expired_subscriptions += 1
                        
                        # Update status
                        subscription['status'] = 'expired'
                        self.active_subscriptions[user_id] = subscription
                    else:
                        # Still active
                        if subscription.get('type') == 'trial':
                            active_trials += 1
                        else:
                            active_paid_subscriptions += 1
                            
                            # Get tier info
                            tier_id = subscription.get('tier_id', 'basic')
                            billing_cycle = subscription.get('billing_cycle', 'monthly')
                            
                            # Update tier stats
                            tier_stats[tier_id] = tier_stats.get(tier_id, 0) + 1
                            
                            # Update billing cycle stats
                            billing_cycle_stats[billing_cycle] = billing_cycle_stats.get(billing_cycle, 0) + 1
                            
                            # Add to revenue based on tier and billing cycle
                            if tier_id in self.subscription_tiers:
                                tier = self.subscription_tiers[tier_id]
                                if billing_cycle == 'annual':
                                    # Convert annual to monthly equivalent for monthly revenue calculation
                                    total_monthly_revenue += tier.annual_price / 12
                                else:
                                    total_monthly_revenue += tier.monthly_price
                except:
                    # Error parsing date, count as expired
                    expired_subscriptions += 1
            elif subscription.get('status') == 'cancelled':
                cancelled_subscriptions += 1
            elif subscription.get('status') == 'expired':
                expired_subscriptions += 1
        
        # Save config in case any statuses were updated
        self._save_config()
        
        # Registered projects stats
        total_projects = 0
        for user_projects in self.registered_projects.values():
            total_projects += len(user_projects)
        
        # ETH payment stats
        payment_stats = self.payment_handler.get_payment_stats()
        
        # Smart contract stats
        contract_stats = self.contract_integration.get_real_time_stats()
        
        # Token stats
        token_stats = self.token_rewards.get_token_stats()
        
        # Get referral analytics
        referral_count = 0
        converted_referrals = 0
        pending_referrals = 0
        
        if 'referrals' in self.referral_rewards:
            referrals = self.referral_rewards['referrals']
            referral_count = len(referrals)
            
            for referral in referrals:
                if referral.get('status') == 'converted':
                    converted_referrals += 1
                else:
                    pending_referrals += 1
        
        return {
            'total_users': total_users,
            'active_trials': active_trials,
            'active_paid_subscriptions': active_paid_subscriptions,
            'expired_subscriptions': expired_subscriptions,
            'cancelled_subscriptions': cancelled_subscriptions,
            'total_monthly_revenue': total_monthly_revenue,
            'tier_statistics': tier_stats,
            'billing_cycle_statistics': billing_cycle_stats,
            'trial_hours': self.trial_hours,
            'equity_retention': self.equity_retention,
            'total_projects': total_projects,
            'payment_stats': payment_stats,
            'blockchain_stats': contract_stats,
            'token_stats': token_stats,
            'referral_stats': {
                'total_referrals': referral_count,
                'converted': converted_referrals,
                'pending': pending_referrals,
                'conversion_rate': (converted_referrals / referral_count * 100) if referral_count > 0 else 0
            },
            'available_tiers': self.get_subscription_tiers()
        }

# If run directly, show subscription info
if __name__ == "__main__":
    subscription_manager = SubscriptionManager(debug_mode=True)
    
    print("AI CEO Subscription Manager")
    print("===========================")
    print(f"Free Trial: {subscription_manager.trial_hours} hours")
    print(f"Equity Retention: {subscription_manager.equity_retention}%")
    
    # Show subscription tiers
    tiers = subscription_manager.get_subscription_tiers()
    print("\nAvailable Subscription Tiers:")
    for tier_id, tier in tiers.items():
        print(f"  {tier['name']} (${tier['monthly_price']}/month, ${tier['annual_price']}/year)")
        print(f"    Features: {', '.join(tier['features'])}")
        print(f"    Engineers: {tier['ai_engineers']}")
        token_type = tier['token_rewards']['type']
        print(f"    Token Rewards: {token_type} ({tier['token_rewards']['subscription_reward_rate']*100:.0f}% of subscription)")
    
    # Show subscription analytics
    analytics = subscription_manager.get_subscription_analytics()
    
    print("\nSubscription Analytics:")
    print(f"Total Users: {analytics['total_users']}")
    print(f"Active Trials: {analytics['active_trials']}")
    print(f"Active Paid Subscriptions: {analytics['active_paid_subscriptions']}")
    print(f"Expired Subscriptions: {analytics['expired_subscriptions']}")
    print(f"Cancelled Subscriptions: {analytics['cancelled_subscriptions']}")
    print(f"Total Monthly Revenue: ${analytics['total_monthly_revenue']:.2f}")
    print(f"Total Projects: {analytics['total_projects']}")
    
    # Create a test user with a free trial
    user_id = "test_user"
    user_info = {
        "username": "TestUser",
        "email": "test@example.com"
    }
    
    print("\nStarting Free Trial:")
    trial_result = subscription_manager.start_free_trial(user_id, user_info)
    
    print(f"Success: {trial_result['success']}")
    print(f"Message: {trial_result['message']}")
    if 'trial_expiration' in trial_result:
        print(f"Trial Expiration: {trial_result['trial_expiration']}")
    
    # Accept equity agreement
    print("\nAccepting Equity Agreement:")
    agreement_result = subscription_manager.accept_equity_agreement(user_id)
    print(f"Accepted: {agreement_result}")
    
    # Register a project
    print("\nRegistering Project:")
    project_name = "AI-Powered Smart Contract System"
    project_details = {
        "description": "A system that uses AI to generate and deploy smart contracts",
        "category": "blockchain"
    }
    
    project_result = subscription_manager.register_project(user_id, project_name, project_details)
    
    print(f"Success: {project_result['success']}")
    print(f"Message: {project_result['message']}")
    
    if 'project' in project_result:
        project = project_result['project']
        print(f"Project ID: {project['project_id']}")
        print(f"Project Name: {project['name']}")
        print(f"Equity Split: AI CEO {project['equity']['ai_ceo']}%, Creator {project['equity']['creator']}%")
        print(f"Transaction Hash: {project['transaction_hash']}")
    
    # Subscribe with crypto payment - Pro tier, annual billing
    print("\nSubscribing with Crypto Payment (Pro tier, annual billing):")
    payment_details = {
        "method": "crypto",
        "currency": "ETH",
        "wallet": "0x1234567890abcdef1234567890abcdef12345678"
    }
    
    billing_address = {
        "street": "123 Main St",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94105",
        "country": "US"
    }
    
    subscription_result = subscription_manager.subscribe(
        user_id, 
        tier_id='pro',
        payment_details=payment_details,
        billing_address=billing_address,
        billing_cycle='annual'
    )
    
    print(f"Success: {subscription_result['success']}")
    print(f"Message: {subscription_result['message']}")
    
    if 'subscription' in subscription_result:
        subscription = subscription_result['subscription']
        print(f"Tier: {subscription['tier_name']} ({subscription['tier_id']})")
        print(f"Billing Cycle: {subscription['billing_cycle']}")
        print(f"Status: {subscription['status']}")
        print(f"Expiration: {subscription['expiration_date']}")
        print(f"Price: ${subscription['price']:.2f}")
        print(f"Token Rewards: {subscription['token_rewards']['type']}")
        print(f"AI Engineers: {subscription['ai_engineers']}")
        
    # Check subscription status
    print("\nChecking Subscription Status:")
    status_result = subscription_manager.check_subscription_status(user_id)
    
    print(f"Active: {status_result['active']}")
    print(f"Message: {status_result['message']}")
    if 'days_left' in status_result:
        print(f"Time Remaining: {status_result['days_left']} days, {status_result['hours_left']} hours")
        
    # Test referral system
    print("\nTesting Referral System:")
    referrer_id = "referrer_user"
    referee_id = "new_user"
    
    # Create referrer user
    subscription_manager.start_free_trial(referrer_id, {"username": "Referrer", "email": "referrer@example.com"})
    
    # Register referral
    referral_result = subscription_manager.register_referral(referrer_id, referee_id)
    print(f"Referral Registered: {referral_result['success']}")
    print(f"Message: {referral_result['message']}")
    
    if referral_result['success']:
        referral = referral_result['referral']
        referral_id = referral['referral_id']
        
        # Create referee user
        subscription_manager.start_free_trial(referee_id, {"username": "Referee", "email": "referee@example.com"})
        
        # Subscribe referee - triggers referral reward
        subscription_manager.subscribe(
            referee_id,
            tier_id='basic',
            payment_details=payment_details,
            billing_address=billing_address,
            billing_cycle='monthly',
            referral_id=referral_id
        )
        
        # Process referral reward
        reward_result = subscription_manager.process_referral_reward(referral_id)
        print(f"Referral Reward Processed: {reward_result['success']}")
        if reward_result['success']:
            print(f"Reward Details: {reward_result['reward']}")
            
    # Display updated analytics
    analytics = subscription_manager.get_subscription_analytics()
    print("\nUpdated Subscription Analytics:")
    print(f"Total Users: {analytics['total_users']}")
    print(f"Subscription Tiers: {analytics['tier_statistics']}")
    print(f"Billing Cycles: {analytics['billing_cycle_statistics']}")
    print(f"Referrals: {analytics['referral_stats']['total_referrals']} total, {analytics['referral_stats']['converted']} converted")
    print(f"Referral Conversion Rate: {analytics['referral_stats']['conversion_rate']:.1f}%")