
a = int(input())
oper = input()
b = int(input())

if oper == '+':
    print(a + b)
elif oper == '-':
    print(a - b)
elif oper == '*':
    print(a * b)
elif oper == '/':
    if b != 0:
        print(a / b)
    elif b == 0:
        print('Деление на ноль')