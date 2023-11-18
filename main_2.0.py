# Variant 412939 % 36 = 19

def nesting_level(string):
    return len(string) - len(string.strip())

def block(string):
    block = ''
    flag = False
    for symb in string:
        if symb == '<':
            flag = True
        if symb == '>':
            block += symb
            break

        if flag:
            block += symb
    return block

with open('schedule.xml', 'r', encoding='utf-8') as fileXML:
    declarationXML = fileXML.readline()
    XML = fileXML.read()

stringsXML = XML.split('\n')
stringsJSON = []

for i in range(len(stringsXML)-1):
    string = stringsXML[i]
    #print(string)
    if '/' not in block(string):
        opening = block(string)
        closing = block(string)[0] + '/' + block(string)[1:]
        if (opening and closing) in string:
            newOpening = f'"{opening[1:-1]}"'
            if nesting_level(string) == nesting_level(stringsXML[i+1]):
                string = string.replace(opening, f'{newOpening}: "')
                newString = string.replace(closing, '",')
            else:
                string = string.replace(opening, f'{newOpening}: "')
                newString = string.replace(closing, '"')
        elif opening in string:
            newOpening = f'"{opening[1:-1]}"'
            newString = string.replace(opening, f'{newOpening}: {{')
    else:
        closing = block(string)
        if nesting_level(string) == nesting_level(stringsXML[i+1]) and nesting_level(string) != 0:
            newClosing = '},'
            newString = string.replace(closing,newClosing)
        else:
            newClosing = '}'
            newString = string.replace(closing, newClosing)
    stringsJSON.append(newString)
    if i == len(stringsXML)-1:
        string = stringsXML[i+1]
        closing = block(string)
        newClosing = '}'
        newString = string.replace(closing,newClosing)
        stringsJSON.append(newString)

JSON = '{\n'
for string in stringsJSON:
    JSON += f'\t{string}\n'
JSON = JSON + '}'

with open('schedule.json', 'w', encoding='utf-8') as fileJSON:
    fileJSON.write(JSON)
    #print("Перевод из XML в JSON выполнен успешно")
