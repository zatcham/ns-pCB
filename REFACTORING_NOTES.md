# ns-pCB Refactoring Notes

## Overview
This document describes the refactoring of ns-pCB to use Object-Oriented Programming (OOP) principles and comprehensive type annotations.

## What Changed

### New Module: `otp_manager.py`
A complete OOP-based OTP management system with:
- **OTPStatus**: Represents the status of a single OTP
- **OTPManager**: Manages OTP lifecycle including issuance, validation, and reuse tracking
- Multi-user support with CSV-based persistence
- OTP reuse tracking with warnings
- Full type annotations

### Refactored: `nsCB.py`
Main application refactored into multiple focused classes:
- **Config**: Configuration management
- **FilePathManager**: File path and directory management
- **OTPConverter**: Converts text to OTP codes using dictionaries
- **TTSGenerator**: Text-to-speech generation
- **AudioMerger**: Audio file merging
- **PDFGenerator**: PDF generation from OTP CSVs
- **NumberStationApp**: Main application coordinator

### Refactored: `nsCB_otpgen.py`
OTP generation refactored into focused classes:
- **RandomNumberGenerator**: Generates random seeds and numbers
- **OTPDictionary**: Manages character-to-number mappings
- **DuplicateChecker**: Validates uniqueness across dictionaries
- **OTPGenerator**: Coordinates the entire OTP generation process

### Refactored: `tscipherlib.py`
Cipher library refactored with:
- **CipherEngine**: Main cipher class with encode/decode methods
- Full type annotations
- Backward-compatible module-level functions

### Refactored: `nsCB_tts.py`
TTS module refactored into focused classes:
- **TTSConfig**: Configuration management
- **AudioFileChecker**: Validates audio file existence
- **SpeechTTSGenerator**: Speech synthesis
- **MorseCodeConverter**: Text to Morse code conversion
- **MorseTTSGenerator**: Morse code audio generation

## New Features

### Multi-User OTP Management
- Each OTP can be tracked by user
- OTP status persisted in CSV format
- Warning system for OTP reuse
- Auto-generation of OTP IDs

### Improved Type Safety
- All functions and methods have type annotations
- Uses `typing` module for complex types (Dict, List, Optional, Tuple)
- Better IDE support and error detection

### Single Responsibility Principle
- Each class has one clear purpose
- Functions are focused and testable
- Improved code maintainability

## Testing

### Unit Tests
- `test_otp_manager.py`: 21 tests covering all OTP manager functionality
- All tests pass successfully

### Integration Tests
- `test_integration.py`: 5 tests covering end-to-end workflows
- Tests multi-user scenarios, OTP generation, and cipher operations

## Backward Compatibility

All refactored modules maintain backward compatibility:
- Module-level convenience functions still available
- Original function signatures preserved where possible
- Existing code can continue to work without modifications

## Usage Examples

### Using OTP Manager
```python
from otp_manager import OTPManager

manager = OTPManager()

# Issue OTP to user
otp_id = manager.issue_otp('alice')

# Validate OTP
is_unused = manager.validate_otp(otp_id)

# Get OTP user
user = manager.get_otp_user(otp_id)

# Reuse OTP
manager.reuse_otp(otp_id, 'bob')
```

### Using Number Station App
```python
from nsCB import NumberStationApp

app = NumberStationApp()
app.run()
```

### Using OTP Generator
```python
from nsCB_otpgen import OTPGenerator

generator = OTPGenerator()
generator.generate_all()
generator.export_to_csv('20250101-120000')
```

### Using Cipher Engine
```python
from tscipherlib import CipherEngine

engine = CipherEngine(key=12345)
encoded = engine.encode("secret message")
decoded = engine.decode(encoded)
```

## Migration Guide

If you have existing code using the old procedural style, here's how to migrate:

### Old Style (Still Works)
```python
from otp_manager import issue_otp, validate_otp

otp = issue_otp('alice')
valid = validate_otp(otp)
```

### New Style (Recommended)
```python
from otp_manager import OTPManager

manager = OTPManager()
otp = manager.issue_otp('alice')
valid = manager.validate_otp(otp)
```

## Code Quality Improvements

1. **Type Annotations**: All functions have proper type hints
2. **Docstrings**: Comprehensive documentation for all classes and methods
3. **Error Handling**: Better exception handling and error messages
4. **Testing**: Comprehensive test coverage
5. **Modularity**: Clear separation of concerns
6. **Maintainability**: Easier to understand and modify

## Future Enhancements

Potential areas for future improvement:
- Add logging throughout the application
- Implement async/await for I/O operations
- Add database backend option for OTP tracking
- Implement REST API for remote access
- Add web interface
- Improve error recovery mechanisms

## Summary

This refactoring brings ns-pCB up to modern Python standards with:
- ✅ Full OOP design
- ✅ Comprehensive type annotations
- ✅ Improved testability
- ✅ Better code organization
- ✅ Multi-user support
- ✅ Backward compatibility
- ✅ Complete test coverage
