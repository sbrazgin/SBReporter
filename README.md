# SBReporter
Create excel reports from oracle database

Здесь буду вести проект по созданию отчетов из базы данных Oracle в формате Excel.

Идея такая: для периодической отправки разнообразных отчетов аналитиков 
		сейчас использую формирование текстовых файлов в sqlplus в формате html
		таким способом:

		SET MARKUP HTML ON
		SPOOL xxxx.xls;
		@@report_business_activity_xxxx.sql;
		spool off; 

		данный формат excel воспринимает, но иногда не совсем корректно отображает.

Задача проекта: формировать отчеты в виде файлов в родном формате excel

Архитектура такая: скрипт на Python, на входе скрипт принимает: 
	1) файл с параметрами
	2) файл с SQL-запросом
	3) шаблон excel-файла (должны быть заполнены все заголовки)
	На выходе скрипт формирует Excel-файл

Версии:	
Версия 0.1 Начальная версия, в целом работоспособна, начало тестирования
		
Версия 0.2 Портирование на linux

Версия 0.3 Работоспособность на linux проверена, исправлены ошибки

Инструкция по установке:
1) Установите Python

1) Скопируйте файл SBReporter.py на сервер 

2) Создайте файл с параметрами

3) Создайте excel шаблон (заголовок отчета)

4) Создайте файл запуска

5) Предоставьте права доступа
	chmod u+x SBReporter.py
	chmod u+x report_mpgu_stat_week.sh
	
6) Тестовый запуск

export ORACLE_HOME=
export LD_LIBRARY_PATH=
./SBReporter.py -i report_MPGU_1_week.ini -o report_mpgu_stat_week_052018.xlsx

7) Добавьте в планировщик cron sh скрипт
		