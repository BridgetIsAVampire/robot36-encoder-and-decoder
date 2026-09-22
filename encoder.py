import argparse,wave
import numpy as np
from PIL import Image
from robot36 import encode,FS
def main():
    p=argparse.ArgumentParser()
    p.add_argument("image"); p.add_argument("wav")
    a=p.parse_args()
    im=Image.open(a.image).convert("RGB").resize((320,240),Image.Resampling.LANCZOS)
    x=np.int16(np.clip(encode(np.asarray(im)),-1,1)*32767)
    with wave.open(a.wav,"wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(FS)
        w.writeframes(x.tobytes())
    print("Wrote",a.wav,"duration",len(x)/FS,"seconds")
if __name__=="__main__": main()
