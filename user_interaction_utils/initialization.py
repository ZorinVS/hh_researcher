from src.saver.vacancy_saver import VacancyJSON


def initialization_menu():
    print("=== Меню инициализации ===")
    print("Выберите, как вы хотите назвать файл для хранения вакансий:")
    print("1. Использовать стандартное имя файла (vacancies.json)")
    print("2. Задать своё имя файла")
    print("===========================")


def set_file_name():
    initialization_menu()

    while True:
        choice = input("Выберите пункт меню (1-2): ")

        if choice == "1":
            vacancy_saver = VacancyJSON()
            print("Используется стандартное имя файла: vacancies.json")
            return vacancy_saver

        elif choice == "2":
            filename = input("Введите имя файла: ").strip()
            if not filename.endswith(".json"):
                filename += ".json"
            vacancy_saver = VacancyJSON(filename)
            print(f"Используется имя файла: {filename}")
            return vacancy_saver
