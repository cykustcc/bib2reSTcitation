#Author Yukun Chen
#email: cykustc@gmail.com
#Date: Sept 04 2015

import getopt
import argparse
import sys
import re

from collections import defaultdict

def displaymatch(match):
    if match is None:
        return None
    return '<Match: %r, groups=%r>' % (match.group(), match.groups())


def bib2rest(input_bibfile,output_txtfile):
	print input_bibfile
	print output_txtfile
	start_pattern = re.compile(r"^(?: |\t)*\@(?:book|article|incollection|inproceedings)\{([a-z0-9]+), *$")
	title_pattern = re.compile(r"^(?: |\t)*title=\{([a-zA-Z0-9 ]+)\}(?: |\t)*,(?: |\t)*$")
	author_pattern = re.compile(r"^(?: |\t)*author=\{([a-zA-Z0-9 ,;\.\-]+)\}(?: |\t)*,(?: |\t)*$")
	other_info_pattern = re.compile(r"^(?: |\t)*(?:journal|volume|number|year|publisher|pages|organization|booktitle)=\{([a-zA-Z0-9 ,;\.-]+)\}(?: |\t)*,(?: |\t)*$")
	end_pattern = re.compile("^(?: |\t)*}(?: |\t)*$")
	with open(input_bibfile,'rb') as input_handle:
		with open(output_txtfile,'wb') as output_handle:
			in_a_bib_block = False;
			rest_ref_block = "";
			title = "";
			author = "";
			ref="";
			output_handle.write(".. _references:\n\n==========\nReferences\n==========\n\n")
			for line in input_handle:
				if not in_a_bib_block:
					# not in a bib block
					if start_pattern.match(line):
						matches = start_pattern.match(line)
						in_a_bib_block = True
						ref = matches.group(1)
					else:
						pass
		
				else:
					# in a bib block
					if end_pattern.match(line):
						matches = end_pattern.match(line)
						in_a_bib_block = False
						rest_ref_block = ".. [" + ref +"]" + " " + author +", " + title +", " + other_info 
						output_handle.write(rest_ref_block+"\n\n")
					elif title_pattern.match(line):
						matches = title_pattern.match(line)
						title = matches.group(1)
					elif author_pattern.match(line):
						matches = author_pattern.match(line)
						author = matches.group(1)
					elif other_info_pattern.match(line):
						matches = other_info_pattern.match(line)
						other_info = matches.group(1)
						rest_ref_block = rest_ref_block + ", "+ other_info
					else:
						pass



if __name__ == '__main__':
	throot = "/".join(sys.path[0].split("/")[:])
	parser = argparse.ArgumentParser(description='bib2reSTcitation is a tool to convert bib tex file to reStructuredText Markup citation format.')
	parser.add_argument('-o', '--output', help='output file path')
	parser.add_argument('-i', '--input', help='input file path')
	args = parser.parse_args()
	input_file = args.input
	if input_file==None:
		input_file = 'tex.bib'
	output_file = args.output
	if output_file==None:
		output_file = "references.txt"
	bib2rest(input_file,output_file)
	