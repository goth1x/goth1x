from collections import UserDict
from datetime import datetime
from random import randint
import csv


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
    def __init__ (self, name):
        super().__init__(name)
        
    @Field.value.setter
    def value(self, name):    
        if isinstance(name, str) and len(name) > 1 and name.isalpha():
            self._Field__value = name
        else:
            raise ValueError("Incorrect name. Name must be more than 2 letters without digits")


class Phone(Field):
    def __init__ (self, phone):
        if self.validate(phone):
            super().__init__(phone)
        else:
            raise ValueError("Number must be 10 digits length")
        
    @staticmethod
    def validate(phone):
        return len(phone) == 10 and phone.isdigit()
    

    @Field.value.setter
    def value(self, value):
        value = str(value)
        if self.validate(value):
            self._Field__value = value

    def __repr__(self) -> str:
        return self.value


class Birthday(Field):
    def __init__ (self, birthday):
        super().__init__(birthday)
        
    @staticmethod  
    def convert_date(birthday):
        return datetime.strptime(birthday, '%Y-%m-%d').date()  

    @Field.value.setter
    def value(self, birthday):
        if birthday:
            try:
                self._Field__value = self.convert_date(birthday)
            except ValueError: 
                print("Birthday must be in format 'YYYY-MM-DD'")
            except TypeError: 
                print("Birthday must be in format 'YYYY-MM-DD'")
        else:
            self._Field__value = None
                     
        
class Record:
    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def __str__(self):
        if str(self.birthday) == "None":
            return f"Contact name: {self.name.value:<15}phones: {'; '.join(p.value for p in self.phones):<40}"
        else:
            return f"Contact name: {self.name.value:<15}phones: {'; '.join(p.value for p in self.phones):<40}birthday: {self.birthday}"

    def add_phone(self, phone):
        self.phones.append(Phone(phone)) 
        
    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.today().date()                                                                                                                                                                   
            birthday_this_year = self.birthday.value.replace(year=datetime.today().year)
            if (birthday_this_year - today).days < 0:
                birthday_this_year = self.birthday.value.replace(datetime.today().year + 1)
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
        
        
    def write_contacts_to_file(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "phone", "birthday"])
            writer.writeheader()
            for item in self.data.items():
                writer.writerow({"name":item[1].name, "phone":f"{';'.join(item.value for item in item[1].phones)}", "birthday":item[1].birthday})
    

    def read_contacts_from_file(self, filename):
        with open(filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row["name"]
                phones = row["phone"].split(';')
                birthday = row["birthday"]
                if birthday == "None":
                    birthday = None
                record = Record(name, birthday)
                for phone in phones:
                    record.add_phone(phone)
                self.add_record(record)
    
    def find_info(self, value):
        flag = 1
        for item in self.data.items():
            if value in str([item[1].name.value, item[1].phones, str(item[1].birthday.value)]):
                flag = 0
                print(f"Contact name: {item[1].name.value}, phones: {'; '.join(p.value for p in item[1].phones)}", f", birthday: {str(item[1].birthday.value)}" if str(item[1].birthday.value) != "None" else "", sep = "")
        if flag:
            print("No matches found")
                
    



if __name__ == '__main__':
    
    book = AddressBook()
    
    book.read_contacts_from_file("contacts.csv") #Зчитування с файлу

    


    # monika_record = Record("Monika", "1970-02-12")
    # monika_record.add_phone("7777711111")
    # monika_record.add_phone("2222244444")
    # book.add_record(monika_record)
    

    # AddressBook реалізує метод iterator, який повертає генератор за записами AddressBook і за одну ітерацію повертає уявлення для N записів.
    for contact in book.iterator(3):
        print(contact)

    
    book.find_info(input("Type to find contact by Name or Number: "))
       
    
    
    
    
    
  
    
    # Виведення всіх записів днів народження у книзі 
    # for name, record in book.data.items():
    #     print(record.days_to_birthday())
   
        
    book.write_contacts_to_file("contacts.csv") #Запис у файл csv