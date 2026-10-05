
# email = str(input("Введіть вашу пошту: "))

# if "@" in email:
#     domain = email.lower().split('@')[1]
#     main = email.lower().split('@')[0]
#     main = main.replace(main,"*" * len(main))
# print(f'Ваш домен: {main}@{domain}')

row = input("Введіть рядок з букв S,F: ").upper()


if not all(ch in ('S', 'F') for ch in row):
    print("Помилка: рядок повинен містити лише символи S та F")
else:
    max_len = 0
    max_start = -1

    cur_len = 0
    cur_start = -1


    for i, ch in enumerate(row):
        if ch == 'F':
            if cur_len == 0:
                cur_start = i + 1
            cur_len += 1


            if cur_len > max_len:
                max_len = cur_len
                max_start = cur_start
        else:
            cur_len = 0
            cur_start = -1

    print(f"довжина {max_len}; початок {max_start}")