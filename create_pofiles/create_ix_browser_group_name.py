import sys
import time
from loguru import logger
from ixbrowser_local_api import IXBrowserClient, Profile, Proxy, Preference, Fingerprint

# Глобальные настройки

# Имя группы, в которой будут создаваться профили (укажи точное название)
profile_group_name = "test"

# Количество профилей, которое нужно создать
number_of_profiles = 5  # 5 указано для примера

# Префикс для имени профиля
profile_name_prefix = "test"

# URL, который будет использоваться в профиле
site_url = None

# Настройки профиля
pref_load_profile_info_page = 0  # Отключаем инфо-страницу с IP
pref_block_audio = 1             # Отключаем звук
pref_cloud_backup = (1, 1, 1, 1)   # Включаем резервное копирование всех 4 параметров
pref_enable_multiple_open = 0      # Включаем множественное открытие

# Настройки отпечатка (Fingerprint)
fingerprint_language_type = 2
fingerprint_language = 'us'

# Режим отладки
show_request_log = False  # или True, если нужно логировать

# Использовать прокси или нет (False – по умолчанию не использовать, изменить на True, если нужно применять прокси
use_proxy = True

# Создаем клиента IXBrowser
client = IXBrowserClient()
client.show_request_log = show_request_log

# Получаем список всех групп
groups_list = client.get_group_list()
if not isinstance(groups_list, list):
    logger.error("Ошибка получения списка групп. Ответ от API: {response}", response=groups_list)
    sys.exit()

# Ищем ID нужной группы по названию (title)
group_id = None
for group in groups_list:
    if group.get("title", "").lower() == profile_group_name.lower():
        group_id = group.get("id")
        break

if group_id is None:
    logger.error("Группа '{group_name}' не найдена! Доступные группы:", group_name=profile_group_name)
    for group in groups_list:
        logger.error("- {title} (ID: {id})", title=group.get('title'), id=group.get('id'))
    sys.exit()

logger.info("Используем группу '{group_name}' с ID {group_id}", group_name=profile_group_name, group_id=group_id)

# Функция для создания настроек профиля на основе глобальных переменных


def create_profile_settings():
    pref = Preference()
    pref.load_profile_info_page = pref_load_profile_info_page
    pref.block_audio = pref_block_audio
    pref.set_cloud_backup(*pref_cloud_backup)
    pref.enable_multiple_open = pref_enable_multiple_open
    return pref


# Если прокси используются, получаем их список, иначе оставляем список пустым
if use_proxy:
    # Получаем список всех прокси с указанием лимита (чтобы получить прокси со всех страниц)
    proxy_list = client.get_proxy_list(limit=1000)
    # Фильтруем только свободные прокси (где нет профилей в использовании)
    free_proxies = [
        {
            "ip": p.get("proxy_ip"),
            "port": p.get("proxy_port"),
            "username": p.get("proxy_user", ""),
            "password": p.get("proxy_password", ""),
            "type": p.get("proxy_type", "socks5")
        }
        for p in proxy_list if p.get("activeWindow", 0) == 0
    ]
    logger.info(f"Найдено {len(free_proxies)} свободных прокси.")
else:
    free_proxies = []
    logger.warning("Прокси не используются.")

# В цикле создаем профили
for i in range(number_of_profiles):
    profile = Profile()
    profile.random_color()
    profile.site_url = site_url

    # Формируем имя профиля с использованием префикса, номера и текущей даты/времени
    profile.name = f'{profile_name_prefix} {i + 1}'
    profile.group_id = group_id

    # Прокси-настройки (только если use_proxy=True)
    if use_proxy:
        if free_proxies:
            proxy_data = free_proxies.pop(0)  # Берем первый свободный прокси из полного списка
            proxy = Proxy()
            proxy.proxy_ip = proxy_data["ip"]
            proxy.proxy_port = proxy_data["port"]
            proxy.proxy_user = proxy_data["username"]
            proxy.proxy_password = proxy_data["password"]
            proxy.proxy_type = proxy_data["type"]
            profile.proxy_config = proxy
            logger.info(f"Используем прокси {proxy_data['ip']}:{proxy_data['port']} для профиля {profile.name}")
        else:
            logger.warning(f"Нет свободных прокси! Профиль {profile.name} создается без прокси.")
    else:
        logger.critical(f"Прокси не используются для профиля {profile.name}.")

    # Применяем настройки профиля
    profile.preference_config = create_profile_settings()
    # Настройки отпечатка (fingerprint)
    fingerprint = Fingerprint()
    fingerprint.language_type = fingerprint_language_type
    fingerprint.language = fingerprint_language
    profile.fingerprint_config = fingerprint

    # Создаем профиль через API
    result = client.create_profile(profile)
    if result is None:
        logger.error("Ошибка создания профиля {num}: Error code = {code}, Error message = {msg}",
                     num=i + 1, code=client.code, msg=client.message)
    else:
        logger.success("Профиль {num} создан успешно: {result}", num=i + 1, result=result)

    # Немного ждем между созданиями профилей
    time.sleep(1)
