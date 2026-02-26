[app]

title = RekapVoucherPro
package.name = rekapvoucher
package.domain = org.junai

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3,kivy,openpyxl

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

android.archs = arm64-v8a, armeabi-v7a

[buildozer]

log_level = 2
