import random
def guesser():
    rand = random.randint(1, 10)
    for i in range(80000):
        guess = input("guess your number: ")
        if int(guess) > rand:
            print("lower")
        elif int(guess) == rand:
            print("==============================================")
            print("youre the winner! the correct number is: " + str(rand))
            print("===============================================")
            print("it took you " + str(i+1) + " tries")

            break
        elif guess == "help":
            print(rand)
        else:
            print("higher")

guesser()
