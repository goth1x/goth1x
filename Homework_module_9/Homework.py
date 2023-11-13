def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            name = list(args)[0].split()[1]
            return f'You have no user {name.capitalize()} in contacts'
        except ValueError:
            return f'Give me name and phone please'
        except IndexError:
            return f'Enter user name'
    return wrapper


@input_error
def add(command):
    name, phone = command.lower().split()[1:]
    users[name] = phone
    return 'New contact was added'


def goodbye():
    print('Goodbye!')
    return


@input_error
def change(command):
    name, phone = command.lower().split()[1:]
    if name not in users:
        return f'You have no user {name.capitalize()} in contacts'
    users[name] = phone
    return 'Phone number was changed'


def hello():
    return 'How can I help you?'


def help():
    print('-'*100)
    print(f'{"Command":^25}|{"Action":^75}')
    print(f'{"Add ...":<25}| - add new user with phone to contact list. Where "..." is name and phone')
    print(f'{"Change ...":<25}| - change user phone number. Where "..." is name and phone')
    print(f'{"Good bye, Close, Exit":<25}| - end work with program')
    print(f'{"Hello":<25}| - greetings')
    print(f'{"Phone ...":<25}| - show phone number. Where "..." is name')
    print(f'{"Show all":<25}| - to see all saved contacts')
    print('-'*100)


def main(command):
    count = 0
    while True:
        action = command.lower().split()[0]
        if action == 'hello':
            print(hello())
        elif action == 'add':
            print(add(command))
        elif action == 'change':
            print(change(command))
        elif action == 'phone':
            print(phone(command))
        elif command.lower() == 'show all':
            show_all()
        elif action == 'help':
            help()
        elif command.lower() in ['close', 'exit', 'good bye', 'goodbye']:
            goodbye()
            break
        elif count > 2:
            print('Too much incorrect tries. Program will close immediately. Bye')
            break
        else:
            print('Unknown command, please try again. To see all commands type "HELP"')
            count += 1
        command = input()


@input_error
def phone(command):
    name = command.lower().split()[1]
    return f'Number for {name.capitalize()} is: {users[name]}'


def show_all():
    for name, phone in users.items():
        print(f'Contact name: {name.capitalize()}. Phone number: {phone}')
    return


users = {}


if __name__ == '__main__':
    main(input())
