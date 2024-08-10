"""For more information:
    https://gtamods.com/wiki/Audio_stream
"""

from io import BufferedReader
import numpy as np
import argparse
import os
import tqdm


encoding_key = [
    0xEA,0x3A,0xC4,0xA1,
    0x9A,0xA8,0x14,0xF3,
    0x48,0xB0,0xD7,0x23,
    0x9D,0xE8,0xFF,0xF1,
]



parser = argparse.ArgumentParser(
    description="Extracts the audio data from Grand Theft Auto: San Andreas audio stream files.\n",
    exit_on_error=True,
    epilog="For more information: https://gtamods.com/wiki/Audio_stream",
)

parser.add_argument(
    "streamDir",
    help="The audio stream file directory from an unmodified GTA:SA install",
    type=str,
)

parser.add_argument(
    "-o",
    "--outputDir",
    help="User-specified output directory.    Defaults to the current working directory of the script",
    type=str,
)
args = parser.parse_args()


def decodeStream(infile: BufferedReader):
    indata = np.frombuffer(infile.read(), dtype="u1").tolist()
    buf = []
    index = 0

    for i in indata:
        buf.append(i ^ encoding_key[index])
        index = (index + 1) % 16

    outdata = np.array(buf, dtype="u1")
    if not os.path.exists('./streams-decoded'):
        os.makedirs('streams-decoded')
    outdata.tofile(f"streams-decoded/{os.path.split(infile.name)[1]}")


class StreamData:
    def __init__(self, stream: BufferedReader):
        self._stream = stream

    def writeTrackToFile(self, output="output") -> None:
        output = args.outputDir if args.outputDir else "output"
        data = self._stream.read()
        data = data.split(bytes.fromhex("0100cdcd"))
        count = 0

        os.makedirs(f"{output}/{os.path.split(self._stream.name)[1]}", exist_ok=True)
        for block in data:
            try:
                with open(
                    f"{output}/{os.path.split(self._stream.name)[1]}/{count}.ogg", "xb+"
                ) as f:
                    f.write(block)
                    f.close()
                count += 1
            except FileExistsError:
                continue

if __name__ == "__main__":
    for path, dirnames, filenames in os.walk(args.streamDir):
        for file in tqdm.tqdm(filenames, desc="Extracting audio from stream..."):
            fullpath = os.path.join(path, file)
            fileHandler = open(fullpath, "rb")
            decodeStream(fileHandler)
            StreamData(open(f"./streams-decoded/{file}", "rb")).writeTrackToFile()

    print(
        "Extracion done\nGo to ",
        args.outputDir if args.outputDir else "./output",
        "To view the output content.",
    )
