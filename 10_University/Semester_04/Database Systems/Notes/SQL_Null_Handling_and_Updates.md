# SQL Null Handling and Updates

[[T.O.C (Database Systems Notes)|Up to Database Systems Notes]]

#concept #sql #nulls

## 1. Null Value Logic

> **Prompt:** "Write an SQL code that queries all the employees with no commission. How is an empty value represented in a DB. Difference between NULL and 0. Why do we consider NULL as empty and not 0 as empty."
> **Lens Applied:** The Inversionist / The Chief Engineer

### Implementation
```sql
-- Querying for "no commission"
SELECT * FROM employees 
WHERE commission IS NULL;
```

### 1. Representation of Empty Values
In a Database, an empty or unknown value is represented as **`NULL`**. It is a state, not a value.

### 2. The Difference: NULL vs. 0
| Aspect | NULL | 0 |
| :--- | :--- | :--- |
| **Meaning** | Unknown / Missing / Non-applicable | A specific quantity (Zero) |
| **Type** | Absence of value | Integer Value |
| **Logic** | `NULL + 10 = NULL` | `0 + 10 = 10` |

### 3. Why 0 is not "Empty"
Consider a Bank Account:
*   **Balance = 0:** You have an account, and it is exactly zero dollars. You are broke.
*   **Balance = NULL:** We don't know if you have money, or the system hasn't loaded your data yet.
Using `0` to mean "empty" is dangerous because `0` is a valid data point that affects averages and calculations. `NULL` is ignored by most aggregate functions (like `AVG`).

---

## 2. Nullable vs. Non-Nullable Fields

> **Prompt:** "Explain the difference between Nullable and non-nullable fields in a table with real world data"
> **Lens Applied:** The Architect

### 1. Non-Nullable (`NOT NULL`)
Columns that **must** contain data.
*   **Example:** `EmployeeID`, `National_ID`, `Email`.
*   **Reason:** These are critical for identification or system operations. You cannot have an employee without an ID.

### 2. Nullable
Columns where data is optional.
*   **Example:** `Middle_Name`, `Alternate_Phone`, `Commission`.
*   **Reason:** Not everyone has a middle name or earns commission.

---

## 3. Calculated Fields and Data Modification

> **Prompt:** "Write an SQL code to get the salary of each employee if we made a 12% increase. This serves as an example to also explain as to name the column 'New Salary'. What happens if I don't use as to name the column. What if we wanted to make the changes, what command would we use instead of SELECT and why?"
> **Lens Applied:** The Optimizationist / The Chief Engineer

### 1. The Projection (View Only)
```sql
SELECT name, salary * 1.12 AS "New Salary" 
FROM employees;
```
*   **What if no `AS`?** The column header will usually be the raw expression (e.g., `salary * 1.12`) or `computed_field`, which is unprofessional and hard to reference.

### 2. The Modification (Persistent Change)
If we wanted to actually **save** this 12% increase to the database, we would use **`UPDATE`**.
```sql
UPDATE employees 
SET salary = salary * 1.12;
```

### Why use UPDATE instead of SELECT?
*   `SELECT` only changes what the **user sees**. The data on the disk remains the same.
*   `UPDATE` physically changes the bits on the disk (the **Data Manipulation**). 
*   **Risk:** `SELECT` is safe. `UPDATE` without a `WHERE` clause will change the salary for *every single employee* in the company. Always use `SELECT` to verify your logic before running an `UPDATE`.
