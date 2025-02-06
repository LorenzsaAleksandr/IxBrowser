# 🚀 Автоматическое создание профилей в IXBrowser

Этот скрипт на Python автоматизирует процесс создания профилей в IXBrowser с заданными настройками. Он использует локальное API IXBrowser для:
- Получения списка групп 📋
- Поиска нужной группы по имени 🔍
- Создания профилей с индивидуальными настройками, включая параметры браузера, прокси и отпечатка (fingerprint) 🖥️

## Оглавление

- [Особенности](#особенности)
- [Установка](#установка)
- [Настройка](#настройка)
- [Запуск](#запуск)
- [Структура кода](#структура-кода)
- [Лицензия](License) 

## Особенности

- **Гибкость настройки:** Можно задать имя группы, количество профилей, префикс имени профиля, URL и другие параметры.
- **Настройки профиля:** Возможность отключения инфо-страницы с IP, отключения звука, резервного копирования, множественного открытия и указания стартовой страницы.
- **Настройки отпечатка (Fingerprint):** Задает параметры, необходимые для имитации браузерного отпечатка, например, язык.
- **Логирование:** Используется библиотека `loguru` для удобного логирования процесса создания профилей 📜.

## Установка

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository

2. **Создайте и активируйте виртуальное окружение (опционально):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/MacOS
   venv\Scripts\activate     # Для Windows

3. **Установите необходимые зависимости:**

   ```bash
   pip install loguru ixbrowser_local_api

## Настройка
**Перед запуском скрипта отредактируйте файл и измените следующие переменные в соответствии с вашими требованиями:**

- **profile_group_name** — имя группы, в которой будут создаваться профили.
- **number_of_profiles** — количество профилей для создания.
- **profile_name_prefix** — префикс, который будет использоваться при формировании имени профиля.
- **site_url** — URL, который будет открыт в каждом профиле.
Параметры в секции Настройки профиля:
- **pref_load_profile_info_page** — отключает инфо-страницу с IP.
- **0** — инфо-страница не отображается ❌.
- **1** — инфо-страница отображается ✅.
- **pref_block_audio** — отключает звук.
- **0** — звук включен 🔊.
- **1** — звук отключен 🔇.
- **pref_cloud_backup** — включает резервное копирование всех 4 параметров из настроек предпочтений ☁️.
- **pref_enable_multiple_open** — включает или отключает возможность множественного открытия профиля.
- **0** — множественное открытие отключено ❌.
- **1** — множественное открытие включено ✅.
- **pref_open_url** — URL, который будет использоваться при открытии профиля (например, Google).
Параметры в секции Настройки отпечатка (Fingerprint):
- **fingerprint_language_type** — определяет тип языка для отпечатка.
- **1** — используется стандартный тип (например, для имитации реального браузера) 🔤.
(Возможны и другие значения, в зависимости от реализации API)
- **fingerprint_language** — задаёт конкретное значение языка отпечатка.
Например, 'en-US' — английский язык (США) 🇺🇸.

## При выполнении скрипта:

- Скрипт получает список групп через API IXBrowser 📋.
- Ищет группу с именем, соответствующим значению profile_group_name 🔍.
- Для каждого из number_of_profiles создается новый профиль с уникальным именем (с добавлением порядкового номера и текущей даты/времени) 🆕.
- Настраиваются параметры профиля, включая URL, настройки прокси и отпечатка.
- Созданный профиль регистрируется через API IXBrowser, а его создание логируется с помощью loguru 📜.

## Запуск
Запустите скрипт с помощью Python:

```bash
python create_ix_browser_group_name.py
