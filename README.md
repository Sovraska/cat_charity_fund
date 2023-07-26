# Проект QRKot  Тут мы помогаем котикам
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)   
  

Бэкенд приложения QRKot на FastAPI для благотворительного фонда, который занимается сбором пожертвований на различные цели, связанные с поддержкой котеек. Фонд использует собранные средства на медицинское обслуживание нуждающихся кошек, обустройство жилища для кошачьей колонии и кормление бездомных кошек.
  
  
## Запуск проекта  
  
Клонируйте репозиторий и перейдите в него

```
git clone git@github.com:Sovraska/cat_charity_fund.git
```
  
Установите и активируйте виртуальное окружение  

```
python -m venv venv 
```
```
. .\venv\Scripts\activate
```
  
Установите зависимости из файла requirements.txt :  
```  
pip install -r requirements.txt  
```  
Через командную строку запустите проект:  
```  
uvicorn app.main:app --reload 
```  
  
## API  
Список доступных эндпоинтов в проекте c примерами запросов, варианты ответов и ошибок приведены в спецификации openapi.yml  или по эндпоинту /docs
  
## Автор  
  
[Семён Новиков](https://github.com/Sovraska)