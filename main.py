import tkinter as tk
from tkinter import ttk, messagebox
import json

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker — Учёт прочитанных книг")
        self.data_file = "books.json"
        self.books = self.load_data()

        # --- Форма ввода ---
        frame_input = tk.LabelFrame(root, text="Добавить новую книгу", padx=10, pady=10)
        frame_input.pack(padx=10, pady=5, fill="x")

        tk.Label(frame_input, text="Название:").grid(row=0, column=0)
        self.ent_title = tk.Entry(frame_input)
        self.ent_title.grid(row=0, column=1, padx=5)

        tk.Label(frame_input, text="Автор:").grid(row=0, column=2)
        self.ent_author = tk.Entry(frame_input)
        self.ent_author.grid(row=0, column=3, padx=5)

        tk.Label(frame_input, text="Жанр:").grid(row=1, column=0, pady=5)
        self.cb_genre = ttk.Combobox(frame_input, values=["Художественная", "Научпоп", "Фэнтези", "Детектив", "Другое"])
        self.cb_genre.grid(row=1, column=1, padx=5)

        tk.Label(frame_input, text="Страниц:").grid(row=1, column=2)
        self.ent_pages = tk.Entry(frame_input)
        self.ent_pages.grid(row=1, column=3, padx=5)

        btn_add = tk.Button(frame_input, text="Добавить книгу", command=self.add_book, bg="#fff9c4")
        btn_add.grid(row=1, column=4, padx=10)

        # --- Фильтры ---
        frame_filter = tk.Frame(root, padx=10)
        frame_filter.pack(fill="x", pady=5)

        tk.Label(frame_filter, text="Жанр:").pack(side="left")
        self.flt_genre = ttk.Combobox(frame_filter, values=["Все", "Художественная", "Научпоп", "Фэнтези", "Детектив", "Другое"], width=15)
        self.flt_genre.current(0)
        self.flt_genre.pack(side="left", padx=5)

        self.var_long_books = tk.BooleanVar()
        tk.Checkbutton(frame_filter, text="Более 200 страниц", variable=self.var_long_books, command=self.update_table).pack(side="left", padx=10)
        
        self.flt_genre.bind("<<ComboboxSelected>>", lambda e: self.update_table())

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("Название", "Автор", "Жанр", "Страницы"), show='headings')
        self.tree.heading("Название", text="Название")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Страницы", text="Страницы")
        self.tree.pack(padx=10, pady=5, fill="both", expand=True)

        self.update_table()

    def add_book(self):
        title = self.ent_title.get().strip()
        author = self.ent_author.get().strip()
        genre = self.cb_genre.get()
        pages = self.ent_pages.get()

        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        try:
            pages = int(pages)
            if pages <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
            return

        self.books.append({"title": title, "author": author, "genre": genre, "pages": pages})
        self.save_data()
        self.update_table()
        
        # Очистка полей
        self.ent_title.delete(0, tk.END)
        self.ent_author.delete(0, tk.END)
        self.ent_pages.delete(0, tk.END)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        f_genre = self.flt_genre.get()
        only_long = self.var_long_books.get()

        for b in self.books:
            match_genre = (f_genre == "Все" or b['genre'] == f_genre)
            match_pages = (not only_long or b['pages'] > 200)

            if match_genre and match_pages:
                self.tree.insert("", "end", values=(b['title'], b['author'], b['genre'], b['pages']))

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False)

    def load_data(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return []

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
