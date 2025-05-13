# TestScript
---
* Запуск скрипта:
python main.py [ваши файлы] --report [Название отчета]
![image](https://github.com/user-attachments/assets/3ae91b14-c114-4004-a084-55b9ab575782)
---
* Пример отчета(Сверху задано название вашего отчета)
![image](https://github.com/user-attachments/assets/32c21943-163b-4fec-af71-ec55e6c2b6c7)
---
# Некоторые детали
* Есть так же две функции которые формируют отчеты в форматах: csv -> report_creator_csv и json -> report_creator_json
* При вызове этих функций создаются отдельные файлы, название которых создается по формуле "report_{название вашего отчета}"
* Код покрыт тестами, использованы библиотеки: unittest, pytest.


