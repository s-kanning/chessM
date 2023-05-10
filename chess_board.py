from tkinter import *
import customtkinter
from PIL import Image
import configurations


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
        self.view_count = 0

        self.game_state_stack = []
        self.capture_stack = []

    def create_everything(self):

        self._connect_chess_images()
        self._make_board(self.parent_frame)
        self._starting_position_setup()
        self._new_game_set()

    def reset_board(self):
        if len(self.move_list) > 0:  # clear any existing pieces off board
            self.move_list.clear()
            self.view_count = 0
            for i in range(0, 64):
                self.piece_location[i] = None
                self.buttons[i].configure(image=self.empty_image)
                self._reset_square_color(i, self.buttons[i])
        self.game_state_stack.clear()
        self.capture_stack.clear()
        self._new_game_set()

    def _connect_chess_images(
            self):  # TODO replaces images with cleaner images: https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces
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
                self.view.btn.configure(
                    command=lambda coordinate=btn_name: self.controller.game_board_click(self, coordinate)
                )
                self.coord.append(btn_name)
                self.buttons.append(self.view.btn)
                self.piece_location.append(None)

    def play_move(self, coordinate):
        ind = self.coord.index(coordinate)
        if self._piece_selected_check():  # piece selected
            if self.move_from_ind is not ind:
                movement = self._follow_movement_rules(self.move_from_ind, ind)
                if movement[0]:  # (from, to)  # includes: legal, special, sliding
                    if self._piece_in_square_check(ind):
                        if self.piece_location[ind].color != self.selected_piece.color:
                            self._capture_piece(ind)
                            self._move_piece(ind)
                            return self._return_notation(ind, coordinate, True, False)
                        else:
                            pass
                    else:
                        if movement[1] == 'castle':
                            print('castle')
                            self._move_piece(ind)
                            self._castle(ind)
                            return self._return_notation(ind, coordinate, False, True)
                        elif movement[1] == 'en passant':
                            print('en passant')
                            self._move_piece(ind)
                            self._en_passant()
                            return self._return_notation(ind, coordinate, True, True)
                        elif movement[1] == 'promotion':
                            print('promotion')
                            self._move_piece(ind)
                            self._promotion(ind)
                            return self._return_notation(ind, coordinate, False, True)
                        else:
                            self._move_piece(ind)
                            return self._return_notation(ind, coordinate, False, False)
                else:  # illegal move = do nothing
                    pass
            else:  # move_from == move_to
                pass
            self._deselect_piece()
        else:  # no piece selected
            if self._piece_in_square_check(ind):  # square has piece
                if self._player_turn_check(ind):  # check for color turn
                    self._select_piece(ind)  # select piece
                else:
                    pass
            else:  # square == empty
                pass  # no selected piece and empty square = do nothing

    def _piece_in_square_check(self, ind):
        if self.piece_location[ind] is None:
            return False
        else:
            return True

    def _piece_selected_check(self):
        if self.selected_piece is None:
            return False
        else:
            return True

    def _select_piece(self, ind):
        self.selected_piece = self.piece_location[ind]
        self.move_from_ind = ind

    def _special_move_rules(self, move_from, move_to, x_and_y):
        if self.selected_piece.piece_notation == '':
            if x_and_y[0] == 0:
                if self.piece_location[move_to] is not None:
                    return False, None
                else:
                    if abs(x_and_y[1]) == 2:
                        if ((move_from - 1) % 8) == 0 or ((move_from - 6) % 8) == 0:
                            return True, None
                        else:
                            return False, None
                    else:
                        if (move_to % 8) == 0 or ((move_to - 7) % 8) == 0:
                            print('promotion')
                            return True, 'promotion'
                        else:
                            return True, None

            else:  # capture, check for en passant
                if self.piece_location[move_to] is not None:
                    return True, None
                else:
                    previous_move = self.game_state_stack[-1]
                    pre_x_and_y = self.convert_coord_change(previous_move[0], previous_move[1])
                    if abs(pre_x_and_y[1]) == 2 and self.piece_location[previous_move[1]].piece_notation == '' and abs(previous_move[1] - move_to) == 1:
                        return True, 'en passant'
                    else:
                        return False, None
        elif self.selected_piece.piece_notation == 'K':
            if abs(x_and_y[0]) == 2:
                print(x_and_y[0])
                print(move_from)
                if move_from == 32:
                    if x_and_y[0] == -2 and self.piece_location[0] is not None:
                        if self.piece_location[0].piece_notation == 'R':
                            return True, 'castle'
                        else:
                            return False, None
                    elif x_and_y[0] == 2 and self.piece_location[56] is not None:
                        if self.piece_location[56].piece_notation == 'R':
                            return True, 'castle'
                        else:
                            return False, None
                    else:
                        return False
                elif move_from == 39:
                    if x_and_y[0] == -2 and self.piece_location[7] is not None:
                        if self.piece_location[7].piece_notation == 'R':
                            return True, 'castle'
                        else:
                            return False, None
                    elif x_and_y[0] == 2 and self.piece_location[63] is not None:
                        if self.piece_location[63].piece_notation == 'R':
                            return True, 'castle'
                        else:
                            return False, None
                    else:
                        return False, None
                else:
                    return False, None
            else:
                return True, None
        else:
            pass

        return True, None

        # castle both sides
        # if self.selected_piece == king:
        # if at starting square can move 2, else cannot move 2
        # also check if a rook is at the starting square # need to add something that moves the rook, also the notation

    def _check_slide(self):
        # for i in range(x/y):  # larger of the 2, abs()
        # check if there is a piece in the square, if yes, return false: up until but not including the final square
        pass

    def _capture_piece(self, ind):
        self.capture_stack.append(self.piece_location[ind])  # add captured piece to stack

    def _player_turn_check(self, ind):
        move_number = len(self.game_state_stack)

        if move_number % 2 == 0:
            piece_color = 'w'
        else:
            piece_color = 'b'

        if piece_color == self.piece_location[ind].color:
            return True
        else:
            return False

    def _move_piece(self, ind):
        # change selected_piece's piece_location[index]
        # update button_image[index]
        # return notation

        self.buttons[ind].configure(image=self.selected_piece.image)
        self.buttons[ind].configure(text='')

        self.buttons[self.move_from_ind].configure(image=self.empty_image)

        if len(self.game_state_stack) > 0:
            self._reset_square_color(self.game_state_stack[-1][0],
                                     self.buttons[self.game_state_stack[-1][0]]
                                     )
            self._reset_square_color(self.game_state_stack[-1][1],
                                     self.buttons[self.game_state_stack[-1][1]]
                                     )

        self.buttons[self.move_from_ind].configure(fg_color=configurations.Highlight_color)
        self.buttons[ind].configure(fg_color=configurations.Highlight_color)

        self.piece_location[self.move_from_ind] = None

        self.piece_location[ind] = self.selected_piece

    def _castle(self, ind):
        if ind == 48:
            # move rook on 56 to 40
            rook = self.piece_location[56]
            self.piece_location[40] = rook
            self.buttons[40].configure(image=rook.image)
            self.buttons[56].configure(image=self.empty_image)
            self.piece_location[56] = None
        elif ind == 16:
            # move rook on 0 to 24
            rook = self.piece_location[0]
            self.piece_location[24] = rook
            self.buttons[24].configure(image=rook.image)
            self.buttons[0].configure(image=self.empty_image)
            self.piece_location[0] = None
        elif ind == 55:
            # move rook on 63 to 47
            rook = self.piece_location[63]
            self.piece_location[47] = rook
            self.buttons[47].configure(image=rook.image)
            self.buttons[63].configure(image=self.empty_image)
            self.piece_location[63] = None
        elif ind == 23:
            rook = self.piece_location[7]
            self.piece_location[31] = rook
            self.buttons[31].configure(image=rook.image)
            self.buttons[7].configure(image=self.empty_image)
            self.piece_location[7] = None
        else:
            pass

    def _en_passant(self):
        prev_move = self.game_state_stack[-1]
        self.capture_stack.append(prev_move[1])
        self.piece_location[prev_move[1]] = None
        self.buttons[prev_move[1]].configure(image=self.empty_image)

    def _promotion(self, ind):
        color = self.selected_piece.color
        new_piece = Queen(self, color)
        self.buttons[ind].configure(image=new_piece.image)

    def _return_notation(self, ind, coordinate, capture, special_move):

        if capture:  # capture notation
            if self.selected_piece.piece_notation == '':  # notation for captures by pawns
                column_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
                move_played = column_list[int(self.move_from_ind / 8)] + 'x' + str(coordinate)
            else:  # notation for captures by pieces
                move_played = str(self.selected_piece.piece_notation) + 'x' + str(coordinate)
        else:  # standard notation
            if special_move:  # castling
                if ind == 48 or ind == 55:  # squares of King-side castling
                    move_played = "O-O"
                else:
                    move_played = "O-O-O"
            else:
                move_played = str(self.selected_piece.piece_notation) + str(coordinate)

        stack_item = (self.move_from_ind, ind, capture, special_move)

        self.move_from_ind = None
        self.selected_piece = None
        self.move_list.append(move_played)
        self.view_count = len(self.move_list)
        self.game_state_stack.append(stack_item)  # take tuple indexes (from, to)

        print(str(move_played))
        return move_played, self.view_count  # return move information str(piece_notation + coord)

    def _deselect_piece(self):
        self.selected_piece = None

    def _follow_movement_rules(self, move_from_ind, move_to_ind):
        # convert index to x and y
        x_and_y = self.convert_coord_change(move_from_ind, move_to_ind)

        # check for legal_move
        movement = self._special_move_rules(move_from_ind, move_to_ind, x_and_y)
        if self.selected_piece.legal_move(x_and_y) and movement[0]:
            return True, movement[1]
        else:
            return False, None

        # check for special_move # TODO board checks if piece ==  king OR piece == pawn checking pawn and king position
        # check move_from_ind

        # TODO: create ability to castle O-O, O-O-O

        # TODO: create ability to play 'en passant'

        # TODO: add promotion ability

        # check for sliding_move

        pass

    # TODO: study mode: reset color after incorrect moves
    def _reset_square_color(self, coord, button):
        if (int((int(coord) / 8)) + (int(int(coord) % 8))) % 2 == 0:
            button.configure(self, fg_color=configurations.Light_green)
        else:
            button.configure(self, fg_color=configurations.Green)

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

        # self.game_state_stack.append(list(self.piece_location))

    # def game_state_append(self, state):  # necessary?
    #     self.game_state_stack.append(state)

    def game_state_pop(self, state):  # necessary?
        self.game_state_stack.pop(state)

    # add conditional for peruse move to pop captured piece
    def peruse_move(self, direction, index=int):
        recorded_move = self.game_state_stack[index]  # select tuple (from, to, capture_bool, special)
        from_square_image = self.empty_image
        from_square_piece = None
        if recorded_move[2]:  # capture=True
            if direction.value[0] == 0:  # if forward and capture=True, push piece onto stack
                self.capture_stack.append(self.piece_location[recorded_move[direction.value[1]]])
            else:  # if backward and capture=True, pop item off stack and place on board
                from_square_piece = self.capture_stack.pop()
                from_square_image = from_square_piece.image
        else:  # if capture=False, proceed
            pass

        #TODO: add castle and en passant logic


        self.buttons[recorded_move[direction.value[1]]].configure(
            image=self.piece_location[recorded_move[direction.value[0]]].image
        )
        self.piece_location[recorded_move[direction.value[1]]] = self.piece_location[recorded_move[direction.value[0]]]
        self.buttons[recorded_move[direction.value[0]]].configure(image=from_square_image)
        self.piece_location[recorded_move[direction.value[0]]] = from_square_piece

    def convert_coord_change(self, move_from, move_to):
        x = (int(int(move_to) / 8)) - (int(int(move_from) / 8))
        y = (int(move_to) % 8) - (int(move_from) % 8)
        return x, y


class King:
    def __init__(self, board, color):
        self.color = color
        if self.color == 'w':
            self.image = board.K_image
        elif self.color == 'b':
            self.image = board.k_image
        self.value = 1000
        self.piece_notation = 'K'

    def legal_move(self, x_and_y):
        x = x_and_y[0]
        y = x_and_y[1]
        if (abs(x) <= 1 and abs(y) <= 1) or (abs(x) == 2 and y == 0):
            return True
        else:
            return False


class Queen:
    def __init__(self, board, color):
        self.color = color
        if self.color == 'w':
            self.image = board.Q_image
        elif self.color == 'b':
            self.image = board.q_image
        self.value = 9
        self.piece_notation = 'Q'

    def legal_move(self, x_and_y):
        x = x_and_y[0]
        y = x_and_y[1]
        if abs(x) == 0 or abs(y) == 0:
            return True
        elif abs(x) == abs(y):
            return True
        else:
            return False


class Rook:
    def __init__(self, board, color):
        self.color = color
        if self.color == 'w':
            self.image = board.R_image
        elif self.color == 'b':
            self.image = board.r_image
        self.value = 5
        self.piece_notation = 'R'

    def legal_move(self, x_and_y):
        x = x_and_y[0]
        y = x_and_y[1]
        if abs(x) == 0 or abs(y) == 0:
            return True
        else:
            return False


class Bishop:
    def __init__(self, board, color):
        self.color = color
        if self.color == 'w':
            self.image = board.B_image
        elif self.color == 'b':
            self.image = board.b_image
        self.value = 3
        self.piece_notation = 'B'

    def legal_move(self, x_and_y):
        x = x_and_y[0]
        y = x_and_y[1]
        if abs(x) == abs(y):
            return True
        else:
            return False


class Knight:
    def __init__(self, board, color):
        self.color = color
        if self.color == 'w':
            self.image = board.N_image
        elif self.color == 'b':
            self.image = board.n_image
        self.value = 3
        self.piece_notation = 'N'

    def legal_move(self, x_and_y):
        x = x_and_y[0]
        y = x_and_y[1]
        if abs(x) != 0 and abs(y) + abs(x) == 3:
            return True
        else:
            return False


class Pawn:
    def __init__(self, board, color):
        self.color = color
        if self.color == 'w':
            self.image = board.P_image
        elif self.color == 'b':
            self.image = board.p_image
        self.value = 1
        self.piece_notation = ''

    def legal_move(self, x_and_y):
        x = x_and_y[0]
        y = x_and_y[1]
        if self.color == 'w':
            if -2 <= y < 0 == x:
                return True
            elif abs(x) == 1 and y == -1:
                return True
            else:
                return False

        if self.color == 'b':
            if 2 >= y > 0 and x == 0:
                return True
            elif abs(x) == 1 and y == 1:
                return True
            else:
                return False


if __name__ == '__main__':
    my_controller = ''

    root = customtkinter.CTk()
    my_frame = customtkinter.CTkFrame(root)
    my_frame.pack()

    chessBoard = ChessBoard(view=root, controller=my_controller, frame=my_frame)
    chessBoard.create_everything()
    root.mainloop()
