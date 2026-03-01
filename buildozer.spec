[app]

# App info
title        = MMA Legends Pro
package.name = mmalegendspro
package.domain = org.mmalegends

# Source
source.dir  = .
source.main = mma_app.py
source.include_exts = py,png,jpg,kv,atlas,ttf,pkl
source.exclude_patterns = build/*,dist/*,*.exe,*.spec,__pycache__/*

version = 1.0

# ── Dependencies ────────────────────────────────────────────────────────────
# kivy must come first; no extra libs needed (pickle / pathlib are stdlib)
requirements = python3,kivy

# ── Orientation / display ───────────────────────────────────────────────────
orientation = portrait
fullscreen   = 1

# ── Android SDK / NDK ───────────────────────────────────────────────────────
android.api          = 33
android.minapi       = 21
android.ndk_version  = 25b
android.accept_sdk_license = True

# Internal storage only — no external-storage permissions needed
# (save file written to app.user_data_dir)
android.permissions  =

# ── Icons / presplash (optional — replace with your own PNGs) ───────────────
# icon.filename     = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/presplash.png

# ── Build settings ──────────────────────────────────────────────────────────
log_level   = 2
warn_on_root = 1

[buildozer]
log_level  = 2
warn_on_root = 1
