from abc import ABC, abstractmethod
import requests
import os

api_key = os.getenv('SJob')


class ParsingError(Exception):
    pass


class API(ABC):
    """Абстрактный метод для работы с API"""
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(API):
    """Класс для работы с API HeadHunter"""
    def __init__(self, keyword: str):
        self.url = 'https://api.hh.ru/vacancies'
        self.params = {
            'text': keyword,
            'area': 113,
            'only_with_salary': True,
            'page': 0,
            'per_page': 100,
            'search_field': 'name'
        }

    def get_vacancies(self):
        """Метод, который возвращает вакансии по заданному параметру"""
        response = requests.get(self.url, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f'Ошибка получения вакансий! '
                               f'Статус: {response.status_code}')
        return response.json()['items']


class SuperJobAPI(API):
    """Класс для работы с API SuperJob"""
    def __init__(self, keyword: str):
        self.url = 'https://api.superjob.ru/2.0/vacancies'
        self.params = {
            'keyword': keyword,
            'countries': 1,
            'count': 100,
            'page': 0
        }

    def get_vacancies(self):
        """Метод, который возвращает вакансии по заданному параметру"""
        headers = {
            'X-Api-App-Id': api_key
        }
        response = requests.get(self.url, headers=headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f'Ошибка получения вакансий! '
                               f'Статус: {response.status_code}')
        return response.json()['objects']


class Vacancy:
    """Класс для создания экземпляров вакансий и работы с ними"""
    __slots__ = {'name', 'url', 'salary', 'requirement'}

    def __init__(self, name: str, url: str, salary: int, requirement: str):
        self.name = name
        self.url = url
        self.salary = salary
        self.requirement = requirement

    def __str__(self):
        return f'Название вакансии - {self.name}\n' \
               f'Ссылка - {self.url}\n'\
               f'Зарплата - {self.salary}RUB\n'\
               f'Требования - {self.requirement}\n'

    def __eq__(self, other):
        return self.salary == other.salary

    def __ne__(self, other):
        return self.salary != other.salary

    def __lt__(self, other):
        return self.salary < other.salary

    def __le__(self, other):
        return self.salary <= other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    def __ge__(self, other):
        return self.salary >= other.salary
