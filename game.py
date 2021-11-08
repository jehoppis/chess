from tabulate import tabulate

#  Author: Jared Hoppis
#  This file defines a 'Game' class for a command line version of chess. The 'Game' class contains all information
#  relevant to a game of chess. Most of the relevant information is in the squares dictionary.


class Game:
    # noinspection PyTypeChecker
    def __init__(self):
        self.turn_count = (
            1  # Tracks current turn count. Updated by move_piece function.
        )

        self.fifty = 0  # Tracks last time a pawn was moved or a piece was captured in order to determine a draw after
        # fifty moves by both players.

        self.rows = range(1, 9)  # Creates the row labels for the chess board
        self.columns = list("abcdefgh")  # Creates the column labels

        self.squares = (
            dict()
        )  # This dictionary is the meat of the class. It will contain info about what piece is on
        # a given square, who the piece belongs to, what diagonals the square belongs to, etc.

        self.diagonalsTLBR = dict(
            {k: [] for k in range(15)}
        )  # Create diagonals slanting from top
        # left to bottom k=0 corresponds to a1. Diagonals are used by is_legal to determine legality of moves for
        # bishops and queens.

        self.diagonalsBLTR = dict(
            {n: [] for n in range(15)}
        )  # Create diagonals slanting from bottom left to top right
        #  k=0 corresponds to a8.

        self.black_king = (
            "e",
            8,
        )  # Property to record the location of black king. Used by is_threat to determine if
        # black is in check.
        self.white_king = ("e", 1)

        self.history = dict()  # Records all moves

        for i, row in enumerate(
            self.rows
        ):  # Filling in the squares dictionary with default info.
            for j, column in enumerate(self.columns):
                self.diagonalsTLBR[i + j].append((column, row))
                self.diagonalsBLTR[7 - i + j].append((column, row))
                if ((i + j) % 2) == 0:
                    self.squares.update(
                        {
                            (column, row): dict(
                                occupied=False, player=False, TLBR=i + j, BLTR=7 - i + j
                            )
                        }
                    )
                if ((i + j) % 2) == 1:
                    self.squares.update(
                        {
                            (column, row): dict(
                                occupied=False, player=False, TLBR=i + j, BLTR=7 - i + j
                            )
                        }
                    )

        # putting the pawns rooks knights bishops queens and kings on the board
        for column in self.columns:
            self.squares[(column, 2)]["occupied"] = "pawn"
            self.squares[(column, 2)]["player"] = "white"
            self.squares[(column, 7)]["occupied"] = "pawn"
            self.squares[(column, 7)]["player"] = "black"
        for i in [1, 8]:
            for j in ["a", "h"]:
                self.squares[(j, i)]["occupied"] = "rook"
                self.squares[(j, i)]["castle"] = True
                if i == 1:
                    self.squares[(j, i)]["player"] = "white"
                else:
                    self.squares[(j, i)]["player"] = "black"
        for i in [1, 8]:
            for j in ["b", "g"]:
                self.squares[(j, i)]["occupied"] = "knight"
                if i == 1:
                    self.squares[(j, i)]["player"] = "white"
                else:
                    self.squares[(j, i)]["player"] = "black"
        for i in [1, 8]:
            for j in ["c", "f"]:
                self.squares[(j, i)]["occupied"] = "bishop"
                if i == 1:
                    self.squares[(j, i)]["player"] = "white"
                else:
                    self.squares[(j, i)]["player"] = "black"
        for i in [1, 8]:
            self.squares[("d", i)]["occupied"] = "queen"
            if i == 1:
                self.squares[("d", i)]["player"] = "white"
            else:
                self.squares[("d", i)]["player"] = "black"
        for i in [1, 8]:
            self.squares[("e", i)]["occupied"] = "king"
            self.squares[("e", i)]["castle"] = True
            if i == 1:
                self.squares[("e", i)]["player"] = "white"
            else:
                self.squares[("e", i)]["player"] = "black"

        for i in [4, 5]:
            for j in self.columns:
                # noinspection PyTypeChecker
                self.squares[(j, i)]["en passant"] = [
                    0,
                    "-",
                ]  # This is a flag for the En Passant move. The default
                # values are never used. They are only defined here to note the format.

    # Constructs a table to show what the board looks like.
    def visualize(self, player="black"):
        def abbreviate(piece, color):
            if not piece:
                return ""
            elif piece == "pawn" and color == "white":
                return "W-p"
            elif piece == "pawn" and color == "black":
                return "B-p"
            elif piece == "rook" and color == "white":
                return "W-r"
            elif piece == "rook" and color == "black":
                return "B-r"
            elif piece == "knight" and color == "white":
                return "W-n"
            elif piece == "knight" and color == "black":
                return "B-n"
            elif piece == "bishop" and color == "white":
                return "W-b"
            elif piece == "bishop" and color == "black":
                return "B-b"
            elif piece == "queen" and color == "white":
                return "W-q"
            elif piece == "queen" and color == "black":
                return "B-q"
            elif piece == "king" and color == "white":
                return "W-K"
            elif piece == "king" and color == "black":
                return "B-K"

        table = dict()
        table["white"] = [
            [
                (
                    ((i + j) % 2)
                    * (not self.squares[self.columns[j], i]["player"])
                    * "-"
                    + ((i + j - 1) % 2)
                    * (not self.squares[self.columns[j], i]["player"])
                    * "-----"
                    + abbreviate(
                        self.squares[self.columns[j], i]["occupied"],
                        self.squares[self.columns[j], i]["player"],
                    )
                )
                for j in range(len(self.columns))
            ]
            for i in range(8, 0, -1)
        ]
        table["black"] = list(reversed([list(reversed(row)) for row in table["white"]]))

        if player == "white":
            print(
                tabulate(
                    table["white"],
                    headers=self.columns,
                    showindex=list(range(8, 0, -1)),
                    stralign="center",
                )
            )
        if player == "black":
            print(
                tabulate(
                    table["black"],
                    headers=list(reversed(self.columns)),
                    showindex=list(range(1, 9)),
                    stralign="center",
                )
            )

    # Assumes current_pos and end_pos are in the right format. Checks to see if moving from current_pos to end_pos
    # is a legal move for player 'color' to make (excluding castling and ignoring check restrictions).
    def is_legal(self, current_pos, end_pos, color):
        cur_col_index = self.columns.index(current_pos[0])
        end_col_index = self.columns.index(end_pos[0])
        if current_pos == end_pos:
            return False
        elif color == self.squares[(end_pos[0], int(end_pos[1]))]["player"]:
            return False
        # Pawn----------------------------------------------------------------------------------------------------------
        elif self.squares[(current_pos[0], int(current_pos[1]))]["occupied"] == "pawn":
            if current_pos[0] == end_pos[0]:
                if (
                    self.squares[(current_pos[0], int(current_pos[1]))]["player"]
                    == "white"
                ):
                    if int(current_pos[1]) == 2:
                        if all(
                            [
                                not self.squares[(current_pos[0], 3)]["occupied"],
                                not self.squares[(current_pos[0], 4)]["occupied"],
                                int(end_pos[1]) == 4,
                            ]
                        ):
                            return True
                    if all(
                        [
                            int(current_pos[1]) + 1 == int(end_pos[1]),
                            not self.squares[(current_pos[0], int(end_pos[1]))][
                                "occupied"
                            ],
                        ]
                    ):
                        return True
                    else:
                        return False
                elif (
                    self.squares[(current_pos[0], int(current_pos[1]))]["player"]
                    == "black"
                ):
                    if int(current_pos[1]) == 7:
                        if all(
                            [
                                not self.squares[(current_pos[0], 6)]["occupied"],
                                not self.squares[(current_pos[0], 5)]["occupied"],
                                int(end_pos[1]) == 5,
                            ]
                        ):
                            return True
                    if all(
                        [
                            int(current_pos[1]) - 1 == int(end_pos[1]),
                            not self.squares[(current_pos[0], int(end_pos[1]))][
                                "occupied"
                            ],
                        ]
                    ):
                        return True
                    else:
                        return False
            if current_pos[0] != end_pos[0]:
                if (
                    self.squares[(current_pos[0], int(current_pos[1]))]["player"]
                    == "white"
                ):
                    if all(
                        [
                            cur_col_index + 1 == end_col_index,
                            int(current_pos[1]) + 1 == int(end_pos[1]),
                            self.squares[(end_pos[0], int(end_pos[1]))]["occupied"],
                        ]
                    ):
                        return True
                    elif all(
                        [
                            cur_col_index - 1 == end_col_index,
                            int(current_pos[1]) + 1 == int(end_pos[1]),
                            self.squares[(end_pos[0], int(end_pos[1]))]["occupied"],
                        ]
                    ):
                        return True
                    elif all(
                        [
                            cur_col_index + 1 == end_col_index,
                            int(current_pos[1]) + 1 == int(end_pos[1]),
                            int(current_pos[1]) == 5,
                        ]
                    ):
                        if self.squares[(current_pos[0], int(current_pos[1]))][
                            "en passant"
                        ] == [self.turn_count, self.columns[end_col_index]]:
                            return True
                    elif all(
                        [
                            cur_col_index - 1 == end_col_index,
                            int(current_pos[1]) + 1 == int(end_pos[1]),
                            int(current_pos[1]) == 5,
                        ]
                    ):
                        if self.squares[(current_pos[0], int(current_pos[1]))][
                            "en passant"
                        ] == [self.turn_count, self.columns[end_col_index]]:
                            return True
                    else:
                        return False
                elif (
                    self.squares[(current_pos[0], int(current_pos[1]))]["player"]
                    == "black"
                ):
                    if all(
                        [
                            cur_col_index + 1 == end_col_index,
                            int(current_pos[1]) - 1 == int(end_pos[1]),
                            self.squares[(end_pos[0], int(end_pos[1]))]["occupied"],
                        ]
                    ):
                        return True
                    elif all(
                        [
                            cur_col_index - 1 == end_col_index,
                            int(current_pos[1]) - 1 == int(end_pos[1]),
                            self.squares[(end_pos[0], int(end_pos[1]))]["occupied"],
                        ]
                    ):
                        return True
                    elif all(
                        [
                            cur_col_index + 1 == end_col_index,
                            int(current_pos[1]) - 1 == int(end_pos[1]),
                            int(current_pos[1]) == 4,
                        ]
                    ):
                        if self.squares[(current_pos[0], int(current_pos[1]))][
                            "en passant"
                        ] == [self.turn_count, self.columns[end_col_index]]:
                            return True
                    elif all(
                        [
                            cur_col_index - 1 == end_col_index,
                            int(current_pos[1]) - 1 == int(end_pos[1]),
                            int(current_pos[1]) == 4,
                        ]
                    ):
                        if self.squares[(current_pos[0], int(current_pos[1]))][
                            "en passant"
                        ] == [self.turn_count, self.columns[end_col_index]]:
                            return True
                    else:
                        return False
        # Rook----------------------------------------------------------------------------------------------------------
        elif self.squares[(current_pos[0], int(current_pos[1]))]["occupied"] == "rook":
            if current_pos[0] != end_pos[0] and current_pos[1] != end_pos[1]:
                return False
            else:
                spaces_are_empty = True
                if current_pos[0] == end_pos[0]:
                    if int(current_pos[1]) < int(end_pos[1]):
                        for i in range(int(current_pos[1]) + 1, int(end_pos[1])):
                            if not self.squares[(current_pos[0], i)]["occupied"]:
                                spaces_are_empty = False
                    elif int(current_pos[1]) > int(end_pos[1]):
                        for i in range(int(current_pos[1]) - 1, int(end_pos[1]), -1):
                            if not self.squares[(current_pos[0], i)]["occupied"]:
                                spaces_are_empty = False
                    if all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return True
                    elif not all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return False
                else:
                    if cur_col_index < end_col_index:
                        for i in range(cur_col_index + 1, end_col_index):
                            if not self.squares[(self.columns[i], int(current_pos[1]))][
                                "occupied"
                            ]:
                                spaces_are_empty = False
                    elif cur_col_index > end_col_index:
                        for i in range(cur_col_index - 1, end_col_index, -1):
                            if not self.squares[(self.columns[i], int(current_pos[1]))][
                                "occupied"
                            ]:
                                spaces_are_empty = False
                    if all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return True
                    elif not all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return False
        # Knight--------------------------------------------------------------------------------------------------------
        elif (
            self.squares[(current_pos[0], int(current_pos[1]))]["occupied"] == "knight"
        ):
            if (
                (
                    int(current_pos[1]) + 2 == int(end_pos[1])
                    and (
                        cur_col_index + 1 == end_col_index
                        or cur_col_index - 1 == end_col_index
                    )
                )
                or (
                    int(current_pos[1]) - 2 == int(end_pos[1])
                    and (
                        cur_col_index + 1 == end_col_index
                        or cur_col_index - 1 == end_col_index
                    )
                )
                or (
                    cur_col_index - 2 == end_col_index
                    and (
                        int(current_pos[1]) + 1 == int(end_pos[1])
                        or int(current_pos[1]) - 1 == int(end_pos[1])
                    )
                )
                or (
                    cur_col_index + 2 == end_col_index
                    and (
                        int(current_pos[1]) + 1 == int(end_pos[1])
                        or int(current_pos[1]) - 1 == int(end_pos[1])
                    )
                )
            ) and self.squares[(end_pos[0], int(end_pos[1]))]["player"] != color:
                return True
            else:
                return False
        # Bishop--------------------------------------------------------------------------------------------------------
        elif (
            self.squares[(current_pos[0], int(current_pos[1]))]["occupied"] == "bishop"
        ):
            spaces_are_empty = True
            if (
                self.squares[(current_pos[0], int(current_pos[1]))]["TLBR"]
                == self.squares[(end_pos[0], int(end_pos[1]))]["TLBR"]
            ):
                cur_diag_index = self.diagonalsTLBR[
                    self.squares[(current_pos[0], int(current_pos[1]))]["TLBR"]
                ].index((current_pos[0], int(current_pos[1])))
                end_diag_index = self.diagonalsTLBR[
                    self.squares[(end_pos[0], int(end_pos[1]))]["TLBR"]
                ].index((end_pos[0], int(end_pos[1])))
                if cur_diag_index < end_diag_index:
                    for i in range(cur_diag_index + 1, end_diag_index):
                        if self.squares[
                            self.diagonalsTLBR[
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "TLBR"
                                ]
                            ][i]
                        ]["occupied"]:
                            spaces_are_empty = False
                    if all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return True
                    else:
                        return False
                elif cur_diag_index > end_diag_index:
                    for i in range(cur_diag_index - 1, end_diag_index, -1):
                        if not self.squares[
                            self.diagonalsTLBR[
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "TLBR"
                                ]
                            ][i]
                        ]["occupied"]:
                            spaces_are_empty = False
                    if all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return True
                    else:
                        return False
            elif (
                self.squares[(current_pos[0], int(current_pos[1]))]["BLTR"]
                == self.squares[(end_pos[0], int(end_pos[1]))]["BLTR"]
            ):
                cur_diag_index = self.diagonalsBLTR[
                    self.squares[(current_pos[0], int(current_pos[1]))]["BLTR"]
                ].index((current_pos[0], int(current_pos[1])))
                end_diag_index = self.diagonalsBLTR[
                    self.squares[(end_pos[0], int(end_pos[1]))]["BLTR"]
                ].index((end_pos[0], int(end_pos[1])))
                if cur_diag_index < end_diag_index:
                    for i in range(cur_diag_index + 1, end_diag_index):
                        if self.squares[
                            self.diagonalsBLTR[
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "BLTR"
                                ]
                            ][i]
                        ]["occupied"]:
                            spaces_are_empty = False
                    if all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return True
                    else:
                        return False
                elif cur_diag_index > end_diag_index:
                    for i in range(cur_diag_index - 1, end_diag_index, -1):
                        if self.squares[
                            self.diagonalsBLTR[
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "BLTR"
                                ]
                            ][i]
                        ]["occupied"]:
                            spaces_are_empty = False
                    if all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return True
                    else:
                        return False
        # Queen---------------------------------------------------------------------------------------------------------
        elif self.squares[(current_pos[0], int(current_pos[1]))]["occupied"] == "queen":
            # Copy of rook movement------------
            if current_pos[0] != end_pos[0] and current_pos[1] != end_pos[1]:
                return False
            else:
                spaces_are_empty = True
                if current_pos[0] == end_pos[0]:
                    if int(current_pos[1]) < int(end_pos[1]):
                        for i in range(int(current_pos[1]) + 1, int(end_pos[1])):
                            if not self.squares[(current_pos[0], i)]["occupied"]:
                                spaces_are_empty = False
                    elif int(current_pos[1]) > int(end_pos[1]):
                        for i in range(int(current_pos[1]) - 1, int(end_pos[1]), -1):
                            if not self.squares[(current_pos[0], i)]["occupied"]:
                                spaces_are_empty = False
                    if all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return True
                    elif not all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return False
                else:
                    if cur_col_index < end_col_index:
                        for i in range(cur_col_index + 1, end_col_index):
                            if not self.squares[(self.columns[i], int(current_pos[1]))][
                                "occupied"
                            ]:
                                spaces_are_empty = False
                    elif cur_col_index > end_col_index:
                        for i in range(cur_col_index - 1, end_col_index, -1):
                            if not self.squares[(self.columns[i], int(current_pos[1]))][
                                "occupied"
                            ]:
                                spaces_are_empty = False
                    if all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return True
                    elif not all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return False
            # Copy of Bishop movement--------------
            spaces_are_empty = True
            if (
                self.squares[(current_pos[0], int(current_pos[1]))]["TLBR"]
                == self.squares[(end_pos[0], int(end_pos[1]))]["TLBR"]
            ):
                cur_diag_index = self.diagonalsTLBR[
                    self.squares[(current_pos[0], int(current_pos[1]))]["TLBR"]
                ].index((current_pos[0], int(current_pos[1])))
                end_diag_index = self.diagonalsTLBR[
                    self.squares[(end_pos[0], int(end_pos[1]))]["TLBR"]
                ].index((end_pos[0], int(end_pos[1])))
                if cur_diag_index < end_diag_index:
                    for i in range(cur_diag_index + 1, end_diag_index):
                        if self.squares[
                            self.diagonalsTLBR[
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "TLBR"
                                ]
                            ][i]
                        ]["occupied"]:
                            spaces_are_empty = False
                    if all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return True
                    else:
                        return False
                elif cur_diag_index > end_diag_index:
                    for i in range(cur_diag_index - 1, end_diag_index, -1):
                        if not self.squares[
                            self.diagonalsTLBR[
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "TLBR"
                                ]
                            ][i]
                        ]["occupied"]:
                            spaces_are_empty = False
                    if all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return True
                    else:
                        return False
            elif (
                self.squares[(current_pos[0], int(current_pos[1]))]["BLTR"]
                == self.squares[(end_pos[0], int(end_pos[1]))]["BLTR"]
            ):
                cur_diag_index = self.diagonalsBLTR[
                    self.squares[(current_pos[0], int(current_pos[1]))]["BLTR"]
                ].index((current_pos[0], int(current_pos[1])))
                end_diag_index = self.diagonalsBLTR[
                    self.squares[(end_pos[0], int(end_pos[1]))]["BLTR"]
                ].index((end_pos[0], int(end_pos[1])))
                if cur_diag_index < end_diag_index:
                    for i in range(cur_diag_index + 1, end_diag_index):
                        if self.squares[
                            self.diagonalsBLTR[
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "BLTR"
                                ]
                            ][i]
                        ]["occupied"]:
                            spaces_are_empty = False
                    if all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return True
                    else:
                        return False
                elif cur_diag_index > end_diag_index:
                    for i in range(cur_diag_index - 1, end_diag_index, -1):
                        if self.squares[
                            self.diagonalsBLTR[
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "BLTR"
                                ]
                            ][i]
                        ]["occupied"]:
                            spaces_are_empty = False
                    if all(
                        [
                            spaces_are_empty,
                            self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            != color,
                        ]
                    ):
                        return True
                    else:
                        return False
        # King----------------------------------------------------------------------------------------------------------
        elif self.squares[(current_pos[0], int(current_pos[1]))]["occupied"] == "king":
            if all(
                [
                    end_col_index
                    in [cur_col_index - 1, cur_col_index, cur_col_index + 1],
                    int(end_pos[1])
                    in [
                        int(current_pos[1]) - 1,
                        int(current_pos[1]),
                        int(current_pos[1]) + 1,
                    ],
                    self.squares[(end_pos[0], int(end_pos[1]))]["player"] != color,
                ]
            ):
                return True
            else:
                return False

    # Again assumes current_pos and end_pos are in the right format. Determines if the given move will put player
    # 'color' in check. If so, gives the row and column of the first piece found that will create check.
    def is_threat(self, current_pos, end_pos, color):
        if all(
            [
                self.squares[(current_pos[0], int(current_pos[1]))]["occupied"]
                == "king",
                color == "white",
            ]
        ):
            self.white_king = (end_pos[0], int(end_pos[1]))
        elif all(
            [
                self.squares[(current_pos[0], int(current_pos[1]))]["occupied"]
                == "king",
                color == "black",
            ]
        ):
            self.black_king = (end_pos[0], int(end_pos[1]))
        temp = self.squares[(end_pos[0], int(end_pos[1]))]["occupied"]
        temp2 = self.squares[(end_pos[0], int(end_pos[1]))]["player"]
        self.squares[(end_pos[0], int(end_pos[1]))]["occupied"] = self.squares[
            (current_pos[0], int(current_pos[1]))
        ]["occupied"]
        self.squares[(end_pos[0], int(end_pos[1]))]["player"] = self.squares[
            (current_pos[0], int(current_pos[1]))
        ]["player"]
        self.squares[(current_pos[0], int(current_pos[1]))]["occupied"] = False
        self.squares[(current_pos[0], int(current_pos[1]))]["player"] = False
        if color == "white":
            for i in self.rows:
                for j in self.columns:
                    if self.squares[(j, i)]["player"] == "black":
                        if self.is_legal((j, i), self.white_king, "black"):
                            self.squares[(current_pos[0], int(current_pos[1]))][
                                "occupied"
                            ] = self.squares[(end_pos[0], int(end_pos[1]))]["occupied"]
                            self.squares[(current_pos[0], int(current_pos[1]))][
                                "player"
                            ] = self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            self.squares[(end_pos[0], int(end_pos[1]))][
                                "occupied"
                            ] = temp
                            self.squares[(end_pos[0], int(end_pos[1]))][
                                "player"
                            ] = temp2
                            if (
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "occupied"
                                ]
                                == "king"
                            ):
                                self.white_king = (current_pos[0], int(current_pos[1]))
                            return True, i, j
            self.squares[(current_pos[0], int(current_pos[1]))][
                "occupied"
            ] = self.squares[(end_pos[0], int(end_pos[1]))]["occupied"]
            self.squares[(current_pos[0], int(current_pos[1]))][
                "player"
            ] = self.squares[(end_pos[0], int(end_pos[1]))]["player"]
            self.squares[(end_pos[0], int(end_pos[1]))]["occupied"] = temp
            self.squares[(end_pos[0], int(end_pos[1]))]["player"] = temp2
            if (
                self.squares[(current_pos[0], int(current_pos[1]))]["occupied"]
                == "king"
            ):
                self.white_king = (current_pos[0], int(current_pos[1]))
            return False, -1, -1
        # ------------------------
        elif color == "black":
            for i in self.rows:
                for j in self.columns:
                    if self.squares[(j, i)]["player"] == "white":
                        if self.is_legal((j, i), self.black_king, "white"):
                            self.squares[(current_pos[0], int(current_pos[1]))][
                                "occupied"
                            ] = self.squares[(end_pos[0], int(end_pos[1]))]["occupied"]
                            self.squares[(current_pos[0], int(current_pos[1]))][
                                "player"
                            ] = self.squares[(end_pos[0], int(end_pos[1]))]["player"]
                            self.squares[(end_pos[0], int(end_pos[1]))][
                                "occupied"
                            ] = temp
                            self.squares[(end_pos[0], int(end_pos[1]))][
                                "player"
                            ] = temp2
                            if (
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "occupied"
                                ]
                                == "king"
                            ):
                                self.black_king = (current_pos[0], int(current_pos[1]))
                            return True, i, j
            self.squares[(current_pos[0], int(current_pos[1]))][
                "occupied"
            ] = self.squares[(end_pos[0], int(end_pos[1]))]["occupied"]
            self.squares[(current_pos[0], int(current_pos[1]))][
                "player"
            ] = self.squares[(end_pos[0], int(end_pos[1]))]["player"]
            self.squares[(end_pos[0], int(end_pos[1]))]["occupied"] = temp
            self.squares[(end_pos[0], int(end_pos[1]))]["player"] = temp2
            if (
                self.squares[(current_pos[0], int(current_pos[1]))]["occupied"]
                == "king"
            ):
                self.black_king = (current_pos[0], int(current_pos[1]))
            return False, -1, -1

    # Again assumes current_pos and end_pos are in the right format. Determines if the given move is a valid castle.
    def is_legal_castle(self, current_pos, end_pos, color):
        if all(
            [
                color == "white",
                (end_pos[0], int(end_pos[1])) in [("c", 1), ("g", 1)],
                (current_pos[0], int(current_pos[1])) == ("e", 1),
            ]
        ):
            temp = self.is_threat(current_pos, current_pos, color)
            if all(
                [
                    self.squares[(current_pos[0], int(current_pos[1]))]["castle"],
                    not temp[0],
                ]
            ):
                if all([end_pos[0] == "c", not self.squares[("b", 1)]["occupied"]]):
                    if self.squares[("a", 1)]["castle"]:
                        temp2 = True
                        for i in ["c", "d"]:
                            temp3 = self.is_threat(current_pos, (i, 1), "white")
                            if not all(
                                [not self.squares[(i, 1)]["occupied"], not temp3[0]]
                            ):
                                temp2 = False
                        return temp2
                elif end_pos[0] == "g":
                    if self.squares[("h", 1)]["castle"]:
                        temp2 = True
                        for i in ["f", "g"]:
                            temp3 = self.is_threat(current_pos, (i, 1), "white")
                            if not all(
                                [not self.squares[(i, 1)]["occupied"], not temp3[0]]
                            ):
                                temp2 = False
                        return temp2
        elif (
            color == "black"
            and (end_pos[0], int(end_pos[1])) in [("c", 8), ("g", 8)]
            and (current_pos[0], int(current_pos[1])) == ("e", 8)
        ):
            temp = self.is_threat(current_pos, current_pos, color)
            if all(
                [
                    self.squares[(current_pos[0], int(current_pos[1]))]["castle"],
                    not temp[0],
                ]
            ):
                if all([end_pos[0] == "c", not self.squares[("b", 8)]["occupied"]]):
                    if self.squares[("a", 8)]["castle"]:
                        temp2 = True
                        for i in ["c", "d"]:
                            temp3 = self.is_threat(current_pos, (i, 8), "white")
                            if not all(
                                [not self.squares[(i, 8)]["occupied"], not temp3[0]]
                            ):
                                temp2 = False
                        return temp2
                elif end_pos[0] == "g":
                    if self.squares[("h", 8)]["castle"]:
                        temp2 = True
                        for i in ["f", "g"]:
                            temp3 = self.is_threat(current_pos, (i, 8), "white")
                            if not all(
                                [not self.squares[(i, 8)]["occupied"], not temp3[0]]
                            ):
                                temp2 = False
                        return temp2
        else:
            return False

    # First asks user to input a square to move from. Checks to see if the input is in the correct format and that the
    # selected square contains a piece belonging to 'color'. Then asks user to input a square to move to, and uses
    # the above functions to determine if it is a legal move. If it is, the function moves the piece, if not, it asks
    # for another input. The 'color' argument determines which player is moving a piece.
    # noinspection PyTypeChecker
    def move_piece(self, color):
        while True:
            while True:
                current_pos = input(
                    "What piece would you ("
                    + str(color)
                    + ") like to move? Type 'help' for assistance.\nInput:"
                )
                if current_pos == "help":
                    print(
                        "To make a move, type the column letter followed by the row number\n"
                        + "of the piece you would like to move. Another query will follow asking you\n"
                        + "where you would like to move that piece. Example: 'c3'."
                    )
                    continue
                if all(
                    [
                        type(current_pos) == str,
                        len(current_pos) == 2,
                    ]
                ):
                    if all(
                        [
                            current_pos[0] in self.columns,
                            int(current_pos[1]) in self.rows,
                            color
                            == self.squares[(current_pos[0], int(current_pos[1]))][
                                "player"
                            ],
                        ]
                    ):
                        print("Input received.")
                        break
                    else:
                        print(
                            "You either typed something that wasn't a square, that square is\n"
                            + "unoccupied, or you do not own that piece."
                        )
                        continue
                else:
                    print(
                        "You either typed something that wasn't a square, that square is\n"
                        + "unoccupied, or you do not own that piece."
                    )
                    continue
            while True:
                end_pos = input(
                    "Where would you like to move your "
                    + str(
                        self.squares[(current_pos[0], int(current_pos[1]))]["occupied"]
                    )
                    + " (currently at "
                    + current_pos
                    + ") to?\nInput:"
                )
                if end_pos == "help":
                    print(
                        "To finish making a move, type the column letter followed by the row number \
                        of the square you would like to move the piece to. Example: 'c3'.\n"
                        + "If you want to select a different piece, type 'back'."
                    )
                    continue
                elif end_pos == "back":
                    break
                if all(
                    [
                        type(end_pos) == str,
                        len(end_pos) == 2,
                    ]
                ):
                    if not all(
                        [
                            end_pos[0] in self.columns,
                            int(end_pos[1]) in self.rows,
                            self.is_legal(current_pos, end_pos, color)
                            or self.is_legal_castle(current_pos, end_pos, color),
                        ]
                    ):
                        print("You typed something that wasn't a valid square.")
                        self.visualize(player=color)
                        continue
                    else:
                        break
                elif all(
                    [
                        type(end_pos) == str,
                        len(end_pos) == 2,
                        end_pos[0] in self.columns,
                        int(end_pos[1]) in self.rows,
                        not self.is_legal(current_pos, end_pos, color),
                        not self.is_legal_castle(current_pos, end_pos, color),
                    ]
                ):
                    print("That is not a legal move.")
                    self.visualize(player=color)
                    break
            if end_pos != "back":
                if self.is_legal(current_pos, end_pos, color):
                    temp = self.is_threat(current_pos, end_pos, color)
                    if temp[0]:
                        i = temp[1]
                        j = temp[2]
                        print(
                            "That move would place white in check from "
                            + str(self.squares[(j, i)]["occupied"])
                            + " at "
                            + str(j)
                            + str(i)
                            + "."
                        )
                    elif not temp[0]:
                        cur_col_index = self.columns.index(current_pos[0])
                        end_col_index = self.columns.index(end_pos[0])
                        if (
                            self.squares[(current_pos[0], int(current_pos[1]))][
                                "occupied"
                            ]
                            == "king"
                        ):
                            if color == "white":
                                self.white_king = (end_pos[0], int(end_pos[1]))
                            elif color == "black":
                                self.black_king = (end_pos[0], int(end_pos[1]))
                        # Keeping track of game progress for the fifty move rule
                        if any(
                            [
                                self.squares[(end_pos[0], int(end_pos[1]))]["occupied"],
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "occupied"
                                ]
                                == "pawn",
                            ]
                        ):
                            self.fifty = self.turn_count
                        # Flagging for en passant
                        if all(
                            [
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "player"
                                ]
                                == "white",
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "occupied"
                                ]
                                == "pawn",
                            ]
                        ):
                            if int(current_pos[1]) == 2:
                                if all(
                                    [
                                        not self.squares[(current_pos[0], 3)][
                                            "occupied"
                                        ],
                                        not self.squares[(current_pos[0], 4)][
                                            "occupied"
                                        ],
                                        int(end_pos[1]) == 4,
                                    ]
                                ):
                                    if cur_col_index > 0:
                                        # noinspection PyTypeChecker
                                        self.squares[
                                            (self.columns[cur_col_index - 1], 4)
                                        ]["en passant"] = [
                                            self.turn_count + 1,
                                            self.columns[cur_col_index],
                                        ]
                                    if cur_col_index < 7:
                                        # noinspection PyTypeChecker
                                        self.squares[
                                            (self.columns[cur_col_index + 1], 4)
                                        ]["en passant"] = [
                                            self.turn_count + 1,
                                            self.columns[cur_col_index],
                                        ]
                            elif all(
                                [
                                    not self.squares[(end_pos[0], int(end_pos[1]))][
                                        "occupied"
                                    ],
                                    cur_col_index != end_col_index,
                                ]
                            ):
                                self.squares[(end_pos[0], int(current_pos[1]))][
                                    "occupied"
                                ] = False
                                self.squares[(end_pos[0], int(current_pos[1]))][
                                    "player"
                                ] = False
                        if all(
                            [
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "player"
                                ]
                                == "black",
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "occupied"
                                ]
                                == "pawn",
                            ]
                        ):
                            if int(current_pos[1]) == 7:
                                if all(
                                    [
                                        not self.squares[(current_pos[0], 6)][
                                            "occupied"
                                        ],
                                        not self.squares[(current_pos[0], 5)][
                                            "occupied"
                                        ],
                                        int(end_pos[1]) == 5,
                                    ]
                                ):
                                    if cur_col_index > 0:
                                        # noinspection PyTypeChecker
                                        self.squares[
                                            (self.columns[cur_col_index - 1], 5)
                                        ]["en passant"] = [
                                            self.turn_count + 1,
                                            self.columns[cur_col_index],
                                        ]
                                    if cur_col_index < 7:
                                        # noinspection PyTypeChecker
                                        self.squares[
                                            (self.columns[cur_col_index + 1], 5)
                                        ]["en passant"] = [
                                            self.turn_count + 1,
                                            self.columns[cur_col_index],
                                        ]
                            elif all(
                                [
                                    not self.squares[(end_pos[0], int(end_pos[1]))][
                                        "occupied"
                                    ],
                                    cur_col_index != end_col_index,
                                ]
                            ):
                                self.squares[(end_pos[0], int(current_pos[1]))][
                                    "occupied"
                                ] = False
                                self.squares[(end_pos[0], int(current_pos[1]))][
                                    "player"
                                ] = False
                        # Making sure a rook that's moved won't be able to castle.
                        if all(
                            [
                                self.squares[(current_pos[0], int(current_pos[1]))][
                                    "occupied"
                                ]
                                == "rook",
                                (current_pos[0], int(current_pos[1]))
                                in [
                                    ("a", 1),
                                    ("a", 8),
                                    ("h", 1),
                                    ("h", 8),
                                ],
                            ]
                        ):
                            self.squares[(current_pos[0], int(current_pos[1]))][
                                "castle"
                            ] = False
                        self.history[self.turn_count] = (
                            self.squares[(current_pos[0], int(current_pos[1]))][
                                "occupied"
                            ],
                            (current_pos[0], int(current_pos[1])),
                            (end_pos[0], int(end_pos[1])),
                        )

                        self.squares[(end_pos[0], int(end_pos[1]))][
                            "player"
                        ] = self.squares[(current_pos[0], int(current_pos[1]))][
                            "player"
                        ]
                        self.squares[(end_pos[0], int(end_pos[1]))][
                            "occupied"
                        ] = self.squares[(current_pos[0], int(current_pos[1]))][
                            "occupied"
                        ]
                        self.squares[(current_pos[0], int(current_pos[1]))][
                            "player"
                        ] = False
                        self.squares[(current_pos[0], int(current_pos[1]))][
                            "occupied"
                        ] = False
                        print("Move completed.")
                        self.turn_count += 1
                        if all(
                            [
                                self.squares[(end_pos[0], int(end_pos[1]))]["occupied"]
                                == "pawn",
                                int(end_pos[1]) in [1, 8],
                            ]
                        ):
                            while True:
                                promo = input(
                                    "What piece would you like to promote your pawn to? Type\n"
                                    "queen, rook, knight, or bishop.\n"
                                    "Input:"
                                )
                                if promo not in ["queen", "rook", "knight", "bishop"]:
                                    print("Invalid selection. Try again.")
                                    continue
                                else:
                                    # noinspection PyTypeChecker
                                    self.squares[(end_pos[0], int(end_pos[1]))][
                                        "occupied"
                                    ] = promo
                                    break
                        if color == "white":
                            self.visualize(player="black")
                        else:
                            self.visualize(player="white")
                        break

                elif self.is_legal_castle(current_pos, end_pos, color):
                    if color == "white":
                        self.white_king = (end_pos[0], int(end_pos[1]))
                    elif color == "black":
                        self.black_king = (end_pos[0], int(end_pos[1]))
                    self.history[self.turn_count] = (
                        self.squares[(current_pos[0], int(current_pos[1]))]["occupied"],
                        (current_pos[0], int(current_pos[1])),
                        (end_pos[0], int(end_pos[1])),
                    )
                    self.squares[(end_pos[0], int(end_pos[1]))][
                        "player"
                    ] = self.squares[(current_pos[0], int(current_pos[1]))]["player"]
                    self.squares[(end_pos[0], int(end_pos[1]))][
                        "occupied"
                    ] = self.squares[(current_pos[0], int(current_pos[1]))]["occupied"]
                    self.squares[(current_pos[0], int(current_pos[1]))][
                        "player"
                    ] = False
                    self.squares[(current_pos[0], int(current_pos[1]))][
                        "occupied"
                    ] = False
                    if (end_pos[0], int(end_pos[1])) == ("c", 1):
                        self.squares[("a", 1)]["occupied"] = False
                        self.squares[("a", 1)]["player"] = False
                        self.squares[("d", 1)]["occupied"] = "rook"
                        self.squares[("d", 1)]["player"] = color
                    if (end_pos[0], int(end_pos[1])) == ("g", 1):
                        self.squares[("h", 1)]["occupied"] = False
                        self.squares[("h", 1)]["player"] = False
                        self.squares[("f", 1)]["occupied"] = "rook"
                        self.squares[("f", 1)]["player"] = color
                    if (end_pos[0], int(end_pos[1])) == ("c", 8):
                        self.squares[("a", 8)]["occupied"] = False
                        self.squares[("a", 8)]["player"] = False
                        self.squares[("d", 8)]["occupied"] = "rook"
                        self.squares[("d", 8)]["player"] = color
                    if (end_pos[0], int(end_pos[1])) == ("g", 8):
                        self.squares[("h", 8)]["occupied"] = False
                        self.squares[("h", 8)]["player"] = False
                        self.squares[("f", 8)]["occupied"] = "rook"
                        self.squares[("f", 8)]["player"] = color
                    print("Move completed.")
                    self.turn_count += 1
                    if color == "white":
                        self.visualize(player="black")
                    else:
                        self.visualize(player="white")
                    break
                elif not self.is_legal_castle(current_pos, end_pos, color):
                    continue
            else:
                continue

    # Checks for game end conditions, checkmate or stalemate either due to unavailability of legal moves w/o check or
    # fifty moves have passed for both players without a captured piece or pawn moved. The fifty move rule comes from
    # tournament chess, despite some conditions existing where more than fifty moves are needed to force checkmate.
    def end(self, color):  # See if 'color' wins the game.
        in_check = False
        is_fifty = self.turn_count - self.fifty
        if color == "white":
            for i in self.rows:
                for j in self.columns:
                    if self.squares[(j, i)]["player"] == "white":
                        if self.is_legal((j, i), self.black_king, "white"):
                            in_check = True
                    if self.squares[(j, i)]["player"] == "black":
                        for m in self.rows:
                            for n in self.columns:
                                if self.squares[(n, m)]["player"] != "black":
                                    if self.is_legal((j, i), (n, m), "black"):
                                        if (
                                            not self.is_threat((j, i), (n, m), "black")[
                                                0
                                            ]
                                            and is_fifty < 101
                                        ):
                                            return False
            if in_check and is_fifty < 101:
                return "checkmate"
            elif not in_check and is_fifty < 101:
                return "stalemate"
            elif is_fifty >= 101:
                return "stalemate"
        elif color == "black":
            for i in self.rows:
                for j in self.columns:
                    if self.squares[(j, i)]["player"] == "black":
                        if self.is_legal((j, i), self.white_king, "black"):
                            in_check = True
                    if self.squares[(j, i)]["player"] == "white":
                        for m in self.rows:
                            for n in self.columns:
                                if self.squares[(n, m)]["player"] != "white":
                                    if self.is_legal((j, i), (n, m), "white"):
                                        if (
                                            not self.is_threat((j, i), (n, m), "white")[
                                                0
                                            ]
                                            and is_fifty < 101
                                        ):
                                            return False
            if in_check and is_fifty < 101:
                return "checkmate"
            elif not in_check and is_fifty < 101:
                return "stalemate"
            elif is_fifty >= 101:
                return "stalemate"


if __name__ == "__main__":
    x = Game()

    try:
        x.visualize(player="white")
        while True:
            x.move_piece("white")
            end = x.end("white")
            if end == "checkmate":
                print("White wins the game!")
                break
            elif end == "stalemate":
                print("The game is a draw.")
                break
            temp = x.is_threat(x.black_king, x.black_king, "black")
            if temp[0]:
                print(
                    "Black is in check from "
                    + str(
                        x.squares[(temp[2], temp[1])]["occupied"]
                        + " located at "
                        + str(temp[2])
                        + str(temp[1])
                        + "."
                    )
                )
            x.move_piece("black")
            end = x.end("black")
            if end == "checkmate":
                print("Black wins the game!")
                break
            elif end == "stalemate":
                print("The game is a draw.")
                break
            temp = x.is_threat(x.white_king, x.white_king, "white")
            if temp[0]:
                print(
                    "White is in check from "
                    + str(
                        x.squares[(temp[2], temp[1])]["occupied"]
                        + " located at "
                        + str(temp[2])
                        + str(temp[1])
                        + "."
                    )
                )
        for key in x.history:
            print(str(key) + ": " + str(x.history[key]))
    except KeyboardInterrupt:
        print("\n \nYou flipped the table!!!")
        for key in x.history:
            print(str(key) + ": " + str(x.history[key]))
