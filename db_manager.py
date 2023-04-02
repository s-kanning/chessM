import sqlite3


# # connect to db (or create)
# conn = sqlite3.connect('chess_database.db')
#
# # create a cursor
# c = conn.cursor()

# create tables
# c.execute("""CREATE TABLE users (
#         username text,
#         password text
#     )""")

# c.execute("""CREATE TABLE openings (
#         user_id integer,
#         opening_name text,
#         move_list text
#      )""")

# example entry
# user_number = 2
# name_of_opening = "Evans Gambit"
# list_of_moves = "1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. b4 Bxb4 5. c3"
# entry = [user_number, name_of_opening, list_of_moves]

# c.execute('''
# UPDATE users
# SET username = :u1,
#     password = :p1
# WHERE
#     oid = 2
# ''',
#           {'u1': 'u2',
#            'p1': 'p2'}
#           )
# conn.commit()

# # c.execute("INSERT INTO openings VALUES (?,?,?)", entry)
# print("executed")
# # c.executemany("INSERT INTO users VALUES (?,?)", #list_var)
#
# # query the database
# c.execute("SELECT * FROM users")
# # # c.fetchone() # returns first
# # # c.fetchmany(3)
# data = c.fetchall()
#
# # #print("Username : Password")
# for item in data:
#     #print(item[0] + " : " + item[1])
#     print(item)
#
# # commit our command
# conn.commit()
# # close connection
# conn.close()


class DbConnection:
    my_conn = ''
    my_c = ''

    def query_db_move_list(self):
        self.my_conn = sqlite3.connect('chess_database.db')
        self.my_c = self.my_conn.cursor()
        self.my_c.execute("SELECT opening_name,move_list FROM openings")  # need to add WHERE user_id = ???
        data = self.my_c.fetchall()
        self.my_conn.commit()
        self.my_conn.close()
        return data

    def create_new_entry(self, entry):  # entry = [user_number, name_of_opening, list_of_moves]
        self.my_conn = sqlite3.connect('chess_database.db')
        self.my_c = self.my_conn.cursor()
        self.my_c.execute("INSERT INTO openings VALUES (?,?,?)", entry)
        self.my_conn.commit()
        self.my_conn.close()

    def edit_db_entry(self, opening_name, move_list):
        self.my_conn = sqlite3.connect('chess_database.db')
        self.my_c = self.my_conn.cursor()
        self.my_c.execute('''UPDATE openings SET
        opening_name = :opening_name,
        move_list = :move_list

        WHERE
        opening_name = :opening_name''',
                          {
                              'opening_name': opening_name,
                              'move_list': move_list
                          }
                          )
        self.my_conn.commit()
        self.my_conn.close()

    def delete_db_entry(self, opening_name):
        self.my_conn = sqlite3.connect('chess_database.db')
        self.my_c = self.my_conn.cursor()
        self.my_c.execute("DELETE from openings WHERE opening_name = (?)", (opening_name,))
        self.my_conn.commit()
        self.my_conn.close()

    def query_db_openings(self, user_id):
        self.my_conn = sqlite3.connect('chess_database.db')
        self.my_c = self.my_conn.cursor()
        self.my_c.execute("SELECT opening_name,move_list FROM openings WHERE user_id = (?)",
                          (user_id,)
                          )
        openings = self.my_c.fetchall()
        self.my_conn.commit()
        self.my_conn.close()
        return openings

    def get_user_id(self, username):
        self.my_conn = sqlite3.connect('chess_database.db')
        self.my_c = self.my_conn.cursor()
        self.my_c.execute("SELECT oid FROM users WHERE username = (?)", (username,))
        user_id = self.my_c.fetchone()
        self.my_conn.commit()
        self.my_conn.close()
        return user_id

    def check_login_details(self, username, password):
        self.my_conn = sqlite3.connect('chess_database.db')
        self.my_c = self.my_conn.cursor()
        self.my_c.execute("SELECT EXISTS(SELECT oid FROM users WHERE username = ? AND password = ?)",
                          (username, password)
                          )
        user_id = self.my_c.fetchall()
        print(str(user_id))
        self.my_conn.commit()
        self.my_conn.close()
        return user_id

    def print_users_table(self):
        self.my_conn = sqlite3.connect('chess_database.db')
        self.my_c = self.my_conn.cursor()
        self.my_c.execute("SELECT * FROM openings")
        data = self.my_c.fetchall()
        self.my_conn.commit()
        self.my_conn.close()
        return data

    def query_everything(self, table):
        self.my_conn = sqlite3.connect('chess_database.db')
        self.my_c = self.my_conn.cursor()
        if table == 'openings':
            self.my_c.execute("SELECT *,oid FROM openings")
            openings = self.my_c.fetchall()
            return openings
        elif table == 'users':
            self.my_c.execute("SELECT *,oid FROM users")
            users = self.my_c.fetchall()
            return users
        self.my_conn.commit()
        self.my_conn.close()

    def delete_anything(self, table, oid):
        self.my_conn = sqlite3.connect('chess_database.db')
        self.my_c = self.my_conn.cursor()
        if table == 'openings':
            self.my_c.execute("DELETE from openings WHERE oid = ?", (oid,))
        elif table == 'users':
            self.my_c.execute("DELETE from users WHERE oid = ?", (oid,))
        self.my_conn.commit()
        self.my_conn.close()
