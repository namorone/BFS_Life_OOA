# Software Requirements Specification (SRS)
## Home Inventory & Warranty Tracker

Version: 1.0  
Date: 2026  

---

# 1. Introduction

## 1.1 Purpose

Цей документ описує вимоги до програмної системи **Home Inventory & Warranty Tracker**.

Система призначена для обліку домашніх речей, збереження інформації про гарантії, історію ремонтів та витрати, а також для управління пов’язаними документами та фотографіями.

Документ призначений для:

- команди розробників
- тестувальників
- викладачів та стейкхолдерів проєкту

---

## 1.2 Scope

Home Inventory & Warranty Tracker — це інформаційна система, яка дозволяє користувачам:

- вести облік домашнього інвентарю
- зберігати гарантійну інформацію
- відстежувати ремонти
- аналізувати витрати
- керувати медіафайлами (фото, документи, чеки)
- отримувати нагадування про закінчення гарантії
- генерувати звіти

Система допомагає користувачам ефективніше управляти своїм майном та витратами.

---

## 1.3 Definitions, Acronyms, Abbreviations

| Term | Description |
|-----|-----|
| Inventory Item | Предмет домашнього інвентарю |
| Warranty | Гарантійна інформація про предмет |
| Repair Record | Запис про ремонт |
| Receipt | Чек покупки |
| SRS | Software Requirements Specification |

---

## 1.4 References

- IEEE 830 Software Requirements Specification
- IEEE 29148 Requirements Engineering Standard

---

# 2. Overall Description

## 2.1 Product Perspective

Система є веб-додатком, який дозволяє користувачам управляти інформацією про домашні речі та витрати.

Основні підсистеми:

- Inventory Management
- Warranty Management
- Repair Management
- Expense Tracking
- Media Management
- Notification System
- Reporting System

---

## 2.2 Product Functions

Основні функції системи:

- управління інвентарем
- збереження фотографій та документів
- управління гарантіями
- облік ремонтів
- аналіз витрат
- генерація звітів
- резервне копіювання даних

---

## 2.3 User Classes

| User Type | Description |
|------|------|
| User | Основний користувач системи |

---

## 2.4 Operating Environment

Система працює у веб-браузері.

Можливий технологічний стек:

Backend:
- Python
- FastAPI

Database:
- PostgreSQL

Frontend:
- React / Vue

---

## 2.5 Constraints

Обмеження системи:

- обмежений час розробки
- невелика команда (3 учасники)
- реалізація MVP функціоналу

---

## 2.6 Assumptions and Dependencies

Передбачається:

- користувачі вводять дані вручну
- система працює як web application
- зберігання файлів можливе у файловій системі або cloud storage

---

# 3. System Features

## 3.1 User Account Management

| ID | Requirement |
|----|-------------|
| FR1 | User can register |
| FR2 | User can login |
| FR3 | User can logout |
| FR4 | User can update profile |

---

## 3.2 Inventory Management

| ID | Requirement |
|----|-------------|
| FR5 | User can add item |
| FR6 | User can edit item |
| FR7 | User can delete item |
| FR8 | User can view inventory |
| FR9 | User can view item details |
| FR10 | User can search items |
| FR11 | User can filter items |
| FR12 | User can sort inventory |

---

## 3.3 Media Management

| ID | Requirement |
|----|-------------|
| FR13 | User can upload photo |
| FR14 | User can view photo |
| FR15 | User can delete photo |
| FR16 | User can upload document |
| FR17 | User can view document |
| FR18 | User can delete document |
| FR19 | User can upload receipt |
| FR20 | User can delete receipt |

---

## 3.4 Warranty Management

| ID | Requirement |
|----|-------------|
| FR21 | User can add warranty |
| FR22 | User can edit warranty |
| FR23 | User can delete warranty |
| FR24 | User can view warranty |
| FR25 | System sends warranty reminder |

---

## 3.5 Repair Management

| ID | Requirement |
|----|-------------|
| FR26 | User can add repair record |
| FR27 | User can edit repair record |
| FR28 | User can delete repair record |
| FR29 | User can view repair history |

---

## 3.6 Expense Tracking

| ID | Requirement |
|----|-------------|
| FR30 | System tracks repair cost |
| FR31 | User can view total expenses |
| FR32 | System generates expense statistics |

---

## 3.7 Reporting

| ID | Requirement |
|----|-------------|
| FR33 | Generate inventory report |
| FR34 | Generate expense report |

---

## 3.8 Notifications

| ID | Requirement |
|----|-------------|
| FR35 | Receive warranty reminder |
| FR36 | View notifications |
| FR37 | Mark notification as read |

---

## 3.9 Data Management

| ID | Requirement |
|----|-------------|
| FR38 | Export data |
| FR39 | Import data |
| FR40 | Backup data |
| FR41 | Restore backup |

---

## 3.10 Category Management

| ID | Requirement |
|----|-------------|
| FR42 | Manage categories |
| FR43 | Add category |
| FR44 | Edit category |
| FR45 | Delete category |

---

## 3.11 Dashboard

| ID | Requirement |
|----|-------------|
| FR46 | View dashboard |

---

## 3.12 System Validation

| ID | Requirement |
|----|-------------|
| FR47 | Validate input |
| FR48 | Display error message |
| FR49 | Save item |

---

# 4. Non-Functional Requirements

## 4.1 Performance

- System response time should be less than **500 ms**.

---

## 4.2 Security

- User data must be protected.
- Authentication must be implemented.

---

## 4.3 Usability

- Interface must be intuitive.
- Main actions should require minimal steps.

---

## 4.4 Reliability

- System availability should be at least **99%**.

---

## 4.5 Scalability

- System should support increasing number of users.

---

# 5. Requirements Traceability Matrix

| Requirement | Use Case |
|-------------|----------|
| FR1 | UC1 Register |
| FR2 | UC2 Login |
| FR5 | UC5 Add Item |
| FR13 | UC13 Upload Photo |
| FR21 | UC21 Add Warranty |
| FR26 | UC26 Add Repair Record |
| FR31 | UC31 View Total Expenses |
| FR33 | UC33 Generate Inventory Report |
| FR34 | UC34 Generate Expense Report |
| FR38 | UC38 Export Data |
| FR40 | UC40 Backup Data |

---

# 6. Use Case Descriptions

## UC1 Register

Actor: User  
Description: User creates an account.

Steps:

1. User opens registration page
2. User enters credentials
3. System validates data
4. Account is created

Result:

User account is created.

---

## UC2 Login

Actor: User  

Steps:

1. User enters credentials
2. System validates credentials
3. User enters system

---

## UC3 Logout

Actor: User  

User exits system.

---

## UC4 Update Profile

User edits profile information.

---

## UC5 Add Item

User adds a new item to inventory.

---

## UC6 Edit Item

User edits item details.

---

## UC7 Delete Item

User removes item from inventory.

---

## UC8 View Inventory

User views list of items.

---

## UC9 Search Item

User searches item.

---

## UC10 Filter Items

User filters items.

---

## UC11 Sort Inventory

User sorts inventory.

---

## UC12 View Item Details

User views detailed information.

---

## UC13 Upload Photo

User uploads photo for item.

---

## UC14 View Photo

User views photo.

---

## UC15 Delete Photo

User deletes photo.

---

## UC16 Upload Document

User uploads document.

---

## UC17 View Document

User views document.

---

## UC18 Delete Document

User deletes document.

---

## UC19 Upload Receipt

User uploads purchase receipt.

---

## UC20 Delete Receipt

User deletes receipt.

---

## UC21 Add Warranty

User adds warranty information.

---

## UC22 Edit Warranty

User edits warranty.

---

## UC23 Delete Warranty

User deletes warranty.

---

## UC24 View Warranty

User views warranty details.

---

## UC25 Warranty Reminder

System notifies user about warranty expiration.

---

## UC26 Add Repair Record

User adds repair information.

---

## UC27 Edit Repair Record

User edits repair record.

---

## UC28 Delete Repair Record

User deletes repair record.

---

## UC29 View Repair History

User views repair history.

---

## UC30 Track Repair Cost

System stores repair cost.

---

## UC31 View Total Expenses

User views total expenses.

---

## UC32 Generate Expense Statistics

System generates expense statistics.

---

## UC33 Generate Inventory Report

System generates inventory report.

---

## UC34 Generate Expense Report

System generates expense report.

---

## UC35 Receive Warranty Reminder

User receives reminder.

---

## UC36 View Notifications

User views notifications.

---

## UC37 Mark Notification as Read

User marks notification as read.

---

## UC38 Export Data

User exports data.

---

## UC39 Import Data

User imports data.

---

## UC40 Backup Data

System creates backup.

---

## UC41 Restore Backup

User restores backup.

---

## UC42 Manage Categories

User manages categories.

---

## UC43 Add Category

User creates category.

---

## UC44 Edit Category

User edits category.

---

## UC45 Delete Category

User deletes category.

---

## UC46 View Dashboard

User views statistics dashboard.

---

## UC47 Validate Input

System validates input.

---

## UC48 Display Error Message

System displays error message.

---

## UC49 Save Item

System saves item.

---

## UC50 View Repair History

User views repair history.
