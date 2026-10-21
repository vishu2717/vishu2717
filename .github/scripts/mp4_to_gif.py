import imageio.v3 as iio
import numpy as np
from PIL import Image
import os

input_path = ".github/assets/header_video.mp4"
output_path = ".github/assets/header.gif"

print("Reading video...")
frames = iio.imread(input_path, plugin="pyav")
print(f"Total frames: {len(frames)}")

# Target ~35 frames to stay well under GitHub's 5MB Camo limit
step = max(1, len(frames) // 35)
selected = frames[::step][:35]

resized = []
for f in selected:
    img = Image.fromarray(f)
    w, h = img.size
    new_w = 400
    new_h = int(h * new_w / w)
    img = img.resize((new_w, new_h), Image.BILINEAR)
    img = img.quantize(colors=96, method=Image.Quantize.FASTOCTREE)
    resized.append(np.array(img.convert('RGB')))

print(f"Writing compressed GIF at {new_w}x{new_h}...")
iio.imwrite(output_path, resized, duration=110, loop=0)

size_mb = os.path.getsize(output_path) / (1024*1024)
print(f"Compression complete! GIF size: {size_mb:.2f} MB (Must be < 5.0 MB for GitHub Camo)")
