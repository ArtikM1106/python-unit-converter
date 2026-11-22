import math
import tkinter as tk
from tkinter import ttk

from units import LinearConverter, TemperatureConverter


class ConverterWindow:
    def __init__(self, root):
        self.converters = {
            "Длина": (("м", "км", "см"), LinearConverter({"м": 1, "км": 1000, "см": 0.01})),
            "Масса": (("г", "кг"), LinearConverter({"г": 1, "кг": 1000})),
            "Температура": (("°C", "°F"), TemperatureConverter()),
        }
        root.title("Конвертер единиц")
        panel = ttk.Frame(root, padding=20)
        panel.grid()
        self.category = ttk.Combobox(panel, values=list(self.converters), state="readonly")
        self.source = ttk.Combobox(panel, state="readonly")
        self.target = ttk.Combobox(panel, state="readonly")
        self.value = ttk.Entry(panel)
        self.result = tk.StringVar()
        for row, (label, widget) in enumerate([
            ("Категория", self.category), ("Число", self.value),
            ("Из", self.source), ("В", self.target),
        ]):
            ttk.Label(panel, text=label).grid(row=row, column=0, sticky="w", pady=6)
            widget.grid(row=row, column=1, padx=12)
        ttk.Button(panel, text="Перевести", command=self.calculate).grid(row=4, columnspan=2, pady=10)
        ttk.Label(panel, textvariable=self.result, wraplength=320).grid(row=5, columnspan=2)
        self.category.current(0)
        self.category.bind("<<ComboboxSelected>>", self.change_category)
        self.change_category()

    def change_category(self, event=None):
        units, _ = self.converters[self.category.get()]
        for field in (self.source, self.target):
            field.configure(values=units)
        self.source.current(0)
        self.target.current(1)
        self.result.set("")

    def calculate(self):
        try:
            value = float(self.value.get().replace(",", "."))
            _, converter = self.converters[self.category.get()]
            result = converter.convert(value, self.source.get(), self.target.get())
            if not math.isfinite(value) or not math.isfinite(result):
                raise ValueError
        except ValueError:
            self.result.set("Введите конечное число допустимого размера.")
            return
        self.result.set(f"{result:.12g} {self.target.get()}")


if __name__ == "__main__":
    root = tk.Tk()
    ConverterWindow(root)
    root.mainloop()

