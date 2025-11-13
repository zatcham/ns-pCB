"""
ns-pCB (number station - project Cherry Blossom)
OTP Generation Module - Object-Oriented Implementation
Developed by Zach Matcham (zatcham)
Version 1.0 | 2025

This module provides OTP (One-Time Pad) generation with duplicate detection
and CSV export functionality.
"""

import time
from random import seed, randint
from datetime import datetime
from typing import Dict, List, Tuple
import pandas as pd


class RandomNumberGenerator:
    """Generates random numbers with time-based seeding."""
    
    @staticmethod
    def generate_seed() -> float:
        """
        Generate a random seed based on Unix time.
        
        Returns:
            Random seed value
        """
        unixtime = time.time()
        ran_time = randint(randint(2, 90000), randint(100001, 330920))
        
        if unixtime > ran_time:
            return unixtime - ran_time
        elif unixtime < ran_time:
            return ran_time - unixtime
        else:
            raise ValueError("Unable to generate seed: time values are equal")
    
    @staticmethod
    def generate_number() -> int:
        """
        Generate a random 3-digit number.
        
        Returns:
            Random number between 100 and 999
        """
        return randint(100, 999)


class OTPDictionary:
    """Represents a dictionary of OTP mappings."""
    
    def __init__(self, name: str, keys: List[str]):
        """
        Initialize OTP dictionary.
        
        Args:
            name: Name of the dictionary (e.g., "Numbers", "Lowercase")
            keys: List of keys to map
        """
        self.name: str = name
        self.mappings: Dict[str, int] = {key: 0 for key in keys}
        self.rng: RandomNumberGenerator = RandomNumberGenerator()
    
    def generate(self, with_output: bool = False) -> None:
        """
        Generate random OTP codes for all keys.
        
        Args:
            with_output: Whether to print generation progress
        """
        for key in self.mappings.keys():
            seed(self.rng.generate_seed())
            self.mappings[key] = self.rng.generate_number()
            
            if with_output:
                print(f"{key} -> {self.mappings[key]}")
    
    def reset(self, with_output: bool = False) -> None:
        """
        Reset all mappings to zero.
        
        Args:
            with_output: Whether to print reset progress
        """
        for key in self.mappings.keys():
            self.mappings[key] = 0
            
            if with_output:
                print(f"Changed key {key} to 0")
        
        if with_output:
            print("Reset all keys to 0")
    
    def has_duplicates_with(self, other: 'OTPDictionary') -> bool:
        """
        Check if this dictionary has duplicate values with another.
        
        Args:
            other: Another OTP dictionary to compare with
            
        Returns:
            True if duplicates found, False otherwise
        """
        self_values = set(self.mappings.values())
        other_values = set(other.mappings.values())
        
        return bool(self_values & other_values)
    
    def has_internal_duplicates(self) -> bool:
        """
        Check if this dictionary has duplicate values internally.
        
        Returns:
            True if internal duplicates found, False otherwise
        """
        values = list(self.mappings.values())
        return len(values) != len(set(values))
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert dictionary to pandas DataFrame.
        
        Returns:
            DataFrame with mappings
        """
        return pd.DataFrame.from_dict(self.mappings, orient="index")
    
    def save_to_csv(self, filepath: str) -> None:
        """
        Save dictionary to CSV file.
        
        Args:
            filepath: Path to output CSV file
        """
        df = self.to_dataframe()
        df.to_csv(filepath)


class DuplicateChecker:
    """Checks for duplicate values across OTP dictionaries."""
    
    @staticmethod
    def check_for_duplicates(dicts: List[OTPDictionary], 
                            debug_print: bool = False) -> bool:
        """
        Check all dictionaries for duplicates.
        
        Args:
            dicts: List of OTP dictionaries to check
            debug_print: Whether to print duplicate information
            
        Returns:
            True if duplicates found, False otherwise
        """
        # Check for internal duplicates
        for dictionary in dicts:
            if dictionary.has_internal_duplicates():
                if debug_print:
                    print(f"Internal duplicate found in {dictionary.name}")
                return True
        
        # Check for cross-dictionary duplicates
        for i, dict1 in enumerate(dicts):
            for dict2 in dicts[i+1:]:
                if dict1.has_duplicates_with(dict2):
                    if debug_print:
                        print(f"Duplicate found between {dict1.name} and {dict2.name}")
                    return True
        
        return False


class OTPGenerator:
    """Main OTP generator coordinating all dictionaries."""
    
    def __init__(self):
        """Initialize OTP generator with all required dictionaries."""
        # Define keys for each dictionary
        number_keys = [str(i) for i in range(10)]
        lowercase_keys = [chr(i) for i in range(ord('a'), ord('z') + 1)]
        uppercase_keys = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        
        # Create dictionaries
        self.numbers = OTPDictionary("Numbers", number_keys)
        self.lowercase = OTPDictionary("Lowercase", lowercase_keys)
        self.uppercase = OTPDictionary("Uppercase", uppercase_keys)
        
        self.checker = DuplicateChecker()
    
    def generate_all(self, with_output: bool = False) -> bool:
        """
        Generate OTPs for all dictionaries, ensuring no duplicates.
        
        Args:
            with_output: Whether to print generation progress
            
        Returns:
            True if generation successful
        """
        attempt_count = 0
        dictionaries = [self.numbers, self.lowercase, self.uppercase]
        
        # Initial generation
        print("Generating Numbers")
        self.numbers.generate(with_output)
        
        print("Generating lowercase alphabet")
        self.lowercase.generate(with_output)
        
        print("Generating uppercase alphabet")
        self.uppercase.generate(with_output)
        
        # Check for duplicates and regenerate if needed
        while self.checker.check_for_duplicates(dictionaries, debug_print=True):
            time.sleep(2)
            attempt_count += 1
            
            print("----")
            print("Regenerating due to duplicates")
            
            # Reset all dictionaries
            for dictionary in dictionaries:
                dictionary.reset(with_output)
            
            # Regenerate
            print("Regenerating Numbers")
            self.numbers.generate(with_output)
            
            print("Regenerating lowercase alphabet")
            self.lowercase.generate(with_output)
            
            print("Regenerating uppercase alphabet")
            self.uppercase.generate(with_output)
        
        if attempt_count > 0:
            print("----")
            print(f"Amount of duplicates found: {attempt_count}")
            print("----")
        
        return True
    
    def export_to_csv(self, date_str: str, output_dir: str = "otp") -> Tuple[str, str, str]:
        """
        Export all OTP dictionaries to CSV files.
        
        Args:
            date_str: Date string for filename
            output_dir: Output directory for CSV files
            
        Returns:
            Tuple of (numbers_file, lowercase_file, uppercase_file)
        """
        num_file = f"{output_dir}/OTPNum-{date_str}.csv"
        lc_file = f"{output_dir}/OTPLC-{date_str}.csv"
        uc_file = f"{output_dir}/OTPUC-{date_str}.csv"
        
        # Create files
        open(num_file, 'a').close()
        open(lc_file, 'a').close()
        open(uc_file, 'a').close()
        
        # Save to CSV
        self.numbers.save_to_csv(num_file)
        self.lowercase.save_to_csv(lc_file)
        self.uppercase.save_to_csv(uc_file)
        
        return num_file, lc_file, uc_file


def generate_date_string() -> str:
    """
    Generate date string for filenames.
    
    Returns:
        Formatted date string
    """
    date_now = datetime.now()
    return date_now.strftime("%d%m%y-%H%M%S")


def otp_main() -> None:
    """Main entry point for OTP generation."""
    generator = OTPGenerator()
    
    if generator.generate_all(with_output=False):
        # Generate date string for filenames
        date_str = generate_date_string()
        
        print("Exporting OTPs to CSV")
        print(f"File names will be:\n"
              f" Numbers: OTPNum-{date_str}.csv\n"
              f" Lowercase: OTPLC-{date_str}.csv\n"
              f" Uppercase: OTPUC-{date_str}.csv")
        
        # Export to CSV
        generator.export_to_csv(date_str)
        
        print("OTP generation complete!")


if __name__ == "__main__":
    otp_main()
