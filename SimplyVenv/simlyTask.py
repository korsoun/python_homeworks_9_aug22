# Создать программу для игры в крестики-нолики, добавить виртуальное окружение.

import random
import pyjokes #VENV
 # Для вывода игрового поля.
def print_field (field):
    print(field[0], field[1], field[2])
    print(field[3], field[4], field[5])
    print(field[6], field[7], field[8])

# Подготовка.
print('============================== К Р Е С Т И К И - Н О Л И К И ==============================')
print()
print('Чтобы ставить крестик или нолик, вводите номер нужной клетки:')
example_field = [' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ', ' 9 ']
print_field(example_field)
print()
player1_name = input('Введите имя первого игрока -> ')
player2_name = input('Введите имя второго игрока -> ')
print()
player1_mark = player2_mark = ''
code_mark = input(f'Игрок {player1_name}, чем играешь?\n1 - крестиками\n2 - ноликами -> ')
if code_mark == '1':
    print(f'Игрок {player1_name} играет крестиками.')
    player1_mark = ' X '
    print(f'Игрок {player2_name} играет ноликами.')
    player2_mark = ' O '
else:
    print(f'Игрок {player1_name} играет ноликами.')
    player1_mark = ' O '
    print(f'Игрок {player2_name} играет крестиками.')
    player2_mark = ' X '
print()
whose_step = random.randint(1, 2)
if whose_step == 1:
    print(f'По жеребьевке начинает игрок {player1_name}!')
else:
    print(f'По жеребьевке начинает игрок {player2_name}!')
print()

# Ход игры.
iswinner = False
remain_steps = {1, 2, 3, 4, 5, 6, 7, 8, 9}
field = [' . ', ' . ', ' . ', ' . ', ' . ', ' . ', ' . ', ' . ', ' . ']
# Пока не определен победитель или есть возможность сделать ход.
while (iswinner == False) and (len(remain_steps) > 0):
    print_field(field)
    choise = None
    # Проверка на допустимость хода
    while not choise in remain_steps:
        choise = int(input(f'Ход игрока {player1_name if whose_step == 1 else player2_name} . Какую клетку выбираешь? -> '))
    # Если выбрана допустимая позиция, она заполняется меткой соответствующего игрока.
    field[choise - 1] = player1_mark if whose_step == 1 else player2_mark
    
    # Страшная проверка на ситуацию, когда победитель определен.
    if field[2] == field[5] == field[8] == player2_mark or field[1] == field[4] == field[7] == player2_mark or field[0] == field[3] == field[6] == player2_mark:
        iswinner = True
    if field[6] == field[7] == field[8] == player2_mark or field[3] == field[4] == field[5] == player2_mark or field[0] == field[1] == field[2] == player2_mark:
        iswinner = True
    if field[6] == field[4] == field[2] == player2_mark or field[0] == field[4] == field[8] == player2_mark:
        iswinner = True
    if field[2] == field[5] == field[8] == player1_mark or field[1] == field[4] == field[7] == player1_mark or field[0] == field[3] == field[6] == player1_mark:
        iswinner = True
    if field[6] == field[7] == field[8] == player1_mark or field[3] == field[4] == field[5] == player1_mark or field[0] == field[1] == field[2] == player1_mark:
        iswinner = True
    if field[6] == field[4] == field[2] == player1_mark or field[0] == field[4] == field[8] == player1_mark:
        iswinner = True
    # Смена очередности хода.
    print(iswinner)
    whose_step = 1 if whose_step == 2 else 2
    remain_steps.discard(choise)

# Объявление победителя.
if iswinner == 1:
    print()
    print(f'==================== Игрок {player1_name if whose_step == 2 else player2_name} победил! ====================')
    print_field(field)
    print()
    print('Хотите шутку?')
    print(pyjokes.get_joke()) #VENV
# Объявление ничьи.
if len(remain_steps) == 0 and iswinner == 0:
    print()
    print('================================================== Ничья! ==================================================')
    print_field(field)
    print()
    print('Хотите шутку?')
    print(pyjokes.get_joke()) #VENV