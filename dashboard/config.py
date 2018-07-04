# -*- coding: utf-8 -*-
import configparser
import os

config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config.read(os.path.normpath(os.getenv('SETTINGS_PATH')))
