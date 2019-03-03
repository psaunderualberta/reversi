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
        self.botColour = ''
        self.playerScore = 2
        self.botScore = 2
        self.playerMoves = []
        self.botMoves = []
        self.moveset = []
        self.boardSize = 8
        self.topLevel = [str(i) for i in range(self.boardSize)]
        self.board = []

    def newGame(self):
        # Produces a clean board for
        # each new game

        self.board = []
        for row in range(self.boardSize):
            self.board.append(['.'] * self.boardSize)

        self.board[3][3], self.board[3][4] = 'w', 'b'
        self.board[4][3], self.board[4][4] = 'b', 'w'

        print('', "Here is the starting board formation:", '', sep='\n')
        self.displayBoard(newGame=True)

    def smartOrNot(self):
        # determines if the player wants a smart bot or naive bot
        botIntelligence = ''
        while botIntelligence not in ["SMART", "NAIVE"]:
            botIntelligence = input(
                "Would you like to play against a smart bot or a naive bot? (smart / naive) ").upper()
        return botIntelligence == "SMART"

    def setPlayerColour(self):
        # Sets the player's colour
        self.playerColour == ''
        while self.playerColour not in ['black', 'white']:
            self.playerColour = input(
                "Which colour would you like to be? (black / white) ").lower()
        self.setBotColour()
        return self.playerColour, self.botColour

    def setBotColour(self):
        # Sets the bot's colour based on self.playerColour
        if self.playerColour == 'black':
            self.botColour = 'white'
            print('Since you chose ', self.playerColour,
                  ', you will play first', sep='')
        else:
            self.botColour = 'black'
            print('Since you chose ', self.playerColour,
                  ', the bot will play first', sep='')

    def displayBoard(self, newGame=False, gameOver=False):
        # Displays the game board for all to see
        print(' ' * 3 + '  '.join(self.topLevel))
        for i in range(self.boardSize):
            print(str(i) + ' ' * 2 + '  '.join(self.board[i]))
        print('\n')
        if not newGame and not gameOver:
            print("The player's score is:", self.playerScore)
            print("The bot's score is:", self.botScore, '\n')

    def getScore(self, colour):
        # Gets the score for the colour inputted
        bot = (colour != self.playerColour)
        colour = colour[0]
        score = 0
        for row in self.board:
            for item in row:
                if item == colour:
                    score += 1
        if bot:
            self.botScore = score
        else:
            self.playerScore = score
        return score

    def inBoard(self, num):
        # returns true if num is inside the board,
        # false otherwise
        return 0 <= num <= 7

    def checkPlayerInput(self, num):
        # Checks the player's input to see if it is valid.
        try:
            int(num)
            assert self.inBoard(
                int(num)), "Please choose an integer between 0 and 7."
        except Exception:
            raise

    def naiveBotValidation(self, position):
        # Validates the naive bot's inputs
        row = position[0]
        col = position[1]
        valid = []

        for coord in row, col:
            if isinstance(coord, int) and self.inBoard(coord):
                valid.append(0)
            else:
                valid.append(1)
        return valid == [0, 0]

    def findValidMoves(self, colour):
        # THIS WORKS DO NOT TOUCH
        # Checks each possible direction to see if there are tiles to flip
        # If there is a possible string of colours, follow it until you reach a '.' or the opposing
        # colour. You will then know if the path is ultimately viable or not.
        colour = colour[0]
        oppColour = 'b' if colour == 'w' else 'w'
        moveset = []
        directions = [[1, 0], [1, 1], [0, 1], [-1, 1],
                      [-1, 0], [-1, -1], [0, -1], [1, -1]]
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                # I got the idea of using a list of directions from inventwithpython.com/Chapter15.html
                if self.board[row][col] in ['.', '*']:
                    for x, y in directions:
                        move = self._findValidMoves(
                            x, y, row, col, colour, oppColour)
                        if move != None:
                            moveset.append(move)

        return moveset

    def _findValidMoves(self, x, y, row, col, colour, oppColour):
        # Helper function to findValidMoves,
        # figures out if the move is valid or not
        middle = (self.boardSize - 1) / 2
        finalX = x
        finalY = y
        finalRow = row + y
        finalCol = col + x
        if (self.inBoard(finalRow) and self.inBoard(finalCol) and
                self.board[row + y][col + x] == oppColour):
            while self.inBoard(finalRow) and self.inBoard(finalCol) and self.board[finalRow][finalCol] == oppColour:
                finalX += x
                finalY += y
                finalRow = row + finalY
                finalCol = col + finalX

            if self.inBoard(finalRow) and self.inBoard(finalCol) and self.board[finalRow][finalCol] == colour:
                # appended as a tuple to protect against multiple moves from same starting point.
                leastSquares = (
                    middle - row) ** 2 + (middle - col) ** 2
                return (row, col, finalRow, finalCol, leastSquares)
        return None

    def isPositionValid(self, position, colour, naiveBot=False):
        # Checks and ensures the positions chosen are valid.
        # If they are valid, appends the valid
        # moves to the respective moveset
        validMoves = []
        self.moveset = self.findValidMoves(colour)
        for move in self.moveset:
            if position == move[:2]:
                validMoves.append(move)
        self.moveset = validMoves
        if naiveBot:  # Only for naive bot
            return validMoves != []
        else:
            try:
                assert validMoves != [], "You cannot choose that " + \
                    "space. Please choose again."
            except Exception:
                raise

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
            print(row, col, finalRow, finalCol)
            if row - finalRow == 0:  # The disks are horizontal
                counter = self.rowMove(
                    row, col, finalRow, finalCol, colour, counter)
            elif col - finalCol == 0:  # The disks are vertical
                counter = self.colMove(
                    row, col, finalRow, finalCol, colour, counter)
            else:  # the disks are diagonal
                counter = self.diagMove(
                    row, col, finalRow, finalCol, colour, counter)

        print('\n')
        if bot:
            print("The bot flipped", counter, "tile(s).")
        else:
            print("The player flipped", counter, "tile(s).")
        print('\n')

    def rowMove(self, row, col, finalRow, finalCol, colour, counter):
        # Runs when the move is on the same row
        currentCoord = min(col, finalCol)
        maxCoord = max(col, finalCol)
        while currentCoord <= maxCoord:
            self.board[row][currentCoord] = colour
            currentCoord += 1
            counter += 1
        return counter

    def colMove(self, row, col, finalRow, finalCol, colour, counter):
        # Runs when the move is on the same column
        currentCoord = min(row, finalRow)
        maxCoord = max(row, finalRow)
        while currentCoord <= maxCoord:
            self.board[currentCoord][col] = colour
            currentCoord += 1
            counter += 1
        return counter

    def diagMove(self, row, col, finalRow, finalCol, colour, counter):
        # Runs when the move is on a diagonal
        currentRow = row
        currentCol = col
        if row < finalRow and col < finalCol:
            # The diagonal is down-right
            while currentRow <= finalRow and currentCol <= finalCol:
                currentRow, currentCol, counter = self.diagAdjust(colour, (currentRow, 1), (currentCol, 1), counter)

        elif row > finalRow and col < finalCol:
            # The diagonal is up-right
            while currentRow >= finalRow and currentCol <= finalCol:
                currentRow, currentCol, counter = self.diagAdjust(colour, (currentRow, -1), (currentCol, 1), counter)

        elif row < finalRow and col > finalCol:
            # The diagonal is down-left
            while currentRow <= finalRow and currentCol >= finalCol:
                currentRow, currentCol, counter = self.diagAdjust(colour, (currentRow, 1), (currentCol, -1), counter)

        elif row > finalRow and col > finalCol:
            # The diagonal is up-left
            while currentRow >= finalRow and currentCol >= finalCol:
                currentRow, currentCol, counter = self.diagAdjust(colour, (currentRow, -1), (currentCol, -1), counter)

        return counter

    def diagAdjust(self, colour, currentRowTup, currentColTup, counter):
        # Performs the incrementing of the diagonal move's
        # position across the board
        currentRow, currentRowIncrement = currentRowTup[0], currentRowTup[1]
        currentCol, currentColIncrement = currentColTup[0], currentColTup[1]
        self.board[currentRow][currentCol] = colour
        currentRow += currentRowIncrement
        currentCol += currentColIncrement
        counter += 1
        return currentRow, currentCol, counter

    def makeMoveNaive(self):
        # Chooses a random spot that is valid,
        # typically has to run multiple times
        # to produce a valid move.
        validBotMove = False
        while not validBotMove:
            move = (randint(0, 7), randint(0, 7))
            valid = self.naiveBotValidation(move)
            if self.isPositionValid(move, self.botColour, True) and valid:
                validBotMove = True
        self.showBotMove(move)
        return move

    def makeMoveSmart(self):
        # The move is chosen from the valid moves, and so
        # since we know the move is valid we do not need to
        # call isPositionValid()
        cornerMoves = []
        edgeMoves = []
        self.moveset = self.findValidMoves(self.botColour)
        if not self.isGameOver():
            for move in self.moveset:
                row = move[0]
                col = move[1]
                # test for corner moves (optimal)
                if (row == 0 or row == self.boardSize - 1) and (col == 0 or col == self.boardSize - 1):
                    cornerMoves.append(move)
                # test for edge moves (second best)
                elif (row == 0 or row == self.boardSize - 1) or (col == 0 or col == self.boardSize - 1):
                    edgeMoves.append(move)
            if cornerMoves != []:
                self.moveset = cornerMoves
            elif edgeMoves != []:
                self.moveset = edgeMoves
            # Choose the best move by its position on the board
            self.moveset = sorted(self.moveset, key=lambda move: move[4])
            bestLeastSquares = self.moveset[0][4]
            optimalMoves = [move for move in self.moveset if move[4] == bestLeastSquares]
            optimalMove = choice(optimalMoves)
            self.moveset = [move for move in optimalMoves if move[:2] == optimalMove[:2]]
            self.showBotMove(optimalMove)
            return optimalMove
        return None

    def showBotMove(self, move):
        # Tell the player what move the bot made
        print("The bot chose the position:")
        print("Row:", move[0])
        print("Column:", move[1])

    def isGameOver(self):
        # Checks if the valid moves are empty (the definition of game over)
        if self.moveset == []:
            print("The current player has no possible moves.")
            return True
        return False

    def decideWinner(self):
        # Decides the winner and prints the results
        print('\n', "The final game board is: ", '\n', sep='')
        self.displayBoard(gameOver=True)
        print("The player has a final score of %d" % (self.playerScore))
        print("and the bot has a final score of %d, and so" % (self.botScore))
        if self.botScore < self.playerScore:
            print("the player wins by %d!" %
                  (self.playerScore - self.botScore))
        elif self.botScore > self.playerScore:
            print("the bot wins by %d!" % (self.botScore - self.playerScore))
        else:
            print("Its a tie!")
        print("\n")
