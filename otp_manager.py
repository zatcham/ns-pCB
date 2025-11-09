"""
ns-pCB (number station - project Cherry Blossom)
OTP Management Module - Object-Oriented Implementation
Developed by Zach Matcham (zatcham)
Version 1.0 | 2025

This module provides OOP-based OTP (One-Time Pad) management with support for:
- Multi-user OTP tracking
- Single-use OTP validation
- OTP reuse with warnings
- Comprehensive CSV-based status tracking
"""

import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple


class OTPStatus:
    """Represents the status of a single OTP."""
    
    def __init__(self, otp_id: str, user: Optional[str] = None, 
                 used: bool = False, timestamp: Optional[str] = None,
                 reused: bool = False):
        """
        Initialize an OTP status object.
        
        Args:
            otp_id: Unique identifier for the OTP
            user: Username who used the OTP
            used: Whether the OTP has been used
            timestamp: ISO format timestamp of last usage
            reused: Whether the OTP has been reused
        """
        self.otp_id: str = otp_id
        self.user: Optional[str] = user
        self.used: bool = used
        self.timestamp: Optional[str] = timestamp
        self.reused: bool = reused
    
    def to_dict(self) -> Dict[str, str]:
        """Convert OTP status to dictionary for CSV storage."""
        return {
            'otp_id': self.otp_id,
            'user': self.user or '',
            'used': str(self.used),
            'timestamp': self.timestamp or '',
            'reused': str(self.reused)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'OTPStatus':
        """Create OTP status from dictionary loaded from CSV."""
        return cls(
            otp_id=data['otp_id'],
            user=data['user'] if data['user'] else None,
            used=data['used'].lower() == 'true',
            timestamp=data['timestamp'] if data['timestamp'] else None,
            reused=data['reused'].lower() == 'true'
        )


class OTPManager:
    """Manages OTP lifecycle including issuance, validation, and reuse tracking."""
    
    def __init__(self, status_file: str = 'otp/otp_status.csv'):
        """
        Initialize the OTP Manager.
        
        Args:
            status_file: Path to CSV file for OTP status tracking
        """
        self.status_file: str = status_file
        self._ensure_status_file()
    
    def _ensure_status_file(self) -> None:
        """Ensure the OTP status file exists with proper headers."""
        Path(self.status_file).parent.mkdir(parents=True, exist_ok=True)
        
        if not os.path.exists(self.status_file):
            with open(self.status_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['otp_id', 'user', 'used', 'timestamp', 'reused'])
                writer.writeheader()
    
    def _load_status(self) -> Dict[str, OTPStatus]:
        """
        Load all OTP statuses from the CSV file.
        
        Returns:
            Dictionary mapping OTP IDs to OTPStatus objects
        """
        statuses: Dict[str, OTPStatus] = {}
        
        if not os.path.exists(self.status_file):
            return statuses
        
        with open(self.status_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                status = OTPStatus.from_dict(row)
                statuses[status.otp_id] = status
        
        return statuses
    
    def _save_status(self, statuses: Dict[str, OTPStatus]) -> None:
        """
        Save all OTP statuses to the CSV file.
        
        Args:
            statuses: Dictionary mapping OTP IDs to OTPStatus objects
        """
        with open(self.status_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['otp_id', 'user', 'used', 'timestamp', 'reused'])
            writer.writeheader()
            for status in statuses.values():
                writer.writerow(status.to_dict())
    
    def issue_otp(self, user: str) -> str:
        """
        Issue a new unused OTP to a user.
        
        Args:
            user: Username to assign the OTP to
            
        Returns:
            The OTP ID that was issued
            
        Raises:
            RuntimeError: If no unused OTPs are available
        """
        statuses = self._load_status()
        
        # Find the first unused OTP or generate a new one
        otp_id = self._find_or_generate_otp(statuses)
        
        # Mark as used
        timestamp = datetime.now().isoformat()
        statuses[otp_id] = OTPStatus(otp_id=otp_id, user=user, used=True, 
                                      timestamp=timestamp, reused=False)
        
        self._save_status(statuses)
        return otp_id
    
    def _find_or_generate_otp(self, statuses: Dict[str, OTPStatus]) -> str:
        """
        Find an unused OTP or generate a new OTP ID.
        
        Args:
            statuses: Current OTP statuses
            
        Returns:
            An unused OTP ID
        """
        # Check for existing unused OTPs
        for otp_id, status in statuses.items():
            if not status.used:
                return otp_id
        
        # Generate new OTP ID
        existing_ids = [int(otp_id.replace('OTP', '')) for otp_id in statuses.keys() 
                       if otp_id.startswith('OTP')]
        next_num = max(existing_ids) + 1 if existing_ids else 1
        return f'OTP{next_num:03d}'
    
    def validate_otp(self, otp_id: str) -> bool:
        """
        Check if an OTP is unused and valid.
        
        Args:
            otp_id: OTP ID to validate
            
        Returns:
            True if OTP is unused, False otherwise
        """
        statuses = self._load_status()
        
        if otp_id not in statuses:
            # OTP not in system yet, consider it valid
            return True
        
        return not statuses[otp_id].used
    
    def get_otp_user(self, otp_id: str) -> Optional[str]:
        """
        Get the user who used a specific OTP.
        
        Args:
            otp_id: OTP ID to query
            
        Returns:
            Username who used the OTP, or None if unused or not found
        """
        statuses = self._load_status()
        
        if otp_id in statuses:
            return statuses[otp_id].user
        
        return None
    
    def reuse_otp(self, otp_id: str, user: str) -> bool:
        """
        Mark an OTP as reused by a user.
        
        Args:
            otp_id: OTP ID to reuse
            user: Username reusing the OTP
            
        Returns:
            True if successfully marked as reused, False if OTP not found
        """
        statuses = self._load_status()
        
        if otp_id not in statuses:
            return False
        
        timestamp = datetime.now().isoformat()
        statuses[otp_id].user = user
        statuses[otp_id].timestamp = timestamp
        statuses[otp_id].reused = True
        
        self._save_status(statuses)
        return True
    
    def get_otp_info(self, otp_id: str) -> Optional[OTPStatus]:
        """
        Get complete information about an OTP.
        
        Args:
            otp_id: OTP ID to query
            
        Returns:
            OTPStatus object or None if not found
        """
        statuses = self._load_status()
        return statuses.get(otp_id)
    
    def list_all_otps(self) -> List[OTPStatus]:
        """
        Get a list of all OTPs in the system.
        
        Returns:
            List of all OTPStatus objects
        """
        statuses = self._load_status()
        return list(statuses.values())
    
    def clear_otp_status(self) -> None:
        """Clear all OTP usage status (reset all OTPs to unused)."""
        # Remove existing file and recreate with just headers
        if os.path.exists(self.status_file):
            os.remove(self.status_file)
        self._ensure_status_file()


# Module-level functions for backward compatibility
_default_manager: Optional[OTPManager] = None


def _get_manager() -> OTPManager:
    """Get or create the default OTP manager instance."""
    global _default_manager
    if _default_manager is None:
        _default_manager = OTPManager()
    return _default_manager


def issue_otp(user: str) -> str:
    """Issue a new OTP to a user (convenience function)."""
    return _get_manager().issue_otp(user)


def validate_otp(otp_id: str) -> bool:
    """Validate if an OTP is unused (convenience function)."""
    return _get_manager().validate_otp(otp_id)


def get_otp_user(otp_id: str) -> Optional[str]:
    """Get the user who used an OTP (convenience function)."""
    return _get_manager().get_otp_user(otp_id)


def reuse_otp(otp_id: str, user: str) -> bool:
    """Mark an OTP as reused (convenience function)."""
    return _get_manager().reuse_otp(otp_id, user)
