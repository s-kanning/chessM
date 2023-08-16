# takes care of the visuals
import tkinter
import customtkinter
from configurations import *

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


# Thoughts for later, reduce login screen, save stuff to minimize work for user
# Reduce size of buttons on the side, main thing to be clicked is board
# make size scalable

class View(customtkinter.CTk):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("ChessM")
        self.iconbitmap(r"C:\Users\sdkan\PycharmProjects\chessMem\images\ChessM icon zoom.ico")
        self.geometry(f"{1240}x{860}")

        # TODO: make scalable

        # self.minsize(width=1240, height=900)
        # self.maxsize(width=1240, height=900)

        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self._make_container_frame()

    def main(self):
        self.mainloop()

    def _make_container_frame(self):
        self.container = customtkinter.CTkFrame(self, border_width=10, corner_radius=0, border_color=Light_green,
                                                bg_color=Light_green
                                                )
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self._make_login_page()
        self.LoginPage.grid(row=0, column=0, rowspan=2, columnspan=4, sticky="NSEW")

        self._make_main_page()
        self._populate_study_frame()
        self._populate_selector_frame()
        self._populate_editor_frame()
        self._populate_database_frame()
        self._populate_play_frame()
        self._populate_lboard_frame()

        self._make_button_panel(self.main_page_display)
        self.MainPage.grid(row=0, column=0, rowspan=2, columnspan=4, sticky="NSEW")

        # self._make_settings_page()
        # self.SettingsPage.grid(row=0, column=0, rowspan=2, columnspan=4, sticky="NSEW")

        # initializing frames to an empty array
        self.frames = {}
        self.frames[self.LoginPage] = self.LoginPage
        self.frames[self.MainPage] = self.MainPage
        # self.frames[self.SettingsPage] = self.SettingsPage  # delete this

        # for F in (self.LoginPage,):
        #     frame = F(self.container, self)
        #     self.frames[F] = frame
        #
        #     frame.grid(row=0, column=0, rowspan=2, columnspan=4, sticky="NSEW")

        self.show_frame(self.LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def show_main_container_frame(self, cont):
        frame = self.display_frames[cont]
        frame.tkraise()

    def _make_login_page(self):
        self.LoginPage = customtkinter.CTkFrame(self.container, border_width=20, corner_radius=0,
                                                border_color=Light_green,
                                                fg_color=Blue_green
                                                )
        login_page_display = customtkinter.CTkFrame(self.LoginPage, corner_radius=40, height=1100, width=580,
                                                    fg_color=Green,
                                                    border_width=10,
                                                    border_color=Light_green
                                                    )
        login_page_display.pack(pady=40, padx=40, side="top", expand=True)

        login_label = customtkinter.CTkLabel(login_page_display, text_color=Light_green,
                                             text="ChessM",
                                             font=(Font, 60)
                                             )
        login_label.grid(row=1, column=0, columnspan=1, padx=20, pady=20, ipadx=40, ipady=40)

        self.username_entry = customtkinter.CTkEntry(login_page_display, corner_radius=100, height=40,
                                                     width=240,
                                                     text_color=Blue_green, placeholder_text="Username",
                                                     font=(Font, 20)
                                                     )
        self.username_entry.grid(row=2, column=0, padx=0, pady=20)

        self.password_entry = customtkinter.CTkEntry(login_page_display, corner_radius=100, height=40,
                                                     width=240,
                                                     show="*",
                                                     text_color=Blue_green,
                                                     placeholder_text="Password", font=(Font, 20)
                                                     )
        self.password_entry.grid(row=3, column=0, padx=0, pady=0)

        login_button = customtkinter.CTkButton(login_page_display, corner_radius=100, text="Login",
                                               font=(Font, 20),
                                               command=lambda button="login": self.controller.on_button_click(button)
                                               )
        login_button.grid(row=4, column=0, columnspan=1, padx=140, pady=50)

    def _make_main_page(self):
        self.MainPage = customtkinter.CTkFrame(self.container, border_width=20, corner_radius=0,
                                               border_color=Light_green,
                                               fg_color=Blue_green
                                               )
        self.main_page_display = customtkinter.CTkFrame(self.MainPage, border_width=0, fg_color=Blue_green)
        self.main_page_display.pack(side="top", expand=True)
        self.main_page_display.grid_rowconfigure(4, weight=1)
        self.main_page_display.grid_columnconfigure(4, weight=1)

        container_frame = customtkinter.CTkFrame(self.main_page_display, border_color=Blue_green, border_width=10)
        container_frame.grid(row=0, column=1, columnspan=4, rowspan=5, sticky="NSEW")
        container_frame.grid_rowconfigure(0, weight=1)
        container_frame.grid_rowconfigure(0, weight=1)

        self.lboard_frame = customtkinter.CTkFrame(container_frame, corner_radius=20, border_width=10,
                                                   bg_color=Blue_green,
                                                   fg_color=Blue_green, border_color=Light_green
                                                   )
        self.database_frame = customtkinter.CTkFrame(container_frame, corner_radius=20, border_width=10,
                                                     bg_color=Blue_green,
                                                     fg_color=Blue_green, border_color=Light_green
                                                     )
        self.selector_frame = customtkinter.CTkFrame(container_frame, corner_radius=20, border_width=10,
                                                     bg_color=Blue_green,
                                                     fg_color=Blue_green, border_color=Light_green
                                                     )
        self.editor_frame = customtkinter.CTkFrame(container_frame, corner_radius=20, border_width=10,
                                                   bg_color=Blue_green,
                                                   fg_color=Blue_green, border_color=Light_green
                                                   )
        self.study_frame = customtkinter.CTkFrame(container_frame, corner_radius=20, border_width=10,
                                                  bg_color=Blue_green,
                                                  fg_color=Blue_green, border_color=Light_green
                                                  )
        self.play_frame = customtkinter.CTkFrame(container_frame, corner_radius=20, border_width=10,
                                                 bg_color=Blue_green,
                                                 fg_color=Blue_green, border_color=Light_green
                                                 )

        self.play_frame.grid(row=0, column=0, sticky='nswe', pady=10, padx=10, ipadx=20)
        self.study_frame.grid(row=0, column=0, sticky='nswe', pady=10, padx=10, ipadx=20)
        self.database_frame.grid(row=0, column=0, sticky='nswe', pady=10, padx=10, ipadx=20)
        self.selector_frame.grid(row=0, column=0, sticky='nswe', pady=10, padx=10, ipadx=20)
        self.editor_frame.grid(row=0, column=0, sticky='nswe', pady=10, padx=10, ipadx=20)
        self.lboard_frame.grid(row=0, column=0, sticky='nswe', pady=10, padx=10, ipadx=20)

        self.display_frames = {}

        self.display_frames[self.lboard_frame] = self.lboard_frame
        self.display_frames[self.database_frame] = self.database_frame
        self.display_frames[self.selector_frame] = self.selector_frame
        self.display_frames[self.editor_frame] = self.editor_frame
        self.display_frames[self.study_frame] = self.study_frame
        self.display_frames[self.play_frame] = self.play_frame

    def _populate_study_frame(self):
        self.study_opening_name = tkinter.StringVar(self.study_frame, "Study"
                                                    )  # use a string variable to easily update the opening name?
        opening_name_label = customtkinter.CTkLabel(self.study_frame, textvariable=self.study_opening_name,
                                                    text_color=Light_green,
                                                    font=(Font, 40),
                                                    bg_color=Blue_green
                                                    )
        opening_name_label.grid(row=0, column=0, columnspan=2, padx=0, pady=(40, 20))

        self.study_move_list_textbox = customtkinter.CTkTextbox(self.study_frame, height=460, width=200,
                                                                corner_radius=20,
                                                                text_color=Blue_green,
                                                                font=(Font, 20)
                                                                )
        self.study_move_list_textbox.grid(row=1, column=3, rowspan=4, pady=(0, 140), padx=0, sticky="n")
        self.study_move_list_textbox.insert("0.0", "Move list: ")
        self.study_move_list_textbox.configure(state="disabled")

        self.backward_button = customtkinter.CTkButton(self.study_frame, width=98, corner_radius=20, text="<<",
                                                       font=(Font, 20), command=lambda
                my_button="backwards": self.controller.on_button_click(my_button)  # deleted disabled
                                                       )
        self.backward_button.grid(row=4, column=3, padx=0, pady=(60, 0), sticky='nw')

        self.forward_button = customtkinter.CTkButton(self.study_frame, width=98, corner_radius=20, text=">>",
                                                      font=(Font, 20), command=lambda
                my_button="forwards": self.controller.on_button_click(my_button)
                                                      )
        self.forward_button.grid(row=4, column=3, padx=0, pady=(60, 0), sticky='ne')
        # forward and backward buttons should only affect the view_count,
        # but only up to the amount of (current move), submit button resets this amount

        self.move_entry = customtkinter.CTkEntry(self.study_frame, height=30, width=200, corner_radius=20,
                                                 placeholder_text="Enter a move",
                                                 font=(Font, 20)
                                                 )
        self.move_entry.grid(row=4, column=3, padx=0, pady=(0, 0), sticky='ew')

        self.study_board_frame = customtkinter.CTkFrame(self.study_frame, height=640, width=640, corner_radius=0)
        self.study_board_frame.grid(row=1, rowspan=4, columnspan=2, padx=40, pady=(0, 40), sticky="EW")

        self.reset_button = customtkinter.CTkButton(self.study_frame, width=200, corner_radius=20,
                                                    text="Reset",
                                                    font=(Font, 20), command=lambda
                my_button="reset": self.controller.on_button_click(my_button)
                                                    )
        self.reset_button.grid(row=4, column=3, padx=0, pady=(0, 40), sticky='s')

    def _populate_play_frame(self):
        opening_name_label = customtkinter.CTkLabel(self.play_frame, text="",
                                                    text_color=Light_green,
                                                    font=(Font, 40),
                                                    bg_color=Blue_green
                                                    )
        opening_name_label.grid(row=0, column=0, columnspan=2, padx=0, pady=(40, 20))

        self.play_move_list_textbox = customtkinter.CTkTextbox(self.play_frame, height=460, width=200,
                                                               corner_radius=20,
                                                               text_color=Blue_green,
                                                               font=(Font, 20)
                                                               )
        self.play_move_list_textbox.grid(row=1, column=3, rowspan=4, pady=(0, 140), padx=0, sticky="n")
        self.play_move_list_textbox.insert("0.0", "Move list: ")
        self.play_move_list_textbox.configure(state="disabled")

        self.play_backward_button = customtkinter.CTkButton(self.play_frame, width=98, corner_radius=20, text="<<",
                                                            font=(Font, 20), command=lambda
                my_button="backwards": self.controller.on_button_click(my_button)
                                                            )
        self.play_backward_button.grid(row=4, column=3, padx=0, pady=(60, 0), sticky='nw')

        self.play_forward_button = customtkinter.CTkButton(self.play_frame, width=98, corner_radius=20, text=">>",
                                                           font=(Font, 20), command=lambda
                my_button="forwards": self.controller.on_button_click(my_button)
                                                           )
        self.play_forward_button.grid(row=4, column=3, padx=0, pady=(60, 0), sticky='ne')

        self.play_board_frame = customtkinter.CTkFrame(self.play_frame, height=640, width=640, corner_radius=0)
        self.play_board_frame.grid(row=1, rowspan=4, columnspan=2, padx=40, pady=(0, 40), sticky="EW")

        self.play_reset_button = customtkinter.CTkButton(self.play_frame, width=200, corner_radius=20,
                                                         text="Reset",
                                                         font=(Font, 20), command=lambda
                my_button="reset": self.controller.on_button_click(my_button)
                                                         )
        self.play_reset_button.grid(row=4, column=3, padx=0, pady=(0, 40), sticky='s')

    # TODO make this a Profile/Settings page with options to change things, username, password,visuals, look at all entries
    def _populate_database_frame(self):
        # make a frame
        database_frame = customtkinter.CTkFrame(self.database_frame, width=600, height=600, corner_radius=0,
                                                fg_color=Blue_green
                                                )
        database_frame.pack(pady=40, padx=40, side="top", expand=True)

        # make a query button
        query_button = customtkinter.CTkButton(database_frame, width=200, corner_radius=20,
                                               text="Query Database Entry",
                                               font=(Font, 20),
                                               command=lambda
                                                   button="query_database_entry": self.controller.on_button_click(
                                                   button
                                               )
                                               )
        query_button.grid(row=1, column=2, padx=0, pady=20)

        # make a text box
        self.database_textbox = customtkinter.CTkTextbox(database_frame, height=400, width=800,
                                                         corner_radius=20,
                                                         text_color=Blue_green,
                                                         font=(Font, 20)
                                                         )
        self.database_textbox.grid(row=2, column=1, columnspan=3)
        self.database_textbox.insert("0.0", "data")

        # make some entry boxes
        self.table_selector = customtkinter.CTkOptionMenu(database_frame, corner_radius=100, height=40,
                                                          width=240, values=["openings", "users"], fg_color='white',
                                                          text_color=Blue_green, anchor='w',
                                                          font=(Font, 20)
                                                          )
        self.table_selector.grid(row=1, column=1, padx=0, pady=20)
        self.table_selector.set("table")

        self.oid_entry_box = customtkinter.CTkEntry(database_frame, corner_radius=100, height=40,
                                                    width=240,
                                                    text_color=Blue_green, placeholder_text="oid",
                                                    font=(Font, 20)
                                                    )
        self.oid_entry_box.grid(row=4, column=1, padx=0, pady=20)

        # make a button to edit
        update_button = customtkinter.CTkButton(database_frame, width=200, corner_radius=20,
                                                text="Update Database Entry",
                                                font=(Font, 20),
                                                command=lambda
                                                    button="update_database_entry": self.controller.on_button_click(
                                                    button
                                                )
                                                )
        update_button.grid(row=3, column=2, padx=0, pady=20)

        # make a delete button
        delete_button = customtkinter.CTkButton(database_frame, width=200, corner_radius=20,
                                                text="Delete Database Entry",
                                                font=(Font, 20),
                                                command=lambda
                                                    button="delete_database_entry": self.controller.on_button_click(
                                                    button
                                                )
                                                )
        delete_button.grid(row=4, column=2, padx=0, pady=0)

    def _populate_selector_frame(self):
        select_label = customtkinter.CTkLabel(self.selector_frame, text="Select an opening:",
                                              text_color=Light_green, font=(Font, 40)
                                              )
        select_label.grid(row=0, column=0, padx=40, pady=(40, 20), sticky='w')

        self.selecting_frame = customtkinter.CTkFrame(self.selector_frame, height=600, width=600, corner_radius=0)
        self.selecting_frame.grid(row=1, rowspan=3, columnspan=2, padx=40, pady=0, sticky="EW")

        self.select_menu = customtkinter.CTkOptionMenu(self.selector_frame, width=200, dynamic_resizing=False,
                                                       values=["opening1", "opening2"], command=lambda
                my_button="selector_menu": self.controller.other_button_clicks(my_button)
                                                       )
        self.select_menu.grid(row=0, column=1, columnspan=2, pady=(40, 20), padx=40, sticky='w')
        self.select_menu.set("Select")

        self.selector_opening_string_var = customtkinter.StringVar(self.selector_frame, "Opening Name")

        select_name_label = customtkinter.CTkLabel(self.selector_frame, height=40, width=200,
                                                   corner_radius=20,
                                                   textvariable=self.selector_opening_string_var,
                                                   text_color=Light_green,
                                                   font=(Font, 20)
                                                   )
        select_name_label.grid(row=0, column=3, pady=(30, 20), padx=0)

        selection_move_textbox = customtkinter.CTkTextbox(self.selector_frame, height=450, width=200,
                                                          corner_radius=20,
                                                          text_color=Blue_green,
                                                          font=(Font, 20),
                                                          state="disabled"
                                                          )
        selection_move_textbox.grid(row=1, column=3, rowspan=4, pady=(0, 10), padx=0, sticky="n")
        selection_move_textbox.insert("0.0", "Move list:")

        study_button = customtkinter.CTkButton(self.selector_frame, width=200, corner_radius=20,
                                               text="Study opening",
                                               font=(Font, 20),
                                               command=lambda button="study": self.controller.on_button_click(button)
                                               )
        study_button.grid(row=3, column=3, padx=0, pady=0)
        edit_opening_button = customtkinter.CTkButton(self.selector_frame, width=200, corner_radius=20,
                                                      text="Edit opening",
                                                      font=(Font, 20), command=lambda
                button="edit_opening": self.controller.on_button_click(button)
                                                      )
        edit_opening_button.grid(row=3, column=3, padx=0, pady=0, sticky='S')

    def _populate_editor_frame(self):
        editor_label = customtkinter.CTkLabel(self.editor_frame, text="Editor",
                                              text_color=Light_green, font=(Font, 40)
                                              )
        editor_label.grid(row=0, column=0, padx=40, pady=(40, 20), sticky='w')

        self.editor_board_frame = customtkinter.CTkFrame(self.editor_frame, height=600, width=600, corner_radius=0)
        self.editor_board_frame.grid(row=1, rowspan=3, columnspan=2, padx=40, pady=0, sticky="EW")

        self.editor_name_textbox = customtkinter.CTkTextbox(self.editor_frame, height=40, width=200,
                                                            corner_radius=20,
                                                            text_color=Blue_green,
                                                            font=(Font, 20)
                                                            )
        self.editor_name_textbox.grid(row=0, column=3, pady=(20, 20), padx=0)
        self.editor_name_textbox.insert("0.0", "Opening Name")

        self.editor_move_list_textbox = customtkinter.CTkTextbox(self.editor_frame, height=400, width=200,
                                                                 corner_radius=20,
                                                                 text_color=Blue_green,
                                                                 font=(Font, 20)
                                                                 )
        self.editor_move_list_textbox.grid(row=1, column=3, rowspan=4, pady=(0, 10), padx=0, sticky="n")
        self.editor_move_list_textbox.insert("0.0", "edit")

        editor_save_button = customtkinter.CTkButton(self.editor_frame, width=200, corner_radius=20,
                                                     text="Save changes",
                                                     font=(Font, 20), command=lambda
                my_button="save_changes": self.controller.on_button_click(my_button)
                                                     )
        editor_save_button.grid(row=3, column=3, padx=0, pady=0)
        editor_delete_button = customtkinter.CTkButton(self.editor_frame, width=200, corner_radius=20,
                                                       text="Delete opening",
                                                       font=(Font, 20), command=lambda
                my_button="delete": self.controller.on_button_click(my_button)
                                                       )
        editor_delete_button.grid(row=3, column=3, padx=0, pady=(80, 0), sticky='EW')

        backward_button = customtkinter.CTkButton(self.editor_frame, width=200, corner_radius=20, text="<<",
                                                  font=(Font, 20), command=lambda
                my_button="backwards": self.controller.on_button_click(my_button)  # deleted disabled
                                                  )
        backward_button.grid(row=3, column=3, padx=0, pady=(60, 0), sticky='n')

        self.editor_reset_button = customtkinter.CTkButton(self.editor_frame, width=200, corner_radius=20,
                                                           text="Reset",
                                                           font=(Font, 20), command=lambda
                my_button="reset": self.controller.on_button_click(my_button)
                                                           )
        self.editor_reset_button.grid(row=3, column=3, padx=0, pady=(0, 40), sticky='s')

    def _populate_lboard_frame(self):
        # make a frame
        lboard_frame = customtkinter.CTkFrame(self.lboard_frame, width=600, height=600, corner_radius=0,
                                              fg_color=Blue_green
                                              )
        lboard_frame.pack(pady=40, padx=40, side="top", expand=True)

        # Entry bar  # Add button
        self.lboard_entry_box = customtkinter.CTkEntry(lboard_frame, corner_radius=100, height=40,
                                                       width=400,
                                                       text_color=Blue_green, placeholder_text="Enter username:",
                                                       font=(Font, 20)
                                                       )
        self.lboard_entry_box.grid(row=0, column=0, columnspan=2, padx=0, pady=(0, 20))

        add_button = customtkinter.CTkButton(lboard_frame, width=200, corner_radius=20,
                                             text="Add user", fg_color=Light_green, text_color=Blue_green,
                                             font=(Font, 20),
                                             command=lambda
                                                 button="add_user_lboard": self.controller.on_button_click(
                                                 button
                                             )
                                             )
        add_button.grid(row=0, column=3, padx=0, pady=(0, 20))

        # Name label # Bullet button # blitz button # rapid button
        username_label = customtkinter.CTkLabel(lboard_frame, width=200, height=30, corner_radius=0,
                                                fg_color=Light_green, text_color=Blue_green, text="User",
                                                font=(Font, 20)
                                                )
        username_label.grid(row=1, column=0, padx=0, pady=0)
        bullet_button = customtkinter.CTkButton(lboard_frame, width=200, corner_radius=0,
                                                text="Bullet", fg_color=Light_green,
                                                font=(Font, 20), text_color=Blue_green,
                                                command=lambda
                                                    button="lboard_bullet": self.controller.on_button_click(
                                                    button
                                                )
                                                )
        bullet_button.grid(row=1, column=1, padx=0, pady=0)
        blitz_button = customtkinter.CTkButton(lboard_frame, width=200, corner_radius=0,
                                               text="Blitz", fg_color=Light_green,
                                               font=(Font, 20), text_color=Blue_green,
                                               command=lambda
                                                   button="lboard_blitz": self.controller.on_button_click(
                                                   button
                                               )
                                               )
        blitz_button.grid(row=1, column=2, padx=0, pady=0)
        rapid_button = customtkinter.CTkButton(lboard_frame, width=200, corner_radius=0,
                                               text="Rapid", fg_color=Light_green, text_color=Blue_green,
                                               font=(Font, 20),
                                               command=lambda
                                                   button="lboard_rapid": self.controller.on_button_click(
                                                   button
                                               )
                                               )
        rapid_button.grid(row=1, column=3, padx=0, pady=0)

        # scrollable frame
        self.lboard_scrollframe = customtkinter.CTkScrollableFrame(lboard_frame, border_width=1,
                                                                   border_color=Blue_green,
                                                                   height=500, width=800, corner_radius=0,
                                                                   fg_color=Light_green
                                                                   )
        self.lboard_scrollframe.grid(row=2, column=0, rowspan=3, columnspan=4, pady=10)

        # labels per user
        clear_button = customtkinter.CTkButton(lboard_frame, width=200, corner_radius=20,
                                               text="Clear", fg_color=Light_green, text_color=Blue_green,
                                               font=(Font, 20), command=lambda
                button="clear_lboard": self.controller.on_button_click(
                button
            )
                                               )
        clear_button.grid(row=5, column=3, padx=0, pady=0)

    def _make_button_panel(self, frame):
        button_panel = customtkinter.CTkFrame(frame, height=300, width=400, corner_radius=0,
                                              border_width=0,
                                              fg_color=Blue_green, border_color=Green
                                              )
        button_panel.grid(row=0, column=0, rowspan=5, padx=(10, 5), pady=10, sticky="ns")
        button_panel.grid_rowconfigure(5, weight=1)

        # panel controls
        panel_button_height = 125
        panel_button_width = 220
        panel_button_spacingy = 10
        panel_button_fontsize = 30

        button1 = customtkinter.CTkButton(button_panel, height=panel_button_height,
                                          width=panel_button_width,
                                          text="Play", text_color=Blue_green,
                                          corner_radius=20, border_width=0,
                                          fg_color=Light_green, border_color=Green,
                                          font=(Font, panel_button_fontsize),
                                          command=lambda button="play": self.controller.on_button_click(button)
                                          )
        button1.grid(row=0, column=0, pady=(0, panel_button_spacingy), sticky='news')

        button2 = customtkinter.CTkButton(button_panel, height=panel_button_height,
                                          width=panel_button_width,
                                          text="Study", text_color=Blue_green,
                                          corner_radius=20, border_width=0,
                                          fg_color=Light_green, border_color=Green,
                                          font=(Font, panel_button_fontsize),
                                          command=lambda button="selector": self.controller.on_button_click(button)
                                          )
        button2.grid(row=1, column=0, pady=(0, panel_button_spacingy), sticky='s')

        button3 = customtkinter.CTkButton(button_panel, height=panel_button_height,
                                          width=panel_button_width,
                                          text="Create", text_color=Blue_green,
                                          corner_radius=20, border_width=0,
                                          fg_color=Light_green, border_color=Green,
                                          font=(Font, panel_button_fontsize),
                                          command=lambda button="create": self.controller.on_button_click(button)
                                          )
        button3.grid(row=2, column=0, pady=(0, panel_button_spacingy), sticky='s')

        button4 = customtkinter.CTkButton(button_panel, height=panel_button_height,
                                          width=panel_button_width,
                                          text="Database", text_color=Blue_green,
                                          corner_radius=20, border_width=0,
                                          fg_color=Light_green, border_color=Green,
                                          font=(Font, panel_button_fontsize),
                                          command=lambda button="database": self.controller.on_button_click(button)
                                          )
        button4.grid(row=3, column=0, pady=(0, panel_button_spacingy), sticky='s')

        button5 = customtkinter.CTkButton(button_panel, height=panel_button_height,
                                          width=panel_button_width,
                                          text="Leaderboard", text_color=Blue_green,
                                          corner_radius=20, border_width=0,
                                          fg_color=Light_green, border_color=Green,
                                          font=(Font, panel_button_fontsize),
                                          command=lambda button="lboard": self.controller.on_button_click(button)
                                          )
        button5.grid(row=4, column=0, pady=(0, panel_button_spacingy), sticky='s')

        logout_button = customtkinter.CTkButton(button_panel, height=panel_button_height,
                                                width=panel_button_width,
                                                text="Logout", text_color=Blue_green,
                                                corner_radius=20, border_width=0,
                                                fg_color=Light_green, border_color=Green,
                                                font=(Font, panel_button_fontsize),
                                                command=lambda button="logout": self.controller.on_button_click(button)
                                                )
        logout_button.grid(row=5, column=0, sticky='s')

    # def _make_settings_page(self):
    #     self.SettingsPage = customtkinter.CTkFrame(self.container, border_width=20, corner_radius=0,
    #                                                border_color=Light_green,
    #                                                fg_color=Blue_green
    #                                                )
    #     settings_page_display = customtkinter.CTkFrame(self.SettingsPage, corner_radius=40, height=1100, width=580,
    #                                                    fg_color=Green,
    #                                                    border_width=10,
    #                                                    border_color=Light_green
    #                                                    )
    #
    #     settings_page_display.pack(pady=0, padx=0, side="top", expand=True)
    #
    #     label1 = customtkinter.CTkLabel(settings_page_display, text="Label1",
    #                                     font=(Font, 20), bg_color='white'
    #                                     )
    #     label1.grid(row=0, column=0, pady=20)
    #     label2 = customtkinter.CTkLabel(settings_page_display, text="Label2",
    #                                     font=(Font, 20), bg_color='white'
    #                                     )
    #     label2.grid(row=1, column=0, pady=20)
    #     label3 = customtkinter.CTkLabel(settings_page_display, text="Label3",
    #                                     font=(Font, 20), bg_color='white'
    #                                     )
    #     label3.grid(row=2, column=0, pady=20)
    #
    #     back_button = customtkinter.CTkButton(settings_page_display, corner_radius=100, text="Back",
    #                                           font=(Font, 20),
    #                                           command=lambda button="main_page": self.controller.on_button_click(button)
    #                                           )
    #     back_button.grid(row=4, column=0, columnspan=1, padx=140, pady=50)

    def update_study_move_list(self, new_move, half_move):
        self.study_move_list_textbox.configure(state="normal")

        if half_move % 2 != 0:
            move_count = (int((half_move + 1) / 2))
            self.study_move_list_textbox.insert('end', "\n" + str(move_count) + ". ")

        self.study_move_list_textbox.insert('end', new_move + ' ')

        self.study_move_list_textbox.configure(state="disabled")

    def clear_study_move_list(self):
        self.study_move_list_textbox.configure(state="normal")
        self.study_move_list_textbox.delete("0.0", "end")
        self.study_move_list_textbox.insert("0.0", "Move list: ")
        self.study_move_list_textbox.configure(state="disabled")

    def update_play_move_list(self, new_move, half_move):
        self.play_move_list_textbox.configure(state="normal")

        if half_move % 2 != 0:
            move_count = (int((half_move + 1) / 2))
            self.play_move_list_textbox.insert('end', "\n" + str(move_count) + ". ")

        self.play_move_list_textbox.insert('end', new_move + ' ')

        self.play_move_list_textbox.configure(state="disabled")

    def clear_play_move_list(self):
        self.play_move_list_textbox.configure(state="normal")
        self.play_move_list_textbox.delete("0.0", "end")
        self.play_move_list_textbox.insert("0.0", "Move list: ")
        self.play_move_list_textbox.configure(state="disabled")

    def update_create_move_list(self, new_move, half_move):
        if half_move % 2 != 0:
            move_count = (int((half_move + 1) / 2))
            self.editor_move_list_textbox.insert('end', str(move_count) + ". ")
        self.editor_move_list_textbox.insert('end', new_move + ' ')

    def clear_create_move_list(self):
        self.editor_move_list_textbox.configure(state="normal")
        self.editor_move_list_textbox.delete("0.0", "end")
        self.editor_move_list_textbox.insert("0.0", "Move list: ")

    def message_correct(self):
        self.correct_frame = customtkinter.CTkFrame(self.study_board_frame, bg_color='green')
        self.correct_frame.grid(row=3, column=1, rowspan=2, columnspan=6)

        self.correct_message_label = customtkinter.CTkLabel(self.correct_frame, text="Correct!", bg_color='green',
                                                            text_color="white", font=(Font, 80)
                                                            )
        self.correct_message_label.grid(row=0, column=0)
        self.correct_frame.update()
        self.correct_frame.after(800, self.correct_frame.destroy())

    def message_incorrect(self):
        incorrect_frame = customtkinter.CTkFrame(self.study_board_frame, bg_color='red')
        incorrect_frame.grid(row=3, column=1, rowspan=2, columnspan=6)

        incorrect_message_label = customtkinter.CTkLabel(incorrect_frame, text="Try again.", bg_color='red',
                                                         text_color="white", font=(Font, 80)
                                                         )
        incorrect_message_label.grid(row=0, column=0)
        incorrect_frame.update()
        incorrect_frame.after(800, incorrect_frame.destroy())

    def message_finish(self):
        finish_frame = customtkinter.CTkFrame(self.study_board_frame, bg_color='red')
        finish_frame.grid(row=3, column=1, rowspan=2, columnspan=6)

        finish_message_label = customtkinter.CTkLabel(finish_frame, text="Finished!", bg_color='green',
                                                      text_color="white", font=(Font, 80)
                                                      )
        finish_message_label.grid(row=0, column=0)
        finish_frame.update()
        finish_frame.after(1500, finish_frame.destroy())

    def add_user_lboard(self, position, username, bullet, blitz, rapid):
        if position % 2 == 0:
            color = Alt_light_green
        else:
            color = Light_green
        height = 50
        user_frame = customtkinter.CTkFrame(self.lboard_scrollframe, width=800, height=height, corner_radius=0,
                                            fg_color=color
                                            )
        user_frame.grid(row=position, column=0, padx=0, pady=0)

        username_label = customtkinter.CTkLabel(user_frame, width=200, height=height,
                                                text_color=Blue_green, font=(Font, 20), text=username
                                                )
        username_label.grid(row=0, column=0, padx=0, pady=0)

        bullet_lbl = customtkinter.CTkLabel(user_frame, width=200, height=height,
                                            text_color=Blue_green, font=(Font, 20), text=bullet
                                            )
        bullet_lbl.grid(row=0, column=1, padx=0, pady=0)

        blitz_lbl = customtkinter.CTkLabel(user_frame, width=200, height=height,
                                           text_color=Blue_green, font=(Font, 20), text=blitz
                                           )
        blitz_lbl.grid(row=0, column=2, padx=0, pady=0)

        rapid_lbl = customtkinter.CTkLabel(user_frame, width=200, height=height,
                                           text_color=Blue_green, font=(Font, 20), text=rapid
                                           )
        rapid_lbl.grid(row=0, column=3, padx=0, pady=0)

    def clear_lboard(self):
        for child in self.lboard_scrollframe.winfo_children():
            child.destroy()
