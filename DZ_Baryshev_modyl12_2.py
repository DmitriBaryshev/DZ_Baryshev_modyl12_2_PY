# Задание 1
from abc import ABC, abstractmethod


class Light:
    def turn_on(self):
        print("Light is on")

    def turn_off(self):
        print("Light is off")


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class TurnOnCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_on()


class TurnOffCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_off()


class RemoteControl:
    def __init__(self):
        self.command = None

    def set_command(self, command):
        self.command = command

    def press_button(self):
        self.command.execute()


light = Light()
turn_on = TurnOnCommand(light)
turn_off = TurnOffCommand(light)

remote = RemoteControl()
remote.set_command(turn_on)
remote.press_button()

remote.set_command(turn_off)
remote.press_button()


# Задание 2
from abc import ABC, abstractmethod
import time


class NumberSet(ABC):
    @abstractmethod
    def get_numbers(self):
        pass

    @abstractmethod
    def add_observer(self, observer):
        pass

    @abstractmethod
    def remove_observer(self, observer):
        pass

    @abstractmethod
    def notify_observers(self):
        pass


class FileNumberSet(NumberSet):
    def __init__(self, filename):
        self.filename = filename
        self.observers = []
        self.numbers = []

    def get_numbers(self):
        with open(self.filename, 'r') as file:
            self.numbers = [int(x) for x in file.read().split()]
        self.notify_observers()
        return self.numbers

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update()


class Logger:
    def __init__(self, filename, subject):
        self.filename = filename
        self.subject = subject
        subject.add_observer(self)

    def update(self):
        with open(self.filename, 'a') as file:
            file.write(f"Numbers updated at {time.ctime()}\n")


class NumberSetProxy(NumberSet):
    def __init__(self, filename):
        self.file_number_set = FileNumberSet(filename)
        self.logger = Logger("log.txt", self.file_number_set)

    def get_numbers(self):
        return self.file_number_set.get_numbers()

    def add_observer(self, observer):
        self.file_number_set.add_observer(observer)

    def remove_observer(self, observer):
        self.file_number_set.remove_observer(observer)

    def notify_observers(self):
        self.file_number_set.notify_observers()


proxy = NumberSetProxy("numbers.txt")
numbers = proxy.get_numbers()
print("Numbers:", numbers)


# Задание 3
from abc import ABC, abstractmethod
import json
import time


# Фабричный метод
class EntityFactory(ABC):
    @abstractmethod
    def create_entity(self):
        pass


# Сущность Книга
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn


# Фабрика для создания книг
class BookFactory(EntityFactory):
    def create_entity(self):
        title = input("Enter the title of the book: ")
        author = input("Enter the author of the book: ")
        isbn = input("Enter the ISBN of the book: ")
        return Book(title, author, isbn)


# Читатель
class Reader:
    def __init__(self, name):
        self.name = name


# Библиотекарь
class Librarian:
    def __init__(self, name):
        self.name = name


# Наблюдатель
class Logger:
    def log(self, message):
        with open("log.txt", "a") as file:
            file.write(f"{message} at {time.ctime()}\n")


# Стратегия для поиска информации
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, query):
        pass


# Стратегия поиска по книгам
class BookSearchStrategy(SearchStrategy):
    def search(self, query):
        # Здесь должен быть код для поиска информации о книгах по запросу
        pass


# Заместитель для сохранения и загрузки данных из файла
class DataProxy:
    def save_to_file(self, data):
        with open("data.json", "w") as file:
            json.dump(data, file)

    def load_from_file(self):
        with open("data.json", "r") as file:
            return json.load(file)


# Клиентский код
def main():
    factory = BookFactory()
    book = factory.create_entity()
    librarian = Librarian("John")
    logger = Logger()
    logger.log(f"Book {book.title} added by {librarian.name}")
    proxy = DataProxy()
    data = {"books": [book.__dict__]}
    proxy.save_to_file(data)
    loaded_data = proxy.load_from_file()
    print("Loaded data:", loaded_data)


if __name__ == "__main__":
    main()



