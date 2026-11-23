"""Zip the flat-pack deliverable."""
import os, zipfile, hashlib, datetime
ROOT = os.path.dirname(os.path.abspath(__file__))
NAME = "FLATPACK-WU09-package.zip"
def main():
    out = os.path.join(ROOT, NAME); n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        files = ["README.md", "make_package.py"]
        for d in ("docs", "cad", "calc", "out"):
            for base, dirs, fs in os.walk(os.path.join(ROOT, d)):
                dirs[:] = [x for x in dirs if x != "__pycache__"]
                for f in fs:
                    files.append(os.path.relpath(os.path.join(base, f), ROOT))
        for f in files:
            p = os.path.join(ROOT, f)
            if os.path.exists(p) and not f.endswith(".pyc"):
                z.write(p, f); n += 1
    print(f"wrote {NAME}: {n} files, {os.path.getsize(out)/1e6:.2f} MB")
if __name__ == "__main__":
    main()
