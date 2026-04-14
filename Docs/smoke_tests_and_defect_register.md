# Smoke-тестування та реєстр дефектів

Цей документ відповідає завданню щодо якості: **набір тестів**, **smoke-перевірки** базової працездатності та **реєстр дефектів** (опис, пріоритет, статус). Документ **розширюється** — для нових підсистем додавайте розділи за зразком нижче (автотести, smoke, таблиця з власним префіксом ID, наприклад `BUG-ITEM-001`).

**Пріоритети:** **P1** — критичний (блокує роботу / безпека), **P2** — високий, **P3** — середній, **P4** — низький / покращення.

**Статуси:** **Відкрито** — потрібна зміна або рішення; **В роботі** — виправляється; **Закрито** — перевірено, поведінка прийнятна або виправлена; **Не дефект** — очікувана поведінка або поза поточним обсягом.

---

## 1. Модуль «Автентифікація» (логін, реєстрація, JWT)

**Обсяг:** backend `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, захищені маршрути з Bearer; frontend `/login`, `/register`, збереження сесії після успіху.

### 1.1 Автоматизований набір тестів (pytest)

| № | Сценарій | Файл / тест |
|---|----------|-------------|
| 1 | Успішна реєстрація: 201, `access_token`, `user` | `test_api_auth_bfs.py::test_bfs_api_auth_register_returns_token_and_user_for_login_flow` |
| 2 | Пароль без цифри → 422 | `test_api_auth_bfs.py::test_bfs_api_auth_register_password_without_digit_422_like_register_page` |
| 3 | Пароль занадто короткий → 422 | `test_api_auth_bfs.py::test_bfs_api_auth_register_password_too_short_422` |
| 4 | Невалідний email → 422 | `test_api_auth_bfs.py::test_bfs_api_auth_register_invalid_email_422` |
| 5 | Повторна реєстрація з тим самим email → 409 | `test_api_auth_bfs.py::test_bfs_api_auth_register_duplicate_email_409` |
| 6 | Успішний логін після реєстрації → 200 | `test_api_auth_bfs.py::test_bfs_api_auth_login_success_matching_login_page` |
| 7 | Логін з email у іншому регістрі після реєстрації → 200 | `test_api_auth_bfs.py::test_bfs_api_auth_login_email_case_insensitive_after_register` |
| 8 | Невірний пароль → 401 | `test_api_auth_bfs.py::test_bfs_api_auth_login_wrong_password_401` |
| 9 | Невідомий email → 401 | `test_api_auth_bfs.py::test_bfs_api_auth_login_unknown_email_401` |
| 10 | Порожній пароль на логіні → 422 | `test_api_auth_bfs.py::test_bfs_api_auth_login_empty_password_422` |
| 11 | Захищений GET без токена → 401 | `test_api_auth_bfs.py::test_bfs_api_jwt_missing_bearer_401_on_protected_route` |
| 12 | Захищений GET з некоректним JWT → 401 | `test_api_auth_bfs.py::test_bfs_api_jwt_garbage_bearer_401_on_protected_route` |
| 13 | Захищений GET з валідним JWT → 200 | `test_api_auth_bfs.py::test_bfs_api_jwt_valid_token_ok_on_protected_route` |
| 14 | Схема пароля: обов’язкові літера й цифра | `test_user_schema_bfs.py` |
| 15 | Ім’я з одних пробілів відхиляється | `test_user_schema_bfs.py` |
| 16 | Хешування пароля та JWT (unit) | `test_security_bfs.py` |

Запуск: `make test-backend` (PostgreSQL `bfs_test`, pytest у контейнері backend).

### 1.2 Smoke-тестування (ручні сценарії)

Перевірки з піднятим стеком (`make run` або еквівалент), фронт і API доступні.

| ID smoke | Дія | Очікуваний результат |
|----------|-----|----------------------|
| SM-01 | Відкрити `/login` | Форма email/пароль, посилання на реєстрацію |
| SM-02 | Відкрити `/register` | Поля ім’я, email, пароль, підтвердження |
| SM-03 | Логін з порожніми полями | Повідомлення «Please fill in all fields» |
| SM-04 | Реєстрація з порожніми полями | Те саме |
| SM-05 | Реєстрація: пароль &lt; 8 символів | Повідомлення про мінімальну довжину |
| SM-06 | Реєстрація: пароль без літери / без цифри | Відповідне повідомлення на UI |
| SM-07 | Реєстрація: паролі не збігаються | «Passwords do not match» |
| SM-08 | Успішна реєстрація валідних даних | Редірект у застосунок, сесія з токеном |
| SM-09 | Успішний логін існуючого користувача | Редірект (або `returnTo` з безпечного шляху) |
| SM-10 | Логін з невірним паролем | Повідомлення про помилку (від API) |
| SM-11 | Повторна реєстрація того ж email | Повідомлення про конфлікт (деталі залежать від `detail` у відповіді) |
| SM-12 | Відкрити захищену сторінку без логіну | Редірект на логін з `returnTo` де налаштовано |
| SM-13 | Після логіну доступ до захищеного API | Дані завантажуються з Bearer |

### 1.3 Реєстр дефектів і спостережень (34, префікс BUG-AUTH-)

| ID | Опис | Пріоритет | Статус |
|----|------|-----------|--------|
| BUG-AUTH-001 | Реєстрація з паролем без цифри має відхилятися API (422) | P2 | Закрито (автотест №2) |
| BUG-AUTH-002 | Реєстрація з надто коротким паролем має давати 422 | P2 | Закрито (автотест №3) |
| BUG-AUTH-003 | Невалідний формат email на реєстрації має давати 422 | P2 | Закрито (автотест №4) |
| BUG-AUTH-004 | Дубль email при повторній реєстрації має давати 409 | P2 | Закрито (автотест №5) |
| BUG-AUTH-005 | Після успішної реєстрації відповідь містить `access_token` і коректні поля `user` | P1 | Закрито (автотест №1) |
| BUG-AUTH-006 | Логін з коректними обліковими даними після реєстрації повертає 200 і профіль | P1 | Закрито (автотест №6) |
| BUG-AUTH-007 | Вхід з email у нижньому регістрі після реєстрації зі змішаним регістром має працювати | P3 | Закрито (автотест №7) |
| BUG-AUTH-008 | Невірний пароль не повинен видавати успішний вхід (401) | P1 | Закрито (автотест №8) |
| BUG-AUTH-009 | Невідомий email не повинен розкривати існування обліковки (401) | P2 | Закрито (автотест №9) |
| BUG-AUTH-010 | Порожній пароль на логіні валідується (422), а не 401 з некоректним тілом | P3 | Закрито (автотест №10) |
| BUG-AUTH-011 | Запит до захищеного ресурсу без `Authorization` має повертати 401 | P1 | Закрито (автотест №11) |
| BUG-AUTH-012 | Невалідний або підроблений JWT не приймається на захищеному маршруті (401) | P1 | Закрито (автотест №12) |
| BUG-AUTH-013 | Валідний JWT після логіну дозволяє виконати захищений GET | P1 | Закрито (автотест №13) |
| BUG-AUTH-014 | Pydantic-схема реєстрації вимагає літеру й цифру в паролі (узгоджено з UI) | P3 | Закрито (unit) |
| BUG-AUTH-015 | Ім’я з одних пробілів відхиляється на рівні схеми (як «порожня» форма) | P3 | Закрито (unit) |
| BUG-AUTH-016 | UI логіну: порожні поля показують зрозумілу помилку | P3 | Закрито (SM-03) |
| BUG-AUTH-017 | UI реєстрації: валідація довжини й складу пароля до відправки на API | P3 | Закрито (SM-05, SM-06) |
| BUG-AUTH-018 | UI реєстрації: перевірка збігу пароля з підтвердженням | P3 | Закрито (SM-07) |
| BUG-AUTH-019 | Після успішної реєстрації / логіну відбувається навігація в застосунок | P2 | Закрито (SM-08, SM-09) |
| BUG-AUTH-020 | Параметр `returnTo` після логіну приймає лише відносні безпечні шляхи (захист від open redirect) | P2 | Закрито (код `safeReturnPath` у `LoginPage.jsx`) |
| BUG-AUTH-021 | Кнопки сабміту блокуються під час запиту (`submitting`), щоб уникнути подвійної відправки | P4 | Закрито |
| BUG-AUTH-022 | На формах виставлені `autoComplete` для зручності браузера / менеджерів паролів | P4 | Закрито |
| BUG-AUTH-023 | Повідомлення про помилки API нормалізуються з `detail` (рядок / масив validation) | P3 | Закрито (`normalizeErrorDetail` у `api.js`) |
| BUG-AUTH-024 | При 401 на не-auth шляхах очищається збережена сесія і редірект на логін | P2 | Закрито |
| BUG-AUTH-025 | Відсутність обмеження частоти запитів (rate limiting) на `/auth/login` та `/auth/register` — ризик брутфорсу та спаму реєстрацій | P3 | Відкрито |
| BUG-AUTH-026 | Відсутність блокування обліковки після N невдалих спроб логіну | P3 | Відкрито |
| BUG-AUTH-027 | Зберігання access token у браузері (наприклад localStorage) збільшує ризик при XSS порівняно з httpOnly cookies | P3 | Відкрито (архітектурний ризик; прийнятно для навчального проєкту за умови санації вводу) |
| BUG-AUTH-028 | Немає явної верхньої межі довжини пароля на фронтенді (обмеження лише на бекенді) — можлива погана UX при дуже довгих рядках | P4 | Відкрито |
| BUG-AUTH-029 | Функція «забув пароль» / скидання пароля не реалізована | P4 | Відкрито (поза поточним обсягом) |
| BUG-AUTH-030 | Двофакторна автентифікація (2FA) не передбачена | P4 | Відкрито (поза обсягом) |
| BUG-AUTH-031 | Тексти помилок на UI переважно англійською; немає повної локалізації українською | P4 | Відкрито |
| BUG-AUTH-032 | Повідомлення для 409 (дубль email) залежить від формату `detail` з API — може виглядати технічно для користувача | P4 | Відкрито |
| BUG-AUTH-033 | Реєстрація з вже існуючим email у різному регістрі: якщо бекенд нормалізує email до lower — дубль коректно ловиться; інакше можливий дубль у БД (залежить від унікального індексу) | P2 | Не дефект (узгоджено з автотестом нормалізації логіну; перевірити унікальність у міграціях) |
| BUG-AUTH-034 | Ручне smoke SM-01–SM-13 потребує актуального `VITE_API_URL` і доступності БД; без цього помилки мережі можуть імітувати «дефект логіну» | P3 | Не дефект (конфігурація середовища) |

<!-- Наступні модулі: ## 2. Модуль «…» з підрозділами 2.1–2.3 та префіксом BUG-… -->

---

---

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

---

## 3. Модуль «Dashboard» (захищена сторінка статистики)

**Обсяг:** frontend `/dashboard` (`DashboardPage.jsx`, `Sidebar.jsx`, `StatCard.jsx`, `Toast.jsx`), backend `GET /api/v1/dashboard/stats`, `GET /api/v1/categories`, protected access через Bearer. Для цього проєкту сторінка dashboard є частиною стандартного ланцюжка **Frontend → API → Service → Repository → Database**.

### 3.1 Автоматизований набір тестів (pytest)

Файл: `tests/integration/test_api_dashboard_bfs.py`

| № | Сценарій | Файл / тест |
|---|----------|-------------|
| 1 | `GET /api/v1/dashboard/stats` без Bearer → 401 | `test_api_dashboard_bfs.py::test_bfs_api_dashboard_requires_auth_401` |
| 2 | Новий користувач без item отримує статистику `0 / 0 / 0` | `test_api_dashboard_bfs.py::test_bfs_api_dashboard_returns_zero_stats_for_new_user` |
| 3 | `total_items` рахує кількість item поточного користувача | `test_api_dashboard_bfs.py::test_bfs_api_dashboard_counts_total_items` |
| 4 | `active_warranties` враховує лише непроcтрочені гарантії | `test_api_dashboard_bfs.py::test_bfs_api_dashboard_counts_only_active_warranties` |
| 5 | `expiring_soon` враховує лише гарантії в межах configured window | `test_api_dashboard_bfs.py::test_bfs_api_dashboard_counts_only_expiring_soon_inside_window` |
| 6 | Статистика ізольована між користувачами | `test_api_dashboard_bfs.py::test_bfs_api_dashboard_excludes_other_users_data` |
| 7 | Відповідь `/dashboard/stats` має правильну структуру | `test_api_dashboard_bfs.py::test_bfs_api_dashboard_response_shape` |

### 3.2 Smoke-тестування (ручні сценарії)

| ID smoke | Дія | Очікуваний результат |
|----------|-----|----------------------|
| SM-DASH-01 | Авторизуватися та перейти на `/dashboard` | Сторінка відкривається без редіректу на `/login` |
| SM-DASH-02 | Відкрити `/dashboard` без логіну | Редірект на логін |
| SM-DASH-03 | Перевірити заголовок сторінки | Видно `Dashboard` та підзаголовок welcome-text |
| SM-DASH-04 | Перевірити лівий sidebar | Видно `Home Inventory`, `Warranty Tracker`, навігацію та `Logout` |
| SM-DASH-05 | Перевірити активний пункт sidebar | `Dashboard` підсвічений активним стилем |
| SM-DASH-06 | Перевірити картку `Total Items` | Є заголовок, підзаголовок і числове значення |
| SM-DASH-07 | Перевірити картку `Active Warranties` | Є заголовок, підзаголовок і числове значення |
| SM-DASH-08 | Перевірити картку `Expiring Soon` | Є заголовок, підзаголовок і числове значення світлішим синім |
| SM-DASH-09 | Відкрити dashboard для нового користувача без item | Показує `0 / 0 / 0` |
| SM-DASH-10 | Створити item без гарантії і повернутися на dashboard | `Total Items` збільшується на 1, інші лічильники не зростають |
| SM-DASH-11 | Створити item з валідною гарантією | `Total Items` і `Active Warranties` збільшуються |
| SM-DASH-12 | Створити item з гарантією, що закінчується в межах configured window | `Expiring Soon` збільшується |
| SM-DASH-13 | Створити item з гарантією далеко в майбутньому | `Expiring Soon` не збільшується |
| SM-DASH-14 | Після успішного додавання item не оновлювати сторінку вручну | Лічильники оновлюються автоматично |
| SM-DASH-15 | Перевірити toast після успішного save | З’являється success toast і зникає сам за кілька секунд |

### 3.3 Реєстр дефектів і спостережень (префікс BUG-DASH-)

| ID | Опис | Пріоритет | Статус |
|----|------|-----------|--------|
| BUG-DASH-001 | `/dashboard` має бути захищеною сторінкою і не відкриватися без токена | P1 | Закрито (SM-DASH-01, SM-DASH-02, автотест №1) |
| BUG-DASH-002 | Порожня статистика нового користувача має повертатися як `0 / 0 / 0`, а не `null` / 500 | P1 | Закрито (автотест №2, SM-DASH-09) |
| BUG-DASH-003 | `total_items` не повинен включати item інших користувачів | P1 | Закрито (автотести №3, №6) |
| BUG-DASH-004 | `Active Warranties` не повинно враховувати прострочені гарантії | P2 | Закрито (автотест №4) |
| BUG-DASH-005 | `Expiring Soon` повинно рахуватися лише в межах `WARRANTY_EXPIRING_DAYS` | P2 | Закрито (автотест №5) |
| BUG-DASH-006 | Відповідь `/dashboard/stats` повинна мати стабільну структуру для фронтенду | P2 | Закрито (автотест №7) |
| BUG-DASH-007 | Кнопка `Add Repair` поки не має реалізованого сценарію / сторінки | P4 | Відкрито |
| BUG-DASH-008 | Sidebar містить пункти на сторінки, які ще не реалізовані (`Inventory`, `Notifications`, `Profile`, `Settings`) | P4 | Відкрито |
| BUG-DASH-009 | У разі помилки bootstrap одночасно є banner error і error toast — можливе дублювання повідомлення | P4 | Відкрито |
| BUG-DASH-010 | `GET /api/v1/categories` не тестується окремим dashboard-набором, хоча використовується для bootstrap форми add-item | P4 | Відкрито |

---

---

## 4. Модуль «Add Item» (modal-форма створення item)

**Обсяг:** frontend `AddItemModal.jsx`, `Toast.jsx`, `api.js::createItem`; backend `POST /api/v1/items`, `ItemService.create_item`, `ItemCreate`, `WarrantyCreate`, `_save_photo`, зв’язок `Item ↔ Warranty`. Форма відправляє `multipart/form-data`, де `payload` — JSON, а `photo` — optional файл.

### 4.1 Автоматизований набір тестів (pytest)

Файл: `tests/integration/test_api_items_bfs.py`  
Додатково unit: `tests/unit/test_item_schema_bfs.py`

| № | Сценарій | Файл / тест |
|---|----------|-------------|
| 1 | `POST /api/v1/items` без Bearer → 401 | `test_api_items_bfs.py::test_bfs_api_items_create_requires_auth_401` |
| 2 | Успішне створення item без фото і без гарантії → 201, коректне тіло відповіді | `test_api_items_bfs.py::test_bfs_api_items_create_minimal_item_201` |
| 3 | Успішне створення item з гарантією → `warranty` присутня у відповіді | `test_api_items_bfs.py::test_bfs_api_items_create_with_warranty_201` |
| 4 | Невалідний JSON у полі `payload` → 422 | `test_api_items_bfs.py::test_bfs_api_items_create_invalid_payload_json_422` |
| 5 | Порожній `name` у payload → 422 від Pydantic-схеми `ItemCreate` | `test_api_items_bfs.py::test_bfs_api_items_create_empty_name_422` |
| 6 | Негативний `purchase_price` → 422 | `test_api_items_bfs.py::test_bfs_api_items_create_negative_price_422` |
| 7 | Гарантія без `expiry_date` → 422 | `test_api_items_bfs.py::test_bfs_api_items_create_warranty_without_expiry_422` |
| 8 | Неіснуючий `category_id` → 404 `Category not found` | `test_api_items_bfs.py::test_bfs_api_items_create_unknown_category_404` |
| 9 | Завантаження фото зберігає `photo_path` і повертає item | `test_api_items_bfs.py::test_bfs_api_items_create_with_photo_persists_photo_path` |
| 10 | Після створення item dashboard-лічильники мають збільшитися | `test_api_items_bfs.py::test_bfs_api_items_create_updates_dashboard_counts` |

### 4.2 Smoke-тестування (ручні сценарії)

| ID smoke | Дія | Очікуваний результат |
|----------|-----|----------------------|
| SM-ITEM-01 | Натиснути `Add Item` на dashboard | Відкривається modal `Add New Item` |
| SM-ITEM-02 | Перевірити заголовок modal | Заголовок чорний, кнопка `×` видима |
| SM-ITEM-03 | Натиснути `Cancel` | Модальне вікно закривається |
| SM-ITEM-04 | Натиснути `×` | Модальне вікно закривається |
| SM-ITEM-05 | Відкрити modal і не заповнювати `Inventory Name`, натиснути `Save` | Показується помилка `Inventory name is required.` |
| SM-ITEM-06 | Відкрити список `Category` | Відображаються категорії, отримані з API |
| SM-ITEM-07 | Ввести `Purchase Price` як додатне десяткове число | Поле приймає значення і submit проходить |
| SM-ITEM-08 | Ввести від’ємну ціну | Бекенд відхиляє запит, UI показує помилку |
| SM-ITEM-09 | Заповнити `Description` довільним текстом | Item зберігається з описом |
| SM-ITEM-10 | Натиснути `Upload Photo` і вибрати зображення | Назва кнопки замінюється на ім’я вибраного файлу |
| SM-ITEM-11 | Натиснути `Add Warranty` | Відкривається блок полів гарантії |
| SM-ITEM-12 | Натиснути `Remove Warranty` | Блок гарантії ховається |
| SM-ITEM-13 | Увімкнути warranty, не заповнити `Warranty Expiry Date`, натиснути `Save` | Показується помилка про обов’язкову дату гарантії |
| SM-ITEM-14 | Увімкнути warranty, заповнити `Warranty Expiry Date`, зберегти | Item і warranty створюються успішно |
| SM-ITEM-15 | Після успішного save modal закривається | Користувач повертається на dashboard |
| SM-ITEM-16 | Після успішного save з’являється success toast | Toast зникає автоматично |
| SM-ITEM-17 | Після помилки від API з’являється error toast | Toast показує текст помилки |
| SM-ITEM-18 | Після створення item dashboard оновлюється без ручного reload | `Total Items` / warranty-лічильники змінюються одразу |

### 4.3 Реєстр дефектів і спостережень (префікс BUG-ITEM-)

| ID | Опис | Пріоритет | Статус |
|----|------|-----------|--------|
| BUG-ITEM-001 | Створення item без Bearer не повинно проходити | P1 | Закрито (автотест №1) |
| BUG-ITEM-002 | Мінімальний валідний item без гарантії має успішно створюватися | P1 | Закрито (автотест №2) |
| BUG-ITEM-003 | Створення item з warranty має повертати пов’язану warranty у відповіді | P1 | Закрито (автотест №3, SM-ITEM-14) |
| BUG-ITEM-004 | Невалідний JSON у `payload` має давати 422, а не 500 | P2 | Закрито (автотест №4) |
| BUG-ITEM-005 | Порожня назва item має відхилятися на UI і бекенді | P1 | Закрито (автотест №5, SM-ITEM-05) |
| BUG-ITEM-006 | Від’ємна ціна не повинна зберігатися | P2 | Закрито (автотест №6, SM-ITEM-08) |
| BUG-ITEM-007 | Warranty без `expiry_date` не повинна проходити | P2 | Закрито (автотест №7, SM-ITEM-13) |
| BUG-ITEM-008 | Неіснуюча категорія має давати 404 `Category not found` | P2 | Закрито (автотест №8) |
| BUG-ITEM-009 | Завантаження фото має зберігати шлях до файлу без падіння сервера | P2 | Закрито (автотест №9, SM-ITEM-10) |
| BUG-ITEM-010 | Після створення item dashboard-лічильники мають оновлюватися без ручного reload | P2 | Закрито (автотест №10, SM-ITEM-18) |
| BUG-ITEM-011 | `Upload Photo` і `Add Warranty` мають бути візуально уніфіковані за висотою / padding | P4 | Закрито |
| BUG-ITEM-012 | `photo_path` зараз повертається як файловий шлях сервера (`./media/...`), а не як публічний URL | P3 | Відкрито |
| BUG-ITEM-013 | На бекенді немає серверної перевірки MIME-type / extension фото; `accept="image/*"` є лише UX-обмеженням браузера | P2 | Відкрито |
| BUG-ITEM-014 | На бекенді немає обмеження розміру upload-файлу | P2 | Відкрито |
| BUG-ITEM-015 | Категорія, дата покупки і ціна є nullable на бекенді — це гнучко для MVP, але може суперечити майбутнім бізнес-вимогам | P4 | Не дефект |
| BUG-ITEM-016 | Modal не закривається кліком по overlay або клавішею Esc | P4 | Відкрито |
| BUG-ITEM-017 | Error path показує і banner, і toast, що дублює повідомлення | P4 | Відкрито |
| BUG-ITEM-018 | Після невдалого save локальна помилка форми і глобальна помилка сторінки можуть містити різний текст | P4 | Відкрито |

---

## Підсумок

- У **розділі 1** автотести покривають основні гілки API реєстрації, логіну та JWT; smoke перевіряє базову цілісність UI.
- У **розділі 2** для Settings і Categories додано smoke-набір, базовий автоматизований набір та реєстр дефектів `BUG-SET-*` / `BUG-CAT-*`.
- У **розділі 3** для dashboard додано **7 автоматизованих** та **15 ручних smoke** сценаріїв, а також дефектний реєстр `BUG-DASH-*`.
- У **розділі 4** для `Add Item` додано **10 автоматизованих** та **18 ручних smoke** сценаріїв, а також дефектний реєстр `BUG-ITEM-*`.

Дата оновлення: квітень 2026.
