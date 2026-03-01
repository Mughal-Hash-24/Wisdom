---
tags:
  - "#concept/unnamed-pipe"
  - "#field/cs"
  - "#subject/os"
  - "#type/expansion"
---
[[T.O.C (Operating Systems)|Up to Operating Systems]]

> **Seed:** "WHat happens when we pass an array of greater size than 2 to an unnamed pipe?"
> **Lens:** First Principles / The Chief Engineer

---

# Unnamed Pipe: Array Bounds and System Call Behavior

## 1. Ontological Definition

In Unix-like operating systems, an **unnamed pipe** is a unidirectional data channel used for inter-process communication (IPC), accessed via a pair of file descriptors. The `pipe(int pipefd[2])` system call is the mechanism used to create this channel, where `pipefd` is an array of two integers that will be populated with the read and write file descriptors, respectively.

## 2. The Internal Mechanics (Under the Hood)

When the `pipe()` system call is invoked, the kernel performs the following sequence of operations:

1.  **Allocation:** It allocates a buffer (typically 64KB on modern Linux) in kernel memory to act as the pipe's storage.
2.  **File Descriptor Creation:** It identifies two available entries in the process's file descriptor table.
3.  **Inode Initialization:** It creates a "pipe" inode in the virtual file system (VFS), which manages the buffer's read and write pointers.
4.  **Populating the Array:** It writes the integer values of the allocated file descriptors into the memory pointed to by the `pipefd` argument.

### The "Array Size > 2" Scenario

The `pipe()` function signature `int pipe(int pipefd[2])` is a hint to the programmer and the compiler, but at the system call level (e.g., `SYS_pipe` on x86_64), the kernel only receives a **memory address** (the pointer to the start of the array).

*   **Fixed Writing:** The kernel's implementation of `pipe()` is hard-coded to write exactly two `int` values (8 bytes on 64-bit systems) to the address provided.
*   **Ignore Excess:** If you pass `int my_pipe[10]`, the kernel writes to `my_pipe[0]` and `my_pipe[1]`. It has no knowledge of the remaining 8 elements (`my_pipe[2]` through `my_pipe[9]`) and leaves them entirely untouched.
*   **Memory Safety:** This is perfectly "safe" from a system perspective because the kernel is writing *less* than the allocated space. The excess memory remains in its previous state (likely zero-initialized or containing garbage).

### Pseudo-Code Representation (Kernel Level)

```c
// Simplified Kernel Implementation of pipe()
long sys_pipe(int *user_pipefd) {
    int fds[2];
    struct file *read_file, *write_file;

    // 1. Create the pipe buffer and file objects
    do_pipe_creation(&read_file, &write_file);

    // 2. Assign file descriptors
    fds[0] = get_unused_fd_flags(0);
    fds[1] = get_unused_fd_flags(0);

    // 3. Copy results back to user space
    // copy_to_user only copies sizeof(fds) which is 2 * sizeof(int)
    if (copy_to_user(user_pipefd, fds, sizeof(fds))) {
        return -EFAULT;
    }

    return 0;
}
```

## 3. Systems Context & Anchoring

**Analogy: The Two-Slot Mailbox**

Imagine you have a custom-built mailbox designed to hold exactly two envelopes: one for "Incoming" and one for "Outgoing."

*   **Normal Case:** You provide a small tray with two slots. The mailman puts the Incoming key in Slot 1 and the Outgoing key in Slot 2.
*   **Array Size > 2:** You provide a massive tray with ten slots. The mailman arrives, sees the tray, and follows his strict protocol: "Put the Incoming key in the first slot and the Outgoing key in the second slot." He ignores slots 3 through 10. You now have your keys in the first two slots, and the rest of the tray is just empty, wasted space.
*   **Array Size < 2 (Danger):** You provide a tray with only one slot. The mailman tries to put the first key in Slot 1, then tries to put the second key where Slot 2 *should* be. He ends up dropping the key on your expensive floor (Memory Corruption/Segmentation Fault).

## 4. Edge Cases & Constraints

1.  **Buffer Overflow (Array Size < 2):** If the array passed is smaller than 2 integers (e.g., `int single_fd[1]`), the kernel will attempt to write 8 bytes into a 4-byte space. This results in a **stack or heap corruption** in the user process. On many systems, this triggers an `EFAULT` if the address is invalid, or a silent, dangerous corruption if it is within a valid page.
2.  **Alignment Requirements:** While the kernel is generally robust, passing a non-aligned pointer (not starting on an `int` boundary) can lead to architecture-specific alignment faults or `EFAULT` errors, as the `copy_to_user` operation might fail to write the integer values atomically.
3.  **Namespace Collisions:** Passing an array of size 10 doesn't break the system, but it may lead to logic errors in the application if the programmer mistakenly assumes the kernel will provide more than two descriptors (e.g., for error handling or auxiliary channels).

---
