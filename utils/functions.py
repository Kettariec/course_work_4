from utils.API_classes import HeadHunterAPI, SuperJobAPI, Vacancy
from utils.Save_classes import JsonSaver


def main():
    """Функция интерфейса"""
    while True:
        user_word = input('Введите номер платформы:'
                          '\nHeadHunter - 1\nSuperJob - 2'
                          '\nДля выхода - 0\n')
        if user_word == '0':
            exit()
        if user_word == '1':
            user_word = input('Введите ключевое слово для поиска вакансии:')
            api_hh = HeadHunterAPI(user_word)
            hh_data = api_hh.get_vacancies()
            vacancies_hh = get_from_headhunter(hh_data)
            saver_hh = JsonSaver('hh_vacancies.json')
            for item in vacancies_hh:
                saver_hh.add_vacancy(item)
            print('Файл с вакансиями создан!')
            break
        elif user_word == '2':
            user_word = input('Введите ключевое слово для поиска вакансии:')
            api_sj = SuperJobAPI(user_word)
            sj_data = api_sj.get_vacancies()
            vacancies_sj = get_from_superjob(sj_data)
            saver_sj = JsonSaver('sj_vacancies.json')
            for item in vacancies_sj:
                saver_sj.add_vacancy(item)
            print('Файл с вакансиями создан!')
            break
        else:
            print('\nВводите только 1 или 2!\n')
            continue


def get_from_headhunter(vacancies: list):
    """Функция для инициализации вакансий с HeadHunter"""
    vacancies_list = []
    for item in vacancies:
        if item['snippet']['requirement']:
            if item['salary']['to']:
                if item['salary']['currency'] == 'RUR':
                    vacancy = Vacancy(item['name'], item['alternate_url'],
                                      item['salary']['to'],
                                      item['snippet']['requirement'])
                    vacancies_list.append(vacancy)
    return vacancies_list


def get_from_superjob(vacancies: list):
    """Функция для инициализации вакансий с SuperJob"""
    vacancies_list = []
    for item in vacancies:
        if item['candidat']:
            if item['payment_to']:
                if item['currency'] == 'rub':
                    vacancy = Vacancy(item['profession'],
                                      item['link'], item['payment_to'],
                                      item['candidat'])
                    vacancies_list.append(vacancy)
    return vacancies_list
