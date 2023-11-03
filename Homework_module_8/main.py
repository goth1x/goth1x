from datetime import date, datetime


def get_birthdays_per_week(users):
    days = ('Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday')
    birthday_boy = {}
    shift = date.today().weekday()
    if len(users) < 1:
        return birthday_boy

    for user in users:
        birthday = user.get('birthday').replace(date.today().year)
        if (birthday - date.today()).days < 0:
            birthday = user.get('birthday').replace(date.today().year + 1)
        dimention = (birthday - date.today()).days
        dimention_shift = (dimention + shift) % 7
        if 0 <= dimention <= 6:
            if (dimention_shift == 6 or dimention_shift == 5) and date.today().weekday() != 0:
                dimention_shift = 0
            try:
                birthday_boy[days[dimention_shift]
                             ] += [user.get('name').split()[0]]
            except KeyError:
                birthday_boy[days[dimention_shift]] = [
                    user.get('name').split()[0]]
    return birthday_boy


if __name__ == "__main__":

    users = [
        {"name": "Tom Hanks", "birthday": datetime(1967, 11, 5).date()},
        {"name": "Jim Carrey", "birthday": datetime(1958, 11, 6).date()},
        {"name": "Will Smith", "birthday": datetime(1994, 11, 7).date()},
        {"name": "Elon Musk", "birthday": datetime(2005, 11, 8).date()},
        {"name": "Jet Li", "birthday": datetime(1968, 11, 1).date()},
        {"name": "Van Damme", "birthday": datetime(1973, 11, 2).date()},
        {"name": "Jackie Chan", "birthday": datetime(1952, 11, 3).date()},
        {"name": "Bruce Willis", "birthday": datetime(1976, 11, 4).date()}
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
