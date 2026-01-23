---
created: 2026-01-20 13:55
tags: [concept, cs, sda, methodologies]
---
# SDA Methodologies

[[10_University/Semester_04/Software Development and Analysis/Notes/T.O.C (Software Development and Analysis Notes)|Up to SDA Notes]]

## Overview
Various methodologies exist to guide the software development process, each with its own philosophy on planning, execution, and delivery.

## Gemini
**1. Waterfall Model**
*   **Description:** A linear, sequential approach where each phase (Requirements -> Design -> Implementation -> Verification -> Maintenance) must be completed before the next begins. Like a waterfall, you can't go back up.
*   **Example:** Construction projects or flight control software. You cannot "refactor" the foundation of a bridge halfway through. All requirements must be known upfront.

**2. Agile Methodology**
*   **Description:** An iterative approach that prioritizes flexibility, customer collaboration, and responding to change over following a rigid plan. Work is broken into small increments.
*   **Example:** A startup building a social media app. They release a basic version, see how users use it, and then add features (stories, reels) based on real feedback rather than guessing everything at the start.

**3. Scrum (An Agile Framework)**
*   **Description:** A specific implementation of Agile. It organizes work into fixed-length iterations called "Sprints" (usually 2 weeks). It has specific roles (Scrum Master, Product Owner) and ceremonies (Daily Standup, Sprint Review).
*   **Example:** A team building an e-commerce site commits to delivering the "Shopping Cart" feature in a 2-week Sprint. They meet daily for 15 minutes to sync up. At the end, they demo the cart to the stakeholder.

**4. DevOps (Development + Operations)**
*   **Description:** Not just a process, but a culture that bridges the gap between Developers (Dev) and IT Operations (Ops). It emphasizes automation (CI/CD pipelines) to release software rapidly and reliably.
*   **Example:** Facebook deploying updates thousands of times a day. When a developer pushes code, automated scripts run tests, package the app, and deploy it to servers without human intervention.

**5. Kanban**
*   **Description:** A visual workflow management method. It uses a board (To Do, Doing, Done) to visualize work and limit "Work In Progress" (WIP) to improve flow.
*   **Example:** A support team handling ticket requests. They pull a new ticket only when they finish the current one, ensuring no one is overwhelmed and tickets move smoothly across the board.
