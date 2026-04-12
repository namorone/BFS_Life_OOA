---

## 2. Модуль «Налаштування та керування категоріями» (Settings, Categories)

**Обсяг:** backend `GET/PUT /api/v1/settings`, `GET/POST/PUT/DELETE /api/v1/categories`; frontend `/settings`, `/categories`, інтеграція з sidebar, захищені маршрути, модальні вікна add/edit/delete category.

### 2.1 Автоматизований набір тестів (pytest)

| № | Сценарій | Файл / тест |
|---|----------|-------------|
| 1 | Health endpoint повертає `200` і `{"status":"ok"}` | `test_health.py::test_health_returns_ok` |
| 2 | GET `/api/v1/settings` повертає об’єкт налаштувань | `test_settings.py::test_get_settings` |
| 3 | PUT `/api/v1/settings` оновлює налаштування | `test_settings.py::test_update_settings` |
| 4 | GET `/api/v1/categories` повертає список | `test_categories.py::test_get_categories` |
| 5 | POST `/api/v1/categories` створює категорію | `test_categories.py::test_create_category` |
| 6 | PUT `/api/v1/categories/{id}` оновлює назву категорії | `test_categories.py::test_update_category` |
| 7 | DELETE `/api/v1/categories/{id}` видаляє категорію | `test_categories.py::test_delete_category` |
| 8 | Після DELETE категорія відсутня у списку | `test_categories.py::test_deleted_category_not_in_list` |

Запуск: `sudo docker exec -it bfs_backend pytest`

---

### 2.2 Smoke-тестування (ручні сценарії)

Перевірки з піднятим стеком (`docker-compose up --build` або еквівалент), після успішного логіну.

| ID smoke | Дія | Очікуваний результат |
|----------|-----|----------------------|
| SM-SET-01 | Увійти в систему валідним користувачем | Відкривається dashboard |
| SM-SET-02 | У sidebar натиснути **Settings** | Відкривається сторінка налаштувань |
| SM-SET-03 | Переконатися, що sidebar на Settings має той самий layout, що й Dashboard | Бічна панель відображається коректно, logout унизу |
| SM-SET-04 | На сторінці Settings перевірити наявність заголовка і підзаголовка | Текст відображається без зламаної верстки |
| SM-SET-05 | Перевірити блок **Notification Preferences** | Відображаються два перемикачі |
| SM-SET-06 | Увімкнути / вимкнути **Email Notifications** | Стан перемикача змінюється |
| SM-SET-07 | Увімкнути / вимкнути **Warranty Expiration Alerts** | Стан перемикача змінюється |
| SM-SET-08 | Перевірити блок **Account Settings** | Відображаються Full Name, Email, Preferred Currency |
| SM-SET-09 | Змінити Full Name і натиснути **Save Changes** | Значення зберігається |
| SM-SET-10 | Змінити Email і натиснути **Save Changes** | Значення зберігається |
| SM-SET-11 | Змінити Preferred Currency на EUR | Значення змінюється у формі |
| SM-SET-12 | Зберегти нову валюту | Після reload валюта лишається зміненою |
| SM-SET-13 | Перезавантажити `/settings` після змін | Збережені значення залишаються |
| SM-SET-14 | Перевірити блок **Appearance** | Блок відображається, UI не ламається |
| SM-SET-15 | Натиснути **Manage Categories** | Відкривається сторінка `/categories` |
| SM-CAT-01 | Відкрити `/categories` після логіну | Сторінка відкривається без редіректу на login |
| SM-CAT-02 | Переконатися, що список категорій завантажився | Відображаються елементи списку |
| SM-CAT-03 | Перевірити кількість категорій у заголовку картки | Лічильник відповідає кількості рядків |
| SM-CAT-04 | Натиснути **Add Category** | Відкривається modal add |
| SM-CAT-05 | Закрити add modal через **Cancel** | Modal закривається |
| SM-CAT-06 | Додати нову категорію з валідною назвою | Нова категорія з’являється у списку |
| SM-CAT-07 | Перезавантажити `/categories` після додавання | Нова категорія лишається у списку |
| SM-CAT-08 | Натиснути edit у будь-якої категорії | Відкривається modal edit |
| SM-CAT-09 | Змінити назву категорії і зберегти | Назва оновлюється у списку |
| SM-CAT-10 | Перезавантажити сторінку після edit | Оновлена назва зберігається |
| SM-CAT-11 | Натиснути delete у будь-якої категорії | Відкривається modal delete |
| SM-CAT-12 | Закрити delete modal через **Cancel** | Категорія не видаляється |
| SM-CAT-13 | Підтвердити delete | Категорія зникає зі списку |
| SM-CAT-14 | Перезавантажити сторінку після delete | Видалена категорія відсутня |
| SM-CAT-15 | Повернутися зі сторінки Categories назад у Settings | Навігація працює коректно |
| SM-CAT-16 | Вийти через **Logout** із sidebar | Сесія очищається, відкривається login |

---

### 2.3 Реєстр дефектів і спостережень (33, префікс BUG-SET- / BUG-CAT-)

| ID | Опис | Пріоритет | Статус |
|----|------|-----------|--------|
| BUG-SET-001 | Settings page спочатку використовувала окремий sidebar і візуально не збігалася з Dashboard | P3 | Закрито |
| BUG-SET-002 | Після первинної реалізації Settings поля форми розташовувалися в один рядок і ламали UX | P2 | Закрито |
| BUG-SET-003 | Settings page зависала на `Loading...` через відсутній/некоректний CORS для frontend origin | P1 | Закрито |
| BUG-SET-004 | Спроба використати `EmailStr` без `email-validator` ламала старт бекенду | P2 | Закрито |
| BUG-SET-005 | Після merge модель `User` містила нові поля settings, але БД не мала відповідних колонок | P1 | Закрито |
| BUG-SET-006 | Реєстрація падала з `UndefinedColumnError` через розсинхрон моделі `User` і міграцій | P1 | Закрито |
| BUG-SET-007 | Зміни налаштувань не зберігались безпосередньо в БД на ранньому етапі (fake settings) | P2 | Закрито / прийнятна еволюція |
| BUG-SET-008 | Settings page не використовувала спільний app layout після merge | P3 | Закрито |
| BUG-SET-009 | Кнопка `Manage Categories` була відсутня в одному з ранніх варіантів UI | P3 | Закрито |
| BUG-SET-010 | На сторінці Settings не було обробки помилки завантаження з бекенду | P3 | Закрито частково |
| BUG-SET-011 | Save action не показує дружнє повідомлення про успіх, окрім простого alert | P4 | Відкрито |
| BUG-SET-012 | Appearance section є в UI, але функціонально dark mode не реалізований | P4 | Відкрито |
| BUG-SET-013 | Поле Email у Settings можна змінити на будь-який рядок без додаткової frontend-валідації | P3 | Відкрито |
| BUG-SET-014 | Відсутня окрема сторінка / діалог зміни пароля в межах Settings | P4 | Відкрито |
| BUG-SET-015 | Відсутня 2FA / security settings поза базовими полями | P4 | Відкрито |
| BUG-SET-016 | При недоступному бекенді Settings page може показувати мінімалістичну помилку без дружнього UX | P3 | Відкрито |
| BUG-CAT-001 | Categories page спочатку використовувала raw `fetch`, через що не підставлявся Bearer token | P1 | Закрито |
| BUG-CAT-002 | Через raw `fetch` захищений `/api/v1/categories` повертав 401 і сторінка ламалася | P1 | Закрито |
| BUG-CAT-003 | При прямому переході на `/categories` сторінка могла бути порожньою через необроблений error state | P2 | Закрито частково |
| BUG-CAT-004 | Categories route на бекенді спочатку був реалізований на fake data і не відповідав новій архітектурі з auth/db | P2 | Закрито |
| BUG-CAT-005 | Після merge CRUD для categories вимагав дописати `create/update/delete` у service/repository | P2 | Закрито |
| BUG-CAT-006 | `schemas/category.py` мав конфлікт між `Category` і `CategoryRead` | P2 | Закрито |
| BUG-CAT-007 | Add category modal не мала достатньої обробки порожнього вводу на ранньому етапі | P3 | Закрито частково |
| BUG-CAT-008 | Edit category modal спочатку не використовувала спільний API client | P2 | Закрито |
| BUG-CAT-009 | Delete category modal спочатку не використовувала спільний API client | P2 | Закрито |
| BUG-CAT-010 | Categories page не інтегрована стилістично з Sidebar/Dashboard layout так само добре, як Settings | P3 | Відкрито |
| BUG-CAT-011 | Categories page не має повноцінного loading state / skeleton | P4 | Відкрито |
| BUG-CAT-012 | Після create/update/delete немає toast-повідомлень про успіх | P4 | Відкрито |
| BUG-CAT-013 | Відсутнє підтвердження у вигляді більш детального тексту про наслідки delete | P4 | Відкрито |
| BUG-CAT-014 | Не реалізована перевірка дубльованих назв категорій | P3 | Відкрито |
| BUG-CAT-015 | Не реалізована пагінація / пошук для довгого списку категорій | P4 | Відкрито |
| BUG-CAT-016 | При backend error користувач бачить технічний текст помилки, а не дружнє повідомлення | P3 | Відкрито |
| BUG-CAT-017 | `Inventory`/`Notifications`/`Profile` пункти sidebar присутні, але пов’язані сторінки можуть бути ще не реалізовані | P4 | Не дефект (поза поточним обсягом) |
| BUG-CAT-018 | Для Categories page ще не завершене повне візуальне вирівнювання під Figma | P4 | В роботі |

---

## Підсумок

- У **розділі 2** автотести покривають базовий API для health, settings і categories.
- Smoke-набір перевіряє базову працездатність Settings і Categories після логіну.
- У реєстрі **BUG-SET / BUG-CAT**: зафіксовано 33 спостереження та дефекти для модуля.

Дата оновлення: квітень 2026.
