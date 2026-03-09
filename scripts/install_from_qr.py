#!/usr/bin/env python3
import argparse
import re
import shutil
import subprocess
import sys
from urllib.parse import urlparse

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
INSTALL_RE = re.compile(r"clawhub\s+install\s+([a-z0-9][a-z0-9-]{1,63})", re.I)


def decode_with_opencv(image_path: str):
    try:
        import cv2  # type: ignore
    except Exception:
        return None
    img = cv2.imread(image_path)
    if img is None:
        return None
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)
    return data.strip() if data else None


def decode_with_zbar(image_path: str):
    if not shutil.which("zbarimg"):
        return None
    try:
        p = subprocess.run(["zbarimg", "--quiet", "--raw", image_path], capture_output=True, text=True, check=True)
        out = p.stdout.strip()
        return out if out else None
    except Exception:
        return None


def decode_qr(image_path: str):
    return decode_with_opencv(image_path) or decode_with_zbar(image_path)


def parse_slug(text: str):
    m = INSTALL_RE.search(text)
    if m:
        return m.group(1).lower()

    if text.startswith("http://") or text.startswith("https://"):
        path = urlparse(text).path.strip("/")
        if not path:
            return None
        parts = [p for p in path.split("/") if p]
        if not parts:
            return None
        candidate = parts[-1].lower()
        return candidate if SLUG_RE.match(candidate) else None

    candidate = text.strip().lower()
    return candidate if SLUG_RE.match(candidate) else None


def main():
    ap = argparse.ArgumentParser(description="Decode QR and install ClawHub skill")
    ap.add_argument("image", help="Path to QR image")
    ap.add_argument("--decode-only", action="store_true", help="Only decode and parse, do not install")
    ap.add_argument("--dir", default=None, help="Custom install dir for clawhub install --dir")
    args = ap.parse_args()

    raw = decode_qr(args.image)
    if not raw:
        print("ERROR: Could not decode QR. Install opencv-python or zbarimg.")
        sys.exit(2)

    slug = parse_slug(raw)
    print(f"Decoded QR: {raw}")
    print(f"Parsed slug: {slug if slug else 'N/A'}")

    if not slug:
        print("ERROR: Unsupported QR payload for auto-install.")
        sys.exit(3)

    cmd = ["clawhub", "install", slug]
    if args.dir:
        cmd.extend(["--dir", args.dir])

    print("Install command:", " ".join(cmd))
    if args.decode_only:
        return

    p = subprocess.run(cmd)
    sys.exit(p.returncode)


if __name__ == "__main__":
    main()
