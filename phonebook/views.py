from typing import Union

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from prettytable import PrettyTable

from django.core.paginator import Paginator

from .models import Phonebook, Organization


def form_args(surname: str = None, name: str = None, middle_name: str = None, job: str = None,
              office_num: str = None, mobile_num: str = None) -> dict:

    """
    Формирует словарь данных для дальнейшего поиска/обновления записей.
    Вспомогательная функция для поиска и обновления записей телефонного справочника.
    """

    args = {}
    if name:
        args['name'] = name
    if surname:
        args['surname'] = surname
    if middle_name:
        args['middle_name'] = middle_name
    if job:
        args['organization__name'] = job
    if office_num:
        args['employee_phone_number'] = office_num
    if mobile_num:
        args['mobile_phone_number'] = mobile_num
    return args


def validate_number(value: str):

    """
    Валидирует номер телефона простейшим образом.
    """

    if not str(value).isdigit():
        raise ValidationError('Номер телефона должен состоять только из цифр')


def create_table(lst: QuerySet) -> PrettyTable:

    """
    Формирует таблицу для удобочитаемости данных.
    """

    table = PrettyTable()
    table.field_names = [
        "№", "Фамилия", "Имя", "Отчество", "Организация", "Рабочий номер телефона", "Личный номер телефона"
    ]
    for contact in lst:
        table.add_row([contact.id, contact.surname, contact.name, contact.middle_name, contact.organization.name,
                       contact.employee_phone_number, contact.mobile_phone_number])
    return table


def add_contact(surname: str = None, name: str = None, middle_name: str = None, job: str = None,
                office_num: str = None, mobile_num: str = None) -> None:

    """
    Добавляет данные контакта в телефонный справочник. Все параметры обязательны для заполнения.

    Атрибуты
    :param surname: Фамилия
    :param name: Имя
    :param middle_name: Отчество
    :param job: Место работы
    :param office_num: Рабочий номер
    :param mobile_num: Личный номер
    """

    if not (surname and name and middle_name and office_num and mobile_num and job):
        raise ValidationError('Все поля обязательны для заполнения')

    validate_number(office_num), validate_number(mobile_num)

    if not Organization.objects.filter(name=job).exists():
        Organization.objects.create(name=job)
    job = Organization.objects.get(name=job)

    Phonebook.objects.create(name=name, surname=surname, middle_name=middle_name, organization=job,
                             employee_phone_number=office_num, mobile_phone_number=mobile_num)
    print('Контакт успешно добавлен!')


def show_contacts(per_pages: str) -> PrettyTable:

    """
    Постранично выводит на экран записи из телефонного справочника.

    Атрибуты
    :param per_pages: Количество записей на страницу
    """

    contacts = Phonebook.objects.all().select_related('organization')
    paginator = Paginator(contacts, per_pages)

    print(f'Количество доступных страниц: {paginator.num_pages}')
    page_number = input('Введите номер страницы: ')

    page_obj = paginator.get_page(page_number)

    return create_table(page_obj)


def search_by_data(data: dict) -> QuerySet:

    """
    Производит поиск по введенным данным.
    Вспомогательная функция для поиска и обновления записей телефонного справочника.
    """

    return Phonebook.objects.filter(**data).select_related('organization')


def search_contact(surname: str = None, name: str = None, middle_name: str = None, job: str = None,
                   office_num: str = None, mobile_num: str = None) -> Union[PrettyTable, None]:

    """
    Формирует и передает данные для поиска в функцию search_by_data. Выводит на экран полученные данные.

    Атрибуты
    :param surname: Фамилия
    :param name: Имя
    :param middle_name: Отчество
    :param job: Место работы
    :param office_num: Рабочий номер
    :param mobile_num: Личный номер
    """

    args = form_args(surname, name, middle_name, job, office_num, mobile_num)

    queryset = search_by_data(args)
    if queryset.exists():
        return create_table(queryset)
    else:
        print('По данному запросу ничего не найдено')


def update(contact: QuerySet) -> QuerySet:

    """
    Редактирует записи по одному или нескольким полям.
    Вспомогательная функция для обновления записей телефонного справочника.
    """

    fields = {
        '1': ('surname', 'фамилию'),
        '2': ('name', 'имя'),
        '3': ('middle_name', 'отчество'),
        '4': ('organization', 'место работы'),
        '5': ('employee_phone_number', 'рабочий номер'),
        '6': ('mobile_phone_number', 'личный номер')
    }

    print('Список полей для редактирования: 1. Фамилия; 2. Имя; 3. Отчество; 4. Место работы; 5. Рабочий номер;'
          '6. Личный номер')
    nums = input('Введите номера полей для редактирования через пробел: ')
    new_data = {}
    for num in nums.split():
        new_data[fields[num][0]] = input(f'Введите {fields[num][1]}: ')

    if 'employee_phone_number' in new_data:
        validate_number(new_data['employee_phone_number'])

    if 'mobile_phone_number' in new_data:
        validate_number(new_data['mobile_phone_number'])

    if 'organization' in new_data:
        if not Organization.objects.filter(name=new_data['organization']).exists():
            new_data['organization'] = Organization.objects.create(name=new_data['organization'])
        else:
            new_data['organization'] = Organization.objects.get(name=new_data['organization'])

    contact.update(**new_data)
    print(type(contact))
    return contact


def update_contact(surname: str = None, name: str = None, middle_name: str = None, job: str = None,
                   office_num: str = None, mobile_num: str = None) -> Union[None, PrettyTable]:

    """
    Формирует и передает данные для поиска в функцию search_by_data, затем в функцию update для редактирования.
    В случае если найдено несколько контактов, необходимо выбрать один из них для редактирования.
    Выводит на экран обновленные данные.

    Атрибуты
    :param surname: Фамилия
    :param name: Имя
    :param middle_name: Отчество
    :param job: Место работы
    :param office_num: Рабочий номер
    :param mobile_num: Личный номер
    """

    args = form_args(surname, name, middle_name, job, office_num, mobile_num)
    queryset = search_by_data(args)
    if queryset.exists():
        if len(queryset) != 1:
            print(create_table(queryset))
            pk = input('По запросу найдено несколько контактов. Выберите один и введите его порядковый номер: ')
            if pk not in [str(contact.pk) for contact in queryset]:
                print('Неверный номер')
                return

            queryset = Phonebook.objects.filter(pk=pk)

        contact = update(queryset)
        print("Контакт успешно обновлен!")
        return create_table(contact)

    else:
        print('По данному запросу ничего не найдено')
