### Содержание
  1. [Введение](#1)
  2. [Объект тестирования](#2)
  3. [Риски](#3)
  4. [Аспекты тестирования](#4)<br>
  5. [Подходы к тестированию](#5)
  6. [Представление результатов](#6)
  7. [Выводы](#7)

<a name="1"></a>
### 1. Введение
  Данный файл содержит тест-план приложения **Bookshop**. Основной целью тестирования является
  проверка приложения на соответствие требованиям SRS.

<a name="2"></a>
### 2. Объект тестирования
Объект тестирования -  приложения **Bookshop**.  
Функция, которую выполняет данное приложение:  
организация системы поиска и покупок книг

Приложение обязано обладать определенными атрибутами качества: 
   
1. Функциональность:
+ функциональная корректность: приложение должно выполнять все заявленные функции;
+ функциональная целесообразность: отсутствуют незаявленные функции, которые бы мешали приложению выполнять первоначально поставленные задачи.
+ функциональная полнота: приложение обязано выполнять все заявленные функции в соответствии с SRS;

2. Удобство использования:  
+ адаптивный UX-дизайн: элементы управления эргономично располагаются на экране;  
+ минималистичность: приложение выполняет только конкретные задачи пользователя.
+ актуальность: обновление необходимой информации происходит при доступе к интернету;  
  
<a name="3"></a>
### 3. Риски
К рискам можно отнести следующие пункты:
* Вход в чужой аккаунт
* Большое количество одновременно выполняющийся запросов

<a name="4"></a>
### 4. Аспекты тестирования
К аспектам тестирования относится реализация основных функций приложения:
* возможность регистрации;
* возможность авторизации;
* возмость поиска книг;
* возможность добавления книг в корзину;
* возможность удаления книг из корзины;
* возможность оформлять заказ на покупку книг;

#### Функциональные требования:

##### Возможность регистрации
Этот вариант использования небходимо протестировать на:
1. Успешное сохранение информации
2. Кликабельность кнопок

##### Возможность авторизации
Этот вариант использования небходимо протестировать на:
1. Успешное сохранение информации
2. Соблюдение условий авторизации, если пользователь не зарегистрирован   
2. Кликабельность кнопок

##### Возможность поиска книг
Этот вариант использования небходимо протестировать на:
1. Поиск книги по названию
2. Поиск книг по конкретному жанру

##### Возможность просмотра имеющихся книг
Этот вариант использования небходимо протестировать на:   
1. Корректность отображение информации о книге: 
   * название
    * цена
    * год публикации
    * описание книги
    * размер (кол-во страниц)
    * обложка (изображение)
    * тип переплета
    * список авторов
    * список жанров
    * категория товара
2. Корректность отображение информации об авторе: 
   * полное имя
    * биография
    * фото автора
#### Нефункциональные требования:
1. Быстрый запуск
2. Надёжность. Доступ к онлайн магазину "Bookshop" должен осуществляться по HTTPS протоколу
2. Удобный и приятный UX дизайн

<a name="5"></a>
### 5. Подходы к тестированию
Каждый аспект тестирования был произведен с помощью системного тестирования.  
Системное тестирование - это тестирование программы в целом.  
Каждый тест производится вручную.  
Такой метод подходит для небольших проектов.

<a name="6"></a>
### 6. Представление результатов
Результаты тестирования представлены в таблице:
Case ID | Case Description | Scenarion/Steps | Expected Result | Action Result | Pass/Fail
--- | --- | --- | --- | --- | ---
1 | Регистрация | 1. Переход по ссылке на страницу регистрации <br> 2. Заполнение формы <br> 3. Отправка формы <br> | Создание нового пользователя в базе данных с параметрами из формы | Новый пользователь зарегистрирован | Pass
2 | Авторизация | 1. Переход по ссылки на страницу авторизации <br> 2. Если пользователь не зарегистрирован, он может пройти регистрацию (1-й тест) <br> 3. Если пользователь уже зарегистрирован, то он заполнияет форму для отправки | Если авторизация прошла успешно, пользователь переходит на главную страницу, иначе он повторяет попытку авторизации | Переход на главную страницу | Pass
3 | Поиск книг | 1. Ввод названия/жанра в форму поиска на главной странице <br> 2. Проверка наличия книг(и) в базе данных | На главную страницу выводится список найденных книг, или не выводится ничего | Отображение найденных книг | Pass
4 | Просмотр имеющихся книг | 1. Нажать на кнопку View при просмотре книги | Переход на страницу с описанием книги | Просмотр информации о книги и ее авторах | Pass
5 | Добавление книги в корзину | 1. Нажать на кнопку View при просмотре книги | 1. Нажать на кнопку ADD TO CARD при отображении информации о книге <br> 2. Если данной книги нет в корзине, то она добавляется как товый товар, иначе количество таких книг в корзине инкрементируется <br> 3. Увеличение цены на стоимость выбранной книги | Книга добавлена в корзину  | Pass
6 | Удаление книги из корзины | 1. Переход на страницу корзины пользователя | 1. Напротив нужной книги нажать кнопку DELETE FORM CARD <br> 2. Даже если тпользователь заказыл несколько таких книг, они все удаляются из корзины | Удаление книги из корзины | Pass
7 | Оформление заказа | 1. Пользователь нажимает на кнопку CHECKOUT, находясь на странице корзины <br> 2. Заполнение формы для обработки заказа <br> 3. Нажать на кнопку Pay и оплатить заказ <br> 4. переход на главную страницу | Создание нового заказа в базе данных | Заказ оформлен и находится в обработке | Pass


<a name="7"></a>
### 7. Выводы
Данный тестовый план позволяет протестировать основной функционал приложения.  
Успешное прохождение всех тестов может свидетельствовать тому, что приложение  
соответствует всем заявленным требованиям и стабильно работает.