def search_menu_items():
    print("\n=== Меню поиска ===")
    print("1. Поиск по всей России")
    print("2. Сделать поиск в определенном городе")
    print("3. Назад в главное меню")
    print("=====================")

    # select_search_items()


def select_search_menu_items(hh_api, data_saver):
    # search_menu_items()

    while True:
        search_menu_items()
        choice = input("Выберите пункт меню (1-3): ").strip()

        if choice == "1":
            if search_vacancies(hh_api, data_saver, search_in_city=False):
                return False
        elif choice == "2":
            if search_vacancies(hh_api, data_saver, search_in_city=True):
                return False
        elif choice == "3":
            return True  # Возврат True, чтобы указать на выход в главное меню


def search_vacancies(hh_api, data_saver, search_in_city):
    print("\n--- Поиск вакансий ---")
    if search_in_city:
        city_name = input("Название города: ").strip()
    query = input("Поисковой запрос: ")
    if search_in_city:
        vacancies = hh_api.get_vacancies(query, city_name)
    else:
        vacancies = hh_api.get_vacancies(query)

    print("\n--- Результат поиска ---")
    if vacancies:
        quantity = len(vacancies)
        print(f"Количество вакансий найденных по запросу '{query}': {quantity}")
        data_saver.save(vacancies)
        return True
    else:
        print(f"По запросу '{query}' ничего не найдено")
        return False
