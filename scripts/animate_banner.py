"""Render the profile's SVG banner as a looping GIF. Requires Pillow and Inkscape."""
from pathlib import Path
import math
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SIZE = (1200, 320)
FRAMES = 80
paths = [
    [(1200, 185), (1074, 185), (1037, 148), (918, 148), (884, 182), (809, 182)],
    [(1040, 320), (1040, 264), (1006, 230), (951, 230)],
    [(905, 0), (905, 44), (952, 91), (1055, 91), (1115, 31), (1200, 31)],
]


def point_along(points, fraction):
    lengths = [math.dist(a, b) for a, b in zip(points, points[1:])]
    remaining = fraction * sum(lengths)
    for a, b, length in zip(points, points[1:], lengths):
        if remaining <= length:
            t = remaining / length
            return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
        remaining -= length
    return points[-1]


with tempfile.TemporaryDirectory() as work:
    poster = Path(work) / 'poster.png'
    subprocess.run(['inkscape', str(ROOT / 'assets/header.svg'),
                    '--export-type=png', f'--export-filename={poster}'], check=True)
    base = Image.open(poster).convert('RGBA')

# One shared palette prevents flashing between frames.
palette_image = Image.new('RGB', (256, 1))
colours = [(16, 30, 43), (242, 245, 244), (131, 221, 199), (180, 196, 207),
           (132, 155, 169), (40, 64, 79)]
for i in range(250):
    t = i / 249
    colours.append(tuple(round(a + t * (b - a)) for a, b in
                         zip((16, 30, 43), (180, 255, 230))))
palette_image.putdata(colours)
palette = palette_image.quantize(colors=256)
frames = []
for frame in range(FRAMES):
    phase = frame / FRAMES
    image = base.copy()
    glow = Image.new('RGBA', SIZE)
    d = ImageDraw.Draw(glow)
    dots = []
    for j, path in enumerate(paths):
        head = (phase + j * .31) % 1
        for k in range(15):
            p = head - k * .006
            if p < 0:
                continue
            x, y = point_along(path, p)
            strength = (1 - k / 15) ** 1.6
            d.ellipse((x-5, y-5, x+5, y+5), fill=(85, 235, 190, round(160*strength)))
        dots.append(point_along(path, head))
    image = Image.alpha_composite(image, glow.filter(ImageFilter.GaussianBlur(7)))
    draw = ImageDraw.Draw(image)
    for x, y in dots:
        draw.ellipse((x-3, y-3, x+3, y+3), fill=(195, 255, 234, 255))
    # A slow status pulse, kept away from the text.
    pulse = (.5 + .5 * math.sin(phase * 2 * math.pi))
    radius = 7 + 4 * pulse
    draw.ellipse((809-radius, 182-radius, 809+radius, 182+radius),
                 outline=(85, round(145 + 70*pulse), 176, 255), width=2)
    frames.append(image.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE))

out = ROOT / 'assets/header.gif'
frames[0].save(out, save_all=True, append_images=frames[1:], duration=80,
               loop=0, optimize=True, disposal=1)
print(f'{out}: {out.stat().st_size:,} bytes; {FRAMES} frames; {FRAMES*.08:.1f}s loop')