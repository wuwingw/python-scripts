#!/usr/bin/env python

# SIMPLE FLASHCARDS

import argparse
import csv
import re
from random import shuffle

class FlashcardTester:

	FLASHCARD_LIST = []
	CSV_FILE = ""

	def main(self):

		# processing command line arguments

		parser = argparse.ArgumentParser(description="Test yourself on simple definitions etc.")
		parser.add_argument('filename', help='Path to the .csv file that contains the flashcard definitions.')
		args = parser.parse_args()

		if not ".csv" in args.filename:
			print "Please specify a .csv file."
			return

		self.CSV_FILE = args.filename
		print "Reading from:", self.CSV_FILE, "\n"

		# create dictreader and load all the flashcards into a list

		with open(self.CSV_FILE) as csvfile:
			reader = csv.DictReader(csvfile)
			self.FLASHCARD_LIST = list(reader)

		self.runRound()
		self.writeOutResults()


	def runRound(self):

		shuffle(self.FLASHCARD_LIST) # shuffles the list in place

		# commence testing

		nwrong = 0

		for cardno, flashcard in enumerate(self.FLASHCARD_LIST):
			self.printLine()
			print "Flashcard ",str(cardno+1)," out of ",str(len(self.FLASHCARD_LIST))
			self.printLine()
			correct = self.testFlashcard(flashcard)

			if not correct:
				nwrong += 1

		# print feedback

		self.printLine()
		print "Finished!"
		self.printLine()
		if nwrong == 0:
			print "You got all ", str(len(self.FLASHCARD_LIST)), " flashcards right! Well done!"
		else:
			print "You got ", str(nwrong), " flashcards wrong out of ", str(len(self.FLASHCARD_LIST)),"."


		print "\nWould you like to do another round? (y/n)"
		response = raw_input(">>> ")
		if response == "y":
			self.runRound()
		else:
			print "\nSee you again soon!"
			return

		
	def writeOutResults(self):

		with open(self.CSV_FILE, 'w') as csvfile:
			fieldnames = self.FLASHCARD_LIST[0].keys()
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			writer.writeheader()
			for flashcard in self.FLASHCARD_LIST:
				writer.writerow(flashcard)


	def printLine(self):
		print "------------------------------"

	def testFlashcard(self, flashcard):

		# a list of all the [terms]
		terms = re.findall(r'\[(.*?)\]', flashcard["text"])
		# remove the terms from the test string
		print re.subn(r'\[(.*?)\]',"_____",flashcard["text"])[0],"\n"

		guesses = [] # list of user's guesses
		for i in xrange(0,len(terms)):
			line = raw_input(">>> ")
			guesses.append(line)

		print ""

		wrong = 0
		for i in xrange(0,len(terms)):
			if guesses[i].lower() != terms[i].lower():
				print "You said: ", guesses[i], "\nThe correct answer is: ", terms[i]
				wrong += 1

		if wrong == 0:
			print "All correct!\n"
			flashcard['nright'] = int(flashcard['nright']) + 1
			return True
		else:
			print "You got ", str(wrong), " term wrong out of ", str(len(terms)), ".\n"
			flashcard['nwrong'] = int(flashcard['nwrong']) + 1
			return False


if __name__ == "__main__":

	tester = FlashcardTester()
	tester.main()