[app]

title = Rekap Penjualan Voucher
package.name = rekapvoucher
package.domain = org.junai

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3,kivy,openpyxl,pandas

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 31
android.minapi = 21
android.ndk = 25b

android.archs = arm64-v8a, armeabi-v7a

# WAJIB untuk Android 11+
android.request_legacy_external_storage = True

[buildozer]

log_level = 2
warn_on_root = 0
