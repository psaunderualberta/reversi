from reversi import Reversi


def main():
    # The main function of the algorithm
    continueGame = True
    reversi = Reversi()
    print(
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
        smartBot = reversi.smartOrNot()
        playerColour, botColour = reversi.setPlayerColour()
    
        # While there is a game on
        validMove = (playerColour == 'black')
        playersTurn = validMove

        while gameOn:
            # reversi.findValidMoves(playerColour)
            # reversi.findValidMoves(botColour, True)
            # Don't display the board again if the
            # player's input was invalid
            if validMove and playersTurn:
                reversi.displayBoard()
            try:
                if playersTurn:
                    if reversi.findValidMoves(playerColour) == []:
                        gameOn = False
                    else:
                        row = input("Which row you would you like to play? ")
                        if row.lower() == 'quit': # easy way to stop the game at any time
                            print("The game was stopped by the player.")
                            gameOn = False
                        else:
                            reversi.checkPlayerInput(row)
                            col = input("Which column would you like to play? ")
                            reversi.checkPlayerInput(col)
                            playerPosition = (int(row), int(col))
                            reversi.isPositionValid(playerPosition, playerColour)
            except AssertionError as e:
                validMove = False
                print(e.args[0])
            except Exception as e:
                validMove = False
                print("Error: Invalid input. Please enter an integer from 0 to 7.")
            else:
                validMove = True
                if gameOn:
                    if playersTurn:
                        reversi.makeMovePlayer(playerPosition)
                        playersTurn = False
                    else:
                        if smartBot:
                            botPosition = reversi.makeMoveSmart()
                        else:
                            botPosition = reversi.makeMoveNaive()
                        if botPosition == False:
                            gameOn = False
                        else:
                            reversi.makeMovePlayer(botPosition, bot=True)
                        playersTurn = True
            reversi.getScore(playerColour)
            reversi.getScore(botColour)

        reversi.decideWinner()
        guess = ''
        while guess not in ['Y', 'N']:
            guess = input("Would you like to play again? (Y/N) ").upper()
        if guess.upper() == 'N':
            print('Thanks for playing!')
            continueGame = False

main()
