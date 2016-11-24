from distutils.core import setup
import py2exe, sys, os
import cv2
import numpy
import PIL
from PIL import Image, ImageTk#
from PIL import ImageEnhance#
from Tkinter import *#
import tkFileDialog#
from tkFileDialog import askopenfilename#
import math#

sys.argv.append('py2exe')

setup(console=['ConstellationIdentifier.py'])
