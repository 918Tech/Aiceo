"""Centralized error handling and logging for AI CEO System."""

import logging
import traceback
from typing import Any, Callable, Optional, Type
from functools import wraps
from datetime import datetime


class AICEOException(Exception):
    """Base exception for AI CEO System."""
    pass


class ConfigurationError(AICEOException):
    """Raised when configuration is invalid."""
    pass


class TokenManagementError(AICEOException):
    """Raised when token operations fail."""
    pass


class SubscriptionError(AICEOException):
    """Raised when subscription operations fail."""
    pass


class LegalComplianceError(AICEOException):
    """Raised when legal compliance checks fail."""
    pass


class dAppIntegrationError(AICEOException):
    """Raised when dApp integration fails."""
    pass


class ErrorHandler:
    """Centralized error handling and logging."""
    
    def __init__(self, log_file: str = "logs/aiceo.log"):
        self.log_file = log_file
        self.logger = self._setup_logger(log_file)
    
    def _setup_logger(self, log_file: str) -> logging.Logger:
        """Configure logging to file and console."""
        logger = logging.getLogger('AICEO')
        logger.setLevel(logging.DEBUG)
        
        # File handler
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not setup file logging: {e}")
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def log_error(self, error: Exception, context: str = "") -> None:
        """Log an error with full traceback."""
        self.logger.error(f"Error in {context}: {str(error)}")
        self.logger.debug(traceback.format_exc())
    
    def log_warning(self, message: str) -> None:
        """Log a warning."""
        self.logger.warning(message)
    
    def log_info(self, message: str) -> None:
        """Log info."""
        self.logger.info(message)
    
    def handle_exception(
        self,
        error: Exception,
        context: str = "",
        recovery_fn: Optional[Callable] = None
    ) -> Any:
        """Handle exception with optional recovery."""
        self.log_error(error, context)
        
        if recovery_fn:
            try:
                self.log_info(f"Attempting recovery for {context}")
                return recovery_fn()
            except Exception as recovery_error:
                self.log_error(recovery_error, f"{context} (recovery)")
                raise AICEOException(f"Failed to recover from {context}") from error
        
        raise error


def require_valid_config(required_keys: list[str]):
    """Decorator to validate configuration before function execution."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            handler = ErrorHandler()
            
            if not hasattr(self, 'config'):
                raise ConfigurationError("Configuration object not found")
            
            missing_keys = [key for key in required_keys if key not in self.config]
            
            if missing_keys:
                error_msg = f"Missing required configuration keys: {missing_keys}"
                raise ConfigurationError(error_msg)
            
            handler.log_info(f"Configuration validated for {func.__name__}")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def handle_errors(exception_types: tuple[Type[Exception], ...] = (Exception,)):
    """Decorator to catch and log errors gracefully."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            handler = ErrorHandler()
            try:
                return func(*args, **kwargs)
            except exception_types as e:
                handler.log_error(e, f"Function {func.__name__}")
                raise
        return wrapper
    return decorator
