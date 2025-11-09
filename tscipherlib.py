"""
tscipherlib - Text Scrambling Cipher Library
Object-Oriented Implementation with Type Annotations

Original by tomrow (https://github.com/tomrow/tscipherlib)
Refactored for ns-pCB project
"""

import math
import random
from typing import List


class CipherEngine:
    """Cipher engine for encoding and decoding text."""
    
    def __init__(self, key: int):
        """
        Initialize cipher engine with a key.
        
        Args:
            key: Encryption key
        """
        self.key: int = key
    
    def _scramble(self, iterate: int) -> int:
        """
        Generate scrambling value for character at position.
        
        Args:
            iterate: Position in text (1-indexed)
            
        Returns:
            Scrambled value
        """
        interim = iterate
        interim += (self.key % 10) * iterate
        interim += math.floor(iterate / 3)
        interim += iterate * 2
        interim += math.floor(9 * math.sin(math.radians(iterate * 2)))
        
        # Complex scrambling iterations
        for _ in range(6):
            interimb = math.sin(math.radians(self.key * 2)) * (2 ** 32)
            interimb = math.floor(interimb)
            interimb = interimb * 3 ^ (iterate * 7)
            
            interimc = interimb >> 5
            interimc = interimc << 5
            
            interimd = interimc << 3
            interime = interimb ^ interimc
            interime += interimd
            
            interim -= interime
        
        interim = interim % 255
        print(interim)
        return interim + 255
    
    def encode(self, text: str) -> List[int]:
        """
        Encode text to list of integers.
        
        Args:
            text: Text to encode
            
        Returns:
            List of encoded integers
        """
        output: List[int] = []
        random.seed(self.key)
        
        for h in range(len(text)):
            i = h + 1
            encoded_value = (ord(text[h]) + self._scramble(i)) % 255
            output.append(encoded_value)
        
        return output
    
    def encode_hex(self, text: str) -> str:
        """
        Encode text to hexadecimal string.
        
        Args:
            text: Text to encode
            
        Returns:
            Hexadecimal encoded string
        """
        output = ""
        random.seed(self.key)
        
        for h in range(len(text)):
            i = h + 1
            chara = hex((ord(text[h]) + self._scramble(i)) % 255)
            chara = chara[2:]  # Remove '0x' prefix
            
            while len(chara) < 2:
                chara = "0" + chara
            
            output += chara
        
        return output
    
    def decode(self, array: List[int]) -> str:
        """
        Decode list of integers to text.
        
        Args:
            array: List of encoded integers
            
        Returns:
            Decoded text
        """
        output = ""
        random.seed(self.key)
        
        for h in range(len(array)):
            i = h + 1
            maths = (array[h] - self._scramble(i))
            output += chr(maths % 255)
        
        return output
    
    def decode_hex(self, string_in: str) -> str:
        """
        Decode hexadecimal string to text.
        
        Args:
            string_in: Hexadecimal encoded string
            
        Returns:
            Decoded text
        """
        str_edit = string_in.lower()
        
        # Ensure even length
        if len(string_in) % 2 == 1:
            str_edit = "0" + string_in
        
        # Hex digit mapping
        hex_digits = {
            "0": 0, "1": 1, "2": 2, "3": 3, "4": 4,
            "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15
        }
        
        # Convert hex pairs to integers
        array: List[int] = []
        for c in range(math.floor(len(str_edit) / 2)):
            ptr = c * 2
            value = (hex_digits[str_edit[ptr]] * 16) + hex_digits[str_edit[ptr + 1]]
            array.append(value)
        
        # Decode array
        return self.decode(array)


# Module-level convenience functions for backward compatibility
def cencode(text: str, key: int) -> List[int]:
    """
    Encode text to list of integers (convenience function).
    
    Args:
        text: Text to encode
        key: Encryption key
        
    Returns:
        List of encoded integers
    """
    engine = CipherEngine(key)
    return engine.encode(text)


def cencodeh(text: str, key: int) -> str:
    """
    Encode text to hexadecimal string (convenience function).
    
    Args:
        text: Text to encode
        key: Encryption key
        
    Returns:
        Hexadecimal encoded string
    """
    engine = CipherEngine(key)
    return engine.encode_hex(text)


def cdecode(array: List[int], key: int) -> str:
    """
    Decode list of integers to text (convenience function).
    
    Args:
        array: List of encoded integers
        key: Encryption key
        
    Returns:
        Decoded text
    """
    engine = CipherEngine(key)
    return engine.decode(array)


def cdecodeh(string_in: str, key: int) -> str:
    """
    Decode hexadecimal string to text (convenience function).
    
    Args:
        string_in: Hexadecimal encoded string
        key: Encryption key
        
    Returns:
        Decoded text
    """
    engine = CipherEngine(key)
    return engine.decode_hex(string_in)


if __name__ == "__main__":
    # Test the cipher
    test_key = 1
    test_text = "hello"
    
    print("Testing CipherEngine:")
    engine = CipherEngine(test_key)
    
    # Test encoding and decoding
    encoded = engine.encode(test_text)
    print(f"Encoded: {encoded}")
    
    decoded = engine.decode(encoded)
    print(f"Decoded: {decoded}")
    
    # Test specific decode
    print(f"Decode [171, 214, 95, 155]: {cdecode([171, 214, 95, 155], 1)}")
