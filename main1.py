import json
import os
import tkinter as tk
from tkinter import messagebox, ttk


class MovieLibraryApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("750x500")
        self.DATA_FILE = "movies.json"
        self.movies = self.load_data()

        self.create_widgets()
        self.update_table(self.movies)

    def load_data(self):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_data(self):
        with open(self.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def create_widgets(self):
        # --- Форма ввода ---
        input_frame = tk.LabelFrame(self.root, text="Добавить фильм", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.entry_title = tk.Entry(input_frame)
        self.entry_title.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky="w")
        self.entry_genre = tk.Entry(input_frame)
        self.entry_genre.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(input_frame, text="Год выпуска:").grid(row=1, column=0, sticky="w")
        self.entry_year = tk.Entry(input_frame)
        self.entry_year.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="w")
        self.entry_rating = tk.Entry(input_frame)
        self.entry_rating.grid(row=1, column=3, padx=5, pady=2)

        btn_add = tk.Button(input_frame, text="Добавить фильм", command=self.add_movie)
        btn_add.grid(row=0, column=4, rowspan=2, padx=15, sticky="ns")

        # --- Блок фильтрации ---
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="По жанру:").grid(row=0, column=0, sticky="w")
        self.filter_genre = tk.Entry(filter_frame)
        self.filter_genre.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(filter_frame, text="По году:").grid(row=0, column=2, sticky="w")
        self.filter_year = tk.Entry(filter_frame)
        self.filter_year.grid(row=0, column=3, padx=5, pady=2)

        btn_filter = tk.Button(filter_frame, text="Применить", command=self.filter_movies)
        btn_filter.grid(row=0, column=4, padx=5)

        btn_reset = tk.Button(filter_frame, text="Сбросить", command=self.reset_filter)
        btn_reset.grid(row=0, column=5, padx=5)

        # --- Таблица вывода ---
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год выпуска")
        self.tree.heading("rating", text="Рейтинг")

        self.tree.column("title", width=250)
        self.tree.column("genre", width=150)
        self.tree.column("year", width=100, anchor="center")
        self.tree.column("rating", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_movie(self):
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year_str = self.entry_year.get().strip()
        rating_str = self.entry_rating.get().strip()

        if not (title and genre and year_str and rating_str):
            messagebox.showerror("Ошибка", "Заполните все поля ввода.")
            return

        if not year_str.isdigit():
            messagebox.showerror("Ошибка", "Год выпуска должен быть числом.")
            return

        try:
            rating = float(rating_str.replace(",", "."))
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10.")
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": int(year_str),
            "rating": rating,
        }
        self.movies.append(movie)
        self.save_data()
        self.update_table(self.movies)

        # Очистка полей
        self.entry_title.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_rating.delete(0, tk.END)

    def update_table(self, data_list):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for m in data_list:
            self.tree.insert(
                "", tk.END, values=(m["title"], m["genre"], m["year"], m["rating"])
            )

    def filter_movies(self):
        f_genre = self.filter_genre.get().strip().lower()
        f_year = self.filter_year.get().strip()

        filtered = self.movies

        if f_genre:
            filtered = [m for m in filtered if f_genre in m["genre"].lower()]

        if f_year:
            filtered = [m for m in filtered if str(m["year"]) == f_year]

        self.update_table(filtered)

    def reset_filter(self):
        self.filter_genre.delete(0, tk.END)
        self.filter_year.delete(0, tk.END)
        self.update_table(self.movies)


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()
