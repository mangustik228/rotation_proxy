

DESCRIPTION_MAIN = """
Сервис для ротации прокси. 

---

## 1.Авторизация

Для использования необходимо иметь **API-ключ** (спроси у Васи). Ключ необходим абсолютно для всех запросов.

Ключ необходимо вставить в headers запроса в поле "X-API-KEY".  

Пример **python**: 
```python 
import requests 

headers = {"X-API-KEY":"YOUR-KEY"}
response = requests.get("example.com", headers=headers)
``` 

---


## 2.Логика использования приложения: 

### Этап 1. Создание сервиса в бд (который собираемся парсить)

Для начала необходимо создать **Parsed_service** (если такого нет). Название сервиса для парсинга возможно произвольное (строка), единственное ограничение - должен отсутствовать символ "**_**"

1. Используем POST-запрос на адрес **/parsed_services** с телом {"name":"name_of_parsed_service"} 


2. Получаем в ответ id сервиса 

**p.s.** Возможно получить все возможные сервисы, обновить, получить по имени и т.п. (см. раздел [PARSED_SERVICES](#operations-tag-PARSED_SERVICES))

### Этап 2. Получение свободных прокси для парсера:

Получаем прокси GET-запросом [/proxies/rotations](#operations-tag-ROTATIONS) необходимое кол-во прокси (параметр `count`). 

- После получения прокси они будут заблокированы в пуле проксей на время указаное в переданном параметре `lock_time`, либо пока их принудительно не освободят (смотри Этап 3, Сценарий 1).


### Этап 3 

#### Сценарий 1. Удачно спарсили, прокси не нужны:

Для каждой прокси, которую хотим освободить, посылаем **/proxies/rotations/free/{id}**. В целом это делать необязательно, т.к. после истечения lock_time - прокси сама попадет в pool доступных проксей.

#### Сценарий 2. Прокси выдает ошибку, меняем: 

Посылаем PATCH запрос на адрес **/proxies/rotations**, указывая необходимые параметры. 
После получения данного запроса сервис разблокирует старую прокси для возврата ее в пул, но в то же время заблокирует конкретно для этого сервиса, с которым возникла ошибка, и сразу вернет новую прокси (если такая имеется).
 
Время блокировки прокси рассчитывается в зависимости от аргумента в параметрах `logic`, `ignore_hours`, `params`. см. Расчет времени блокировки

--- 

## 3. Расчет времени блокировки: 

При получение запроса на блокировку прокси (`PATCH /proxies/rotations`) сервис высчитывает насколько необходимо заблокировать прокси. 
Под капотом происходит следующее: 
- Получение прошлых блокировок (`last_blocks`), которые произошли за последние `ignore_hours` часов. Пример:
  - Сейчас **"2023-12-31T00:00:01"** 
  - Параметр ignore_hours указан 24 (часы, значение по умолчанию)
  - Прокси блокировалось ранее в: 
    1. **"2023-12-30T12:00:05"** на 20 минут
    2. **"2023-12-30T03:00:05"** на 15 минут
    3. **"2023-12-29T12:00:05"** на 13 минут
  - В результате, мы получаем список `last_blocks`: [("2023-12-30T12:00:05", 1200),("2023-12-30T03:00:05", 900)]
- Далее, в зависимости от указанной логики, вызывается соответствующая функция: 
- В функцию для расчета времени передается список `last_blocks` и словарь `params`
- Полученный результат рандомизируется +-15% 

### Функции расчета времени: 
#### Функция 1. `linear` 

В `params` передается только `base_time`(по умолчанию 600 секунд): 

- Возвращает `base_time` + "Кол-во прошлых блокировок" * `base_time`

- Пример, если `base_time` = 100 
  - Первая блокировка 100 (100 + 0*100) 
  - Вторая блокировка 200 (100 + 1*100)
  - Третья блокировка 300 (100 + 2*100)
  - Четвертая блокировка 400 (100 + 3*100)
  - * Допустим, слетела первая (прошло более 24 часов): 
  - Пятая блокировка 400 (100 + 3*100)


#### Функция 2. `sum_history`

В `params` передается только `base_time`(по умолчанию 600 секунд): 

Если `last_blocks` пустой: 
- Возвращает `base_time`

Если `last_blocks` не пустой: 
- Возвращает сумму "время блокировки" прошлых блокировок

- Пример, если `base_time`=100: 
  - Первая блокировка 100 (100 (base_time))
  - Вторая блокировка 100 (100)
  - Третья блокировка 200 (100 + 100)
  - Четвертая блокировка 400 (200 + 100 + 100)
  - * Допустим, слетела первая (прошло более 24 часов):
  - Пятая блокировка 700 (400 + 200 + 100)


---

## 4.Справка по методам
- PUT/PATCH/DELETE/POST запросы - параметры передаются в теле запроса
- GET запросы - параметры передаються в Query-string

---

## 5.Примечание по геолокации 

База данных выглядит следующим образом: 

|id|name|parent_id|
|--|--|--|
|1|'Russia'|Null|
|2|'Moscow'|1|
|3|'Saint-Peterburg'|1|
|4|'Germany'|Null|
p.s. Питера и Германии не было на момент написания. привел для примера.

- Если запросить прокси не указывая location_id - то получим все доступные прокси 
- Если запросить прокси указав location_id=1 , получим прокси, в которых location_id попадает в id - 1,2,3 
- Если запросить прокси указав location_id=2, то получим только прокси из Москвы.

"""
