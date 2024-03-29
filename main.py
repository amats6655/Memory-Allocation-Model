from random import randint, choice
import string
import os

os.system('cls')
RAM = 256  # Объем ОЗУ
QUEUE_MAX = 20  # Максимальный размер очереди задач

# Запрашиваем размер разделов у исполнителя
while True:
    try:
        SECTION_SIZE = int(input("Введите размер разделов (от 30 до 256): "))
        if 29 < SECTION_SIZE <= 256:
            break
        else:
            print("Введенный размер не подходит")
            continue
    except ValueError:
        print('Введите целое число')

SECTION_COUNT = RAM // SECTION_SIZE  # Определяем количество разделов ОЗУ
if SECTION_COUNT > 10:
    # по условиям задачи - максимальное количество разделов = 10
    SECTION_COUNT = 10
tasks_ram = []  # Список задач в ОЗУ
tasks_queue = []  # Список задач в очереди


# метод для создания задачи размером от 30 до 100, с рандомным именем длиной в 5 символов
def generate_task():
    task_size = randint(30, 100)
    task_name = ''.join(choice(string.ascii_letters.lower()) for _ in range(5))
    task = {'name': task_name, 'size': task_size}
    return task


# метод для добавления задачи в ОЗУ, либо в очередь задач
def put_task():
    task = generate_task()  
    os.system('cls')  
    print(task)  
    if task['size'] >= SECTION_SIZE:  # Если задача превышает размер секции
        print('\033[31m\033[40m Данная задача превышает размер раздела и не может быть помещена в память\033[0m\n')
    elif len(tasks_ram) < SECTION_COUNT:  # Если задача не превышает размер секции и имеется свободная секция в ОЗУ
        tasks_ram.append(task)
        return tasks_ram
    elif len(tasks_ram) >= SECTION_COUNT and len(tasks_queue) < QUEUE_MAX:  # если нет свободной секции в ОЗУ, но есть место в очереди задач
        tasks_queue.append(task)
        return tasks_queue
    else:  # Если заняты все секции ОЗУ и нет свободных мест в очереди задач
        print('\033[31m\033[40m ОЗУ и очередь заняты, задача не будет добавлена. Очистите очередь заданий или ОЗУ\033[0m\n')


# метод для закрытия задач, принимает в аргументах имя задачи
def close_task(name):
    for search_task_in_ram in tasks_ram: 
        if search_task_in_ram['name'] == name:  # Если имя в аргументе и имя элемента из ОЗУ совпадает
            tasks_ram.pop(tasks_ram.index(search_task_in_ram)) 
            if len(tasks_queue) != 0:  
                tasks_ram.append(tasks_queue[-1])  # Добавляем в ОЗУ последнюю добавленную задачу из очереди
                tasks_queue.pop(-1)  
            return tasks_ram, tasks_queue
    for search_task_in_queue in tasks_queue:  
        if search_task_in_queue['name'] == name:  # Если имя в аргументе и имя элемента очереди совпадает
            tasks_queue.pop(tasks_queue.index(search_task_in_queue))
            return tasks_queue


# Основной цикл программы
while True:

    print('\033[32m\033[40m Если хотите посмотреть список текущих задач, введите list, для выхода введите exit\033[0m\n')
    new_task = input('Хотите ли вы запустить новую задачу? (Y/n): \n')
    if new_task.lower() == 'n' or new_task.lower() == 'no':
        os.system('cls')
        print(f'Вот список задач в ОЗУ:\n'
              f'{tasks_ram}\n'
              f'Вот список задач в очереди задач:\n'
              f'{tasks_queue}')
        name = input('Введите имя задачи, которую вы хотите закрыть: \n')
        close_task(name)
        continue
    elif new_task.lower() == 'list':
        os.system('cls')
        print(f'Вот список задач в ОЗУ:\n'
              f'{tasks_ram}\n'
              f'Вот список задач в очереди задач:\n'
              f'{tasks_queue}')
        continue
    elif new_task.lower() == 'exit':
        os.system('cls')
        print('До свидания')
        os.system('pause')
        break
    else:
        os.system('cls')
        put_task()
        print(f'Состояние памяти в данный момент: \n'
              f'Количество разделов: {SECTION_COUNT};\n'
              f'количество запущенных задач в ОЗУ: {len(tasks_ram)}; \n'
              f'количество задач в очереди: {len(tasks_queue)}; \n'
              f'Вся память| Свободная память| Занятая память|\n'
              f'   {RAM}    |       {RAM - SECTION_SIZE * len(tasks_ram)}       |     {SECTION_SIZE * len(tasks_ram)} ')
        continue
