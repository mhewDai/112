#################################################
# hw2.py
# name:Matthew Dai  
# andrew id:mdai2
#################################################

import cs112_s22_week2_linter
import math
import random

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Part A
#################################################

def digitCount(n):
    count = 0
    n = abs(n)
    if (n == 0):
        return 1
    while (n > 0):
        n //= 10
        count += 1
    return count

def gcd(a,b):
    a,b = abs(a),abs(b)
    if (b > a):
        a,b = b,a 
    if (a == b):
        return a
    while (a%b > 0):
        rem = a%b
        a = b
        b = rem
    return b

def hasConsecutiveDigits(n):
    n = abs(n)
    previousDigit = -1
    while (n>0):
        lastDigit = n%10
        n //= 10
        if (previousDigit == lastDigit):
            return True
        previousDigit = lastDigit
    return False

def isPrime(n):
    n = int(abs(n))
    if (n < 2):
        return False
    for factor in range(2, n):
        if (n % factor == 0):
            return False
    return True

def isAdditivePrime(n):
    if (isPrime(n) == False):
        return False
    sum = 0
    while (n > 0):
        lastdigit = n % 10
        sum += lastdigit
        n //= 10 
    if (isPrime(sum) == False):
        return False
    return True

def nthAdditivePrime(n):
#guess is n+1 number if values so far, while n is the first additive prime 
#found = n+1 it breaks
    guess = 0
    found = 0
    while(found <= n):
        guess += 1
        if isAdditivePrime(guess):
            found += 1
    return guess

def countOccurrence(digit, n):
    if (digit == 0 and n == 0):
        return 1
    count = 0
    while n > 0:
        currentDigit = n%10
        if currentDigit == digit:
            count += 1
        n //=10
    return count

def mostFrequentDigit(n):
    n = abs(n)
    bestDigit = -1
    bestCount = -1
    for digit in range(0,10):
        occurrence = countOccurrence(digit, n)
        if (occurrence > bestCount):
            bestCount = occurrence
            bestDigit = digit
    return bestDigit

def isRotation(x, y):
    x, y = abs(x),abs(y)
    count = 0
    digit = digitCount (x) 
    while (x != y):
            lastDigit = x % 10
            x //= 10
            x += lastDigit * 10**(digit-1)
            count += 1
            if (count == digit):
                return False
    return True

def integral(f, a, b, N):
    length = (b-a)/N
    result = 0
    for i in range(1,N+1):
        result += (f(a) + f(a+length))*0.5*length
        a+=length
    return result

#################################################
# Part B
#################################################

def findZeroWithBisection(f, x0, x1, epsilon):
    if (x0 < 0 and x1 < 0):
        return None
    while(x1 - x0 > epsilon):
        midpoint = (x0 + x1)/2
        if (f(midpoint) * f(x0) > 0):
            x0 = midpoint
        if (f(midpoint) * f(x1) > 0):
            x1 = midpoint
        if almostEqual(f(midpoint),0,epsilon):
            return midpoint
    return midpoint

def carrylessAdd(x1, x2):
    if (x2 > x1):
        x1,x2 = x2,x1
    sum = 0
    result = 0
    digits = digitCount(x1)
    for i in range(0,digits):
        sum = (x1%10+x2%10)%10
        result += sum*10**i
        x1 //= 10
        x2 //= 10
    return result

def digitSum(n):
    n = abs(n)
    sum = 0
    while(n>0):
        lastDigit = n%10
        sum += lastDigit
        n //= 10
    return sum

def nthPrime(n):
    guess = 0
    found = 0
    while(found <= n):
        guess += 1
        if isPrime(guess):
            found += 1
    return guess

def primeSum(n):
    n = abs(n)
    sum = 0
    i = 0
    while (n >1):     
        while(n % nthPrime(i) == 0):
            n //= nthPrime(i)
            sum += digitSum(nthPrime(i))
        i +=1
    return sum

def isSmith(n):
    if (n == 1):
        return False
    if isPrime(n):
        return False
    if (digitSum(n) == primeSum(n)):
        return True
    return False

def nthSmithNumber(n):
    guess = 0
    found = 0
    while(found <= n):
        guess += 1
        if (isSmith(guess) == True):
            found += 1
    return guess

def PlayPig():
    choice = input('Do you want to play Pig? Enter yes or no:',)
    vault1  = 0
    vault2  = 0
    while(choice != 'yes' and choice != 'no'):
        print('Please Enter yes or no!')
        choice = input()
        if (choice == 'yes' or choice == 'no'):
            break
    if choice == 'yes':
        print('The Game Starts Now!')
        print('Player 1 will start.') 
        score1 = 0
        score2 = 0
        while (vault1 < 100 or vault2 < 100):
            choice1 = input('Player 1 enter yes to roll dice and no to not:',)
            while(choice1 != 'yes' and choice1 != 'no'):
                print('Please Enter yes or no!')
                choice1 = input()
                if (choice1 == 'yes' or choice1 == 'no'):
                    break
            while(choice1 == 'yes'):
                n = random.randint(1,6)
                if choice1 == 'yes':
                    if (n == 1):
                        score1 = 0
                        print(n)
                        print('Sorry you got unlucky. Best luck next time!')
                        print('Current Score is now:', vault1)
                        print('Player 2 get ready')
                        break
                    score1 += n
                    print(score1)
                    if score1 >= 100:
                        vault1 += score1
                        break
                    choice1 = input('To Continue Enter yes and no to not:',)
                    while(choice1 != 'yes' and choice1 != 'no'):
                        print('Please Enter yes or no!')
                        choice1 = input()
                        if (choice1 == 'yes' or choice1 == 'no'):
                            break
                if (choice1 == 'no'):
                    vault1 += score1
                    if (vault1 >= 100):
                        break
                    print('Total Score: ', vault1)
                    break
            if (score1 >= 100 or vault1 >= 100):
                break
            choice2 = input('Player 2 enter yes to roll dice and no to not:',)
            while(choice2 != 'yes' and choice2 != 'no'):
                print('Please Enter yes or no!')
                choice2 = input()
                if (choice2 == 'yes' or choice2 == 'no'):
                    break
            while(choice2 == 'yes'):
                n = random.randint(1,6)
                if choice2 == 'yes':
                    if (n == 1):
                        score2 = 0
                        print(n)
                        print('Sorry you got unlucky. Best luck next time!')
                        print('Current Score is now:', vault1)
                        print('Player 1 get ready')
                        break
                    score2 += n
                    print(score2)
                    if score2 >= 100:
                        vault2 += score2
                        break
                    choice2 = input('To Continue Enter yes and no to not:',)
                    while(choice2 != 'yes' and choice2 != 'no'):
                        print('Please Enter yes or no!')
                        choice2 = input()
                        if (choice2 == 'yes' or choice2 == 'no'):
                            break
                if (choice2 == 'no'):
                    vault2 += score2
                    if (vault2 >= 100):
                        break
                    print('Total Score: ', vault2)
                    break
            if (score2 >= 100 or vault2 >= 100):
                break

    if (vault1 >= 100):
        print('Congrats Player 1, You have won!')
    if (vault2 >= 100):
        print('Congrats Player 2, You have won!')
    if choice == 'no':
        print('See you next time!')

#################################################
# Bonus/Optional
#################################################
def multiCarrylessAdd(n):
    x1 = 140
    lastDigit = n%10 
    result = 0
    while (lastDigit>0):
            result = carrylessAdd(result,x1)
            lastDigit -= 1
    return result
# print(carrylessAdd(320,140))
# print(multiCarrylessAdd(134))

def bonusPlay112(game):
    return 42

def bonusCarrylessMultiply(x1, x2):
    if (x2 > x1):
        x1,x2 = x2,x1
    sum = 0
    digits = 0
    digitsCounts = digitCount(x2)
    while (x2 > 0):
        lastDigit = x2%10
        result = 0
        x2 //= 10
        while (lastDigit>0):
            result = carrylessAdd(result,x1)
            lastDigit -= 1
        while (digits < digitsCounts):
            sum = carrylessAdd(sum,result * 10 **(digits-1)) 
            digits += 1
    return sum
############################
# spicy bonus: integerDataStructures
############################

def intCat(n, m): pass
def lengthEncode(value): pass
def lengthDecode(encoding): pass
def lengthDecodeLeftmostValue(encoding): pass
def newIntList(): pass
def intListLen(intList): pass
def intListGet(intList, i): pass
def intListSet(intList, i, value): pass
def intListAppend(intList, value): pass
def intListPop(intList): pass
def newIntSet(): pass
def intSetAdd(intSet, value): pass
def intSetContains(intSet, value): pass
def newIntMap(): pass
def intMapGet(intMap, key): pass
def intMapContains(intMap,key): pass
def intMapSet(intMap, key, value): pass
def newIntFSM(): pass
def isAcceptingState(fsm, state): pass
def addAcceptingState(fsm, state): pass
def setTransition(fsm, fromState, digit, toState): pass
def getTransition(fsm, fromState, digit): pass
def accepts(fsm, inputValue): pass
def states(fsm, inputValue): pass
def encodeString(s): pass
def decodeString(intList): pass

#################################################
# Test Functions
#################################################

def testDigitCount():
    print('Testing digitCount()...', end='')
    assert(digitCount(3) == 1)
    assert(digitCount(33) == 2)
    assert(digitCount(3030) == 4)
    assert(digitCount(-3030) == 4)
    assert(digitCount(0) == 1)
    print('Passed!')

def testGcd():
    print('Testing gcd()...', end='')
    assert(gcd(3, 3) == 3)
    assert(gcd(3**6, 3**6) == 3**6)
    assert(gcd(3**6, 2**6) == 1)
    assert (gcd(2*3*4*5,3*5) == 15)
    x = 1568160 # 2**5 * 3**4 * 5**1 *        11**2
    y = 3143448 # 2**3 * 3**6 *        7**2 * 11**1
    g =    7128 # 2**3 * 3**4 *               11**1
    assert(gcd(x, y) == g)
    print('Passed!')

def testHasConsecutiveDigits():
    print('Testing hasConsecutiveDigits()...', end='')
    assert(hasConsecutiveDigits(0) == False)
    assert(hasConsecutiveDigits(123456789) == False)
    assert(hasConsecutiveDigits(1212) == False)
    assert(hasConsecutiveDigits(1212111212) == True)
    assert(hasConsecutiveDigits(33) == True)
    assert(hasConsecutiveDigits(-1212111212) == True)
    print('Passed!')

def testNthAdditivePrime():
    print('Testing nthAdditivePrime()... ', end='')
    assert(nthAdditivePrime(0) == 2)
    assert(nthAdditivePrime(1) == 3)
    assert(nthAdditivePrime(5) == 23)
    assert(nthAdditivePrime(10) == 61)
    assert(nthAdditivePrime(15) == 113)
    print('Passed!')

def testMostFrequentDigit():
    print('Testing mostFrequentDigit()...', end='')
    assert mostFrequentDigit(0) == 0
    assert mostFrequentDigit(1223) == 2
    assert mostFrequentDigit(12233) == 2
    assert mostFrequentDigit(-12233) == 2
    assert mostFrequentDigit(1223322332) == 2
    assert mostFrequentDigit(123456789) == 1
    assert mostFrequentDigit(1234567789) == 7
    assert mostFrequentDigit(1000123456789) == 0
    print('Passed!')

def testIsRotation():
    print('Testing isRotation()... ', end='')
    assert(isRotation(1, 1) == True)
    assert(isRotation(1234, 4123) == True)
    assert(isRotation(1234, 3412) == True)
    assert(isRotation(1234, 2341) == True)
    assert(isRotation(1234, 1234) == True)
    assert(isRotation(1234, 123) == False)
    assert(isRotation(1234, 12345) == False)
    assert(isRotation(1234, 1235) == False)
    assert(isRotation(1234, 1243) == False)
    print('Passed!')

def f1(x): return 42
def i1(x): return 42*x 
def f2(x): return 2*x  + 1
def i2(x): return x**2 + x
def f3(x): return 9*x**2
def i3(x): return 3*x**3
def f4(x): return math.cos(x)
def i4(x): return math.sin(x)
def testIntegral():
    print('Testing integral()...', end='')
    epsilon = 10**-4
    assert(almostEqual(integral(f1, -5, +5, 1), (i1(+5)-i1(-5)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f1, -5, +5, 10), (i1(+5)-i1(-5)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f2, 1, 2, 1), 4,
                      epsilon=epsilon))
    assert(almostEqual(integral(f2, 1, 2, 250), (i2(2)-i2(1)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f3, 4, 5, 250), (i3(5)-i3(4)),
                      epsilon=epsilon))
    assert(almostEqual(integral(f4, 1, 2, 250), (i4(2)-i4(1)),
                      epsilon=epsilon))
    print("Passed!")

def testFindZeroWithBisection():
    print('Testing findZeroWithBisection()... ', end='')
    def f1(x): return x*x - 2 # root at x=sqrt(2)
    x = findZeroWithBisection(f1, 0, 2, 0.000000001)
    assert(almostEqual(x, 1.41421356192))   
    def f2(x): return x**2 - (x + 1)  # root at x=phi
    x = findZeroWithBisection(f2, 0, 2, 0.000000001)
    assert(almostEqual(x, 1.61803398887))
    def f3(x): return x**5 - 2**x # f(1)<0, f(2)>0
    x = findZeroWithBisection(f3, 1, 2, 0.000000001)
    assert(almostEqual(x, 1.17727855081))
    print('Passed!')

def testCarrylessAdd():
    print('Testing carrylessAdd()... ', end='')
    assert(carrylessAdd(785, 376) == 51)
    assert(carrylessAdd(0, 376) == 376)
    assert(carrylessAdd(785, 0) == 785)
    assert(carrylessAdd(30, 376) == 306)
    assert(carrylessAdd(785, 30) == 715)
    assert(carrylessAdd(12345678900, 38984034003) == 40229602903)
    print('Passed!')

def testNthSmithNumber():
    print('Testing nthSmithNumber()... ', end='')
    assert(nthSmithNumber(0) == 4)
    assert(nthSmithNumber(1) == 22)
    assert(nthSmithNumber(2) == 27)
    assert(nthSmithNumber(3) == 58)
    assert(nthSmithNumber(4) == 85)
    assert(nthSmithNumber(5) == 94)
    print('Passed!')

def testPlayPig():
    print('** Note: You need to manually test playPig()')
    PlayPig()

def testBonusPlay112():
    print("Testing bonusPlay112()... ", end="")
    assert(bonusPlay112( 5 ) == "88888: Unfinished!")
    assert(bonusPlay112( 521 ) == "81888: Unfinished!")
    assert(bonusPlay112( 52112 ) == "21888: Unfinished!")
    assert(bonusPlay112( 5211231 ) == "21188: Unfinished!")
    assert(bonusPlay112( 521123142 ) == "21128: Player 2 wins!")
    assert(bonusPlay112( 521123151 ) == "21181: Unfinished!")
    assert(bonusPlay112( 52112315142 ) == "21121: Player 1 wins!")
    assert(bonusPlay112( 523 ) == "88888: Player 1: move must be 1 or 2!")
    assert(bonusPlay112( 51223 ) == "28888: Player 2: move must be 1 or 2!")
    assert(bonusPlay112( 51211 ) == "28888: Player 2: occupied!")
    assert(bonusPlay112( 5122221 ) == "22888: Player 1: occupied!")
    assert(bonusPlay112( 51261 ) == "28888: Player 2: offboard!")
    assert(bonusPlay112( 51122324152 ) == "12212: Tie!")
    print("Passed!")

def testBonusCarrylessMultiply():
    print("Testing bonusCarrylessMultiply()...", end="")
    assert(bonusCarrylessMultiply(643, 59) == 417)
    assert(bonusCarrylessMultiply(6412, 387) == 807234)
    print("Passed!")

# Integer Data Structures

def testLengthEncode():
    print('Testing lengthEncode()...', end='')
    assert(lengthEncode(789) == 113789)
    assert(lengthEncode(-789) == 213789)
    assert(lengthEncode(1234512345) == 12101234512345)
    assert(lengthEncode(-1234512345) == 22101234512345)
    assert(lengthEncode(0) == 1110)
    print('Passed!')

def testLengthDecodeLeftmostValue():
    print('Testing lengthDecodeLeftmostValue()...', end='')
    assert(lengthDecodeLeftmostValue(111211131114) == (2, 11131114))
    assert(lengthDecodeLeftmostValue(112341115) == (34, 1115))
    assert(lengthDecodeLeftmostValue(111211101110) == (2, 11101110))
    assert(lengthDecodeLeftmostValue(11101110) == (0, 1110))
    print('Passed!')

def testLengthDecode():
    print('Testing lengthDecode()...', end='')
    assert(lengthDecode(113789) == 789)
    assert(lengthDecode(213789) == -789)
    assert(lengthDecode(12101234512345) == 1234512345)
    assert(lengthDecode(22101234512345) == -1234512345)
    assert(lengthDecode(1110) == 0)
    print('Passed!')

def testIntList():
    print('Testing intList functions...', end='')
    a1 = newIntList()
    assert(a1 == 1110) # length = 0, list = []
    assert(intListLen(a1) == 0)
    assert(intListGet(a1, 0) == 'index out of range')

    a1 = intListAppend(a1, 42)
    assert(a1 == 111111242) # length = 1, list = [42]
    assert(intListLen(a1) == 1)
    assert(intListGet(a1, 0) == 42)
    assert(intListGet(a1, 1) == 'index out of range')
    assert(intListSet(a1, 1, 99) == 'index out of range')

    a1 = intListSet(a1, 0, 567)
    assert(a1 == 1111113567) # length = 1, list = [567]
    assert(intListLen(a1) == 1)
    assert(intListGet(a1, 0) == 567)

    a1 = intListAppend(a1, 8888)
    a1 = intListSet(a1, 0, 9)
    assert(a1 == 111211191148888) # length = 2, list = [9, 8888]
    assert(intListLen(a1) == 2)
    assert(intListGet(a1, 0) == 9)
    assert(intListGet(a1, 1) == 8888)

    a1, poppedValue = intListPop(a1)
    assert(poppedValue == 8888)
    assert(a1 == 11111119) # length = 1, list = [9]
    assert(intListLen(a1) == 1)
    assert(intListGet(a1, 0) == 9)
    assert(intListGet(a1, 1) == 'index out of range')

    a2 = newIntList()
    a2 = intListAppend(a2, 0)
    assert(a2 == 11111110)
    a2 = intListAppend(a2, 0)
    assert(a2 == 111211101110)
    print('Passed!')

def testIntSet():
    print('Testing intSet functions...', end='')
    s = newIntSet()
    assert(s == 1110) # length = 0
    assert(intSetContains(s, 42) == False)
    s = intSetAdd(s, 42)
    assert(s == 111111242) # length = 1, set = [42]
    assert(intSetContains(s, 42) == True)
    s = intSetAdd(s, 42) # multiple adds --> still just one
    assert(s == 111111242) # length = 1, set = [42]
    assert(intSetContains(s, 42) == True)
    print('Passed!')

def testIntMap():
    print('Testing intMap functions...', end='')
    m = newIntMap()
    assert(m == 1110) # length = 0
    assert(intMapContains(m, 42) == False)
    assert(intMapGet(m, 42) == 'no such key')
    m = intMapSet(m, 42, 73)
    assert(m == 11121124211273) # length = 2, map = [42, 73]
    assert(intMapContains(m, 42) == True)
    assert(intMapGet(m, 42) == 73)
    m = intMapSet(m, 42, 98765)
    assert(m == 11121124211598765) # length = 2, map = [42, 98765]
    assert(intMapGet(m, 42) == 98765)
    m = intMapSet(m, 99, 0)
    assert(m == 11141124211598765112991110) # length = 4, 
                                            # map = [42, 98765, 99, 0]
    assert(intMapGet(m, 42) == 98765)
    assert(intMapGet(m, 99) == 0)
    print('Passed!')

def testIntFSM():
    print('Testing intFSM functions...', end='')
    fsm = newIntFSM()
    assert(fsm == 111211411101141110) # length = 2, 
                                      # [empty stateMap, empty startStateSet]
    assert(isAcceptingState(fsm, 1) == False)

    fsm = addAcceptingState(fsm, 1)
    assert(fsm == 1112114111011811111111)
    assert(isAcceptingState(fsm, 1) == True)

    assert(getTransition(fsm, 0, 8) == 'no such transition')
    fsm = setTransition(fsm, 4, 5, 6)
    # map[5] = 6: 111211151116
    # map[4] = (map[5] = 6):  111211141212111211151116
    assert(fsm == 1112122411121114121211121115111611811111111)
    assert(getTransition(fsm, 4, 5) == 6)

    fsm = setTransition(fsm, 4, 7, 8)
    fsm = setTransition(fsm, 5, 7, 9)
    assert(getTransition(fsm, 4, 5) == 6)
    assert(getTransition(fsm, 4, 7) == 8)
    assert(getTransition(fsm, 5, 7) == 9)

    fsm = newIntFSM()
    assert(fsm == 111211411101141110) # length = 2, 
                                      # [empty stateMap, empty startStateSet]
    fsm = setTransition(fsm, 0, 5, 6)
    # map[5] = 6: 111211151116
    # map[0] = (map[5] = 6):  111211101212111211151116
    assert(fsm == 111212241112111012121112111511161141110)
    assert(getTransition(fsm, 0, 5) == 6)

    print('Passed!')

def testAccepts():
    print('Testing accepts()...', end='')
    fsm = newIntFSM()
    # fsm accepts 6*7+8
    fsm = addAcceptingState(fsm, 3)
    fsm = setTransition(fsm, 1, 6, 1) # At state 1, receive 6, move to state 1
    fsm = setTransition(fsm, 1, 7, 2) # At state 1, receive 7, move to state 2
    fsm = setTransition(fsm, 2, 7, 2) # At state 1, receive 7, move to state 2
    fsm = setTransition(fsm, 2, 8, 3) # At state 1, receive 8, move to state 3
    assert(accepts(fsm, 78) == True)
    assert(states(fsm, 78) == 1113111111121113) # length = 3, list = [1,2,3]
    assert(accepts(fsm, 678) == True)
    assert(states(fsm, 678) == 11141111111111121113) # length = 4, 
                                                     # list = [1,1,2,3]

    assert(accepts(fsm, 5) == False)
    assert(accepts(fsm, 788) == False)
    assert(accepts(fsm, 67) == False)
    assert(accepts(fsm, 666678) == True)
    assert(accepts(fsm, 66667777777777778) == True)
    assert(accepts(fsm, 7777777777778) == True)
    assert(accepts(fsm, 666677777777777788) == False)
    assert(accepts(fsm, 77777777777788) == False)
    assert(accepts(fsm, 7777777777778) == True)
    assert(accepts(fsm, 67777777777778) == True)
    print('Passed!')

def testEncodeDecodeStrings():
    print('Testing encodeString and decodeString...', end='')
    assert(encodeString('A') == 111111265) # length = 1, str = [65]
    assert(encodeString('f') == 1111113102) # length = 1, str = [102]
    assert(encodeString('3') == 111111251) # length = 1, str = [51]
    assert(encodeString('!') == 111111233) # length = 1, str = [33]
    assert(encodeString('Af3!') == 1114112651131021125111233) # length = 4, 
                                                          # str = [65,102,51,33]
    assert(decodeString(111111265) == 'A')
    assert(decodeString(1114112651131021125111233) == 'Af3!')
    assert(decodeString(encodeString('WOW!!!')) == 'WOW!!!')
    print('Passed!')

def testIntegerDataStructures():
    testLengthEncode()
    testLengthDecode()
    testLengthDecodeLeftmostValue()
    testIntList()
    testIntSet()
    testIntMap()
    testIntFSM()
    testAccepts()
    testEncodeDecodeStrings()

#################################################
# testAll and main
#################################################

def testAll():
    # comment out the tests you do not wish to run!
    # Part A:
    # testDigitCount()
    # testGcd()   
    # testHasConsecutiveDigits()   
    # testNthAdditivePrime()   
    # testMostFrequentDigit()
    testIsRotation()
    # testIntegral()

    # Part B:
    # testFindZeroWithBisection()
    # testCarrylessAdd()
    # testNthSmithNumber()
    # testPlayPig()

    # Bonus:
    # testBonusPlay112()
    # testBonusCarrylessMultiply()
    # testIntegerDataStructures()

def main():
    cs112_s22_week2_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
