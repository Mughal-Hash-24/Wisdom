---
tags:
- field/cs
- subject/cs-theory
- concept/neat/(neuroevolution
---

# NEAT (NeuroEvolution of Augmenting Topologies)
Created: 2026-01-07 01:29:12.502018

# NEAT (NeuroEvolution of Augmenting Topologies)

**Tags:** #AI #NeuralNetworks #EvolutionaryAlgorithms #GameDev #MachineLearning

## Overview
**NeuroEvolution of Augmenting Topologies (NEAT)** is a genetic algorithm (GA) for the generation of evolving artificial neural networks. developed by Kenneth Stanley and Risto Miikkulainen in 2002. Unlike traditional neural network training (which modifies weights on a fixed topology using backpropagation), NEAT evolves both the **weights** and the **topology** (structure) of the network simultaneously.

## Core Concepts

### 1. Evolving Topology
NEAT begins with the simplest possible networks (often just input and output neurons with no hidden layers). As evolution progresses, the algorithm adds complexity incrementally:
* **Add Node Mutation:** Splits an existing connection, placing a new node in between.
* **Add Connection Mutation:** Adds a new connection between two existing nodes.

This "complexification" strategy ensures that the solution is only as complex as it needs to be, optimizing performance and efficiency.

### 2. Genetic Encoding (Genotypes)
NEAT uses a specific encoding scheme to represent the network. Each genome is a list of connection genes, where each gene contains:
* In-node & Out-node
* Weight
* Enable/Disable bit
* **Innovation Number:** A historical marker that identifies the origin of a gene. This allows NEAT to crossover genomes with different topologies without losing structural integrity.

### 3. Speciation (Protecting Innovation)
One of NEAT's most critical features is **speciation**. When a topological change occurs (e.g., a new node is added), the new network typically performs worse initially than established networks because its new weights aren't optimized.
* NEAT groups similar networks into species based on their topology (compatibility distance).
* Networks compete primarily within their own species.
* This protects new structural innovations, giving them time to optimize their weights before competing with the entire population.

## Role in Game AI

NEAT is particularly prominent in Game AI and reinforcement learning tasks where a "correct" dataset (supervised learning) doesn't exist, but a fitness score (survival time, score, distance) is available.

### Advantages
* **No Backpropagation Required:** Useful for sparse reward environments.
* **Novel Strategies:** Can discover gameplay strategies that human developers might not anticipate.
* **Dynamic Adaptation:** Capable of real-time adaptation in some implementations (rtNEAT).

### Notable Examples
* **MarI/O:** A famous implementation where a NEAT-based AI learned to play Super Mario World level 1-1 without prior knowledge, eventually exploiting glitches and complex movement.
* **Flappy Bird:** A common "Hello World" for NEAT, where birds evolve to navigate pipes.

## Summary
NEAT bridges the gap between simple weight optimization and the architectural search for neural networks, making it a powerful tool for generating agents in complex, open-ended game environments.
