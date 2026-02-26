[app]

title = Rekap Voucher Ruijie
package.name = rekapruijie
package.domain = com.ruijie

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3,kivy,openpyxl,et_xmlfile,plyer

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO
android.request_legacy_external_storage = True

android.api = 33
android.minapi = 24
android.sdk = 33
android.ndk = 25b
android.enable_androidx = True

[buildozer]
log_level = 2
