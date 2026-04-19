import argparse
import math
from pathlib import Path

from PIL import Image

BORDER = 40

RESOLUTION = 360
A4_WIDTH = 29.7
A4_HEIGHT = 21.0
CM_TO_INCH = 2.54

IMAGE_WIDTH = math.ceil(A4_WIDTH / CM_TO_INCH * RESOLUTION)
IMAGE_HEIGHT = math.ceil(A4_HEIGHT / CM_TO_INCH * RESOLUTION)


def process_image(file):
    path = valid_file(file)
    tiff = Image.open(path)

    icc_data = tiff.info.get("icc_profile")

    if tiff.mode in ("RGBA", "LA"):
        background = Image.new("RGB", tiff.size, (255, 255, 255))
        background.paste(tiff, mask=tiff.split()[-1])
        tiff = background
    elif tiff.mode != "RGB":
        tiff = tiff.convert("RGB")

    canvas = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255))

    border_x = math.ceil((IMAGE_WIDTH - tiff.width) / 2)
    border_y = math.ceil((IMAGE_HEIGHT - tiff.height) / 2)

    canvas.paste(tiff, (border_x, border_y))

    canvas.save(
        path.with_suffix(".jpg"),
        "JPEG",
        quality=95,
        icc_profile=icc_data,
        dpi=(RESOLUTION, RESOLUTION),
    )


def valid_file(value):
    path = Path(value)
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"File not found: {value}")
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="addborder",
        description="Add a white border to a TIFF and save it as a JPEG.",
        epilog="Example: addborder image1.tiff image2.tiff",
    )
    parser.add_argument("files", nargs="+", help="TIFF file(s) to process")
    args = parser.parse_args()

    for file in args.files:
        process_image(file)
