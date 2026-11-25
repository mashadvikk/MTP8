# Лабораторная работа №8. Экосистемы Python, их использование

**Двикалюк Мария Викторовна, группа 220042-11, вариант 4, лабораторная №8**

Дисциплина «Методы и технологии программирования» (часть 1).

## Задания варианта 4

| Сложность | № | Задание | Где сделано |
|---|---|---|---|
| Средняя | 4 | Реализовать TDD для калькулятора | `tests/test_model.py`, `mvc_calc/model.py` |
| Средняя | 6 | Настроить flake8 | `.flake8` |
| Средняя | 10 | Описать архитектуру MVC для приложения | `docs/mvc.md` |
| Повышенная | 5 | Применить TDD к API | `tests/test_api.py`, `mvc_calc/api.py` |
| Повышенная | 9 | Создать свой пакет и опубликовать на TestPyPI | `pyproject.toml`, пакет `mashadvikk-calc` |

```bash
pip install -e ".[api,dev]"
python -m mvc_calc            # консольный калькулятор
python -m mvc_calc api        # REST API, http://127.0.0.1:8000/docs
python -m pytest
python -m flake8
```

## Средняя 4. TDD калькулятора

Каждый шаг — два коммита: тест, который ещё не проходит (red), и код,
после которого он проходит (green). Это видно в истории:

```
test: describe calculator behaviour (red)
feat: add expression calculator (green)
test: describe length limit and history (red)
feat: add length limit, history and ans (green)
```

Калькулятор понимает `+ - * / ^`, скобки, унарный знак, десятичную запятую
и слово `ans` — предыдущий результат. Выражение разбирает собственный
парсер, `eval` не используется.

```
$ python -m mvc_calc
Введите выражение или команду: история, очистить, выход
> 2+3*4
2+3*4 = 14
> ans/2
ans/2 = 7
> 1/0
Ошибка: деление на ноль
```

Проверить шаг red можно, вернувшись к его коммиту:
`git checkout <коммит>` и `python -m pytest`.

## Средняя 6. flake8

В `.flake8` заданы длина строки 79, сложность функции не больше 8 и
исключённые каталоги. Проверка кода замечаний не выдаёт.

## Средняя 10. Архитектура MVC

Описание, схема и пример прохождения запроса — в
[docs/mvc.md](docs/mvc.md).

## Повышенная 5. TDD для API

| Метод | Адрес | Действие | Ответы |
|---|---|---|---|
| POST | `/calculations` | вычислить выражение | 201, 400, 422 |
| GET | `/calculations` | история | 200 |
| DELETE | `/calculations` | очистить историю | 204 |

Тесты написаны до кода: `test: describe rest api (red)`, затем
`feat: add rest api (green)`.

## Повышенная 9. Пакет для TestPyPI

Пакет собирает `setuptools`, публикует `twine`:

```bash
python -m build
python -m twine check dist/*
python -m twine upload --repository testpypi dist/*
```

Установка опубликованного пакета:

```bash
pip install -i https://test.pypi.org/simple/ mashadvikk-calc
mvc-calc
```

## Тесты

```
$ python -m pytest -q
67 passed
```
