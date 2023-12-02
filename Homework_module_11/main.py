from collections import UserDict
from datetime import datetime
from random import randint


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return str(self.value)
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    pass


class Phone(Field):
    def __init__ (self, phone):
        if self.validate(phone):
            super().__init__(phone)
        else:
            raise ValueError("Number must be 10 digits length")
        
    @staticmethod
    def validate(phone):
        return len(phone) == 10 and phone.isdigit()
    
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        value = str(value)
        if self.validate(value):
            self.__value = value

    def __repr__(self) -> str:
        return self.value


class Birthday(Field):
    def __init__ (self, birthday):
        self.__birthday = None
        self.birthday = birthday
        
    @staticmethod  
    def convert_date(birthday):
        return datetime.strptime(birthday, '%Y-%m-%d').date()  

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        if birthday:
            try:
                self.__birthday = self.convert_date(birthday)
            except ValueError: 
                print("Birthday must be in format 'YYYY-MM-DD'")
            except TypeError: 
                print("Birthday must be in format 'YYYY-MM-DD'")
        else:
            self.__birthday = None
                     
        
class Record:
    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone):
        self.phones.append(Phone(phone)) 
        
    def days_to_birthday(self):
        if self.birthday.birthday:
            today = datetime.today().date()                                                                                                                                                                   
            birthday_this_year = self.birthday.birthday.replace(year=datetime.today().year)
            if (birthday_this_year - today).days < 0:
                birthday_this_year = self.birthday.birthday.replace(datetime.today().year + 1)
            return f"{self.name} has birthday in {(birthday_this_year - datetime.today().date()).days} days"
        else:
            return f"We don't know when {self.name} has birthday"
        

    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(old_phone):
            for i, phone in enumerate(self.phones):
                if phone.value == old_phone:
                    self.phones[i] = Phone(new_phone)
        else:
            raise ValueError(f"Contact {self.name} don't has {old_phone} number")        
        
    def find_phone(self, value):  
        for phone in self.phones:
            if phone.value == value:
                return phone

    def remove_phone(self, phone):
        self.phones.remove(self.find_phone(phone))


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            
    def __str__(self) -> str:
        return str(self.data)

    def __iter__(self):
        return iter(self.data.values())

    def iterator(self, n):
        counter = 0
        result = ''
        for record in self.data.values():
            result += f"{record}\n"
            counter += 1
            if counter >= n:
                yield result
                counter = 0
                result = ''
        yield result
        
    
if __name__ == '__main__':

    book = AddressBook()
        

    john_record = Record("John", "2003-12-22")
    max_record = Record("Max", "1989-01-09")
    will_record = Record("Will")
    ban_record = Record("Ban")
    jane_record = Record("Jane")
    kenny_record = Record("Kenny", "1999-08-14")
    bond_record = Record("Bond" )
    mikel_record = Record("Mikel")
    billy_record = Record("Billy", "1958-04-02")
    hanna_record = Record("Hanna")
    ola_record = Record("Ola", "1973-05-12")
    iren_record = Record("Iren")
    nikela_record = Record("Nikela")
    kaladin_record = Record("Kaladin")

    nameslist = [john_record, max_record, will_record, ban_record, jane_record, kenny_record, bond_record, mikel_record, billy_record, hanna_record, ola_record, iren_record, nikela_record, kaladin_record]


    for name in nameslist:
        for i in range(randint(1, 4)):
            # Додавання телефону для ...
            name.add_phone(str(randint(1000000000, 9999999999)))
        # Додавання запису ... до адресної книги
        book.add_record(name)

    for i in range(2):
        print('\n')

    # Виведення всіх записів у книзі
    # for name, record in book.data.items():
    #     print(record)
    
    
    # # print(billy_record.phones)
    # billy_record.edit_phone(str(billy_record.phones[0]), "1112223333")

    
    # Пошук конкретного телефону у записі John
    # found_phone = billy_record.find_phone("1112223333")
    
    # print(f"{billy_record.name}: {found_phone}")  # Виведення: 1112223333
    
    # print(billy_record)
    # Видалення запису Jane
    book.delete("Jane")
    
    # Перевіряємо чи видалено запис Jane
    # for name, record in book.data.items():
    #     print(record)

    
    # AddressBook реалізує метод iterator, який повертає генератор за записами AddressBook і за одну ітерацію повертає уявлення для N записів.
    for contact in book.iterator(3):
        print(contact)
    
    # # Виведення всіх записів днів народження у книзі 
    for name, record in book.data.items():
        print(record.days_to_birthday())