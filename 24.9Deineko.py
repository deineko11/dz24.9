import tkinter as tk
from tkinter import messagebox


class VectorInputDialog(tk.Toplevel):
    """Модальний діалог для введення вектора з n компонент."""

    def __init__(self, parent: tk.Tk, n: int, title: str = "Введіть вектор"):
        super().__init__(parent)
        self.parent = parent
        self.n = n
        self.result = None     # стане списком з float після успішного введення

        self.title(title)
        self.resizable(False, False)

        # Формуємо поле введення для кожної компоненти
        self.entries = []
        for i in range(n):
            tk.Label(self, text=f"x{i + 1}:").grid(row=i, column=0, padx=6, pady=3, sticky="e")
            e = tk.Entry(self, width=10)
            e.grid(row=i, column=1, padx=6, pady=3)
            self.entries.append(e)

        # Кнопки OK / Скасувати
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=n, column=0, columnspan=2, pady=8)

        ok_btn = tk.Button(btn_frame, text="OK", width=8, command=self._on_ok)
        ok_btn.pack(side="left", padx=4)

        cancel_btn = tk.Button(btn_frame, text="Скасувати", width=8, command=self.destroy)
        cancel_btn.pack(side="left", padx=4)

        # Робимо діалог модальним
        self.grab_set()
        self.entries[0].focus_set()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _on_ok(self):
        values = []
        for idx, entry in enumerate(self.entries, 1):
            text = entry.get().strip()
            if not text:
                messagebox.showerror("Помилка", f"Компоненту x{idx} не заповнено.")
                return
            try:
                values.append(float(text.replace(",", ".")))
            except ValueError:
                messagebox.showerror("Помилка", f"Компонента x{idx} має бути числом.")
                return
        self.result = values
        self.destroy()


class ScalarProductApp(tk.Frame):
    """Головне вікно застосунку."""

    def __init__(self, master: tk.Tk):
        super().__init__(master)
        master.title("Скалярний добуток двох векторів")
        master.resizable(False, False)
        self.grid(padx=10, pady=10)

        # Ввід n
        tk.Label(self, text="n (кількість компонент):").grid(row=0, column=0, sticky="e")
        self.n_entry = tk.Entry(self, width=6)
        self.n_entry.grid(row=0, column=1, sticky="w", padx=(0, 12))

        # Кнопка введення векторів
        self.input_btn = tk.Button(self, text="Ввести вектори", command=self.input_vectors)
        self.input_btn.grid(row=0, column=2, padx=4, pady=4)

        # Списки для векторів
        tk.Label(self, text="Вектор 1:").grid(row=1, column=0, pady=(10, 0))
        tk.Label(self, text="Вектор 2:").grid(row=1, column=2, pady=(10, 0))

        self.list1 = tk.Listbox(self, height=10, width=10)
        self.list1.grid(row=2, column=0, rowspan=4, padx=(0, 12))

        self.list2 = tk.Listbox(self, height=10, width=10)
        self.list2.grid(row=2, column=2, rowspan=4, padx=(0, 12))

        # Результат
        self.result_lbl = tk.Label(self, text="Скалярний добуток: —", font=("Arial", 12, "bold"))
        self.result_lbl.grid(row=6, column=0, columnspan=3, pady=(12, 0))

    def input_vectors(self):
        # Перевіряємо n
        n_text = self.n_entry.get().strip()
        if not n_text:
            messagebox.showerror("Помилка", "Введіть n.")
            return
        if not n_text.isdigit():
            messagebox.showerror("Помилка", "n має бути додатним цілим числом.")
            return
        n = int(n_text)
        if n <= 0:
            messagebox.showerror("Помилка", "n має бути > 0.")
            return

        # Введення першого вектора
        dlg1 = VectorInputDialog(self.master, n, title="Введіть 1-й вектор")
        self.master.wait_window(dlg1)
        if dlg1.result is None:
            return  # користувач скасував

        # Введення другого вектора
        dlg2 = VectorInputDialog(self.master, n, title="Введіть 2-й вектор")
        self.master.wait_window(dlg2)
        if dlg2.result is None:
            return

        v1, v2 = dlg1.result, dlg2.result

        # Показуємо компоненти у списках
        self.list1.delete(0, tk.END)
        self.list2.delete(0, tk.END)
        for x in v1:
            self.list1.insert(tk.END, f"{x:g}")
        for y in v2:
            self.list2.insert(tk.END, f"{y:g}")

        # Обчислюємо скалярний добуток
        scalar_prod = sum(x * y for x, y in zip(v1, v2))
        self.result_lbl.config(text=f"Скалярний добуток: {scalar_prod:g}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ScalarProductApp(root)
    app.mainloop()