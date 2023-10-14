import shogi

board = shogi.Board()

print(shogi.Move.from_usi("3g3f") in board.legal_moves)

