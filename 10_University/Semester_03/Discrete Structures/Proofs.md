
---

### I. Direct Proofs

The most straightforward method. This method is used to prove conditional statements $\mathbf{p \rightarrow q}$.

| **Technique**    | **Goal**                                                                                                | **Strategy**                                                                                                                                                            | **When to Use**                                                                                                                                               |
| ---------------- | ------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Direct Proof** | To show that if the hypothesis $\mathbf{p}$ is true, the conclusion $\mathbf{q}$ **must** also be true. | 1. **Assume** $p$ is true. 2. Use definitions, axioms, and previously proven theorems to create a direct chain of logical deductions. 3. **Conclude** that $q$ is true. | When the definitions of $p$ and $q$ are easy to work with and a logical chain from $p$ to $q$ is obvious (e.g., proving the sum of two odd integers is even). |

**Example Area:** Proving that the sum of two rational numbers is rational (the proof we just worked through was a direct proof of existence).

### II. Indirect Proofs

Indirect proofs are essential when a direct path from $p$ to $q$ is complicated. They use logical equivalences to prove a different, but equivalent, statement.

#### 1. Proof by Contraposition

This is based on the logical equivalence $\mathbf{p \rightarrow q \equiv \sim q \rightarrow \sim p}$ (the contrapositive).

|**Technique**|**Goal**|**Strategy**|**When to Use**|
|---|---|---|---|
|**Contraposition**|To prove $p \rightarrow q$ is true by proving its logically equivalent **contrapositive** $\mathbf{\sim q \rightarrow \sim p}$.|1. **Assume** the negation of the conclusion ($\sim q$) is true. 2. Use a direct proof style (logical steps). 3. **Conclude** the negation of the hypothesis ($\sim p$) is true.|When $\sim q$ is a more specific or easier assumption to work with than $p$. For example, proving "If $n^2$ is even, then $n$ is even," is often easier by proving "If $n$ is odd ($\sim q$), then $n^2$ is odd ($\sim p$)."|

#### 2. Proof by Contradiction (Reductio ad Absurdum)

This is a powerful technique that can be used to prove _any_ statement $P$, not just conditional ones. It works on the principle that if assuming the opposite of $P$ leads to a falsehood, $P$ must be true.

|**Technique**|**Goal**|**Strategy**|**When to Use**|
|---|---|---|---|
|**Contradiction**|To prove statement $P$ is true.|1. **Assume** the negation of the statement ($\mathbf{\sim P}$) is true. 2. Derive a chain of logical statements from $\sim P$. 3. **Conclude** a contradiction (a statement of the form $r \land \sim r$), which is impossible. 4. Since the assumption $\sim P$ led to a contradiction, the original statement $P$ must be true.|Best for proving statements like **uniqueness** (assume two exist, find a contradiction) or **irrationality** (like proving $\sqrt{2}$ is irrational, which you will cover). It is also great when the logical negation ($\sim P$) is a very specific statement.|

### III. Proofs Involving Quantifiers

The statements you dealt with in the last turn involved quantifiers ($\forall$ and $\exists$).

|**Technique**|**Statement Type**|**Strategy**|
|---|---|---|
|**Disproof by Counterexample**|Disproving a **Universal Statement** ($\mathbf{\forall x, P(x)}$)|Find a **single** value of $x$ (the counterexample) in the domain that makes the property $P(x)$ false. This is enough to disprove the entire universal claim.|
|**Constructive Existence Proof**|Proving an **Existential Statement** ($\mathbf{\exists x, P(x)}$)|Find or construct a **specific example** $x$ that satisfies the property $P(x)$. (Your proof about the multiplicative inverse of rational numbers was a constructive existence proof once we excluded $q=0$).|
|**Non-Constructive Existence Proof**|Proving an **Existential Statement** ($\mathbf{\exists x, P(x)}$)|Prove that an object $x$ exists without actually finding it. This is often done using a proof by contradiction (assume no such $x$ exists and derive a contradiction).|

### IV. Specialized Structural Proofs

These methods deal with proving statements where the domain is too large or involves different scenarios.

|**Technique**|**Goal**|**Strategy**|**When to Use**|
|---|---|---|---|
|**Proof by Cases**|Proving a statement $\mathbf{(p_1 \lor p_2 \lor \dots \lor p_k) \rightarrow q}$.|Show that the conditional statement $p_i \rightarrow q$ is true for every single case $i$. For the proof to be valid, the cases $p_1, \dots, p_k$ must cover _all possibilities_ in the domain.|When the proof naturally splits into distinct scenarios (e.g., when a proof involves properties of even/odd numbers, positive/negative numbers, or remainders after division).|
|**Proof by Exhaustion**|A special form of proof by cases.|Check the statement against **every single element** in a **finite** (and usually small) domain.|When the domain being tested is small enough to examine individually. (e.g., proving a property for all prime numbers less than 10).|


---
---

The proofs in Chapter 4 of a typical discrete mathematics textbook generally move beyond basic conditional statements ($p \rightarrow q$) to focus on **quantified statements** (universal and existential) and other versatile **indirect proof** and **decomposition** methods.

Here is an explanation of each major aspect of proofs covered in this chapter, excluding the specific $p \rightarrow q$ structure you requested:

### 1. Proofs Involving Quantifiers

This section focuses on proving statements that apply to _all_ elements in a domain or _at least one_ element in a domain.

|**Statement Type**|**Form**|**Proof Method**|**Explanation**|
|---|---|---|---|
|**Universal**|**For all $x$, $P(x)$** ($\forall x P(x)$)|**Generalization from the Generic Particular** (A form of Direct Proof)|To prove that a property $P(x)$ holds for all elements $x$ in a set, you must choose an **arbitrary** element, say $a$, from that set. You then show, using a deductive argument, that $P(a)$ is true. Since $a$ was chosen arbitrarily, the conclusion is true for every element in the set.|
|**Existential**|**There exists an $x$ such that $P(x)$** ($\exists x P(x)$)|**Constructive Proof of Existence**|The most natural way to prove an existential statement is to produce a specific example, called a **witness**, for which the property holds. You explicitly name a value $a$ and show that $P(a)$ is true.|
|**Existential**|**There exists an $x$ such that $P(x)$** ($\exists x P(x)$)|**Non-Constructive Proof of Existence**|In some cases, you may prove that a value must exist without being able to explicitly name it. This often involves using a **Proof by Contradiction** to show that its non-existence leads to a logical inconsistency.|

---

### 2. Disproving Statements

To show that a statement is false, you must prove the negation of that statement is true.

|**Statement Type to Disprove**|**Form to Disprove**|**Method of Disproof**|**Explanation**|
|---|---|---|---|
|**Universal**|$\forall x P(x)$|**Disproof by Counterexample**|The negation of $\forall x P(x)$ is the existential statement $\exists x \neg P(x)$. To prove this negation true, you only need to find a single, specific example (a counterexample) $a$ in the domain for which $P(a)$ is false.|
|**Existential**|$\exists x P(x)$|**Proof of Universal Negation**|The negation of $\exists x P(x)$ is the universal statement $\forall x \neg P(x)$. To prove this negation, you must use a general proof method (like a Direct Proof) to show that $\neg P(x)$ is true for **all** elements $x$ in the domain.|

---

### 3. Indirect Proof Techniques (Beyond $p \rightarrow q$)

These methods prove a statement by examining what happens if the statement were false.

#### A. Proof by Contradiction

This is the most general and powerful indirect method.

- **Goal:** To prove a statement $P$ is true.
    
- **Method:**
    
    1. Assume the statement is false (i.e., assume the negation, $\neg P$, is true).
        
    2. Use logical deduction, axioms, and previously proven theorems to derive a new statement.
        
    3. Show that this new statement, or the chain of logic, leads to a **contradiction** (a statement of the form $r \land \neg r$, which is always false).
        
    4. Since the assumption $\neg P$ led to a false statement, the assumption must be false, meaning the original statement $P$ must be true.
        
- **Classic Application:** **Proving Irrationality**. To prove a number $r$ is irrational, you assume the opposite ($\neg P$), that $r$ is rational (meaning $r = a/b$ for integers $a$ and $b$ with no common factors). You then show that this assumption leads to a contradiction, such as $a$ and $b$ having a common factor, or a number being simultaneously even and odd.
    

#### B. Proof by Contraposition (Briefly Noted)

While you excluded the $p \rightarrow q$ form, this technique is a special case of indirect proof, and is often mentioned alongside contradiction.

- The statement **"If $p$, then $q$"** ($p \rightarrow q$) is logically equivalent to its **contrapositive: "If not $q$, then not $p$"** ($\neg q \rightarrow \neg p$).
    
- The method involves giving a **direct proof** of the contrapositive statement.
    

---

### 4. Proof by Cases and Exhaustion

These are forms of direct proof used when the universe of objects naturally breaks down into a few distinct categories.

#### A. Proof by Cases

Used when the hypothesis of a statement can be split into a finite number of conditions or cases ($p_1 \lor p_2 \lor \ldots \lor p_n$).

- **Goal:** To prove a conclusion $q$.
    
- **Method:**
    
    1. Show that the cases are **exhaustive** (i.e., every possible scenario falls into at least one of the cases).
        
    2. For each case $p_i$, prove the implication $p_i \rightarrow q$ separately. This is done until you have proved $q$ holds true in every possible case.
        
- **Example:** A statement about all integers can be proven by splitting the universe into the two cases: Case 1: $n$ is an **even** integer, and Case 2: $n$ is an **odd** integer. This method can handle an infinite set of objects by categorizing them into a finite number of types.
    

#### B. Proof by Exhaustion

This is a **special type of Proof by Cases** used when the entire set of objects being considered is **small and finite**.

- **Method:** The proof proceeds by literally examining (exhausting) every single possible example or scenario and verifying the statement is true for each one.
    
- **Example:** Proving a property holds for all natural numbers less than 10 would involve checking $n=1, n=2, \ldots, n=9$ individually.