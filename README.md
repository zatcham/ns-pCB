# ns-pCB
##### (number station - project Cherry Blossom)
A Python-based OTP generator and encoder, which can output MP3s to serve as a number station

It does not yet decode, however OTPs are produced as a PDF/CSV format 

### Folder Structure
```
ns-pCB/
    otp/
    audio/
       preamble.mp3
    nsCB_otpgen.py
    nsCB.py
    tscipherlib.py
```

### How to use ns-pCB

### OTP Generation
OTPs (One Time Pads) are generated via `nsCB_otpgen.py`. It requires a directory called `otp` inside where it is executed from. 
It will create 3 CSVs, with the file name containing the date and time of generation. These CSVs can be used on their own to decode, or alternatively the main program can convert these into a single PDF. 

### Dependancies
##### Bundled with
  * ns-pCB_OTPGen
  * tscipherlib (https://github.com/tomrow/tscipherlib)
##### To be installed via Pip:
  * pandas
  * fpdf
  * pydub (also requires ffmpeg)
  * gTTS

### TODO
 * ✅ Integrate OTP Generation into main program
 * Integrate tscipherlib
 * Decoding
 * Web-based decoding
 * Finish playback
 * ✅ Remove hardcoded directories
