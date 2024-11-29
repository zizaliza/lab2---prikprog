from requests import RequestException
from regex_service import RegexService
from record_manager import JsonRecordRepository


def main():
    repository = JsonRecordRepository()
    service = RegexService(repository)

    while True:
        print("\nВыберите действие:")
        print("1. Получить дату из файла")
        print("2. Получить дату с веб-страницы")
        print("3. Найти дату в тексте")
        print("4. Выход")

        try:
            user_input = input("Введите номер действия: ").strip().lower()
            choice = int(user_input)

            match choice:
                case 1:
                    record = service.get_dates_in_file()
                        
                    print(f"Результат из файла: {record.date}")

                case 2:
                    url = input("Введите URL веб-страницы: ")
                    record = service.get_dates_in_web(url)

                    print(f"Результат с веб-страницы: {record.date}")

                case 3:
                    text = input("Введите текст: ")
                    dates_list = service.get_dates_in_text(text)

                    print(f"Результат из текста: {dates_list}")

                case 4:
                    print("Выход из программы.")
                    break

                case _:
                    print("Ошибка: выбрано недопустимое действие. Попробуйте снова.")

        except RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
        except KeyboardInterrupt:
            print("\nВыход из программы.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
