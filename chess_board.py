from tkinter import *
import customtkinter
from PIL import Image
import configurations


# TODO: connect textbox and chess board -> priority1
#       when a move is made on the board, write it in the next box. disable textbox
#       make a list the records move lists
#       append moves to the list -> click
#       create a function to pop() a move off the list -> use case?

# TODO: add functionality of view buttons to cycle through move list -> priority2
#        separate list of moves necessary?

# TODO: create rules for piece movement

# TODO: create ability to castle O-O, O-O-O

# TODO: create ability to play 'en passant'


class ChessBoard:
    controller = None
    parent_frame = None
    view = None

    empty_image = None
    image_size = 70

    def __init__(self, view, controller, frame):
        self.view = view
        self.controller = controller
        self.parent_frame = frame

        self.coord = []
        self.buttons = []
        self.move_list = []
        self.piece_location = []
        self.starting_position = []
        self.selected_piece = None
        self.move_from_ind = None
        self.half_move_count = 0

    def create_everything(self):

        self._connect_chess_images()
        self._make_board(self.parent_frame)
        self._starting_position_setup()
        self._new_game_set()

    def reset_board(self):
        if len(self.move_list) > 0:  # clear any existing pieces off board
            self.move_list = []
            self.half_move_count = 0
            for i in range(0, 64):
                self.piece_location[i] = None
                self.buttons[i].configure(image=self.empty_image)
        self._new_game_set()

    def _connect_chess_images(self):
        self.K_image = customtkinter.CTkImage(
            light_image=Image.open(r"C:\Users\sdkan\PycharmProjects\chessMem\images\K.png"),
            size=(self.image_size, self.image_size)
        )

        self.k_image = customtkinter.CTkImage(
            light_image=Image.open(r"C:\Users\sdkan\PycharmProjects\chessMem\images\kk.png"),
            size=(self.image_size, self.image_size)
        )
        self.Q_image = customtkinter.CTkImage(
            light_image=Image.open(r"C:\Users\sdkan\PycharmProjects\chessMem\images\Q.png"),
            size=(65, 65)
        )
        self.q_image = customtkinter.CTkImage(
            light_image=Image.open(r"C:\Users\sdkan\PycharmProjects\chessMem\images\qq.png"),
            size=(65, 65)
        )
        self.R_image = customtkinter.CTkImage(
            light_image=Image.open(r"C:\Users\sdkan\PycharmProjects\chessMem\images\R.png"),
            size=(self.image_size, self.image_size)
        )
        self.r_image = customtkinter.CTkImage(
            light_image=Image.open(r"C:\Users\sdkan\PycharmProjects\chessMem\images\rr.png"),
            size=(self.image_size, self.image_size)
        )
        self.B_image = customtkinter.CTkImage(
            light_image=Image.open(r"C:\Users\sdkan\PycharmProjects\chessMem\images\B.png"),
            size=(self.image_size, self.image_size)
        )
        self.b_image = customtkinter.CTkImage(
            light_image=Image.open(r"C:\Users\sdkan\PycharmProjects\chessMem\images\bb.png"),
            size=(self.image_size, self.image_size)
        )
        self.N_image = customtkinter.CTkImage(
            light_image=Image.open(r"C:\Users\sdkan\PycharmProjects\chessMem\images\N.png"),
            size=(self.image_size, self.image_size)
        )
        self.n_image = customtkinter.CTkImage(
            light_image=Image.open(r"C:\Users\sdkan\PycharmProjects\chessMem\images\nn.png"),
            size=(self.image_size, self.image_size)
        )
        self.P_image = customtkinter.CTkImage(
            light_image=Image.open(r"C:\Users\sdkan\PycharmProjects\chessMem\images\P.png"),
            size=(55, self.image_size)
        )
        self.p_image = customtkinter.CTkImage(
            light_image=Image.open(r"C:\Users\sdkan\PycharmProjects\chessMem\images\pp.png"),
            size=(self.image_size, self.image_size)
        )
        self.empty_image = customtkinter.CTkImage(
            light_image=Image.open(r"C:\Users\sdkan\PycharmProjects\chessMem\images\empty square.png"), size=(1, 1)
        )

    def _make_board(self, frame):
        button_size = 80
        column_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        row_list = [8, 7, 6, 5, 4, 3, 2, 1]

        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 0:
                    square_color = configurations.Light_green
                else:
                    square_color = configurations.Green

                btn_name = str(column_list[x]) + str(row_list[y])
                self.view.btn = customtkinter.CTkButton(frame, corner_radius=0, text='', width=button_size,
                                                        height=button_size,
                                                        fg_color=square_color
                                                        )
                self.view.btn.grid(column=x, row=y, padx=0, pady=0, sticky=N + S + E + W)
                self.view.btn.configure(command=lambda coordinate=btn_name: self.controller.game_board_click(self, coordinate))
                self.coord.append(btn_name)
                self.buttons.append(self.view.btn)
                self.piece_location.append(None)

    def click(self, coordinate):
        ind = self.coord.index(coordinate)

        if self.selected_piece is not None:  # on click, if exists selected piece, place at square

            if self.move_from_ind == ind:  # set selected piece to None
                self.selected_piece = None
                print("deselected piece")

            else:  # play piece and append it to move_list
                self.buttons[ind].configure(image=self.selected_piece.image)
                self.buttons[ind].configure(text='')
                self.buttons[self.move_from_ind].configure(image=self.empty_image)
                self.piece_location[self.move_from_ind] = None

                if self.piece_location[ind] is not None:
                    move_played = str(self.selected_piece.piece_notation) + 'x' + str(coordinate)
                else:
                    move_played = str(self.selected_piece.piece_notation) + str(coordinate)
                self.piece_location[ind] = self.selected_piece

                print("move played: " + move_played)
                self.selected_piece = None
                self.move_from_ind = None
                self.half_move_count += 1
                self.move_list.append(move_played)

                return move_played, self.half_move_count  # return move information str(piece_notation + coord)

        elif self.piece_location[ind] is not None:
            self.selected_piece = self.piece_location[ind]  # if no selected piece, select piece
            self.move_from_ind = ind

        else:  # if no piece in square, pass
            pass

    def _starting_position_setup(self):
        self.white_starting_pieces = []
        self.black_starting_pieces = []

        wp1 = Pawn(self, 'w')
        self.white_starting_pieces.append(wp1)
        wp2 = Pawn(self, 'w')
        self.white_starting_pieces.append(wp2)
        wp3 = Pawn(self, 'w')
        self.white_starting_pieces.append(wp3)
        wp4 = Pawn(self, 'w')
        self.white_starting_pieces.append(wp4)
        wp5 = Pawn(self, 'w')
        self.white_starting_pieces.append(wp5)
        wp6 = Pawn(self, 'w')
        self.white_starting_pieces.append(wp6)
        wp7 = Pawn(self, 'w')
        self.white_starting_pieces.append(wp7)
        wp8 = Pawn(self, 'w')
        self.white_starting_pieces.append(wp8)

        wr1 = Rook(self, 'w')
        self.white_starting_pieces.append(wr1)
        wn1 = Knight(self, 'w')
        self.white_starting_pieces.append(wn1)
        wb1 = Bishop(self, 'w')
        self.white_starting_pieces.append(wb1)
        wq1 = Queen(self, 'w')
        self.white_starting_pieces.append(wq1)
        wk = King(self, 'w')
        self.white_starting_pieces.append(wk)
        wb2 = Bishop(self, 'w')
        self.white_starting_pieces.append(wb2)
        wn2 = Knight(self, 'w')
        self.white_starting_pieces.append(wn2)
        wr2 = Rook(self, 'w')
        self.white_starting_pieces.append(wr2)

        br1 = Rook(self, 'b')
        self.black_starting_pieces.append(br1)
        bn1 = Knight(self, 'b')
        self.black_starting_pieces.append(bn1)
        bb1 = Bishop(self, 'b')
        self.black_starting_pieces.append(bb1)
        bq1 = Queen(self, 'b')
        self.black_starting_pieces.append(bq1)
        bk = King(self, 'b')
        self.black_starting_pieces.append(bk)
        bb2 = Bishop(self, 'b')
        self.black_starting_pieces.append(bb2)
        bn2 = Knight(self, 'b')
        self.black_starting_pieces.append(bn2)
        br2 = Rook(self, 'b')
        self.black_starting_pieces.append(br2)

        bp1 = Pawn(self, 'b')
        self.black_starting_pieces.append(bp1)
        bp2 = Pawn(self, 'b')
        self.black_starting_pieces.append(bp2)
        bp3 = Pawn(self, 'b')
        self.black_starting_pieces.append(bp3)
        bp4 = Pawn(self, 'b')
        self.black_starting_pieces.append(bp4)
        bp5 = Pawn(self, 'b')
        self.black_starting_pieces.append(bp5)
        bp6 = Pawn(self, 'b')
        self.black_starting_pieces.append(bp6)
        bp7 = Pawn(self, 'b')
        self.black_starting_pieces.append(bp7)
        bp8 = Pawn(self, 'b')
        self.black_starting_pieces.append(bp8)

    def _new_game_set(self):
        for i in range(0, 16):  # set up starting position
            if i < 8:
                x = 6 + (i * 8)  # white pawns start at square 6
                self.piece_location[x] = self.white_starting_pieces[i]
            else:
                x = 7 + ((i - 8) * 8)  # white pieces start at square 7
                self.piece_location[x] = self.white_starting_pieces[i]

        for i in range(0, 16):
            if i < 8:
                x = 0 + (i * 8)  # black pieces start from square 0
                self.piece_location[x] = self.black_starting_pieces[i]
            else:
                x = 1 + ((i - 8) * 8)  # black pawns start from square 1
                self.piece_location[x] = self.black_starting_pieces[i]

        for i in range(0, 64):
            x = self.piece_location[i]

            if x is not None:
                self.buttons[i].configure(image=x.image, anchor='center')
                self.buttons[i].configure(text="")
            else:
                pass  # to skip the empty squares


class King:
    def __init__(self, board, color):
        self.color = color
        if self.color == 'w':
            self.image = board.K_image
        elif self.color == 'b':
            self.image = board.k_image
        self.value = 1000
        self.piece_notation = 'K'


class Queen:
    def __init__(self, board, color):
        self.color = color
        if self.color == 'w':
            self.image = board.Q_image
        elif self.color == 'b':
            self.image = board.q_image
        self.value = 9
        self.piece_notation = 'Q'


class Rook:
    def __init__(self, board, color):
        self.color = color
        if self.color == 'w':
            self.image = board.R_image
        elif self.color == 'b':
            self.image = board.r_image
        self.value = 5
        self.piece_notation = 'R'


class Bishop:
    def __init__(self, board, color):
        self.color = color
        if self.color == 'w':
            self.image = board.B_image
        elif self.color == 'b':
            self.image = board.b_image
        self.value = 3
        self.piece_notation = 'B'


class Knight:
    def __init__(self, board, color):
        self.color = color
        if self.color == 'w':
            self.image = board.N_image
        elif self.color == 'b':
            self.image = board.n_image
        self.value = 3
        self.piece_notation = 'N'


class Pawn:
    def __init__(self, board, color):
        self.color = color
        if self.color == 'w':
            self.image = board.P_image
        elif self.color == 'b':
            self.image = board.p_image
        self.value = 1
        self.piece_notation = ''


if __name__ == '__main__':
    my_controller = ''

    root = customtkinter.CTk()
    my_frame = customtkinter.CTkFrame(root)
    my_frame.pack()

    chessBoard = ChessBoard(view=root, controller=my_controller, frame=my_frame)
    chessBoard.create_everything()
    root.mainloop()
