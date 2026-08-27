"""Input validation utilities for AI CEO System."""

from typing import Any, Dict, List, Optional
from enum import Enum
import re


class ValidationError(ValueError):
    """Raised when validation fails."""
    pass


class SubscriptionTier(Enum):
    """Valid subscription tiers."""
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class InputValidator:
    """Centralized input validation."""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError(f"Invalid email format: {email}")
        return True
    
    @staticmethod
    def validate_ethereum_address(address: str) -> bool:
        """Validate Ethereum address format."""
        if not isinstance(address, str):
            raise ValidationError("Address must be a string")
        if not address.startswith('0x'):
            raise ValidationError("Ethereum address must start with '0x'")
        if len(address) != 42:
            raise ValidationError("Ethereum address must be 42 characters")
        try:
            int(address, 16)
        except ValueError:
            raise ValidationError(f"Invalid Ethereum address: {address}")
        return True
    
    @staticmethod
    def validate_token_amount(amount: float) -> bool:
        """Validate token amount."""
        if not isinstance(amount, (int, float)):
            raise ValidationError("Token amount must be numeric")
        if amount <= 0:
            raise ValidationError("Token amount must be positive")
        if amount > 1e18:  # Reasonable upper limit
            raise ValidationError("Token amount exceeds maximum limit")
        return True
    
    @staticmethod
    def validate_subscription_config(config: Dict[str, Any]) -> bool:
        """Validate subscription configuration."""
        required_keys = {'tier', 'billing_cycle', 'price', 'user_id'}
        missing = required_keys - set(config.keys())
        if missing:
            raise ValidationError(f"Missing required keys: {missing}")
        
        # Validate tier
        valid_tiers = [t.value for t in SubscriptionTier]
        if config['tier'] not in valid_tiers:
            raise ValidationError(f"Invalid tier. Must be one of {valid_tiers}")
        
        # Validate billing cycle
        valid_cycles = {'monthly', 'annual'}
        if config['billing_cycle'] not in valid_cycles:
            raise ValidationError(f"Invalid billing cycle. Must be one of {valid_cycles}")
        
        # Validate price
        if not isinstance(config['price'], (int, float)) or config['price'] < 0:
            raise ValidationError("Price must be a non-negative number")
        
        InputValidator.validate_ethereum_address(config['user_id'])
        return True
    
    @staticmethod
    def validate_dapp_config(config: Dict[str, Any]) -> bool:
        """Validate dApp configuration."""
        required_keys = {'name', 'contract_address', 'chain_id'}
        missing = required_keys - set(config.keys())
        if missing:
            raise ValidationError(f"Missing dApp config keys: {missing}")
        
        if not isinstance(config['name'], str) or not config['name'].strip():
            raise ValidationError("dApp name must be a non-empty string")
        
        InputValidator.validate_ethereum_address(config['contract_address'])
        
        if not isinstance(config['chain_id'], int) or config['chain_id'] <= 0:
            raise ValidationError("chain_id must be a positive integer")
        
        return True
    
    @staticmethod
    def validate_legal_document(doc: Dict[str, Any]) -> bool:
        """Validate legal document structure."""
        required_keys = {'type', 'content', 'jurisdiction'}
        missing = required_keys - set(doc.keys())
        if missing:
            raise ValidationError(f"Missing legal doc keys: {missing}")
        
        valid_types = {'NDA', 'TOS', 'PRIVACY', 'COMPLIANCE'}
        if doc['type'] not in valid_types:
            raise ValidationError(f"Invalid doc type. Must be one of {valid_types}")
        
        if not isinstance(doc['content'], str) or not doc['content'].strip():
            raise ValidationError("Document content cannot be empty")
        
        return True
