import random

a = []
for i in range(1, 201):
    a.append(i / 2)
    #print(i/2)

print()
print("="*20)
print("="*20)
print()

sp_re = 75
s_re = 70

summ = 0
for j in range(10):
    s = 0
    for i in range(100):
        shanc = 0
        r = 10
        a = True
        while r >= 0.1:
            if round(s_re * (r - 0.1), 1) < round(s_re * r, 1) <= sp_re:
                #print(round(s_re * r, 1), sp_re)
                break
            r = round(r - 0.1, 1)
            shanc += a
            a = not a

        #print(shanc)
        rand = random.randint(1, 100)
        while shanc > 0:
            if rand == shanc:
                s += 1
                break
            shanc -= 1

    # print('-' * 10)
    # print(s)
    summ += s

print()
print('='*10)
print(summ / 10)

print('='*10)
print(4000//375)
print('='*10)

s = 0

for i in range(10):
    s = s + 1 if s < 3 else 0
    print(s)
