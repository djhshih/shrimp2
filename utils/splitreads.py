#!/usr/bin/python
#	$Id: splitreads.py,v 1.3 2009/03/06 18:58:49 rumble Exp $

import sys
from utils import *

if len(sys.argv) != 3 and len(sys.argv) != 4:
	print >> sys.stderr, "usage: %s [--paired | -p] <reads_per_file|pairs_per_file> <fasta_file>" % (sys.argv[0])
	sys.exit(1)

if sys.argv[1] == '--paired' or sys.argv[1] == '-p':
	mode = 'paired'
	mod = 1
else:
	mode = 'unpaired'
	mod = 0

READS_PER_FILE = int(sys.argv[1+mod])

if mode == 'paired':
	READS_PER_FILE *= 2

out = None
readsdone = 0

suffix = "fasta"
if sys.argv[2].lower().strip().endswith(".csfasta"):
	suffix = "csfasta"
elif sys.argv[2].lower().strip().endswith(".csfa"):
	suffix = "csfa"
elif sys.argv[2].lower().strip().endswith(".fa"):
	suffix = "fa"

fd = open_gz_or_ascii(sys.argv[2+mod])
for line in fd:
	if line.startswith("#"):
		continue

	if line.startswith(">") and (readsdone % READS_PER_FILE) == 0:
		if out != None:
			out.close()

		fname = "%u_to_%u.%s" % (readsdone, readsdone + READS_PER_FILE - 1, suffix)

		out = open(fname, "w")

	out.write(line)

	if line.startswith(">"):
		readsdone = readsdone + 1

if out != None:
	out.close()
