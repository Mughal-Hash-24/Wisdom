[[T.O.C (Database Systems Notes)|Up to Database Systems Notes]]

> **Prompt:** "Explain the detailed concept of Nested queries in SQL with syntax cases and common errors... What are the scenarios in which a nested query can be used. What are the limitations. Discuss in detail"
> **Lens Applied:** The Chief Engineer / First Principles

# Deep Dive: SQL Nested Queries (Subqueries)

## 1. Ontological Definition
A **Nested Query** (or Subquery) is a `SELECT` statement embedded within another SQL query. It allows the result of one query to be used as a parameter or data source for another, enabling complex logic that single-level queries cannot express.

## 2. Scenarios & Syntax Cases

### A. Scalar Subqueries (Returns a single value)
Used in `SELECT`, `WHERE`, or `HAVING` clauses.
*   **Scenario:** Compare a value against an aggregate (e.g., "find everyone paid more than the average").
*   **Syntax:** `WHERE col > (SELECT AVG(col) FROM table)`

### B. Row/List Subqueries (Returns a set of values)
Used with operators like `IN`, `ANY`, `ALL`, or `EXISTS`.
*   **Scenario:** Filter based on membership in another set.
*   **Syntax:** `WHERE id IN (SELECT id FROM other_table WHERE condition)`

### C. Table Subqueries (Derived Tables)
Used in the `FROM` clause.
*   **Scenario:** Treating a query result as a temporary table to perform further operations (like secondary aggregation).
*   **Syntax:** `FROM (SELECT ...) AS temp_table`

### D. Correlated Subqueries
A subquery that references columns from the outer query. It is executed once for every row processed by the outer query.
*   **Scenario:** "Find employees whose salary is higher than the average salary *of their own department*."
*   **Syntax:** `WHERE sal > (SELECT AVG(s2.sal) FROM emp s2 WHERE s2.deptNo = s1.deptNo)`

## 3. Systems Context: Performance & Mechanics
*   **Execution Flow:** Non-correlated subqueries are executed once. Correlated subqueries are $O(N 	imes M)$, where $N$ is outer rows and $M$ is inner rows.
*   **Optimizer:** Modern database engines (PostgreSQL, SQL Server) often attempt to **Flatten** subqueries into `JOIN` operations to improve performance.

## 4. Limitations & Constraints
1.  **Readability:** Deeply nested queries (3+ levels) become "Write-Only" code—impossible to maintain.
2.  **Performance:** Large-scale correlated subqueries can paralyze a database.
3.  **Scope:** Subqueries cannot use `ORDER BY` unless they also use `TOP` or `LIMIT` (varies by dialect), as the set is unordered by definition.
4.  **Single Column Rule:** A subquery used with comparison operators ($=, <, >$) must return exactly one column and one row.

## 5. Common Errors
*   **Subquery returns more than 1 value:** Using `=` instead of `IN`.
*   **Ambiguous Column Names:** Forgetting to alias tables when referencing them in nested levels.
*   **Null Handling:** `NOT IN` with a subquery that returns a `NULL` value will result in an empty set for the entire outer query (due to Three-Valued Logic).
