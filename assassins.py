#!/usr/bin/env python

# ASSASSINS

# everybody in a group is assigned the name of somebody else in the group that they must 'assassinate'
# this is done by handing them a certain object in a certain location
# this script generates the assignments for you
# avoiding the problems that may arise if you just draw names out of hat
# namely, getting yourself, and people trying to assassinate each other

import argparse
import os
from random import randint
from random import shuffle

class Assassins:

	playerNames = []
	locationNames = []
	objectNames = []

	def main(self):

		parser = argparse.ArgumentParser(description="Assign a target, location and object to every person.")

		nameList = []
		print "Please input the names of the players (one name per line): \n"
		for line in iter(raw_input, ""):
			if line not in nameList:
				self.playerNames.append({ "name" : line, "targeted" : False })
				nameList.append(line)
			else:
				print "Everybody must have a different name! The duplicate will be ignored."
				continue
		print ""

		print "Please input ", str(len(self.playerNames)), " locations: \n"
		for i in xrange(0,len(self.playerNames)):
			self.locationNames.append(raw_input())
		print ""

		print "Please input ", str(len(self.playerNames)), " objects: \n"
		for i in xrange(0,len(self.playerNames)):
			self.objectNames.append(raw_input())
		print ""

		self.assignTargets()

		print "Okay! Form a queue in the order you typed in the names: "
		print ", ".join(nameList)
		print "\nCome up one by one to receive your target, location and object."
		print "Hit ENTER once and the three names will be displayed."
		print "When you are finished reading, hit ENTER once to clear the terminal."

		print "" 

		print self.playerNames[0]["name"] + ", up you come!\n\n"

		for player in self.playerNames:
			print "Hello, " + player["name"] + ".\n"

			raw_input("Hit ENTER to reveal your assignment.\n")
			print "TARGET: ", player["target"]
			print "LOCATION: ", player["location"]
			print "OBJECT: ", player["object"]
			
			raw_input("\nHit ENTER to clear the screen.")
			os.system("cls")
			os.system("clear")

		print "Everybody has received their assignments. Good luck!"
		return

	def assignTargets(self):

		shuffleme = list(xrange(0,len(self.playerNames)))

		for player in self.playerNames:

			target = player
			shuffle(shuffleme)

			# we want to select a target that is:
			# not already targeted, not the player, and not targeting the player
			for i in shuffleme:
				target = self.playerNames[i]
				if (target["targeted"] == False and target != player and target.get("target") != player["name"]):
					target["targeted"] = True
					player["target"] = target["name"]
					break

			player["location"] = self.locationNames.pop(randint(0,len(self.locationNames)-1))
			player["object"] = self.objectNames.pop(randint(0,len(self.objectNames)-1))


if __name__ == "__main__":

	assassins = Assassins()
	assassins.main()