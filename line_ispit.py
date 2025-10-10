class AttitudeForChislo:
    def __init__(self, a: int or float):
        self.a = a
        self.attitude = 0
        self.dlina = 0

    def dlina_func(self, b):
        self.dlina = abs(self.a - b)

    def attitude_func(self, b):
        self.attitude = self.a / b


LINERGBA255 = tuple[AttitudeForChislo, AttitudeForChislo, AttitudeForChislo, AttitudeForChislo]


class StyleLine:
    def __init__(self, colors: dict[int: LINERGBA255, int: LINERGBA255, int: LINERGBA255, int: LINERGBA255],
                 max_znach: float):
        self.colors = colors
        self.max_znach = max_znach
        self.znach = 0

        def dlina(state1, state2):
            color = []
            for state in self.colors:
                for i in self.colors[state]:
                    if state == state1:
                        color.append(i.a)
                    elif state == state2:
                        for j in color:
                            if self.colors[state].index(i) == color.index(j):
                                i.dlina_func(j)

        def attitude():
            for state in self.colors:
                for i in self.colors[state]:
                    i.attitude_func(self.max_znach)

        color = []
        for state in self.colors:
            for i in self.colors[state]:
                if state == 1:
                    color.append(i.a)
        for state in self.colors:
            for i in self.colors[state]:
                if state == 0:
                    for j in color:
                        if self.colors[state].index(i) == color.index(j):
                            i.dlina_func(j)
        dlina(0, 1)
        dlina(1, 2)
        dlina(2, 3)
        dlina(3, 4)

        attitude()

        self.color = self.colors[1]

    def update(self, line_state, raznica, izmen):
        for state in self.colors:
            if state == line_state:
                self.color = self.colors[state]

        spis = []
        for i in self.color:
            if not izmen:
                i.a -= raznica * i.__attitude
            elif izmen:
                i.a += raznica * i.__attitude
            spis.append(i.a)

        print(spis)

    def print_color(self):
        # for state in self.colors:
        #     for a in self.colors[state]:
        #         print(a.a, state)
        #         print(a.dlina, state)
        #         print(a.attitude, state)

        for i in self.color:
            print(i.a, i.__attitude, i.__dlina)


colors = {0: (AttitudeForChislo(255), AttitudeForChislo(0), AttitudeForChislo(0), AttitudeForChislo(255)),
          1: (AttitudeForChislo(200), AttitudeForChislo(0), AttitudeForChislo(0), AttitudeForChislo(255)),
          2: (AttitudeForChislo(150), AttitudeForChislo(0), AttitudeForChislo(0), AttitudeForChislo(255)),
          3: (AttitudeForChislo(100), AttitudeForChislo(0), AttitudeForChislo(0), AttitudeForChislo(255)),
          4: (AttitudeForChislo(50), AttitudeForChislo(0), AttitudeForChislo(0), AttitudeForChislo(255))}

s_line = StyleLine(colors, 200)
s_line.print_color()

# s_line.update(1, 100, False)
# s_line.update(1, 12, False)
# s_line.update(1, 50, True)
# s_line.update(1, 34, False)
# s_line.update(1, 20, True)
