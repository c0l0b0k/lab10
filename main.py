import os
import psutil
from prometheus_client import REGISTRY, start_http_server, Gauge, CollectorRegistry
from time import sleep
from dotenv import load_dotenv
load_dotenv()

# Создаем собственный реестр
custom_registry = CollectorRegistry()

# Основные метрики
cpu_usage = Gauge('cpu_usage_percent', 'Процент использования CPU', registry=custom_registry)
memory_total = Gauge('memory_total_bytes', 'Общий объем оперативной памяти', registry=custom_registry)
memory_used = Gauge('memory_used_bytes', 'Используемая оперативная память', registry=custom_registry)
disk_total = Gauge('disk_total_bytes', 'Общий объем дисков', registry=custom_registry)
disk_used = Gauge('disk_used_bytes', 'Используемый объем дисков', registry=custom_registry)

# Метрики для яндекса
browser_cpu_usage = Gauge('yandex_browser_cpu_percent', 'Процент использования CPU Яндексом', registry=custom_registry)
browser_memory_used = Gauge('yandex_browser_memory_used_bytes', 'Используемая память Яндекс.Браузером', registry=custom_registry)

def collect_metrics():
    # Получение общих метрик системы
    cpu_usage.set(psutil.cpu_percent())
    memory_total.set(psutil.virtual_memory().total)
    memory_used.set(psutil.virtual_memory().used)
    disk_total.set(psutil.disk_usage('C:/').total)
    disk_used.set(psutil.disk_usage('C:/').used)

    # Определение метрик для Яндекса
    total_browser_cpu = 0
    total_browser_memory = 0

    # Получение метрик для Яндекса
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        # Пробуем получить запущенные процессы
        try:
            if 'yandex' in proc.info['name'].lower() or 'browser' in proc.info['name'].lower():
                total_browser_cpu += proc.info['cpu_percent']
                total_browser_memory += proc.info['memory_info'].rss
        # Игнорируем не рабочие процессы
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Установка метрик для Яндекса
    browser_cpu_usage.set(total_browser_cpu)
    browser_memory_used.set(total_browser_memory)

def main():
    # Получаем переменные окружения для хоста и порта
    exporter_host = os.getenv("EXPORTER_HOST")
    exporter_port = int(os.getenv("EXPORTER_PORT"))

    # Запуск HTTP сервера для Prometheus, используя собственный реестр
    start_http_server(exporter_port, addr=exporter_host, registry=custom_registry)
    print(f"Получение метрик запущено по адресу {exporter_host}:{exporter_port}")

    # Сбор метрик и обновление каждые 3 секунды
    while True:
        collect_metrics()
        sleep(3)


if __name__ == '__main__':
    main()
