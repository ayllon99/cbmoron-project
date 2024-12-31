import customtkinter as ctk
from tkinter import filedialog, colorchooser, ttk
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        self.title("Player Analysis")
        self.geometry("1000x800")
        self.name = tk.StringVar()
        self.league_selected = tk.StringVar()
        self.season_selected = tk.StringVar()
        self.team_selected = tk.StringVar()
        self.player_selected = tk.StringVar()
        self.stat_mode = tk.StringVar(value="AVERAGE")
        self.stat = tk.StringVar()
        self.player_image = tk.StringVar()
        self.player_image_height = 200
        self.player_image_width = 200
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(pady=20, padx=10, fill="both", expand=True)
        self.tab1 = self.tabs.add("Home")
        self.tab2 = self.tabs.add("About")
        self.home_tab()
        self.about_tab()

    def home_tab(self):
        self.main_frame = ctk.CTkFrame(self.tab1)
        self.main_frame.pack(pady=20, padx=10, fill="both", expand=True)
        # Search bar
        self.search_frame = ctk.CTkFrame(self.main_frame)
        self.search_frame.pack(pady=10, padx=10, fill="x")
        self.search_bar = ctk.CTkEntry(self.search_frame, placeholder_text="Player name", width=200)
        self.search_bar.pack(side="left", padx=10)
        self.search_button = ctk.CTkButton(self.search_frame, text="Search", command=self.search_player)
        self.search_button.pack(side="left", padx=10)
        # League, season, team and player selectors
        self.selectors_frame = ctk.CTkFrame(self.main_frame)
        self.selectors_frame.pack(pady=10, padx=10, fill="x")
        self.league_label = ctk.CTkLabel(self.selectors_frame, text="League:")
        self.league_label.pack(side="left", padx=10)
        self.league_option = ctk.CTkOptionMenu(self.selectors_frame, variable=self.league_selected, values=["League 1", "League 2", "League 3"])
        self.league_option.pack(side="left", padx=10)
        self.season_label = ctk.CTkLabel(self.selectors_frame, text="Season:")
        self.season_label.pack(side="left", padx=10)
        self.season_option = ctk.CTkOptionMenu(self.selectors_frame, variable=self.season_selected, values=["Season 1", "Season 2", "Season 3"])
        self.season_option.pack(side="left", padx=10)
        self.team_label = ctk.CTkLabel(self.selectors_frame, text="Team:")
        self.team_label.pack(side="left", padx=10)
        self.team_option = ctk.CTkOptionMenu(self.selectors_frame, variable=self.team_selected, values=["Team 1", "Team 2", "Team 3"])
        self.team_option.pack(side="left", padx=10)
        self.player_label = ctk.CTkLabel(self.selectors_frame, text="Player:")
        self.player_label.pack(side="left", padx=10)
        self.player_option = ctk.CTkOptionMenu(self.selectors_frame, variable=self.player_selected, values=["Player 1", "Player 2", "Player 3"])
        self.player_option.pack(side="left", padx=10)
        # Submit button
        self.submit_button = ctk.CTkButton(self.main_frame, text="Submit", command=self.submit_player)
        self.submit_button.pack(pady=10, padx=10, fill="x")
        # Player details frame
        self.player_details_frame = ctk.CTkFrame(self.main_frame)
        self.player_details_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.player_image_label = ctk.CTkLabel(self.player_details_frame, text="Player Image")
        self.player_image_label.pack(pady=10, padx=10)
        self.player_name_label = ctk.CTkLabel(self.player_details_frame, text="Player Name")
        self.player_name_label.pack(pady=10, padx=10)
        self.player_details_text = tk.Text(self.player_details_frame, height=10, width=50)
        self.player_details_text.pack(pady=10, padx=10)
        self.stat_mode_option = ctk.CTkOptionMenu(self.main_frame, variable=self.stat_mode, values=["AVERAGE", "TOTAL"])
        self.stat_mode_option.pack(pady=10, padx=10)
        self.stat_option = ctk.CTkOptionMenu(self.main_frame, variable=self.stat, values=["Points", "Rebounds", "Assists"])
        self.stat_option.pack(pady=10, padx=10)
        self.chart_frame = ctk.CTkFrame(self.main_frame)
        self.chart_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.create_charts()

    def about_tab(self):
        self.about_frame = ctk.CTkFrame(self.tab2)
        self.about_frame.pack(pady=20, padx=10, fill="both", expand=True)
        self.about_text = tk.Text(self.about_frame, height=20, width=50)
        self.about_text.pack(pady=10, padx=10)
        self.about_text.insert(tk.INSERT, "This is an application for analyzing basketball players.")
        self.table_frame = ctk.CTkFrame(self.about_frame)
        self.table_frame.pack(pady=10, padx=10, fill="x")
        self.table = ttk.Treeview(self.table_frame)
        self.table['columns'] = ('Player', 'Points', 'Rebounds', 'Assists')
        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.column("Player", anchor=tk.W, width=100)
        self.table.column("Points", anchor=tk.W, width=100)
        self.table.column("Rebounds", anchor=tk.W, width=100)
        self.table.column("Assists", anchor=tk.W, width=100)
        self.table.heading("#0", text="", anchor=tk.W)
        self.table.heading("Player", text="Player", anchor=tk.W)
        self.table.heading("Points", text="Points", anchor=tk.W)
        self.table.heading("Rebounds", text="Rebounds", anchor=tk.W)
        self.table.heading("Assists", text="Assists", anchor=tk.W)
        self.table.pack(pady=10, padx=10, fill="x")
        self.insert_table_data()

    def search_player(self):
        player_name = self.search_bar.get()
        if player_name:
            self.player_name_label.configure(text=player_name)
            self.player_details_text.delete(1.0, tk.END)
            self.player_details_text.insert(tk.INSERT, f"Player name: {player_name}\nLeague: {self.league_selected.get()}\nSeason: {self.season_selected.get()}\nTeam: {self.team_selected.get()}")

    def submit_player(self):
        player_name = self.player_selected.get()
        if player_name:
            self.player_name_label.configure(text=player_name)
            self.player_details_text.delete(1.0, tk.END)
            self.player_details_text.insert(tk.INSERT, f"Player name: {player_name}\nLeague: {self.league_selected.get()}\nSeason: {self.season_selected.get()}\nTeam: {self.team_selected.get()}")

    def create_charts(self):
        self.figure = Figure(figsize=(7, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.plot([1, 2, 3, 4, 5])
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.image = Image.open('frontend_container/image_not_found.png')
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.player_image_label = ctk.CTkLabel(self.chart_frame, image=self.image_tk)
        self.player_image_label.image = self.image_tk
        self.player_image_label.pack(pady=10, padx=10)

    def insert_table_data(self):
        for i in range(10):
            self.table.insert('', 'end', values=(f"Player {i}", random.randint(1, 100), random.randint(1, 100), random.randint(1, 100)))

if __name__ == "__main__":
    app = App()
    app.mainloop()