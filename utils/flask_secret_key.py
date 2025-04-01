"""Utilities for secure secret key generation and management for Flask applications.

This module provides functions to create and manage a cryptographically secure secret key
that's stored in a file with appropriate permissions. The secret key is essential for
Flask session security and other cryptographic operations.
"""

import os
import secrets

# File where the secret key will be stored
SECRET_KEY_FILE = "flask_secret.key"

def ensure_secret_key():
    """Ensure a secret key exists by generating one if it doesn't.
    
    Creates a new cryptographically secure random key if the key file doesn't exist.
    Sets strict file permissions (read/write only by owner) for security.
    
    Raises:
        OSError: If there are issues creating or writing to the key file.
    """
    if not os.path.exists(SECRET_KEY_FILE):
        # Generate a 32-byte (256-bit) random hex string
        key = secrets.token_hex(32)
        
        # Write the key to file with restricted permissions
        with open(SECRET_KEY_FILE, "w") as f:
            f.write(key)
        
        # Set file permissions to owner read/write only (600)
        os.chmod(SECRET_KEY_FILE, 0o600)

def load_secret_key():
    """Load the secret key from the designated file.
    
    Returns:
        str: The secret key content.
        
    Raises:
        FileNotFoundError: If the key file doesn't exist (should call ensure_secret_key first).
        IOError: If there are issues reading the key file.
    """
    with open(SECRET_KEY_FILE, "r") as f:
        return f.read().strip()