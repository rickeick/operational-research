'''
# Fábrica de Plásticos

## Problema

Uma empresa fabrica malas, bolsas, pastas e sacolas de plástico. Ela compra sua matéria-prima em rolos com uma certa largura e corta em tiras adequadas a cada tipo de objeto produzido. Sabendo-se que
existem três tamanhos para cada item, as possibilidades de cortes estão resumidas na tabela abaixo:

| Corte   |   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| Malas   | P | 2 | 1 | – | 1 | – | – | – | – | 1 |
| Malas   | M | 1 | 2 | 1 | 1 | – | – | – | 3 | – |
| Malas   | G | 1 | – | – | – | – | 2 | 2 | – | – |
| Bolsas  | P | 2 | 1 | – | 2 | – | – | – | – | 1 |
| Bolsas  | M | 3 | – | 1 | 4 | 1 | 2 | – | 3 | – |
| Bolsas  | G | – | – | 1 | 1 | – | 2 | 2 | – | – |
| Pastas  | P | 6 | 4 | 2 | 1 | – | – | – | – | 1 |
| Pastas  | M | 1 | 1 | 1 | 1 | – | 2 | – | 4 | 1 |
| Pastas  | G | – | 2 | 1 | 1 | 2 | 2 | 3 | – | 1 |
| Sacolas | P | – | 2 | – | 1 | 2 | – | – | – | 1 |
| Sacolas | M | – | – | 2 | 1 | 2 | – | – | 2 | 1 |
| Sacolas | G | – | 1 | 1 | – | 2 | – | 3 | – | 1 |
| Perda   |   | 3 | 5 | 5 | 2 | 4 | 7 | 1 | 3 | 8 |

Em um determinado dia os pedidos para a fabricação são (pequeno, médio, grande):
malas: 10, 20, 13; bolsas: 5, 2, 6; pastas: 4, 3, 12; sacolas: 5, 5, 3.

Formular o problema de PL para minimizar as perdas de material.

## Modelo

Variáveis
- x_{j}: Quantidade de cortes do método j

Objetivo
- min f = sum_{j}(x_{j} * per_{j})

Restrição do Pedido p
- sum_{j}(x_{j} * L_{p,j}) >= p

Model += 
'''
import pulp
from itertools import product
from argparse import ArgumentParser
from json import load

# Argumentos
parser = ArgumentParser()
parser.add_argument('instancia', type=str, help='Instância do problema para executar')
args = parser.parse_args()

# Instância
with open(args.instancia, 'r', encoding='utf-8') as file:
    instancia = load(file)
itens = instancia['itens']
tamanhos = instancia['tamanhos']
cortes = range(instancia['cortes'])
tabela = instancia['tabela']
perdas = instancia['perdas']
pedido = instancia['pedido']

# Modelo
model = pulp.LpProblem("Fábrica_de_Plástico", pulp.LpMinimize)

# Variáveis
x = [pulp.LpVariable(f'x{j+1}', cat=pulp.LpInteger, lowBound=0) for j in cortes]

# Objetivos
model += pulp.lpSum([x[j] * perdas[j] for j in cortes])

# Restrições do Pedido
for item, tamanho in product(itens, tamanhos):
    p = item + tamanho
    model += pulp.lpSum([x[j] * tabela[p][j] for j in cortes]) >= pedido[p]

# Solução
model.solve(pulp.PULP_CBC_CMD(msg=False))

# Relatório
print('Relatório'.center(40, '='))
print(f'Status: {pulp.LpStatus[model.status]}'.center(40))
print(f'Objective: {model.objective.value()}'.center(40)+'\n')
print('Esquema de Cortes'.center(40, '='))
for var in x:
    print(f'{var.name}: {int(var.value())}'.center(40))
