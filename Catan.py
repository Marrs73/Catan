#Программа для сборки статистики во время игры в катан
# Начало разработки: +- 21.08.2022
# Testing VS code integration with GitHub
# Заметки: никаких
# При вводе имён не должно содержаться символа "_"
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import re
from math import*
from colorama import*
init()


def ask(text):
    print(Fore.MAGENTA + text)
    print(Fore.YELLOW, end="")

def command_line(line):
    if  (line[0] == "+"):
        line = line.replace("+", "")
        list = line.split("_")

        dictionary[list[0]][0].append(list[1] + "-" + list[2])

    else: 
        hexs[int(line) - 2] += 1
        if (int(line)-2 != 5):
            for i in dictionary:
                pattern = f"{line}-\w+"
                count = 0
                for tile in dictionary[i][0]:
                    if (re.fullmatch(pattern, tile) != None): 
                        count += 1
                        index = tile.find("-")+1
                        dictionary[i][2][tile[index:]] += 1
                dictionary[i][1][int(line)-2] += count

# выбор режима
ask("Введите режим ввода информации [файл\динамика]:")
mode = input().lower()
name_list = list()
    
# Получение имён
if (mode == "динамика"):
    # Заготовка файла для вывода данных 
    open(r"statistics.txt", "w").close()
    file = open(r"statistics.txt", "w+", encoding="utf-8")
    file.write("\nИмена игроков:\n")

    ask("Вводите имена игроков [Для завершения пропишите end]:")
    while (True):
        new_name = input()
        file.write(new_name + "\n")
        if (new_name == "end"): break
        else: name_list.append(new_name)

elif (mode == "файл"):
    save = open(r"statistics_save1.txt", "r", encoding="utf-8")
    ask("Введите номер записи в файле сохранения:")
    note_num = input()

    if (note_num == "1"):
        save.readline()
    else:
        while(True):
            if (f"([{str(int(note_num)-1)}])" in save.readline()):
                [save.readline() for _ in range(5)]
                break
    
    while(True):
        new_name = save.readline()
        if (new_name == "end\n"): break
        else: name_list.append(new_name[:-1])
    save.readline()

# Создание списков для данных
dictionary = {name: [[], [0, 0, 0, 0, 0, "-", 0, 0, 0, 0, 0], {"mud":0, "sheep":0, "wheat":0, "iron":0, "wood":0}] 
for name in name_list}
hexs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Основной цикл работы
if (mode == "динамика"):
    file.write("Выпавшие суммы и приобретения по очереди:\n")
    
    ask("Вводите значения или комманды [Для завершения пропишите end]:")
    while (True):
        command = input()
        file.write(command + "\n")
        if (command == "end"): break

        command_line(command)
            
            
    # Выводы статистики в файл
    file.write(f"\nВыпавшие значения в игре:  {hexs}\n")
    file.write("Player stats: \n")
    [file.write(f"   {name}: \n      Полученные значения: {dictionary[name][1]}\n      Полученные ресурсы: {dictionary[name][2]}\n") 
    for name in name_list]
    file.close()

    # Сохранение статистики в запасной файл
    ask("Хотите ли вы сохранить файл статистики [да\нет]?:")
    if (input().lower() == "да"):
        ask("Запись сохранена")
        file = open(r"statistics.txt", "r", encoding="utf-8")
        save = open(r"statistics_save1.txt", "a+", encoding="utf-8")

        file_end = save.tell()
        save.seek(0)
        if (save.read() == ""): counter = 1
        else: 
            save.seek(file_end)
            save.seek(file_end-3)
            counter = int(save.read(1))+1
        save.seek(file_end)
        
        if (counter != 1): save.write("\n\n\n\n")
        text = file.readlines()
        save.writelines(text)
        save.write(f"Это была запись номер: ([{counter}])")
        file.close()
        save.close()
    
elif (mode == "файл"):
    while(True):
        new_line = save.readline()
        new_line = new_line.replace("\n", "")
        if (new_line == "end"): break
        
        command_line(new_line)

# заключительные выводы в консоль
    print(Fore.MAGENTA)
    print(hexs)
    print(*[Fore.MAGENTA + i + Fore.YELLOW + " - " + str(*[dictionary[i]]) for i in dictionary], sep="\n")

# ПОСТРОЕНИЕ ГРАФИКОВ В КОНЦЕ КОНЦОВ
fig = plt.figure(figsize=(10, 5))
fig.set_facecolor("#AABBCC")
labels = [str(i+2) for i in range(len(hexs))]
expect =  [i * sum(hexs) for i in [1/36, 2/36, 3/36, 4/36, 5/36, 6/36, 5/36, 4/36, 3/36, 2/36, 1/36]]
gs = GridSpec(ncols=2, nrows=1, figure=fig,  width_ratios=[2, 1])

x = np.arange(len(labels)) 
width = 0.35  

ax1 = plt.subplot(gs[0, 0])
#ax2 = plt.subplot(gs[0, 1])
rects1 = ax1.bar(x - width/2, hexs,   width, label="Итог игры")
rects2 = ax1.bar(x + width/2, expect, width, label="Мат. ожидание", color="#AAA")

# Add some text for labels, title and custom x-axis tick labels, etc.
ax1.set_ylabel("Число выпадений")
ax1.set_title("Сравнение итога и ожидания сумм")
ax1.set_xticks(x, labels)
ax1.legend()
plt.figtext(0.68, 0.87, "Отношение полученных к ожидаемым", size=11)
[plt.figtext(0.7, 0.8 - i*0.05, f"[{i+2}] - {hexs[i]}\{round(expect[i])}     {round(hexs[i]*100/sum(hexs))}% \ {round(expect[i]*100/sum(hexs))}%") for i in range(len(hexs))]

ax1.bar_label(rects1, padding=3)
fig.tight_layout()

# Второе окно
val_mud = [dictionary[i][2]["mud"] for i in name_list if (dictionary[i][2]["mud"] != 0)]
val_sheep = [dictionary[i][2]["sheep"]  for i in name_list if (dictionary[i][2]["sheep"] != 0)]
val_wheat = [dictionary[i][2]["wheat"]  for i in name_list if (dictionary[i][2]["wheat"] != 0)]
val_iron = [dictionary[i][2]["iron"]  for i in name_list if (dictionary[i][2]["iron"] != 0)]
val_wood = [dictionary[i][2]["wood"]  for i in name_list if (dictionary[i][2]["wood"] != 0)]
name_list1 = [i for i in name_list if (dictionary[i][2]["mud"] != 0)]
name_list2 = [i for i in name_list if (dictionary[i][2]["sheep"] != 0)]
name_list3 = [i for i in name_list if (dictionary[i][2]["wheat"] != 0)]
name_list4 = [i for i in name_list if (dictionary[i][2]["iron"] != 0)]
name_list5 = [i for i in name_list if (dictionary[i][2]["wood"] != 0)]
fig2 = plt.figure(figsize=(10, 6))
fig2.set_facecolor("#CCBBAA")
gs2 = GridSpec(ncols=3, nrows=2, figure=fig2)
ax_pie_1 = plt.subplot(gs2[0, 0])
ax_pie_2 = plt.subplot(gs2[0, 1])
ax_pie_3 = plt.subplot(gs2[0, 2])
ax_pie_4 = plt.subplot(gs2[1, 0])
ax_pie_5 = plt.subplot(gs2[1, 1])
ax_pie_1.pie(val_mud, labels=name_list1)
ax_pie_1.set_title("Глина", weight=900)
ax_pie_2.pie(val_sheep, labels=name_list2)
ax_pie_2.set_title("Скот", weight=900)
ax_pie_3.pie(val_wheat, labels=name_list3)
ax_pie_3.set_title("Зерно", weight=900)
ax_pie_4.pie(val_iron, labels=name_list4)
ax_pie_4.set_title("Руда", weight=900)
ax_pie_5.pie(val_wood, labels=name_list5)
ax_pie_5.set_title("Древесина", weight=900)
plt.figtext(0.67, 0.4,  "Отношения ресурсов", size=15, weight=900, color="#8A7968")
plt.figtext(0.69, 0.35, "игроков по виду", size=15, weight=900, color="#8A7968")
resources = ["mud", "sheep", "wheat", "iron", "wood"]
resources_ru = ["глина", "Скот", "Зерно", "Руда", "Древесина"]
[plt.figtext(0.65, 0.25 - 0.05 * i, f'{name_list[i]}:{dictionary[name_list[i]][2]["mud"]}, {dictionary[name_list[i]][2]["sheep"]}, {dictionary[name_list[i]][2]["wheat"]}, {dictionary[name_list[i]][2]["iron"]}, {dictionary[name_list[i]][2]["wood"]}') for i in range(len(name_list))]
#[plt.figtext(0.67, 0.30 - i*0.05, f"{i}:{dictionary[i][2]["mud"]}") for i in dictionary]
plt.show()