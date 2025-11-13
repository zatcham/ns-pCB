"""
ns-pCB (number station - project Cherry Blossom)
TTS Module - Object-Oriented Implementation
Developed by Zach Matcham (zatcham)
Version 1.0 | 2025

This module provides text-to-speech and Morse code generation functionality.
"""

import os
import configparser
from datetime import datetime
from typing import List, Dict
from pydub import AudioSegment


# Morse code dictionary
MORSE_DICT: Dict[str, str] = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 
    'D': '-..', 'E': '.', 'F': '..-.', 
    'G': '--.', 'H': '....', 'I': '..', 
    'J': '.---', 'K': '-.-', 'L': '.-..', 
    'M': '--', 'N': '-.', 'O': '---', 
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 
    'V': '...-', 'W': '.--',
    'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ',': '--..--', '.': '.-.-.-',
    '?': '..--..', '/': '-..-.', '-': '-....-',
    '(': '-.--.', ')': '-.--.-'
}


class TTSConfig:
    """Configuration manager for TTS settings."""
    
    def __init__(self, config_file: str = "config.cb"):
        """
        Initialize TTS configuration.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file: str = config_file
        self.morse_delay1: int = 500
        self.morse_delay2: int = 500
        self.morse_delay3: int = 1000
        self.morse_loop: int = 2
        self.morseloop_delay1: int = 1000
        self.morseloop_delay2: int = 1000
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        conf = configparser.ConfigParser()
        conf.read(self.config_file)
        
        self.morse_delay1 = int(conf.get("TTS", "morse_delay1"))
        self.morse_delay2 = int(conf.get("TTS", "morse_delay2"))
        self.morse_delay3 = int(conf.get("TTS", "morse_delay3"))
        self.morse_loop = int(conf.get("TTS", "morse_loop"))
        self.morseloop_delay1 = int(conf.get("TTS", "morseloop_delay1"))
        self.morseloop_delay2 = int(conf.get("TTS", "morseloop_delay2"))


class AudioFileChecker:
    """Validates existence of required audio files."""
    
    def __init__(self):
        """Initialize audio file checker with default file paths."""
        self.speech_files: List[str] = [
            'tts_gen/voice/0.mp3', 'tts_gen/voice/1.mp3',
            'tts_gen/voice/2.mp3', 'tts_gen/voice/3.mp3',
            'tts_gen/voice/4.mp3', 'tts_gen/voice/5.mp3',
            'tts_gen/voice/6.mp3', 'tts_gen/voice/7.mp3',
            'tts_gen/voice/8.mp3', 'tts_gen/voice/9.mp3'
        ]
        self.morse_files: List[str] = [
            'tts_gen/morse/dot.mp3',
            'tts_gen/morse/dash.mp3'
        ]
    
    def check_files(self) -> bool:
        """
        Check if all required audio files exist.
        
        Returns:
            True if all files exist, False otherwise
        """
        speech_ok = all(os.path.isfile(f) for f in self.speech_files)
        morse_ok = all(os.path.isfile(f) for f in self.morse_files)
        
        if speech_ok:
            print("All speech files exist")
        else:
            print("Speech files missing")
            return False
        
        if morse_ok:
            print("All morse files exist")
        else:
            print("Morse files missing")
            return False
        
        return True


class SpeechTTSGenerator:
    """Generates speech TTS from numeric strings."""
    
    def __init__(self, config: TTSConfig, file_checker: AudioFileChecker):
        """
        Initialize speech TTS generator.
        
        Args:
            config: TTS configuration
            file_checker: Audio file checker
        """
        self.config: TTSConfig = config
        self.file_checker: AudioFileChecker = file_checker
    
    def generate(self, text: str, save_to_file: bool = False) -> AudioSegment:
        """
        Generate speech TTS audio from text.
        
        Args:
            text: Text to convert (should contain digits 0-9 and spaces)
            save_to_file: Whether to save output to file
            
        Returns:
            Generated audio segment
        """
        if not self.file_checker.check_files():
            raise FileNotFoundError("Required audio files are missing")
        
        audio = AudioSegment.empty()
        
        for char in text:
            if char in '0123456789':
                # Load audio file for digit
                digit_audio = AudioSegment.from_mp3(f'tts_gen/voice/{char}.mp3')
                audio += digit_audio
                audio += AudioSegment.silent(duration=50)
            elif char == ' ':
                # Add longer silence for spaces
                audio += AudioSegment.silent(duration=300)
        
        if save_to_file:
            self._save_audio(audio, "speech")
        
        return audio
    
    def _save_audio(self, audio: AudioSegment, mode: str) -> str:
        """
        Save audio to file.
        
        Args:
            audio: Audio segment to save
            mode: Mode string for filename
            
        Returns:
            Path to saved file
        """
        date_now = datetime.now()
        date_str = date_now.strftime("%d%m%y-%H%M%S")
        filename = f"tts_gen/out/{date_str}-{mode}.mp3"
        audio.export(filename, format="mp3")
        return filename


class MorseCodeConverter:
    """Converts text to Morse code."""
    
    def __init__(self):
        """Initialize Morse code converter."""
        self.morse_dict: Dict[str, str] = MORSE_DICT
    
    def text_to_morse(self, text: str) -> str:
        """
        Convert text to Morse code representation.
        
        Args:
            text: Text to convert (will be uppercased)
            
        Returns:
            Morse code string with dots, dashes, and spaces
        """
        text = text.upper()
        morse_output = ""
        
        for char in text:
            if char != " ":
                if char in self.morse_dict:
                    morse_output += self.morse_dict[char] + " "
            else:
                morse_output += " "
        
        return morse_output


class MorseTTSGenerator:
    """Generates Morse code audio from text."""
    
    def __init__(self, config: TTSConfig, file_checker: AudioFileChecker):
        """
        Initialize Morse TTS generator.
        
        Args:
            config: TTS configuration
            file_checker: Audio file checker
        """
        self.config: TTSConfig = config
        self.file_checker: AudioFileChecker = file_checker
        self.converter: MorseCodeConverter = MorseCodeConverter()
    
    def generate(self, text: str, save_to_file: bool = False) -> AudioSegment:
        """
        Generate Morse code audio from text.
        
        Args:
            text: Text to convert to Morse code
            save_to_file: Whether to save output to file
            
        Returns:
            Generated audio segment
        """
        if not self.file_checker.check_files():
            raise FileNotFoundError("Required audio files are missing")
        
        # Convert text to Morse code
        morse_code = self.converter.text_to_morse(text)
        
        # Generate audio
        audio = AudioSegment.empty()
        silence1 = AudioSegment.silent(duration=self.config.morse_delay1)
        silence2 = AudioSegment.silent(duration=self.config.morse_delay2)
        silence3 = AudioSegment.silent(duration=self.config.morse_delay3)
        
        i = 0
        while i < len(morse_code):
            char = morse_code[i]
            
            if char == '-':
                dash = AudioSegment.from_mp3('tts_gen/morse/dash.mp3')
                audio += dash
                audio += silence1
            elif char == '.':
                dot = AudioSegment.from_mp3('tts_gen/morse/dot.mp3')
                audio += dot
                audio += silence1
            elif char == ' ':
                # Check if it's a double space
                if i + 1 < len(morse_code) and morse_code[i + 1] == ' ':
                    audio += silence3
                    i += 1  # Skip next space
                else:
                    audio += silence2
            
            i += 1
        
        if save_to_file:
            self._save_audio(audio, "morse")
        
        return audio
    
    def generate_loop(self, text: str, save_to_file: bool = False) -> AudioSegment:
        """
        Generate Morse code audio with looping.
        
        Args:
            text: Text to convert to Morse code
            save_to_file: Whether to save output to file
            
        Returns:
            Generated audio segment with loops
        """
        if not self.file_checker.check_files():
            raise FileNotFoundError("Required audio files are missing")
        
        # Print Morse code representation
        print(self.converter.text_to_morse(text))
        
        # Generate base audio
        base_audio = self.generate(text, save_to_file=False)
        
        # Loop the audio
        looped_audio = AudioSegment.empty()
        silence = AudioSegment.silent(duration=self.config.morseloop_delay1)
        loop_delay = AudioSegment.silent(duration=self.config.morseloop_delay2)
        
        for i in range(self.config.morse_loop):
            looped_audio += base_audio
            looped_audio += loop_delay
            print(f"Loop {i + 1} of {self.config.morse_loop}")
        
        if self.config.morse_loop > 1:
            looped_audio += silence
        
        if save_to_file:
            self._save_audio(looped_audio, "morse-loop")
        
        return looped_audio
    
    def _save_audio(self, audio: AudioSegment, mode: str) -> str:
        """
        Save audio to file.
        
        Args:
            audio: Audio segment to save
            mode: Mode string for filename
            
        Returns:
            Path to saved file
        """
        date_now = datetime.now()
        date_str = date_now.strftime("%d%m%y-%H%M%S")
        filename = f"tts_gen/out/{date_str}-{mode}.mp3"
        audio.export(filename, format="mp3")
        return filename


# Module-level convenience functions for backward compatibility
_config: TTSConfig = None
_file_checker: AudioFileChecker = None


def checkConfig() -> None:
    """Load configuration (convenience function)."""
    global _config
    _config = TTSConfig()


def checkForFiles() -> None:
    """Check for required files (convenience function)."""
    global _file_checker
    if _file_checker is None:
        _file_checker = AudioFileChecker()
    _file_checker.check_files()


def generateTTS(text: str) -> AudioSegment:
    """
    Generate speech TTS (convenience function).
    
    Args:
        text: Text to convert
        
    Returns:
        Generated audio segment
    """
    global _config, _file_checker
    if _config is None:
        _config = TTSConfig()
    if _file_checker is None:
        _file_checker = AudioFileChecker()
    
    generator = SpeechTTSGenerator(_config, _file_checker)
    return generator.generate(text, save_to_file=(__name__ == "__main__"))


def generateMorse(text: str) -> AudioSegment:
    """
    Generate Morse code audio (convenience function).
    
    Args:
        text: Text to convert
        
    Returns:
        Generated audio segment
    """
    global _config, _file_checker
    if _config is None:
        _config = TTSConfig()
    if _file_checker is None:
        _file_checker = AudioFileChecker()
    
    generator = MorseTTSGenerator(_config, _file_checker)
    return generator.generate(text, save_to_file=(__name__ == "__main__"))


def generateMorseLoop(text: str) -> AudioSegment:
    """
    Generate Morse code audio with looping (convenience function).
    
    Args:
        text: Text to convert
        
    Returns:
        Generated audio segment with loops
    """
    global _config, _file_checker
    if _config is None:
        _config = TTSConfig()
    if _file_checker is None:
        _file_checker = AudioFileChecker()
    
    generator = MorseTTSGenerator(_config, _file_checker)
    return generator.generate_loop(text, save_to_file=(__name__ == "__main__"))


def generateMorseTxt(text: str) -> str:
    """
    Convert text to Morse code representation (convenience function).
    
    Args:
        text: Text to convert
        
    Returns:
        Morse code string
    """
    converter = MorseCodeConverter()
    return converter.text_to_morse(text)


def generateMorseAud(text: str) -> AudioSegment:
    """
    Generate Morse audio (convenience function, alias for generateMorse).
    
    Args:
        text: Text to convert
        
    Returns:
        Generated audio segment
    """
    return generateMorse(text)


if __name__ == "__main__":
    checkConfig()
    text = input("Enter string: ")
    generateTTS(text)
    print(generateMorseTxt(text))
    generateMorseAud(text)
