import random

def test_para(arg):
    print(arg + "Response to Email")
    arg=="end"
    return arg

# True or False generator to test and make sure word will pass back and forth between main.py and responseToEmail.py

def trueOrFalse(word):

    random_number = random.randint(0,10)
    if (random_number % 2):
        word=True
    elif (random_number == 0):
        word = 'Zero'
    else:
        word=False
    return word
