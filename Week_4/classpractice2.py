def swap_first_last(list):
    temp = list[-1]
    list[-1] = list[0]
    list[0] = temp

def greet(name, greeting = "Hello") :
    return greeting + " " + name

lst = [1,2,3,4,5,6]
print(lst)
swap_first_last(lst)
print(f"lst after swap_first_last  {lst}")

greet_sam = greet("sam")
print(greet_sam)