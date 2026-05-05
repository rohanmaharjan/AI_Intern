# 📊 MySQL Data Engineering Mini Project  
### Multi-Table System + API Change Detection Monitor

---

## 🚀 Project Overview

This project demonstrates two advanced data engineering tasks using **Python + MySQL**:

- **Task A:** Multi-table relational database system (`store_db`)
- **Task B:** API monitoring system with change detection (`monitor_db`)

---

# 🟩 Task A · Multi-Table Relational System

## 📌 Objective
Design a relational database with proper relationships and perform analytical queries.

---

## 🧱 Database Design

### Tables:

#### customers
- id (Primary Key)
- name
- city

#### products
- id (Primary Key)
- name
- price

#### orders
- id (Primary Key)
- customer_id (Foreign Key → customers.id)
- product_id (Foreign Key → products.id)
- quantity

---

## 🔗 Relationships
- One customer → Many orders  
- One product → Many orders  
- Orders acts as a junction table  

---

## 💡 Key Concepts Learned

### 1. Relational Database Design
- Normalization
- Primary Key & Foreign Key usage
- Referential integrity

---

### 2. Parameterized Queries
```python
cursor.execute(
    "INSERT INTO customers (name, city) VALUES (%s, %s)",
    (name, city)
)
```

---

### 3. SQL joins
```SQL
SELECT c.name, SUM(p.price * o.quantity) AS total_spent
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN products p ON o.product_id = p.id
GROUP BY c.name
ORDER BY total_spent DESC;
```

---

### 5. GROUP BY + HAVING
```SQL
SELECT c.name, COUNT(o.id)
FROM orders o
JOIN customers c ON o.customer_id = c.id
GROUP BY c.name
HAVING COUNT(o.id) > 2;
```

---