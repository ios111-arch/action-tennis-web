"""
Setup script for building ActionTennis.app using py2app
"""

from setuptools import setup

APP = ['action_tennis.py']
DATA_FILES = []
OPTIONS = {
    'iconfile': None,
    'plist': {
        'CFBundleName': 'ActionTennis',
        'CFBundleDisplayName': 'ActionTennis',
        'CFBundleGetInfoString': "ActionTennis Game",
        'CFBundleIdentifier': 'com.example.actiontennis',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright 2024',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13',
    }
}
// Test Github rule
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)