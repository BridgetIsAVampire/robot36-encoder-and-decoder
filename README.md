# Robot 36 en/decoder
    Simple python decoder and encoder for robot36.
    The generated files SHOULD work in QSSTV, if QSSTV reports an invalid header, try rewriting the WAV file with SoX.
    
Install:
    python -m pip install -r requirements.txt

Encode:
    python encoder.py (inputfile).jpg/.png (outputfilename).wav
Decode:
    python decoder.py (inputfile).wav (outputfilename).jpg/.png
SoX rewrite if header invalid:
    sox audio.wav audio_qsstv.wav
    
Files:
decoder.py
encoder.py
README.md
requirements.txt
robot36.py
    
Robot 36:
Resolution: 320x240
VIS: 8
Duration: ~36 seconds
Image frequencies: 1500-2300 Hz

Header:
300 ms 1900 Hz leader
10 ms 1200 Hz break
300 ms 1900 Hz leader
30 ms VIS start/data/parity/stop

Image lines:
9 ms sync
3 ms porch
88 ms Y
4.5 ms separator
1.5 ms porch
44 ms chroma

Chroma:
Even R-Y
Odd B-y

Example:
python encoder.py woof.jpg meow.wav
python decoder.py hi.wav hi.png
