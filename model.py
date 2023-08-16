# takes care of the information requests and the logic
import db_manager

db_connection = db_manager.DbConnection


class Model:

    def __init__(self):
        self.active_user = ''
        self.user_id = ''
        self.active_opening_name = ''
        self.active_opening_moves = ''
        self.users_openings = []
        # self.current_move = 0
        self.active_moves_only = []
        self.active_game_stack = []
        self.active_capture_stack = []

        self.lboard_list = []

    def login(self, username, password):
        check = db_connection.check_login_details(self, username, password)  # returns a list of tuples

        if check[0][0] == 1:  # check if that username/password combo exists
            self.set_active_user(username)

            self.user_id = self.get_user_id(self.active_user)
            print(username + " logged in")
            #  also delete the text boxes
            return True

        else:
            print("Invalid login")
            return False

        # def create_account(self, new_username, new_password):
        #     pass

    def set_active_user(self, username):
        self.active_user = username

    def set_active_opening(self, opening_name, move_list):
        self.active_opening_name = opening_name
        self.active_opening_moves = move_list

    def get_user_id(self, username):
        query = (db_connection.get_user_id(self, username))
        user_id = query[0]
        print("get_user_id: " + str(user_id))
        return user_id

    def get_user_openings(self, id_number):
        query = db_connection.query_db_openings(self, id_number)
        return query

    def create_db_entry(self, user_number, name_of_opening, list_of_moves, game_stack, capture_stack):
        print("called: create_db_entry")
        new_entry = [user_number, name_of_opening,
                     list_of_moves, game_stack, capture_stack]  # entry = [user_number, name_of_opening, list_of_moves, game_stack, capture_stack]
        db_connection.create_new_entry(self, new_entry)

    def edit_db_entry(self, opening_name, list_of_moves, game_stack, capture_stack):
        print("called: edit_db_entry")
        db_connection.edit_db_entry(self, opening_name, list_of_moves, game_stack, capture_stack)

    def delete_db_entry(self, opening_name):
        print("called: delete_db_entry")
        db_connection.delete_db_entry(self, opening_name)

    def admin_query_full_database(self, table):
        data = db_connection.query_everything(self, table)
        return data

    def admin_delete_db_entry(self, table, oid):
        db_connection.delete_anything(self, table, oid)

    def format_move_list(self, move_string):
        temp_list = move_string.split()
        n = 3  # used to remove every 3rd item of the list, the numbers of the move list
        del temp_list[::n]  # remove the move numbers
        move_only_list = temp_list

        return move_only_list

    def lboard_list_append(self, item):
        self.lboard_list.append(item)

    def lboard_list_sort(self, rating_type):
        # rating_type = 1, 2, or 3 : bullet, blitz, rapid
        for i in range(len(self.lboard_list)-1, 0, -1):
            for j in range(i):
                if self.lboard_list[j][rating_type] < self.lboard_list[j+1][rating_type]:
                    temp = self.lboard_list[j]
                    self.lboard_list[j] = self.lboard_list[j+1]
                    self.lboard_list[j+1] = temp

    def lboard_list_clear(self):
        self.lboard_list.clear()
