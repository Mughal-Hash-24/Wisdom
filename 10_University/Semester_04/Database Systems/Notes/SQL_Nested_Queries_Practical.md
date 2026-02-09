[[T.O.C (Database Systems Notes)|Up to Database Systems Notes]]

> **Prompt:** "Construct various nested queries like 'I want to see employees whose dep is in new york'. Make sure to incorporate other examples matching 2 3 4 columns... Construct a query for 'List emp whose salary is more than the average salary of dept 30'. ALSO why does this query not work: [Logical Error Analysis]"
> **Lens Applied:** The Rubber Duck / The Inversionist

# SQL Nested Queries: Practical Implementation

## 1. The Laboratory: Sample Data
We use two primary tables to demonstrate relational nesting.

### Table: `Dept`
| DeptNo | Dname | Loc |
| :--- | :--- | :--- |
| 10 | ACCOUNTING | NEW YORK |
| 20 | RESEARCH | DALLAS |
| 30 | SALES | CHICAGO |

### Table: `Emp`
| EmpNo | EName | Sal | DeptNo |
| :--- | :--- | :--- | :--- |
| 7839 | KING | 5000 | 10 |
| 7782 | CLARK | 2450 | 10 |
| 7698 | BLAKE | 2850 | 30 |
| 7900 | JAMES | 950 | 30 |

## 2. Practical Examples

### Example A: Employees in New York (Relational Nesting)
```sql
SELECT EName
FROM Emp
WHERE DeptNo IN (SELECT DeptNo FROM Dept WHERE Loc = 'NEW YORK');
```
*   **Output:** `KING`, `CLARK`

### Example B: Multiple Columns (Row Constructors)
Find employees with the same Job and Salary as anyone in Dept 20.
```sql
SELECT EName, Job, Sal
FROM Emp
WHERE (Job, Sal) IN (SELECT Job, Sal FROM Emp WHERE DeptNo = 20);
```

### Example C: Scalar Comparison
List employees earning more than the average salary of Dept 30.
```sql
SELECT EName, Sal
FROM Emp
WHERE Sal > (SELECT AVG(Sal) FROM Emp WHERE DeptNo = 30);
```

---

## 3. Error Analysis: The "Implicit Grouping" Trap

### The Symptom
The following query is syntactically valid in some dialects but logically broken:
```sql
SELECT ename, sal
FROM emp
WHERE depNo = 30
GROUP BY ename, sal
HAVING sal > avg(sal)
```

### The Root Cause (Logic Analysis)
1.  **Granularity Mismatch:** By grouping by `ename` and `sal`, every group contains exactly **one distinct salary value**.
2.  **The Result of `AVG(sal)`:** Because each group is effectively a single row, the `AVG(sal)` for that group is simply equal to the `sal` of that row.
3.  **The Predicate:** The condition `sal > avg(sal)` is mathematically equivalent to `sal > sal`, which is **always false**.

### The Fix
To compare a row's value against a **global** or **departmental** average, you cannot use the `GROUP BY` of the outer query. You must use a subquery to calculate the constant average value first.

**Corrected Code:**
```sql
SELECT ename, sal
FROM emp
WHERE depNo = 30
  AND sal > (SELECT avg(sal) FROM emp WHERE depNo = 30);
```

### Dry Run (Why it fails)
1.  **Outer Query** selects Blake (2850) and James (950).
2.  **Grouping** creates Group A: {Blake, 2850} and Group B: {James, 950}.
3.  **Having Clause** for Group A: `2850 > AVG(2850)` -> `2850 > 2850` -> `FALSE`.
4.  **Having Clause** for Group B: `950 > AVG(950)` -> `950 > 950` -> `FALSE`.
5.  **Result:** Empty Set.
