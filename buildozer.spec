[app]
title = Rekap Ruijie Pro
package.name = rekapruijie
package.domain = com.ruijie

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3,kivy==2.2.1,openpyxl,plyer

orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 23
android.sdk = 33
android.ndk = 25b

android.accept_sdk_license = True
p4a.branch = stable

android.permissions = \
    READ_EXTERNAL_STORAGE,\
    WRITE_EXTERNAL_STORAGE,\
    INTERNET

[buildozer]
log_level = 2
warn_on_root = 0
