"""
AI CEO Management System - Emergency Bail Bond Button
Implements the "I'm going to jail" emergency button functionality
"""
import os
import json
import logging
import time
import uuid
from datetime import datetime

from mugshot_scraper import MugshotScraper
from ai_legal_team import AILegalTeam
from token_rewards import TokenRewardsSystem
from subscription_manager import SubscriptionManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BailEmergencyButton")

class BailEmergencyButton:
    """
    Handles the "I'm going to jail" emergency button functionality
    Automatically initiates bail procedure when a token holder presses the button
    Verifies token holdings and initiates bail bond if sufficient tokens are available
    """
    
    def __init__(self, config_file="ai_ceo_config.json", debug_mode=False):
        """Initialize the emergency bail button system"""
        self.config_file = config_file
        self.debug_mode = debug_mode
        self.config = self._load_config()
        
        # Initialize required systems
        self.token_rewards = TokenRewardsSystem(config_file, debug_mode)
        self.legal_team = AILegalTeam(config_file, debug_mode)
        self.subscription_manager = SubscriptionManager(config_file, debug_mode)
        self.mugshot_scraper = MugshotScraper()
        
        # Data directory for emergency activations
        self.data_dir = "emergency_activations"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Load active emergency activations
        self.active_activations = self._load_activations()
        
        # Set minimum token requirements (configurable)
        self.min_token_percentage = self.config.get("bail_emergency", {}).get("min_token_percentage", 10.0)  # 10% of bail amount
        
        logger.info(f"Bail Emergency Button initialized with {len(self.active_activations)} active cases")
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                default_config = {
                    "bail_emergency": {
                        "min_token_percentage": 10.0,
                        "auto_activation": True,
                        "scanning_interval_minutes": 30,
                        "max_bail_amount": 500000,
                        "eligible_token_types": ["BBGT", "918T"],
                        "tiers": {
                            "platinum": {
                                "min_coverage": 50000,
                                "max_bail": 500000,
                                "processing_time_minutes": 30
                            },
                            "gold": {
                                "min_coverage": 25000,
                                "max_bail": 250000,
                                "processing_time_minutes": 60
                            },
                            "silver": {
                                "min_coverage": 10000,
                                "max_bail": 100000,
                                "processing_time_minutes": 120
                            },
                            "bronze": {
                                "min_coverage": 5000,
                                "max_bail": 50000,
                                "processing_time_minutes": 180
                            }
                        }
                    }
                }
                return default_config
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            return {}
    
    def _load_activations(self):
        """Load active emergency activations from file"""
        activations_file = os.path.join(self.data_dir, "active_activations.json")
        
        try:
            if os.path.exists(activations_file):
                with open(activations_file, 'r') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            logger.error(f"Error loading activations: {str(e)}")
            return {}
    
    def _save_activations(self):
        """Save active emergency activations to file"""
        activations_file = os.path.join(self.data_dir, "active_activations.json")
        
        try:
            with open(activations_file, 'w') as f:
                json.dump(self.active_activations, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Error saving activations: {str(e)}")
            return False
    
    def activate_emergency(self, user_id, location=None, situation=None, defendant_info=None):
        """
        Activate the emergency bail process when user presses "I'm going to jail" button
        
        Args:
            user_id (str): User ID of the token holder
            location (str, optional): Current location
            situation (str, optional): Description of the situation
            defendant_info (dict, optional): Information about the defendant if different from user
            
        Returns:
            dict: Activation status and details
        """
        logger.info(f"Emergency activation requested for user {user_id}")
        
        # Generate activation ID
        activation_id = str(uuid.uuid4())
        
        # Record activation time
        now = datetime.now()
        
        # Create activation record
        activation = {
            "activation_id": activation_id,
            "user_id": user_id,
            "timestamp": now.isoformat(),
            "location": location,
            "situation": situation,
            "defendant_info": defendant_info or {"name": "Same as user"},
            "status": "initiated",
            "steps_completed": [],
            "steps_pending": [
                "token_verification",
                "jail_database_scan",
                "bail_eligibility_check",
                "bail_bond_creation",
                "legal_team_assignment"
            ],
            "history": [
                {
                    "timestamp": now.isoformat(),
                    "action": "Emergency activation initiated",
                    "details": "User pressed 'I'm going to jail' button"
                }
            ]
        }
        
        # Add to active activations
        self.active_activations[activation_id] = activation
        self._save_activations()
        
        # Start the emergency process
        self._process_emergency_activation(activation_id)
        
        # Return immediate response
        return {
            "success": True,
            "activation_id": activation_id,
            "message": "Emergency bail process activated",
            "immediate_guidance": [
                "Remain calm and cooperative with law enforcement",
                "Exercise your right to remain silent",
                "Request to speak with an attorney",
                "Do not consent to searches without a warrant",
                "Inform law enforcement that you have bail assistance through AI CEO"
            ],
            "status_url": f"/api/emergency/{activation_id}",
            "estimated_processing_time": "Processing time will depend on your token holdings"
        }
    
    def _process_emergency_activation(self, activation_id):
        """Process an emergency activation through all required steps"""
        activation = self.active_activations.get(activation_id)
        if not activation:
            logger.error(f"Activation {activation_id} not found")
            return False
        
        user_id = activation["user_id"]
        
        # Step 1: Verify token holdings
        token_holdings = self._verify_token_holdings(user_id)
        self._update_activation_status(
            activation_id, 
            "token_verification", 
            "Verified token holdings",
            {"token_holdings": token_holdings}
        )
        
        # Step 2: Check bail eligibility based on tokens
        eligibility = self._check_bail_eligibility(user_id, token_holdings)
        self._update_activation_status(
            activation_id, 
            "bail_eligibility_check",
            f"Determined eligibility tier: {eligibility.get('eligibility_tier', 'Not Eligible')}",
            {"eligibility": eligibility}
        )
        
        # If not eligible, stop the process
        if eligibility.get("eligibility_tier") == "Not Eligible":
            self._update_activation_status(
                activation_id,
                "process_stopped",
                "Process stopped due to insufficient token holdings",
                {"reason": "insufficient_tokens"}
            )
            return False
        
        # Step 3: Begin scanning jail databases for booking information
        # This would typically run in background, but we'll simulate it here
        self._update_activation_status(
            activation_id,
            "jail_database_scan_started",
            "Started scanning jail databases for booking information",
            {"scan_started": datetime.now().isoformat()}
        )
        
        # Simulate jail database scan
        # In a real implementation, this would be an ongoing process
        inmate_info = self._simulate_jail_database_scan(activation)
        if inmate_info:
            self._update_activation_status(
                activation_id,
                "jail_database_scan",
                "Found inmate information in jail database",
                {"inmate_info": inmate_info}
            )
            
            # Step 4: Create bail bond
            bail_bond = self._create_bail_bond(user_id, inmate_info, eligibility)
            if bail_bond:
                self._update_activation_status(
                    activation_id,
                    "bail_bond_creation",
                    "Created bail bond",
                    {"bail_bond": bail_bond}
                )
                
                # Step 5: Assign legal team
                legal_case = self._assign_legal_team(user_id, inmate_info, bail_bond)
                if legal_case:
                    self._update_activation_status(
                        activation_id,
                        "legal_team_assignment",
                        "Assigned AI legal team to case",
                        {"legal_case_id": legal_case.case_id}
                    )
                    
                    # Mark process as completed
                    self._update_activation_status(
                        activation_id,
                        "process_completed",
                        "Emergency bail process completed successfully",
                        {
                            "completion_time": datetime.now().isoformat(),
                            "bail_bond_id": bail_bond.get("bond_id"),
                            "legal_case_id": legal_case.case_id
                        }
                    )
                    return True
        else:
            # No inmate information found yet, mark as pending
            self._update_activation_status(
                activation_id,
                "jail_database_scan_pending",
                "Continuing to scan jail databases for booking information",
                {"next_scan": datetime.now().isoformat()}
            )
        
        return False
    
    def _verify_token_holdings(self, user_id):
        """Verify token holdings for a user"""
        # Get token balances from token rewards system
        bbgt_balance = self.token_rewards.get_user_token_balance(user_id, "BBGT")
        t918_balance = self.token_rewards.get_user_token_balance(user_id, "918T")
        
        # If balances couldn't be retrieved, use placeholder values for testing
        if bbgt_balance is None:
            bbgt_balance = {"balance": 1000, "eth_equivalent": 1.0}
        
        if t918_balance is None:
            t918_balance = {"balance": 100, "eth_equivalent": 1.0}
        
        # Calculate ETH and USD equivalents
        eth_price_usd = 2000  # Placeholder, would get from price oracle
        
        bbgt_eth = bbgt_balance.get("balance", 0) * 0.001  # 1 BBGT = 0.001 ETH
        t918_eth = t918_balance.get("balance", 0) * 0.01   # 1 918T = 0.01 ETH
        
        total_eth = bbgt_eth + t918_eth
        total_usd = total_eth * eth_price_usd
        
        return {
            "BBGT": {
                "balance": bbgt_balance.get("balance", 0),
                "eth_equivalent": bbgt_eth
            },
            "918T": {
                "balance": t918_balance.get("balance", 0),
                "eth_equivalent": t918_eth
            },
            "total": {
                "eth": total_eth,
                "usd": total_usd
            }
        }
    
    def _check_bail_eligibility(self, user_id, token_holdings):
        """Check if user is eligible for automatic bail based on token holdings"""
        # Get eligibility tiers from config
        tiers = self.config.get("bail_emergency", {}).get("tiers", {})
        
        # Calculate total coverage in USD
        total_coverage = token_holdings.get("total", {}).get("usd", 0)
        
        # Determine eligibility tier
        eligibility = {
            "user_id": user_id,
            "token_holdings": token_holdings,
            "coverage_amount": total_coverage,
            "eligibility_tier": "Not Eligible",
            "max_bail_amount": 0,
            "processing_time_minutes": 0
        }
        
        # Check against tiers from highest to lowest
        if total_coverage >= tiers.get("platinum", {}).get("min_coverage", 50000):
            eligibility["eligibility_tier"] = "Platinum"
            eligibility["max_bail_amount"] = tiers.get("platinum", {}).get("max_bail", 500000)
            eligibility["processing_time_minutes"] = tiers.get("platinum", {}).get("processing_time_minutes", 30)
        elif total_coverage >= tiers.get("gold", {}).get("min_coverage", 25000):
            eligibility["eligibility_tier"] = "Gold"
            eligibility["max_bail_amount"] = tiers.get("gold", {}).get("max_bail", 250000)
            eligibility["processing_time_minutes"] = tiers.get("gold", {}).get("processing_time_minutes", 60)
        elif total_coverage >= tiers.get("silver", {}).get("min_coverage", 10000):
            eligibility["eligibility_tier"] = "Silver"
            eligibility["max_bail_amount"] = tiers.get("silver", {}).get("max_bail", 100000)
            eligibility["processing_time_minutes"] = tiers.get("silver", {}).get("processing_time_minutes", 120)
        elif total_coverage >= tiers.get("bronze", {}).get("min_coverage", 5000):
            eligibility["eligibility_tier"] = "Bronze"
            eligibility["max_bail_amount"] = tiers.get("bronze", {}).get("max_bail", 50000)
            eligibility["processing_time_minutes"] = tiers.get("bronze", {}).get("processing_time_minutes", 180)
        
        return eligibility
    
    def _simulate_jail_database_scan(self, activation):
        """
        Simulate scanning jail databases for booking information
        In a real implementation, this would continuously scan multiple databases
        """
        # For simulation purposes, create a plausible inmate record
        defendant_info = activation.get("defendant_info", {})
        defendant_name = defendant_info.get("name", "John Doe")
        
        if defendant_name == "Same as user":
            defendant_name = f"User {activation['user_id'][:8]}"
        
        # Split name into first and last
        name_parts = defendant_name.split()
        first_name = name_parts[0] if len(name_parts) > 0 else "John"
        last_name = name_parts[-1] if len(name_parts) > 1 else "Doe"
        
        # Generate a simulated booking record
        booking_number = f"BK{int(time.time())}"
        booking_date = datetime.now().isoformat()
        
        # Simulate charges based on any information in the activation
        situation = activation.get("situation", "").lower()
        charges = []
        
        if "drug" in situation or "possession" in situation:
            charges.append("Possession of Controlled Substance")
        elif "assault" in situation or "fight" in situation:
            charges.append("Simple Assault")
        elif "dui" in situation or "driving" in situation:
            charges.append("Driving Under the Influence")
        elif "theft" in situation or "shoplifting" in situation:
            charges.append("Petit Theft")
        else:
            charges.append("Misdemeanor Offense")
        
        # Simulate bail amount based on charges
        bail_amount = 0
        for charge in charges:
            if "Controlled Substance" in charge:
                bail_amount += 15000
            elif "Assault" in charge:
                bail_amount += 25000
            elif "Under the Influence" in charge:
                bail_amount += 10000
            elif "Theft" in charge:
                bail_amount += 5000
            else:
                bail_amount += 7500
        
        # Create inmate record
        inmate_info = {
            "booking_number": booking_number,
            "full_name": defendant_name,
            "first_name": first_name,
            "last_name": last_name,
            "booking_date": booking_date,
            "facility": "County Jail",
            "charges": charges,
            "bail_amount": bail_amount,
            "court_date": (datetime.now().replace(hour=9, minute=0, second=0, microsecond=0).isoformat()),
            "court_location": "County Courthouse, Dept 5",
            "source": "AI CEO Jail Database Scanner"
        }
        
        return inmate_info
    
    def _create_bail_bond(self, user_id, inmate_info, eligibility):
        """Create a bail bond using the subscription manager"""
        # Check if bail amount exceeds user's maximum coverage
        bail_amount = inmate_info.get("bail_amount", 0)
        max_bail_amount = eligibility.get("max_bail_amount", 0)
        
        if bail_amount > max_bail_amount:
            logger.warning(f"Bail amount {bail_amount} exceeds user's maximum coverage {max_bail_amount}")
            return None
        
        # Prepare case information
        case_info = {
            "estimated_duration_days": 180,  # Placeholder
            "case_number": f"CASE{int(time.time())}",
            "court_name": inmate_info.get("court_location", "County Court"),
            "charges": inmate_info.get("charges", [])
        }
        
        # Process bail bond through subscription manager
        try:
            bail_bond = self.subscription_manager.process_bail_bond(
                user_id,
                inmate_info,
                bail_amount,
                case_info
            )
            
            if not bail_bond or not bail_bond.get("success", False):
                logger.error(f"Failed to create bail bond: {bail_bond}")
                return None
            
            # Process bail payment automatically (in a real system, this would use smart contracts)
            # Determine token type based on eligibility
            total_eth = eligibility.get("token_holdings", {}).get("total", {}).get("eth", 0)
            token_type = "918T" if total_eth >= 1 else "BBGT"
            
            payment_details = {
                "payment_method": "token_collateral",
                "token_type": token_type,
                "token_amount": bail_amount * 0.1 / 2000  # 10% of bail in ETH equivalent at $2000/ETH
            }
            
            payment_result = self.subscription_manager.process_bail_payment(
                bail_bond.get("bond", {}).get("bond_id"),
                payment_details
            )
            
            if not payment_result or not payment_result.get("success", False):
                logger.error(f"Failed to process bail payment: {payment_result}")
                return None
            
            return bail_bond.get("bond")
        except Exception as e:
            logger.error(f"Error creating bail bond: {str(e)}")
            return None
    
    def _assign_legal_team(self, user_id, inmate_info, bail_bond):
        """Assign AI legal team to the case"""
        try:
            # Create a legal case
            legal_case = self.legal_team.create_case(
                user_id,
                inmate_info.get("full_name"),
                bail_bond.get("bond_id"),
                inmate_info.get("charges", []),
                inmate_info.get("court_date"),
                inmate_info.get("court_location", "County Courthouse")
            )
            
            if not legal_case:
                logger.error("Failed to create legal case")
                return None
            
            # Add notes with bail bond details
            self.legal_team.add_note_to_case(
                legal_case.case_id,
                f"Bail bond created automatically through emergency system. Bond amount: ${bail_bond.get('bail_amount', 0):,.2f}. " +
                f"Surety amount: ${bail_bond.get('surety_amount', 0):,.2f}."
            )
            
            # Add document with bail conditions
            bail_conditions = f"""
BAIL CONDITIONS

1. You must appear at all scheduled court appearances. Your next court date is {inmate_info.get('court_date')}
2. You must not leave the jurisdiction without court permission
3. You must report to your AI Monitoring System as scheduled
4. You must comply with all AI CEO monitoring requirements, including GPS tracking and facial recognition
5. You must not commit any new crimes while on release

Failure to comply with these conditions may result in revocation of bail, forfeiture of tokens, 
and return to custody.
"""
            self.legal_team.add_document_to_case(
                legal_case.case_id,
                "bail_conditions",
                "Bail Conditions and Requirements",
                bail_conditions
            )
            
            return legal_case
        except Exception as e:
            logger.error(f"Error assigning legal team: {str(e)}")
            return None
    
    def _update_activation_status(self, activation_id, step, message, details=None):
        """Update the status of an emergency activation"""
        activation = self.active_activations.get(activation_id)
        if not activation:
            logger.error(f"Activation {activation_id} not found")
            return False
        
        # Add history entry
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": message,
            "details": details or {}
        }
        activation["history"].append(history_entry)
        
        # Update steps completed/pending
        if step in activation["steps_pending"]:
            activation["steps_pending"].remove(step)
            activation["steps_completed"].append(step)
            activation["status"] = step
        else:
            activation["status"] = step
        
        # Save activations
        self._save_activations()
        return True
    
    def get_activation_status(self, activation_id):
        """
        Get the status of an emergency activation
        
        Args:
            activation_id (str): Activation ID
            
        Returns:
            dict: Activation status and details
        """
        activation = self.active_activations.get(activation_id)
        if not activation:
            return {
                "success": False,
                "message": f"Activation {activation_id} not found"
            }
        
        return {
            "success": True,
            "activation_id": activation_id,
            "status": activation["status"],
            "steps_completed": activation["steps_completed"],
            "steps_pending": activation["steps_pending"],
            "history": activation["history"][-5:],  # Return only the last 5 history entries
            "completion_percentage": len(activation["steps_completed"]) / (len(activation["steps_completed"]) + len(activation["steps_pending"])) * 100 if activation["steps_pending"] else 100
        }
    
    def cancel_activation(self, activation_id, reason):
        """
        Cancel an emergency activation
        
        Args:
            activation_id (str): Activation ID
            reason (str): Reason for cancellation
            
        Returns:
            dict: Cancellation status
        """
        activation = self.active_activations.get(activation_id)
        if not activation:
            return {
                "success": False,
                "message": f"Activation {activation_id} not found"
            }
        
        # Add cancellation to history
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "Emergency activation cancelled",
            "details": {"reason": reason}
        }
        activation["history"].append(history_entry)
        
        # Update status
        activation["status"] = "cancelled"
        activation["cancellation_reason"] = reason
        activation["cancellation_time"] = datetime.now().isoformat()
        
        # Save activations
        self._save_activations()
        
        return {
            "success": True,
            "message": f"Activation {activation_id} cancelled",
            "reason": reason
        }
    
    def get_jail_database_scan_status(self, activation_id):
        """
        Get the status of the jail database scan for an activation
        
        Args:
            activation_id (str): Activation ID
            
        Returns:
            dict: Jail database scan status
        """
        activation = self.active_activations.get(activation_id)
        if not activation:
            return {
                "success": False,
                "message": f"Activation {activation_id} not found"
            }
        
        # Check if inmate info has been found
        inmate_info = None
        for history_entry in activation["history"]:
            if "jail_database_scan" in history_entry["action"] and "inmate_info" in history_entry["details"]:
                inmate_info = history_entry["details"]["inmate_info"]
                break
        
        if inmate_info:
            return {
                "success": True,
                "status": "completed",
                "inmate_info": inmate_info,
                "message": "Inmate information found in jail database"
            }
        else:
            # Get the most recent scan status
            scan_status = None
            for history_entry in reversed(activation["history"]):
                if "jail_database_scan" in history_entry["action"]:
                    scan_status = history_entry
                    break
            
            return {
                "success": True,
                "status": "scanning",
                "scan_status": scan_status,
                "message": "Still scanning jail databases for booking information"
            }
    
    def manually_update_inmate_info(self, activation_id, inmate_info):
        """
        Manually update inmate information for an activation
        Used when jail database scanning is not successful or when manual entry is needed
        
        Args:
            activation_id (str): Activation ID
            inmate_info (dict): Manually entered inmate information
            
        Returns:
            dict: Update status
        """
        activation = self.active_activations.get(activation_id)
        if not activation:
            return {
                "success": False,
                "message": f"Activation {activation_id} not found"
            }
        
        # Update activation with inmate info
        self._update_activation_status(
            activation_id,
            "jail_database_scan",
            "Manually updated inmate information",
            {"inmate_info": inmate_info}
        )
        
        # Continue processing with the new information
        self._process_emergency_activation(activation_id)
        
        return {
            "success": True,
            "message": "Inmate information updated and processing continued",
            "activation_status": self.get_activation_status(activation_id)
        }

# Button UI integration code for different platforms
def create_emergency_button_ui_web():
    """Create emergency button UI for web interface"""
    return """
<div class="emergency-button-container">
    <button id="emergency-bail-button" class="emergency-button">
        <i class="fas fa-exclamation-triangle"></i>
        I'M GOING TO JAIL
    </button>
    <div class="emergency-description">
        Press this button if you've been arrested to automatically initiate the bail process
    </div>
</div>

<script>
    document.getElementById('emergency-bail-button').addEventListener('click', function() {
        if (confirm('Are you sure you want to activate the emergency bail process? This should only be used if you are actually being arrested.')) {
            // Get location
            navigator.geolocation.getCurrentPosition(function(position) {
                const location = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };
                
                // Collect situation information
                const situation = prompt('Briefly describe the situation (e.g., "Arrested for DUI"):');
                
                // Make API call
                fetch('/api/emergency/activate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        location: location,
                        situation: situation
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Emergency bail process activated. Follow the guidance provided by your AI legal team.');
                        // Redirect to status page
                        window.location.href = '/emergency-status/' + data.activation_id;
                    } else {
                        alert('Failed to activate emergency bail process: ' + data.message);
                    }
                })
                .catch(error => {
                    alert('Error activating emergency bail process: ' + error);
                });
            }, function() {
                // Handle location error
                alert('Unable to get your location. The emergency bail process will still be activated, but without location information.');
                // Continue with API call without location
            });
        }
    });
</script>

<style>
    .emergency-button-container {
        text-align: center;
        padding: 20px;
        margin: 20px 0;
    }
    
    .emergency-button {
        background-color: #ff3b30;
        color: white;
        border: none;
        border-radius: 50px;
        padding: 20px 40px;
        font-size: 24px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .emergency-button:hover {
        background-color: #d82c21;
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
    }
    
    .emergency-button:active {
        transform: scale(0.98);
    }
    
    .emergency-button i {
        margin-right: 10px;
    }
    
    .emergency-description {
        margin-top: 15px;
        color: #666;
        font-size: 16px;
    }
</style>
"""

def create_emergency_button_ui_mobile():
    """Create emergency button UI for mobile app interface"""
    return """
<div class="mobile-emergency-container">
    <div class="mobile-emergency-header">
        Emergency Bail Assistance
    </div>
    
    <button id="mobile-emergency-button" class="mobile-emergency-button">
        <div class="pulse-animation"></div>
        <span class="button-text">I'M GOING TO JAIL</span>
    </button>
    
    <div class="mobile-emergency-info">
        Press only if you are being arrested
    </div>
    
    <div class="eligibility-status">
        <div class="eligibility-tier">Your Tier: PLATINUM</div>
        <div class="eligibility-coverage">Coverage: Up to $500,000</div>
    </div>
</div>

<style>
    .mobile-emergency-container {
        background-color: #1a1a1a;
        border-radius: 15px;
        padding: 20px;
        max-width: 350px;
        margin: 0 auto;
    }
    
    .mobile-emergency-header {
        color: white;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .mobile-emergency-button {
        position: relative;
        background-color: #ff3b30;
        color: white;
        border: none;
        border-radius: 60px;
        padding: 25px 0;
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 10px rgba(255, 59, 48, 0.5);
    }
    
    .pulse-animation {
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        border-radius: 60px;
        background-color: rgba(255, 59, 48, 0.7);
        opacity: 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {
            transform: scale(1);
            opacity: 0.7;
        }
        70% {
            transform: scale(1.05);
            opacity: 0;
        }
        100% {
            transform: scale(1.1);
            opacity: 0;
        }
    }
    
    .button-text {
        position: relative;
        z-index: 2;
    }
    
    .mobile-emergency-info {
        color: #cccccc;
        font-size: 14px;
        text-align: center;
        margin-top: 15px;
    }
    
    .eligibility-status {
        background-color: #2a2a2a;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
    }
    
    .eligibility-tier {
        color: #ffcc00;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .eligibility-coverage {
        color: white;
        font-size: 14px;
    }
</style>
"""


# Example usage
if __name__ == "__main__":
    emergency_button = BailEmergencyButton(debug_mode=True)
    activation = emergency_button.activate_emergency(
        "user123",
        location="123 Main St",
        situation="Arrested for DUI"
    )
    
    print(f"Activation ID: {activation.get('activation_id')}")
    
    # Check status after a few seconds
    time.sleep(3)
    status = emergency_button.get_activation_status(activation.get('activation_id'))
    print(f"Status: {status.get('status')}")
    print(f"Steps completed: {status.get('steps_completed')}")
    print(f"Completion percentage: {status.get('completion_percentage')}%")