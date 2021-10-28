'''
	Author:	Nicholas Mattei
	Org:	NICTA and UNSW
	Date:	25 Sept. 2014
			10 Oct. 2015
	
	Description:
	This file checks the output of a wedding seat problem.  To do this 
	we take 2 arguments, the input to the solver, and the solver output.
	Note that this only checks that the happiness adds up; it does not 
	verify optimality.
	
	The input to the solver shall have the following form:
	
%Wedding Seat Assignment Data File.
%Evaluation (0 = Utilitarian, 1 = Egalitarian)
Evaluation = 0;

%Number of Tables
nTables = 3;

%Number of Seats per Table:
nSeats = 3;

%Number of Guests:
nGuests = 9;

nGroups = 3;
%Groups that Must be seated together
Groups = [{1,3},
          {5,6},
          {8,9}];

%Pref Weight
PrefWeight = 3;
%Preference Graph: Row i is the person that Guest i would like to sit with.
%There must be as many rows as nGuests.
Pref = [{2,3,4},
        {1,6,9},
        {1,4},
        {3,9},
        {6},
        {5},
        {1,8,9},
        {7,9},
        {4}];

%Troublemakers
Trouble = {2, 3};

	Note that we will discard any line starting with a %.
	The variable names should lead the corresponding line;
	otherwise this will not parse correctly.
'''
def clean(x):
	remove = ["{", "}", ";", "]", "["]
	for i in remove:
		x = x.replace(i, "")
	return x


def parseData(inf):
	nTables = -1
	nSeats = -1
	nGuests = -1
	nGroups = -1
	Groups = [-1]
	PrefWeight = -1
	Pref = {-1:-1}
	
	lines = inf.readlines()
	for ln in range(len(lines)):
		cline = lines[ln]
		if len(cline.strip()) > 0 and cline.strip()[0] != "%":
			bits = cline.strip().split("=")
			if bits[0].strip() == "nTables":
				nTables = int(bits[1].strip().replace(";", ""))
			if bits[0].strip() == "nSeats":
				nSeats = int(bits[1].strip().replace(";", ""))
			if bits[0].strip() == "nGuests":
				nGuests = int(bits[1].strip().replace(";", ""))
			if bits[0].strip() == "nGroups":
				nGroups = int(bits[1].strip().replace(";", ""))
			if bits[0].strip() == "PrefWeight":
				PrefWeight = int(bits[1].strip().replace(";", ""))
			if bits[0].strip() == "Trouble":
				t = bits[1].strip().replace(";", "")
				t = t.replace("{", "")
				t = t.replace("}", "")
				n = t.strip().split(",")
				Trouble = [int(x.strip()) for x in n]


			if bits[0].strip() == "Groups":
				#Groups must have line + nGroups more, bomb if we haven't caught nGroups.
				if not nGuests > 0:
					print("***** ERROR: nGroups must appear before the Groups matrix.")
					exit()
				Groups = []
				for i in range(1, nGroups+1):
					kn = lines[ln + i].strip()
					kn = clean(kn)
					kn = kn.split(",")
					kn = [int(x.strip()) for x in kn if x != ""]
					Groups.append(kn)

			if bits[0].strip() == "Pref":
				#Groups must have line + nGuests more, bomb if we haven't caught nGuests.
				if not nGuests > 0:
					print("***** ERROR: nGuests must appear before the Pref matrix.")
					exit()
				Pref = {}
				for i in range(1, nGuests+1):
					kn = lines[ln + i].strip()
					kn = clean(kn)
					kn = kn.split(",")
					kn = [int(x.strip()) for x in kn if x != '']
					Pref[i] = kn
		

	print("***** Parsed the following: ")
	print("nTables = " + str(nTables))
	print("nSeats = " + str(nSeats))
	print("nGuests = " + str(nGuests))
	print("nGroups = " + str(nGroups))
	print("PrefWeight = " + str(PrefWeight))
	print("Trouble = " + str(Trouble))


	print("Groups = ")
	for i in Groups:
		print(str(i) + " must sit together.")

	print("Preferences = ")
	for i in Pref.keys():
		print(str(i) + " preferes to sit with " + str(Pref[i]))

	if nTables == -1 or nSeats == -1 or nGuests == -1 or nGroups == -1 or PrefWeight == -1 or Pref == {-1:-1} or Groups == {-1,-1}:
		print("***** ERROR: There were not enough parameters in the datafile.")
		exit()

	return nTables, nSeats, nGuests, nGroups, PrefWeight, Pref, Groups, Trouble
		
'''	
	
	The output shall have the following form:
	
Table: Guests:
   1 : {1, 3, 4}
   2 : {2, 5, 6}
   3 : 7..9
Mom's Happiness: 21
----------

	Line 1: the header is not checked in this parser.  It is appropriate
	to use the .. relation.  The solution checker will ensure the constraints
	are met by the proposed solution.
'''
def parseSolution(inf, nTables):
	Tables = {}
	#first line is not useful.
	inf.readline()
	lines = inf.readlines()
	#neither is the last...
	for i in range(nTables):
		assn = lines[i].split(":")[1].strip()
		if assn[0] == "{":
			assn = assn.replace("{", "")
			assn = assn.replace("}", "")	
			assn = assn.split(",")
			if len(assn) > 0 and assn[0] != "":
				#strip off the possible last element if they have the comma problem
				if assn[len(assn)-1].strip() == "":
					assn = assn[:len(assn)-1]
			if len(assn) > 0 and assn[0] != "":
				items = [int(x.strip()) for x in assn]
				Tables[i+1] = items
			else:
				Tables[i+1] = []
		else:
			assn = lines[i].split(":")[1].strip()
			bits = assn.split("..")
			start = int(bits[0].strip())
			end = int(bits[1].strip())
			items = [x for x in range(start, end+1)]
			Tables[i+1] = items

	# Util Happiness is the next line...
	util = lines[nTables]
	util = util.split(":")
	util = int(util[1].strip())

	egal = lines[nTables+1]
	egal = egal.split(":")
	egal = int(egal[1].strip()) 
	
	print("***** Parsed the following solution....")
	print("Table:    Guests:")
	for i in sorted(Tables.keys()):
		print(str(i) + "   :" + str(Tables[i]))
	print("Utilitarian Happiness: " + str(util))
	print("Egalitarian Happiness: " + str(egal))

	return Tables, util, egal

#Give us access to the command line arguments.
import sys 


if __name__ == '__main__':
	if(len(sys.argv) != 3):
		print("Use: " + str(sys.argv[0]) + " <Input Data File> <Solution Output> \n")
		sys.exit()
		
	#Open and parse the inputfile.
	print("***** Reading specification file.....")
	inf = open(sys.argv[1], "r")
	nTables, nSeats, nGuests, nGroups, PrefWeight, Pref, Groups, Trouble = parseData(inf)
	inf.close()

	#Open and parse the solution..
	print("***** Read Solution File")
	inf = open(sys.argv[2], "r")
	Tables, util, egal = parseSolution(inf, nTables)
	inf.close()

	#Build a lookup table so we have Guest --> Table no.
	People = {}
	for i in sorted(Tables.keys()):
		for p in Tables[i]:
			People[p] = i
	
	# Verify the conditions...
	solution = True
	if len(Tables.keys()) != nTables:
		print("***** There are not the same number of Tables as nTables!")
		solution = False
	
	if len(People.keys()) != nGuests:
		print("***** There are a different number of guests than nGuests!")
		solution = False
	
	for i in Tables.values():
		if len(i) > nSeats:
			print("***** There are more people at a table than nSeats!")
			solution = False
	
	for i in Tables.values():
		if len(i) < nSeats//2:
			print("***** There are not floor(nSeats/2) people at a table!")
			solution = False

	for i in Tables.values():
		if len(set(i).intersection(Trouble)) > 1:
			print("***** There are more Troublemakers at a table than allowed!")
			solution = False
	
	for i in Groups:
		if not all(People[i[0]] == People[x] for x in i):
			print("***** Group " + str(i) + " is not all seated together!")
			solution = False

	#Compute Satisfaction of this assignment...
	TotalHappy = 0
	for i in People.keys():
		for j in Pref[i]:
			if People[i] == People[j]:
				TotalHappy += PrefWeight
	
	#Compute Egal...
	EgalHappy = PrefWeight * 100
	for i in People.keys():
		t = 0
		for j in Pref[i]:
			if People[i] == People[j]:
				t += PrefWeight
		print(t)
		if t < EgalHappy:
			EgalHappy = t


	if TotalHappy != util:
		print("***** Utilitarian Happiness is not being correctly computed...")
		solution = False
	if EgalHappy != egal:
		print("***** Egalitarian Happiness is not being correctly computed...")
		solution = False

	if solution:
		print("***** GREAT! This is a valid problem and solution!")