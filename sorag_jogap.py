import tkinter as tk  # Импортируем библиотеку tkinter для создания GUI
from tkinter import messagebox  # Импортируем messagebox из tkinter для показа окон с сообщениями
import time  # Импортируем библиотеку time для работы со временем

class SoragJogap:
    def __init__(self, master):
        self.master = master
        self.master.title("Interwýu sorag & jogap")  # Устанавливаем заголовок окна
        self.master.geometry("800x800")  # Устанавливаем размер окна
        self.master.configure(bg="white")  # Устанавливаем фоновый цвет окна

        self.dogry_jogap = 0  # Инициализируем количество правильных ответов
        self.sorag_indeksy = -1  # Инициализируем индекс текущего вопроса
        self.soraglar = []  # Создаем пустой список для вопросов
        self.dogry_jogaplar = []  # Создаем пустой список для правильных ответов
        self.start_wagty = time.time()  # Сохраняем текущее время для вычисления общего потраченного времени теста.
        self.bashlanan_wagt = time.time()  # Сохраняем текущее время начала для таймера
        self.sorag_wagt_limit = 30  # Устанавливаем лимит времени на вопрос в 30 секунд

        self.soraglary_yukle()  # Загружаем вопросы из файла
        self.widgetler_yasa()  # Создаем виджеты для интерфейса
        self.indiki_sorag()  # Показываем новый вопрос

    def soraglary_yukle(self):
        with open('soraglar.txt', 'r') as file:  # Открываем файл с вопросами
            setirler = file.readlines()  # Читаем все строки из файла

        sorag = ""  # Инициализируем переменную для хранения текста вопроса
        sechimler = []  # Инициализируем список для хранения вариантов ответа
        for setir in setirler:
            if setir.strip().startswith("Jogap:"):  # Если строка начинается с "Jogap:"
                self.dogry_jogaplar.append(setir.split(":")[1].strip())  # Добавляем правильный ответ в список
                self.soraglar.append((sorag, sechimler))  # Добавляем вопрос и варианты ответов в список вопросов
                sorag = ""  # Очищаем переменную для следующего вопроса
                sechimler = []  # Очищаем список вариантов ответов
            elif setir.strip().startswith(('A)', 'B)', 'C)', 'D)')):  # Если строка начинается с одного из вариантов ответа
                sechimler.append(setir.strip())  # Добавляем вариант ответа в список
            else:
                sorag = setir.strip()  # Если это текст вопроса, сохраняем его

    def widgetler_yasa(self):
        self.container = tk.Frame(self.master, bg="white")  # Создаем фрейм для размещения виджетов
        self.container.pack(expand=True)  # Располагаем фрейм по центру

        self.sorag_label = tk.Label(self.container, text="", wraplength=800, font=("Arial", 24), justify="center", bg="white", fg="blue")
        self.sorag_label.pack(pady=20)  # Создаем метку для отображения вопроса

        self.var = tk.StringVar()  # Создаем переменную для хранения выбранного варианта ответа
        self.options_frame = tk.Frame(self.container, bg="white")  # Создаем фрейм для размещения вариантов ответов
        self.options_frame.pack(pady=20)
        self.options = []  # Создаем список для хранения виджетов вариантов ответов
        for _ in range(4):
            cb = tk.Radiobutton(self.options_frame, text="", variable=self.var, value="", font=("Arial", 22), bg="white", activebackground="white", selectcolor="white")
            cb.pack(anchor='w', pady=5)  # Создаем радиокнопки для вариантов ответов
            self.options.append(cb)

        # Fixed size buttons using width and height options
        self.tassykla_knopka = tk.Button(self.container, text="Tassykla", command=self.jogaby_barla, font=("Arial", 22), fg="black", width=15, height=2)
        self.tassykla_knopka.pack(pady=10)  # Создаем кнопку для подтверждения ответа

        self.next_button = tk.Button(self.container, text="Indiki sorag", command=self.indiki_sorag, font=("Arial", 22), fg="black", width=15, height=2, state=tk.DISABLED)
        self.next_button.pack(pady=10)  # Создаем кнопку для перехода к следующему вопросу

        self.dogry_jogap_label = tk.Label(self.container, text="", wraplength=800, font=("Arial", 20), justify="center", bg="white", fg="green")
        self.dogry_jogap_label.pack(pady=20)  # Создаем метку для отображения правильного ответа

    def indiki_sorag(self):
        self.sorag_indeksy += 1  # Увеличиваем индекс текущего вопроса
        if self.sorag_indeksy < len(self.soraglar):  # Если есть еще вопросы
            sorag, sechimler = self.soraglar[self.sorag_indeksy]  # Получаем текущий вопрос и варианты ответов
            self.sorag_label.config(text=sorag)  # Обновляем текст вопроса
            self.dogry_jogap_label.config(text="")  # Очищаем текст правильного ответа
            for i, choice in enumerate(sechimler):
                self.options[i].config(text=choice, value=choice.split(')')[0].strip(), state=tk.NORMAL)  # Обновляем текст и значения вариантов ответов
            self.var.set("")  # Сбрасываем выбранный вариант ответа
            self.bashlanan_wagt = time.time()  # Сбрасываем таймер
            self.tassykla_knopka.config(state=tk.NORMAL)  # Активируем кнопку подтверждения
            self.next_button.config(state=tk.DISABLED)  # Деактивируем кнопку следующего вопроса
        else:
            self.sorag_jogaby_tamamla()  # Если вопросы закончились, завершаем тест

    def jogaby_barla(self):
        saylanan_jogap = self.var.get()  # Получаем выбранный вариант ответа
        dogry_jogaby = self.dogry_jogaplar[self.sorag_indeksy]
        if saylanan_jogap == dogry_jogaby:  # Проверяем, совпадает ли он с правильным ответом
            self.dogry_jogap += 1  # Если совпадает, увеличиваем счетчик правильных ответов
            self.dogry_jogap_label.config(text="Dogry jogap!")  # Обновляем метку правильного ответа
        else:
            self.dogry_jogap_label.config(text=f"Nädogry jogap! Dogry jogap: {dogry_jogaby}")  # Обновляем метку правильного ответа и показываем правильный ответ

        self.tassykla_knopka.config(state=tk.DISABLED)  # Деактивируем кнопку подтверждения
        self.next_button.config(state=tk.NORMAL)  # Активируем кнопку следующего вопроса

    def sorag_jogaby_tamamla(self):
        jemi_wagt = time.time() - self.start_wagty   # Вычисляем общее время прохождения теста
        messagebox.showinfo("Sorag & Jogap tamamlandy", f"Siziň netijäňiz: {self.dogry_jogap} dogry jogab\n{len(self.soraglar)} soragdan\nSarp edilen wagt: {int(jemi_wagt)/60:.0f} minut")
        self.master.quit()  # Показываем сообщение с результатами и закрываем приложение

if __name__ == "__main__":
    root = tk.Tk()  # Создаем главное окно
    app = SoragJogap(root)  # Создаем экземпляр нашего приложения
    root.mainloop()  # Запускаем главный цикл обработки событий
