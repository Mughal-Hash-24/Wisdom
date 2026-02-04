# SQL Fundamentals and Retrieval

[[T.O.C (Database Systems Notes)|Up to Database Systems Notes]]

#concept #sql #dbms

## 1. The SELECT Keyword

> **Prompt:** "Explain in detail the concept if SELECT keyword in SQL."
> **Lens Applied:** The Chief Engineer / First Principles

# Technical Breakdown: SELECT (Data Projection)

### 1. Ontological Definition
The `SELECT` keyword is the primary operator for **projection** and **retrieval** in Relational Algebra. It instructs the Database Engine to extract specific columns (attributes) from one or more tables. It does *not* modify the underlying data; it creates a temporary, virtual table (the "Result Set") in memory.

### 2. The Internal Mechanics
When you execute `SELECT`, the SQL Optimizer performs several steps:
1.  **Parsing:** Validates syntax.
2.  **Binding:** Checks if the table and columns exist in the Schema.
3.  **Plan Generation:** Decides whether to use an Index Scan or a Full Table Scan.
4.  **Projection:** Filters the physical disk blocks to return only the requested fields.

---

## 2. Retrieval vs. Non-Retrieval Commands

> **Prompt:** "Explain retrieval and non retrieval commands in SQL. Use examples"
> **Lens Applied:** The Architect / Systems Thinking

### 1. Retrieval Commands (DQL)
**Data Query Language (DQL)** is used solely to fetch data.
*   **Command:** `SELECT`
*   **Nature:** Idempotent and Read-Only. It has no side effects on the persistent state of the database.

### 2. Non-Retrieval Commands (DML, DDL, DCL)
These commands modify the state, structure, or permissions of the database.
*   **DML (Data Manipulation):** `INSERT`, `UPDATE`, `DELETE`. (Changes the *rows*).
*   **DDL (Data Definition):** `CREATE`, `ALTER`, `DROP`. (Changes the *schema*).
*   **DCL (Data Control):** `GRANT`, `REVOKE`. (Changes *access*).

---

## 3. Range Queries (BETWEEN & Logical Operators)

> **Prompt:** "Write in SQL to select all employees with salary in the range 1000 and 3000. using between and logical operators. Explain each and every keyword in detail along with all the edge cases"
> **Lens Applied:** The Debugger / The Inversionist

### Implementation
```sql
-- Solution 1: Using Logical Operators
SELECT * FROM employees 
WHERE salary >= 1000 AND salary <= 3000;

-- Solution 2: Using BETWEEN
SELECT * FROM employees 
WHERE salary BETWEEN 1000 AND 3000;
```

### Keyword Breakdown
*   **BETWEEN:** A shorthand operator. **Crucial Detail:** In SQL, `BETWEEN` is **inclusive**. It is equivalent to `>= AND <=`.
*   **AND:** A logical conjunction. Both sides must evaluate to `TRUE`.

### Edge Cases & Constraints
1.  **Inclusivity:** If an employee earns exactly `1000`, they *are* included. 
2.  **NULL Values:** If an employee's salary is `NULL`, they will **not** appear in either result. `NULL` is not between any numbers.
3.  **String Ranges:** `BETWEEN` can work on strings (alphabetical order), but behavior depends on the Collation settings.

---

## 4. Multi-Condition Logic (IN vs. OR)

> **Prompt:** "Write SQL for all employees who are either clerk or analyst. All possible solutions with detailed explanations"
> **Lens Applied:** The Optimizationist

### Implementation
```sql
-- Option 1: Using OR
SELECT * FROM employees 
WHERE job = 'CLERK' OR job = 'ANALYST';

-- Option 2: Using IN (Best Practice)
SELECT * FROM employees 
WHERE job IN ('CLERK', 'ANALYST');
```

### Analysis
*   **The 'OR' Approach:** Evaluates each condition sequentially.
*   **The 'IN' Approach:** Internally optimized as a set membership check. It is cleaner to read and faster for large lists.

---

## 5. Unique Values (DISTINCT)

> **Prompt:** "Write SQL code for selecting the salaries offered by the company with the number of offerings of each. Make sure to provide all possible solutions with detailed explanations of each. Use distinct keyword"
> **Lens Applied:** The Chief Engineer

### Implementation
```sql
-- To see unique salaries offered:
SELECT DISTINCT salary FROM employees;

-- To see salary offerings and their count (The Aggregate approach):
SELECT salary, COUNT(*) as offering_count
FROM employees
GROUP BY salary;
```

### Keyword: DISTINCT
The `DISTINCT` keyword forces the engine to perform a **sort and unique** operation on the result set, removing duplicate rows.

---

## 6. Column Renaming (Aliasing)

> **Prompt:** "Explain the concept of renaming columns in query results using 'as'. Explain the implications and applications using 3 detailed examples of varying complexities"
> **Lens Applied:** The Architect

### 1. The Concept
The `AS` keyword creates an **Alias**. It changes the column header in the *output* but does not change the table definition.

### 2. Detailed Examples
1.  **Complexity: Low (Clarity)**
    ```sql
    SELECT emp_name AS "Employee Name" FROM employees;
    ```
2.  **Complexity: Medium (Calculated Fields)**
    ```sql
    SELECT salary * 1.12 AS "Adjusted_Salary" FROM employees;
    ```
3.  **Complexity: High (Self-Joins/Subqueries)**
    ```sql
    SELECT e.name AS "Manager Name" FROM employees AS e ...
    ```
    *Note: Here `AS` is used to differentiate between two instances of the same table.*
