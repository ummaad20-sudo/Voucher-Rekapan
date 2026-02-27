[app]

title = Rekap Voucher Ruijie
package.name = rekapruijie
package.domain = com.ruijie

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3==3.10.9,kivy==2.2.1,openpyxl,et_xmlfile,plyer,Cython==0.29.36

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES
android.request_legacy_external_storage = True

android.api = 33
android.minapi = 21
android.ndk = 25b
android.enable_androidx = True

[buildozer]
log_level = 2
