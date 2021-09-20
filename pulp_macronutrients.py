import pulp as pl


data = {
    'Картошка фри': {'Б': 3.4, 'Ж': 15,  'У': 41},
    'Котлета': {'Б': 14.1, 'Ж': 15.7, 'У':      6.6},
    'Хлеб': {'Б': 8.8, 'Ж': 3.3, 'У':  46.7},
    'Помидор': {'Б': 1.1,  'Ж': 0.2, 'У': 3.8},
    'Молочный коктейль': {'Б': 6, 'Ж': 5, 'У': 45},
    'Огурец': {'Б': 0.8, 'Ж': 0.1, 'У': 2.5},
}


# Макронутриенты (БЖУ), которые нужно получить
neaded = {'Б': 30, 'Ж': 25, 'У': 60}

# Минимум 10 гр. надо съесть, иначе может посчитать с нулями
# Можно задать для каждого продукта отдельно
MIN = 0.1
# Максимум 150 гр.
MAX = 1.5


prob = pl.LpProblem("The Nutrients Problem", pl.LpMinimize)
# Создаем переменные для каждого продукта
food = pl.LpVariable.dicts('Food', data, MIN, MAX)
for nutrient in list('БЖУ'):
    # Для бел., жиров и угл. создаем условия
    prob += pl.lpSum([data[k][nutrient] * food[k]
                      for k in data]) == neaded[nutrient]

prob.writeLP("Nutrients.lp")
prob.solve()

# Нельзя съесть -минус 10 гр. огурцов. Значит решения нет, если есть хоть 1
# отрицательное значение
if any((v.varValue or 0) < 0 for v in prob.variables()) is False:
    for v in prob.variables():
        if not v.varValue:
            continue
        name = v.name.replace('Food_', '')
        weight = int(v.varValue*100)
        print(f'{name}: {weight} гр.')
