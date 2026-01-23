Union of Subspaces Analysis Using Augmented Matrices

## Part (a): S₁ = Span{(1, 2, 1)} and S₂ = Span{(1, 5, -1), (2, 7, 0)}

### Step 1: Check if S₁ ⊆ S₂ using augmented matrix

To determine if (1, 2, 1) ∈ S₂, we solve:
c₁(1, 5, -1) + c₂(2, 7, 0) = (1, 2, 1)

**Set up augmented matrix:**
```
[1  2 | 1]
[5  7 | 2]
[-1 0 | 1]
```

**Row reduction:**

Step 1: R₂ → R₂ - 5R₁, R₃ → R₃ + R₁
```
[1   2 | 1]
[0  -3 | -3]
[0   2 | 2]
```

Step 2: R₂ → -1/3 × R₂
```
[1   2 | 1]
[0   1 | 1]
[0   2 | 2]
```

Step 3: R₃ → R₃ - 2R₂
```
[1   2 | 1]
[0   1 | 1]
[0   0 | 0]
```

Step 4: Back substitution - R₁ → R₁ - 2R₂
```
[1   0 | -1]
[0   1 | 1]
[0   0 | 0]
```

**Solution:** c₁ = -1, c₂ = 1

**Verification:** 
(-1)(1, 5, -1) + (1)(2, 7, 0) = (-1, -5, 1) + (2, 7, 0) = (1, 2, 1) ✓

**Conclusion:** Since the system is consistent, (1, 2, 1) ∈ S₂, therefore **S₁ ⊆ S₂**.

### Step 2: Conclusion for Part (a)
Since S₁ ⊆ S₂, by the theorem: **S₁ ∪ S₂ = S₂ is a subspace**.

---

## Part (b): S₁ = Span{(1, 0, 0)} and S₂ = Span{(1, 1, 0), (0, 1, 1)}

### Step 1: Check if S₁ ⊆ S₂ using augmented matrix

To determine if (1, 0, 0) ∈ S₂, we solve:
c₁(1, 1, 0) + c₂(0, 1, 1) = (1, 0, 0)

**Set up augmented matrix:**
```
[1  0 | 1]
[1  1 | 0]
[0  1 | 0]
```

**Row reduction:**

Step 1: R₂ → R₂ - R₁
```
[1  0 | 1]
[0  1 | -1]
[0  1 | 0]
```

Step 2: R₃ → R₃ - R₂
```
[1  0 | 1]
[0  1 | -1]
[0  0 | 1]
```

**Analysis:** The last row gives us 0 = 1, which is impossible.

**Conclusion:** The system is **inconsistent**, so (1, 0, 0) ∉ S₂, therefore **S₁ ⊄ S₂**.

### Step 2: Check if S₂ ⊆ S₁ using augmented matrix

We need to check if both spanning vectors of S₂ are in S₁.

**Check if (1, 1, 0) ∈ S₁:**
S₁ = Span{(1, 0, 0)} = {t(1, 0, 0) : t ∈ ℝ}

For (1, 1, 0) = t(1, 0, 0), we need:
```
1 = t  →  t = 1
1 = 0  →  Impossible!
0 = 0  →  Always true
```

Since 1 ≠ 0, (1, 1, 0) ∉ S₁.

**Conclusion:** **S₂ ⊄ S₁**.

### Step 3: Show S₁ ∪ S₂ is not a subspace using augmented matrix approach

Since neither subspace contains the other, we expect S₁ ∪ S₂ to fail closure under addition.

**Find counterexample vectors:**
- u = (1, 0, 0) ∈ S₁
- v = (1, 1, 0) ∈ S₂

**Sum:** u + v = (2, 1, 0)

**Check if (2, 1, 0) ∈ S₁:**
For (2, 1, 0) = t(1, 0, 0):
- 2 = t → t = 2
- 1 = 0 → Impossible!

So (2, 1, 0) ∉ S₁.

**Check if (2, 1, 0) ∈ S₂ using augmented matrix:**
Solve: c₁(1, 1, 0) + c₂(0, 1, 1) = (2, 1, 0)

**Set up augmented matrix:**
```
[1  0 | 2]
[1  1 | 1]
[0  1 | 0]
```

**Row reduction:**

Step 1: R₂ → R₂ - R₁
```
[1  0 | 2]
[0  1 | -1]
[0  1 | 0]
```

Step 2: R₃ → R₃ - R₂
```
[1  0 | 2]
[0  1 | -1]
[0  0 | 1]
```

**Analysis:** The last row gives us 0 = 1, which is impossible.

**Conclusion:** (2, 1, 0) ∉ S₂, so **(2, 1, 0) ∉ S₁ ∪ S₂**.

### Final Conclusion for Part (b)
Since u, v ∈ S₁ ∪ S₂ but u + v ∉ S₁ ∪ S₂, **S₁ ∪ S₂ fails closure under addition** and is **NOT a subspace**.

---

## Additional Analysis: Understanding S₂ in Part (b)

Let's use augmented matrix to find the general form of vectors in S₂.

Any vector in S₂ has the form: v = c₁(1, 1, 0) + c₂(0, 1, 1) = (c₁, c₁ + c₂, c₂)

**Alternative approach - Find the constraint defining S₂:**

If (x, y, z) ∈ S₂, then (x, y, z) = (c₁, c₁ + c₂, c₂) for some c₁, c₂.

From this:
- x = c₁
- y = c₁ + c₂ = x + c₂, so c₂ = y - x
- z = c₂ = y - x

Therefore: **z = y - x**, or equivalently: **x - y + z = 0**

We can verify this constraint:
- (1, 1, 0): 1 - 1 + 0 = 0 ✓
- (0, 1, 1): 0 - 1 + 1 = 0 ✓

So S₂ = {(x, y, z) : x - y + z = 0}, which is indeed a plane.

**Verify our counterexample:**
- (1, 0, 0): 1 - 0 + 0 = 1 ≠ 0, so (1, 0, 0) ∉ S₂ ✓
- (2, 1, 0): 2 - 1 + 0 = 1 ≠ 0, so (2, 1, 0) ∉ S₂ ✓

---

## Summary Using Augmented Matrix Method

### Part (a): Union IS a subspace
- **Augmented matrix showed:** S₁ ⊆ S₂ (consistent system)
- **Result:** S₁ ∪ S₂ = S₂ (a plane)

### Part (b): Union is NOT a subspace
- **Augmented matrices showed:** 
  - S₁ ⊄ S₂ (inconsistent system)
  - S₂ ⊄ S₁ (direct verification)
- **Counterexample found:** (1,0,0) + (1,1,0) = (2,1,0) ∉ S₁ ∪ S₂
- **Result:** Closure under addition fails

The augmented matrix method provides a systematic way to check containment relationships and verify subspace properties through solving linear systems.