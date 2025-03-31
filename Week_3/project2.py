print ("                    Izfin Technology ATR Calc")
while True:
    age =    int(input("ENTER AGE OF THE STAFF :              "))
    yOfExp = int(input("ENTER YEARS OF EXPERIENCE OF STAFF :  "))
    atr = 0
    if  yOfExp > 25 and age >= 55 :
        atr = 5_600_000
    elif yOfExp > 20 and age >= 45:
        atr = 4_480_000
    elif yOfExp > 10 and age >= 35 :
        atr = 1_500_000
    elif yOfExp < 10 and age < 35 :
        atr = 550_000
    else :
        atr = "\\_(*_*)_/"
    print("ANNUAL TAX REVENUE FOR THE STAFF IS :   ", atr)
    print("\nWOULD YOU LIKE TO GO AGAIN?\n YES = 1\n NO = 0")
    opt = int(input("OPTION :   "))
    if opt == 0 :
        break;
