# Сервис ротации прокси 

## 

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
