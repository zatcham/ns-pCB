# Editing the config file
The file `config.cb` should be located in the ns-pCB working directory, and contains some default parameters. 
Should you have an urge to change these to suit your preferences, it is very unambiguous process. 

The config file can be opened in any decent text editor (so this excludes vim 😉) and is analogous to an .INI file.

# Parameters that can be changed

### [TTS] :
- `tts_mode`         
  -    Default setting: `google`
  -    Options:
              This changes what TTS engine to use, you can choose between `nscb` and `google`
              `nscb` is the custom engine that comes with this project, it purely concatenates audio recordings of numbers into a single MP3 file. More information                 about this can be found within `tts_readme.md`.     
               `google` provides more flexiblity and has some differences, but does require an internet connection, whilst `nscb` does not.
- `google_tld` :
  -    Default setting: `co.uk`
  -    Options:
              This option only works in `google` mode
              This link provides the various TLDs that you can change the setting to: https://gtts.readthedocs.io/en/latest/module.html#localized-accents
              There is not yet support for any language that is not `en`. Please make sure to omit a prepending `.` to the TLD, as it will not work. The format shown on the site is what you need to change it to.
- `nscb_mode` :
  -    Default setting: `speech`
  -    Options:
              This option only works in `nscb` mode
              It chooses between the 2 options of output, either `morse`, which will output a MP3 of morse code or `speech` which functions as a rudimentary TTS engine
- `morse_delay1` :
  -    Default setting: `500`
  -    Options:
              This option takes a number in milliseconds and will change the delay based on that. 
              More specifically, this controls the delay after each dot or dash.
- `morse_delay2` :
  -    Default setting: `500`
  -    Options:
              This option takes a number in milliseconds and will change the delay based on that. 
              More specifically, this controls the delay after each character.
- `morse_delay3` :
  -    Default setting: `1000`
  -    Options:
              This option takes a number in milliseconds and will change the delay based on that. 
              More specifically, this controls the delay after each word.
- `morse_loop` :
  -    Default setting: `1`
  -    Options:
              This option takes a integer and controls how many times the morse will repeat itself. In a later update, a tone will be added after every repeat.
- `morseloop_delay1` :
  -    Default setting: `1000`
  -    Options:
              This option takes a number in milliseconds and will change the delay based on that. 
              More specifically, this controls the delay at the end, after it has completed the specified amount of loops
- `morseloop_delay2` :
  -    Default setting: `1000`
  -    Options:
              This option takes a number in milliseconds and will change the delay based on that. 
              More specifically, this controls the delay after each loop.

### [Audio] :
- `preamble_fn` : 
  -   Default setting: `preamble.mp3`
  -   Options:
             Any MP3 file will work, provided it is located in the `/audio/` directory, located within the ns-pCB working directory.
             Alternatively, you can simply rename your preamble file to `preamble.mp3`
          
### [Station] :          
- `station_ident` :
  - Default setting: `001`
  - Options:
          Any string will work, but I'd personally recommend keeping it short.
          
### [OTP] :          
- `cipher_type` :
  - Default setting: `nspcb`
  - Options:
          This option allows you to select what cipher you would want to use for your message.
          `nspcb` will not cipher the text beyond the OTP, which is utilised with every cipher method.
          `tscipherlib` will utilise tscipherlib (https://github.com/tomrow/tscipherlib) in conjunction with the OTP. You must enter a numerical key (integer) at time of running.