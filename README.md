# Yatube Django UnitTest
# Учебный Проект. Тесты
В этом проекте я настраивал большой диапазон тестов, чтобы познакомиться с принципами Unittest в Django, были проведены следующие тесты:

- Unittest в Django: тестирование моделей
  - Протестированы модели приложения posts в Yatube

- Unittest в Django: тестирование URLs
  - Проверка доступности страниц и названия шаблонов приложения Posts проекта Yatube. Проверка учитывает права доступа

- Unittest в Django: тестирование Views
  - Тесты которые проверяют, что во view-функциях используются правильные html-шаблоны
  - Проверка словаря context, передаваемого в шаблон при вызове

- Unittest в Django: тестирование Forms
  - при отправке валидной формы со страницы создания поста
  - при отправке валидной формы со страницы редактирования поста

## Инструкция по установке 

Клонируем репозиторий

<code>git clone https://github.com/ZOMini/hw04_tests</code>

Переходим в папку с проектом

<code>hw04_tests/</code>

Устанавливаем отдельное виртуальное окружение для проекта

<code>python -m venv venv</code>

Активируем виртуальное окружение

<code>venv\Scripts\activate</code>

Устанавливаем модули необходимые для работы проекта

<code>pip install -r requirements.txt</code>

# Требования
Python 3.6 +

Работает под ОС Linux, Windows, macOS, BSD
