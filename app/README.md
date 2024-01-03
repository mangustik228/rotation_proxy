# Сервис ротации прокси 

## Добавление логики расчёта времени блокировки

Допустим хотим добавть метод расчета `some_func`
1. Добавляем в переменную logic название функции
`app/schemas/_proxies_rotation.py::_proxies_rotation.PatchRequestAvailableProxy`

```python 
class PatchRequestAvailableProxy(BaseModel): 
    ... 
    logic: Literal["sum_history", "linear", "some_func"]

```

2. Создаем класс в котором указываем базовые значения и параметры в `app/schemas/_calculators.py`:

```python 
class SomeCalc(BaseModel): 
    param1: int = 100 
    param2: int = 300 
```

3. Добавляем одноименный метод в класс `CalculateDelay` в (`app/services/calculate_delay.py`)

```python 
class CalculateDelay: 
    ... 
    def some_func(self): 
        params = S.SomeCalc(**self.params)
        ... # Реализуем логику
```

## Тестирование 
Тесты запускаються только в докер-контейнере. Чтоб запустились, необходимо создать вручную базу данных `test_proxies`. Без нее будет ошибка. Для запуска тестов, необходимо поднять контейнеры с redis и postgres, а также контейнер web_dev.


### pytest (Запуск тестов)

```python 
# Запуск тестов
docker compose exec web_dev pytest 
```

### coverage (Генерация отчета)
Для получения отчета о покрытии тестами можно воспользоваться утилитой coverage
```bash
# Заходим в контейнер
docker compose exec web_dev /bin/bash 

# Устанавливаем .coverage(Отсутствует в requirements.txt)
pip install coverage pytest-cov

# Запускаем тесты с помощью coverege 
coverage run -m pytest 

# Экспортируем отчет
coverage report -m --format=text > coverage-report.txt
``` 





















---

created: 2023-09-17 05:58
author: Vasiliy_mangust228
email: <a href="mailto:bacek.mangust@gmail.com">bacek.mangust@gmail.com</a>
tg: https://t.me/mangusik228
