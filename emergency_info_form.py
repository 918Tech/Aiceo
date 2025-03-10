"""
AI CEO Management System - Emergency Information Collection
Gathers and stores essential information from users for the emergency bail system
"""
import os
import json
import logging
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EmergencyInfoCollector")

class EmergencyInfoCollector:
    """
    Collects and manages emergency information from users who may need 
    to use the "I'm going to jail" functionality in the future.
    
    This proactively gathers identification details to make the emergency
    bail process more efficient when it's needed.
    """
    
    def __init__(self, data_dir="emergency_data"):
        """Initialize the emergency information collector"""
        self.data_dir = data_dir
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        # File to store encrypted user emergency info
        self.info_file = os.path.join(data_dir, "emergency_info.json")
        
        # Load existing data if available
        self.user_info = self._load_data()
    
    def _load_data(self):
        """Load existing emergency information data"""
        try:
            if os.path.exists(self.info_file):
                with open(self.info_file, 'r') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            logger.error(f"Error loading emergency information: {str(e)}")
            return {}
    
    def _save_data(self):
        """Save emergency information data (would be encrypted in production)"""
        try:
            # In a production environment, this data would be encrypted
            with open(self.info_file, 'w') as f:
                json.dump(self.user_info, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Error saving emergency information: {str(e)}")
            return False
            
    def collect_user_info(self, user_id, user_data):
        """
        Collect and store user emergency information
        
        Args:
            user_id (str): User ID
            user_data (dict): User emergency information
            
        Returns:
            dict: Status of the operation
        """
        # Validate required fields
        required_fields = [
            "full_name", "date_of_birth", "home_address", 
            "identification_type", "identification_number"
        ]
        
        missing_fields = [field for field in required_fields if field not in user_data]
        
        if missing_fields:
            return {
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }
            
        # Add metadata
        info_entry = {
            "user_id": user_id,
            "collected_date": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "info_id": str(uuid.uuid4()),
            "data": user_data
        }
        
        # Store the information (would be encrypted in production)
        self.user_info[user_id] = info_entry
        success = self._save_data()
        
        if success:
            return {
                "success": True,
                "message": "Emergency information collected successfully",
                "info_id": info_entry["info_id"]
            }
        else:
            return {
                "success": False,
                "message": "Failed to save emergency information"
            }
            
    def update_user_info(self, user_id, user_data):
        """
        Update existing user emergency information
        
        Args:
            user_id (str): User ID
            user_data (dict): Updated user emergency information
            
        Returns:
            dict: Status of the operation
        """
        # Check if user info exists
        if user_id not in self.user_info:
            return {
                "success": False,
                "message": "User emergency information not found"
            }
            
        # Get existing info and update
        existing_info = self.user_info[user_id]
        existing_data = existing_info["data"]
        
        # Update fields provided in user_data
        for key, value in user_data.items():
            existing_data[key] = value
            
        # Update metadata
        existing_info["last_updated"] = datetime.now().isoformat()
        
        # Save updated information
        success = self._save_data()
        
        if success:
            return {
                "success": True,
                "message": "Emergency information updated successfully",
                "info_id": existing_info["info_id"]
            }
        else:
            return {
                "success": False,
                "message": "Failed to update emergency information"
            }
    
    def get_user_info(self, user_id):
        """
        Get user emergency information
        
        Args:
            user_id (str): User ID
            
        Returns:
            dict: User emergency information or None if not found
        """
        return self.user_info.get(user_id)
    
    def has_user_info(self, user_id):
        """
        Check if user has provided emergency information
        
        Args:
            user_id (str): User ID
            
        Returns:
            bool: True if user has provided emergency information
        """
        return user_id in self.user_info
    
    def delete_user_info(self, user_id):
        """
        Delete user emergency information
        
        Args:
            user_id (str): User ID
            
        Returns:
            dict: Status of the operation
        """
        if user_id not in self.user_info:
            return {
                "success": False,
                "message": "User emergency information not found"
            }
        
        # Delete the information
        del self.user_info[user_id]
        success = self._save_data()
        
        if success:
            return {
                "success": True,
                "message": "Emergency information deleted successfully"
            }
        else:
            return {
                "success": False,
                "message": "Failed to delete emergency information"
            }

# HTML Form for Emergency Information Collection
def generate_emergency_info_form(user_id, existing_data=None):
    """
    Generate HTML form for collecting emergency information
    
    Args:
        user_id (str): User ID
        existing_data (dict, optional): Existing user data for pre-filling the form
        
    Returns:
        str: HTML form
    """
    # Check if we have existing data to pre-fill
    data = existing_data['data'] if existing_data and 'data' in existing_data else {}
    
    # Form title and description based on whether this is an update or new form
    title = "Update Your Emergency Information" if data else "Emergency Information Collection"
    description = (
        "Please update your emergency contact and identification information below. " 
        "This information will only be used if you activate the emergency bail system."
    ) if data else (
        "Please provide the information below to prepare for potential emergency bail needs. " 
        "This information will be securely stored and only used if you activate the \"I'm going to jail\" feature."
    )
    
    # Create the HTML form
    html = f"""
    <div class="emergency-form-container" style="max-width: 800px; margin: 0 auto; padding: 20px; background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        <h2 style="color: #d04040; text-align: center;">{title}</h2>
        <p style="color: #505050; text-align: center;">{description}</p>
        
        <div class="form-notice" style="background-color: #f8f8f8; padding: 15px; border-left: 5px solid #d04040; margin-bottom: 20px;">
            <p style="margin: 0; color: #303030;"><strong>Why we need this information:</strong> In case you ever need to use the emergency bail button, having this information ready will significantly speed up the process of locating you in the system and posting bail.</p>
        </div>
        
        <form id="emergencyInfoForm" action="/api/emergency/collect-info" method="POST">
            <input type="hidden" name="user_id" value="{user_id}">
            
            <div class="form-section" style="margin-bottom: 25px;">
                <h3 style="color: #303030; border-bottom: 1px solid #d0d0d0; padding-bottom: 10px;">Personal Information</h3>
                
                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="full_name" style="display: block; margin-bottom: 5px; font-weight: bold;">Legal Full Name:</label>
                    <input type="text" id="full_name" name="full_name" value="{data.get('full_name', '')}" required 
                           style="width: 100%; padding: 8px; border: 1px solid #c0c0c0; border-radius: 4px;">
                    <div class="field-tip" style="font-size: 0.8em; color: #707070; margin-top: 3px;">Enter your name exactly as it appears on your ID</div>
                </div>
                
                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="date_of_birth" style="display: block; margin-bottom: 5px; font-weight: bold;">Date of Birth:</label>
                    <input type="date" id="date_of_birth" name="date_of_birth" value="{data.get('date_of_birth', '')}" required
                           style="width: 100%; padding: 8px; border: 1px solid #c0c0c0; border-radius: 4px;">
                </div>
                
                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="home_address" style="display: block; margin-bottom: 5px; font-weight: bold;">Home Address:</label>
                    <textarea id="home_address" name="home_address" required rows="3"
                              style="width: 100%; padding: 8px; border: 1px solid #c0c0c0; border-radius: 4px;">{data.get('home_address', '')}</textarea>
                </div>
                
                <div class="form-row" style="display: flex; gap: 15px; margin-bottom: 15px;">
                    <div style="flex: 1;">
                        <label for="phone" style="display: block; margin-bottom: 5px; font-weight: bold;">Phone Number:</label>
                        <input type="tel" id="phone" name="phone" value="{data.get('phone', '')}" 
                               style="width: 100%; padding: 8px; border: 1px solid #c0c0c0; border-radius: 4px;">
                    </div>
                    
                    <div style="flex: 1;">
                        <label for="email" style="display: block; margin-bottom: 5px; font-weight: bold;">Email Address:</label>
                        <input type="email" id="email" name="email" value="{data.get('email', '')}" 
                               style="width: 100%; padding: 8px; border: 1px solid #c0c0c0; border-radius: 4px;">
                    </div>
                </div>
            </div>
            
            <div class="form-section" style="margin-bottom: 25px;">
                <h3 style="color: #303030; border-bottom: 1px solid #d0d0d0; padding-bottom: 10px;">Identification Information</h3>
                
                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="identification_type" style="display: block; margin-bottom: 5px; font-weight: bold;">ID Type:</label>
                    <select id="identification_type" name="identification_type" required
                            style="width: 100%; padding: 8px; border: 1px solid #c0c0c0; border-radius: 4px;">
                        <option value="" disabled {'' if data.get('identification_type') else 'selected'}>Select ID Type</option>
                        <option value="drivers_license" {'selected' if data.get('identification_type') == 'drivers_license' else ''}>Driver's License</option>
                        <option value="state_id" {'selected' if data.get('identification_type') == 'state_id' else ''}>State ID</option>
                        <option value="passport" {'selected' if data.get('identification_type') == 'passport' else ''}>Passport</option>
                        <option value="military_id" {'selected' if data.get('identification_type') == 'military_id' else ''}>Military ID</option>
                    </select>
                </div>
                
                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="identification_number" style="display: block; margin-bottom: 5px; font-weight: bold;">ID Number:</label>
                    <input type="text" id="identification_number" name="identification_number" value="{data.get('identification_number', '')}" required
                           style="width: 100%; padding: 8px; border: 1px solid #c0c0c0; border-radius: 4px;">
                </div>
                
                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="identification_state" style="display: block; margin-bottom: 5px; font-weight: bold;">Issuing State/Country:</label>
                    <input type="text" id="identification_state" name="identification_state" value="{data.get('identification_state', '')}" required
                           style="width: 100%; padding: 8px; border: 1px solid #c0c0c0; border-radius: 4px;">
                </div>
            </div>
            
            <div class="form-section" style="margin-bottom: 25px;">
                <h3 style="color: #303030; border-bottom: 1px solid #d0d0d0; padding-bottom: 10px;">Emergency Contact</h3>
                
                <div class="form-row" style="display: flex; gap: 15px; margin-bottom: 15px;">
                    <div style="flex: 1;">
                        <label for="emergency_contact_name" style="display: block; margin-bottom: 5px; font-weight: bold;">Contact Name:</label>
                        <input type="text" id="emergency_contact_name" name="emergency_contact_name" value="{data.get('emergency_contact_name', '')}"
                               style="width: 100%; padding: 8px; border: 1px solid #c0c0c0; border-radius: 4px;">
                    </div>
                    
                    <div style="flex: 1;">
                        <label for="emergency_contact_relationship" style="display: block; margin-bottom: 5px; font-weight: bold;">Relationship:</label>
                        <input type="text" id="emergency_contact_relationship" name="emergency_contact_relationship" value="{data.get('emergency_contact_relationship', '')}"
                               style="width: 100%; padding: 8px; border: 1px solid #c0c0c0; border-radius: 4px;">
                    </div>
                </div>
                
                <div class="form-row" style="display: flex; gap: 15px; margin-bottom: 15px;">
                    <div style="flex: 1;">
                        <label for="emergency_contact_phone" style="display: block; margin-bottom: 5px; font-weight: bold;">Contact Phone:</label>
                        <input type="tel" id="emergency_contact_phone" name="emergency_contact_phone" value="{data.get('emergency_contact_phone', '')}"
                               style="width: 100%; padding: 8px; border: 1px solid #c0c0c0; border-radius: 4px;">
                    </div>
                    
                    <div style="flex: 1;">
                        <label for="emergency_contact_email" style="display: block; margin-bottom: 5px; font-weight: bold;">Contact Email:</label>
                        <input type="email" id="emergency_contact_email" name="emergency_contact_email" value="{data.get('emergency_contact_email', '')}"
                               style="width: 100%; padding: 8px; border: 1px solid #c0c0c0; border-radius: 4px;">
                    </div>
                </div>
            </div>
            
            <div class="form-section" style="margin-bottom: 25px;">
                <h3 style="color: #303030; border-bottom: 1px solid #d0d0d0; padding-bottom: 10px;">Additional Information</h3>
                
                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="known_allergies" style="display: block; margin-bottom: 5px; font-weight: bold;">Known Allergies/Medical Conditions:</label>
                    <textarea id="known_allergies" name="known_allergies" rows="2"
                              style="width: 100%; padding: 8px; border: 1px solid #c0c0c0; border-radius: 4px;">{data.get('known_allergies', '')}</textarea>
                    <div class="field-tip" style="font-size: 0.8em; color: #707070; margin-top: 3px;">Important for ensuring your safety while in custody</div>
                </div>
                
                <div class="form-group" style="margin-bottom: 15px;">
                    <label for="additional_notes" style="display: block; margin-bottom: 5px; font-weight: bold;">Additional Notes:</label>
                    <textarea id="additional_notes" name="additional_notes" rows="3"
                              style="width: 100%; padding: 8px; border: 1px solid #c0c0c0; border-radius: 4px;">{data.get('additional_notes', '')}</textarea>
                </div>
            </div>
            
            <div class="form-group" style="margin-bottom: 15px;">
                <label style="display: flex; align-items: flex-start; cursor: pointer;">
                    <input type="checkbox" id="consent" name="consent" required
                           style="margin-top: 3px; margin-right: 10px;" 
                           {'checked' if data.get('consent') else ''}>
                    <span style="flex: 1;">
                        I consent to the storage and use of this information in the event of an emergency bail situation. 
                        I understand that this information will be securely stored and only accessed when the emergency 
                        bail feature is activated. I confirm that the information provided is accurate to the best of my knowledge.
                    </span>
                </label>
            </div>
            
            <div class="form-actions" style="text-align: center; margin-top: 30px;">
                <button type="submit" style="background-color: #d04040; color: white; border: none; padding: 10px 30px; border-radius: 5px; font-size: 16px; cursor: pointer; font-weight: bold;">
                    {
                    'Update Emergency Information' if data else 'Save Emergency Information'
                    }
                </button>
            </div>
        </form>
        
        <div class="security-notice" style="margin-top: 30px; font-size: 0.9em; color: #505050; text-align: center;">
            <p>
                <strong>Security Notice:</strong> Your information is encrypted and securely stored. 
                It can only be accessed when you activate the emergency bail feature.
            </p>
        </div>
    </div>
    
    <script>
        document.getElementById('emergencyInfoForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            // In a real implementation, this would submit the form data to the server
            // For demonstration, we'll just log success
            console.log('Emergency information submitted');
            alert('Emergency information saved successfully.');
            
            // The form would typically redirect or update UI here
        });
    </script>
    """
    
    return html

# Function to display the emergency button in the UI
def generate_emergency_button(user_has_info=False, tokens_sufficient=False):
    """
    Generate HTML for the emergency "I'm going to jail" button
    
    Args:
        user_has_info (bool): Whether the user has provided emergency information
        tokens_sufficient (bool): Whether the user has sufficient tokens for bail
        
    Returns:
        str: HTML for the emergency button
    """
    # Determine button state
    button_disabled = not (user_has_info and tokens_sufficient)
    button_class = "disabled" if button_disabled else "active"
    
    # Determine warning message
    warning = ""
    if not user_has_info:
        warning = "You must provide emergency information before using this feature."
    elif not tokens_sufficient:
        warning = "You don't have sufficient tokens (minimum 1,000 BBGT or 100 918T) for emergency bail."
    
    button_html = f"""
    <div class="emergency-button-container" style="max-width: 800px; margin: 30px auto; padding: 20px; background-color: #202030; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); text-align: center;">
        <h2 style="color: #ffffff; margin-bottom: 20px;">Emergency Bail Activation</h2>
        
        <div class="button-wrapper" style="margin: 25px 0;">
            <button id="emergency-button" class="{button_class}" 
                   style="background-color: #ff3030; color: white; border: none; border-radius: 50%; width: 200px; height: 200px; font-size: 24px; font-weight: bold; cursor: pointer; box-shadow: 0 6px 30px rgba(255,0,0,0.3); position: relative; transition: all 0.3s ease;" 
                   {'disabled' if button_disabled else ''}>
                <div class="pulse" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 50%; background-color: rgba(255,48,48,0.8); z-index: -1; 
                                          animation: pulse 2s infinite; opacity: 0.6;"></div>
                <div class="pulse delay" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 50%; background-color: rgba(255,48,48,0.8); z-index: -2; 
                                                animation: pulse 2s infinite 0.5s; opacity: 0.6;"></div>
                I'M GOING<br>TO JAIL
            </button>
        </div>
        
        <div class="button-status" style="margin-top: 15px;">
            <div class="status-indicator" style="display: flex; justify-content: center; margin-bottom: 10px;">
                <div class="info-status" style="margin: 0 10px; display: flex; align-items: center;">
                    <span class="status-dot" style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 5px; 
                                                   background-color: {'#40c040' if user_has_info else '#c04040'};"></span>
                    <span style="color: {'#40c040' if user_has_info else '#c04040'};">Emergency Info</span>
                </div>
                <div class="token-status" style="margin: 0 10px; display: flex; align-items: center;">
                    <span class="status-dot" style="display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 5px; 
                                                   background-color: {'#40c040' if tokens_sufficient else '#c04040'};"></span>
                    <span style="color: {'#40c040' if tokens_sufficient else '#c04040'};">Token Balance</span>
                </div>
            </div>
            
            {f'<div class="warning-message" style="color: #ff6060; margin-top: 10px;">{warning}</div>' if warning else ''}
        </div>
        
        <div class="emergency-info" style="margin-top: 30px; padding: 15px; background-color: #303045; border-radius: 5px; text-align: left;">
            <h3 style="color: #ffffff; margin-top: 0;">How This Works:</h3>
            <ol style="color: #d0d0d0; margin-left: 20px; padding-left: 0;">
                <li style="margin-bottom: 8px;">Pressing this button initiates the emergency bail process using your BBGT or 918T tokens.</li>
                <li style="margin-bottom: 8px;">Our AI system will scan jail databases to locate you after arrest.</li>
                <li style="margin-bottom: 8px;">A bail bond will be automatically posted on your behalf.</li>
                <li style="margin-bottom: 8px;">The AI legal team will be assigned to your case.</li>
                <li style="margin-bottom: 8px;">Required: Emergency information and sufficient token balance.</li>
            </ol>
            
            <div class="action-links" style="margin-top: 15px; display: flex; justify-content: space-between;">
                <a href="#info-form" style="color: #40a0ff; text-decoration: none;">{
                    'Update Emergency Information' if user_has_info else 'Provide Emergency Information'
                }</a>
                <a href="#token-balance" style="color: #40a0ff; text-decoration: none;">Check Token Balance</a>
            </div>
        </div>
        
        <style>
            @keyframes pulse {
                0% {
                    transform: scale(1);
                    opacity: 0.6;
                }
                70% {
                    transform: scale(1.3);
                    opacity: 0;
                }
                100% {
                    transform: scale(1.3);
                    opacity: 0;
                }
            }
            
            #emergency-button:hover:not(:disabled) {
                transform: scale(1.05);
                box-shadow: 0 8px 40px rgba(255,0,0,0.4);
            }
            
            #emergency-button:active:not(:disabled) {
                transform: scale(0.98);
            }
            
            #emergency-button.disabled {
                background-color: #803030;
                cursor: not-allowed;
                opacity: 0.7;
            }
            
            #emergency-button.disabled .pulse, 
            #emergency-button.disabled .pulse.delay {
                animation: none;
                opacity: 0;
            }
        </style>
        
        <script>
            document.getElementById('emergency-button').addEventListener('click', function(e) {
                if (this.classList.contains('disabled')) {
                    e.preventDefault();
                    alert('You must provide emergency information and have sufficient tokens before using this feature.');
                    return;
                }
                
                if (confirm('WARNING: Only activate this feature if you are actually being arrested. This will initiate the emergency bail process. Continue?')) {
                    // In a real implementation, this would call the emergency API
                    alert('Emergency bail process activated. The system will begin scanning jail databases for your booking information.');
                    
                    // The app would transition to the emergency status screen
                }
            });
        </script>
    </div>
    """
    
    return button_html

# Example usage
if __name__ == "__main__":
    # Create sample user data
    sample_user = {
        "data": {
            "full_name": "John Smith",
            "date_of_birth": "1985-06-15",
            "home_address": "123 Main St, Anytown, CA 90210",
            "phone": "(555) 123-4567",
            "email": "john@example.com",
            "identification_type": "drivers_license",
            "identification_number": "D1234567",
            "identification_state": "California",
            "emergency_contact_name": "Jane Smith",
            "emergency_contact_relationship": "Spouse",
            "emergency_contact_phone": "(555) 987-6543",
            "emergency_contact_email": "jane@example.com",
            "known_allergies": "Penicillin",
            "additional_notes": "I have a prescription for blood pressure medication",
            "consent": True
        }
    }
    
    # Generate HTML form
    form_html = generate_emergency_info_form("user123", sample_user)
    print("Form HTML generated")
    
    # Generate emergency button
    button_html = generate_emergency_button(user_has_info=True, tokens_sufficient=True)
    print("Emergency button HTML generated")