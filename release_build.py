"""Create a portable release zip of the project.
Usage:
    python release_build.py [--include-media]

This script zips the project root into ../diabetic_retinopathy_system_release.zip
excluding virtualenv, .git, staticfiles, venv, __pycache__, and optionally includes
`media/` when --include-media is provided.
"""
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / f"{ROOT.name}_release.zip"
EXCLUDES = {'.git', 'venv', 'venv/', '__pycache__', 'staticfiles', 'media', '.env'}

include_media = '--include-media' in sys.argv

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(ROOT):
        relroot = os.path.relpath(root, ROOT)
        # Skip excluded directories
        skip = False
        for ex in EXCLUDES:
            if relroot == ex or relroot.startswith(ex + os.sep) or root.endswith(ex):
                skip = True
                break
        if skip:
            continue
        for f in files:
            # Skip the script output itself if present
            if f == OUT.name:
                continue
            # Skip .pyc and env file
            if f.endswith('.pyc') or f == '.env':
                continue
            filepath = Path(root) / f
            arcname = Path(relroot) / f if relroot != '.' else Path(f)
            zf.write(filepath, arcname)
    if include_media:
        media_dir = ROOT / 'media'
        if media_dir.exists():
            for root, dirs, files in os.walk(media_dir):
                for f in files:
                    filepath = Path(root) / f
                    arcname = Path('media') / Path(root).relative_to(media_dir) / f
                    zf.write(filepath, arcname)

print(f"Created {OUT}")
