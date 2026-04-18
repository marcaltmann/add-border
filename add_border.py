import math

from PIL import Image

BORDER = 40

RESOLUTION = 360
A4_WIDTH = 29.7
A4_HEIGHT = 21.0
CM_TO_INCH = 2.54

IMAGE_WIDTH = math.ceil(A4_WIDTH / CM_TO_INCH * RESOLUTION)
IMAGE_HEIGHT = math.ceil(A4_HEIGHT / CM_TO_INCH * RESOLUTION)


# 1. Open the TIFF
tiff = Image.open("/home/marc/Bilder/darktable_exported/birdie.tif")

# 2. Grab the embedded ICC profile (if any)
icc_data = tiff.info.get("icc_profile")

# 3. Ensure it's in a JPEG-compatible mode (no alpha)
if tiff.mode in ("RGBA", "LA"):
    background = Image.new("RGB", tiff.size, (255, 255, 255))
    background.paste(tiff, mask=tiff.split()[-1])
    tiff = background
elif tiff.mode != "RGB":
    tiff = tiff.convert("RGB")

# 4. Create the white canvas and paste
canvas = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255))

border_x = math.ceil((IMAGE_WIDTH - tiff.width) / 2)
border_y = math.ceil((IMAGE_HEIGHT - tiff.height) / 2)

canvas.paste(tiff, (border_x, border_y))

# 5. Save as JPEG, carrying the original profile forward
canvas.save("output.jpg", "JPEG", quality=92, icc_profile=icc_data, dpi=(RESOLUTION, RESOLUTION))
