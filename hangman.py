#Created by Ryan S

#import modules
import os, random, sys, urllib2, time
#change the current system directory
if not 'idlelib.run' in sys.modules:
    full_path = os.path.realpath(__file__)
    os.chdir(os.path.dirname(full_path))

#function to see if connected to internet
def check_link(urlfile):
    try:
        urllib2.urlopen(urlfile,timeout=2)
        return True
    except urllib2.URLError as err: pass
    return False

#Clear the terminal
def cls():
    if not 'idlelib.run' in sys.modules:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

#function to see if string is just spaces
def linespace(i):
    linespace = True
    for s in range(0,len(i) - 1):
        if i[s] != " ":
            return False
    return True
#function to test user with a yes or no question
def testUser(string, Exit):
    result = raw_input(string).lower()
    while True:
        if result.startswith('y') or result == "sure" or result == "go ahead" or result == "ok":
            return True
            break
        elif result.startswith('n'):
            if Exit:
                #if not user:
                    #os.remove('text.data')
                #else:
                if os.path.exists('.hmdatad.txt'):
                    os.remove('.hmdatad.txt')
                if os.path.exists('.hmdatau.txt'):
                    os.remove('.hmdatau.txt')
                sys.exit()
            
            return False
            break
        else:
            result = raw_input("Type in 'y' or 'n'")

#Randomly choose a word based on the category the user selects
def getWords():
    cls()
    global listofwords
    global categories
    global filename
    listofwords = []
    categories = []
    if testUser("Do you want to use a default word list? Recommended!(downloaded from internet)\ny/n", False):
        filename = 'default word list'
        #Once the file is downloaded we don't need to download it again
        try:
            with open('.hmdatad.txt') as f:
                textfile = open('.hmdatad.txt', 'r')
                pass
        except IOError as e:
            print 'Downloading...'
            urlfile = "https://dl.dropbox.com/s/4sf350ftxj1k98y/wordlist.txt"
            #Check to see if internet is on
            while not check_link(urlfile):
                testUser("Can't download the default word file. Check your internet conection. \ny - try again \nn - exit \n", True)
            #download a wordlist from a source
            tempfile = urllib2.urlopen(urlfile, "r")
           #open up a temperary file
            textfile = open('.hmdatad.txt', 'w')
            #put the conents from the source to the temperary file
            textfile.write(tempfile.read())
            textfile = open('.hmdatad.txt', 'r')
            tempfile.close()
            
    else:
        filename = ''
        while not os.path.exists(filename):
            filename = raw_input("Enter the exact name of the wordlist in this directory. e.g. wordlist.txt: ")

        userfile = open(filename, 'r')
        textfile = open('.hmdatau.txt', 'w')
        textfile.write(userfile.read())
        textfile = open('.hmdatau.txt', 'r')
    
    
    for i in textfile.readlines():
        i = i.translate(None, """!@$%^&*()_+={}[]|\/;"'<>?""")
        #Check to see if line is valid
        if i[0] != "#" and i[0] != "\n" and i[0] != "\r" and not linespace(i):
            b = 0
            a = ""
            while b < len(i) - 1:
                if i[b] == ":":
                    break
                    b = 0
                b += 1
            tempcat = i[0:b]
            #Check if the category is not same length as the line, else display warning and quit
            if b >= len(i) - 1:
                cls()
                quitstring = "Invalid word file...  Use default wordlist next time! Quitting"
                for q in range(0,3):
                    print (quitstring + ("." * q))
                    time.sleep(1)
                    cls()
                sys.exit()
            categories.append(i[0:b])
            i = i.lower()
            i = i[len(tempcat) + 1:len(tempcat)+ len(i)]
            #Split up the words into a list
            categorywords = (i.strip().split(","))
            #remove duplicate words and spaces
            singleWordList = []
            for x in range(0,len(categorywords)):
                singleWord = categorywords[x]
                #check to see if the word is not empty
                if singleWord != "":
                    #remove spaces at the beginning of the word
                    singleWord = singleWord.lstrip()
                    #remove spaces at the end of word
                    while singleWord[len(singleWord) - 1] == " ":
                        singleWord = singleWord[0:len(singleWord) - 1]
                    singleWordList.append(singleWord)
                if singleWordList.count(singleWord) >=2:
                    singleWordList.remove(singleWord)
                       
            categorywords = singleWordList
            #Add the category words to the list of words
            listofwords += [categorywords]
            
        #close the file
        textfile.close()
    return listofwords

#get category that the user wants to use    
def getCategory(listofwords, categories):
    print ("These are the categories:")

    print

    print (" \n".join(categories))

    print
    global category
    global wordList
    wordList = []
    category = raw_input("Type one of these categories: ").lower()

    #lower the case of the categories
    for x in range(0,len(categories)):
        categories[x] = categories[x].lower()
        
    while category not in categories:
        print("That is not a category.  Please type in one of the categories above EXACTLY as shown.").lower()
        category = raw_input("Type one of these categories: ").lower()
    
    for a in range(0,len(listofwords)):
        if category == categories[a]:
            wordList = listofwords[a][0:len(listofwords[a])]
    word = ""
    return wordisDone(wordList)

#Randomize the word and check to see if it was not justed used
def wordisDone(wordList):
    word = wordList[random.randint(0, len(wordList) - 1)]
    while word in usedWords:
        word = wordList[random.randint(0, len(wordList) - 1)]
    return word

#Make the blanks
def getBlanks():
    wordblanks = []
    for i in range(0,len(word)):
        if word[i] == " ":
            wordblanks.append("  ")
        elif word[i] == "-":
            wordblanks.append(" -  ")
        else:
            wordblanks.append("_ ")
    return wordblanks


#Display elements of the game
def displayGame(won):
    cls()
    print("Category: " + category.title())
    if won:
        print(hangmanpics[7])
    else:
        print(hangmanpics[guesses])
        print("Missed letters: " + "  ".join(missedLetters))
    
    print(guessArea())


#Check if user input is indeed a single letter
def userLetterInput(guess):
    global guesses
    while True:
        guess = raw_input("Guess a letter:")
        guess = guess.lower()
        if(guess in missedLetters or guess in correctLetters):
            print("You already guessed that letter")
        elif(len(guess) > 1 or guess not in "abcdefghijklmnopqrstuvwxyz"):
            global notletterguess
            notletterguess += 1
            if(notletterguess == 1):
                print("Please enter a single LETTER")
            if(notletterguess == 2):
                print("O.K. Hacker, Please enter 1 LETTER.  GET IT!?")
            if(notletterguess == 3):
                print("I give up.  Stop trying to mess with the program!")
            if(notletterguess == 4):
                print("That's enough.  Next time I'm shutting down")
            if(notletterguess == 5):
                sys.exit()
        else:
            #Add letter to the list of correcct letters if it is in the word
            if guess in word:
                correctLetters.append(guess)
            else:
                guesses += 1
                missedLetters.append(guess)
            return guess
        
#Replace the blanks with the letters
def guessArea():
    for i in correctLetters:
        for x in range(0,len(word)):
            if i == word[x]:
                wordblanks.insert(x, word[x] + " ")
                wordblanks.pop(x + 1)
    return ''.join(wordblanks)

#Check to see if all the letters are found
def foundAllLetters():
    for i in range(len(word)):
        if word[i] != " " and word[i] != "-":
            if word[i] not in correctLetters:
                return False
                break
    return True


#Define Variables
guesses = 0
guess = ''
missedLetters = []
correctLetters = []
notletterguess = 0
guessWord = ""
allowedGuesses = 6
usedWords = []

#Make the hangman pics        
hangmanpics = [
'''+---+
|  
|
|
|
|
=========''',
'''+---+
|   O
|
|
|
|
=========''',
'''+---+
|   O
|   |
|
|
|
=========''',
'''+---+
|   O
|   |\ 
|
|
|
=========''',
'''+---+
|   O
|  /|\ 
|
|
|
=========''',
'''+---+
|   O
|  /|\ 
|    \ 
|
|
=========''',
'''+---+
|   x
|  /|\ 
|  / \ 
|
|
=========''',
'''+---+
|   
|  I lived!
|     :)
|    /|\ 
|    / \       
========='''
               ]


#Clear the console screen
cls()

testUser("Welcome to Hangman! Do you want to play (y/n)", True)

#See if the user is running the program in IDLE
if 'idlelib.run' in sys.modules:
    testUser("It seems that you are running this game in IDLE.  \nFor this game to be the best it can be, please use a terminal window. \n'y' to continue anyway (Not recommeded) \n'n' to exit\n", True)

#Get word and the blanks
word = getCategory(getWords(), categories)
wordblanks = getBlanks()

#Main Game Loop
while True:
    #Let the user keep guessing for the amount of allowed quesses
    while guesses <= (allowedGuesses - 1):
        #If the user finds all the letters, they win!
        if foundAllLetters():
            displayGame(True)
            print("You won!")
            doneGame = True
            break
        #Update the game display
        displayGame(False)
        #Ask for a letter
        userLetterInput(guess)
    #If all the guesses are used and not all the letters were found, the user loses
    if not foundAllLetters():
        displayGame(False)
        print("Game Over." + " The word was: " + word + ". Good try!")
        doneGame = True
    #Reset the variables when the game is played again
    if doneGame:
        testUser("Do you want to play again? (y,n)", True)
        
        #Only keep the last three words in the usedWords list
        usedWords.append(word)
        if len(usedWords) > 3:
            usedWords.pop(0)
        #Re-define variables
        guesses = 0
        guess = ''
        missedLetters = []
        correctLetters = []
        notletterguess = 0
        guessWord = ""

        #See if user wants to change the category or wordfile
        if testUser('The category is ' + category + ' in ' + filename + '.' + 'Do you want to change the category or word file? (y,n)', False):
            if testUser("Do you want to change the wordfile? (y,n)", False):
                word = getCategory(getWords(), categories)
            else:
                print("Then you must want to change the category...")
                word = getCategory(listofwords, categories)
                
        else:
            word = wordisDone(wordList)

        wordblanks = getBlanks()
