import argparse,wave
import numpy as np
from PIL import Image
from robot36 import decode,FS
def main():
    p=argparse.ArgumentParser()
    p.add_argument("wav"); p.add_argument("image")
    a=p.parse_args()
    with wave.open(a.wav,"rb") as w:
        if w.getnchannels()!=1 or w.getsampwidth()!=2 or w.getframerate()!=FS:
            raise ValueError("input must be mono 16-bit 48000 Hz WAV")
        x=np.frombuffer(w.readframes(w.getnframes()),dtype="<i2").astype(float)/32768
    Image.fromarray(decode(x),"RGB").save(a.image)
    print("Wrote",a.image)
if __name__=="__main__": main()
