from json import dump

instancia = {
    'custos': [5.1, 3.6, 6.8],
    'receitas': [330, 300, 420],
    'pilotos': [30, 20, 10],
    'verba': 400
}

with open('inst.json', 'w', encoding='utf-8') as file:
    dump(instancia, file, ensure_ascii=False, indent=4)
