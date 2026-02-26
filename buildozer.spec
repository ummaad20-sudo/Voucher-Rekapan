[app]

title = Voucher Monitor
package.name = voucher_monitor
package.domain = org.jun.monitor

source.dir = .
source.include_exts = py,png,jpg,kv

version = 1.0

requirements = python3,kivy,kivymd,requests,urllib3,chardet,idna,certifi

orientation = portrait

fullscreen = 0

android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

android.permissions = INTERNET

android.accept_sdk_license = True

# penting untuk stabilitas
p4a.branch = stable

log_level = 2
warn_on_root = 1
