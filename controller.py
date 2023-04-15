# acts as an intermediary between the model and the view
from view import View
from model import Model
from chess_board import ChessBoard
from enum import Enum, auto


class ChessMode(Enum):
    PLAY = auto()
    STUDY = auto()
    CREATE = auto()
    INACTIVE = auto()


class Direction(Enum):
    FORWARD = (0, 1)
    BACKWARD = (1, 0)


class Controller:

    def __init__(self):
        self.model = Model()
        self.view = View(self)

        self.play_board = ChessBoard(view=self.view, controller=self, frame=self.view.play_board_frame)
        self.play_board.create_everything()
        self.study_board = ChessBoard(view=self.view, controller=self, frame=self.view.board_frame)
        self.study_board.create_everything()
        self.selector_board = ChessBoard(view=self.view, controller=self, frame=self.view.selecting_frame)
        self.selector_board.create_everything()
        self.editor_board = ChessBoard(view=self.view, controller=self, frame=self.view.editor_board_frame)
        self.editor_board.create_everything()

        self.app_mode = ChessMode.PLAY  # create enum 'modes' to determine active mode and thus board behavior

    def main(self):
        self.view.main()

    def on_button_click(self, button):
        # print(f"button clicked: {button}")
        if button == 'login':
            username = self.view.username_entry.get()
            password = self.view.password_entry.get()
            if self.model.login(username, password):
                self.view.show_frame(self.view.MainPage)
                pass
            else:
                pass

        if button == 'selector':
            self.app_mode = ChessMode.INACTIVE
            data = self.model.get_user_openings(self.model.user_id)  # get list of user openings
            #  print(data)
            temp_list = []
            for item in data:
                temp_list.append(item[0])

            self.view.select_menu.configure(values=temp_list)
            # populate the selector_menu with the opening names, the first item of each tuple in the openings list

            self.view.show_main_container_frame(self.view.selector_frame)

        if button == 'selector_menu':  # useless? the menu uses the button name, not this name
            info = self.view.select_menu.get()
            print("this is the info: " + info)

            # take an opening and populate the opening page, get ready to pass information to 'study' button

        if button == 'study':
            self.app_mode = ChessMode.STUDY
            self.view.show_main_container_frame(self.view.study_frame)

            opening = self.view.selector_opening_string_var.get()
            self.view.study_opening_name.set(opening)
            self.model.active_opening_name = opening

            data = self.model.get_user_openings(self.model.user_id)

            active_opening_moves = ''
            for item in data:
                if item[0] == opening:
                    active_opening_moves = item[1]
                    self.model.active_game_stack = item[2]
                    self.model.active_capture_stack = item[3]
            self.model.active_opening_moves = active_opening_moves
            print("model active opening name: " + self.model.active_opening_name)
            print("model active opening moves: " + self.model.active_opening_moves)
            print("active game stack" + self.model.active_game_stack)
            print("active capture stack" + self.model.active_capture_stack)

            self.model.active_moves_only = self.model.format_move_list(self.model.active_opening_moves)
            # self.model.current_move = 0
            print("active moves only: ")
            print(self.model.active_moves_only)

        if button == 'database':
            self.view.show_main_container_frame(self.view.database_frame)

        if button == 'play':
            self.view.show_main_container_frame(self.view.play_frame)
            self.app_mode = ChessMode.PLAY

        if button == 'logout':
            self.view.show_frame(self.view.LoginPage)
            self.model.user_id = ''
            self.model.active_user = ''
            #  add some kind of reset function to clear everything and reset the values of each page/label etc.

        if button == 'main_page':
            self.view.show_frame(self.view.MainPage)

        if button == 'edit_opening':
            self.app_mode = ChessMode.CREATE
            self.view.show_main_container_frame(self.view.editor_frame)
            opening = self.view.selector_opening_string_var.get()

            # set the title to the opening's name
            self.view.editor_name_textbox.delete("0.0", "end")
            self.view.editor_name_textbox.insert("0.0", opening)

            data = self.model.get_user_openings(self.model.user_id)

            editor_opening_moves = ''
            for item in data:
                if item[0] == opening:
                    editor_opening_moves = item[1]

            #  set the move list in the text box
            self.view.editor_move_list_textbox.delete("0.0", "end")
            self.view.editor_move_list_textbox.insert("0.0", editor_opening_moves)

        if button == 'create':
            self.app_mode = ChessMode.CREATE
            self.view.show_main_container_frame(self.view.editor_frame)

        if button == 'save_changes':  # button found on create/edit frame
            data = self.model.get_user_openings(self.model.user_id)  # get list of user openings
            #  print(data)
            temp_list = []
            for item in data:
                temp_list.append(item[0])
            new_entry_name = self.view.editor_name_textbox.get("1.0", 'end-1c')

            if new_entry_name in temp_list:  # if opening name already exists in database, give warning message and ask if user wants to update, otherwise create new entry
                opening_name = self.view.editor_name_textbox.get("1.0", 'end-1c'
                                                                 )  # "1.0",'end-1c' is necessary to remove the last character, otherwise a new line is added,
                print("Updated entry: " + opening_name)

                move_list = self.view.editor_move_list_textbox.get("1.0", 'end-1c')
                game_stack = str(self.editor_board.game_state_stack)
                capture_stack = str(self.editor_board.capture_stack)
                self.model.edit_db_entry(opening_name, move_list, game_stack, capture_stack)
            else:
                opening_name = self.view.editor_name_textbox.get("1.0", 'end-1c')
                move_list = self.view.editor_move_list_textbox.get("1.0", 'end-1c')
                game_stack = str(self.editor_board.game_state_stack)
                capture_stack = str(self.editor_board.capture_stack)
                self.model.create_db_entry(self.model.user_id, opening_name, move_list, game_stack, capture_stack)
                print("Created new entry: " + opening_name)

        if button == 'delete':  # button found on create/edit frame
            print("delete entry from database")
            opening_name = self.view.editor_name_textbox.get("0.0", "end")
            self.model.delete_db_entry(opening_name)

        # TODO: call function for correct/incorrect answers, update board to play next move -> priority1
        if button == 'submit':  # check user input against move list
            if self.view.move_entry.get() == self.model.active_moves_only[self.study_board.view_count - 1]:  # -1 for 0 indexing
                print("correct")
                player_move = self.view.move_entry.get(), self.study_board.half_move_count
                self.update_move_list_textbox(player_move)
                self.view.move_entry.delete('0', 'end')
            else:
                print("incorrect")
                self.view.move_entry.delete('0', 'end')
                # self.study_board.peruse_move(Direction.BACKWARD, (len(self.study_board.game_state_stack)-1))  # replaced game_stack with tuple list
                # self.study_board.game_state_pop(-1)

        if button == 'backwards':  # decrease board.move_view_count, update chessboard
            if self.app_mode == ChessMode.PLAY:
                if self.play_board.view_count - 1 >= 0:
                    self.play_board.view_count -= 1
                    self.play_board.peruse_move(Direction.BACKWARD, self.play_board.view_count)
                else:
                    pass   # peruse_move(self, direction, index=int)

            elif self.app_mode == ChessMode.STUDY:
                if self.study_board.view_count - 1 >= 0:
                    self.study_board.view_count -= 1
                    self.study_board.peruse_move(Direction.BACKWARD, self.study_board.view_count)
                    print(self.study_board.view_count)
                else:
                    pass
            elif self.app_mode == ChessMode.CREATE:
                if self.editor_board.view_count - 1 >= 0:
                    self.editor_board.view_count -= 1
                    self.editor_board.peruse_move(Direction.BACKWARD, self.editor_board.view_count)
                else:
                    pass
            elif self.app_mode == ChessMode.INACTIVE:
                pass
            else:
                pass

        if button == 'forwards':  # increase board.move_view_count, update chessboard
            if self.app_mode == ChessMode.PLAY:
                if self.play_board.view_count + 1 <= len(self.play_board.game_state_stack):
                    self.play_board.peruse_move(Direction.FORWARD, self.play_board.view_count)
                    self.play_board.view_count += 1
                else:
                    pass

            elif self.app_mode == ChessMode.STUDY:
                if self.study_board.view_count + 1 <= len(self.study_board.game_state_stack):
                    self.study_board.peruse_move(Direction.FORWARD, self.study_board.view_count)
                    self.study_board.view_count += 1
                else:
                    pass
            elif self.app_mode == ChessMode.CREATE:
                if self.editor_board.view_count + 1 <= len(self.editor_board.game_state_stack):
                    self.editor_board.peruse_move(Direction.FORWARD, self.editor_board.view_count)
                    self.editor_board.view_count += 1
                else:
                    pass
            elif self.app_mode == ChessMode.INACTIVE:
                pass
            else:
                pass

        if button == 'reset':  # call the reset function
            self.reset_board_and_textbox()

        if button == 'update_database_entry':
            pass

        if button == 'delete_database_entry':
            table = self.view.table_selector.get()
            oid = self.view.oid_entry_box.get()
            self.model.admin_delete_db_entry(table, oid)

        if button == 'query_database_entry':
            table = self.view.table_selector.get()

            info = self.model.admin_query_full_database(table)
            self.view.database_textbox.delete("0.0", "end")

            for item in info:
                self.view.database_textbox.insert("end", str(item) + "\n")

        # if button == 'game_board':
        #     print("game_board: click")
        #     pass

    def other_button_clicks(self, button):
        print(f"other button clicks: {button}")
        self.view.selector_opening_string_var.set(button)

    def game_board_click(self, board, button):
        if board.view_count != board.half_move_count:
            pass
        else:
            if self.app_mode is ChessMode.INACTIVE:
                pass
            else:
                player_move = board.play_move(button)

                if player_move is not None:
                    if self.app_mode == ChessMode.PLAY:
                        self.update_move_list_textbox(player_move)
                    elif self.app_mode == ChessMode.STUDY:
                        self.view.move_entry.delete('0', 'end')
                        self.view.move_entry.insert('0', str(player_move[0]))
                    elif self.app_mode == ChessMode.CREATE:
                        self.update_move_list_textbox(player_move)
                        pass

    def update_move_list_textbox(self, player_move):
        if self.app_mode == ChessMode.PLAY:
            self.view.update_play_move_list(player_move[0], player_move[1])

        elif self.app_mode == ChessMode.STUDY:
            self.view.update_study_move_list(player_move[0], player_move[1])

        elif self.app_mode == ChessMode.CREATE:
            self.view.update_create_move_list(player_move[0], player_move[1])

        elif self.app_mode == ChessMode.INACTIVE:
            pass

    def reset_board_and_textbox(self):
        if self.app_mode == ChessMode.PLAY:
            self.view.clear_play_move_list()
            self.play_board.reset_board()

        elif self.app_mode == ChessMode.STUDY:
            self.view.clear_study_move_list()
            self.study_board.reset_board()
            self.view.move_entry.delete('0', 'end')

        elif self.app_mode == ChessMode.CREATE:
            self.view.clear_create_move_list()
            self.editor_board.reset_board()

        elif self.app_mode == ChessMode.INACTIVE:
            pass


if __name__ == '__main__':
    chessApp = Controller()
    chessApp.main()
