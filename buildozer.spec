[app]

title = Voucher Rekapan
package.name = voucherrekapan
package.domain = org.junai

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,txt

version = 1.0

requirements = python3,kivy==2.3.0,openpyxl,plyer,requests

orientation = portrait
fullscreen = 0

# ===== ANDROID =====
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# PERMISSION WAJIB
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET

# Lebih stabil di GitHub
android.enable_androidx = True
android.accept_sdk_license = True

# ===== BUILD =====
log_level = 2
warn_on_root = 0

# ===== PYTHON FOR ANDROID =====
p4a.bootstrap = sdl2
p4a.branch = master

# ===== OPTIMASI =====
android.release_artifact = apk
android.gradle_dependencies =

[buildozer]

log_level = 2
warn_on_root = 0
