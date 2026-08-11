>## **`PROJECT_RAZGROM`**
> Автоматизация сканирования внешнего периметра и исходного кода на базе Open Source утилит и собственных разработок.

>### Внешний периметр DAST
   - `Сбор активов периметра` Используются утилиты пассивного и активного скана для сбора информации о поддоменах, ip, портах.
   - `Сбор и анализ веб-контента` Поиск страниц и анализ их содержимого, определение используемых технологий, уязвимостей html, cookie, headers, js.
   - `Поиск уязвимостей` Выявление типовых уязвимостей веб-приложений, исходя из известных шаблонов атак.

>### Исходный код SAST/SCA
   - `Анализ исходного кода` - Обнаружение небезопасных паттернов и уязвимого кода.
   - `Сканирование цепочки зависимостей` - Определение версий библиотек и проверка на известные уязвимости CVE/BDU.
   - `Анализ IaC конфигурационных файлов` - Обнаружение небезопасных паттернов в конфигурационных файлах инфраструктуры.
   - `Поиск секретов` - Анализ исходного кода на наличие утечек конфиденциальных данных: API-ключи, токены доступа, пароли, приватные ключи и другие чувствительные артефакты, случайно оставленные в коде.

>### Архитектура
Система состоит из микро-сервисной архитектуры:
1. [Api Gateway (krakenD)](app/services/kraken_d/README.md)
2. [Основной сервис-контроллер (core_service)](app/services/core_service/README.md)
3. [Сервис работы с пользователями (auth_service)](app/services/auth_service/README.md)
4. [Сервис сбора скриншотов страниц (screenshot_service)](app/services/dast/screenshot_service/README.md)
5. [Сервис обертка над feroxbuster для сбора страниц (feroxbuster_service)](app/services/dast/feroxbuster_service/README.md)
6. [Сервис обертка над naabu для поиска открытых портов (naabu_service)](app/services/dast/naabu_service/README.md)
7. [Сервис обертка над dnsx для активного поиска поддоменов (dnsx_service)](app/services/dast/dnsx_service/README.md)
8. [Self Hosted S3 для хранения скриншотов страниц и правил для утилит (minio)](app/services/docker-compose.yaml#L269)
9. [Сервис обертка над nuclei для DAST анализа собранных активов (nuclei_service)](app/services/dast/nuclei_service/README.md)
10. [Сервис обертка над subfiender для пассивного поиска поддоменов (subfinder_service)](app/services/dast/subfinder_service/README.md)
11. [Сервис обертка над nmap для поиска открытых портов и анализа сервисов на них (nmap_service)](app/services/dast/nmap_service/README.md)
12. [Сервис обертка над katana для поиска ресурсов на домене: страницы/файлы/js/css и тд (katana_service)](app/services/dast/katana_service/README.md)
13. [Сервис обертка над httpx для сбора данных о странице: статус код, заголовок, тип/длина контента, технологии (httpx_service)](app/services/dast/httpx_service/README.md)
