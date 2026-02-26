[app]

title = Voucher Rekapan
package.name = voucherrekapan
package.domain = org.jun

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3,kivy,kivymd,pandas,openpyxl,requests

orientation = portrait

fullscreen = 0

android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET

android.allow_backup = True

[buildozer]

log_level = 2
warn_on_root = 1
