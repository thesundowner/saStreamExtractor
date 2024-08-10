# saStreamExtractor

saStreamExtractor is a simple script that decodes and extracts the audio data from Grand Theft Auto: San Andreas' game files. This script only works on the streams, as found as on the directory  `audio/streams`.

## How to

1. Install Python (It it isn't available in your system)
2. Clone the repository
3. Open a terminal in the repo folder
4. install dependencies using this command: `pip install -r requirements.txt`
5. run the script using this command:

   `py extractor.py <directory-to-stream-files>  -o <output-folder>`

`-o` is optional and if its not specified, it will store the directory in the same place as the script in a folder called `output`.
