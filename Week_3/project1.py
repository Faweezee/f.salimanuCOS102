students = {
    'stud1' : {'name' : 'Evelyn', 'age' : 17, 'height' : 5.5, 'score' : 80},
    'stud2' : {'name' : 'Jessica', 'age' : 16, 'height' : 6.0, 'score' : 85},
    'stud3' : {'name' : 'Somto', 'age' : 17, 'height' : 5.4, 'score' : 70},
    'stud4' : {'name' : 'Edith', 'age' : 18, 'height' : 5.9, 'score' : 60},
    'stud5' : {'name' : 'Liza', 'age' : 16, 'height' : 5.6, 'score' : 76},
    'stud6' : {'name' : 'Madonna', 'age' : 18, 'height' : 5.5, 'score' : 66},
    'stud7' : {'name' : 'Waje', 'age' : 17, 'height' : 6.1, 'score' : 87},
    'stud8' : {'name' : 'Tola', 'age' : 20, 'height' : 6.0, 'score' : 95},
    'stud9' : {'name' : 'Aisha', 'age' : 19, 'height' : 5.7, 'score' : 50},
    'stud10': {'name' : 'Latifa', 'age' : 17, 'height' : 5.5, 'score' : 49},
    'stud11': {'name' : 'Chinedu', 'age' : 19, 'height' : 5.7, 'score' : 74},
    'stud12': {'name' : 'Liam', 'age' : 16, 'height' : 5.9, 'score' : 87},
    'stud13': {'name' : 'Wale', 'age' : 18, 'height' : 5.8, 'score' : 75},
    'stud14': {'name' : 'Gbenga', 'age' : 17, 'height' : 6.1, 'score' : 68},
    'stud15': {'name' : 'Abiola', 'age' : 20, 'height' : 5.9, 'score' : 66},
    'stud16': {'name' : 'Kola', 'age' : 19, 'height' : 5.5, 'score' : 78},
    'stud17': {'name' : 'Kunle', 'age' : 16, 'height' : 6.1, 'score' : 87},
    'stud18': {'name' : 'George', 'age' : 18, 'height' : 5.4, 'score' : 98},
    'stud19': {'name' : 'Thomas', 'age' : 17, 'height' : 5.8, 'score' : 54},
    'stud20': {'name' : 'Wesley', 'age' : 19, 'height' : 5.7, 'score' : 60},
}
#10, 5, 8, 7
print ("|  NAME    | AGE | HEIGHT | SCORE |")
print ("+----------+-----+--------+-------+")

for stud in students.values() :
    print(f"| {stud['name']:^8} | {stud['age']:^3} | {stud['height']:^6} | {stud['score']:^5} |")
