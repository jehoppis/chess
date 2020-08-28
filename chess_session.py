# noinspection PyUnresolvedReferences
import game

# Creates an instance of the class 'Game' from game.py. Runs a loop consisting of white moves, check to see if the game
# is over (either white wins or stalemate), prints if black is in check, repeats for black. Loop repeats until one of
# the end checks returns 'checkmate' or 'stalemate'. Then prints all of the moves that were made. Can end the game early
# by pressing ctrl+C.

x = game.Game()

try:
    x.visualize()
    while True:
        x.move_piece('white')
        end = x.end('white')
        if end == 'checkmate':
            print('White wins the game!')
            break
        elif end == 'stalemate':
            print('The game is a draw.')
            break
        temp = x.is_threat(x.black_king, x.black_king, 'black')
        if temp[0] is True:
            print('Black is in check from '+str(x.squares[(temp[2], temp[1])]['occupied']+' located at '
                                               +str(temp[2])+str(temp[1])+'.'))
        x.move_piece('black')
        end = x.end('black')
        if end == 'checkmate':
            print('Black wins the game!')
            break
        elif end == 'stalemate':
            print('The game is a draw.')
            break
        temp = x.is_threat(x.white_king, x.white_king, 'white')
        if temp[0] is True:
            print('White is in check from '+str(x.squares[(temp[2], temp[1])]['occupied']+' located at '
                                               +str(temp[2])+str(temp[1])+'.'))
    for key in x.history:
        print(str(key) + ': ' + str(x.history[key]))
except KeyboardInterrupt:
    print('\n \nYou flipped the table!!!')
    for key in x.history:
        print(str(key) + ': ' + str(x.history[key]))