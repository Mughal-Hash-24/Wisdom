# Database Systems (Semester 4)
## Constructing Queries
{Given any english statement for a query construct a well defined step by step procedure of converting it to an equivalent SQL query using the following keywords:
- SELECT
- FROM
- WHERE
- GROUP BY
- HAVING
- ORDER BY

After the construction of this system perform it on 5 highly complex examples like 'I want to see all jobs having total salaries > 10000'. You can have even more complex examples}

## Nested Queries
{Explain the detailed concept of Nested queries in SQL with syntax cases and common errors}
{Consider the following tables:
TABLE 1: Emp NO, EName, DeptNo
TABLE 2: Dept No, Dname, Dep Location

Construct various nested queries like 'I want to see employees whose dep is in new york'. Make sure to incorporate other examples matching 2 3 4 columns. Explain each example in detail. Also fill in the tables with sample values and give outputs of each example query}
### More on nested queries
{What are the scenarios in which a nested query can be used. What are the limitations. Discuss in detail}

### Examples
{Construct a query for 'List emp whose salary is more than the average salary of dept 30'.
ALSO why does this query not work:
```sql
SELECT ename, sal
FROM emp
WHERE depNo = 30
GROUP BY ename, sal
HAVING sal > avg(sal)
```
This is not a syntax error but a logical error. Explain in detail with a dry run on why it doesn't work
}