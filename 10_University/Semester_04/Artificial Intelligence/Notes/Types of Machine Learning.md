---
created: 2026-01-21
tags: [concept, cs, ai, ml]
related: [[AI vs ML vs DL]]
---
# Types of Machine Learning

[[T.O.C (Artificial Intelligence Notes)|Up to AI Notes]]

## Overview
Machine Learning is generally categorized by how the system learns from data: with supervision, without supervision, or via interaction with an environment.

## Gemini

### The Three Main Types

#### 1. Supervised Learning
The model is trained on **labeled data**. You show it the input (X) and the correct answer (Y). It learns to map X to Y.
*   **Task:** Classification (Is this a cat or dog?) or Regression (Predict the price of this house).
*   **Real World Example:**
    *   **Medical Diagnosis:** Training a system with X-rays (input) and doctor's diagnosis (label: "Tumor" or "No Tumor") to detect cancer automatically.

#### 2. Unsupervised Learning
The model is given **unlabeled data**. It must find structure, patterns, or relationships on its own.
*   **Task:** Clustering (Group similar items) or Association (People who bought X also bought Y).
*   **Real World Example:**
    *   **Customer Segmentation:** A bank analyzes customer data (spending habits) without predefined labels to find groups like "Student Savers" or "High-Income Spenders" for targeted marketing.

#### 3. Reinforcement Learning (RL)
The agent learns by interacting with an environment. It takes actions and receives **rewards** or **punishments**. It aims to maximize cumulative reward.
*   **Task:** Navigation, Game Playing, Control Systems.
*   **Real World Example:**
    *   **AlphaGo:** It played millions of games of Go against itself. Winning was a reward, losing was a punishment. It learned strategies no human had ever taught it.

### Types of Reinforcement Learning
RL is further divided based on how the agent learns:

*   **Model-Based RL:** The agent tries to build a "model" of how the world works (e.g., "If I do action A, state B happens"). It plans using this model.
    *   *Example:* A robot learning to walk by simulating physics.
*   **Model-Free RL:** The agent doesn't learn the physics; it just learns the value of actions (Q-Learning) or policies directly.
    *   *Example:* A video game bot that just knows "Jump when you see a pit" without understanding gravity.
*   **Policy Optimization:** The agent learns a policy function (map of state -> action) directly.
*   **Q-Learning:** The agent learns a value function (how good is it to be in this state?).

## Connections
- [[AI vs ML vs DL]]
- [[AI Subfields and Concepts]]
