"""
Encryption and decryption utilities.

This module provides:
- Symmetric encryption/decryption using Fernet
- Key derivation from passwords
- File encryption/decryption
- Secure key generation and management
"""

import base64
from pathlib import Path
from typing import Optional, Union
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
from app.core.config import settings
from app.core.exceptions.validation_exceptions import ValidationException


class EncryptionManager:
    """
    Encryption and decryption manager using Fernet (symmetric encryption).
    
    This class handles:
    - Data encryption and decryption
    - File encryption and decryption
    - Key derivation from passwords
    - Secure key generation
    """
    
    def __init__(self, key: Optional[bytes] = None):
        """
        Initialize encryption manager.
        
        Args:
            key: Encryption key (if None, derives from SECRET_KEY)
        """
        if key:
            self.key = key
        else:
            self.key = self._derive_key(settings.SECRET_KEY)
        
        self.cipher = Fernet(self.key)
    
    def _derive_key(
        self,
        password: str,
        salt: Optional[bytes] = None,
        iterations: int = 100000
    ) -> bytes:
        """
        Derive encryption key from password using PBKDF2.
        
        Args:
            password: Password to derive key from
            salt: Salt for key derivation (default: fixed salt)
            iterations: Number of iterations for PBKDF2
            
        Returns:
            Derived key suitable for Fernet
            
        Note:
            In production, use a random salt stored securely.
            The fixed salt here is for simplicity.
        """
        if salt is None:
            # WARNING: In production, use a random salt stored securely
            salt = b'hostel_management_encryption_salt_v1'
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
            backend=default_backend()
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt(self, data: Union[str, bytes]) -> str:
        """
        Encrypt data.
        
        Args:
            data: Data to encrypt (string or bytes)
            
        Returns:
            Base64-encoded encrypted data
            
        Raises:
            ValidationException: If encryption fails
            
        Example:
            >>> em = EncryptionManager()
            >>> encrypted = em.encrypt("sensitive data")
            >>> print(encrypted)  # Base64 encrypted string
        """
        try:
            if isinstance(data, str):
                data = data.encode()
            
            encrypted_data = self.cipher.encrypt(data)
            return base64.urlsafe_b64encode(encrypted_data).decode()
            
        except Exception as e:
            raise ValidationException(f"Encryption failed: {str(e)}")
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt data.
        
        Args:
            encrypted_data: Base64-encoded encrypted data
            
        Returns:
            Decrypted string
            
        Raises:
            ValidationException: If decryption fails
            
        Example:
            >>> em = EncryptionManager()
            >>> decrypted = em.decrypt(encrypted_data)
            >>> print(decrypted)  # Original data
        """
        try:
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.cipher.decrypt(decoded_data)
            return decrypted_data.decode()
            
        except InvalidToken:
            raise ValidationException("Invalid encryption token or corrupted data")
        except Exception as e:
            raise ValidationException(f"Decryption failed: {str(e)}")
    
    def encrypt_dict(self, data: dict) -> str:
        """
        Encrypt a dictionary by converting to JSON.
        
        Args:
            data: Dictionary to encrypt
            
        Returns:
            Encrypted JSON string
            
        Example:
            >>> em = EncryptionManager()
            >>> data = {"credit_card": "1234-5678-9012-3456"}
            >>> encrypted = em.encrypt_dict(data)
        """
        import json
        json_data = json.dumps(data)
        return self.encrypt(json_data)
    
    def decrypt_dict(self, encrypted_data: str) -> dict:
        """
        Decrypt data back to dictionary.
        
        Args:
            encrypted_data: Encrypted JSON string
            
        Returns:
            Decrypted dictionary
            
        Example:
            >>> em = EncryptionManager()
            >>> data = em.decrypt_dict(encrypted_data)
            >>> print(data["credit_card"])
        """
        import json
        decrypted_json = self.decrypt(encrypted_data)
        return json.loads(decrypted_json)
    
    def encrypt_file(
        self,
        input_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None
    ) -> Path:
        """
        Encrypt a file.
        
        Args:
            input_path: Path to file to encrypt
            output_path: Path for encrypted file (default: input_path.encrypted)
            
        Returns:
            Path to encrypted file
            
        Raises:
            ValidationException: If file encryption fails
            
        Example:
            >>> em = EncryptionManager()
            >>> encrypted_file = em.encrypt_file("sensitive.pdf")
        """
        try:
            input_path = Path(input_path)
            
            if output_path is None:
                output_path = input_path.with_suffix(input_path.suffix + '.encrypted')
            else:
                output_path = Path(output_path)
            
            # Read file
            with open(input_path, 'rb') as file:
                file_data = file.read()
            
            # Encrypt
            encrypted_data = self.cipher.encrypt(file_data)
            
            # Write encrypted file
            with open(output_path, 'wb') as file:
                file.write(encrypted_data)
            
            return output_path
            
        except Exception as e:
            raise ValidationException(f"File encryption failed: {str(e)}")
    
    def decrypt_file(
        self,
        input_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None
    ) -> Path:
        """
        Decrypt a file.
        
        Args:
            input_path: Path to encrypted file
            output_path: Path for decrypted file
            
        Returns:
            Path to decrypted file
            
        Raises:
            ValidationException: If file decryption fails
            
        Example:
            >>> em = EncryptionManager()
            >>> decrypted_file = em.decrypt_file("sensitive.pdf.encrypted")
        """
        try:
            input_path = Path(input_path)
            
            if output_path is None:
                # Remove .encrypted extension
                if input_path.suffix == '.encrypted':
                    output_path = input_path.with_suffix('')
                else:
                    output_path = input_path.with_suffix('.decrypted')
            else:
                output_path = Path(output_path)
            
            # Read encrypted file
            with open(input_path, 'rb') as file:
                encrypted_data = file.read()
            
            # Decrypt
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Write decrypted file
            with open(output_path, 'wb') as file:
                file.write(decrypted_data)
            
            return output_path
            
        except InvalidToken:
            raise ValidationException("Invalid encryption or corrupted file")
        except Exception as e:
            raise ValidationException(f"File decryption failed: {str(e)}")
    
    @staticmethod
    def generate_key() -> str:
        """
        Generate a new Fernet encryption key.
        
        Returns:
            Base64-encoded encryption key
            
        Example:
            >>> new_key = EncryptionManager.generate_key()
            >>> print(f"New encryption key: {new_key}")
        """
        return Fernet.generate_key().decode()
    
    @staticmethod
    def generate_key_from_password(
        password: str,
        salt: Optional[bytes] = None
    ) -> str:
        """
        Generate encryption key from password.
        
        Args:
            password: Password to derive key from
            salt: Salt for key derivation
            
        Returns:
            Base64-encoded encryption key
            
        Example:
            >>> key = EncryptionManager.generate_key_from_password("strong_password")
        """
        if salt is None:
            import os
            salt = os.urandom(16)
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key.decode()
    
    def rotate_key(self, new_key: bytes, data: str) -> str:
        """
        Re-encrypt data with a new key.
        
        Args:
            new_key: New encryption key
            data: Currently encrypted data
            
        Returns:
            Data encrypted with new key
            
        Example:
            >>> em = EncryptionManager()
            >>> new_key = Fernet.generate_key()
            >>> re_encrypted = em.rotate_key(new_key, old_encrypted_data)
        """
        # Decrypt with current key
        decrypted = self.decrypt(data)
        
        # Create new cipher with new key
        new_cipher = Fernet(new_key)
        
        # Encrypt with new key
        encrypted_data = new_cipher.encrypt(decrypted.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def encrypt_field(self, value: Optional[str]) -> Optional[str]:
        """
        Encrypt a database field value.
        
        Args:
            value: Field value to encrypt
            
        Returns:
            Encrypted value or None
            
        Example:
            >>> em = EncryptionManager()
            >>> encrypted_ssn = em.encrypt_field("123-45-6789")
        """
        if value is None:
            return None
        return self.encrypt(value)
    
    def decrypt_field(self, encrypted_value: Optional[str]) -> Optional[str]:
        """
        Decrypt a database field value.
        
        Args:
            encrypted_value: Encrypted field value
            
        Returns:
            Decrypted value or None
            
        Example:
            >>> em = EncryptionManager()
            >>> ssn = em.decrypt_field(encrypted_ssn)
        """
        if encrypted_value is None:
            return None
        
        try:
            return self.decrypt(encrypted_value)
        except Exception:
            return None


# Global encryption manager instance
encryption_manager = EncryptionManager()