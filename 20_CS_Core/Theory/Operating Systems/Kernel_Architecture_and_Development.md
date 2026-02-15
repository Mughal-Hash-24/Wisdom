---
tags:
- field/cs
- subject/software-engineering
- concept/kernel/architecture
---

[[T.O.C (Operating Systems)|Up to Operating Systems]]

# Kernel Architecture and Development

#concept #os #low_level #system_programming

## 1. What is a Kernel?
The **kernel** is the core component of an operating system (OS). It has complete control over everything in the system. It is the first program loaded after the bootloader and remains in memory until the system shuts down.

It acts as a bridge between **Software** (Applications) and **Hardware** (CPU, RAM, Devices).

### Core Functions
1.  **Process Management:** 
    *   Decides which process runs on the CPU and for how long (Scheduling).
    *   Handles context switching (saving/restoring state).
2.  **Memory Management:**
    *   Allocates and deallocates memory spaces.
    *   Implements Virtual Memory (Paging/Segmentation) to isolate processes.
3.  **Device Management:**
    *   Interacts with hardware via **Device Drivers**.
    *   Abstracts hardware complexity from applications.
4.  **System Calls:**
    *   Provides an API for user-space applications to request privileged services (e.g., `read()`, `write()`, `fork()`).
5.  **File System Management:**
    *   Maps files to physical storage locations on disks.

---

## 2. Kernel Architectures

Different designs trade off between performance, stability, and modularity.

### A. Monolithic Kernel
*   **Concept:** All OS services (File System, Drivers, Scheduler, Network Stack) run in the **same address space** (Kernel Space).
*   **Pros:** High performance (direct function calls between components).
*   **Cons:** A bug in a driver can crash the entire system. Large codebase is hard to maintain.
*   **Examples:** Linux, Unix, MS-DOS.

### B. Microkernel
*   **Concept:** Only the absolute bare minimum runs in Kernel Space (IPC, basic scheduling, memory primitives). Everything else (Drivers, FS, Network) runs in **User Space** as separate servers.
*   **Pros:** High stability (driver crash doesn't kill the kernel). Secure and modular.
*   **Cons:** Performance overhead due to context switching and message passing (IPC).
*   **Examples:** Minix, QNX, L4.

### C. Hybrid Kernel
*   **Concept:** A compromise. Structurally similar to a Microkernel but runs some non-essential services in Kernel Space for performance.
*   **Examples:** Windows NT (Windows 10/11), macOS (XNU).

### D. Exokernel
*   **Concept:** Extremely minimal. It barely manages resources; instead, it securely multiplexes hardware, letting applications manage their own physical resources.
*   **Use Case:** Specialized high-performance research systems.

---

## 3. How to Build a Kernel (From Scratch)

Building a kernel is the ultimate test of system programming skills. It requires a specific toolchain and deep hardware knowledge.

### Prerequisites
*   **Languages:** C (for logic) and Assembly (x86/ARM for boot/hardware interaction).
*   **Concepts:** Pointers, Memory Addressing, Registers, Stack management.

### The Toolchain
You cannot use your standard system compiler (e.g., `gcc` on Ubuntu) because it targets your host OS (Linux). You need a **Cross-Compiler**.
1.  **Cross-Compiler (i686-elf-gcc):** Compiles code for a generic 32-bit system without OS dependencies.
2.  **Assembler (nasm):** Compiles assembly files.
3.  **Linker (ld):** Combines object files into a raw binary or ELF format.
4.  **Emulator (QEMU/Bochs):** To run and debug the kernel safely.

### Development Steps

#### Step 1: The Boot Process
When a PC turns on:
1.  **BIOS/UEFI** starts.
2.  Loads the **Bootloader** (e.g., GRUB) from the MBR/EFI partition.
3.  Bootloader loads your **Kernel** into memory and jumps to it.

*Note: Writing a bootloader from scratch is complex (switching to Protected Mode). Most hobbyists use **Multiboot** compliant bootloaders like GRUB.*

#### Step 2: The "Hello World" (Assembly Stub)
You need a small assembly file (`boot.s`) to:
*   Define the Multiboot header (so GRUB recognizes it).
*   Set up the initial stack.
*   Call the C `main` function.

```nasm
; Simple nasm example snippet
section .text
global start
start:
    mov esp, stack_space  ; Set up stack
    call kernel_main      ; Jump to C code
    hlt                   ; Halt CPU if return
```

#### Step 3: The Kernel (C Code)
This is "Freestanding C". You have **no Standard Library** (`<stdio.h>`, `<stdlib.h>` do not exist).
You must implement `printf`, `memcpy`, etc., yourself by writing directly to Video Memory (Address `0xB8000` for VGA text mode).

```c
void kernel_main() {
    char* video_memory = (char*) 0xB8000;
    *video_memory = 'X'; // Prints 'X' to top-left corner
}
```

#### Step 4: Linking
Use a **Linker Script** (`linker.ld`) to tell the compiler where to place code in memory (usually starting at `1MB` mark to avoid BIOS reserved areas).

#### Step 5: Packaging & Running
1.  Compile C and Assembly files.
2.  Link them into a kernel binary (e.g., `kernel.bin`).
3.  Create an ISO image with GRUB configuration.
4.  Run in QEMU: `qemu-system-i386 -kernel kernel.bin`.

### Advanced Challenges
After "Hello World", the real work begins:
1.  **GDT/IDT:** Setting up Descriptor Tables to handle Interrupts (Keyboard, Timer).
2.  **Memory Manager:** Writing a Physical Memory Manager (PMM) and Virtual Memory Manager (VMM/Paging).
3.  **Heap:** Implementing `malloc` and `free`.
4.  **Filesystem:** Reading from a disk (ATA/SATA drivers).

---

## Resources
*   **OSDev Wiki:** The bible of kernel development. (wiki.osdev.org)
*   **"Little Book about OS Development"**: Excellent practical guide.
