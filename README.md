# Real Estate Price Prediction in Ukraine

Welcome to my pet project! This project is a flask app and telegram bot with an integrated machine learning model. A model based on XGBoost allows you to predict the cost of apartments in various cities of Ukraine based on features such as city, region, area, floor and number of rooms.  

### Installation
1. Ensure you have Docker and Docker Compose installed.
2. Clone the project repository with the command _git clone https://github.com/Boohdaaaan/ML-Property-valuation.git_.
3. Set environment variables _PASSWORD_EMAIL_APP_ - Gmail app password and _API_TOKEN_ - Telegram bot API token.
4. Start the project with the command _docker compose up --build_.

All necessary requirements for the project will be automatically installed when running containers with Docker Compose.

### How to Interact with the Project
Open the web application in your browser by visiting http://localhost:5000/.  
Enter the necessary parameters of the real estate property (city, region, area, floor, and number of rooms) and click the "Predict" button.  
To use the Telegram bot, find it on Telegram by its name and start a dialogue with it. The bot will ask you for the required property features and will send back the predicted price in response.

### Data
The dataset used for this project was scraped from the most popular real estate listings website in Ukraine.  
Before training the XGBoost model, the data underwent thorough preprocessing.  
1. Data cleaning was performed to correct any errors in the dataset.
2. Outliers were removed to improve the model's robustness.
3. Feature selection was conducted to identify the most relevant attributes for predicting real estate prices.

### ML Model
In this project, I employed the XGBoost machine learning model.  
To optimize the model's performance and achieve the best results, I used the Optuna library for hyperparameters tuning. This process allowed me to fine-tune the model on optimal hyperparameters, leading to improved prediction quality.

## Docker
For a convenient deployment in the future, I used Docker Compose. My project has two Dockerfiles and a docker-compose.yml.
Dockerfile create docker image, define settings and environments inside a container.
docker-compose.yml defines the services to be started, environment and network settings.
____

# Прогнозування цін на нерухомість в Україні
Ласкаво прошу до мого пет-проєкту! Цей проєкт є веб-додатком та телеграм-ботом із інтегрованою моделлю машинного навчання. Модель на основі XGBoost дозволяє прогнозувати вартість квартир у різних містах України за такими ознаками як місто, регіон, район, поверх і кількість кімнат.

### Запуск проєкту
1. Переконайтеся, що у вас встановлено Docker і Docker Compose.
2. Клонуйте репозиторій проєкту за допомогою команди _git clone https://github.com/Boohdaaaan/ML-Property-valuation.git_.
3. Установіть змінні середовища _PASSWORD_EMAIL_APP_ - пароль додатку Gmail та _API_TOKEN_ - API токен телеграм-бота.
4. Запустіть проєкт командою _docker compose up --build_.

Усі необхідні залежності для проєкту будуть автоматично встановлені під час запуску контейнерів із Docker Compose.

### Як взаємодіяти з проєктом 
Відкрийте веб-додаток у своєму браузері, відвідавши http://localhost:5000/.  
Введіть необхідні параметри квартири (місто, область, площа, поверх, кількість кімнат) і натисніть кнопку «Розрахувати».  
Щоб скористатися Telegram-ботом, знайдіть його в Telegram за назвою та почніть з ним діалог. Бот запитає у вас необхідні параметри нерухомості та надішле прогнозовану ціну у відповідь.

### Дані
Набір даних, використаний для цього навчання моделі, я зпарсив з найпопулярнішого сайту оголошень в Україні.
Перед навчанням моделі машинного навчання дані пройшли ретельну попередню обробку.
1. Виконано очищення даних, щоб виправити усі помилки в даних.
2. Видалено викиди, щоб покращити стійкість моделі.
3. Вибрано найкращі ознаки для прогнозування цін на нерухомість.

### ML Модель
У цьому проекті я використовував алгоритм машинного навчання XGBoost.
Щоб покращити точність моделі, я використовував бібліотеку Optuna для налаштування гіперпараметрів. Цей процес дозволив мені обрати оптимальні гіперпараметри, що призвело до покращення якості прогнозу.

## Docker
Для зручного деплою у майбутньому я використав Docker Compose. У проекті є два Dockerfile та docker-compose.yml.
Dockerfile створює docker-образ, визначає налаштування та оточення всередині контейнера.
docker-compose.yml визначає служби які мають бути запущені, налаштування оточення та мережі.
