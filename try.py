list1 = {
        "name" : "ergrtjtuktgrf",
        "range" : "automisation",
        "department" : "biggest room"
}
lines = []
with open('info1.txt', 'r') as file:
    content = file.readlines()
    if list1['name'] in content:
        pass
    else:
        lines.append(list1)

print(lines)