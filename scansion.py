#!/usr/bin/env python

# LATIN POETRY SCANSION SCRIPT

import sys

# TO DO:
# - some sort of backtracking?
# - counting syllables to figure out possible combinations of Ss and Ds
# - ellisions
# - text file input



vowels = ["a","e","i","o","u"]

diphthongs = ["ae","au","ei","eu","oe","ui"] # long syllable
combinedVowels = ["ue"] # one syllable but short

longEndingsUsual = ["o","i","u","as","es","os"] # usually long by nature
shortEndingsUsual = ["a","is","e","us"] # usually short by nature
shortEndingsAlways = ["am","em","um"] # always short by nature


singleConsonant = ["qu"] # counts as one consonant/letter
doubleConsonants = ["x","z"] # will lengthen a preceding vowel
digraphs = ["ch","ph","th"] # count as one consonant

mutes = ["b","c","d","g","p","t"]
softPairs = [ (x + "l") for x in mutes] # will not always lengthen a preceding vowel or h
softPairs = softPairs + [ (x + "r") for x in mutes]

ellisions = ["am","em","im","om","um"] # will elide with vowel at start of next word



def main():

	print "Welcome to the Latin Poetry Scansion Script!"

	# processing arguments

	if len(sys.argv) > 1 and sys.argv[1] == "-f": # reading from a file
		if len(sys.argv) == 2: # too few arguments
			print "Please specify the text file to scan."
			return
		else:
			filename = sys.argv[2]
			print "Scanning: " + filename
			return
	else: # get input from command line
		print "Type the poetry to be scanned, separating with single newlines: \n"
		textLines = [] # list of strings; each element is a line of poetry
		for line in iter(raw_input, ""):
			textLines.append(line)
		print textLines

	# scan line by line

	for line in textLines:
		wordSyllableList = splitIntoSyllables(line) # split into syllables
		scannedResult = scan(wordSyllableList)


def splitIntoSyllables(line):
	if line == "":
		return []

	# first split into words
	wordList = line.split(" ")

	wordSyllableList = []

	for word in wordList:
		syllables = []
		i = 0 # which letter we are up to; has not yet been added to a syllable
		while i < len(word):
			currentSyllable = ""

			# first pick up any consonants
			while not(word[i] in vowels):
				# detecting qu
				if (i < len(word) -1 and (word[i] + word[i+1] in singleConsonant)):
					currentSyllable = currentSyllable + word[i] + word[i+1]
					i += 2
					break

				currentSyllable = currentSyllable + word[i]
				i += 1
				if i >= len(word):
					break

			if i == len(word) - 1:
				# last letter must be a syllable
				currentSyllable = currentSyllable + word[i]
				syllables.append(currentSyllable)
				i += 1
				continue
		
			if word[i]+word[i+1] in diphthongs or word[i]+word[i+1] in combinedVowels: 	
				# combine vowels into single syllable
				currentSyllable = currentSyllable + word[i] +word[i+1]
				i += 2
				if i >= len(word):
					syllables.append(currentSyllable)
					break

				# get all succeeding consonants
				while not(word[i] in vowels):
					currentSyllable = currentSyllable + word[i]
					i += 1
					if i >= len(word):
						break
				syllables.append(currentSyllable)
				continue
			else:
				currentSyllable = currentSyllable + word[i]
				i += 1
				while not(word[i] in vowels):
					currentSyllable = currentSyllable + word[i]
					i += 1
					if i >= len(word):
						break
				syllables.append(currentSyllable)
				continue
		syllables[-1] = syllables[-1] + " "
		wordSyllableList =  wordSyllableList + syllables

	print wordSyllableList
	return wordSyllableList


def scan(wslist):
	scanned = [" " for x in wslist] # initialise to empty

	# first mark the known bits ||- ?????|-uu||-x||
	scanned[0] = "||-"
	scanned[-1] = "x||"
	scanned[-2] = "|-"
	scanned[-3] = "u|"
	scanned[-4] = "u"
	scanned[-5] = "|-"

	def containsOneOf(syllable, l):
		for x in l:
			if x in syllable:
				return True
		return False

	def markLong(i):

		def doTheMark(i):
			original = scanned[i]
			if scanned[i+1] == "u":
				scanned[i] = "|-"
				return True
			elif scanned[i+1] == "u|":
				return False
			elif scanned[i+1] == "-|":
				scanned[i] = "|-"
				if scanned[i-1] == "-":
					original2 = scanned[i-1]
					success = markLong(i-1)
					if success:
						return True
					else:
						scanned[i-1] = original2
						scanned[i] = original
						return False					
			elif scanned[i+1] == "|-":
				scanned[i] = "-|"
				# know the one before must be long
				original2 = scanned[i-1]
				success = markLong(i-1)
				if success:
					return True
				else:
					scanned[i-1] = original2
					scanned[i] = original
					return False
			elif scanned[i-1] == "u":
				return False
			elif scanned[i-1] == "u|":
				scanned[i] = "|-"
				return True
			elif scanned[i-1] == "-|":
				scanned[i] = "|-"
				return True
			elif scanned[i-1] == "|-":
				scanned[i] = "-|"
				return True
			elif scanned[i+1] == "-" or scanned[i-1] == "-":
				scanned[i] = "-"
				return True
			elif scanned[i+1] == " " or scanned[i-1] == " ":
				scanned[i] = "-"
				return True
			else:
				raise ValueError("Trying to mark long at " + str(i) + ". Before: " + scanned[i-1] + ", After: " + scanned[i+1])

		success = doTheMark(i)
		if success:
			return True
		else:
			print "Inconsistent. Was trying to mark " + str(i)

	# make one pass forwards through the array marking things that are definitely long

	for i in xrange(1,len(wslist)-5):

		print "CURRENT SYLLABLE: " + wslist[i]

		# check diphthongs
		if containsOneOf(wslist[i], diphthongs):
			markLong(i)
			continue

		# check long by position

		currentSyllable = wslist[i]
		nextSyllable = wslist[i+1]

		# get consonants at start of next syllable
		for letter in nextSyllable:
			if not(letter in vowels):
				currentSyllable = currentSyllable + letter
			else:
				break

		# count consecutive consonants from end of string
		endConsonants = ""
		for letter in reversed(currentSyllable):
			if not(letter in vowels):
				if not(letter == " "):
					endConsonants = letter + endConsonants
			else:
				break
		print "END CONSONANTS: " + endConsonants

		if len(endConsonants) > 2:
			markLong(i)
			continue
		elif len(endConsonants) == 2:
			if not(endConsonants in digraphs):
				if not(endConsonants in softPairs):
					markLong(i)
					continue
				else:
					# markMaybeLong(i) ?
					pass
			# otherwise could be short or long - don't know
			continue
		elif len(endConsonants) == 1:
			if endConsonants in doubleConsonants:
				markLong(i)
				continue
			else:
				# don't know
				continue

	print scanned

	# fill in any obvious gaps between longs
	for i in xrange(1,len(wslist)-4):
		if scanned[i] == "|-":
			if "-" in scanned[i-2]:
				print "found a gap at: " + str(i-1)
				markLong(i-1)
			if "-" in scanned[i+2]:
				print "found a gap at: " + str(i+1)
				markLong(i+1)

	print scanned

	# try to figure out the rest by counting

	# count the full feet
	fullFeet = 2 # know we have two full feet at the end
	footLoose = [] # the syllables that aren't in a proper foot yet
	i = 0
	while i < len(wslist)-5:
		if scanned[i] == "|-":
			if scanned[i+1] == "-|" or scanned[i+1] + scanned[i+2] == "uu|":
				fullFeet += 1
				i += 2
				continue
		footLoose.append(i)
		i += 1

	print "FULL FEET: " + str(fullFeet)
	print footLoose
	print len(footLoose)

	missingFeet = 6 - fullFeet

	if 2 * missingFeet == len(footLoose):
		# must all be spondaes
		print "spondaeess"
		k = 0
		while k < len(footLoose):
			assert (footLoose[k] == footLoose[k+1]-1)
			scanned[footLoose[k]] = "|-"
			scanned[footLoose[k+1]] = "-|"
			k += 2
		print "SUCCESS"
	elif 3 * missingFeet == len(footLoose):
		# must all be dactyls
		print "dactyls"

		# check we have one spondae per missing foot, or less
		looseSyllables = [scanned[k] for k in footLoose]
		if (len([x for x in looseSyllables if "-" in x]) > missingFeet):
			print "Something's gone wrong."
		
		# fill in the missing feet
		k = 0
		while k < len(footLoose):
			assert (footLoose[k] == footLoose[k+1]-1 and footLoose[k] == footLoose[k+2]-2)
			scanned[footLoose[k]] = "|-"
			scanned[footLoose[k+1]] = "u"
			scanned[footLoose[k+2]] = "u|"
			k += 3
		print "SUCCESS"

	print scanned








if __name__ == "__main__":
	main()
