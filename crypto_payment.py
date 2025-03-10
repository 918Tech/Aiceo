"""
AI CEO Management System - Crypto Payment Handler
Manages cryptocurrency payments for the AI CEO subscription service
"""

import os
import json
import uuid
import hashlib
import datetime
from datetime import datetime, timedelta
import requests

class CryptoPaymentHandler:
    """
    Handles cryptocurrency payments for the AI CEO subscription service
    Specifically processes Ethereum payments to the founder's wallet
    """
    
    def __init__(self, config_file="ai_ceo_config.json", debug_mode=False):
        """Initialize the crypto payment handler"""
        self.config_file = config_file
        self.debug_mode = debug_mode
        self.config = self._load_config()
        
        # Get ETH wallet address from config
        self.eth_wallet = self.config.get('subscription', {}).get('payment_details', {}).get(
            'eth_wallet', '0xE93480549a181cc19708277ad0cAbCB99C53eC99'
        )
        
        # Load or initialize payment records
        self.payment_records = self._load_payment_records()
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            if self.debug_mode:
                print(f"Error loading config: {str(e)}")
            return {}
    
    def _load_payment_records(self):
        """Load payment records from file"""
        payment_file = 'crypto_payments.json'
        try:
            if os.path.exists(payment_file):
                with open(payment_file, 'r') as f:
                    return json.load(f)
            else:
                # Initialize payment records
                records = {
                    "payments": [],
                    "stats": {
                        "total_eth_paid": 0.0,
                        "total_usd_value": 0.0,
                        "last_payment_date": None
                    }
                }
                
                # Save initial records
                with open(payment_file, 'w') as f:
                    json.dump(records, f, indent=4)
                    
                return records
                
        except Exception as e:
            if self.debug_mode:
                print(f"Error loading payment records: {str(e)}")
            return {
                "payments": [],
                "stats": {
                    "total_eth_paid": 0.0,
                    "total_usd_value": 0.0,
                    "last_payment_date": None
                }
            }
    
    def _save_payment_records(self):
        """Save payment records to file"""
        payment_file = 'crypto_payments.json'
        try:
            with open(payment_file, 'w') as f:
                json.dump(self.payment_records, f, indent=4)
            return True
        except Exception as e:
            if self.debug_mode:
                print(f"Error saving payment records: {str(e)}")
            return False
    
    def get_eth_price(self):
        """
        Get current ETH price in USD
        Uses a public API to get price data
        """
        try:
            # Use CoinGecko API (no API key required for basic usage)
            response = requests.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('ethereum', {}).get('usd', 0)
            else:
                if self.debug_mode:
                    print(f"Error getting ETH price: {response.status_code}")
                # Fallback price for demo purposes
                return 3000.0
                
        except Exception as e:
            if self.debug_mode:
                print(f"Error getting ETH price: {str(e)}")
            # Fallback price for demo purposes
            return 3000.0
    
    def calculate_eth_amount(self, usd_amount):
        """
        Calculate ETH amount based on USD amount
        
        Args:
            usd_amount (float): Amount in USD
            
        Returns:
            float: Equivalent amount in ETH
        """
        eth_price = self.get_eth_price()
        
        if eth_price <= 0:
            if self.debug_mode:
                print("Invalid ETH price, using fallback")
            eth_price = 3000.0
            
        eth_amount = usd_amount / eth_price
        return eth_amount
    
    def generate_payment_request(self, user_id, usd_amount, subscription_details):
        """
        Generate a crypto payment request
        
        Args:
            user_id (str): User ID
            usd_amount (float): Amount in USD
            subscription_details (dict): Subscription details
            
        Returns:
            dict: Payment request details
        """
        eth_amount = self.calculate_eth_amount(usd_amount)
        eth_price = self.get_eth_price()
        
        # Generate payment ID
        payment_id = str(uuid.uuid4())
        
        # Format ETH amount to 6 decimal places (standard for ETH)
        eth_amount_formatted = "{:.6f}".format(eth_amount)
        
        # Current timestamp
        timestamp = datetime.now().isoformat()
        
        # Generate payment memo for verification
        # This would be used to verify the payment on the blockchain
        payment_memo = hashlib.sha256(
            f"{payment_id}:{user_id}:{eth_amount_formatted}:{timestamp}".encode()
        ).hexdigest()[:10]
        
        # Create payment request
        payment_request = {
            "payment_id": payment_id,
            "user_id": user_id,
            "wallet_address": self.eth_wallet,
            "usd_amount": usd_amount,
            "eth_amount": eth_amount_formatted,
            "eth_price_at_request": eth_price,
            "payment_memo": payment_memo,
            "timestamp": timestamp,
            "status": "pending",
            "subscription_details": subscription_details
        }
        
        # Save to payment records
        self.payment_records["payments"].append(payment_request)
        self._save_payment_records()
        
        return payment_request
    
    def record_payment(self, payment_id, transaction_hash):
        """
        Record a completed payment
        
        Args:
            payment_id (str): Payment request ID
            transaction_hash (str): Blockchain transaction hash
            
        Returns:
            dict: Updated payment record
        """
        # Find the payment record
        for payment in self.payment_records["payments"]:
            if payment["payment_id"] == payment_id:
                # Update payment status
                payment["status"] = "completed"
                payment["transaction_hash"] = transaction_hash
                payment["completed_at"] = datetime.now().isoformat()
                
                # Update stats
                eth_amount = float(payment["eth_amount"])
                usd_amount = payment["usd_amount"]
                
                self.payment_records["stats"]["total_eth_paid"] += eth_amount
                self.payment_records["stats"]["total_usd_value"] += usd_amount
                self.payment_records["stats"]["last_payment_date"] = payment["completed_at"]
                
                # Save updated records
                self._save_payment_records()
                
                return payment
        
        # If payment not found
        return None
    
    def process_subscription_payment(self, user_id, subscription_details):
        """
        Process a subscription payment in ETH
        
        Args:
            user_id (str): User ID
            subscription_details (dict): Subscription details
            
        Returns:
            dict: Payment request details
        """
        # Get subscription fee from config
        subscription_fee = self.config.get('subscription', {}).get('monthly_fee', 49.99)
        
        # Generate payment request
        payment_request = self.generate_payment_request(
            user_id,
            subscription_fee,
            subscription_details
        )
        
        return payment_request
    
    def get_payment_status(self, payment_id):
        """
        Get status of a payment
        
        Args:
            payment_id (str): Payment request ID
            
        Returns:
            dict: Payment status
        """
        # In a real implementation, this would check the blockchain
        # For this demo, we'll simulate payment verification
        
        for payment in self.payment_records["payments"]:
            if payment["payment_id"] == payment_id:
                return {
                    "payment_id": payment["payment_id"],
                    "status": payment["status"],
                    "wallet_address": payment["wallet_address"],
                    "eth_amount": payment["eth_amount"],
                    "usd_amount": payment["usd_amount"],
                    "created_at": payment["timestamp"],
                    "completed_at": payment.get("completed_at")
                }
        
        return {"error": "Payment not found"}
    
    def get_payment_stats(self):
        """
        Get payment statistics
        
        Returns:
            dict: Payment statistics
        """
        stats = self.payment_records["stats"].copy()
        
        # Add additional stats
        stats["total_payments"] = len([p for p in self.payment_records["payments"] if p["status"] == "completed"])
        stats["pending_payments"] = len([p for p in self.payment_records["payments"] if p["status"] == "pending"])
        stats["current_eth_price"] = self.get_eth_price()
        
        # Calculate current USD value of all ETH paid
        if stats["total_eth_paid"] > 0:
            stats["current_usd_value"] = stats["total_eth_paid"] * stats["current_eth_price"]
        else:
            stats["current_usd_value"] = 0
            
        return stats
    
    def verify_eth_payment(self, payment_id, transaction_data):
        """
        Verify an ETH payment based on transaction data
        
        Args:
            payment_id (str): Payment request ID
            transaction_data (dict): Transaction data from blockchain
            
        Returns:
            dict: Verification result
        """
        # This is a simplified version for demonstration
        # In a real implementation, this would verify the transaction on the Ethereum blockchain
        
        # Find the payment record
        payment = None
        for p in self.payment_records["payments"]:
            if p["payment_id"] == payment_id:
                payment = p
                break
                
        if not payment:
            return {"verified": False, "message": "Payment request not found"}
            
        # Check if already completed
        if payment["status"] == "completed":
            return {
                "verified": True, 
                "message": "Payment already verified",
                "transaction_hash": payment.get("transaction_hash")
            }
            
        # Basic verification checks
        # 1. Check destination address
        if transaction_data.get("to_address") != self.eth_wallet:
            return {"verified": False, "message": "Incorrect destination wallet"}
            
        # 2. Check amount (with some tolerance for gas fees)
        expected_amount = float(payment["eth_amount"])
        actual_amount = float(transaction_data.get("amount", 0))
        
        # Allow a 1% tolerance
        if actual_amount < expected_amount * 0.99:
            return {"verified": False, "message": "Insufficient payment amount"}
            
        # 3. Check transaction confirmation
        if transaction_data.get("confirmations", 0) < 3:
            return {"verified": False, "message": "Not enough confirmations yet"}
            
        # If passed all checks, record the payment
        transaction_hash = transaction_data.get("transaction_hash")
        self.record_payment(payment_id, transaction_hash)
        
        return {
            "verified": True,
            "message": "Payment successfully verified",
            "transaction_hash": transaction_hash
        }
    
    def simulate_payment_verification(self, payment_id):
        """
        Simulate payment verification for testing purposes
        
        Args:
            payment_id (str): Payment request ID
            
        Returns:
            dict: Verification result
        """
        # Find the payment record
        payment = None
        for p in self.payment_records["payments"]:
            if p["payment_id"] == payment_id:
                payment = p
                break
                
        if not payment:
            return {"verified": False, "message": "Payment request not found"}
            
        # Check if already completed
        if payment["status"] == "completed":
            return {
                "verified": True, 
                "message": "Payment already verified",
                "transaction_hash": payment.get("transaction_hash")
            }
            
        # Create a simulated transaction hash
        transaction_hash = "0x" + hashlib.sha256(f"simulated:{payment_id}:{datetime.now().isoformat()}".encode()).hexdigest()
        
        # Record the payment
        self.record_payment(payment_id, transaction_hash)
        
        return {
            "verified": True,
            "message": "Payment successfully verified (SIMULATED)",
            "transaction_hash": transaction_hash,
            "note": "This is a simulated payment for demonstration purposes"
        }

# If run directly, show some basic information
if __name__ == "__main__":
    payment_handler = CryptoPaymentHandler(debug_mode=True)
    
    print("AI CEO Crypto Payment Handler")
    print(f"Founder ETH Wallet: {payment_handler.eth_wallet}")
    
    eth_price = payment_handler.get_eth_price()
    print(f"Current ETH Price: ${eth_price:.2f} USD")
    
    subscription_fee = payment_handler.config.get('subscription', {}).get('monthly_fee', 49.99)
    eth_amount = payment_handler.calculate_eth_amount(subscription_fee)
    
    print(f"Monthly Subscription: ${subscription_fee:.2f} USD")
    print(f"Equivalent in ETH: {eth_amount:.6f} ETH")
    
    print("\nPayment Statistics:")
    stats = payment_handler.get_payment_stats()
    print(f"Total Payments: {stats['total_payments']}")
    print(f"Pending Payments: {stats['pending_payments']}")
    print(f"Total ETH Paid: {stats['total_eth_paid']:.6f} ETH")
    print(f"Total USD Value: ${stats['total_usd_value']:.2f} USD")
    print(f"Current USD Value: ${stats['current_usd_value']:.2f} USD")
    
    # Demonstrate generating a payment request
    user_id = "demo_user"
    subscription_details = {"plan": "monthly", "duration": 1}
    
    print("\nGenerating sample payment request...")
    payment_request = payment_handler.process_subscription_payment(user_id, subscription_details)
    
    print(f"Payment ID: {payment_request['payment_id']}")
    print(f"ETH Amount: {payment_request['eth_amount']} ETH")
    print(f"USD Amount: ${payment_request['usd_amount']:.2f} USD")
    print(f"Wallet Address: {payment_request['wallet_address']}")
    print(f"Payment Memo: {payment_request['payment_memo']}")
    
    # Simulate payment verification
    print("\nSimulating payment verification...")
    verification = payment_handler.simulate_payment_verification(payment_request['payment_id'])
    
    print(f"Verified: {verification['verified']}")
    print(f"Message: {verification['message']}")
    if 'transaction_hash' in verification:
        print(f"Transaction Hash: {verification['transaction_hash']}")
        
    print("\nUpdated Payment Statistics:")
    stats = payment_handler.get_payment_stats()
    print(f"Total Payments: {stats['total_payments']}")
    print(f"Pending Payments: {stats['pending_payments']}")
    print(f"Total ETH Paid: {stats['total_eth_paid']:.6f} ETH")
    print(f"Total USD Value: ${stats['total_usd_value']:.2f} USD")