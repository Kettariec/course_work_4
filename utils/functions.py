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
            user_word = input('Введите название вакансии:')
            if user_word == '0':
                exit()
            api_hh = HeadHunterAPI(user_word)
            hh_data = api_hh.get_vacancies()
            vacancies = get_from_headhunter(hh_data)
            while True:
                user_top = input('Какое количество топовых'
                                 ' вакансий получить? От 1 до 30:')
                if user_top == '0':
                    exit()
                if int(user_top) < 0:
                    print('Число не может быть отрицательным!')
                    continue
                if int(user_top) > 30:
                    print('Используйте число до 30!')
                    continue
                if 0 < int(user_top) <= 30:
                    top_vacancies = get_top_vacancies(vacancies, int(user_top))
                    break
                else:
                    print('Введите число!')
                    continue
            if len(top_vacancies) == 0:
                print('\nВакансии не найдены!')
                continue
            saver = JsonSaver('hh_vacancies.json')
            for item in top_vacancies:
                saver.add_vacancy(item)
            print('\nФайл с топовыми вакансиями создан!')
            break
        elif user_word == '2':
            user_word = input('Введите название вакансии:')
            if user_word == '0':
                exit()
            api_sj = SuperJobAPI(user_word)
            sj_data = api_sj.get_vacancies()
            vacancies = get_from_superjob(sj_data)
            while True:
                user_top = input('Какое количество топовых'
                                 ' вакансий получить? От 1 до 30:')
                if user_top == '0':
                    exit()
                if int(user_top) < 0:
                    print('Число не может быть отрицательным!')
                    continue
                if int(user_top) > 30:
                    print('Используйте число до 30!')
                    continue
                if 0 < int(user_top) <= 30:
                    top_vacancies = get_top_vacancies(vacancies, int(user_top))
                    break
                else:
                    print('Введите число!')
                    continue
            if len(top_vacancies) == 0:
                print('\nВакансии не найдены!')
                continue
            saver = JsonSaver('sj_vacancies.json')
            for item in top_vacancies:
                saver.add_vacancy(item)
            print('\nФайл с топовыми вакансиями создан!')
            break
        else:
            print('\nВводите только 1 или 2!\n')
            continue
    while True:
        filter_words = input("Для фильтрации вакансий введите"
                             " ключевые слова через пробел:\n").lower()
        if filter_words == '0':
            exit()
        filtered_vacancies = filter_vacancies(
            top_vacancies, filter_words.split()
        )
        if len(filtered_vacancies) == 0:
            print('\nНет вакансий по данным критериям!'
                  '\nДля выхода введите - 0\n')
            continue
        else:
            for i in filtered_vacancies:
                print(i)
            break
    while True:
        user_del = input('\nВведите ссылку на вакансию,'
                         ' чтобы удалить её из файла:\n')
        if user_del == '0':
            exit()
        saver.delete_vacancy(user_del)
        print('\nДля выхода из программы введите - 0')
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


def filter_vacancies(vacancies: list, filter_words: list):
    """Функция для фильтрации вакансий"""
    filtered_list = []
    for vacancy in vacancies:
        for word in filter_words:
            if word in vacancy.requirement.lower().split():
                filtered_list.append(vacancy)
    return filtered_list


def get_top_vacancies(vacancies_list: list, top_number: int):
    """Функция для получения топовых вакансий по зарплате"""
    return sorted(vacancies_list)[-top_number:]
