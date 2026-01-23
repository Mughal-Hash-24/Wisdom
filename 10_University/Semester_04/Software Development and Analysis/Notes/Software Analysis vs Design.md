---
created: 2026-01-20 14:00
tags: [concept, cs, sda, design-patterns]
---
# Software Analysis vs Design

[[10_University/Semester_04/Software Development and Analysis/Notes/T.O.C (Software Development and Analysis Notes)|Up to SDA Notes]]

## OOP and OODA in SDA

## Gemini
**How they come together:**
Object-Oriented Programming (OOP) is the tool, while Object-Oriented Analysis and Design (OOAD) is the blueprint.
1.  **OO Analysis (OOA):** You look at the real world (the "Problem Domain") and identify the "objects." For a School System, you identify "Student," "Teacher," and "Course" as concepts, not code. You define what they *are* (attributes) and what they *do* (behaviors).
2.  **OO Design (OOD):** You take those conceptual objects and map them to software structures. You decide that "Student" will be a Class, "Name" will be a private String variable, and "Enroll()" will be a public method. You apply patterns (like Factory or Singleton) here.
3.  **OOP:** You actually write the code (`public class Student { ... }`) based on the Design.

**In SDA:** These three steps ensure that the code you write (OOP) accurately reflects the real-world problem (OOA) through a robust technical plan (OOD).

## Software Analysis
An investigation of the problem and its requirements rather than focusing on the solution.

## Gemini
**Explanation:**
Software Analysis is the "What" phase. It is purely about understanding the problem domain without worrying about *how* to solve it technically. It's about gathering facts and constraints.
*   **Simple Example:**
    *   **Scenario:** You want to build a "Smart Toaster."
    *   **Analysis:** You research *what* a toaster needs to do. It needs to toast bread, it needs different heat settings, it needs to pop up when done, and it must be safe to touch. You *don't* worry about what microchip to use or the wiring diagram yet. You just define the requirements: "Must toast bread in under 2 minutes."

## Software Design
A conceptual solution that fulfils the analysed requirements.

## Gemini
**Explanation:**
Software Design is the "How" phase. It takes the requirements from the Analysis phase and invents a solution structure. It transforms the "what" into a plan for construction.
*   **Simple Example:**
    *   **Scenario:** The "Smart Toaster" from above.
    *   **Design:** You decide *how* to make it toast bread in 2 minutes. You design the circuit diagram. You choose a specific heating element alloy. You decide to use a microcontroller to handle the timer. You draw the shape of the casing. This is the technical solution to the requirements.

## The difference

## Gemini
| Feature | Software Analysis | Software Design |
| :--- | :--- | :--- |
| **Focus** | The Problem (Problem Domain). | The Solution (Solution Domain). |
| **Question** | "What does the system need to do?" | "How will the system do it?" |
| **Output** | Requirement Specifications (SRS), Use Cases. | Architecture Documents, UML Diagrams, Tech Stack. |
| **Mindset** | Investigative / Detective. | Creative / Engineering. |
| **Example** | "The car needs an engine that goes 0-60 in 3s." | "We will use a V8 Turbo engine with this specific transmission." |
