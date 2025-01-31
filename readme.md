
Данная программа предоставляет метрики о загрузке CPU, использовании памяти и дисков для вашей системы, а также мониторит ресурсы, потребляемые **Яндекс.Браузером**

## Запуск

1. Установите зависимости:
   Для установки всех зависимостей используйте команду:
   ```bash
   pip install -r requirements.txt  
2. Установите переменные окружения в файле .env: 

   ```ini
   EXPORTER_HOST=127.0.0.1
   EXPORTER_PORT=8000
4. Запустите код:

   ```bash
   python main.py
   ```
   Экспортер будет доступен по адресу: http://127.0.0.1:8000/metrics.

5. Метрики

1) Общие метрики системы:  
   cpu_usage_percent: Процент использования CPU.  
   memory_total_bytes: Общий объем оперативной памяти в байтах.  
   memory_used_bytes: Объем используемой оперативной памяти в байтах.  
   disk_total_bytes: Общий объем доступных дисков в байтах.   
   disk_used_bytes: Объем используемого пространства на дисках в байтах.  
2) Метрики для Яндекс.Браузера:  
   yandex_browser_cpu_percent: Процент использования CPU Яндекс.Браузером.  
   yandex_browser_memory_used_bytes: Объем памяти, используемый Яндекс.Браузером в байтах.  
