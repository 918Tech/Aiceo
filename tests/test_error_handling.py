"""Tests for error handling system."""

import pytest
from utils.error_handler import (
    ErrorHandler,
    ConfigurationError,
    TokenManagementError,
    SubscriptionError,
    LegalComplianceError,
    dAppIntegrationError,
    require_valid_config,
    handle_errors
)
from utils.validators import (
    InputValidator,
    ValidationError,
    SubscriptionTier
)


class TestErrorHandler:
    """Test error handler functionality."""
    
    def test_logger_initialization(self):
        handler = ErrorHandler()
        assert handler.logger is not None
    
    def test_log_error(self, caplog):
        handler = ErrorHandler()
        error = Exception("Test error")
        handler.log_error(error, "test context")
        assert "Error in test context" in caplog.text
    
    def test_handle_exception_without_recovery(self):
        handler = ErrorHandler()
        error = ValueError("Test error")
        with pytest.raises(ValueError):
            handler.handle_exception(error, "test")
    
    def test_handle_exception_with_recovery(self):
        handler = ErrorHandler()
        error = ValueError("Test error")
        recovery_value = "recovered"
        result = handler.handle_exception(
            error,
            "test",
            recovery_fn=lambda: recovery_value
        )
        assert result == recovery_value


class TestInputValidator:
    """Test input validation."""
    
    def test_valid_email(self):
        assert InputValidator.validate_email("user@example.com")
    
    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            InputValidator.validate_email("invalid-email")
    
    def test_valid_ethereum_address(self):
        valid_addr = "0x" + "a" * 40
        assert InputValidator.validate_ethereum_address(valid_addr)
    
    def test_invalid_ethereum_address_format(self):
        with pytest.raises(ValidationError):
            InputValidator.validate_ethereum_address("0xinvalid")
    
    def test_invalid_ethereum_address_length(self):
        with pytest.raises(ValidationError):
            InputValidator.validate_ethereum_address("0x" + "a" * 38)
    
    def test_valid_token_amount(self):
        assert InputValidator.validate_token_amount(100.5)
    
    def test_invalid_token_amount_negative(self):
        with pytest.raises(ValidationError):
            InputValidator.validate_token_amount(-10)
    
    def test_invalid_token_amount_zero(self):
        with pytest.raises(ValidationError):
            InputValidator.validate_token_amount(0)
    
    def test_valid_subscription_config(self):
        config = {
            'tier': 'premium',
            'billing_cycle': 'monthly',
            'price': 99.99,
            'user_id': '0x' + 'a' * 40
        }
        assert InputValidator.validate_subscription_config(config)
    
    def test_missing_subscription_config_keys(self):
        config = {'tier': 'premium'}  # Missing other required keys
        with pytest.raises(ValidationError):
            InputValidator.validate_subscription_config(config)
    
    def test_invalid_subscription_tier(self):
        config = {
            'tier': 'invalid',
            'billing_cycle': 'monthly',
            'price': 99.99,
            'user_id': '0x' + 'a' * 40
        }
        with pytest.raises(ValidationError):
            InputValidator.validate_subscription_config(config)
    
    def test_valid_dapp_config(self):
        config = {
            'name': 'TestDApp',
            'contract_address': '0x' + 'b' * 40,
            'chain_id': 1
        }
        assert InputValidator.validate_dapp_config(config)
    
    def test_valid_legal_document(self):
        doc = {
            'type': 'TOS',
            'content': 'Terms of Service content here',
            'jurisdiction': 'US'
        }
        assert InputValidator.validate_legal_document(doc)
    
    def test_invalid_legal_document_type(self):
        doc = {
            'type': 'INVALID',
            'content': 'content',
            'jurisdiction': 'US'
        }
        with pytest.raises(ValidationError):
            InputValidator.validate_legal_document(doc)


class TestDecorators:
    """Test decorator functions."""
    
    def test_handle_errors_decorator(self):
        @handle_errors((ValueError,))
        def raises_value_error():
            raise ValueError("Test error")
        
        with pytest.raises(ValueError):
            raises_value_error()
    
    def test_require_valid_config_decorator(self):
        class TestClass:
            def __init__(self):
                self.config = {'key1': 'value1'}
            
            @require_valid_config(['key1'])
            def valid_method(self):
                return True
            
            @require_valid_config(['missing_key'])
            def invalid_method(self):
                return True
        
        obj = TestClass()
        assert obj.valid_method() is True
        
        with pytest.raises(ConfigurationError):
            obj.invalid_method()
