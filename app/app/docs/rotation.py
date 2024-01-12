DESCRIPTION_CHANGE_WITHOUT_ERROR = """
Поменять прокси. 
Главное отличие от `PATCH /proxies/rotations` в том что прокси не будет заблокирована для этого сервиса, а просто освбодиться и может быть выдана опять через несколько запросов.

"""

DESCRIPTION_FREE_PROXY = """Освобождает прокси. Убирает прокси из "занятых", если в данный момент она занята"""

DESCRIPTION_GET_AVAILABLE = """
Получить свободные прокси, эти прокси не будут выдаваться другим сервисам в течение `lock_time`, либо пока не будут "Освобождены". Описание передаваемых параметров:     
- `parsed_service_id`: id сервиса, для которого необходимо выдать прокси. Если не существует, то необходимо предварительно создать (POST /parsed_services) (см. документацию).     
- `parsed_service`: Название сервиса, указывать не обязательно, но предпочтительно.    
- `count`: Количество прокси, которое необходимо выдать.
- `location_id`: Геолокация прокси. **Можно не указывать**. По умолчанию не проверяет. (см. Примечание по геолокации)
- `type_id`: Тип прокси. **Можно не указывать**. По умолчанию 1 - соответствет 'IPv4'(Индивидуальные),  На момент создания сервиса других типов прокси пока не используется.
- `lock_time`: Количество секунд, на которое будет заблокировано прокси и не будет выдаваться для других парсеров. По умолчанию - 300.
- `expire_proxy`: По умолчанию выдаются прокси, которые "живые" в момент запроса. В специфичных случаях: например, небходимо быть уверенным, что прокси будет работать до определенного времени, тогда можно указать время в строковом формате: "2023-12-31T12:00:00".
    """

DESCRIPTION_PATCH_PROXY = """
Поменять прокси, если используемая прокси выдала ошибка.  
Необходимо воспользоваться этим методом, выслав "плохую" прокси, указав время блокировки, 
взамен получить новую. Описание передаваемых параметров:

- `proxy_id`: id прокси, которое необходимо изменить.
- `parsed_service_id`: id сервиса, для которого необходимо выдать прокси. Если не существует, то необходимо предварительно создать (POST /parsed_services) (см. документацию).
- `parsed_service`: Название сервиса указывать не обязательно, но предпочтительно.
- `expire_proxy`: По умолчанию выдаются прокси, которые "живые" в момент запроса. В специфичных случаях: например, небходимо быть уверенным, что прокси будет работать до определенного времени, тогда можно указать время в строковом формате: "2023-12-31T12:00:00".
- `location_id`: Геолокация прокси. **Можно не указывать**. По умолчанию не проверяет. (см. Примечание по геолокации)
- `type_id`: Тип прокси. **Можно не указывать**. По умолчанию 1 - соответствет 'IPv4'(Индивидуальные).  На момент создания сервиса других типов прокси пока не используется.
- `lock_time`: Количество секунд, на которое будет заблокировано прокси и не будет выдаваться для других парсеров. По умолчанию - 300. 
- `logic`: Логика расчета времени для блокировки конкретно для этого сервиса. По умолчанию "linear". Другие варианты (см. Расчет времени блокировки).
- `reason`: Причина, по которой прокси была заблокирована. **УКАЗЫВАТЬ ОБЯЗАТЕЛЬНО**. 
- `params`: Словарь с параметрами, которые можно передать в функцию расчета времени. (см. описание соответствующих функций в разделе "Функции расчета времени").
- `ignore_hours`: Количество часов. Если есть ошибки с данной прокси для указанного парсящегося сервиса(`parsed_service_id`), то при расчёте времени будут учитываться только ошибки, возникшие за последние (`ignore_hours`) часов. Если непонятно, пишите - попытаюсь объяснить. По умолчанию - 24 часа, параметр важный. 
"""
