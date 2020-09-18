#! /usr/bin/env python3
import os
import codecs
import shutil

languages = ["de", "en"]
outputs = ["html", "pdf"]

def copy_images(filename, source_dir, destination):
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

def listdirs(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d.startswith("opsi")]

for lang in languages:
	print(listdirs(lang))
	
	for root, dirs, files in os.walk(lang):
		if "opsi" not in root:
			continue
		
		for f in files:
			root_basename = os.path.basename(root)
			print(f"{root_basename} --- {os.path.splitext(f)[0]}")
			if root_basename == os.path.splitext(f)[0]:
				print("########: ", f)
				source = os.path.join(root,f)
				for output in outputs:
					destination_folder = f"build-test/{lang}/{output}/{root_basename}"
					try:
						os.makedirs(destination_folder)
					except OSError:
						print ("Creation of the directory %s failed" % destination_folder)
					else:
						print ("Successfully created the directory %s " % destination_folder)

					destination = os.path.join(destination_folder, f"{root_basename}.{output}")
					if output == "pdf":
						print(f"asciidoctor -r asciidoctor-pdf -b pdf -a icons=font -a doctype=book -a icons=font -a pdf-style=conf/pdf-theme.yml -a imagesdir=../images -D '{destination_folder}' {f}")
						os.system(f"asciidoctor -r asciidoctor-pdf -b pdf -a icons=font -a doctype=book -a icons=font -a pdf-style=conf/pdf-theme.yml -a imagesdir=../images -D '{destination_folder}' {os.path.join(root, f)}")					
					if output == "html":
						os.system(f'asciidoctor -a encoding=UTF-8 -a doctype=book -a icons=font -a xrefstyle=full -a lang={lang} --verbose  --out-file "{destination}" {source} ')
						copy_images(destination, f"{lang}/images", destination_folder)

		# print("root: %s", root)
		# print("dirs: %s", dirs)
		# print("files: %s", files)

