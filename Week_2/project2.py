print("                 ROOT CALCULATOR ")
print("\nTo calculate the root you will first have to select the type of equation ")
print("1. QUADRATIC\n2.CUBIC\n3. QUARTIC")
opt = int(input("Please input the number associated with\nthe type of equation you'd like to calculate for :   "))
if opt == 1:
    print("You have chosen QUADRATIC EQUATION")
    a= float(input("WHAT IS A, THE COEFFICIENT OF X^2 :    "))
    b = float(input("WHAT IS B, THE COEFFICIENT OF X :   "))
    c = float(input("WHAT IS C, THE CONSTANT :    "))
    d = (b**2) - (4*a*c)
    if d > 0 :
        x1 = (-b + (d**0.5) )  / (2*a)
        x2 = (-b - (d**0.5) )  / (2*a)
        print(f"THE EQUATION : {a}x^2 + {b}x + {c} has two real and distinct roots")
        print(f"The roots are  x= {x1} or {x2}")
    elif d == 0 :
        x =  -b / (2*a)
        print(f"THE EQUATION : {a}x^2 + {b}x + {c} has two real and equal roots")
        print(f"The roots are  x= {x}")
    elif d < 0 :
        print("The equation has imaginary roots")
elif opt == 2 :
    print("You have chosen CUBIC EQUATION")
    a = float(input("WHAT IS A, THE COEFFICIENT OF X^3 :    "))
    b = float(input("WHAT IS B, THE COEFFICIENT OF X^2 :   "))
    c = float(input("WHAT IS C, THE COEFFICIENT OF X :   "))
    d = float(input("WHAT IS D, THE CONSTANT :    "))
    print(f"THE EQUATION : {a}x^3 + {b}x^2 + {c}x + {d} ")
elif opt == 3:
    print("You have chosen QUARTIC EQUATION")
