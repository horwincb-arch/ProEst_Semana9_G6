stack = []


def push(item):
    if not is_full(capacity):
        stack.append(item)
        return "Elemento apilado"
    return "La Pila esta llena"


def isEmpty():
    return not len(stack)

def is_full(capacity):
    return len(stack) == capacity

def peek():
    if not isEmpty():
        return stack[-1]
    return "Pila  vacia"

def pop_stack():
    if not isEmpty():
        return stack.pop()
    return "La pila esta vacia"

def show():
    message = ""
    for item in reversed(stack):
        message += f"| {item :6} |\n"
        message += f"└" + "─" + ""
capacity = int(input("Dime el tamaño de la pila: "))
while True:
    item = input("Dime un valor: ")
    answer = input("Desea ingresar otro dato [S / N]: ")
    if answer.lower() == "n":
        break

print('Mostrar tope')
print(peek())
print(peek())

print("Desapilar")
while True:
    answer = input("Desea desapilar [S | N]: ")
    if answer.lower() == "s":
        print(pop_stack())
    elif answer.lower() == "n":
        break
    else:
        print("Opcion invalida.....")