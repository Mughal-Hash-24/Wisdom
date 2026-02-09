[[T.O.C (Database Systems Notes)|Up to Database Systems Notes]]

> **Prompt:** "Given any english statement for a query construct a well defined step by step procedure of converting it to an equivalent SQL query using the following keywords: SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY. After the construction of this system perform it on 5 highly complex examples..."
> **Lens Applied:** The Chief Engineer / First Principles

# Deep Dive: English-to-SQL Conversion System

## 1. Ontological Definition
The conversion of natural language to Structured Query Language (SQL) is a mapping process from a **Declarative Intent** to a **Relational Algebra Execution Plan**. SQL follows a logical processing order that differs from its syntax order.

## 2. The Conversion Procedure (The "S-F-W-G-H-O" Pipeline)

To convert an English requirement to SQL, follow this deterministic sequence:

1.  **Phase 1: Source Identification (`FROM`)**
    *   *Question:* Which tables contain the raw data?
    *   *Action:* Identify the entities mentioned. Use `JOIN` if data is split across tables.
2.  **Phase 2: Row-Level Filtering (`WHERE`)**
    *   *Question:* What are the constraints on individual records?
    *   *Action:* Apply filters that do not involve aggregations (e.g., "status is active", "date > 2023").
3.  **Phase 3: Dimensionality & Granularity (`GROUP BY`)**
    *   *Question:* Do we need "per" something? (e.g., "per department", "per year").
    *   *Action:* Group by the non-aggregated columns in the result set.
4.  **Phase 4: Group-Level Filtering (`HAVING`)**
    *   *Question:* Are there constraints on the sums, counts, or averages?
    *   *Action:* Apply filters on aggregate results (e.g., "total sales > 10,000").
5.  **Phase 5: Attribute Selection (`SELECT`)**
    *   *Question:* What specific columns or calculations are needed in the final output?
    *   *Action:* Project the columns and apply aggregate functions (`SUM`, `AVG`, `COUNT`).
6.  **Phase 6: Final Presentation (`ORDER BY`)**
    *   *Question:* What is the sorting priority?
    *   *Action:* Specify columns and direction (`ASC`/`DESC`).

## 3. Complex Examples

### Example 1: "Total salaries per job for jobs where total salary exceeds 10,000"
*   **FROM:** `Employees`
*   **GROUP BY:** `Job_Title`
*   **HAVING:** `SUM(Salary) > 10000`
*   **SELECT:** `Job_Title, SUM(Salary)`
```sql
SELECT Job_Title, SUM(Salary)
FROM Employees
GROUP BY Job_Title
HAVING SUM(Salary) > 10000;
```

### Example 2: "Average department budget for departments in New York with more than 5 employees, sorted by budget"
*   **FROM:** `Dept d JOIN Emp e ON d.id = e.dept_id`
*   **WHERE:** `d.location = 'New York'`
*   **GROUP BY:** `d.name, d.budget`
*   **HAVING:** `COUNT(e.id) > 5`
*   **SELECT:** `d.name, d.budget`
*   **ORDER BY:** `d.budget DESC`

### Example 3: "List projects that started in 2024 having more than 3 distinct roles assigned"
```sql
SELECT project_name, COUNT(DISTINCT role_id)
FROM assignments
WHERE start_date >= '2024-01-01'
GROUP BY project_name
HAVING COUNT(DISTINCT role_id) > 3;
```

### Example 4: "Find customers who placed more than 2 orders in January, whose total spend is over $500"
```sql
SELECT customer_id, SUM(total_price)
FROM orders
WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY customer_id
HAVING COUNT(order_id) > 2 AND SUM(total_price) > 500;
```

### Example 5: "Most profitable category per region where category has at least 10 items sold"
```sql
SELECT region, category, SUM(profit)
FROM sales
GROUP BY region, category
HAVING COUNT(item_id) >= 10
ORDER BY region, SUM(profit) DESC;
```

## 4. Systems Context & C++ Anchor
In C++ terms, the `WHERE` clause is equivalent to a `std::remove_if` on a raw collection, while `HAVING` is a filter applied *after* a `std::map` or `std::unordered_map` has been used to bucket/reduce the data. The `GROUP BY` is the hashing/bucketing phase.
