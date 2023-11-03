from abc import ABC, abstractmethod
import json


class Saver(ABC):
    """Абстрактный класс для сохранения данных в файл"""
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_data_by_salary(self, salary):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JsonSaver(Saver):
    """Класс для работы с данными в json-файле"""
    def __init__(self, file):
        self.file = file

    def load_file(self):
        with open(self.file, encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

    def save_file(self, data):
        with open(self.file, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)
            # ensure_ascii - для корректного отображения кириллицы

    def add_vacancy(self, vacancy):
        """Метод для добавления вакансии в json-файл"""
        new_vacancy = {
            'name': vacancy.name, 'url': vacancy.url,
            'salary': vacancy.salary, 'requirement': vacancy.requirement
        }
        data_file = self.load_file()
        data_file.append(new_vacancy)
        self.save_file(data_file)

    def get_data_by_salary(self, salary: int):
        """Метод, возвращающий вакансии по заданной зарплате"""
        result = []
        data_file = self.load_file()
        for item in data_file:
            if item['salary'] >= salary:
                result.append(item)
        return result

    def delete_vacancy(self, vacancy):
        """Метод удаляющий вакансию из json-файла"""
        data = self.load_file()
        for item in data:
            if item['url'] == vacancy.url:
                data.remove(item)
        self.save_file(data)
