# ONYX-16 PROCESSOR ARCHITECTURE REFERENCE MANUAL

**Document ID:** LM-ARCH-001
**Recovered & Restored by:** Lazarus Machinae Preservation Society — FAST University
**Classification:** Technical Preservation Archive — Complete System Specification
**Status:** Reconstructed from Recovered Schematics, Annotated Datasheets, and Partial Firmware Images

---

## FOREWORD

This document is the complete architectural specification of the ONYX-16 16-bit processor system. It was reconstructed by the Lazarus Machinae team from a combination of physical schematics, eroded datasheets, and a set of miraculously intact compiled binary payloads.

The hardware no longer exists. The task before you is to reconstruct it in software so precisely that those binary payloads execute identically to how they ran on the original silicon. This document describes every component, every electrical interface, and every behavioral rule of the system exactly as it was manufactured.

There is only one correct reconstruction. The hardware had no ambiguities — neither should yours.

---

## CHAPTER 1: SYSTEM ARCHITECTURE

The ONYX-16 is a **16-bit word machine** with **byte-level addressing**. Every memory address points to a single 8-bit byte. Instructions are 16 bits wide and therefore require two consecutive single-byte fetches from memory to load.

The minimum viable system requires the following five physical components to be assembled together:

| Component | Role |
|-----------|------|
| **Processor** | Fetches, decodes, and executes instructions from memory |
| **Memory Module** | Stores the program binary and runtime data |
| **Mainboard** | Provides the shared signal pathways and routes every bus transaction |
| **Power Supply Unit** | Provides regulated voltage; cuts power if draw exceeds capacity |
| **Graphics Adapter + Display** | Receives output bytes from MMIO and renders them to screen |

**Each component is a physically distinct, separately manufactured unit.** No two components are fused together at the factory. They are assembled at runtime by plugging them into the mainboard's physical sockets. A component that is unplugged leaves every other component unaffected.

---

## CHAPTER 2: THE STORAGE BANK

The Processor die contains a single **Storage Bank** unit. The Storage Bank is a monolithic hardware block that houses eleven individually sealed storage cells.

| Cell | Width | Purpose |
|------|-------|---------|
| R0 | 16-bit | General Purpose Register |
| R1 | 16-bit | General Purpose Register |
| R2 | 16-bit | General Purpose Register |
| R3 | 16-bit | General Purpose Register |
| R4 | 16-bit | General Purpose Register |
| R5 | 16-bit | General Purpose Register |
| R6 | 16-bit | General Purpose Register |
| R7 | 16-bit | General Purpose Register |
| PC | 16-bit | Program Counter — the byte address of the *next* instruction to fetch |
| IR | 16-bit | Instruction Register — holds the *currently executing* instruction word |
| FLAGS | 8-bit | Status Latch — encodes the outcome of the last arithmetic or comparison operation |

### 2.1 Physical Access Constraint

**Each storage cell is individually potted and sealed.** The internal charge state of a cell is not directly observable or writable from outside the unit. The Storage Bank exposes exactly two signal lines per cell to the rest of the processor:

- A **READ signal**, which places the cell's current value onto the internal data rail.
- A **WRITE signal**, which loads a new value into the cell.

There is no other interface. No cell can be probed, shorted, or reset except through these two signal lines. Any design that reaches inside a storage cell without using these signals is physically impossible and constitutes an invalid reconstruction.

**Power-On State:** All sixteen-bit cells initialize to `0x0000`. The FLAGS latch initializes to `0x00`.

### 2.2 The FLAGS Status Latch

The FLAGS register is an 8-bit status latch. Only four bits carry architectural meaning. The remaining bits must never be written by software and must be preserved across all operations.

| Bit | Mask | Name | Condition for Setting |
|-----|------|------|-----------------------|
| 0 | `0x01` | **Zero Flag (ZF)** | A comparison found both operands equal, or an arithmetic result was exactly `0`. |
| 1 | `0x02` | **Negative Flag (NF)** | A comparison found the left operand strictly less than the right operand. |
| 2 | `0x04` | **Positive Flag (PF)** | A comparison found the left operand strictly greater than the right operand. |
| 7 | `0x80` | **Halt Flag (HF)** | Set only by a thermal shutdown event. Once set, it cannot be cleared. The processor refuses to execute any further instructions. |

**Mutual exclusion rule:** ZF, NF, and PF are mutually exclusive. Setting any one of them **must** simultaneously clear the other two.

---

## CHAPTER 3: THE ARITHMETIC EXECUTION CORE (AEC)

The ONYX-16 contains a single **Arithmetic Execution Core**, the circuit responsible for all computation. It is a **stateless combinational block** — it holds no data between invocations and has no memory of previous operations.

### 3.1 Signal Interface

The AEC receives the following inputs at each invocation:

1. An **operation selector** (derived from the instruction opcode).
2. **Operand A** — a 16-bit value (the destination register's current value).
3. **Operand B** — a 16-bit value (the source register's current value, or zero for unary ops).
4. A **direct wired connection to the FLAGS latch** inside the Storage Bank.

The AEC produces exactly one output:

- A **16-bit result value** — written back to the destination register by the Control Unit.

**The FLAGS latch connection is not an output pin.** It is a permanent internal wire. The AEC mutates the FLAGS latch directly and silently as a side-effect of execution. The circuit that invoked the AEC does not receive a separate flags signal — it simply reads the FLAGS latch afterward and finds it already updated.

### 3.2 Operation Table

| Operation | Input Used | Result Written to Register? | FLAGS Updated |
|-----------|------------|-----------------------------|---------------|
| **ADD** | A + B | Yes | ZF only |
| **SUB** | A − B | Yes | ZF only |
| **MUL** | A × B | Yes | ZF only |
| **DIV** | A ÷ B | Yes | ZF only |
| **AND** | A & B | Yes | ZF only |
| **OR** | A \| B | Yes | ZF only |
| **XOR** | A ^ B | Yes | ZF only |
| **NOT** | ~A (B unused) | Yes | ZF only |
| **INC** | A + 1 (B unused) | Yes | ZF only |
| **DEC** | A − 1 (B unused) | Yes | ZF only |
| **CMP** | A vs B (no value produced) | **No** | ZF, NF, PF — full update |

**DIV by zero:** If Operand B is zero, the hardware does not fault. The result is silently forced to `0x0000`.

**Overflow:** All arithmetic is unsigned 16-bit. Results wrap silently on overflow.

**ZF update rule for arithmetic operations:** After any non-CMP operation, if the result word is `0x0000`, ZF is set. Otherwise, ZF is cleared.

**CMP flag update rules:**
- If A == B → Set ZF, clear NF and PF.
- If A < B → Set NF, clear ZF and PF.
- If A > B → Set PF, clear ZF and NF.

CMP does not produce a numeric result. No register writeback occurs.

---

## CHAPTER 4: THE SYSTEM PATHWAYS

The ONYX-16 mainboard contains three **System Pathways** — the signal conduits through which every memory transaction travels. These pathways are not manufactured as separate components. **They are copper traces etched directly into the mainboard substrate during fabrication.**

**Physical Consequence:** If the mainboard is destroyed, the pathways are destroyed with it. A pathway cannot be manufactured, purchased, transported, or mounted independently. The pathways exist only as long as, and only as part of, the mainboard. Any reconstruction that allows a pathway to exist outside of a mainboard, or to be created before a mainboard exists, is architecturally incorrect.

| Pathway | Width | Function |
|---------|-------|----------|
| **Address Pathway** | 16-bit | Carries the target memory address for the pending transaction |
| **Data Pathway** | 8-bit | Carries the data byte being read from or written to memory |
| **Control Pathway** | 2 signal lines | **READ ENABLE** and **WRITE ENABLE** — only one may be asserted at a time |

### 4.1 Bus Transaction Protocol

Every memory access — whether issued by the Processor, the bootloader, or any bus master — follows this exact sequence:

**For a READ transaction:**
1. Write the target address to the **Address Pathway**.
2. Assert the **READ ENABLE** line on the Control Pathway.
3. The mainboard completes routing and places the retrieved byte onto the **Data Pathway**.
4. The READ ENABLE line is de-asserted automatically by the mainboard after the transaction.

**For a WRITE transaction:**
1. Write the target address to the **Address Pathway**.
2. Write the data byte to the **Data Pathway**.
3. Assert the **WRITE ENABLE** line on the Control Pathway.
4. The mainboard routes the byte to the target destination.
5. The WRITE ENABLE line is de-asserted automatically by the mainboard after the transaction.

**Only one transaction may occur per clock pulse.** The pathways are not shared concurrently. A second transaction must wait for the first to complete.

---

## CHAPTER 5: THE MEMORY MODULE

The ONYX-16 uses a single flat **Memory Module**. It is a separately manufactured unit that plugs into a dedicated slot on the mainboard.

| Property | Value |
|----------|-------|
| **Total Capacity** | 3,840 bytes |
| **Valid Address Range** | `0x0000` – `0x0EFF` (inclusive) |
| **Cell Width** | 8 bits (byte-addressed) |
| **Power-On State** | All cells initialized to `0x00` |

**Out-of-Bounds Access:** Any read or write targeting an address of `0x0F00` or higher constitutes a **Segmentation Fault**. On an invalid read, the Data Pathway floats to `0xFF`. On an invalid write, the data is discarded. In both cases, a hardware fault diagnostic message is emitted.

The Memory Module does not implement the MMIO address intercept. It only ever sees addresses it is legally authorized to service. The routing decision — whether a given address reaches the Memory Module or not — is made exclusively by the mainboard's address decoder (see Chapter 6).

---

## CHAPTER 6: THE ADDRESS MAP AND MMIO DECODER

The mainboard contains a **hardware address decoder** that inspects every bus transaction before forwarding it. The complete physical address map of the ONYX-16 is as follows:

| Address Range | Size | Region | Routed To |
|---------------|------|--------|-----------|
| `0x0000` – `0x07FF` | 2,048 bytes | **Code Segment** | Memory Module |
| `0x0800` – `0x0EFF` | 1,792 bytes | **Data Segment** | Memory Module |
| `0x0F00` – `0x0FEF` | — | **Fault Zone** | Segmentation Fault — no valid device |
| `0x0FF0` | 1 byte | **Keyboard Character Port** | I/O Panel — READ only |
| `0x0FF1` | 1 byte | **Display Character Port** | Graphics Adapter — WRITE only |
| `0x0FF2` | 1 byte | **Display Integer Port** | Graphics Adapter — WRITE only |
| `0x0FF3` | 1 byte | **Keyboard Integer Port** | I/O Panel — READ only |

### 6.1 MMIO Interception Rule

When the address decoder detects a transaction targeting addresses `0x0FF0` through `0x0FF3`, **it intercepts the transaction before it reaches the Memory Module.** The Memory Module never sees these addresses. The mainboard redirects the transaction directly to the appropriate peripheral hardware.

This interception is performed inside the mainboard itself. No external circuit, no Processor logic, and no Memory Module logic participates in this decision. The mainboard is the sole authority.

### 6.2 Peripheral Port Contracts

| Port | Direction | Contract |
|------|-----------|----------|
| `0x0FF0` | READ | Returns the ASCII byte value of the next character in the keyboard input buffer. If the buffer is empty, the mainboard suspends the clock and waits for the user to provide input before completing the transaction. |
| `0x0FF1` | WRITE | The written byte is treated as an ASCII character code and forwarded directly to the display for rendering. |
| `0x0FF2` | WRITE | The written byte is treated as an unsigned 8-bit integer. The mainboard converts it to its decimal digit string and writes each ASCII character to the display sequentially. Example: writing `0x2A` (decimal 42) renders the characters `'4'` then `'2'`. |
| `0x0FF3` | READ | Reads and parses a complete decimal integer token from the keyboard buffer. Returns the parsed value as an unsigned 8-bit result. If the buffer is empty, the mainboard suspends the clock and waits for input. |

---

## CHAPTER 7: THE PERIPHERAL UNITS

### 7.1 The I/O Panel (Keyboard)

The keyboard is a separate physical chassis component. It maintains an internal **FIFO input buffer**. When polled and the buffer is empty, the keyboard unit emits a `[Hardware Interrupt]` diagnostic and blocks until the user types a line of text, which it then enqueues into the buffer character by character, followed by a space delimiter.

**Electrical interface exposed to the mainboard:**

| Signal | Direction | Behavior |
|--------|-----------|----------|
| `PENDING_INPUT` | Output pin | Driven HIGH when the buffer contains at least one non-whitespace character. The mainboard reads this pin before deciding whether to suspend execution. |
| `READ_CHAR` | Triggered by mainboard | Pops and returns the next non-whitespace byte from the buffer as an 8-bit ASCII value. |
| `READ_INT` | Triggered by mainboard | Parses and consumes the next complete decimal integer token from the buffer. Returns an 8-bit unsigned value. Leading and trailing whitespace is discarded automatically. |

### 7.2 The Graphics Adapter

The Graphics Adapter is a separate physical card that plugs into the mainboard's expansion slot. It receives raw byte payloads from the mainboard's MMIO interceptor and translates them for the connected display.

The Graphics Adapter requires a **Display Unit to be physically connected to its output port.** If no display is connected, all received payloads are silently discarded.

**Electrical interface exposed to the mainboard:**

| Signal | Triggered By | Behavior |
|--------|--------------|----------|
| `CHAR_PAYLOAD` | Write to `0x0FF1` | Forwards the received byte directly to the display as a single ASCII character. |
| `INT_PAYLOAD` | Write to `0x0FF2` | Converts the received byte to a decimal digit string and sends each character to the display sequentially. |

### 7.3 The Phosphor Display

The Phosphor Display is a **32-column × 16-row** CRT screen. It maintains an internal string buffer. Characters accumulate in the buffer as they arrive from the Graphics Adapter during program execution.

The buffer is **not flushed to the screen automatically** during execution. The display renders its entire buffer exactly once — at the explicit conclusion of program execution — inside a bordered phosphor-green terminal frame. Lines longer than 32 characters wrap to the next row. Rows beyond 16 are clipped.

---

## CHAPTER 8: THE PROCESSOR

The Processor is a single-chip unit. It contains four internal sub-units:

| Internal Sub-Unit | Role |
|-------------------|------|
| **Storage Bank** | Holds all registers (Chapter 2) |
| **Arithmetic Execution Core** | Performs all computation (Chapter 3) |
| **Block Cache** | 16-byte high-speed prefetch buffer (Section 8.1) |
| **Instruction Decode Matrix** | Decodes instructions and drives the execution datapath (Section 8.2) |

### 8.1 Physical Bus Dependency

The Processor has **three physical connector ports** on its underside that mate with the three system pathways on the mainboard. **These ports carry no voltage until the Processor is physically seated in a mainboard socket.** Without a connected mainboard:

- The Processor cannot read from or write to memory.
- The Processor cannot receive input or produce output.
- The Processor cannot execute any instruction.

When the Processor is seated, the mainboard drives the Address, Data, and Control pathway pins into the Processor's connector ports. The Processor then holds a live reference to all three pathways for the duration of its installation. **The Processor does not own these pathways** — they belong to the mainboard and continue to exist if the Processor is removed.

### 8.2 The Block Cache

Embedded in the Processor die is a **16-byte block cache**. It mirrors a single contiguous 16-byte block from main memory to reduce repeated bus transactions during instruction fetching.

| Property | Value |
|----------|-------|
| **Block size** | 16 bytes |
| **Number of blocks** | 1 (single-block, direct-mapped) |
| **Base address register** | Records the starting address of the block currently loaded |
| **Valid bit** | A single flag indicating whether the cache currently holds valid data |

**Cache hit:** A requested byte address falls within `[base, base + 16)` **and** the valid bit is set. The byte is returned directly from the cache without a bus transaction.

**Cache miss:** Either the valid bit is not set, or the requested address falls outside the cached block. The Processor issues a bus read transaction to the mainboard, retrieves the byte, and the cache is updated with a fresh 16-byte block starting at the aligned boundary.

**Cache invalidation:** Any write transaction to an address within the currently cached block immediately clears the valid bit.

### 8.3 The Instruction Decode Matrix

The Instruction Decode Matrix is a fixed 256-entry lookup table burned into the Processor at manufacture time. It is indexed by the 8-bit **opcode** field of an instruction. Each entry in the table is a **signal vector** — a collection of boolean and selector flags that dictates exactly how the execution datapath should behave for that instruction.

The signal vector for any given opcode specifies:

| Signal | Type | Meaning |
|--------|------|---------|
| `IS_VALID` | bool | Whether this opcode is recognized. Invalid opcodes emit a hardware fault and abort the cycle. |
| `USES_AEC` | bool | Whether the Arithmetic Execution Core should be invoked. |
| `AEC_OPERATION` | enum | Which operation the AEC should perform (ADD, SUB, MUL, etc.). |
| `IS_MEMORY_READ` | bool | Whether the cycle should read a byte from memory via the bus. |
| `IS_MEMORY_WRITE` | bool | Whether the cycle should write a byte to memory via the bus. |
| `IS_BRANCH` | bool | Whether the PC should be conditionally or unconditionally redirected. |
| `BRANCH_ON_ZERO` | bool | If branching, only branch when ZF is set. |
| `BRANCH_ON_NOT_ZERO` | bool | If branching, only branch when ZF is clear. |
| `WRITES_TO_REGISTER` | bool | Whether the result of this cycle should be written back to the destination register. |
| `IS_4BIT_IMMEDIATE` | bool | Whether the operand is a 4-bit immediate packed into the instruction word (Format B). |
| `IS_16BIT_IMMEDIATE` | bool | Whether the operand is a 16-bit immediate requiring a second word fetch (Format D). |

**The Decode Matrix eliminates all branching logic from the execution engine.** The execution datapath reads the signal vector and mechanically follows its flags — it never inspects the opcode itself. All semantic intelligence is pre-burned into the table at construction time.

### 8.4 The Fetch-Decode-Execute Cycle

Each clock tick drives the Processor through exactly one complete instruction cycle:

**Step 1 — FETCH (Two bus reads):**
1. Place the current value of `PC` on the Address Pathway. Assert READ ENABLE. Receive the **high byte** from the Data Pathway.
2. Place `PC + 1` on the Address Pathway. Assert READ ENABLE. Receive the **low byte** from the Data Pathway.
3. Assemble the 16-bit instruction word: `instruction = (highByte << 8) | lowByte`.
4. Write the assembled word into the `IR` register.

**Step 2 — INCREMENT PC:**
Advance `PC` by 2 (one instruction word = two bytes). This happens *before* decode so that any branch instruction in the decode phase calculates offsets relative to the next instruction, not the current one.

**Step 3 — DECODE:**
Extract the opcode from bits `[15:8]` of `IR`. Look up the signal vector in the Decode Matrix.

If `IS_16BIT_IMMEDIATE` is set (Format D instruction), the Decode Matrix triggers two additional bus reads at the *current* `PC` to fetch the 16-bit immediate payload word. `PC` is then advanced by an additional 2 bytes.

**Step 4 — EXECUTE:**
The datapath follows the signal vector mechanically:
- If `USES_AEC`: invoke the AEC with the selected operation and operands; update FLAGS via the direct latch connection.
- If `IS_MEMORY_READ`: place the source register's value on the Address Pathway, assert READ

<thinking>
The user wants me to continue the document from where it was cut off. I was in the middle of Step 4 — EXECUTE in Section 8.4 The Fetch-Decode-Execute Cycle. Let me continue from there.

I was at:
"- If `IS_MEMORY_READ`: place the source register's value on the Address Pathway, assert READ"

Let me continue from there and complete:
- Step 4 EXECUTE (finish)
- Step 5 WRITEBACK
- Chapter 9: The Mainboard
- Chapter 10: System Assembly Protocol
- Appendix A: Instruction Set Reference
- Appendix B: Instruction Encoding Formats


- Appendix C: Assembly Language Reference

Now I'm moving into the assembly language reference section to document the syntax and usage patterns for the instruction set.
</thinking>

Continuing exactly from the cut-off point:

---

- If `IS_MEMORY_READ`: place the source register's value on the Address Pathway, assert READ ENABLE, receive the byte from the Data Pathway. That byte becomes the execution result.
- If `IS_MEMORY_WRITE`: place the pointer register's value on the Address Pathway, place the source register's value on the Data Pathway, assert WRITE ENABLE.
- If `IS_BRANCH`: check the `BRANCH_ON_ZERO` and `BRANCH_ON_NOT_ZERO` signals against the current ZF. If neither is set, the branch is unconditional. If the condition is satisfied, load the target register's value directly into `PC`, overwriting it.
- If `IS_4BIT_IMMEDIATE`: the execution result is the 4-bit immediate value packed into the lower nibble of the instruction word. No bus transaction occurs.
- If `IS_16BIT_IMMEDIATE`: the execution result is the 16-bit value fetched during the decode step. No further bus transaction occurs.

**Step 5 — WRITEBACK:**
If `WRITES_TO_REGISTER` is set in the signal vector, write the execution result into the destination register (identified by bits `[7:4]` of the instruction word).

**Halt Condition:**
Before each cycle begins, the Processor checks the HF bit (`0x80`) of the FLAGS latch. If it is set, the Processor silently refuses to execute and the clock loop terminates.

---

## CHAPTER 9: THE MAINBOARD

The Mainboard is the central chassis of the system. It performs two roles simultaneously: it **owns** the System Pathways physically, and it **routes** every bus transaction that travels through them.

### 9.1 Component Sockets

The Mainboard exposes the following physical slots. Each slot is either empty or occupied by exactly one component at a time. A component plugged into a slot does not become part of the mainboard — it remains a separate, independently manufactured unit that can be removed without damaging anything else.

| Socket | Accepts | Notes |
|--------|---------|-------|
| **CPU Socket** | Processor | Upon insertion, the mainboard immediately drives the Address, Data, and Control pathway pins into the Processor's connector ports. |
| **RAM Slot** | Memory Module | The Memory Module receives all standard address-range transactions. |
| **Expansion Slot** | Graphics Adapter | Receives MMIO write payloads from the address decoder. |
| **ATX Power Connector** | Power Supply Unit | Without a connected PSU, the system has no power and all clock pulses are suppressed. |
| **I/O Panel Connector** | Keyboard | Polled by the address decoder on MMIO read transactions. |

**A socket with nothing installed is a floating pin.** If the address decoder routes a transaction to an unoccupied slot, the Data Pathway floats to `0x00` on reads, and writes are silently discarded. No crash occurs.

### 9.2 The Hardware Clock — `pulseClock()`

The mainboard exposes a single public signal line: `pulseClock()`. This is the heartbeat of the entire system. **Every bus transaction in the entire machine is completed by calling `pulseClock()` exactly once.**

No component other than the mainboard performs any routing. No component directly accesses another component. The Processor never speaks to the Memory Module directly. The Processor never speaks to the Keyboard directly. The Processor places values on the pathway pins, asserts a control signal, and calls `pulseClock()`. The mainboard does everything else.

`pulseClock()` behavior:

```
chips/chips/motherboard/Motherboard.h#L1-5
If the system has no power: return immediately, do nothing.

Otherwise:
  Read the current address from the Address Pathway.

  If READ ENABLE is asserted:
    Run the address through the MMIO decoder (Chapter 6).
    Route the read to the correct peripheral or Memory Module.
    Place the returned byte on the Data Pathway.
    De-assert READ ENABLE.

  Else if WRITE ENABLE is asserted:
    Run the address through the MMIO decoder.
    Route the write to the correct peripheral or Memory Module.
    De-assert WRITE ENABLE.
```

### 9.3 The Power Supply and the Power Trip

The Power Supply Unit plugs into the mainboard's ATX connector. It carries a maximum wattage capacity set at manufacture time. The PSU holds a **back-reference to the mainboard it is connected to** — not the other way around.

On each clock cycle, the total power draw of active components is polled and passed to the PSU. If the total draw exceeds the PSU's rated capacity, the PSU calls `killPower()` on the mainboard through its stored back-reference. This sets the system power flag to false, which causes all subsequent `pulseClock()` calls to return immediately, permanently halting execution.

**The PSU does not own the mainboard.** It holds a reference to it. The mainboard exists before the PSU is connected and continues to exist in its current state after the PSU trips. Only the power flag changes.

---

## CHAPTER 10: THE SYSTEM ASSEMBLY PROTOCOL

The ONYX-16 system must be assembled in the following exact sequence. Each step reflects a physical action: manufacturing a component, connecting a wire, or inserting a card into a slot.

**Phase 1 — Manufacture all components independently.**
Each of the following units must be constructed as a standalone, self-contained unit, in no particular order. None of them communicate with each other yet:

- Processor
- Memory Module
- Power Supply Unit (rated at 400W)
- Graphics Adapter
- Phosphor Display
- Keyboard
- Mainboard

**Phase 2 — Wire the display to the Graphics Adapter.**
Connect the Phosphor Display's input cable to the Graphics Adapter's output port. This connection is made at the chassis level, not through the mainboard.

**Phase 3 — Install components into the Mainboard.**
Plug each component into the mainboard in the following order. Each insertion may trigger immediate handshake logic:

1. **Processor** → CPU Socket. The mainboard immediately connects its pathway pins to the Processor's connector ports.
2. **Memory Module** → RAM Slot.
3. **Power Supply** → ATX Connector. The system now has power.
4. **Graphics Adapter** → Expansion Slot.
5. **Keyboard** → I/O Panel Connector.

**Phase 4 — The Bootloader Flash Sequence.**
Before any instruction can execute, the compiled binary must be physically written into RAM via bus transactions. The bootloader performs this using `pulseClock()` directly:

1. Flash the **Code Segment** byte-by-byte starting at address `0x0000`. Each 16-bit instruction word requires two consecutive write transactions (high byte first, then low byte).
2. Flash the **Data Segment** byte-by-byte starting at address `0x0800`. Same two-write-per-word protocol.

**Phase 5 — The Master Clock Loop.**
With RAM loaded, the clock loop begins. On each iteration:

1. Peek at the two bytes at the current `PC` address using two read transactions through `pulseClock()`.
2. If both bytes are `0x00` (the word `0x0000`), the end-of-program marker has been reached. Halt.
3. Otherwise, trigger one full Fetch-Decode-Execute cycle on the Processor.
4. Repeat until halted or until the maximum tick safety limit is reached.

**Phase 6 — Post-Execution.**
After the loop terminates:
1. Dump the final register state of the Processor.
2. Call `flushDisplay()` on the Phosphor Display to render all buffered output.

---

## APPENDIX A: INSTRUCTION SET REFERENCE

The ONYX-16 ISA contains 13 distinct opcodes. Each instruction accepts operands in one of three encoding formats (see Appendix B). The ISA supports two dialects: the original **Urdu Assembly** dialect and the preserved **English** transliteration. Both compile to identical machine code.

| Opcode | Urdu Mnemonic | English Mnemonic | Format | Operation Description |
|--------|--------------|-----------------|--------|-----------------------|
| `0x00` | `AARAM` | `NOP` | A | No operation. A full instruction word of `0x0000` also signals end-of-program to the bootloader. |
| `0x01` | `JAMA` | `ADD` | A | `R[dest] = R[dest] + R[src]`. Updates ZF. |
| `0x02` | `TAFREEK` | `SUB` | A | `R[dest] = R[dest] - R[src]`. Updates ZF. |
| `0x03` | `ZARAB` | `MUL` | A | `R[dest] = R[dest] * R[src]`. Updates ZF. |
| `0x04` | `TAQSEEM` | `DIV` | A | `R[dest] = R[dest] / R[src]`. Updates ZF. Result is `0` if `R[src]` is zero. |
| `0x0A` | `MUWAZANA` | `CMP` | A | Compare `R[dest]` against `R[src]`. No register writeback. Updates ZF, NF, and PF. |
| `0x10` | `CHHALANG` | `JMP` | A | `PC = R[src]`. Unconditional jump. The dest nibble is unused (set to 0). |
| `0x11` | `AGAR_SIFAR` | `JZ` | A | If `ZF = 1`: `PC = R[src]`. Jump if the last comparison was equal. The dest nibble is unused. |
| `0x12` | `AGAR_MAUJOOD` | `JNZ` | A | If `ZF = 0`: `PC = R[src]`. Jump if the last comparison was *not* equal. The dest nibble is unused. |
| `0x1A` | `BHARO` | `LDR_IMM` | B | `R[dest] = imm4`. Loads a 4-bit immediate value (range `0x0` to `0xF`). Single-word instruction. |
| `0x1B` | `BHARO` | `LDR_IMM` | D | `R[dest] = imm16`. Loads a full 16-bit immediate value. Two-word instruction (see Appendix B). Used for all values above `0x000F` and for all label addresses. |
| `0x20` | `PARHO` | `LDR` | A | `R[dest] = Memory[R[src]]`. Loads one byte from the address held in `R[src]` into `R[dest]`. |
| `0x21` | `RAKHO` | `STR` | A | `Memory[R[src]] = R[dest]`. Writes the value in `R[dest]` to the address held in `R[src]`. The dest nibble carries the value; the src nibble carries the pointer. |

**Important note on `BHARO` / `LDR_IMM`:** The assembler automatically selects Format B or Format D based on the magnitude of the immediate value. Any immediate value from `0` to `15` uses Format B (single word). Any value above `15`, any hex literal above `0x000F`, and all label references unconditionally use Format D (two words). The programmer does not select the format — the assembler does.

---

## APPENDIX B: INSTRUCTION ENCODING FORMATS

All instructions on the ONYX-16 are encoded in one of three physical formats. The format is determined by the opcode and is pre-defined in the Decode Matrix — it is not programmer-selectable.

### Format A — Standard Two-Register (Single Word)

Used by all arithmetic, comparison, memory, and branch instructions.

```
/dev/null/format-a.txt#L1-5
Bit Layout (16 bits):
[ 15 ........... 8 ] [ 7 ... 4 ] [ 3 ... 0 ]
[    OPCODE (8)    ] [ DEST (4)] [ SRC  (4)]

Total size: 2 bytes (1 word)
```

- **OPCODE** (bits 15–8): 8-bit operation selector.
- **DEST** (bits 7–4): Index of the destination register (0–7). For branch instructions, this nibble is `0` and is ignored.
- **SRC** (bits 3–0): Index of the source register (0–7). For `STR`, this is the pointer register; the value register is in the DEST nibble.

### Format B — 4-bit Immediate (Single Word)

Used exclusively by `BHARO` / `LDR_IMM` when the immediate value fits in 4 bits.

```
/dev/null/format-b.txt#L1-5
Bit Layout (16 bits):
[ 15 ........... 8 ] [ 7 ... 4 ] [ 3 ... 0 ]
[    OPCODE (8)    ] [ DEST (4)] [ IMM4 (4)]

Total size: 2 bytes (1 word)
Opcode: 0x1A
```

- **IMM4** (bits 3–0): The literal 4-bit unsigned integer to load. Range: `0x0` to `0xF`.

### Format D — 16-bit Immediate (Two Words)

Used by `BHARO` / `LDR_IMM` when the immediate value exceeds 4 bits, or when the operand is a label address.

```
/dev/null/format-d.txt#L1-9
Bit Layout — Word 1 (Header, 16 bits):
[ 15 ........... 8 ] [ 7 ... 4 ] [ 3 ... 0 ]
[    OPCODE (8)    ] [ DEST (4)] [ 0000    ]

Bit Layout — Word 2 (Payload, 16 bits):
[ 15 ............. 0 ]
[   IMM16  (16)      ]

Total size: 4 bytes (2 consecutive words)
Opcode: 0x1B
```

- **Word 1** is the header word. Its lower nibble is always zero.
- **Word 2** is the immediate payload word. It is fetched by the Control Unit during the decode phase via two additional bus reads at the current `PC`.
- After the payload is consumed, `PC` is advanced by an additional 2 bytes (past the payload word) before any branch logic can fire.

**Assembler behavior for Format D label resolution:** During Pass 1, the assembler tracks the exact byte size of every instruction (including whether a given `BHARO` will expand to Format B or D). It uses this to calculate the precise byte address of every label. In Pass 2, all label references are substituted with their resolved 16-bit byte addresses and are always encoded as Format D, regardless of the numeric value of the address.

---

## APPENDIX C: THE ONYX-16 ASSEMBLY LANGUAGE

The source language compiles to ONYX-16 machine code via a two-pass assembler. Programs are written in plain text files using either the Urdu dialect or the English dialect (both are recognized interchangeably).

### C.1 Program Structure

A source file may contain two sections, declared in order:

| Section Directive | Urdu | English | Purpose |
|------------------|------|---------|---------|
| Data section | `.MAWAAD` | `.DATA` | Static string and integer data loaded into RAM at `0x0800`. |
| Code section | `.HIDAYAT` | `.CODE` | Executable instructions loaded into RAM at `0x0000`. |

If no `.MAWAAD` / `.DATA` section is present, the file is treated as code-only. The `.HIDAYAT` / `.CODE` directive is optional if there is no data section — all lines default to code.

### C.2 Data Section Declarations

Labels in the data section map a name to a physical RAM address starting at `0x0800`. Two data types are supported:

**String literals:**
```
chips/chips/programs/hello.txt#L1-3
LABEL_NAME: "your text here\0"
```
Strings are stored as raw ASCII bytes in memory, two bytes per word, high byte first. The null terminator `\0` is stored as byte `0x00`. The newline escape `\n` is stored as byte `0x0A`. The address of `LABEL_NAME` resolves to the first byte of the string.

**Integer values:**
```
chips/chips/programs/auth.txt#L4-4
LABEL_NAME: 42
```
A single integer is stored as one 16-bit word. Comma-separated lists store multiple words consecutively.

### C.3 Code Section Instructions

All mnemonics follow the pattern `MNEMONIC DEST, SRC`. Commas are optional and are stripped by the assembler. The `[bracket]` syntax around a register denotes an indirect memory reference (the register holds an address, not a value).

| Syntax Pattern | Example | Meaning |
|----------------|---------|---------|
| `MNEMONIC Rd, Rs` | `JAMA R1, R2` | Operate on two registers |
| `MNEMONIC Rd, [Rs]` | `PARHO R1, [R5]` | Load: `R1 = Memory[R5]` |
| `MNEMONIC Rd, [Rs]` | `RAKHO R1, [R6]` | Store: `Memory[R6] = R1` |
| `MNEMONIC Rd, value` | `BHARO R3, 0x0FF1` | Load immediate into register |
| `MNEMONIC Rd, LABEL` | `BHARO R0, LOOP` | Load label address into register |
| `MNEMONIC Rs` | `CHHALANG R0` | Branch to address in register |

### C.4 Labels in the Code Section

A label in the code section is declared by placing its name followed by a colon on its own line:

```
chips/chips/programs/calculator.txt#L43-44
DO_JAMA:
JAMA R1, R2
```

The label resolves to the byte address of the instruction immediately following it. Labels consume zero bytes and produce no machine code. They are resolved in Pass 1 and substituted as 16-bit immediate values in Pass 2.

### C.5 Comments

Single-line comments begin with `//`. Everything from `//` to the end of the line is ignored by the assembler.

### C.6 Assembler Pass Summary

**Pass 1 — Address Tracking:**
The assembler walks every line, tracks the current code byte address (`currentCodePC`, starting at `0x0000`) and the current data byte address (`currentDataPC`, starting at `0x0800`). It records every label name and its resolved byte address into a lookup table. It does not generate any binary output in this pass.

**Pass 2 — Binary Generation:**
The assembler walks the collected lines again. For each instruction, it encodes the correct machine word(s) using the resolved label table from Pass 1. The output is two arrays: a `codeSegment` array of 16-bit words (for loading at `0x0000`) and a `dataSegment` array of 16-bit words (for loading at `0x0800`).

---

## APPENDIX D: HARDWARE FAULT REFERENCE

The following diagnostic messages are emitted to the system console when hardware violations occur. They do not terminate the program except where noted.

| Fault Message | Trigger Condition | Effect |
|---------------|------------------|--------|
| `[HARDWARE FAULT] Segmentation Fault: Read out of bounds` | Memory Module receives a read to address ≥ `0x0F00` | Returns `0xFF`; execution continues |
| `[HARDWARE FAULT] Segmentation Fault: Write out of bounds` | Memory Module receives a write to address ≥ `0x0F00` | Write discarded; execution continues |
| `[MOTHERBOARD FAULT] Invalid Read Address` | Address decoder receives a read to an unmapped address | `0x00` placed on Data Pathway; execution continues |
| `[MOTHERBOARD FAULT] Invalid Write Address` | Address decoder receives a write to an unmapped address | Write discarded; execution continues |
| `[HARDWARE FAULT] Invalid Instruction` | Decode Matrix lookup returns `IS_VALID = false` | Cycle aborted; execution continues at next PC |
| `[CRITICAL WARNING] Power Draw exceeded PSU Capacity` | Polled wattage exceeds PSU rated capacity | PSU calls `killPower()` on the Mainboard — **permanent halt** |
| `[CRITICAL ERROR] Thermal threshold exceeded` | Processor temperature exceeds `90.0°C` | Sets HF bit in FLAGS — **permanent halt** |
| `[Hardware Interrupt] Awaiting Keyboard Input` | MMIO read to `0x0FF0` or `0x0FF3` with empty buffer | Clock suspended until user types; execution resumes after input |

---

*End of ONYX-16 Architecture Reference Manual — LM-ARCH-001*
*All specifications are binding. Deviations from this document are physical impossibilities and will result in a non-functional reconstruction.*

---

That's the complete document. Here's a summary of every "trap" quietly embedded in the hardware language, mapped to the OOP concept it forces:

| Hardware Phrase | OOP Concept Forced |
|---|---|
| *"Potted and sealed storage cells — only READ/WRITE signal lines exposed"* | `RegisterBank` needs `private` state with `public` getter/setter methods |
| *"FLAGS latch is a permanent internal wire to the AEC — not an output pin"* | `ALU::execute()` takes `uint8_t& flags` by reference, mutates it internally |
| *"Pathways are copper traces etched into the mainboard substrate — destroyed with it"* | `AddressBus`, `DataBus`, `ControlBus` are **composed** inside `Motherboard`, never created independently |
| *"The Processor does not own these pathways — they belong to the mainboard"* | `Processor` holds `AddressBus*`, `DataBus*`, `ControlBus*` pointers — **Aggregation** |
| *"The PSU holds a back-reference to the mainboard"* | `PowerSupply` holds a `Motherboard*` — also Aggregation |
| *"A component plugged into a slot remains a separate unit — removal leaves others unaffected"* | `Motherboard` holds `Processor*`, `MemoryModule*`, etc. as pointers — **Aggregation** for slots |
| *"The mainboard is the sole authority on address routing"* | All MMIO logic lives inside `Motherboard::pulseClock()` — not in CPU, not in RAM |
| *"No component directly accesses another component — only through pathway pins"* | No component holds a direct reference to another component except through `Motherboard` |
| *"The Decode Matrix eliminates all branching logic from the execution engine"* | `CU` uses a `ControlSignals microcodeROM[256]` array, not a giant `switch` block |

