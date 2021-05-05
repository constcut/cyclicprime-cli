'''This module used for generating sequenses of cyclic prime numbers in a proper way to store them on OEIS
Also it could be used to generate cyclic prime numbers from any prime number or cyclic number using console

Usage:python cyclicprime.py (-prime prime_number | -number number) numeric_system max_digits
'''

import sys, os
import math
import gmpy2
from factordb.factordb import FactorDB
import logging


'''
This function generates all the sub-numbers inside number.
Used to generate sequences for OEIS.

Inputs: number - origin, N - numeric system, digitsMin, digitsMax - range.
Outputs: list of sub numbers.
'''

def listSubNumbers(number, N, digitsMin, digitsMax):
    digitsString = number #moved from gmpy2.mpz because of numbers like '01'
    period = len(digitsString)
    requiredDigits = period + digitsMax - 1

    if requiredDigits % period == 0:
        multiplyCycles = gmpy2.f_div(requiredDigits, period)
    else:
        multiplyCycles = gmpy2.f_div(requiredDigits, period) + 1
    
     
    digitsString *= multiplyCycles

    subNumbers = []

    for i in range(digitsMin, digitsMax + 1):
        for j in range(period):
            subString = digitsString[j: j + i]
            subNum = gmpy2.mpz(subString, N)
            subNumbers.append(subNum)

    return subNumbers


'''
This function returns list of indecies from a list of numbers. 
Used to generate sequences for OEIS.

Inputs: listOfNumbers, startsFromZero - if sets to True indexation starts from 0
Outputs: list of indecies of prime numbers from the listOfNumbers
'''

def primeIndecies(listOfNumbers, startsFromZero = False):
    idxList = []
    for i in range(len(listOfNumbers)):
        if gmpy2.is_prime(listOfNumbers[i]):
            if startsFromZero:
                idxList.append(i)
            else:
                idxList.append(i + 1)
    return idxList


'''
This function returns list of prime numbers in a given list of numbers.


Inputs: listOfNumbers.
Outputs: listOfPrimeNumbers.
'''


def primeNumbersInList(listOfNumbers):
    listOfPrimeNumbers = []
    for i in range(len(listOfNumbers)):
  
        digits = listOfNumbers[i].digits(10) #decimal used here only to check then length of prime number to avoid local check for long numbers

        if len(digits) < 200:
            if gmpy2.is_prime(listOfNumbers[i]):
                listOfPrimeNumbers.append(listOfNumbers[i])
                logging.info(digits)
        else:
            f = FactorDB(listOfNumbers[i])
            connection = f.connect()
            factorList = f.get_factor_list()
            if len(factorList) == 1:
                listOfPrimeNumbers.append(listOfNumbers[i])
                logging.info(digits)
            
    return listOfPrimeNumbers


'''
This function helps to recreate cyclic prime numbers, from amount of digits and first digit.

Inputs: numbers, N - numeric system, first - first digit, size - amount of digits.
Outputs: repairedNumber.
'''

def repairByFirstAndSize(number, N, first, size):

    numStr = number.digits(N) 
    period = len(numStr)
    
    if size % period == 0:
        multiplyCycles = gmpy2.f_div(size, period) + 1
    else:
        multiplyCycles = gmpy2.f_div(size, period) + 2

    numStr *= multiplyCycles

    firstIdx = numStr.find(str(first))
    repairedNumber = numStr[firstIdx:firstIdx + size]
    return repairedNumber

    
'''
This function helps to recreate cyclic prime numbers, from index in sub-numbers list of a number.

Inputs: numbers, N - numeric system, idx - index in sub-numbers list.
Outputs: repairedNumber.
'''

def repairByIdxSpecial(number, N, idx):
    
    numberString = number.digits(N)
    period = len(numberString)

    singleDigList = listSubNumbers(number, N, 1, 1)
    singleDigList.sort()

    if idx % period == 0:
        totalDigits = gmpy2.f_div(idx, period)
    else:
        totalDigits = gmpy2.f_div(idx, period) + 1

    offset = idx % period 
    if offset == 0: 
        offset += period 

    firstDigit = singleDigList[offset - 1]
    #TODO move repairByFirstAndSize #TODO 17 !
    repairedNumber = repairByFirstAndSize(number, N, firstDigit, totalDigits)
    #print('Repaired: ', totalDigits, offset, 'first', firstDigit)
    #print('Repaired Prime: ', rep)
    return repairedNumber


'''
This function gets the index in list of sub-numbers, without using list of sub-numbers but only the original number.
One of functions used only for OEIS.

Inputs: numbers, N - numeric system, prime - cyclic prime number to get index.
Outputs: index.
'''

def getIdx(number, N, prime):

    prime = gmpy2.mpz(prime)
    numberString = number.digits(N)
    period = len(numberString) 

    singleDigList = listSubNumbers(number, N, 1, 1)
    singleDigList.sort()

    primeString = prime.digits(N)
    totalDigits = len(primeString) 

    firstIdx = singleDigList.index(int(primeString[0]))
    index = (totalDigits - 1) * period + firstIdx + 1 
    return index

'''
This function creates a cyclic number from certain prime in certain numeric system.
It also returns reptend level, for example if the prime was 2nd reprend level in the numeric system.

Inputs: P - prime number, N - numeric system.
Outputs: cyclicNumber, reptendLevel.
'''

def makeCyclicNumber(P, N, numerator=1):
    for period in range(1, P): 
        if (gmpy2.mpz(N) ** period) % P  == 1: 
            break
        
    cyclicNumber = gmpy2.f_div(numerator * (gmpy2.mpz(N) ** period), P)
    reptendLevel = (P - 1) / period
    cyclicNumber = cyclicNumber.digits(N)

    while len(cyclicNumber) < period:
        cyclicNumber = '0' + cyclicNumber

    return cyclicNumber, reptendLevel, period



'''
This function used to explore certain prime number P, in numeric system N, looking for maxDigits.

Input: P - prime, N - numeric system, maxDigits.
'''

def exploreByPrime(P, N, maxDigits):

    cyclicNum, repLevel, period = makeCyclicNumber(P, N, numerator=2)

    print('For the prime number', P, 'in numeric system', N, 'we got cyclic number', cyclicNum, ' that is ', repLevel, 'reptend level')
    print('Period', period)


    listOfSubNumbers = listSubNumbers(cyclicNum, N, 1, maxDigits) 
    listOfSubNumbers.sort()

    primes = primeNumbersInList(listOfSubNumbers)

    for p in primes: 
        originalDigits = p.digits(N)
        print(originalDigits, " in decimal is ", int(p))



'''
This function used to explore certain number (for example cyclic number), in numeric system N, looking for maxDigits.
It only explores specific number, so for example 142857 and 285714 are different numbers.

Input: number - prime, N - numeric system, maxDigits.
'''

def explorByNumber(number, N, maxDigits):
    listOfSubNumbers = listSubNumbers(number, N, 1, maxDigits) 
    listOfSubNumbers.sort()

    primes = primeNumbersInList(listOfSubNumbers)

    for p in primes: 
        originalDigits = p.digits(N)
        print()
        print(originalDigits, " in decimal is ", int(p))



if __name__ == '__main__':

    if len(sys.argv) > 1:

        logging.basicConfig(level=logging.INFO, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")

        logging.info("Application started")

        if sys.argv[1] == '-prime':

            P = int(sys.argv[2])
            N = int(sys.argv[3])
            maxDigits = int(sys.argv[4])

            exploreByPrime(P, N, maxDigits)

        if sys.argv[1] == '-number':

            number = sys.argv[2]
            N = int(sys.argv[3])
            maxDigits = int(sys.argv[4])

            explorByNumber(number, N, maxDigits)
    else:
        print('Usage:python cyclicprime.py (-prime prime_number | -number number) numeric_system max_digits')

