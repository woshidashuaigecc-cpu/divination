[app]

# (str) Title of your application
title = 占卜起卦

# (str) Package name
package.name = divination

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,pyjnius

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or sensorPortrait)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PYTHON, NAME:ENTRYPOINT_TO_PYTHON

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 1.9.1

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for new android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon,
# navy, olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
#android.ndk = 19b

# (int) Android NDK API to use. This is the minimum API your APK will support.
#android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk =

# (str) python-for-android fork to use, defaults to upstream/upstream
#android.p4a_branch = master

# (str) python-for-android url to use for building.
#android.p4a_dir =

# (list) python-for-android git clone directory (if empty, it will be automatically cloned from github.
#android.p4a_dir =

# (list) The directory keys are stored and added to your APK.
#android.arch = armeabi-v7a

# (bool) Indicate whether an automatic debug or not.
#android.debug = False

# (bool) Skip APK build, it will not compile.
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = arm64-v8a

#
# Python for android (p4a) specific
#

# (str) python-for-android directory (deprecated)
#p4a.source_dir =

# (str) The directory used for bootstrap compilation.
#p4a.bootstrap = sdl2

# (str) Bootstrap to use for android builds (sdl2, webview, service_library or empty)
#p4a.bootstrap = sdl2

# (int) port number to specify an arbitrary port (default 0, random)
#p4a.port = 0

# (bool) Use --blacklist/whitelist for the app.
#p4a.blacklist_srcs =

# (int) overrides the default whitelist.
#p4a.whitelist_srcs =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
#android.arch = armeabi-v7a
