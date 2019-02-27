from random import randint, choice

# This is the class 'Reversi'
# An instance of this class represents a complete game

# Strategy for the 'makeMoveSmart' method was gotten
# from the following link: en.wikibooks.org/wiki/Reversi/Strategy

# I chose to automatically pick corners if they were available,
# and then if no corners were available to pick pieces on edges,
# and then if no edges or corners were available to pick the spot closest to
# the centre using a 'least-squares' method (line 139)


class Reversi:
    def __init__(self):
        # Initializes the game
        self.playerColour = ''
        self.playerScore = 0
        self.botColour = ''
        self.botScore = 0
        self.boardSize = 8
        self.topLevel = [str(i) for i in range(self.boardSize)]
        self.board = []
        self.moveset = []
        self.hint = False

    def newGame(self):
        # Produces a clean board for
        # each new game

        self.board = []
        for i in range(self.boardSize):
            self.board.append(['.'] * self.boardSize)

        self.board[3][3], self.board[3][4] = 'w', 'b'
        self.board[4][3], self.board[4][4] = 'b', 'w'

        print('', "Here is the starting board formation:", '', sep='\n')
        self.displayBoard()

    def setPlayerColour(self):
        # Sets the player's colour
        self.playerColour == ''
        while self.playerColour not in ['black', 'white']:
            self.playerColour = input("Which colour would you like to be? (black / white) ").lower()
        if self.playerColour == 'black':
            self.botColour = 'white'
            print('Since you chose ', self.playerColour,
                  ', you will play first', sep='')
        else:
            self.botColour = 'black'
            print('Since you chose ', self.playerColour, ', the bot will play first', sep='')
        return self.playerColour, self.botColour

    def displayBoard(self):
        # Displays the game board for all to see
        print(' ' * 3 + '  '.join(self.topLevel))
        for i in range(self.boardSize):
            print(str(i) + ' ' * 2 + '  '.join(self.board[i]))
        print('\n')

    def getScore(self, colour):
        # Gets the score for the colour inputted
        colour = colour[0]
        score = 0
        if colour == self.playerColour:
            bot = False
        else:
            bot = True

        for row in self.board:
            for item in row:
                if item == colour:
                    score += 1
        if bot:
            self.botScore = score
        else:
            self.playerScore = score
        return score

    def checkInput(self, dig, bot=False):
        # Checks the player's input to see if it is valid.
        # The bot's input is checked in 'botValidation'
        try:
            int(dig)
            assert self.inBoard(int(dig)), "Please choose an integer between 0 and 7."
        except TypeError:
            raise
        except AssertionError:
            raise

    def inBoard(self, num):
        # returns true if the number is inside board,
        # false otherwise
        return 0 <= num <= 7

    def botValidation(self, position):
        # Validates the naive bot's inputs
        row = position[0]
        col = position[1]
        valid = []

        for coord in row, col:
            if isinstance(coord, int) and 0 <= coord and coord <= 7:
                valid.append(0)
            else:
                valid.append(1)
        return valid

    def findValidMoves(self, colour, hint=False):
        # THIS WORKS DO NOT TOUCH
        # Checks each possible direction to see if there are tiles to flip
        # If there is a possible string of colours, follow it until you reach a '.' or the opposing
        # colour. You will then know if the path is ultimately viable or not.
        colour = colour[0].lower()
        if colour == 'b':
            oppColour = 'w'
        else:
            oppColour = 'b'

        # Get list of valid moves for each player
        # '- 1' so it gives equal opportunity to each side of the board
        middle = (self.boardSize - 1) / 2
        validMoves = []
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                # I got the idea of using a list of directions from inventwithpython.com/Chapter15.html
                if self.board[row][col] in ['.', '*']:
                    for x, y in [[1, 0], [1, 1], [0, 1], [-1, 1],
                                 [-1, 0], [-1, -1], [0, -1], [1, -1]]:
                        finalX = x
                        finalY = y
                        finalRow = row + y
                        finalCol = col + x
                        possibleScore = 0
                        if (self.inBoard(row + y) and self.inBoard(col + x) and
                                self.board[row + y][col + x] == oppColour):
                            while self.inBoard(finalRow) and self.inBoard(finalCol) and self.board[finalRow][finalCol] == oppColour:
                                finalX += x
                                finalY += y
                                finalRow = row + finalY
                                finalCol = col + finalX
                                possibleScore += 1

                            if self.inBoard(finalRow) and self.inBoard(finalCol) and self.board[finalRow][finalCol] == colour:
                                # appended as a tuple to protect against multiple moves from same starting point.
                                leastSquares = (
                                    middle - row) ** 2 + (middle - col) ** 2
                                validMoves.append(
                                    (row, col, finalRow, finalCol, possibleScore, leastSquares))
        # if hint:
        #     for row in range(len(self.board)):
        #         for col in range(len(self.board)):
        #             for move in validMoves:
        #                 if (row, col) == move[:2]:
        #                     self.board[row][col] = '*'

        return validMoves

    def isPositionValid(self, position, validMoves, colour, valid, bot=True):
        # Checks and ensures the positions chosen are valid.
        # If they are valid, determines
        self.moveset = []
        if valid == [0, 0]:
            for move in validMoves:
                if position == move[:2]:
                    self.moveset.append(move)
        # This is where 'findValidMoves' went before I moved it.

        return self.moveset != []

    # I don't use position (self.moveset instead), I just have it to appease the CMPUT175 Gods
    def makeMovePlayer(self, position, bot=False):
        # Makes the player's move once it has been validated
        if bot:
            colour = self.botColour[0]
        else:
            colour = self.playerColour[0]

        counter = 0

        for move in self.moveset:
            # print('Bot: ' + str(bot) + '. Move: ' + str(move))
            counter += -2  # to account for the two end tiles
            row = move[0]
            col = move[1]
            finalRow = move[2]
            finalCol = move[3]
            if row - finalRow == 0:  # The disks are horizontal
                # print("The horizontal was handled")
                currentCoord = min(col, finalCol)
                maxCoord = max(col, finalCol)
                while currentCoord <= maxCoord:
                    self.board[row][currentCoord] = colour
                    currentCoord += 1
                    counter += 1

            elif col - finalCol == 0:  # The disks are vertical
                # print("The vertical was handled")
                currentCoord = min(row, finalRow)
                maxCoord = max(row, finalRow)
                while currentCoord <= maxCoord:
                    self.board[currentCoord][col] = colour
                    currentCoord += 1
                    counter += 1
            else:
                # the disks are diagonal
                currentRow = row
                currentCol = col
                if row < finalRow and col < finalCol:
                    # The diagonal is down-right
                    while currentRow <= finalRow and currentCol <= finalCol:
                        self.board[currentRow][currentCol] = colour
                        currentRow += 1
                        currentCol += 1
                        counter += 1
                elif row > finalRow and col < finalCol:
                    # The diagonal is up-right
                    while currentRow >= finalRow and currentCol <= finalCol:
                        self.board[currentRow][currentCol] = colour
                        currentRow += -1
                        currentCol += 1
                        counter += 1
                elif row < finalRow and col > finalCol:
                    # The diagonal is down-left
                    while currentRow <= finalRow and currentCol >= finalCol:
                        self.board[currentRow][currentCol] = colour
                        currentRow += 1
                        currentCol += -1
                        counter += 1
                elif row > finalRow and col > finalCol:
                    # The diagonal is up-left
                    while currentRow >= finalRow and currentCol >= finalCol:
                        self.board[currentRow][currentCol] = colour
                        currentRow += -1
                        currentCol += -1
                        counter += 1

        print('\n')
        if bot:
            print("The bot flipped", counter, "tile(s).")
        else:
            print("The player flipped", counter, "tile(s).")
        print('\n')

    def makeMoveNaive(self, validMoves):
        # Chooses a random spot that is valid,
        # typically has to run multiple times
        # to produce a valid move.
        validBotMove = False
        while not validBotMove:
            row = randint(0, 7)
            col = randint(0, 7)
            valid = self.botValidation((row, col))
            if self.isPositionValid((row, col), validMoves, self.botColour, valid):
                validBotMove = True
        return (row, col)

    def makeMoveSmart(self, validMoves):
        # Who fucking knows
        # I fucking know
        cornerMoves = []
        edgeMoves = []
        for move in validMoves:
            row = move[0]
            col = move[1]
            # test for corner moves
            if (row == 0 or row == self.boardSize - 1) and (col == 0 or col == self.boardSize - 1):
                cornerMoves.append(move)
            # test for edge moves
            elif (row == 0 or row == self.boardSize - 1) or (col == 0 or col == self.boardSize - 1):
                edgeMoves.append(move)

        if cornerMoves != []:
            optimalMove = choice(cornerMoves)
            self.isPositionValid(optimalMove[:2], validMoves, self.botColour, [0, 0])
        elif edgeMoves != []:
            optimalMove = choice(edgeMoves)
            self.isPositionValid(optimalMove[:2], validMoves, self.botColour, [0, 0])
        else:
            # print('Make Move Smart')
            validMoves = sorted(validMoves, key=lambda move: move[5])
            # print("The sorted and valid moves:", validMoves)
            bestLeastSquares = validMoves[0][5]
            optimalMoves = [move for move in validMoves if move[5] == bestLeastSquares]
            optimalMove = choice(optimalMoves)
            self.isPositionValid(optimalMove[:2], validMoves, self.botColour, [0, 0])
        
        return optimalMove[:2]

    def isGameOver(self, validMoves):
        # Checks if the valid moves are empty (the definition of game over)
        return validMoves == []

    def decideWinner(self, botScore, playerScore):
        # Decides the winner and prints the results
        print("Game Over!", '\n', "The final game board is: ", '\n', sep='')
        self.displayBoard()
        if botScore < playerScore:
            print("The player wins by", str(playerScore - botScore))
        elif botScore > playerScore:
            print("The bot wins by", str(botScore - playerScore))
        else:
            print("Its a tie!")
        print("The player has a final score of " +
              str(playerScore))
        print("The bot has a final score of " +
              str(botScore))
