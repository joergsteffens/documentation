#! /usr/bin/env python3
import os
import codecs
import shutil

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-l", "--lang", type=str, help="languages to build (en,de)")
parser.add_argument("-o", "--outputs", type=str, help="output formates (html,pdf)")
parser.add_argument("-f", "--files", type=str, help="docu files to build")
parser.add_argument("-t", "--theme", type=str, help="pdf theme to use (opsi)")
parser.add_argument("-s", "--stylesheet", type=str, help="html style to use (opsi)")
parser.add_argument("-p", "--project-path", type=str, help="path to docu project")
args = parser.parse_args()

print(args)

if not args.project_path:
	project_path = os.getcwd()
print(project_path)

languages = []
if args.lang:
	for lang in args.lang.split(","):
			languages.append(lang)
if len(languages) == 0:
	languages = ["de", "en"]

outputs = []
if args.outputs:
	for output in args.outputs.split(","):
		outputs.append(output)
if len(outputs) == 0:
	outputs = ["html", "pdf"]

input_files = []
if args.files:
	for f in args.files.split(","):
		input_files.append(f)

#-a pdf-style=conf/opsi-theme.yml
if args.theme:
	pdf_style = f"-a pdf-style={project_path}/conf/{args.theme}-theme.yml"
else:
	pdf_style = ""

if args.stylesheet:
	html_style = f"-a stylesdir={project_path}/conf/stylesheets -a stylesheet={args.stylesheet}.css"
else:
	html_style = ""

print(languages)
print(outputs)
print(input_files)
print(pdf_style)
print(html_style)


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
		# print(f"copy {f} to {destination}")
		shutil.copy(f"{source_dir}/{f}", destination)
	if html_style:
		print("copy css images")
		if os.path.exists(f"{destination}/opsi-css"):
			shutil.rmtree(f"{destination}/opsi-css")
		shutil.copytree(f"{project_path}/conf/stylesheets/images", f"{destination}/opsi-css")

def listdirs(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d.startswith("opsi")]

for lang in languages:
	print(listdirs(lang))
	
	for root, dirs, files in os.walk(lang):
		if "opsi" not in root:
			continue
		
		for f in files:
			if input_files and os.path.splitext(f)[0] not in input_files:
				continue
			root_basename = os.path.basename(root)
			print(f"{root_basename} --- {os.path.splitext(f)[0]}")
			if root_basename == os.path.splitext(f)[0]:
				print("########: ", f)
				source = os.path.join(root,f)
				for output in outputs:
					destination_folder = f"build/{lang}/{output}/{root_basename}"
					try:
						os.makedirs(destination_folder)
					except OSError:
						print ("Creation of the directory %s failed" % destination_folder)
					else:
						print ("Successfully created the directory %s " % destination_folder)

					destination = os.path.join(destination_folder, f"{root_basename}.{output}")
					if output == "pdf":
						print(f"asciidoctor -r asciidoctor-pdf -b pdf -a icons=font -a doctype=book -a icons=font {pdf_style} -a imagesdir=../images -D '{destination_folder}' {f}")
						os.system(f"asciidoctor -r asciidoctor-pdf -b pdf -a icons=font -a doctype=book -a icons=font {pdf_style} -a imagesdir=../images -D '{destination_folder}' {os.path.join(root, f)}")					
					if output == "html":
						print(f'asciidoctor -a encoding=UTF-8 -a doctype=book -a icons=font -a xrefstyle=full -a lang={lang} {html_style} --verbose  --out-file "{destination}" {source} ')
						os.system(f'asciidoctor -a encoding=UTF-8 -a doctype=book -a icons=font -a xrefstyle=full -a lang={lang} {html_style} --verbose  --out-file "{destination}" {source} ')
						copy_images(destination, f"{lang}/images", destination_folder)
					if output == "epub":
						shutil.copytree(f"{root}/../images", f"{root}/images")
						print(f"asciidoctor -r asciidoctor-epub3 -b epub3 -a icons=font -a doctype=book -a icons=font -a imagesdir=images -D '{destination_folder}' {f}")
						os.system(f"asciidoctor -r asciidoctor-epub3 -b epub3 -a icons=font -a doctype=book -a icons=font -a imagesdir=images -D '{destination_folder}' {os.path.join(root, f)}")
						shutil.rmtree(f"{root}/images")
		