[app]

title = Rekap Penjualan Voucher
package.name = rekapvoucher
package.domain = org.junai

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3==3.10.11,kivy==2.2.1,openpyxl,et_xmlfile

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b

android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True
android.request_legacy_external_storage = True

[buildozer]

log_level = 2
