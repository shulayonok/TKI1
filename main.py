from termcolor import cprint
import random


# Перевод алфавита в кодировку ASCII
def alphabet_to_byte(alph):
    return " ".join(f"{ord(i.encode('cp1251')):08b}" for i in alph)


# Режим кодирования
def encoding(bytes):
    for i in range(len(bytes)):
        code = list(-1 for i in range(13))
        for j in range(len(discharges)):
            code[discharges[j]] = int(bytes[i][j])
        code[0] = code[2] ^ code[4] ^ code[6] ^ code[8] ^ code[10]
        code[1] = code[2] ^ code[5] ^ code[6] ^ code[9] ^ code[10]
        code[3] = code[4] ^ code[5] ^ code[6] ^ code[11]
        code[7] = code[8] ^ code[9] ^ code[10] ^ code[11]
        code[12] = 1 if sum(code[i] for i in range(12)) % 2 != 0 else 0
        bytes[i] = code


# Генерируем ошибки
def generate_error(bytes, errors=None):
    result = bytes
    if errors is None:
        errors = list([] for i in range(len(bytes)))
    for i in range(len(bytes)):
        rand = random.randint(0, 12)
        while rand in errors:
            rand = random.randint(0, 12)
        errors[i].append(rand)
        result[i][rand] = 1 if bytes[i][rand] == 0 else 0
    return result, errors


def generate_errors(bytes):
    bytes, errors = generate_error(bytes)
    return generate_error(bytes, errors)


# Режим декодирования
def decode(bytes):
    for byte in bytes:
        byte[0] = byte[2] ^ byte[4] ^ byte[6] ^ byte[8] ^ byte[10]
        byte[1] = byte[2] ^ byte[5] ^ byte[6] ^ byte[9] ^ byte[10]
        byte[3] = byte[4] ^ byte[5] ^ byte[6] ^ byte[11]
        byte[7] = byte[8] ^ byte[9] ^ byte[10] ^ byte[11]
        byte[12] = 1 if sum(byte[i] for i in range(12)) % 2 != 0 else 0


def printing(bytes):
    for byte in bytes:
        for i in range(len(byte)):
            if i in discharges:
                print(byte[i], end="")
            else:
                if i == 12:
                    cprint(byte[i], "green", end="")
                else:
                    cprint(byte[i], "yellow", end="")
        print()
    print()


def printitng_with_errors(bytes, errors):
    for i in range(len(bytes)):
        for j in range(13):
            if j in errors[i]:
                cprint(bytes[i][j], "red", end="")
                continue
            if j in discharges:
                print(bytes[i][j], end="")
            else:
                if j == 12:
                    cprint(bytes[i][j], "green", end="")
                else:
                    cprint(bytes[i][j], "yellow", end="")
        print()
    print()


alphabet = "РСТУФ"
discharges = [2, 4, 5, 6, 8, 9, 10, 11]

alphaBytes = alphabet_to_byte(alphabet).split(" ")
print("Вывод алфавита с кодировке win 1251")
print(alphaBytes)
print()

print("Кодирование")
encoding(alphaBytes)
printing(alphaBytes)

print("Декодирование с одной ошибкой")
anotherAlpha, errors = generate_error(alphaBytes)
printitng_with_errors(anotherAlpha, errors)
decode(anotherAlpha)
printing(anotherAlpha)

print("Декодирование с двумя ошибками")
alphaBytes, errors = generate_errors(alphaBytes)
printitng_with_errors(alphaBytes, errors)
decode(alphaBytes)
printing(alphaBytes)


