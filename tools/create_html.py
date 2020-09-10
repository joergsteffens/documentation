#! /usr/bin/env python3
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--source", type=str, help="source file")
parser.add_argument("-d", "--destination", type=str, help="Destination folder")
parser.add_argument("-I", "--image_path", type=str, help="image folder")
args = parser.parse_args()

source = args.source
destination_folder = args.destination
image_path = args.image_path



print(source)
print(destination_folder)


try:
    os.makedirs(destination_folder)
except OSError:
    print ("Creation of the directory %s failed" % destination_folder)
else:
    print ("Successfully created the directory %s " % destination_folder)

destination_file = os.path.basename(source)
destination_file = f"{os.path.splitext(destination_file)[0]}.html"
destination_file_path = os.path.join(destination_folder, destination_file)

print(destination_file_path)


os.system(f'asciidoctor -a encoding=UTF-8 -a doctype=book -a imagedir="{image_path}" -a lang=de --verbose  --out-file "{destination_file_path}" {source} ')
