import random
def guesser():
    maxNum = 1
    lvl = 0
    while lvl != 8:
        rand = random.randint(1, maxNum*10)
        print("")
        print(rand)
        print("this is level: "+str(lvl+1))
        print("you are guessing between the numbers 1 and " + str(maxNum*10))
        for i in range(80000):
            guess = input("guess your number: ")
            if int(guess) > rand:
                print("lower")
            elif int(guess) == rand:
                print("==============================================")
                print("You're the winner! the correct number is: " + str(rand))
                print("===============================================")
                print("it took you " + str(i+1) + " tries")
                lvl += 1
                if lvl > 5:
                    maxNum *= 1000
                else:
                    maxNum *= 10

                break
            elif guess == "help":
                print(rand)
            else:
                print("higher")

    sandBox()

def sandBox():
    print("YOU HAVE UNLOCKED SANDBOX MODE!")
    print("you need to pick 2 numbers that you want to guess between")
    start = input(" Enter the starting number: ")
    maxNum = input(" Enter the Final number: ")
    rand = random.randint(int(start), int(maxNum))
    print("")
    print(rand)
    print("you are guessing between the numbers " + str(start) + " and " + str(maxNum))
    for i in range(80000):
        guess = input("guess your number: ")
        if int(guess) > rand:
            print("lower")
        elif int(guess) == rand:
            print("==============================================")
            print("You're the winner! the correct number is: " + str(rand))
            print("===============================================")
            print("it took you " + str(i + 1) + " tries")

            break
        elif guess == "help":
            print(rand)
        else:
            print("higher")



guesser()
