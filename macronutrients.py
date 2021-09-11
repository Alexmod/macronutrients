from itertools import combinations

import numpy as np

# Сами продукты, чем больше ввести тем больше вероятность,
# того, что найдутся нужные комбинации
data = {"Гречка": {"Белки": 11.7, "Жиры": 2.7, "Углеводы": 75},
        "Яйца": {"Белки": 12.7, "Жиры": 11.5, "Углеводы": 0.7},
        "Авокадо": {"Белки": 2, "Жиры": 15, "Углеводы": 9},
        "Оливковое масло": {"Белки": 0, "Жиры": 99.8, "Углеводы": 0}
        }

# Макронутриенты (БЖУ), которые нужно получить
neaded = [30, 25, 60]


def get_gramms(data, neaded):
    results = []
    # Разбиваем на всевозможные комбинации по 3 шт.
    for comb in combinations(data.keys(), 3):
        meals = [list(data[a].values()) for a in comb]
        # Инициация матрицы
        m = np.matrix(meals)
        # Обратная матрица
        m_inverse = np.linalg.inv(m)
        need = np.array(neaded)
        # Умножаем матрицу
        res = need.dot(m_inverse)
        if np.all(res > 0):
            # Отсекаем варианты с отрицательными значениями
            # Ведь нельзя съесть минус -20 гр. гречки
            res_list = res.tolist()[0]
            res_dict = {name: f'{int(100*res_list[i])} гр.'
                        for i, name in enumerate(comb)}
            results.append(res_dict)
    return results


print(get_gramms(data, neaded))
