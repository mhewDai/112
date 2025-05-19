#################################################
# hw8py.
# Your name:Matthew Dai
# Your andrew id:mdai2
#################################################

import cs112_s22_week8_linter
from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Midterm1 Free Responses
#################################################
def digitCount(n):
    counter = 0
    if n == 0:
        return 1
    while n > 0:
        counter += 1
        n //= 10
    return counter

def isPreSquareNumber(n):
    length = digitCount(n)
    tempN = n
    for i in range(1,length): 
        leftPart = n % 10 ** i
        rightPart = tempN // 10 ** i
        #checks the left part and the right part to see if the left is a square
        if leftPart == rightPart**2:
            return True         
    return False

def nearestPreSquareNumber(n):
    tempN = n
    while not isPreSquareNumber(tempN):
        if isPreSquareNumber(n):
            return n
        if n < 0:
            tempN += 1
        else:
            n += 1   
            tempN -= 1
    return tempN     

def points(L,team):
    #finds the two team scores
    place = L.index(team)
    teamScore = L[place+1]
    opponentScore = L[len(L)-1] if place == 0 else L[1]
    return teamScore,opponentScore

def getRecord(team,scores):
    win,loss,tie = 0,0,0
    L = []
    for games in scores.splitlines():
        for words in games.strip().split(' '):
            L.append(words)
            #takes the characters in the line and transfers to a list to index
        if team in L:
            teamScore,opponentScore = points(L,team)
            teamScore,opponentScore = int(teamScore),int(opponentScore)
            if teamScore > opponentScore:
            #win case
                win += 1
            elif teamScore < opponentScore:
            #loss case
                loss += 1
            else:
            #tie case
                tie += 1
        L = []
    return win,loss,tie

#################################################
# Other Classes and Functions for you to write
#################################################

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.friends = []
        self.friendsName = set()
        
    def getName(self):
        return self.name

    def getAge(self):
        return self.age

    def addFriend(self,friend):
        if friend not in self.friends:
        #if the person is not friends then its added to each others list
            self.friends.append(friend)
            friend.friends.append(self)

    def addFriends(self,friend):
        for persons in friend.friends:
        #adds all the friends in list to list
            self.friends.append(persons)  

    def getFriends(self):
        L = []
        for elements in self.friends:
            if elements not in L:
                L.append(elements)
        return L

    def getFriendsNames(self):
        L = []
        for elements in self.friends:
            self.friendsName.add(elements.name)
        for elements1 in self.friendsName:
            L.append(elements1)
        L.sort()
        #sorts the list 
        return L

def getPairSum(L, target):
    s = set()
    pair1 = ()
    diff = 0
    for elems in L:
    #checks if the current number has a sum pair inside the set of past numbers
        diff = target - elems
        if diff not in s:
            s.add(elems)
        else:
            pair1 = diff, elems
    #if the tuple is empty then no pairs were found
    if pair1 == ():
        return None
    return pair1

def containsPythagoreanTriple(L):
    s = set(L)
    dupeS = set()
    for i in range(len(L)-1):
        for j in range(i,len(L)):
            #chooses two numbers and see if the third side is in the set
            (thirdSideType1,thirdSideType2) = ((L[i]**2 + L[j]**2)**0.5,
            abs((L[j]**2 - L[i]**2)**0.5)) 
            if (thirdSideType1 in s or thirdSideType2 in s 
                and L[i] not in dupeS and L[j] not in dupeS):
                return True
    return False

def movieAwards(oscarResults):
    movieDict = dict()
    for award, movie in oscarResults:
        #the number of times the movie appears, it is noted in the dictionary
        movieDict[movie] = movieDict.get(movie,0) + 1
    return movieDict

def friendsOfFriends(friends):
    newFriendDict = dict()
    setOfFriends = set()
    for people in friends:
        friend = friends[people]
        newFriendDict[people] = newFriendDict.get(people,0)
        for elems in friend:
            potentialFriends = friends[elems]
            for elems2 in potentialFriends:
                #checks if the friend is a friend and 
                #if the friend's friend is a friend 
                #if both of these cases are not true then it adds to a set
                if elems2 not in friend and elems2 not in setOfFriends:
                    if elems2 != people:
                        setOfFriends.add(elems2)
        newFriendDict[people] = setOfFriends
        setOfFriends = set()
    return newFriendDict

#################################################
# Bonus Animation
#################################################

def bonus_appStarted(app):
    app.counter = 0
    app.rectangles = []

def bonus_keyPressed(app, event):
    pass

def bonus_mousePressed(app, event):
    pass

def bonus_timerFired(app):
    if len(app.rectangles) < 20:
        coords = 30,20 + 5*app.counter
        app.rectangles.append(coords)
    app.counter += 1

def bonus_redrawAll(app, canvas):
    canvas.create_text(app.width/2, 0,
                       text=f'Selection Sort', font='Arial 25 bold', 
                       fill = 'black', anchor = N)
    for x, y in app.rectangles:
        canvas.create_text(20+15*(app.counter+0.5), 250, 
                            text='hi',fill = 'black',font='Arial 15 bold')
        canvas.create_rectangle(0,200,0 + x,200+y, 
                                fill = 'white',outline = 'black')

def bonusAnimation():
    runApp(width=400, height=400, fnPrefix='bonus_')

#################################################
# Test Functions
#################################################

def testNearestPreSquareNumber():
    print('Testing nearestPreSquareNumber(n)...', end='')
    assert(nearestPreSquareNumber(0) == 11)
    assert(nearestPreSquareNumber(6000) == 6036)
    assert(nearestPreSquareNumber(-100) == 11)
    #Negatives should still work
    assert(nearestPreSquareNumber(20202) == 20004)
    #Halfway between 20004 and 20400
    assert(nearestPreSquareNumber(30100) == 30009)
    #Some solutions may be too slow!
    print('Passed!')

def testGetRecord():
    print('Testing getRecord()...', end='')
    scores = '''\
    Chi 2 - Pit 1
    Chi 2 - Pit 11
    Mia 13 - Pit 0
    Pit 4 - Mia 4
    Chi 2 - Mia 3'''
    assert(getRecord('Pit', scores) == (1, 2, 1))
    assert(getRecord('Mia', scores) == (2, 0, 1))
    assert(getRecord('Chi', scores) == (1, 2, 0))
    assert(getRecord('Det', scores) == (0, 0, 0))
    print('Passed')

def testPersonClass():
    print('Testing Person Class...', end='')
    fred = Person('fred', 32)
    # Note that fred != "fred" - one is an object, and the other is a string.
    assert(isinstance(fred, Person))
    assert(fred.getName() == 'fred')
    assert(fred.getAge() == 32)
    # Note: person.getFriends() returns a list of Person objects who
    #       are the friends of this person, listed in the order that
    #       they were added.
    # Note: person.getFriendNames() returns a list of strings, the
    #       names of the friends of this person.  This list is sorted!
    assert(fred.getFriends() == [ ])
    assert(fred.getFriendsNames() == [ ])

    wilma = Person('wilma', 35)
    assert(wilma.getName() == 'wilma')
    assert(wilma.getAge() == 35)
    assert(wilma.getFriends() == [ ])

    wilma.addFriend(fred)
    assert(wilma.getFriends() == [fred])
    assert(wilma.getFriendsNames() == ['fred'])
    assert(fred.getFriends() == [wilma]) # friends are mutual!
    assert(fred.getFriendsNames() == ['wilma'])

    wilma.addFriend(fred)
    assert(wilma.getFriends() == [fred]) # don't add twice!

    betty = Person('betty', 29)
    fred.addFriend(betty)
    assert(fred.getFriendsNames() == ['betty', 'wilma'])

    pebbles = Person('pebbles', 4)
    betty.addFriend(pebbles)
    assert(betty.getFriendsNames() == ['fred', 'pebbles'])

    barney = Person('barney', 28)
    barney.addFriend(pebbles)
    barney.addFriend(betty)
    barney.addFriends(fred) # add ALL of Fred's friends as Barney's friends
    assert(barney.getFriends() == [pebbles, betty, wilma])
    assert(barney.getFriendsNames() == ['betty', 'pebbles', 'wilma'])
    fred.addFriend(wilma)
    fred.addFriend(barney)
    assert(fred.getFriends() == [wilma, betty, barney])
    assert(fred.getFriendsNames() == ['barney', 'betty', 'wilma']) # sorted!
    assert(barney.getFriends() == [pebbles, betty, wilma, fred])
    assert(barney.getFriendsNames() == ['betty', 'fred', 'pebbles', 'wilma'])
    print('Passed!')

def testGetPairSum():
    print("Testing getPairSum()...", end="")
    assert(getPairSum([1], 1) == None)
    assert(getPairSum([5, 2], 7) in [ (5, 2), (2, 5) ])
    assert(getPairSum([10, -1, 1, -8, 3, 1], 2) in
                      [ (10, -8), (-8, 10),(-1, 3), (3, -1), (1, 1) ])
    assert(getPairSum([10, -1, 1, -8, 3, 1], 10) == None)
    assert(getPairSum([10, -1, 1, -8, 3, 1, 8, 19, 0, 5], 10) in
                      [ (10, 0), (0, 10)] )
    assert(getPairSum([10, -1, 1, -8, 3, 1, 8, 19, -9, 5], 10) in
                      [ (19, -9), (-9, 19)] )
    assert(getPairSum([1, 4, 3], 2) == None) # catches reusing values! 1+1...
    print("Passed!")

def testContainsPythagoreanTriple():
    print("Testing containsPythagoreanTriple()...", end="")
    assert(containsPythagoreanTriple([1,3,6,2,5,1,4]) == True)
    assert(containsPythagoreanTriple([1,3,6,2,8,1,4]) == False)
    assert(containsPythagoreanTriple([1,730,3,6,54,2,8,1,728,4])
                                      == True) # 54, 728, 730
    assert(containsPythagoreanTriple([1,730,3,6,54,2,8,1,729,4]) == False)
    assert(containsPythagoreanTriple([1,731,3,6,54,2,8,1,728,4]) == False)
    assert(containsPythagoreanTriple([1,731,3,6,54,2,8,1,728,4,
                                6253, 7800, 9997]) == True) # 6253, 7800, 9997
    assert(containsPythagoreanTriple([1,731,3,6,54,2,8,1,728,4,
                                      6253, 7800, 9998]) == False)
    assert(containsPythagoreanTriple([1,731,3,6,54,2,8,1,728,4,
                                      6253, 7800, 9996]) == False)
    assert(containsPythagoreanTriple([1, 2, 3, 67, 65, 35,83, 72, 
                                      97, 25, 98, 12]) == True) # 65, 72, 97
    assert(containsPythagoreanTriple([1, 1, 1]) == False)
    assert(containsPythagoreanTriple([1, 1, 2]) == False)
    assert(containsPythagoreanTriple([3, 5, 5]) == False)
    print("Passed!")

def testMovieAwards():
    print('Testing movieAwards()...', end='')
    tests = [
      (({ ("Best Picture", "The Shape of Water"), 
          ("Best Actor", "Darkest Hour"),
          ("Best Actress", "Three Billboards Outside Ebbing, Missouri"),
          ("Best Director", "The Shape of Water") },),
        { "Darkest Hour" : 1,
          "Three Billboards Outside Ebbing, Missouri" : 1,
          "The Shape of Water" : 2 }),
      (({ ("Best Picture", "Moonlight"),
          ("Best Director", "La La Land"),
          ("Best Actor", "Manchester by the Sea"),
          ("Best Actress", "La La Land") },),
        { "Moonlight" : 1,
          "La La Land" : 2,
          "Manchester by the Sea" : 1 }),
      (({ ("Best Picture", "12 Years a Slave"),
          ("Best Director", "Gravity"),
          ("Best Actor", "Dallas Buyers Club"),
          ("Best Actress", "Blue Jasmine") },),
        { "12 Years a Slave" : 1,
          "Gravity" : 1,
          "Dallas Buyers Club" : 1,
          "Blue Jasmine" : 1 }),
      (({ ("Best Picture", "The King's Speech"),
          ("Best Director", "The King's Speech"),
          ("Best Actor", "The King's Speech") },),
        { "The King's Speech" : 3}),
      (({ ("Best Picture", "Spotlight"), ("Best Director", "The Revenant"),
          ("Best Actor", "The Revenant"), ("Best Actress", "Room"),
          ("Best Supporting Actor", "Bridge of Spies"),
          ("Best Supporting Actress", "The Danish Girl"),
          ("Best Original Screenplay", "Spotlight"),
          ("Best Adapted Screenplay", "The Big Short"),
          ("Best Production Design", "Mad Max: Fury Road"),
          ("Best Cinematography", "The Revenant") },),
        { "Spotlight" : 2,
          "The Revenant" : 3,
          "Room" : 1,
          "Bridge of Spies" : 1,
          "The Danish Girl" : 1,
          "The Big Short" : 1,
          "Mad Max: Fury Road" : 1 }),
       ((set(),), { }),
            ]
    for args,result in tests:
        if (movieAwards(*args) != result):
            print('movieAwards failed:')
            print(args)
            print(result)
            assert(False)
    print('Passed!')

def testFriendsOfFriends():
    print("Testing friendsOfFriends()...", end="")
    d = dict()
    d["fred"] = set(["wilma", "betty", "barney", "bam-bam"])
    d["wilma"] = set(["fred", "betty", "dino"])
    d["betty"] = d["barney"] = d["bam-bam"] = d["dino"] = set()
    fof = friendsOfFriends(d)
    assert(fof["fred"] == set(["dino"]))
    assert(fof["wilma"] == set(["barney", "bam-bam"]))
    result = { "fred":set(["dino"]),
               "wilma":set(["barney", "bam-bam"]),
               "betty":set(),
               "barney":set(),
               "dino":set(),
               "bam-bam":set()
             }
    assert(fof == result)
    d = dict()
    #                A    B    C    D     E     F
    d["A"]  = set([      "B",      "D",        "F" ])
    d["B"]  = set([ "A",      "C", "D",  "E",      ])
    d["C"]  = set([                                ])
    d["D"]  = set([      "B",            "E",  "F" ])
    d["E"]  = set([           "C", "D"             ])
    d["F"]  = set([                "D"             ])
    fof = friendsOfFriends(d)
    assert(fof["A"] == set(["C", "E"]))
    assert(fof["B"] == set(["F"]))
    assert(fof["C"] == set([]))
    assert(fof["D"] == set(["A", "C"]))
    assert(fof["E"] == set(["B", "F"]))
    assert(fof["F"] == set(["B", "E"]))
    result = { "A":set(["C", "E"]),
               "B":set(["F"]),
               "C":set([]),
               "D":set(["A", "C"]),
               "E":set(["B", "F"]),
               "F":set(["B", "E"])
              }
    assert(fof == result)
    print("Passed!")

def testBonusAnimation():
    bonusAnimation()

def testAll():
    # testNearestPreSquareNumber()
    # testGetRecord()
    testPersonClass()
    # testGetPairSum()
    # testContainsPythagoreanTriple()
    # testMovieAwards()
    # testFriendsOfFriends()
    testBonusAnimation()

#################################################
# main
#################################################

def main():
    cs112_s22_week8_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
