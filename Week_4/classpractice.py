def calculate_area( rad) :
    pi = 3.14
    return pi * rad * rad

def is_palindrome(word) :
    word = word.lower()
    rev = ""
    temp = ""
    for i in word :
        rev = i + temp
        temp = rev
    if rev == word :
        return True
    else :
        return False

def find_factors(num) :
    factors = []
    i = 1
    while i <= num :
        if num % i == 0:
            factors.append(i)
            i += 1
        else :
            i += 1
    return factors


rads = 7
word = "madam"
number = 30
print (f"Area of a circle with radius {rads}, is :  {calculate_area(rads)}")
print(f"The word, {word} is a palindrome : {is_palindrome(word)}")
print(f"The factors of the number, {number}, are : {find_factors(number)}")
