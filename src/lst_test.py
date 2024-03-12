d = []

d.append(123)
d.append(23)
d.append(45)
d.append(66)
d.append(77)

d.append((23, 45))

print(*d)

for el in d:
    print(el)

if 23 in d:
    print("Hello")

if 23 not in d:
    print("Bad")
else:
    print("You-hu")

