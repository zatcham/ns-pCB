"""
ns-pCB (number station - project Cherry Blossom)
OTP Manager Unit Tests
Version 1.0 | 2025

Unit tests for the OTP management module.
"""

import unittest
import os
import tempfile
import shutil
from pathlib import Path
from otp_manager import OTPManager, OTPStatus, issue_otp, validate_otp, get_otp_user, reuse_otp


class TestOTPStatus(unittest.TestCase):
    """Test cases for OTPStatus class."""
    
    def test_otp_status_initialization(self):
        """Test OTPStatus object initialization."""
        status = OTPStatus(otp_id='OTP001', user='alice', used=True, 
                          timestamp='2025-01-01T12:00:00', reused=False)
        
        self.assertEqual(status.otp_id, 'OTP001')
        self.assertEqual(status.user, 'alice')
        self.assertTrue(status.used)
        self.assertEqual(status.timestamp, '2025-01-01T12:00:00')
        self.assertFalse(status.reused)
    
    def test_otp_status_defaults(self):
        """Test OTPStatus with default values."""
        status = OTPStatus(otp_id='OTP002')
        
        self.assertEqual(status.otp_id, 'OTP002')
        self.assertIsNone(status.user)
        self.assertFalse(status.used)
        self.assertIsNone(status.timestamp)
        self.assertFalse(status.reused)
    
    def test_otp_status_to_dict(self):
        """Test conversion of OTPStatus to dictionary."""
        status = OTPStatus(otp_id='OTP003', user='bob', used=True, 
                          timestamp='2025-01-02T10:30:00', reused=True)
        
        result = status.to_dict()
        
        self.assertEqual(result['otp_id'], 'OTP003')
        self.assertEqual(result['user'], 'bob')
        self.assertEqual(result['used'], 'True')
        self.assertEqual(result['timestamp'], '2025-01-02T10:30:00')
        self.assertEqual(result['reused'], 'True')
    
    def test_otp_status_from_dict(self):
        """Test creation of OTPStatus from dictionary."""
        data = {
            'otp_id': 'OTP004',
            'user': 'charlie',
            'used': 'true',
            'timestamp': '2025-01-03T14:45:00',
            'reused': 'false'
        }
        
        status = OTPStatus.from_dict(data)
        
        self.assertEqual(status.otp_id, 'OTP004')
        self.assertEqual(status.user, 'charlie')
        self.assertTrue(status.used)
        self.assertEqual(status.timestamp, '2025-01-03T14:45:00')
        self.assertFalse(status.reused)


class TestOTPManager(unittest.TestCase):
    """Test cases for OTPManager class."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.status_file = os.path.join(self.test_dir, 'otp_status.csv')
        self.manager = OTPManager(status_file=self.status_file)
    
    def tearDown(self):
        """Clean up after each test."""
        # Remove temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_manager_initialization(self):
        """Test OTPManager initialization creates status file."""
        self.assertTrue(os.path.exists(self.status_file))
    
    def test_issue_otp(self):
        """Test issuing a new OTP to a user."""
        otp_id = self.manager.issue_otp('bob')
        
        self.assertEqual(otp_id, 'OTP001')
        self.assertFalse(self.manager.validate_otp('OTP001'))
    
    def test_issue_multiple_otps(self):
        """Test issuing multiple OTPs generates sequential IDs."""
        otp1 = self.manager.issue_otp('alice')
        otp2 = self.manager.issue_otp('bob')
        otp3 = self.manager.issue_otp('charlie')
        
        self.assertEqual(otp1, 'OTP001')
        self.assertEqual(otp2, 'OTP002')
        self.assertEqual(otp3, 'OTP003')
    
    def test_validate_otp_unused(self):
        """Test validating an unused OTP returns True."""
        # New OTP should be valid (unused)
        self.assertTrue(self.manager.validate_otp('OTP999'))
    
    def test_validate_otp_used(self):
        """Test validating a used OTP returns False."""
        otp_id = self.manager.issue_otp('alice')
        
        # After issuing, OTP should be marked as used
        self.assertFalse(self.manager.validate_otp(otp_id))
    
    def test_get_otp_user(self):
        """Test retrieving the user who used an OTP."""
        self.manager.issue_otp('alice')
        self.manager.issue_otp('bob')
        
        user1 = self.manager.get_otp_user('OTP001')
        user2 = self.manager.get_otp_user('OTP002')
        
        self.assertEqual(user1, 'alice')
        self.assertEqual(user2, 'bob')
    
    def test_get_otp_user_nonexistent(self):
        """Test getting user for non-existent OTP returns None."""
        user = self.manager.get_otp_user('OTP999')
        self.assertIsNone(user)
    
    def test_reuse_otp(self):
        """Test marking an OTP as reused."""
        # First issue an OTP
        otp_id = self.manager.issue_otp('alice')
        
        # Now reuse it with a different user
        result = self.manager.reuse_otp(otp_id, 'bob')
        
        self.assertTrue(result)
        self.assertEqual(self.manager.get_otp_user(otp_id), 'bob')
        
        # Check that reused flag is set
        otp_info = self.manager.get_otp_info(otp_id)
        self.assertTrue(otp_info.reused)
    
    def test_reuse_nonexistent_otp(self):
        """Test reusing a non-existent OTP returns False."""
        result = self.manager.reuse_otp('OTP999', 'alice')
        self.assertFalse(result)
    
    def test_get_otp_info(self):
        """Test retrieving complete OTP information."""
        otp_id = self.manager.issue_otp('alice')
        
        info = self.manager.get_otp_info(otp_id)
        
        self.assertIsNotNone(info)
        self.assertEqual(info.otp_id, otp_id)
        self.assertEqual(info.user, 'alice')
        self.assertTrue(info.used)
        self.assertIsNotNone(info.timestamp)
        self.assertFalse(info.reused)
    
    def test_list_all_otps(self):
        """Test listing all OTPs in the system."""
        self.manager.issue_otp('alice')
        self.manager.issue_otp('bob')
        self.manager.issue_otp('charlie')
        
        all_otps = self.manager.list_all_otps()
        
        self.assertEqual(len(all_otps), 3)
        otp_ids = [otp.otp_id for otp in all_otps]
        self.assertIn('OTP001', otp_ids)
        self.assertIn('OTP002', otp_ids)
        self.assertIn('OTP003', otp_ids)
    
    def test_clear_otp_status(self):
        """Test clearing all OTP status."""
        self.manager.issue_otp('alice')
        self.manager.issue_otp('bob')
        
        self.manager.clear_otp_status()
        
        # After clearing, file should exist but be empty (only headers)
        self.assertTrue(os.path.exists(self.status_file))
        all_otps = self.manager.list_all_otps()
        self.assertEqual(len(all_otps), 0)
    
    def test_persistence(self):
        """Test that OTP status persists across manager instances."""
        # Issue OTPs with first manager
        self.manager.issue_otp('alice')
        self.manager.issue_otp('bob')
        
        # Create a new manager with same status file
        new_manager = OTPManager(status_file=self.status_file)
        
        # Check that OTPs are still there
        all_otps = new_manager.list_all_otps()
        self.assertEqual(len(all_otps), 2)
        
        user1 = new_manager.get_otp_user('OTP001')
        user2 = new_manager.get_otp_user('OTP002')
        self.assertEqual(user1, 'alice')
        self.assertEqual(user2, 'bob')


class TestModuleFunctions(unittest.TestCase):
    """Test cases for module-level convenience functions."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        # Create temporary test directory
        self.test_dir = tempfile.mkdtemp()
        self.status_file = os.path.join(self.test_dir, 'otp_status.csv')
        
        # Initialize module-level manager with test file
        import otp_manager
        otp_manager._default_manager = OTPManager(status_file=self.status_file)
    
    def tearDown(self):
        """Clean up after each test."""
        # Reset module-level manager
        import otp_manager
        otp_manager._default_manager = None
        
        # Remove temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_issue_otp_function(self):
        """Test module-level issue_otp function."""
        otp_id = issue_otp('alice')
        self.assertEqual(otp_id, 'OTP001')
    
    def test_validate_otp_function(self):
        """Test module-level validate_otp function."""
        otp_id = issue_otp('bob')
        self.assertFalse(validate_otp(otp_id))
        self.assertTrue(validate_otp('OTP999'))
    
    def test_get_otp_user_function(self):
        """Test module-level get_otp_user function."""
        issue_otp('charlie')
        user = get_otp_user('OTP001')
        self.assertEqual(user, 'charlie')
    
    def test_reuse_otp_function(self):
        """Test module-level reuse_otp function."""
        otp_id = issue_otp('alice')
        result = reuse_otp(otp_id, 'bob')
        self.assertTrue(result)
        self.assertEqual(get_otp_user(otp_id), 'bob')


if __name__ == '__main__':
    unittest.main()
