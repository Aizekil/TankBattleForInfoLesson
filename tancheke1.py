import tkinter as tk
from tkinter import messagebox
import random


class Tank:
    def __init__(self, name, armor, damage, crew):
        self.name = name
        self.armor = armor
        self.damage = damage
        self.crew = crew
        self.destroyed = False

    def get_info(self):
        status = "💀 УНИЧТОЖЕН" if self.destroyed else "✅ В БОЮ"
        return f"{self.name}\n🗿Броня: {self.armor}\n⚔Урон: {self.damage}\n👨‍👨‍👦Экипаж: {self.crew}"


# Создаем танки
tanks = [
    Tank("Шерман", 70, 80, 5),
    Tank("Тигр", 85, 90, 5),
    Tank("Т-34", 65, 85, 4)
]

# Создаем главное окно
window = tk.Tk()
window.title("Танковая битва")
window.geometry("600x500")
window.configure(bg="#5e5e5e")

BUTTON_STYLE = {
    "font": ("Comic Sans MS"),
    "width": 25,
    "height": 3,
    "relief": tk.RAISED,
    "bd": 3
}

# Глобальные переменные для элементов интерфейса
player_info_label = None
enemy_info_label = None
battle_text = None


def create_tank_selection():
    # Очищаем окно
    for widget in window.winfo_children():
        widget.destroy()

    # Восстанавливаем танки (на случай новой игры)
    for tank in tanks:
        tank.destroyed = False
        if tank.name == "Шерман":
            tank.crew = 5
        elif tank.name == "Тигр":
            tank.crew = 5
        elif tank.name == "Т-34":
            tank.crew = 4

    tk.Label(window, text="⚜ ТАНКОВАЯ БИТВА", font=("Courier New", 18, "bold"), bg="#bdbdbd").pack(pady=20)
    tk.Label(window, text="ВЫБЕРИТЕ ВАШ ТАНК", font=("Courier New", 14)).pack(pady=10)
    tk.Label(window, text="При создании игры ни один танк не пострадал", font=("Courier New",8)).pack(pady=5)
    # Создаем кнопки для каждого танка
    for tank in tanks:
        def select_tank(selected_tank=tank):
            start_battle(selected_tank)

        btn = tk.Button(
            window,
            text=tank.get_info(),
            font=("Arial", 11),
            command=select_tank,
            width=25,
            height=5
        )
        btn.pack(pady=10)


def start_battle(player_tank):
    # Выбираем случайного противника
    enemy_tank = random.choice([t for t in tanks if t != player_tank])

    # Очищаем окно
    for widget in window.winfo_children():
        widget.destroy()

    # Создаем интерфейс битвы
    tk.Label(window, text="БИТВА НАЧАЛАСЬ!", font=("Courier New", 16, "bold")).pack(pady=10)

    # Фрейм для танков
    tanks_frame = tk.Frame(window)
    tanks_frame.pack(pady=10)

    # Информация о игроке
    global player_info_label
    player_frame = tk.Frame(tanks_frame)
    player_frame.pack(side=tk.LEFT, padx=20)
    tk.Label(player_frame, text="ВАШ ТАНК", font=("Courier New", 12, "bold")).pack()
    player_info_label = tk.Label(player_frame, text=player_tank.get_info(), font=("Arial", 10))
    player_info_label.pack()

    # Информация о противнике
    global enemy_info_label
    enemy_frame = tk.Frame(tanks_frame)
    enemy_frame.pack(side=tk.RIGHT, padx=20)
    tk.Label(enemy_frame, text="ТАНК ПРОТИВНИКА", font=("Courier New", 12, "bold")).pack()
    enemy_info_label = tk.Label(enemy_frame, text=enemy_tank.get_info(), font=("Arial", 10))
    enemy_info_label.pack()

    # Кнопка для атаки
    attack_btn = tk.Button(
        window,
        text="АТАКОВАТЬ!",
        font=("Courier New", 14, "bold"),
        command=lambda: attack(player_tank, enemy_tank),
        bg="red",
        fg="white",
        width=15,
        height=2
    )
    attack_btn.pack(pady=10)

    # Кнопка для возврата к выбору танка
    back_btn = tk.Button(
        window,
        text="ВЫБРАТЬ ДРУГОЙ ТАНК",
        font=("Arial", 10),
        command=create_tank_selection
    )
    back_btn.pack(pady=5)

    # Поле для вывода боя
    global battle_text
    battle_frame = tk.Frame(window)
    battle_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    tk.Label(battle_frame, text="ХОД БОЯ:", font=("Courier New", 12)).pack()

    text_frame = tk.Frame(battle_frame)
    text_frame.pack(fill=tk.BOTH, expand=True, padx=20)

    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    battle_text = tk.Text(text_frame, height=10, yscrollcommand=scrollbar.set)
    battle_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=battle_text.yview)


def attack(player, enemy):
    # Добавляем разделитель в текст
    battle_text.insert(tk.END, "-" * 50 + "\n")

    # Ход игрока
    battle_text.insert(tk.END, f"Ваш ход: {player.name} атакует {enemy.name}!\n")

    # Расчет шанса попадания
    chance = 50 - enemy.armor + player.damage
    chance = max(10, min(90, chance))

    if random.randint(1, 100) <= chance:
        # Попадание!
        damage = random.randint(1, 2)
        enemy.crew -= damage
        battle_text.insert(tk.END, f"Попадание! Выбито {damage} членов экипажа.\n")

        if enemy.crew <= 0:
            enemy.destroyed = True
            enemy.crew = 0
            battle_text.insert(tk.END, f"Танк {enemy.name} уничтожен!\n\n")
            messagebox.showinfo("Победа!", "Вы победили!")
            update_tank_info(player, enemy)
            return
    else:
        battle_text.insert(tk.END, "Промах!\n")

    battle_text.insert(tk.END, "\n")

    # Ход противника
    battle_text.insert(tk.END, f"Ход противника: {enemy.name} атакует {player.name}!\n")

    chance = 50 - player.armor + enemy.damage
    chance = max(10, min(90, chance))

    if random.randint(1, 100) <= chance:
        # Попадание!
        damage = random.randint(1, 2)
        player.crew -= damage
        battle_text.insert(tk.END, f"Попадание! Выбито {damage} членов экипажа.\n")

        if player.crew <= 0:
            player.destroyed = True
            player.crew = 0
            battle_text.insert(tk.END, f"Танк {player.name} уничтожен!\n\n")
            messagebox.showinfo("Поражение", "Вы проиграли!")
            update_tank_info(player, enemy)
            return
    else:
        battle_text.insert(tk.END, "Промах!\n")

    # Обновляем информацию о танках
    update_tank_info(player, enemy)

    # Прокручиваем текст вниз
    battle_text.see(tk.END)


def update_tank_info(player, enemy):
    player_info_label.config(text=player.get_info())
    enemy_info_label.config(text=enemy.get_info())


# Запускаем выбор танка при старте
create_tank_selection()

window.mainloop()