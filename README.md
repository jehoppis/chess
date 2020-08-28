# chess

The file "game.py" defines a "Game" class. This class is for a two player game of chess. The only module it requires is tabulate, which it uses to make a simple display of the chess board's current state. This class has support for both castling and en passant and contains functions to determine if there is a check or checkmate. There is limited support to determine if there is a stalemate, though the condition is using a tournament rule. In tournament chess, either player can claim stalemate after both players have made 50 consecutive moves in which no pieces have been captured by either player and no pawns have moved. This method was chosen because of the large number of different stalemate conditions that exist.

The file "chess_session.py" creates an instance of the "Game" class and sets up a loop using it's methods to make a typical two player game of chess, asking for alternating user inputs until an end condition (either checkmate, stalemate, or ctrl+C) is met.
