"""robotaxi_crop_photos.py

Purpose
    Crop and enlarge regions of official robotaxi press photos (e.g. the roof
    "halo", front apron, fenders) so that sensor windows can be inspected and,
    where possible, counted. Used on the Lucid/Nuro/Uber CES 2026 press photos.

Inputs
    --img FILE        source image (jpg/png/webp)
    --box X0 Y0 X1 Y1 crop box in pixels of the ORIGINAL image (repeatable)
    --scale S         optional factor applied to the box coordinates (default 1.0;
                      use it when boxes were read off a down-scaled preview)
    --up N            enlargement factor for the saved crop (default 2)
    --out PREFIX      output file prefix (default "crop")

Outputs
    PREFIX_<k>.png    one enlarged crop per --box, next to the given prefix path

Notes
    A photo count of sensor windows is an inference, not a specification: windows
    can hide several sensors, and lidar apertures are not always distinguishable
    from camera or radar covers in night or low-resolution shots.

Date: 2026-10-03
"""
import argparse

from PIL import Image


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--img", required=True)
    ap.add_argument("--box", nargs=4, type=float, action="append", required=True)
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--up", type=int, default=2)
    ap.add_argument("--out", default="crop")
    args = ap.parse_args()
    im = Image.open(args.img).convert("RGB")
    print(args.img, im.size)
    for k, (x0, y0, x1, y1) in enumerate(args.box, start=1):
        s = args.scale
        c = im.crop((int(x0 * s), int(y0 * s), int(x1 * s), int(y1 * s)))
        c = c.resize((c.width * args.up, c.height * args.up), Image.LANCZOS)
        name = f"{args.out}_{k}.png"
        c.save(name)
        print("saved", name, c.size)


if __name__ == "__main__":
    main()
