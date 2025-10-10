import open_files

FALSE_STR = 'False'
TRUE_STR = 'True'

s_kast_scena = 0
kast_scena = TRUE_STR
state = 1


if s_kast_scena == 0:
    open_files.write_file(r'files/kast_scena.txt', [TRUE_STR, f'{s_kast_scena}'])
    open_files.write_file(r'files/NEW_GAME.txt', ['True'])
    open_files.write_file(r'files/settings.txt', ['Средний', '100', '100'])
    open_files.write_file(r'files/states.txt', [
        [False, False, False, False, False, False, False, False, False, False, False, False, False], False, False,
        False, 'Для передвижения нажимайте на клавиши "A" и "D", либо же на стрелки влево и вправо'
    ])
    open_files.write_csv_file(r'files/positions.csv', [
        ['Oyuun', -500, 200, 1]
    ], ['pers', 'center_x', 'center_y', 'storona'])
    open_files.write_csv_file(r'files/bosses.csv', [], ['pers', 'hp'])
elif s_kast_scena == 1:
    open_files.write_file(r'files/kast_scena.txt', [FALSE_STR, f'{s_kast_scena}'])
    open_files.write_file(r'files/NEW_GAME.txt', [FALSE_STR])
    open_files.write_file(r'files/settings.txt', ['Средний', '100', '100'])
    open_files.write_file(r'files/states.txt', [
        [False, False, False, False, False, False, False, False, False, False, False, False, False], False,
        False,
        False, 'Для передвижения нажимайте на клавиши "A" и "D", либо же на стрелки влево и вправо'
    ])
    open_files.write_csv_file(r'files/positions.csv', [
        ['Oyuun', 45, 191, 0]
    ], ['pers', 'center_x', 'center_y', 'storona'])
    open_files.write_csv_file(r'files/bosses.csv', [], ['pers', 'hp'])
elif s_kast_scena == 2:
    open_files.write_file(r'files/kast_scena.txt', [FALSE_STR, f'{s_kast_scena}'])
    open_files.write_file(r'files/NEW_GAME.txt', [FALSE_STR])
    open_files.write_file(r'files/settings.txt', ['Средний', '100', '100'])
    open_files.write_file(r'files/states.txt', [
        [True, True, True, True, True, False, False, False, False, False, False, False, False], False,
        False,
        False, 'Для передвижения нажимайте на клавиши "A" и "D", либо же на стрелки влево и вправо'
    ])
    open_files.write_csv_file(r'files/positions.csv', [
        ['Oyuun', 1052, 191, 0], ['Sinhelm', 1500, 191, 1], ['Bratislav', 4000, 191, 1], ['Rock', 14000, -150, 1]
    ], ['pers', 'center_x', 'center_y', 'storona'])
    open_files.write_csv_file(r'files/bosses.csv', [['Rock', 6100]], ['pers', 'hp'])
elif s_kast_scena == 3:
    open_files.write_file(r'files/kast_scena.txt', [FALSE_STR, f'{s_kast_scena}'])
    open_files.write_file(r'files/NEW_GAME.txt', [FALSE_STR])
    open_files.write_file(r'files/settings.txt', ['Средний', '100', '100'])
    open_files.write_file(r'files/states.txt', [
        [True, True, True, True, True, False, False, False, False, False, False, False, False], False,
        False,
        False, 'Для передвижения нажимайте на клавиши "A" и "D", либо же на стрелки влево и вправо'
    ])
    open_files.write_csv_file(r'files/positions.csv', [
        ['Oyuun', 3466, 192, 0], ['Sinhelm', -145, 192, 1], ['Bratislav', 4000, 192, 1], ['Rock', 14000, -150, 1]
    ], ['pers', 'center_x', 'center_y', 'storona'])
    open_files.write_csv_file(r'files/bosses.csv', [['Rock', 6100]], ['pers', 'hp'])
elif s_kast_scena == 4:
    open_files.write_file(r'files/kast_scena.txt', [FALSE_STR, f'{s_kast_scena}'])
    open_files.write_file(r'files/NEW_GAME.txt', [FALSE_STR])
    open_files.write_file(r'files/settings.txt', ['Средний', '100', '100'])
    open_files.write_file(r'files/states.txt', [
        [True, True, True, True, False, False, False, False, False, False, False, False, False], False,
        False,
        False, 'Нажмите на ПРОБЕЛ для нанесения обычных ударов'
    ])
    if state == 0:
        open_files.write_csv_file(r'files/positions.csv', [
            ['Oyuun', 12500, 192, 0], ['Sinhelm', -145, 192, 1], ['Bratislav', 12000, 192, 1], ['Rock', 14000, -150, 1]
        ], ['pers', 'center_x', 'center_y', 'storona'])
    else:
        open_files.write_csv_file(r'files/positions.csv', [
            ['Oyuun', 3900, 192, 0], ['Sinhelm', -145, 192, 1], ['Bratislav', 4000, 192, 1], ['Rock', 14000, -150, 1]
        ], ['pers', 'center_x', 'center_y', 'storona'])
    open_files.write_csv_file(r'files/bosses.csv', [['Rock', 6100]], ['pers', 'hp'])
elif s_kast_scena == 5:
    open_files.write_file(r'files/kast_scena.txt', [FALSE_STR, f'{s_kast_scena}'])
    open_files.write_file(r'files/NEW_GAME.txt', [FALSE_STR])
    open_files.write_file(r'files/settings.txt', ['Средний', '100', '100'])
    open_files.write_csv_file(r'files/positions.csv', [
        ['Oyuun', 13213, 192, 0], ['Sinhelm', -145, 192, 1], ['Bratislav', 12439, 192, 1], ['Rock', 14000, 384, 1]
    ], ['pers', 'center_x', 'center_y', 'storona'])
    if state == 0:
        open_files.write_file(r'files/states.txt', [
            [True, True, True, True, True, False, False, False, False, False, False, False, False],
            True,
            True,
            False,
            'Нажмите на ПРОБЕЛ для нанесения обычных ударов'
        ])
        open_files.write_csv_file(r'files/bosses.csv', [['Rock', 6100]], ['pers', 'hp'])
    else:
        open_files.write_file(r'files/states.txt', [
            [True, True, True, True, True, True, True, True, True, True, True, True, False],
            False,
            False,
            False,
            'Раскрошите эту скалу'
        ])
        open_files.write_csv_file(r'files/bosses.csv', [['Rock', 0]], ['pers', 'hp'])
elif s_kast_scena == 6:
    open_files.write_file(r'files/kast_scena.txt', [FALSE_STR, f'{s_kast_scena}'])
    open_files.write_file(r'files/NEW_GAME.txt', [FALSE_STR])
    open_files.write_file(r'files/settings.txt', ['Средний', '100', '100'])
    open_files.write_file(r'files/states.txt', [
        [True, True, True, True, True, True, True, True, True, True, True, True, False],
        True,
        False,
        False,
        'Сделайте двойное нажатие на A или левую стрелку'
    ])
    open_files.write_csv_file(r'files/positions.csv', [
        ['Oyuun', 11900, 192, 0], ['Sinhelm', 8644, 192, 1], ['Bratislav', 16813, 192, 1], ['Rock', 14000, 384, 1]
    ], ['pers', 'center_x', 'center_y', 'storona'])
    open_files.write_csv_file(r'files/bosses.csv', [['Rock', 0]], ['pers', 'hp'])

t = []
print(t)
open_files.read_file('tests/files/test1.txt', t)
print(t)

