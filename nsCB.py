"""
ns-pCB (number station - project Cherry Blossom)
Main Application Module - Object-Oriented Implementation
Developed by Zach Matcham (zatcham)
Version 1.0 | 2025

This module provides the main workflow for the number station system,
including TTS generation, OTP management, and audio output.
"""

import os
import csv
import re
import configparser
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from gtts import gTTS
import pandas as pd
from fpdf import FPDF
from pydub import AudioSegment

# Suppress pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

from tscipherlib import cencodeh
import nsCB_otpgen
import nsCB_tts
from otp_manager import OTPManager


class Config:
    """Configuration manager for ns-pCB."""
    
    def __init__(self, config_file: str = "config.cb"):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file: str = config_file
        self.tts_tld: str = ""
        self.preamble_fn: str = ""
        self.station_ident: str = ""
        self.tts_type: str = ""
        self.nscb_mode: str = ""
        self.otp_numlength: str = ""
        self.keep_original: str = ""
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        conf = configparser.ConfigParser()
        conf.read(self.config_file)
        
        self.tts_tld = conf.get("TTS", "google_tld")
        self.preamble_fn = conf.get("Audio", "preamble_fn")
        self.station_ident = conf.get("Station", "station_ident")
        self.tts_type = conf.get("TTS", "tts_mode")
        self.nscb_mode = conf.get("TTS", "nscb_mode")
        self.otp_numlength = conf.get("OTP", "otp_numlength")
        self.keep_original = conf.get("Station", "keeporiginal")


class FilePathManager:
    """Manages file paths and directory structure for ns-pCB."""
    
    def __init__(self, main_dir: Optional[str] = None):
        """
        Initialize file path manager.
        
        Args:
            main_dir: Main working directory (defaults to current directory)
        """
        self.main_dir: str = main_dir or os.getcwd()
    
    def check_paths(self) -> bool:
        """
        Check if required directories exist.
        
        Returns:
            True if all required paths exist, False otherwise
        """
        if os.path.exists(self.main_dir):
            return os.path.exists(os.path.join(self.main_dir, "audio"))
        return False
    
    def generate_audio_filename(self) -> str:
        """
        Generate timestamped filename for audio output.
        
        Returns:
            Full path to audio file
        """
        date_now = datetime.now()
        date_str = date_now.strftime("%d%m%y-%H%M%S")
        return os.path.join(self.main_dir, "audio", f"{date_str}.mp3")


class OTPConverter:
    """Converts text to OTP codes using OTP dictionaries."""
    
    def __init__(self, otp_dir: str = "otp"):
        """
        Initialize OTP converter.
        
        Args:
            otp_dir: Directory containing OTP CSV files
        """
        self.otp_dir: str = otp_dir
        self.num_dict: Dict[str, int] = {}
        self.lc_dict: Dict[str, int] = {}
        self.uc_dict: Dict[str, int] = {}
    
    def load_otps(self) -> bool:
        """
        Load OTP dictionaries from CSV files.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            p = Path(self.otp_dir)
            
            # Find latest OTP files
            num_latest = max([fn for fn in p.glob('*OTPNum*.csv')], 
                           key=lambda f: f.stat().st_mtime)
            lc_latest = max([fn for fn in p.glob('*OTPLC*.csv')], 
                          key=lambda f: f.stat().st_mtime)
            uc_latest = max([fn for fn in p.glob('*OTPUC*.csv')], 
                          key=lambda f: f.stat().st_mtime)
            
            # Load dictionaries
            self.num_dict = pd.read_csv(num_latest, dtype={"a": int, "b": int}, 
                                       header=None, index_col=0, squeeze=True).to_dict()
            self.lc_dict = pd.read_csv(lc_latest, header=None, index_col=0, 
                                      squeeze=True).to_dict()
            self.uc_dict = pd.read_csv(uc_latest, header=None, index_col=0, 
                                      squeeze=True).to_dict()
            
            print(f"Loaded OTP dictionaries: {len(self.num_dict)} numbers, "
                  f"{len(self.lc_dict)} lowercase, {len(self.uc_dict)} uppercase")
            return True
            
        except (ValueError, StopIteration) as error:
            print(f"Error loading OTP files: {error}")
            return False
    
    def convert_to_otp(self, text: str) -> List[str]:
        """
        Convert text to OTP codes.
        
        Args:
            text: Text to convert
            
        Returns:
            List of OTP codes
        """
        otp_list: List[str] = []
        
        for char in text:
            if char.isdigit():
                # Handle numbers
                for key, value in self.num_dict.items():
                    if str(char) == str(key):
                        otp_code = str(value)
                        print(f"{char} -> {otp_code}")
                        otp_list.append(otp_code)
                        break
                        
            elif char.islower():
                # Handle lowercase letters
                for key, value in self.lc_dict.items():
                    if char == str(key):
                        otp_code = str(value)
                        print(f"{char} -> {otp_code}")
                        otp_list.append(otp_code)
                        break
                        
            elif char.isupper():
                # Handle uppercase letters
                for key, value in self.uc_dict.items():
                    if char == str(key):
                        otp_code = str(value)
                        print(f"{char} -> {otp_code}")
                        otp_list.append(otp_code)
                        break
                        
            elif char.isspace():
                # Handle spaces
                otp_list.append("--")
            else:
                print(f"Warning: Special character '{char}' not supported")
        
        return otp_list


class TTSGenerator:
    """Generates text-to-speech audio for number station output."""
    
    def __init__(self, config: Config, file_manager: FilePathManager):
        """
        Initialize TTS generator.
        
        Args:
            config: Configuration object
            file_manager: File path manager
        """
        self.config: Config = config
        self.file_manager: FilePathManager = file_manager
    
    def generate(self, phrase: str) -> str:
        """
        Generate TTS audio from text.
        
        Args:
            phrase: Text to convert to speech
            
        Returns:
            Path to generated audio file
        """
        filename = self.file_manager.generate_audio_filename()
        
        if self.config.tts_type == "google":
            self._generate_google_tts(phrase, filename)
        elif self.config.tts_type == "nscb":
            self._generate_nscb_tts(phrase, filename)
        
        print(f"Generated TTS file: {filename}")
        return filename
    
    def _generate_google_tts(self, phrase: str, filename: str) -> None:
        """Generate TTS using Google TTS."""
        tts_obj = gTTS(text=phrase, lang="en", tld=self.config.tts_tld, slow=False)
        tts_obj.save(filename)
    
    def _generate_nscb_tts(self, phrase: str, filename: str) -> None:
        """Generate TTS using custom nsCB engine."""
        if self.config.nscb_mode == "morse":
            print("Morse mode selected")
            audio = nsCB_tts.generateMorseLoop(phrase)
        elif self.config.nscb_mode == "speech":
            print("Speech mode selected")
            audio = nsCB_tts.generateTTS(phrase)
        else:
            raise ValueError(f"Unknown nsCB mode: {self.config.nscb_mode}")
        
        audio.export(filename, format="mp3")


class AudioMerger:
    """Merges preamble and generated audio files."""
    
    def __init__(self, config: Config, file_manager: FilePathManager):
        """
        Initialize audio merger.
        
        Args:
            config: Configuration object
            file_manager: File path manager
        """
        self.config: Config = config
        self.file_manager: FilePathManager = file_manager
    
    def merge(self, tts_file: str) -> str:
        """
        Merge preamble with TTS audio.
        
        Args:
            tts_file: Path to TTS audio file
            
        Returns:
            Path to merged audio file
        """
        # Load audio segments
        tts_audio = AudioSegment.from_mp3(tts_file)
        preamble_path = os.path.join(self.file_manager.main_dir, "audio", 
                                     self.config.preamble_fn)
        preamble = AudioSegment.from_mp3(preamble_path)
        
        # Merge with silence
        silence = AudioSegment.silent(duration=2000)
        merged = preamble + silence + tts_audio
        
        # Generate output filename
        date_now = datetime.now()
        date_str = date_now.strftime("%d%m%y-%H%M%S")
        output_file = os.path.join(self.file_manager.main_dir, "audio", 
                                   f"{date_str}-merge.mp3")
        
        # Export merged audio
        merged.export(output_file, format="mp3")
        
        # Remove original if configured
        if self.config.keep_original.lower() == "false":
            os.remove(tts_file)
        
        print(f"Merged audio saved: {output_file}")
        return output_file


class PDFGenerator:
    """Generates PDF documents from OTP CSV files."""
    
    def __init__(self, otp_dir: str = "otp"):
        """
        Initialize PDF generator.
        
        Args:
            otp_dir: Directory containing OTP CSV files
        """
        self.otp_dir: str = otp_dir
    
    def generate(self) -> str:
        """
        Generate PDF from latest OTP CSV files.
        
        Returns:
            Path to generated PDF file
        """
        print("\nns-pCB - OTP PDF Creation\n")
        print("Generating PDFs from latest OTP CSVs\n")
        
        date_now = datetime.now()
        date_display = date_now.strftime("%d/%m/%y %H:%M:%S")
        date_filename = date_now.strftime("%d%m%y-%H%M%S")
        output_filename = f"OTP {date_filename}.pdf"
        
        print(f"File name: {output_filename}\n")
        
        # Find latest OTP files
        p = Path(self.otp_dir)
        num_file = max([fn for fn in p.glob('*OTPNum*.csv')], 
                      key=lambda f: f.stat().st_mtime)
        lc_file = max([fn for fn in p.glob('*OTPLC*.csv')], 
                     key=lambda f: f.stat().st_mtime)
        uc_file = max([fn for fn in p.glob('*OTPUC*.csv')], 
                     key=lambda f: f.stat().st_mtime)
        
        # Create PDF
        with open(num_file, newline='') as f1, \
             open(lc_file, newline='') as f2, \
             open(uc_file, newline='') as f3:
            
            pdf = FPDF()
            pdf.add_page()
            page_width = pdf.w - 2 * pdf.l_margin
            
            # Header
            pdf.set_font('Courier', '', 14.0)
            pdf.cell(page_width, 0.0, f'ns-pCB OTP - Exported: {date_display}', 
                    align='C')
            pdf.ln(10)
            
            # Content
            pdf.set_font('Courier', '', 12)
            col_width = page_width / 4
            th = pdf.font_size
            
            pdf.ln(4)
            pdf.cell(page_width, 10.0, 'Double hyphen = space', align='L')
            pdf.ln(10)
            
            # Numbers section
            self._add_section(pdf, f1, "Numbers:", col_width, th)
            
            # Lowercase section
            self._add_section(pdf, f2, "Lowercase:", col_width, th)
            
            # Uppercase section
            self._add_section(pdf, f3, "Uppercase:", col_width, th)
            
            # Footer
            pdf.ln(10)
            pdf.set_font('Times', '', 10.0)
            pdf.cell(page_width, 0.0, '- end of report -', align='C')
            
            pdf.output(output_filename, 'F')
        
        print(f"PDF generated: {output_filename}")
        return output_filename
    
    def _add_section(self, pdf: FPDF, file, title: str, 
                     col_width: float, th: float) -> None:
        """Add a section to the PDF."""
        pdf.ln(4)
        pdf.cell(pdf.w - 2 * pdf.l_margin, 10.0, title, align='L')
        pdf.ln(10)
        
        reader = csv.reader(file)
        for row in reader:
            pdf.cell(col_width, th, str(row[0]), border=1)
            pdf.cell(col_width, th, row[1], border=1)
            pdf.ln(th)


class NumberStationApp:
    """Main application class for ns-pCB number station."""
    
    def __init__(self):
        """Initialize the number station application."""
        self.config: Config = Config()
        self.file_manager: FilePathManager = FilePathManager()
        self.otp_manager: OTPManager = OTPManager()
        self.otp_converter: OTPConverter = OTPConverter()
        self.tts_generator: TTSGenerator = TTSGenerator(self.config, self.file_manager)
        self.audio_merger: AudioMerger = AudioMerger(self.config, self.file_manager)
        self.pdf_generator: PDFGenerator = PDFGenerator()
    
    def run(self) -> None:
        """Run the main application loop."""
        print("ns-pCB Initialization:")
        
        if not self.file_manager.check_paths():
            print("Main directory does not exist, exiting")
            print(f"Make sure {self.file_manager.main_dir} exists with /audio subdirectory")
            return
        
        print("Init done\n")
        self._show_menu()
    
    def _show_menu(self) -> None:
        """Display main menu and handle user input."""
        print("Welcome to ns-pCB\n")
        
        while True:
            menu_choice = input(
                "Select an option:\n"
                " 1. TTS Generation\n"
                " 2. TTS Output (not yet implemented)\n"
                " 3. OTP Generation\n"
                " 4. Convert OTP into PDF\n"
                " 5. Exit\n"
            )
            
            if menu_choice == "1":
                self._tts_generation_workflow()
            elif menu_choice == "2":
                self._tts_output_workflow()
            elif menu_choice == "3":
                self._otp_generation_workflow()
            elif menu_choice == "4":
                self.pdf_generator.generate()
            elif menu_choice == "5":
                print("Goodbye")
                break
            elif menu_choice != "":
                print("Incorrect input, try again")
    
    def _tts_generation_workflow(self) -> None:
        """Handle TTS generation workflow with OTP management."""
        print("\nns-pCB - TTS Generation\n")
        
        # Get user information
        user = input("Enter your username: ")
        otp_id = input("Enter your OTP ID (or press Enter to auto-assign): ")
        
        # Handle OTP validation and reuse
        if otp_id and not self.otp_manager.validate_otp(otp_id):
            # OTP already used
            otp_user = self.otp_manager.get_otp_user(otp_id)
            print(f"Warning: OTP {otp_id} has already been used by {otp_user}.")
            reuse_choice = input("Type Y to reuse this OTP, or any other key to go back: ")
            
            if reuse_choice != "Y":
                print("Returning to main menu.")
                return
            
            self.otp_manager.reuse_otp(otp_id, user)
            print("OTP marked as reused. Proceeding.")
        else:
            # OTP is unused or auto-assign requested
            if not otp_id:
                otp_id = self.otp_manager.issue_otp(user)
                print(f"Assigned OTP: {otp_id}")
            else:
                self.otp_manager.issue_otp(user)
                print("OTP is unused. Proceeding.")
        
        # Load OTP dictionaries
        if not self.otp_converter.load_otps():
            print("Failed to load OTP files. Returning to menu.")
            return
        
        # Get message to encode
        message = input("String to convert (no special chars): ")
        
        # Convert to OTP codes
        otp_codes = self.otp_converter.convert_to_otp(message)
        print(f"OTP codes: {otp_codes}")
        
        # Generate TTS
        tts_phrase = f"{self.config.station_ident}   {otp_codes}"
        tts_file = self.tts_generator.generate(tts_phrase)
        
        # Merge with preamble
        self.audio_merger.merge(tts_file)
        
        print("TTS generation complete!")
    
    def _tts_output_workflow(self) -> None:
        """Handle TTS output workflow."""
        print("TTS output not yet implemented")
    
    def _otp_generation_workflow(self) -> None:
        """Handle OTP generation workflow."""
        print("\nns-pCB - OTP Generation\n")
        print("Warning: By running this, all future TTS Generations will require the new OTP.")
        
        choice = input("To continue, enter Y, or to return to main menu, press any other key: ")
        
        if choice == "Y":
            print()
            nsCB_otpgen.otp_main()
            self.otp_manager.clear_otp_status()
            print()


def main() -> None:
    """Main entry point for the application."""
    app = NumberStationApp()
    app.run()


if __name__ == "__main__":
    main()
