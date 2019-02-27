from reversi import Reversi



def main():
    # The main function of the algorithm
    continueGame = True
    reversi = Reversi()
    print('', "NEW GAME", '',
        "Welcome to 'Reversi'!",
        "Reversi is a 2-player game, played on an 8 x 8 board. ",
        "Players take turns placing their disks on the board",
        "with their assigned colour (Black and White). ",
        "Black is the first player to move. A player may place their ",
        "disk anywhere on the board, as long as it surrounds a group of the opponents ",
        "disks (vertically, horizontally, or diagonally) on opposite sides. ",
        "Any disks that you surround will become yours and will flip over to your colour. ",
        "The game is over when the current player has no possible legal move.",
        "You will be playing against an artificial intelligence (AI)",
        "If at any point you would like to stop playing, type 'quit' when prompted for a row.", sep='\n')

    # While the program is on
    while continueGame:
        gameOn = True
        reversi.newGame()
        playerColour, botColour = reversi.setPlayerColour()
        playerScore = 2
        botScore = 2
    
        # While there is a game on
        validMove = (playerColour == 'black')
        playersTurn = validMove
        print("The player's score is:", playerScore)
        print("The bot's score is:", botScore, '\n')

        while gameOn:
            playerMoves = reversi.findValidMoves(playerColour)
            botMoves = reversi.findValidMoves(botColour)
            print("Player's moves:", playerMoves)
            print("Bot's moves:", botMoves)
            if reversi.isGameOver(playerMoves) or reversi.isGameOver(botMoves):
                gameOn = False
            else:
                # Don't display the board again if the
                # player's input was invalid
                if validMove and playersTurn:
                    reversi.displayBoard()
                    print("The player's score is:", playerScore)
                    print("The bot's score is:", botScore, '\n')
                # Validate input and moves
                try:
                    if playersTurn and gameOn:
                        row = input("Which row you would you like to play? ")
                        if row.lower() == 'quit': # easy way to stop the game at any time
                            gameOn = False
                        reversi.checkInput(row)
                        col = input("Which column would you like to play? ")
                        reversi.checkInput(col)
                        playerPosition = (int(row), int(col))
                        move = reversi.isPositionValid(playerPosition, playerMoves, playerColour, [0, 0])
                        assert move, "You cannot choose that " + \
                            "space. Please choose again."
                except AssertionError as e:
                    validMove = False
                    print(e.args[0])
                except Exception:
                    print("Error: Invalid input. Please enter an integer from 0 to 7.")
                else:
                    validMove = True
                    if playersTurn:
                        reversi.makeMovePlayer(playerPosition)
                        playersTurn = False
                    elif gameOn:
                        # botPosition = reversi.makeMoveNaive(botMoves)
                        botPosition = reversi.makeMoveSmart(botMoves)
                        print("The bot chose the position:")
                        print("Row:", botPosition[0])
                        print("Column:", botPosition[1])
                        reversi.makeMovePlayer(botPosition, True)
                        playersTurn = True
            playerScore = reversi.getScore(playerColour)
            botScore = reversi.getScore(botColour)
        
        if botMoves ==[]:
            print("The bot has no more possible moves!")
        elif playerMoves == []:
            print("The player has no more possible moves!")

        reversi.decideWinner(botScore, playerScore)
        guess = ''
        while guess not in ['Y', 'N']:
            guess = input("Would you like to play again? (Y/N) ").upper()
        if guess.upper() == 'N':
            print('Thanks for playing!')
            continueGame = False

main()
