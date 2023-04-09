# FuzzyGuard

FuzzyGuard is a script designed to simplify the process of fuzzing websites using FFUF. By automatically generating FFUF commands based on the target website, FuzzyGuard eliminates the need to manually add filters when dealing with an influx of 200 status codes.<br>

```
> cat subdomains.txt | python3 fuzzyguard.py --silent

ffuf -u https://example.com/FUZZ -w WORDLIST
ffuf -u https://example.com/FUZZ -w WORDLIST -fl 550-560 -fw 1619 -fs 18000-19000
ffuf -u https://example.com/FUZZ -w WORDLIST -fl 169 -fw 792 -fs 160000-170000
```
## Usage
The script only has 2 options :
```
               ,       _____
        _.-"` `'-.    |   __|_ _ ___ ___ _ _
        '._ __{}_(    |   __| | |- _|- _| | |
        |'--.__\      |__|  |___|___|___|_  |
        (   =_\ =      _____            |___|
         |   _ |      |   __|_ _ ___ ___ _| |
         )\___/       |  |  | | | .'|  _| . |
     .--'`:._]        |_____|___|__,|_| |___|
    /  \      '-.              Made By: @castilho101
    

  --ffuf-flags FFUF_FLAGS   Extra FFUF flags, ex: --ffuf-extra "-mc all -fc 404"
  --silent                  Silent mode
```
