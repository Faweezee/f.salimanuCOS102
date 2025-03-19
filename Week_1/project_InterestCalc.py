def s_interest():
    print("CALCULATING SIMPLE INTEREST ...")
    p = int( input( "WHAT IS THE PRINCIPAL (IN NAIRA) :     "))
    t = int( input( "WHAT IS THE TIME (IN YEARS) :     "))
    r = int(input("WHAT IS THE RATE (IN PERCENTAGE) :     "))
    a = p * (1 + ((r/100)*t))
    print("\n\n     PARAMETERS")
    print("PRINCIPAL :  ",p,"\nTIME (years) :  ", t, "\nRATE (%) :  ", r)
    print("\n           THE AMOUNT FOR THE ABOVE PARAMETERS IS :  ",  round (a, 2), "   (2 d.p)")


def c_interest():
    print("CALCULATING COMPOUND INTEREST ...")
    p = int( input( "WHAT IS THE PRINCIPAL (IN NAIRA) :     "))
    t = int( input( "WHAT IS THE TIME (IN YEARS) :     "))
    r = int(input("WHAT IS THE RATE (IN PERCENTAGE) :     "))
    n = int(input("WHAT IS THE NUMBER OF PERIODS PER YEAR (IN NUMBERS) :     "))
    a = p * (1 + ((r/100)/n)) ** (n * t)
    print("\n\n     PARAMETERS")
    print("PRINCIPAL :  ",p,"\nTIME (years) :  ", t, "\nRATE (%) :  ", r,"\nNUMBER OF PERIODS :  ", n)
    print("\n           THE AMOUNT FOR THE ABOVE PARAMETERS IS :  ",  round (a, 2), "   (2 d.p)")


def a_plan():
    print("CALCULATING ANNUITY PLAN  ...")
    p = int( input( "WHAT IS THE PERIODIC PAYMENT (IN NAIRA) :     "))
    t = int(input("WHAT IS THE TIME (IN YEARS) :     "))
    r = int(input("WHAT IS THE RATE (IN PERCENTAGE) :     "))
    n = int(input("WHAT IS THE NUMBER OF PERIODS PER YEAR (IN NUMBERS) :     "))
    a = p * ( (((1 + ((r/100)/n)) ** (n * t)) - 1) / ((r/100)/n))
    print("\n\n     PARAMETERS")
    print("PERIODIC PAYMENT :  ",p,"\nTIME (years) :  ", t, "\nRATE (%) :  ", r,"\nNUMBER OF PERIODS :  ", n)
    print("\n           THE AMOUNT FOR THE ABOVE PARAMETERS IS :  ", round (a, 2), "   (2 d.p)")


print("                     INTEREST CALCULATOR")
print(" \nThis interest calculator can calculate : 1. SIMPLE INTEREST")
print("                                         2. COMPOUND INTEREST")
print("                                         3. ANNUITY PLAN")
print("\nWhich of the listed would you like to calculate?")
choice = int( input( "Please input the number beside the interest type you would like to calculate :     "))

match choice :
    case 1:
        s_interest()
    case 2:
        c_interest()
    case 3:
        a_plan()
    case _ :
        print(" INVALID INPUT!")

