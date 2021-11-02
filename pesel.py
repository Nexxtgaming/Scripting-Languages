PESEL_LENGTH = 11
PESEL_WEIGHT = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)


def valid_checksum(pesel):
    checksum = 0
    for i in range(PESEL_LENGTH - 1):
        checksum += PESEL_WEIGHT[i] * int(pesel[i])
    checksum = (10 - (checksum % 10)) % 10
    if checksum == int(pesel[10]):
        return True
    else:
        return False


def pesel_len(pesel):
    if len(pesel) != PESEL_LENGTH:
        return False
    return True


def sex(pesel):
    if int(pesel[9]) % 2 == 0:
        return True
    else:
        return False


def valid_date(pesel):
    month = pesel[2] + pesel[3]
    month_int = int(month)
    day = pesel[4] + pesel[5]
    long_months = (1, 3, 5, 7, 8, 10, 12)
    short_months = (4, 6, 9, 11)
    century = ("19", "20", "21", "22", "18")
    is_leap = False
    i = 0
    while month_int not in range(1, 13):
        month_int = month_int - 20
        if month_int <= 0:
            return False
        else:
            i += 1
    year = int(century[i] + pesel[0] + pesel[1])
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        is_leap = True
    if is_leap is True and month_int == 2 and int(day) not in range(1, 30):
        return False
    if month_int == 2 and int(day) not in range(1, 29) and is_leap is False:
        return False
    if month_int in long_months and int(day) not in range(1, 32):
        return False
    if month_int in short_months and int(day) not in range(1, 31):
        return False
    return True


total = correct = male = female = 0
invalid_length = invalid_digit = invalid_date = invalid_checksum = 0

file = open("1e6.dat", "r")

for pesel in file:
    pesel = pesel.strip()
    total += 1
    if pesel_len(pesel) is False:
        invalid_length += 1
    elif pesel.isdigit() is False:
        invalid_digit += 1
    elif valid_date(pesel) is False:
        invalid_date += 1
    elif valid_checksum(pesel) is False:
        invalid_checksum += 1
    else:
        correct += 1
        if sex(pesel) is True:
            female += 1
        else:
            male += 1


file.close()

print(total, correct, female, male)
print(invalid_length, invalid_digit, invalid_date, invalid_checksum)
