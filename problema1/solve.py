'''
# Compra de Aviões da VAB

## Problema

A Viação Aérea Brasileira está estudando a compra de três tipos de aviões: Boeing 717 para as pontes
aéreas de curta distância, Boeing 737-500 para voos domésticos e internacionais de média distância e
MD-11 para voos internacionais de longa distância. Em um estudo preliminar, considerou-se que a capacidade
máxima dos aviões a serem comprados será sempre preenchida para efeito de planejamento.
Os dados de planejamento constam da Tabela abaixo:

| Tipo do Avião  | Custo | Receita Teórica | Pilotos Aptos |
| BOEING 717     |  5,1  |       330       |       30      |
| BOEING 737-500 |  3,6  |       300       |       20      |
| MD-11          |  6,8  |       420       |       10      |

A verba disponível para as compras é de 220 milhões de dólares. Os pilotos de MD-11 podem pilotar
todos os aviões da empresa, mas os demais pilotos só podem ser escalados às aeronaves a que foram
habilitados. Cada aeronave necessita de dois pilotos para operar. As oficinas de manutenção podem
suportar até 40 Boeings 717. Um Boeing 737-500 equivale, em esforço de manutenção, a 3/4, e um
MD-11 a 5/3, quando referidos ao Boeing 717. Formular o modelo de PL do problema de otimizar as
aquisições de aviões.

## Modelo

Variáveis
- x1: Número de BOEING 717
- x2: Número de BOEING 737-500
- x3: Número de MD-11
- p1: Pilotos de MD-11 para BOEING 717
- p2: Pilotos de MD-11 para BOEING 737-500
- p3: Pilotos de MD-11 para MD-11

Objetivo
- max f(x1, x2, x3) = (330-5.1)*x1 + (200-3.6)*x2 + (420-6.8)*x3

Restrições
- Custo:
    - 5.1*x1 + 3.6*x2 + 6.8*x3 <= 220
- Pilotos:
    - p1 + p2 + p3 <= 10
    - x1 <= (30 + p1)/2
    - x2 <= (20 + p2)/2
    - x3 <= p3/2
- Manutenção:
    - x1 + (3/4)*x2 + (5/3)*x3 <= 40
'''
import pulp
from argparse import ArgumentParser
from json import load

# Argumentos
parser = ArgumentParser()
parser.add_argument('instancia', type=str, help='Instância do problema para executar')
args = parser.parse_args()

# Instância
with open(args.instancia, 'r', encoding='utf-8') as file:
    instancia = load(file)
C = instancia['custos']
R = instancia['receitas']
P = instancia['pilotos']
V = instancia['verba']

# Modelo
model = pulp.LpProblem("Compra_de_Avioes", pulp.LpMaximize)

# Variáveis
x1 = pulp.LpVariable('Boeing_717', cat=pulp.LpInteger, lowBound=0)
x2 = pulp.LpVariable('Boeing_737', cat=pulp.LpInteger, lowBound=0)
x3 = pulp.LpVariable('MD_11', cat=pulp.LpInteger, lowBound=0)

# Pilotos de MD-11
p1 = pulp.LpVariable('Pilotos_para_B717', cat=pulp.LpInteger, lowBound=0)
p2 = pulp.LpVariable('Pilotos_para_B737', cat=pulp.LpInteger, lowBound=0)
p3 = pulp.LpVariable('Pilotos_para_MD11', cat=pulp.LpInteger, lowBound=0)

# Objetivo
model += ((R[0]-C[0])*x1 + (R[1]-C[1])*x2 + (R[2]-C[2])*x3, 'Maximizar_Lucro')

# Restrição de Custo
model += (C[0]*x1 + C[1]*x2 + C[2]*x3 <= V, 'Gasto_por_Avião')

# Restrições de Pilotos
model += (p1 + p2 + p3 <= P[2], 'Total_Pilotos_MD11')
model += (x1 <= (P[0]+p1)/2, 'Pilotos_MD11_para_B717')
model += (x2 <= (P[1]+p2)/2, 'Pilotos_MD11_para_B737')
model += (x3 <= p3/2, 'Pilotos_MD11_para_MD11')

# Restrição de Manutenção
model += (x1 + (3/4)*x2 + (5/3)*x3 <= 40, 'Capacidade_Manutenção')

# Solução
model.solve(pulp.PULP_CBC_CMD(msg=False))

# Relatório
print('Relatório'.center(40, '='))
print(f'Status: {pulp.LpStatus[model.status]}'.center(40))
print(f'Objective: {abs(model.objective.value()):.1f}'.center(40)+'\n')
print('Aviões para Comprar'.center(40, '='))
print(f'Boeing 717: {int(x1.value())}'.center(40))
print(f'Boeing 737 500: {int(x2.value())}'.center(40))
print(f'MD-11: {int(x3.value())}'.center(40)+'\n')
print('Alocação de Pilotos MD-11'.center(40, '='))
print(f'Boeing 717: {int(p1.value())}'.center(40))
print(f'Boeing 737 500: {int(p2.value())}'.center(40))
print(f'MD-11: {int(p3.value())}'.center(40))
