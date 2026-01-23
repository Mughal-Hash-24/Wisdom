Here is a detailed description of the conditional jump instructions, focusing on their "back working" with the CPU flags.

## The Core Concept: `CMP` and the `EFLAGS` Register

These jump instructions almost never work alone. They are designed to be used _after_ an instruction that sets the CPU's `EFLAGS` register, most commonly the `CMP` (Compare) instruction.

When you do:

CMP eax, ebx

The CPU performs a "pretend" subtraction: `eax - ebx`. It **does not save the result**, but it **sets a group of flags** based on what that result _would have been_.

The most important flags for jumps are:

- **`ZF` (Zero Flag):** Set if the result was 0. (i.e., `eax == ebx`).
    
- **`SF` (Sign Flag):** Set if the result was negative (i.e., the most significant bit was 1).
    
- **`CF` (Carry Flag):** Set if an _unsigned_ operation needed a borrow (i.e., `eax < ebx` in an unsigned sense).
    
- **`OF` (Overflow Flag):** Set if a _signed_ operation's result overflowed (e.g., `(positive) - (negative) = (negative)`).
    

The specific jump instruction you choose (`jl`, `jb`, etc.) tells the CPU which _combination_ of these flags to check.

---

## The Big Division: Signed vs. Unsigned

This is the most critical concept to understand. The CPU doesn't know if `0xFF` means `255` (unsigned) or `-1` (signed). You tell it how to interpret the numbers by which jump you use.

- **Signed Jumps (`g`/`l`):** Use `g` (Greater) and `l` (Less). These are for comparing signed numbers that can be positive or negative. They check the **Sign Flag (`SF`)** and **Overflow Flag (`OF`)**.
    
- **Unsigned Jumps (`a`/`b`):** Use `a` (Above) and `b` (Below). These are for comparing unsigned numbers that are always positive (like memory addresses, sizes, or array indices). They check the **Carry Flag (`CF`)**.
    

---

## Group 1: Signed Jumps (Arithmetic)

These are used for comparing signed numbers.

### `jl` (Jump if Less)

- **Mnemonic:** Jump if **L**ess.
    
- **Opposite:** `jge` (Jump if Greater or Equal).
    
- **Description:** Jumps if the `destination` is less than the `source` (signed).
    
- **Back Working:** It jumps if the **Sign Flag is not equal to the Overflow Flag (`SF != OF`)**.
    
    - **Why?** This is the magic for signed comparison.
        
        - **Case 1 (No Overflow, `OF=0`):** We want a negative result, so we want `SF=1`. This matches `1 != 0`.
            
        - **Case 2 (Overflow, `OF=1`):** An overflow happened (e.g., `-2147483648 - 1`). The result _should be_ negative, but it wrapped around and _looks_ positive (`SF=0`). This also matches `0 != 1`.
            

### `jle` (Jump if Less or Equal)

- **Mnemonic:** Jump if **L**ess or **E**qual.
    
- **Opposite:** `jg` (Jump if Greater).
    
- **Description:** Jumps if the `destination` is less than or equal to the `source` (signed).
    
- **Back Working:** It jumps if **(`SF != OF`) OR (`ZF == 1`)**.
    
- **Explanation:** It's the same logic as `jl`, but _also_ jumps if the Zero Flag is set (meaning the operands were equal).
    

### `jg` (Jump if Greater)

- **Mnemonic:** Jump if **G**reater.
    
- **Opposite:** `jle` (Jump if Less or Equal).
    
- **Description:** Jumps if the `destination` is greater than the `source` (signed).
    
- **Back Working:** It jumps if **(`SF == OF`) AND (`ZF == 0`)**.
    
- **Explanation:** This is the opposite of `jle`. It wants a positive result _and_ for the operands to not be equal. `SF == OF` is the logic for "positive" in signed-overflow math, and `ZF=0` ensures they aren't equal.
    

### `jge` (Jump if Greater or Equal)

- **Mnemonic:** Jump if **G**reater or **E**qual.
    
- **Opposite:** `jl` (Jump if Less).
    
- **Description:** Jumps if the `destination` is greater than or equal to the `source` (signed).
    
- **Back Working:** It jumps if **`SF == OF`**.
    
- **Explanation:** This is the opposite of `jl`. It jumps if the result is positive _or_ zero. The `SF == OF` logic handles all "positive" cases (with or without overflow), and it inherently works for zero as well (where `SF=0`, `OF=0`).
    

---

## Group 2: Unsigned Jumps (Logical)

These are used for comparing unsigned numbers (like addresses or sizes). They are much simpler and only care about the Carry and Zero flags.

The logic is simple: `CMP A, B` sets the **Carry Flag (`CF`)** if a borrow is needed (i.e., if `A < B`).

### `jb` (Jump if Below)

- **Mnemonic:** Jump if **B**elow.
    
- **Also called:** `jc` (Jump if Carry), `jnae` (Jump if Not Above or Equal).
    
- **Opposite:** `jae` (Jump if Above or Equal).
    
- **Description:** Jumps if the `destination` is less than the `source` (unsigned).
    
- **Back Working:** It jumps if **`CF == 1`**.
    
- **Explanation:** The Carry Flag is set, meaning a borrow _was_ required for `A - B`. This means `A` was smaller than `B`.
    

### `jbe` (Jump if Below or Equal)

- **Mnemonic:** Jump if **B**elow or **E**qual.
    
- **Also called:** `jna` (Jump if Not Above).
    
- **Opposite:** `ja` (Jump if Above).
    
- **Description:** Jumps if the `destination` is less than or equal to the `source` (unsigned).
    
- **Back Working:** It jumps if **(`CF == 1`) OR (`ZF == 1`)**.
    
- **Explanation:** It jumps if a borrow was needed (`CF=1`) _or_ if the result was zero (`ZF=1`).
    

### `ja` (Jump if Above)

- **Mnemonic:** Jump if **A**bove.
    
- **Also called:** `jnbe` (Jump if Not Below or Equal).
    
- **Opposite:** `jbe` (Jump if Below or Equal).
    
- **Description:** Jumps if the `destination` is greater than the `source` (unsigned).
    
- **Back Working:** It jumps if **(`CF == 0`) AND (`ZF == 0`)**.
    
- **Explanation:** No borrow was needed (`CF=0`), so `A >= B`. We also check that they aren't equal (`ZF=0`). This means `A` must be strictly greater than `B`.
    

### `jae` (Jump if Above or Equal)

- **Mnemonic:** Jump if **A**bove or **E**qual.
    
- **Also called:** `jnb` (Jump if Not Below), `jnc` (Jump if No Carry).
    
- **Opposite:** `jb` (Jump if Below).
    
- **Description:** Jumps if the `destination` is greater than or equal to the `source` (unsigned).
    
- **Back Working:** It jumps if **`CF == 0`**.
    
- **Explanation:** No borrow was needed, so `A` must be greater than or equal to `B`.
    

---

## Example: Signed vs. Unsigned in Action

Let's compare -1 and 5.

In a 32-bit register (like eax), -1 is represented as 0xFFFFFFFF.

Code snippet

```
.data
    is_less_msg  DB "Signed: -1 is less than 5", 0
    is_above_msg DB "Unsigned: 0xFFFFFFFF is above 5", 0

.code
main PROC
    mov eax, 0xFFFFFFFF  ; -1 (signed), 4,294,967,295 (unsigned)
    mov ebx, 5           ;  5 (signed), 5 (unsigned)

    cmp eax, ebx         ; Performs (eax - ebx).
                         ; Sets SF=1, OF=0, CF=1, ZF=0

    ; --- Signed Check ---
    jl handle_less       ; Jumps because SF != OF (1 != 0)

    ; --- Unsigned Check ---
    ja handle_above      ; Jumps because CF=0 and ZF=0 ... 
                         ; **Wait!** My flag check was wrong.
                         ; (0xFFFFFFFF - 5) *DOES* borrow. CF=1.
                         ; Let's re-run the `cmp`
                         ; `cmp 0xFFFFFFFF, 5`
                         ; `CF` *is* set to 1. 
                         ; My text for `ja` is correct (CF=0),
                         ; so `ja` will *NOT* jump.

    ; Let's fix the example to be more clear.
    ; Let's compare 10 and 5.
    
    mov eax, 10
    mov ebx, 5
    cmp eax, ebx        ; (10 - 5). Sets ZF=0, CF=0, SF=0, OF=0

    ; Signed check
    jg signed_greater   ; Jumps because (SF==OF) and (ZF==0)
                        ; (0 == 0) and (0 == 0) -> TRUE

    ; Unsigned check
    ja unsigned_above   ; Jumps because (CF==0) and (ZF==0)
                        ; (0 == 0) and (0 == 0) -> TRUE
    
    ; --- Now let's do the -1 vs 5 example ---
    mov eax, 0xFFFFFFFF  ; -1
    mov ebx, 5
    cmp eax, ebx         ; (-1 - 5). Result is -6. 
                         ; No signed overflow.
                         ; Flags: SF=1, OF=0, ZF=0
                         ; Unsigned (0xFFFFFFFF - 5) *borrows*.
                         ; Flags: CF=1

    ; Signed check:
    jl signed_less       ; Jumps? (SF != OF) -> (1 != 0) -> TRUE. 
                         ; Yes, jumps to signed_less.

    ; Unsigned check:
    ja unsigned_above    ; Jumps? (CF == 0) AND (ZF == 0)
                         ; (1 == 0) AND (0 == 0) -> FALSE.
                         ; Does NOT jump.
    
    ; Unsigned check 2:
    jb unsigned_below    ; Jumps? (CF == 1) -> (1 == 1) -> TRUE.
                         ; Yes, jumps to unsigned_below.

signed_less:
    ; We'd print "-1 is less than 5"
    jmp done

unsigned_above:
    ; This code is not reached
    jmp done

unsigned_below:
    ; We'd print "0xFFFFFFFF is below 5"
    jmp done

signed_greater:
    ; ...
    jmp done
    
unsigned_above:
    ; ...
    jmp done

done:
    ; ...
```

This example shows how `cmp` sets the flags, and then _you_ decide which ones to test (signed or unsigned) by picking the correct jump instruction.