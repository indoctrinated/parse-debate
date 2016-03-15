#!/usr/bin/python
# parse-debate by Alex Campbell <alex@alexthejourno.com>
#
# This program's purpose is to parse and pull data about keywords from
# debates or interviews, keeping track of hits from each speaker.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import re

# Let's get all of our arguments sorted out.
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", nargs='+', type=str, help="Input file to read", required=True)
parser.add_argument("-v", "--verbose", help="Verbose output", action="count", default=0)
parser.add_argument("-t", "--terms", help="Comma delinated list of terms to search for", required=True)
# parser.add_argument("-w", "--write", help="Output lines for each speaker into their own files", action="store_true")
parser.add_argument("-o", "--output", help="Write CSV output results data to file", action="store_true")
parser.add_argument("-s", "--silent", help="Prints output to std out", action="store_true")
parser.add_argument("-c", "--case", help="Preserve case sensitivity in search for terms", action="store_true", default=False)

# Handle inputs
args = parser.parse_args()

# init our data structure:
# data
# - term
#   - file
#     - name:occurances
#
data = {}


# Make a table for each of our terms
terms = args.terms.split(",")
for term in terms:
	data[term] = []

# Pattern that finds speakers (taken out of a loop to save time)
speaker_pattern = re.compile("^(?P<name>[A-Z]([A-Z]|[a-z])+):\s")

# Keep a list of all speakers encountered. This will come in handy later
speaker_list = []

# Now read through the files
for findex,fname in enumerate(args.file):
	# Populate files for each term
	for term in terms:
		data[term].append({})
		i = len(data[term]) - 1
	try:
		f = open(fname, "r")
		current_speaker = None
		for line in f:	
			# Find out if we have a new speaker
			has_speaker = speaker_pattern.search(line)
			if has_speaker:
				current_speaker = has_speaker.group("name").upper()
				# See if we already have the speaker in our list of speakers
				if not (current_speaker in speaker_list):
					speaker_list.append(current_speaker)
			# Don't bother searching paragraphs that don't belong to anyone
			if current_speaker:
				for term in terms:
					# Check for case-sensitive searches
					if args.case:
						data[term][i][current_speaker] = data[term][i].get(current_speaker, 0) + line.count(term)
					# Case insensitive searches
					else:
						
						data[term][i][current_speaker] = data[term][i].get(current_speaker, 0) + line.lower().count(term.lower())
						#print data		
	except IOError:
		print "Error: Could not read \"" + fname + "\"\n"
		exit()
	finally:
		f.close()

# Let's write out the data
for term in terms:
	# Create the CSV header
	out = "speaker"
	for fname in args.file:
		out += "," + fname
	out += "\n"

	# Create one row for each speaker, one column for each file
	for speaker in speaker_list:
		out += speaker
		for findex,fname in enumerate(args.file):
			out += "," + str(data[term][findex][speaker])
		out += "\n"
	
	# Write to screen
	if not args.silent:
		print "Term: " + term + "\n" + out

	# Write to file
	if args.output:
		try:
			f = open(term + "-results.csv", "w")
			f.write(out)
		except IOError:
			print "Error: could not write \"" + term + "-results.csv\"\n"
			exit()
		finally:
			f.close()
	

exit()
		















