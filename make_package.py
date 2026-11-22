"""Zip the complete deliverable package."""
import os, zipfile, hashlib, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
NAME = "GI-RAD-STAND-R09-package.zip"
INCLUDE_DIRS = ["docs", "cad", "calc", "out"]
skip_ext = {".pyc"}
skip_names = {"__pycache__", ".venv"}

def main():
    out = os.path.join(ROOT, NAME)
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        files = ["README.md", "prompt.md", "make_package.py"]
        for d in INCLUDE_DIRS:
            for base, dirs, fs in os.walk(os.path.join(ROOT, d)):
                dirs[:] = [x for x in dirs if x not in skip_names]
                for f in fs:
                    files.append(os.path.relpath(os.path.join(base, f), ROOT))
        for f in files:
            p = os.path.join(ROOT, f)
            if os.path.exists(p) and os.path.splitext(f)[1] not in skip_ext:
                z.write(p, f)
                n += 1
    size = os.path.getsize(out) / 1e6
    print(f"wrote {NAME}: {n} files, {size:.2f} MB")
    # manifest
    h = hashlib.sha256(open(out, "rb").read()).hexdigest()[:16]
    with open(os.path.join(ROOT, "out", "package_manifest.txt"), "w") as fh:
        fh.write(f"package: {NAME}\nfiles: {n}\nsize_MB: {size:.2f}\n"
                 f"sha256_16: {h}\nbuilt: {datetime.date.today()}\n")

if __name__ == "__main__":
    main()
