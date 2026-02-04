# SQL Sorting and Ordering

[[T.O.C (Database Systems Notes)|Up to Database Systems Notes]]

#concept #sql #sorting

## 1. Sorted Data Retrieval

> **Prompt:** "Write an SQL code to view the records in increasing order of salary, then descending order. Give me explanations of both. What other keywords and commands are there for sorting retrieval of data"
> **Lens Applied:** The Optimizationist / The Chief Engineer

### Implementation
```sql
-- Increasing Order (Ascending)
SELECT * FROM employees 
ORDER BY salary ASC;

-- Decreasing Order (Descending)
SELECT * FROM employees 
ORDER BY salary DESC;
```

### 1. The ORDER BY Clause
The `ORDER BY` clause is used to sort the result-set in ascending or descending order.
*   **ASC:** (Default) Sorts from lowest to highest (1-10, A-Z).
*   **DESC:** Sorts from highest to lowest (10-1, Z-A).

### 2. Multi-Level Sorting
You can sort by multiple columns. If two employees have the same salary, you can sort them by name.
```sql
SELECT * FROM employees 
ORDER BY salary DESC, name ASC;
```

### 3. Other Sorting Keywords/Concepts
*   **NULLS FIRST / NULLS LAST:** Specifies where `NULL` values should appear in the sort.
*   **Column Index:** You can sort by position (e.g., `ORDER BY 2`), though this is considered poor practice in production code.
*   **Limit/Top:** Often used with sorting to find extremes (e.g., "Top 5 salaries").
```sql
-- MySQL/Postgres
SELECT * FROM employees ORDER BY salary DESC LIMIT 5;
```

### 4. Performance Note
Sorting is an **expensive** operation ($O(N \log N)$). Large tables should ideally be sorted using an **Index** on the column used in `ORDER BY` to avoid high CPU usage.
