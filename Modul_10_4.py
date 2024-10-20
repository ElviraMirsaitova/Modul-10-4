from threading import Thread
from time import sleep
from random import randint
from queue import Queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        free_tables = len(self.tables)
        for guest in guests:
            if not free_tables:
                self.queue.put(guest)
                print(f'{guest.name} в очереди')
                continue
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    guest.start()
                    print(f'{guest.name} сел(-а) за стол номер {table.number}')
                    break
            free_tables = free_tables - 1


    def discuss_guests(self):
        #пока каждый объект класса Стол имеет значение атрибута НЕ Нон для объекта из списка объектов сэлфтэйблс
        #или не текущая очередь пустая:
        while any(table.guest is not None for table in self.tables) or not self.queue.empty():
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest.join()
                    if not self.queue.empty():
                        table.guest = self.queue.get()
                        print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                        table.guest.start()
                    else:
                        table.guest = None

if __name__ == '__main__':
# Создание столов
    tables = [Table(number) for number in range(1, 6)]
# Имена гостей
    guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
    ]
# Создание гостей
    guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
    cafe = Cafe(*tables)
# Приём гостей
    cafe.guest_arrival(*guests)
# Обслуживание гостей
    cafe.discuss_guests()

