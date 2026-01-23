## 1. How floats are represented

### Single precision (`REAL4` / `float` in C, 32 bits)

- **1 bit** → sign (0 = positive, 1 = negative)
    
- **8 bits** → exponent (with bias of 127)
    
- **23 bits** → fraction (the mantissa, without the leading 1)
    

So a `REAL4` number is stored as:

`SEEEEEEE EFFFFFFFFFFFFFFFFFFFFFF`

### Double precision (`REAL8` / `double`, 64 bits)

- **1 bit** → sign
    
- **11 bits** → exponent (bias = 1023)
    
- **52 bits** → fraction
    

### Extended precision (`REAL10` in MASM, 80 bits)

Used by the x87 FPU internally.

- 1 sign bit
    
- 15 exponent bits (bias = 16383)
    
- 64 fraction bits (with explicit leading 1)
    

That’s why old MASM examples sometimes show `fld tbyte ptr [var]` for highest precision.

---

## 2. Example: `3.5` as a float (REAL4)

- Binary value: `3.5 = 11.1₂`
    
- Normalized: `1.11 × 2¹`
    
    - Sign = 0 (positive)
        
    - Exponent = 1 + bias 127 = 128 → `1000 0000`
        
    - Mantissa = `.11` → `1100…` padded
        

So in hex:

`3.5f = 0x40600000`

Stored in memory (little endian on x86):

`00 00 60 40`

---

## 3. Negative example: `-2.25` as float

- `2.25 = 10.01₂ = 1.001 × 2¹`
    
- Sign = 1
    
- Exponent = 1 + 127 = 128 → `1000 0000`
    
- Mantissa = `001…`
    

Hex:

`-2.25f = 0xC0100000`

In memory (little endian):

`00 00 10 C0`

---

## 4. Declaring floats in MASM

`.data f1 REAL4 3.5      ; 32-bit float f2 REAL8 -2.25    ; 64-bit double f3 REAL10 1.2345  ; 80-bit extended precision`

The assembler automatically encodes the IEEE-754 binary pattern into those bytes in your data segment.

---

## 5. Loading into FPU

MASM uses x87 instructions (`fld`, `fstp`, etc.):

`fld f1       ; load REAL4 into ST(0) fld f2       ; load REAL8 into ST(0) fld f3       ; load REAL10 into ST(0)`

Internally, the FPU converts them into its 80-bit registers, even if they were stored as 32-bit or 64-bit.

---

## 6. Edge cases to know

- `0.0` has all bits zero.
    
- `-0.0` has sign bit = 1, everything else zero.
    
- Exponent all 1’s + nonzero fraction → NaN (Not a Number).
    
- Exponent all 1’s + fraction = 0 → ±Infinity.
    
- Exponent all 0’s + nonzero fraction → denormalized numbers (for tiny values close to 0).
    

---

So: **floats are just integers in disguise** — a carefully packed bit pattern that represents sign, exponent, and fraction. MASM doesn’t do runtime math when you write `REAL4 3.5`; it precomputes the bit pattern (`00 00 60 40`) and dumps that into your `.data` section.