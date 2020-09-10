#! /usr/bin/env python3
import argparse
import os
import codecs
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", type=str, help="HTML file")
parser.add_argument("-s", "--source_dir", type=str, help="Image source dir")
parser.add_argument("-d", "--destination", type=str, help="Destination folder")
args = parser.parse_args()

print(args.filename)
filename = args.filename
source_dir = args.source_dir
destination = args.destination

img_lines = []
img_files = []
with codecs.open(filename, "r") as html:
	for line in html:
		if "<img src=" in line:
			img_line = line.split("\"")
			for s in img_line:
				if ".png" in s or ".jpg" in s or ".jpeg" in s:
					img_files.append(s)


for f in img_files:
	print(f"copy {f} to {destination}")
	shutil.copy(f"{source_dir}/{f}", destination)

