def printinfo(arg1, *vartuple):
    #This is test
    print ("Output is: ")
    print (arg1)
    for var in vartuple:
        print (var)
        return;
printinfo( 10 );
printinfo( 70, 60, 50 );