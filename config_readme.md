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
- `tts_tld` :
  -    Default setting: `co.uk`
  -    Options:
              This option only works in `google` mode
              This link provides the various TLDs that you can change the setting to: https://gtts.readthedocs.io/en/latest/module.html#localized-accents
              There is not yet support for any language that is not `en`. Please make sure to omit a prepending `.` to the TLD, as it will not work. The format shown on the site is what you need to change it to.

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
          
