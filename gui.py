# Imports
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import db_manager

class GameStatsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Stats Tracker")
        self.create_main_frame()

        db_manager.create_tables()
        self.load_games()

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.add_game_button = ttk.Button(self.main_frame, text='Add Game', command=self.add_game)
        self.add_game_button.grid(row=0, column=0, pady=10)

        self.games_listbox = tk.Listbox(self.main_frame, height=10, width=50)
        self.games_listbox.grid(row=1, column=0, pady=10)

        self.add_session_button = ttk.Button(self.main_frame, text='Add Game Session', command=self.add_session)
        self.add_session_button.grid(row=2, column=0, pady=10)

        self.add_attribute_button = ttk.Button(self.main_frame, text='Add Attribute (stat)', command=self.add_attribute)
        self.add_attribute_button.grid(row=3, column=0, pady=10)

    def add_game(self):
        add_game_window = tk.Toplevel(self.root)
        add_game_window.title("Add Game")

        ttk.Label(add_game_window, text='Game Name:').grid(row=0, column=0, padx=10, pady=5)
        game_name_entry = ttk.Entry(add_game_window)
        game_name_entry.grid(row=0, column=1, padx=10, pady=5)

        def save_game():
            game_name = game_name_entry.get()
            self.save_game_to_db(game_name)
            self.games_listbox.insert(tk.END, game_name)
            add_game_window.destroy()

        save_button = ttk.Button(add_game_window, text='Save', command=save_game)
        save_button.grid(row=1, column=1, pady=10)

    def save_game_to_db(self, game_name):
        conn = db_manager.connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO games (name) VALUES (?)', (game_name,))
        conn.commit()
        conn.close()

    def load_games(self):
        conn = db_manager.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM games')
        games = cursor.fetchall()
        for game in games:
            self.games_listbox.insert(tk.END, game[0])
        conn.close()

    def add_session(self):
        add_session_window = tk.Toplevel(self.root)
        add_session_window.title("Add Game Session")

        game_names = self.get_game_names()
        ttk.Label(add_session_window, text='Game:').grid(row=0, column=0, padx=10, pady=5)
        game_combobox = ttk.Combobox(add_session_window, values=game_names)
        game_combobox.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(add_session_window, text='Session Date:').grid(row=1, column=0, padx=10, pady=5)
        session_date_entry = ttk.Entry(add_session_window)
        session_date_entry.grid(row=1, column=1, padx=10, pady=5)

        attributes_frame = ttk.Frame(add_session_window)
        attributes_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Label(attributes_frame, text='Attribute Name').grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(attributes_frame, text='Attribute Value').grid(row=0, column=1, padx=10, pady=5)

        attribute_entries = []

        def add_attribute_entry():
            row = len(attribute_entries)
            attribute_name_entry = ttk.Entry(attributes_frame)
            attribute_name_entry.grid(row=row+1, column=0, padx=10, pady=5)
            attribute_value_entry = ttk.Entry(attributes_frame)
            attribute_value_entry.grid(row=row+1, column=1, padx=10, pady=5)
            attribute_entries.append((attribute_name_entry, attribute_value_entry))

        add_attribute_button = ttk.Button(attributes_frame, text='Add Attribute', command=add_attribute_entry)
        add_attribute_button.grid(row=1, column=2, padx=10, pady=5)
        add_attribute_entry()

        def save_session():
            game_name = game_combobox.get()
            session_date = session_date_entry.get()
            game_id = self.get_game_id(game_name)

            session_id = self.save_session_to_db(game_id, session_date)

            for attribute_name_entry, attribute_value_entry in attribute_entries:
                attribute_name = attribute_name_entry.get()
                attribute_value = attribute_value_entry.get()
                self.save_attribute_to_db(session_id, attribute_name, attribute_value)

            add_session_window.destroy()

        save_button = ttk.Button(add_session_window, text='Save', command=save_session)
        save_button.grid(row=3, column=1, pady=10)

    def add_attribute(self):
        add_attribute_window = tk.Toplevel(self.root)
        add_attribute_window.title("Add Attribute")

        ttk.Label(add_attribute_window, text='Game:').grid(row=0, column=0, padx=10, pady=5)
        game_names = self.get_game_names()
        game_combobox = ttk.Combobox(add_attribute_window, values=game_names)
        game_combobox.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(add_attribute_window, text='Attribute Name:').grid(row=1, column=0, padx=10, pady=5)
        attribute_name_entry = ttk.Entry(add_attribute_window)
        attribute_name_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(add_attribute_window, text='Attribute Value:').grid(row=2, column=0, padx=10, pady=5)
        attribute_value_entry = ttk.Entry(add_attribute_window)
        attribute_value_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(add_attribute_window, text='Calculation (optional):').grid(row=3, column=0, padx=10, pady=5)
        calculation_entry = ttk.Entry(add_attribute_window)
        calculation_entry.grid(row=3, column=1, padx=10, pady=5)

        def save_attribute():
            game_name = game_combobox.get()
            attribute_name = attribute_name_entry.get()
            attribute_value = attribute_value_entry.get()
            calculation = calculation_entry.get()

            game_id = self.get_game_id(game_name)
            session_id = self.save_session_to_db(game_id, 'N/A')  # Use 'N/A' as a placeholder date for attributes

            if calculation:
                attribute_value = self.calculate_attribute_value(session_id, calculation)

            self.save_attribute_to_db(session_id, attribute_name, attribute_value)
            add_attribute_window.destroy()

        save_button = ttk.Button(add_attribute_window, text='Save', command=save_attribute)
        save_button.grid(row=4, column=1, pady=10)

    def get_game_names(self):
        conn = db_manager.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM games')
        games = cursor.fetchall()
        conn.close()
        return [game[0] for game in games]

    def get_game_id(self, game_name):
        conn = db_manager.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM games WHERE name = ?', (game_name,))
        game_id = cursor.fetchone()[0]
        conn.close()
        return game_id

    def save_session_to_db(self, game_id, session_date):
        conn = db_manager.connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sessions (game_id, session_date) VALUES (?, ?)', (game_id, session_date))
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id

    def save_attribute_to_db(self, session_id, attribute_name, attribute_value):
        conn = db_manager.connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO attributes (session_id, attribute_name, attribute_value) VALUES (?, ?, ?)',
                       (session_id, attribute_name, attribute_value))
        conn.commit()
        conn.close()

    def calculate_attribute_value(self, session_id, calculation):
        conn = db_manager.connect_db()
        cursor = conn.cursor()

        cursor.execute('SELECT attribute_name, attribute_value FROM attributes WHERE session_id = ?', (session_id,))
        attributes = {name: float(value) for name, value in cursor.fetchall()}
        conn.close()

        try:
            result = eval(calculation, {"__builtins__": None}, attributes)
            return str(result)
        except Exception as e:
            messagebox.showerror("Calculation Error", f"Error in calculation: {e}")
            return ""

if __name__ == "__main__":
    root = tk.Tk()
    app = GameStatsApp(root)
    root.mainloop()
