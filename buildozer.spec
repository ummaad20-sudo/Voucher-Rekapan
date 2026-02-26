[app]
title = Rekap Ruijie Pro
package.name = rekapruijie
package.domain = com.ruijie

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3,kivy,openpyxl,plyer

orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

android.permissions = \
    READ_EXTERNAL_STORAGE,\
    WRITE_EXTERNAL_STORAGE,\
    INTERNET

[buildozer]
log_level = 2
