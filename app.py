import json
from flask import Flask, render_template, request
from sfen2HTML import sfen2HTML
from move import ShogiPiece

# from finish import
import shogi
import re

selected = False
before_move = ""


app = Flask(__name__)

board= shogi.Board()

sfen = board.sfen()





@app.route("/")
def board_func():
    # move_piece = ShogiPiece("歩", (3, 3))  # ShogiPiece クラスのインスタンスを作成
    # board = [[None for _ in range(9)] for _ in range(9)]  # サンプルの将棋盤
    # legal_moves = move_piece.legal_moves(board)  # 歩の動きを取得
    # print(legal_moves)
    global sfen
    banmen = sfen2HTML(sfen)
    global selected
    global before_move
    selected = False
    before_move = ""

    return render_template("board.html", banmen=banmen)


@app.route("/call_from_ajax", methods=["POST"])
def callfromajax():
    global selected
    global before_move
    global board
    dict = {}
    if request.method == "POST":
        try:
            masu = request.form["masu"]
        except Exception as e:
            masu = str(e)

        if selected == False:
            before_move = masu
            selected= True
        elif selected == True:
            # print(選択した駒をどこに動かしますか？)
            selected = False
            print(before_move + masu)
            board.push_usi(before_move + masu)
            print(board.sfen())
            print(sfen2HTML(board.sfen()))
            before_move = ""
            dict = {"answer": sfen2HTML(board.sfen())}
    return json.dumps(dict)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
