# Robot 36 Encoder / Decoder

A simple Python encoder and decoder for **Robot 36 SSTV**.

The generated WAV files should work with **QSSTV**. If QSSTV reports an invalid WAV header, try rewriting the file with **SoX**.

## Installation

Install the required Python dependencies:

```bash
python -m pip install -r requirements.txt
```

## Encoding

Convert a JPG or PNG image into a Robot 36 WAV file:

```bash
python encoder.py <inputfile>.jpg <outputfile>.wav
```

For example:

```bash
python encoder.py woof.jpg meow.wav
```

## Decoding

Convert a Robot 36 WAV file back into an image:

```bash
python decoder.py <inputfile>.wav <outputfile>.png
```

For example:

```bash
python decoder.py hi.wav hi.png
```

## QSSTV / WAV Header Issues

If QSSTV reports an **invalid WAV header**, rewrite the WAV file using SoX:

```bash
sox audio.wav audio_qsstv.wav
```

Then try opening `audio_qsstv.wav` in QSSTV.

## Project Files

| File               | Description                               |
| ------------------ | ----------------------------------------- |
| `encoder.py`       | Encodes images into Robot 36 audio        |
| `decoder.py`       | Decodes Robot 36 audio into images        |
| `robot36.py`       | Robot 36 encoding/decoding implementation |
| `requirements.txt` | Python dependencies                       |
| `README.md`        | Project documentation                     |

## Robot 36 Specification

| Property          | Value          |
| ----------------- | -------------- |
| Resolution        | `320 × 240`    |
| VIS Code          | `8`            |
| Duration          | ~36 seconds    |
| Image Frequencies | `1500–2300 Hz` |

### Header

The Robot 36 header consists of:

1. **300 ms** — 1900 Hz leader
2. **10 ms** — 1200 Hz break
3. **300 ms** — 1900 Hz leader
4. **30 ms** — VIS start, data, parity, and stop bits

### Image Lines

Each image line consists of:

| Component     | Duration |
| ------------- | -------: |
| Sync          |     9 ms |
| Porch         |     3 ms |
| Y (luminance) |    88 ms |
| Separator     |   4.5 ms |
| Porch         |   1.5 ms |
| Chroma        |    44 ms |

### Chroma

Chroma samples alternate between:

* **Even lines:** R-Y
* **Odd lines:** B-Y

## Example

Encode an image:

```bash
python encoder.py woof.jpg meow.wav
```

Decode the resulting audio:

```bash
python decoder.py meow.wav output.png
```

The resulting image should be `320 × 240` and use the Robot 36 SSTV format.
