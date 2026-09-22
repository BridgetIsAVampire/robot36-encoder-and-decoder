import numpy as np
from scipy.signal import butter, sosfiltfilt, hilbert

FS=48000
W,H=320,240
def tone(f,ms,phase=0):
    n=round(FS*ms/1000); k=np.arange(n)
    step=2*np.pi*f/FS
    return np.sin(phase+step*k), (phase+step*n)%(2*np.pi)

def header(vis=8):
    p=[]; ph=0.0
    for f,ms in [(1900,300),(1200,10),(1900,300),(1200,30)]:
        x,ph=tone(f,ms,ph); p.append(x)
    parity=0
    for i in range(7): Vis stuff
        bit=(vis>>i)&1
        parity ^= bit
        x,ph=tone(1100 if bit else 1300,30,ph); p.append(x)
    x,ph=tone(1100 if parity else 1300,30,ph); p.append(x)
    x,ph=tone(1200,30,ph); p.append(x)
    return np.concatenate(p)

def rgb_to_ycrcb(rgb):
    a=rgb.astype(float)/255
    r,g,b=a[...,0],a[...,1],a[...,2]
    y=.299*r+.587*g+.114*b
    cr=.5+(r-y)*.713
    cb=.5+(b-y)*.564
    return np.clip(y*255,0,255),np.clip(cr*255,0,255),np.clip(cb*255,0,255)

def ycrcb_to_rgb(y,cr,cb):
    y=y/255.; cr=cr/255.; cb=cb/255.
    r=y+(cr-.5)/.713
    b=y+(cb-.5)/.564
    g=(y-.299*r-.114*b)/.587
    return np.clip(np.stack([r,g,b],-1)*255,0,255).astype(np.uint8)

def scan(v,ms):
    n=round(FS*ms/1000); v=np.asarray(v)
    out=np.empty(n); pos=np.linspace(0,len(v),n,endpoint=False).astype(int)
    ph=0.
    # filegen phase
    for i in range(len(v)):
        a=round(i*n/len(v)); b=round((i+1)*n/len(v))
        if b<=a: continue
        f=1500+800*np.clip(v[i],0,255)/255
        k=np.arange(b-a); st=2*np.pi*f/FS
        out[a:b]=np.sin(ph+st*k); ph=(ph+st*(b-a))%(2*np.pi)
    return out

def encode(rgb):
    if rgb.shape!=(H,W,3): raise ValueError("image must be 320x240")
    y,cr,cb=rgb_to_ycrcb(rgb)
    p=[header(8)]
    for row in range(H):
        p.append(tone(1200,9)[0])
        p.append(tone(1500,3)[0])
        p.append(scan(y[row],88))
        if row%2==0:
            p.append(tone(1500,4.5)[0])
            p.append(tone(1900,1.5)[0])
            c=(cr[row]+cr[min(row+1,H-1)])/2
        else:
            p.append(tone(2300,4.5)[0])
            p.append(tone(1900,1.5)[0])
            c=(cb[row]+cb[max(row-1,0)])/2
        p.append(scan(c[::2],44))
    a=np.concatenate(p).astype(np.float32)
    return a/np.max(np.abs(a))

def decode(audio):
    # decoder for clean wav
    x=np.asarray(audio,float)
    sos=butter(5,[900,2600],btype="bandpass",fs=FS,output="sos")
    z=sosfiltfilt(sos,x)
    ph=np.unwrap(np.angle(hilbert(z)))
    f=np.gradient(ph)*FS/(2*np.pi)
    # Detect 1200-Hz syncs using stf
    m=((f>1050)&(f<1350)).astype(float)
    win=round(FS*.002)
    q=np.convolve(m,np.ones(win)/win,'same')>.6
    d=np.diff(np.r_[0,q.astype(np.int8),0])
    starts=np.flatnonzero(d==1)
    ends=np.flatnonzero(d==-1)
    cand=[a for a,b in zip(starts,ends) if .006<(b-a)/FS<.012]
    sync=[]; gap=round(FS*.10)
    for a in cand:
        if not sync or a-sync[-1]>gap: sync.append(a)
    if len(sync)<240: raise ValueError("fewer than 240 Robot 36 syncs found")
    # Pick the first 240 that has the ~105 ms line spacing.
    ls=round(FS*105/1000)
    best=min((sync[i:i+240] for i in range(len(sync)-239)),
             key=lambda s: np.median(np.abs(np.diff(s)-ls)))
    y=np.zeros((H,W)); cr=np.ones((H,W))*128; cb=np.ones((H,W))*128
    yo=round(FS*12/1000); yl=round(FS*88/1000)
    co=round(FS*(9+3+88+4.5+1.5)/1000); cl=round(FS*44/1000)
    def vals(a,b,n):
        q=f[a:b]; q=q[max(1,len(q)//30):-max(1,len(q)//30)]
        return np.interp(np.linspace(0,1,n),np.linspace(0,1,len(q)),np.clip((q-1500)*255/800,0,255))
    for r,s in enumerate(best):
        y[r]=vals(s+yo,s+yo+yl,W)
        c=vals(s+co,s+co+cl,W//2); c=np.repeat(c,2)
        if r%2==0: cr[r]=c
        else: cb[r]=c
    for r in range(H):
        if r%2: cr[r]=cr[r-1]
        elif r>0: cb[r]=cb[r-1]
    return ycrcb_to_rgb(y,cr,cb)
