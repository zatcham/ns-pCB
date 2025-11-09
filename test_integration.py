"""
ns-pCB (number station - project Cherry Blossom)
Integration Tests
Version 1.0 | 2025

Integration tests for the complete ns-pCB system.
"""

import unittest
import os
import tempfile
import shutil
from pathlib import Path
from otp_manager import OTPManager
from nsCB_otpgen import OTPGenerator, generate_date_string


class TestOTPGenerationIntegration(unittest.TestCase):
    """Integration tests for OTP generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.otp_dir = os.path.join(self.test_dir, 'otp')
        os.makedirs(self.otp_dir)
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.test_dir)
    
    def test_generate_otps(self):
        """Test generating OTPs end-to-end."""
        generator = OTPGenerator()
        
        # Generate all OTPs
        result = generator.generate_all(with_output=False)
        self.assertTrue(result)
        
        # Check that dictionaries are populated
        self.assertEqual(len(generator.numbers.mappings), 10)
        self.assertEqual(len(generator.lowercase.mappings), 26)
        self.assertEqual(len(generator.uppercase.mappings), 26)
        
        # Check that all values are in valid range
        for value in generator.numbers.mappings.values():
            self.assertGreaterEqual(value, 100)
            self.assertLessEqual(value, 999)
    
    def test_export_otps_to_csv(self):
        """Test exporting OTPs to CSV files."""
        generator = OTPGenerator()
        generator.generate_all(with_output=False)
        
        date_str = generate_date_string()
        num_file, lc_file, uc_file = generator.export_to_csv(date_str, self.otp_dir)
        
        # Check that files were created
        self.assertTrue(os.path.exists(num_file))
        self.assertTrue(os.path.exists(lc_file))
        self.assertTrue(os.path.exists(uc_file))
        
        # Check that files have content
        self.assertGreater(os.path.getsize(num_file), 0)
        self.assertGreater(os.path.getsize(lc_file), 0)
        self.assertGreater(os.path.getsize(uc_file), 0)


class TestOTPManagerIntegration(unittest.TestCase):
    """Integration tests for OTP manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.status_file = os.path.join(self.test_dir, 'otp_status.csv')
        self.manager = OTPManager(status_file=self.status_file)
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.test_dir)
    
    def test_multi_user_workflow(self):
        """Test complete multi-user OTP workflow."""
        # User 1 gets an OTP
        otp1 = self.manager.issue_otp('alice')
        self.assertEqual(otp1, 'OTP001')
        
        # User 2 gets a different OTP
        otp2 = self.manager.issue_otp('bob')
        self.assertEqual(otp2, 'OTP002')
        
        # Validate that OTP1 is used
        self.assertFalse(self.manager.validate_otp(otp1))
        
        # Check who used OTP1
        self.assertEqual(self.manager.get_otp_user(otp1), 'alice')
        
        # User 3 tries to reuse OTP1
        result = self.manager.reuse_otp(otp1, 'charlie')
        self.assertTrue(result)
        
        # Check that OTP1 is now associated with charlie
        self.assertEqual(self.manager.get_otp_user(otp1), 'charlie')
        
        # Check that reused flag is set
        otp_info = self.manager.get_otp_info(otp1)
        self.assertTrue(otp_info.reused)


class TestCipherIntegration(unittest.TestCase):
    """Integration tests for cipher functionality."""
    
    def test_encode_decode_cycle(self):
        """Test encoding and decoding with tscipherlib."""
        from tscipherlib import CipherEngine
        
        engine = CipherEngine(key=12345)
        original_text = "hello world"
        
        # Encode
        encoded = engine.encode(original_text)
        self.assertIsInstance(encoded, list)
        self.assertEqual(len(encoded), len(original_text))
        
        # Decode
        decoded = engine.decode(encoded)
        self.assertEqual(decoded, original_text)
    
    def test_hex_encode_decode_cycle(self):
        """Test hex encoding and decoding."""
        from tscipherlib import cencodeh, cdecodeh
        
        original_text = "test message"
        key = 9876
        
        # Encode to hex
        encoded_hex = cencodeh(original_text, key)
        self.assertIsInstance(encoded_hex, str)
        
        # Decode from hex
        decoded = cdecodeh(encoded_hex, key)
        self.assertEqual(decoded, original_text)


if __name__ == '__main__':
    unittest.main()
