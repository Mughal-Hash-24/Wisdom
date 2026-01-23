
## Memory Allocation
Memory allocation for a program written in MASM is done in the **.data** section before the main procedure.
It follows the following syntax:
```cpp
.data
	[identifier] Directive/type [Data to be stored]
```
Here:
**Identifier** is not necessary and when it's missing the memory is allocated and the desired data is stored but there is no keyword in the program to access it. So, that data can only be accessed using offsets from other identifiers.
Example:
```cpp
.data
	DB 101
	DD 0FFh
```

## Back Slash '\\'
The back slash '\\'  symbol is used in MASM to break a long line into multiple lines:
```cpp
.data
	v1 \
	DB \
	"Hello", \    ; comment can succeed it
	0FFh, 0AAh
```
An interesting thing about it is that it can only precede a blank space ' ' or a comment before the newline character '\\n'
```cpp
.data
	v1 \
	DB "Hello" \,
	0FFh
```
This is an error as ',' is not an allowed character in between '\\' and '\\n'.
Also, '\\' can't be used inside the **.code** section of the program.

## String Data Allocation
As we know that we can allocate memory and store character arrays inside. Each character requires 1 byte of memory so 'DB' or 'BYTE' are enough but what happens if we use types or directives that allocate space larger than 1 byte.
```cpp
.data
	str1 DW 'AB'
```
Above example code will run just fine because there are 2 bytes allocated and there are exactly 2 characters so in memory they'll show up as:
```
42 41 ; little endian
```
But, consider this example:
```cpp
.data
	str1 DW 'OBSIDIAN', "$" ; error
```
Now, this will result in an error because the assembler will not be able to allocate an array to accommodate all these characters because it falls the in decision paralysis of whether to allocate 2 bytes each or divide 2 bytes among 2 characters. So, to fix this we'll write each character in separate quotations:
```cpp
.data
	str1 DW 'A', 'B', 'C', 'I', 'D', 'I', 'A', 'N', '$'
```
In this way each character is stored in 2 bytes and this will be the layout in little endian format:
```
41 00 42 00 43 00 49 00 44 00 49 00 41 00 4e 00
```

## Why do we write a 0 before Hex values specifically the ones that start with alphabets?

**Consider the following code:**

```cpp
.code
    mov eax FFEEDDCCh ; Error
    mov eax 0FFEEDDCCh ; works fine
```
   
We discussed during the lectures that this is just what the assembler wants. It turns out that the assembler doesn't want things out of the blue. There is always going to be an explanation. In this case the explanation is an ambiguity that whether this "FFEEDDCCh" is an identifier for a memory location or a HEX number. So to solve this issue it's mandatory for all HEX values that start with a letter to have a leading zero.

### Overflow/Underflow but sometimes

Consider the following example:

```cpp
.data
    var1 BYTE -128 ; Fine
    var2 SBYTE -128 ; Fine
    var3 BYTE -129 ; Fine
    var4 SBYTE -129 ; Fine
    var5 BYTE 256 ; Error
```

Here we observe that the assembler can detect overflow/underflow but is able to solve only the underflow. The reason for this asymmetry is that it's ambiguous because the negative out of range literal is still in the valid range when stored in memory in 2's compliment. In this case -129 is stored as 127 and that's valid as it requires 8 or less bits. But in the case of 256, that's 9 bits and assembler sees this as an error.

[[1.2 Memory Allocation and Accessing]]
[[1.4 Movsx and Movzx]]
[[1.5 Misc]]