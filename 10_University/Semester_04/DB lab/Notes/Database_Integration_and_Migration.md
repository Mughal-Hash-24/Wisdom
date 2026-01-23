---
created: 2026-01-22 14:40
tags: [concept, architecture, integration, migration]
related: [[Three_Tier_Architecture]]
---
# Database Integration & Migration

[[T.O.C (DB lab Notes)|Up to DB Lab Notes]]

## The Kernel Architect: Systems Integration
**Context:** Heterogeneous Enterprise Environments.

### 1. The Applications of Databases
Databases are not just for websites.
*   **OLTP (Online Transaction Processing):** Banking, E-commerce. High frequency, small writes. (ACID is King).
*   **OLAP (Online Analytical Processing):** Data Warehousing, BI. Low frequency, massive reads.
*   **Embedded Systems:** SQLite in Android/iOS apps, Firmware configuration.
*   **Real-Time Systems:** Telecommunications, Stock Trading (Time-series DBs like Kdb+).

---

## 2. Integration Flows: The Babel Tower
How do different technologies talk to the Database?

#### Scenario: The Enterprise Spaghetti
We have a **Web Client**, an **IIS Server** (Microsoft), a **Java App**, and **Oracle Forms** all needing data.

1.  **Web Client -> IIS -> MS SQL Server**
    *   **The Stack:** C# (.NET Core).
    *   **Driver:** ADO.NET / Entity Framework.
    *   **Flow:** Browser (JS) -> IIS (C# Controller) -> `System.Data.SqlClient` -> TCP Port 1433 -> MS SQL.
2.  **Java Application -> Oracle DB**
    *   **The Stack:** JVM.
    *   **Driver:** JDBC (Java Database Connectivity).
    *   **Flow:** App -> `DriverManager.getConnection()` -> `ojdbc8.jar` (Socket implementation) -> TCP Port 1521 -> Oracle.
3.  **Oracle Forms -> SQL Plus -> Oracle DB**
    *   **The Stack:** Legacy Middleware.
    *   **Driver:** SQL*Net (TNS).
    *   **Flow:** Forms Runtime -> TNS Listener -> Dedicated Server Process -> DB File.

#### Integration Diagram
```mermaid
graph TD
    subgraph Clients
        WC[Web Client (React)]
        JA[Java Desktop App]
        OF[Oracle Forms App]
    end
    
    subgraph Middleware
        IIS[IIS / ASP.NET]
    end
    
    subgraph Drivers
        ADO[ADO.NET]
        JDBC[JDBC Driver]
        SQLPlus[SQL*Plus / TNS]
    end
    
    subgraph Databases
        MSSQL[(MS SQL Server)]
        ORA[(Oracle DB)]
    end
    
    WC --> IIS
    IIS --> ADO
    ADO --"Port 1433"--> MSSQL
    
    JA --> JDBC
    JDBC --"Port 1521"--> ORA
    
    OF --> SQLPlus
    SQLPlus --"IPC / TCP"--> ORA
```

---

## 3. Database Migration
Moving data from System A to System B. This is one of the riskiest operations in engineering.

#### Types of Migration
1.  **Big Bang:**
    *   Shutdown System A.
    *   Copy *everything* to System B.
    *   Point Apps to System B.
    *   Start System B.
    *   *Risk:* High downtime. If it fails, you are dead in the water.
2.  **Trickle (Phased) Migration:**
    *   Run System A and B in parallel.
    *   Use **CDC (Change Data Capture)** to replicate updates from A to B in real-time.
    *   Slowly move read traffic to B.
    *   Eventually switch write traffic.
    *   *Risk:* Data consistency (Race conditions).

#### The Migration Pipeline (ETL)
1.  **Extract:** Read data from Source (CSV, Old DB, API).
    *   *Challenge:* Handling encoding (ASCII vs UTF-8), Legacy formats (COBOL Copybooks).
2.  **Transform:** Cleanse and Normalize.
    *   *Example:* Convert "M/F" in Old DB to "Male/Female" in New DB.
    *   *Example:* Split "FullName" into "FirstName, LastName".
3.  **Load:** Bulk insert into Target DB.
    *   *Optimization:* Disable Indexes/Constraints during load for speed, rebuild them after.

#### Real World Example: On-Prem to Cloud
Moving a 10TB Oracle DB from a basement server to AWS RDS.
1.  **Schema Conversion Tool (SCT):** Converts PL/SQL procedures to pgSQL (if moving to Postgres).
2.  **Database Migration Service (DMS):** Replicates the data.
3.  **Cutover:** A 5-minute window at 3 AM Sunday to switch the DNS to point to AWS.
