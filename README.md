<div align="center">
<h1> Телефонный справочник </h1>
</div>

## About

Телефонный справочник представляет собой утилиту для хранения, вывода, занесения и изменения контактных данных сотрудников.
Интерфейс программы реализован через командную строку Django Shell. Фикстуры хранятся в файле contacts.json в корне проекта.

---
## Installation

### Application
Клонируйте репозиторий:
```
git clone git@github.com:amahmetov1998/phonebook.git
cd phonebook
```
Создайте виртуальное окружение:
```
make venv
```
Активируйте виртуальное окружение:
```
make activate
```
Установите зависимости:
```
make install
```
### Migrations
Создайте и примените миграции:
```
make migrate
```
### Fixtures
Загрузите данные в БД:
```
make load_data
```
## Usage
Запустите командную оболочку Django Shell:
```
make load_data
```
Импортируйте следующие функции:
```
from phonebook.views import add_contact, show_contacts, search_contact, update_contact
```
Описание основных функций:
#### add_contact
Функция принимает следующие обязательные параметры: фамилию, имя, отчество, название организации, телефон рабочий, телефон личный.
В случае если текущая организация в БД отсутствует, она создается. Введенные номера телефонов проходят простейшую валидацию.
Если все поля введены верно, в БД создается новая запись, а на экран выводится соответствующее сообщение.

#### show_contacts
Функция принимает один параметр: количество записей на страницу. Затем необходимо ввести номер необходимой страницы.
Полученные данные сортируются в алфавитном порядке.

#### search_contact
Функция принимает следующие параметры: фамилию, имя, отчество, название организации, телефон рабочий, телефон личный.
Можно искать записи как по одному, так и нескольким параметрам. Найденные записи выводятся на экран.
В случае отсутствия записей на экран будет выведено соответствующее сообщение.

#### update_contact
Функция принимает следующие параметры для поиска нужной записи: фамилию, имя, отчество, название организации, телефон рабочий, телефон личный.
Введенные данные передает функции поиска. Затем необходимо ввести новые данные.
В случае если найдено несколько контактов, необходимо выбрать один из них для редактирования.
Если все поля введены верно, данные обновляются, а на экран выводится соответствующее сообщение.