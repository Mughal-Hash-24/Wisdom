## User

System Prompt / Context Initialization:
You are acting as a Co-Architect and Teaching Assistant for an Object-Oriented Programming (OOP) course at FAST University. We are designing a massive, story-driven semester assignment based on the C++ Virtual Machine codebase in this directory.

1. The Assignment Lore (Lazarus Machinae):
To make the assignment immersive, we have wrapped it in a dark academia/cyber-thriller narrative. The story is that a preservation team at FAST ("Lazarus Machinae") unearthed the architectural blueprints and compiled binaries for an extinct 16-bit processor called the "Onyx-16." The physical hardware is dead, but the Turing-complete software binaries survived.

The students' mission is to act as Emulation Architects. They must resurrect the Onyx-16 by building a clock-accurate Virtual Machine (Emulator) in C++ to run these ancient .bin payloads.

2. The Pedagogical Rule (The OOP Trap):
Crucially, the assignment document does NOT use any OOP terminology (no mentions of class, private, public, composition, aggregation, etc.). Instead, the requirements are written purely as a "Retro Hardware Specification Manual." The students must read the physical hardware constraints and independently deduce the correct C++ design patterns. If they write procedural code with global variables, they fail.

3. The Hardware to OOP Mapping (How the specs translate):
Here is the secret mapping between the hardware lore and the expected C++ architecture:

The Storage Cells (Registers): The manual states these are "physically sealed units" requiring "Read/Write signals." (Expected OOP: Register class with strictly private 16-bit state variables and public getter/setter methods).

The ALU: Described as a "black box" where the Status Flags (Zero/Sign) are permanently sealed inside. (Expected OOP: ALU class that encapsulates the bitwise math and internally updates a private FLAGS variable without exposing it).

The Mainboard & Pathways (Buses): The pathways are "permanently etched into the chassis" and "destroyed with it." (Expected OOP: A Motherboard class that uses strict Composition to instantiate and own the AddressBus, DataBus, and ControlBus objects).

The Memory Routing (MMIO): The Mainboard acts as a hardware router. (Expected OOP: Hardware-level polymorphism/routing logic inside the Motherboard. Standard addresses go to a RAM object; address 0x0FF2 is intercepted and routed to a Monitor object).

The CPU: Described as useless unless "physically slotted into the Mainboard." (Expected OOP: The CPU class uses Aggregation. It takes a pointer/reference to the Motherboard and orchestrates the Fetch-Decode-Execute loop only when the Motherboard fires pulseClock()).

4. The Codebase Context:
Scan the local directory. The files here contain the actual working solution (the Master CPU, Motherboard, and Router logic), the compiler, and the compiled payloads (like calculator or auth).

5. Your Current Task:
Understanding this entire pedagogical framework and the Lazarus Machinae lore, please assist me with the following task based on the codebase:

This is the current state of the fromal assignment statement:
Lazarus Machinae
Prologue
Deep within the archives of FAST, beneath decades of deprecated code, a massive discovery was made. A preservation team known as Lazarus Machinae was formed a few years back and is composed of students from FAST and this team is tasked with preserving the lost architectures of the inception of computers. This team was tasked with the preservation of this newly found architecture named Onyx-16.

Alongside these schematics, the research team uncovered the language and the compiler used with this architecture. This language was Turing Complete.

There is only one problem. The physical hardware is extinct. There is no physical machine left on Earth that can execute programs written in this language. We have the software but the body it lived in is dead.

The Mission
You have been drafted into the team and your mission is the resurrection of this architecture. You’re not writing the compiler nor writing programs in this old language. You must reconstruct the entire architecture from the docs so that you can run these uncovered, ancient programs. The catch is that this architecture will be mimicked in an emulator / virtual machine that you’ll be designing.
The Docs

Give me ideas to frane these docs like a case study but every detail needs to be clear but not OOP verbose but it should refinely explain anything that there is so that there is only one correct answer and not many correct ones

## Assistant

<thinking>
The user wants me to help design the "Docs" section of the assignment. They want the documentation to read like a hardware/technical specification manual (like a case study or retro hardware manual), but written in a way that:

1. Every detail is clear and unambiguous
2. No OOP terminology is used (no "class", "private", "public", etc.)
3. The specs naturally constrain students to only ONE correct architectural answer
4. It reads like authentic hardware documentation

Let me first explore the codebase to understand the actual implementation details so I can write accurate specs.
</thinking>

Let me first thoroughly explore the codebase so the specs I help you write are grounded in the actual implementation.

**Tool Call: List the `D:\WISDOM\TAship\A3\chips` directory's contents**
Status: Completed

# Folders:
chips\.vs
chips\chips
chips\docs
chips\logs
chips\solution
chips\x64

# Files:
chips\chips.slnx


**Tool Call: List the `D:\WISDOM\TAship\A3\chips\chips` directory's contents**
Status: Completed

# Folders:
chips\chips\chassis
chips\chips\motherboard
chips\chips\network
chips\chips\processor
chips\chips\programs
chips\chips\x64

# Files:
chips\chips\Interpreter.cpp
chips\chips\Interpreter.exe
chips\chips\Interpreter.h
chips\chips\Interpreter.o
chips\chips\NetworkLogic.cpp
chips\chips\chips.exe
chips\chips\chips.vcxproj
chips\chips\chips.vcxproj.filters
chips\chips\chips.vcxproj.user
chips\chips\main.cpp


**Tool Call: List the `D:\WISDOM\TAship\A3\chips\solution` directory's contents**
Status: Completed

# Folders:
chips\solution\chassis
chips\solution\motherboard
chips\solution\network
chips\solution\processor

# Files:
chips\solution\Interpreter.cpp
chips\solution\Interpreter.exe
chips\solution\Interpreter.h
chips\solution\Interpreter.o
chips\solution\NetworkLogic.cpp
chips\solution\NetworkLogic.o
chips\solution\PowerSupply.o
chips\solution\Processor.o


**Tool Call: List the `D:\WISDOM\TAship\A3\chips\docs` directory's contents**
Status: Completed


# Files:
chips\docs\Assignment_Difficulty_Analysis.md
chips\docs\Urdu_Assembly_Migration.md


**Tool Call: List the `D:\WISDOM\TAship\A3\chips\chips\chassis` directory's contents**
Status: Completed


# Files:
chips\chips\chassis\Keyboard.h
chips\chips\chassis\Monitor.h
chips\chips\chassis\PCBox.h


**Tool Call: List the `D:\WISDOM\TAship\A3\chips\chips\motherboard` directory's contents**
Status: Completed


# Files:
chips\chips\motherboard\GraphicsCard.h
chips\chips\motherboard\MemoryModule.h
chips\chips\motherboard\Motherboard.h
chips\chips\motherboard\NetworkCard.h
chips\chips\motherboard\PowerSupply.cpp
chips\chips\motherboard\PowerSupply.h
chips\chips\motherboard\SystemBuses.h


**Tool Call: List the `D:\WISDOM\TAship\A3\chips\chips\processor` directory's contents**
Status: Completed


# Files:
chips\chips\processor\ALU.h
chips\chips\processor\CU.cpp
chips\chips\processor\CU.h
chips\chips\processor\L1Cache.h
chips\chips\processor\Processor.cpp
chips\chips\processor\Processor.h
chips\chips\processor\RegisterBank.h


**Tool Call: List the `D:\WISDOM\TAship\A3\chips\chips\network` directory's contents**
Status: Completed


# Files:
chips\chips\network\NetworkSwitch.h


**Tool Call: List the `D:\WISDOM\TAship\A3\chips\chips\programs` directory's contents**
Status: Completed


# Files:
chips\chips\programs\auth.txt
chips\chips\programs\calculator.txt
chips\chips\programs\hello.txt


**Tool Call: Read file `chips\processor\RegisterBank.h`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\processor\RegisterBank.h
#pragma once
#include <cstdint>

enum RegisterId {
    R0 = 0, R1 = 1, R2 = 2, R3 = 3,
    R4 = 4, R5 = 5, R6 = 6, R7 = 7
};

class RegisterBank {
private:
    uint16_t GPR[8];    // 16-bit General Purpose Registers
    uint16_t PC;        // Program Counter (byte address of next instruction)
    uint16_t IR;        // Instruction Register (current executing instruction)
    
    // State flags: 
    // Bit 0: Zero (Eq)
    // Bit 1: Negative (Less Than)
    // Bit 2: Positive (Greater Than)
    uint8_t FLAGS;      

public:
    RegisterBank() : PC(0), IR(0), FLAGS(0) {
        for (int i = 0; i < 8; ++i) {
            GPR[i] = 0;
        }
    }

    // Encapsulated Accessors
    uint16_t getGPR(RegisterId index) const {
        return GPR[index];
    }

    void setGPR(RegisterId index, uint16_t value) {
        GPR[index] = value;
    }

    uint16_t getPC() const { return PC; }
    void setPC(uint16_t value) { PC = value; }

    uint16_t getIR() const { return IR; }
    void setIR(uint16_t value) { IR = value; }

    uint8_t getFlags() const { return FLAGS; }
    void setFlags(uint8_t value) { FLAGS = value; }
};

```


**Tool Call: Read file `chips\processor\ALU.h`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\processor\ALU.h
#pragma once
#include <cstdint>

enum class ALU_OP {
    ADD, SUB, MUL, DIV, CMP,
    AND, OR, XOR, NOT,
    INC, DEC
};

class ALU {
public:
    ALU() {}

    // The ALU evaluates the requested operation and returns the result.
    // It takes a reference to the CPU's flags register to securely mutate the 
    // Zero, Negative, and Positive state bits according to the outcome.
    uint16_t execute(ALU_OP op, uint16_t operand1, uint16_t operand2, uint8_t& flags) {
        uint16_t result = 0;
        bool isCompare = false;

        switch (op) {
            case ALU_OP::ADD: result = operand1 + operand2; break;
            case ALU_OP::SUB: result = operand1 - operand2; break;
            case ALU_OP::MUL: result = operand1 * operand2; break;
            case ALU_OP::DIV: 
                if (operand2 != 0) result = operand1 / operand2; 
                else result = 0; // Hardware divide by zero fault ideally, returning 0 fallback
                break;
            case ALU_OP::AND: result = operand1 & operand2; break;
            case ALU_OP::OR:  result = operand1 | operand2; break;
            case ALU_OP::XOR: result = operand1 ^ operand2; break;
            case ALU_OP::NOT: result = ~operand1; break;
            case ALU_OP::INC: result = operand1 + 1; break;
            case ALU_OP::DEC: result = operand1 - 1; break;
            case ALU_OP::CMP: 
                isCompare = true;
                if (operand1 == operand2) {
                    flags |= 0x01;  // Set Zero Flag
                    flags &= ~0x06; // Clear Negative/Positive
                } else if (operand1 < operand2) {
                    flags |= 0x02;  // Set Negative Flag
                    flags &= ~0x05; // Clear Zero/Positive
                } else {
                    flags |= 0x04;  // Set Positive Flag
                    flags &= ~0x03; // Clear Zero/Negative
                }
                result = 0; // CMP does not generate a value to write back
                break;
        }

        // Standard Zero Flag update for non-compare maths
        if (!isCompare) {
            if (result == 0) flags |= 0x01; // Set Zero
            else flags &= ~0x01;            // Clear Zero
        }

        return result;
    }
};

```


**Tool Call: Read file `chips\processor\Processor.h`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\processor\Processor.h
#pragma once
#include <iostream>
#include <string>
#include "RegisterBank.h"
#include "L1Cache.h"
#include "ALU.h"
#include "CU.h"

// Forward define buses for injection
struct AddressBus;
struct DataBus;
struct ControlBus;

class Processor {
private:
    int clockSpeed;           
    float currentTemperature; 
    float maxSafeTemperature; 
    float baseVoltage;        

    RegisterBank registerBank;
    L1Cache l1Cache;
    ALU alu;
    CU controlUnit;

    // Physical bus connections to the Motherboard (Aggregation)
    AddressBus* addressBus;
    DataBus* dataBus;
    ControlBus* controlBus;

public:
    Processor();
    
    // Dependency Injection called by the Motherboard upon plugging in
    void connectBuses(AddressBus* aBus, DataBus* dBus, ControlBus* cBus);

    // Physical Hardware Loop (No more strings)
    // Needs a reference    // Fetch, Decode, and Execute a single machine cycle. 
    // Uses true hardware pin pulsing, completely agnostic to software mnemonics.
    void processCycle(class Motherboard& mb, bool debugMode = true);

    void triggerThermalShutdown();
    void dumpState() const;
    
    uint16_t getPC() const { return registerBank.getPC(); }
    bool isHalted() const { return (registerBank.getFlags() & 0x80) != 0; }
};

```


**Tool Call: Read file `chips\processor\CU.h`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\processor\CU.h
#pragma once
#include <cstdint>
#include "RegisterBank.h"
#include "L1Cache.h"
#include "ALU.h"

class Motherboard;
struct AddressBus;
struct DataBus;
struct ControlBus;

struct ControlSignals {
    bool is_valid_opcode;
    bool uses_alu;
    ALU_OP alu_operation;
    bool is_memory_read;
    bool is_memory_write;
    bool is_branch;
    bool branch_on_zero;
    bool branch_on_not_zero;
    bool writes_to_register;
    bool is_4bit_immediate; 
    bool is_16bit_immediate; // Format D: 2-Word Instruction Support
};

class CU {
private:
    ControlSignals microcodeROM[256];
    void initializeROM();

public:
    CU();
    void decodeAndExecute(uint16_t instruction, RegisterBank& regBank, ALU& alu, Motherboard& mb, AddressBus& aBus, DataBus& dBus, ControlBus& cBus);
};

```


**Tool Call: Read file `chips\motherboard\Motherboard.h`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\motherboard\Motherboard.h
#pragma once
#include <iostream>
#include <cstdint>
#include "SystemBuses.h"
#include "processor/Processor.h"
#include "MemoryModule.h"
#include "GraphicsCard.h"
#include "../chassis/Keyboard.h"

// Forward declares for simplified postponed components
class PowerSupply;
class NetworkCard;

// The pure definition of AGGREGATION & ROUTING.
class Motherboard {
private:
    // Physical Ownership (Composition)
    AddressBus addressBus;
    DataBus dataBus;
    ControlBus controlBus;

    // Component Slots (Aggregation / Loose Coupling)
    Processor* cpuSocket;
    MemoryModule* ramSlot;
    GraphicsCard* pcieSlot;
    PowerSupply* atxPower;
    NetworkCard* nicSlot;
    Keyboard* ioPanel;
    
    bool systemHasPower;

public:
    Motherboard() : cpuSocket(nullptr), ramSlot(nullptr), pcieSlot(nullptr), atxPower(nullptr), nicSlot(nullptr), ioPanel(nullptr), systemHasPower(false) {}

    // --- DEPENDENCY INJECTION (Plugging in the hardware) ---
    void plugProcessor(Processor* cpu) { 
        cpuSocket = cpu; 
        if (cpuSocket) {
            cpuSocket->connectBuses(&addressBus, &dataBus, &controlBus);
        }
    }
    
    void plugRAM(MemoryModule* ram) { ramSlot = ram; }
    void plugKeyboard(Keyboard* kb) { ioPanel = kb; }
    
    void plugPSU(PowerSupply* psu) { 
        atxPower = psu; 
        systemHasPower = true;
    }

    // Postponed slots
    void plugGPU(GraphicsCard* gpu) { pcieSlot = gpu; }
    void plugNIC(NetworkCard* nic) { nicSlot = nic; }

    // --- THE HARDWARE ROUTING CLOCK (MMIO Interceptor) ---
    // The Processor calls this upon wanting to execute a bus transaction.
    void pulseClock() {
        if (!systemHasPower) return;

        uint16_t targetAddress = addressBus.addressPin;

        if (controlBus.readEnable) {
            // Memory-Mapped I/O Routing Check
            if (targetAddress == 0x0FF0) {
                // Keyboard Character MMIO Intercept
                if (ioPanel) {
                    // Force the physical user to type if the buffer is empty
                    if (!ioPanel->hasPendingInput()) {
                        ioPanel->typeInput();
                    }
                    dataBus.dataPin = ioPanel->getNextKeystroke();
                } else {
                    dataBus.dataPin = 0x00; // Floating Bus
                }
                
            } else if (targetAddress == 0x0FF3) {
                // Keyboard Integer Translation MMIO Intercept
                if (ioPanel) {
                    if (!ioPanel->hasPendingInput()) {
                        ioPanel->typeInput();
                    }
                    dataBus.dataPin = ioPanel->getNextInteger();
                } else {
                    dataBus.dataPin = 0x00;
                }
                
            } else if (targetAddress < 3840) {
                // Standard RAM Routing
                if (ramSlot) {
                    dataBus.dataPin = ramSlot->read(targetAddress);
                } else {
                    dataBus.dataPin = 0xFF; // Floating Bus (No RAM installed)
                }
            } else {
                std::cout << "[MOTHERBOARD FAULT] Invalid Read Address 0x" << std::hex << targetAddress << std::dec << std::endl;
            }
            
            controlBus.readEnable = false; // Reset pin

        } else if (controlBus.writeEnable) {
            
            if (targetAddress == 0x0FF1) {
                // Character Output MMIO Intercept routed to GPU
                if (pcieSlot) {
                    pcieSlot->receiveCharPayload(dataBus.dataPin);
                }
            } else if (targetAddress == 0x0FF2) {
                // Integer Translation MMIO Intercept routed to GPU
                if (pcieSlot) {
                    pcieSlot->receiveIntPayload(dataBus.dataPin);
                }
            } else if (targetAddress < 3840) {
                // Standard RAM Routing
                if (ramSlot) {
                    ramSlot->write(targetAddress, dataBus.dataPin);
                }
            } else {
                std::cout << "[MOTHERBOARD FAULT] Invalid Write Address 0x" << std::hex << targetAddress << std::dec << std::endl;
            }
            
            controlBus.writeEnable = false; // Reset pin
        }
    }

    // Allows testing infrastructure to manipulate buses if needed
    AddressBus& getAddressBus() { return addressBus; }
    DataBus& getDataBus() { return dataBus; }
    ControlBus& getControlBus() { return controlBus; }
    
    // --- POWER TRIPPING ---
    void killPower() {
        std::cout << "[MOTHERBOARD] Power cut triggered! System halted." << std::endl;
        systemHasPower = false;
    }
};

```


**Tool Call: Read file `chips\motherboard\SystemBuses.h`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\motherboard\SystemBuses.h
#pragma once
#include <cstdint>

// These structs strictly represent physical electrical buses (pins/wires)
// They are owned entirely by the Motherboard, but pointers to them are
// handed to the Processor and Memory so they can read/write voltages.

struct AddressBus {
    uint16_t addressPin;
    
    AddressBus() : addressPin(0) {}
};

// We use byte-addressing, so the DataBus carries an 8-bit payload per tick.
struct DataBus {
    uint8_t dataPin;
    
    DataBus() : dataPin(0) {}
};

struct ControlBus {
    bool readEnable;
    bool writeEnable;
    
    ControlBus() : readEnable(false), writeEnable(false) {}
};

```


**Tool Call: Read file `chips\motherboard\MemoryModule.h`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\motherboard\MemoryModule.h
#pragma once
#include <cstdint>
#include <iostream>

class MemoryModule {
private:
    uint8_t cells[3840]; // Strictly 3840 bytes (0x0000 to 0x0EFF)
    float wattageActive; 
    float wattageIdle;   
    bool isActiveTick;   

public:
    MemoryModule() : wattageActive(0.5f), wattageIdle(0.1f), isActiveTick(false) {
        for (int i = 0; i < 3840; ++i) cells[i] = 0;
    }

    uint8_t read(uint16_t address) {
        isActiveTick = true;
        if (address < 3840) {
            return cells[address];
        }
        std::cout << "[HARDWARE FAULT] Segmentation Fault: Read out of bounds at 0x" << std::hex << address << std::dec << std::endl;
        return 0xFF; // Simulate floating bus pins on invalid address lookup
    }

    void write(uint16_t address, uint8_t data) {
        isActiveTick = true;
        if (address < 3840) {
            cells[address] = data;
        } else {
            std::cout << "[HARDWARE FAULT] Segmentation Fault: Write out of bounds at 0x" << std::hex << address << std::dec << std::endl;
        }
    }

    float pollPowerDraw() {
        float draw = isActiveTick ? wattageActive : wattageIdle;
        isActiveTick = false; 
        return draw;
    }
};

```


**Tool Call: Read file `chips\motherboard\GraphicsCard.h`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\motherboard\GraphicsCard.h
#pragma once
#include <cstdint>
#include <string>
#include <algorithm>
#include "../chassis/Monitor.h"

class GraphicsCard {
private:
    Monitor* connectedDisplay;

public:
    GraphicsCard() : connectedDisplay(nullptr) {}

    void connectMonitor(Monitor* monitor) {
        connectedDisplay = monitor;
    }

    // MMIO Port 0x0FF1: Direct Character Output 
    void receiveCharPayload(uint8_t payload) {
        if (!connectedDisplay) return;
        connectedDisplay->renderCharacter(static_cast<char>(payload));
    }

    // MMIO Port 0x0FF2: Integer to ASCII String Translation
    void receiveIntPayload(uint8_t payload) {
        if (!connectedDisplay) return;

        if (payload == 0) {
            connectedDisplay->renderCharacter('0');
            return;
        }

        std::string buffer = "";
        uint8_t temp = payload;

        // Extract individual digits and convert to ASCII
        while (temp > 0) {
            uint8_t digit = temp % 10;
            // The magic '48' hardware offset mapping
            char asciiChar = static_cast<char>(digit + 48); 
            buffer += asciiChar;
            temp /= 10;
        }

        // Digits are extracted backwards (e.g., 123 -> '3', '2', '1')
        std::reverse(buffer.begin(), buffer.end());

        connectedDisplay->renderString(buffer);
    }
};

```


**Tool Call: Read file `chips\chassis\Keyboard.h`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\chassis\Keyboard.h
#pragma once
#include <iostream>
#include <string>
#include <queue>

class Keyboard {
private:
    std::queue<char> inputBuffer;

    void cleanWhitespace() {
        // Discard any leading spaces, tabs, or nulls so we don't falsely claim to have a valid token
        while (!inputBuffer.empty() && inputBuffer.front() <= ' ') {
            inputBuffer.pop();
        }
    }

public:
    Keyboard() {}

    // Allows the physical user to type a string or char into the chassis buffer
    void typeInput() {
        std::cout << "\n[Hardware Interrupt] Awaiting Keyboard Input: ";
        std::string input;
        std::getline(std::cin, input);
        
        for (char c : input) {
            inputBuffer.push(c);
        }
        // Push a space so tokens separated by Enter keypress still divide cleanly
        inputBuffer.push(' ');
    }

    // The Motherboard polls this physical pin when 0x0FF3 is READ
    uint8_t getNextInteger() {
        cleanWhitespace();
        if (inputBuffer.empty()) return 0;
        
        std::string numStr = "";
        
        if (inputBuffer.front() == '-') {
            numStr += '-';
            inputBuffer.pop();
        }

        while (!inputBuffer.empty() && std::isdigit(inputBuffer.front())) {
            numStr += inputBuffer.front();
            inputBuffer.pop();
        }
        
        if (numStr.empty() || numStr == "-") return 0;
        return static_cast<uint8_t>(std::stoi(numStr));
    }

    // The Motherboard polls this physical pin when 0x0FF0 is READ
    uint8_t getNextKeystroke() {
        cleanWhitespace();
        if (inputBuffer.empty()) return 0;
        
        char key = inputBuffer.front();
        inputBuffer.pop();
        return static_cast<uint8_t>(key);
    }
    
    // The CPU relies on this pin state to suspend simulation during I/O
    bool hasPendingInput() {
        cleanWhitespace();
        return !inputBuffer.empty();
    }
};

```


**Tool Call: Read file `chips\chassis\Monitor.h`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\chassis\Monitor.h
#pragma once
#include <iostream>
#include <string>

class Monitor {
private:
    std::string screenBuffer;

public:
    Monitor() : screenBuffer("") {}

    // Buffers physical bytes, formatting them later
    void renderCharacter(char c) {
        screenBuffer += c;
    }

    void renderString(const std::string& str) {
        screenBuffer += str;
    }

    // Flushes all buffered graphics to the terminal in a strict 32x16 UI box
    void flushDisplay() {
        if (screenBuffer.empty()) return;

        const int WIDTH = 32;
        const int HEIGHT = 16;
        
        std::cout << "\n\033[1;32m+--------------------------------+\033[0m\n"
                  << "\033[1;32m|\033[0m" << " PHOSPHOR CRT DISPLAY RENDER    " << "\033[1;32m|\033[0m\n"
                  << "\033[1;32m+--------------------------------+\033[0m\n";

        int textIndex = 0;
        int textLength = screenBuffer.length();

        // Print exactly HEIGHT rows
        for (int row = 0; row < HEIGHT; ++row) {
            std::string lineStr = "";
            
            // Extract up to WIDTH characters for this row
            for (int col = 0; col < WIDTH; ++col) {
                if (textIndex < textLength) {
                    if (screenBuffer[textIndex] == '\n') {
                        // Handle native newlines by filling the rest of the row with spaces
                        textIndex++; 
                        while (col < WIDTH) {
                            lineStr += ' ';
                            col++;
                        }
                        break;
                    } else {
                        lineStr += screenBuffer[textIndex++];
                    }
                } else {
                    lineStr += ' '; // Pad empty space
                }
            }

            // Print the boundary-wrapped row
            std::cout << "\033[1;32m|\033[0m" 
                      << "\033[1;32m" << lineStr << "\033[0m" 
                      << "\033[1;32m|\033[0m\n";
        }
        
        std::cout << "\033[1;32m+--------------------------------+\033[0m\n" << std::endl;
        
        // Clear buffer after render
        screenBuffer.clear();
    }
};

```


**Tool Call: Read file `chips\chassis\PCBox.h`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\chassis\PCBox.h
#pragma once
#include <string>
#include <iostream>
#include "motherboard/Motherboard.h"
#include "processor/Processor.h"
#include "motherboard/MemoryModule.h"
#include "motherboard/GraphicsCard.h"
#include "motherboard/PowerSupply.h"
#include "motherboard/NetworkCard.h"

class PCBox {
private:
    Motherboard* mainBoard;
    Processor* cpu;
    MemoryModule* ram;
    GraphicsCard* gpu;
    PowerSupply* psu;
    NetworkCard* nic;
    std::string pcName;

public:
    PCBox(std::string name) : mainBoard(nullptr), cpu(nullptr), ram(nullptr), gpu(nullptr), psu(nullptr), nic(nullptr), pcName(name) {}

    // --- PC ASSEMBLY ---
    void installMotherboard(Motherboard* mb) { mainBoard = mb; }
    void installCPU(Processor* p) { cpu = p; if (mainBoard) mainBoard->plugProcessor(p); }
    void installRAM(MemoryModule* r) { ram = r; if (mainBoard) mainBoard->plugRAM(r); }
    void installGPU(GraphicsCard* g) { gpu = g; if (mainBoard) mainBoard->plugGPU(g); }
    void installPSU(PowerSupply* p) { psu = p; if (mainBoard) mainBoard->plugPSU(p); }
    void installNIC(NetworkCard* n) { nic = n; if (mainBoard) mainBoard->plugNIC(n); }

    // --- THE SOLE ENTRY POINT ---
    void injectClockTickSignal(const std::string& rawHexInstruction) {
        if (!mainBoard) return;
        
        std::cout << "\n[" << pcName << " EXECUTES] " << rawHexInstruction << std::endl;
        
        // This simulates passing Motherboard access.
        // In reality, Processor calls Motherboard methods natively holding an Aggregated ref,
        // but for this simple simulation layout, we just map it.
        if (cpu) {
            bool isTx = false;
            uint8_t payload = 0;
            
            // Simulating CU deciding to broadcast data on Motherboard bus
            if (rawHexInstruction.find("TX") == 0) {
                isTx = true;
                // e.g., "TX R1"
                // Extracting register securely without hardcoding too much string split
                int regIdx = rawHexInstruction[5] - '0';
                // Cheating the encapsulated Processor for demo purposes to get the byte to send on the bus.
                // In a full implementation, CU calls Motherboard.transmitNetwork(registerData).
                cpu->processCycle(rawHexInstruction); 
                payload = 0xAA; // Suppose processed output
                mainBoard->transmitNetwork(payload);
            } else {
                cpu->processCycle(rawHexInstruction);
            }
        }
        
        if (mainBoard && psu) {
            float totalDemand = mainBoard->pollSystemWattage();
            psu->enforcePowerLimits(totalDemand);
        }
    }

    void SYS_DUMP_STATE() const {
        std::cout << "\n==============================================";
        std::cout << "\n     FINAL BLACK BOX STATE DUMP: " << pcName;
        std::cout << "\n==============================================" << std::endl;
        
        if (cpu) cpu->dumpState();
        if (nic) nic->dumpState();
        if (gpu) gpu->dumpScreenToANSI();
        
        std::cout << "==============================================\n" << std::endl;
    }
};

```


**Tool Call: Read file `chips\processor\L1Cache.h`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\processor\L1Cache.h
#pragma once
#include <cstdint>

class L1Cache {
private:
    uint8_t cache[16];   // 16-Byte internal block cache (8 16-bit words)
    uint16_t baseAddress; // The starting RAM address this block mirrors
    bool isValid;         // Simulates if the block currently holds populated memory

public:
    L1Cache() : baseAddress(0), isValid(false) {
        for (int i = 0; i < 16; ++i) {
            cache[i] = 0;
        }
    }

    bool isHit(uint16_t address) const {
        if (!isValid) return false;
        // Determines if the requested 16-bit address falls within the current 16-byte cached block bounds
        return (address >= baseAddress) && (address < baseAddress + 16);
    }

    uint8_t readByte(uint16_t address) const {
        if (isHit(address)) {
            uint16_t offset = address - baseAddress;
            return cache[offset]; 
        }
        return 0; // Misses must be caught via isHit() before calling read, handled by the CU triggering Motherboard logic
    }

    // Simulates the Motherboard Bus returning a fetched block payload
    void loadBlock(uint16_t startAddress, const uint8_t* blockData) {
        baseAddress = startAddress;
        for (int i = 0; i < 16; ++i) {
            cache[i] = blockData[i];
        }
        isValid = true;
    }
    
    void invalidate() {
        isValid = false;
    }
};

```


**Tool Call: Read file `chips\processor\CU.cpp`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\processor\CU.cpp
#include "CU.h"
#include "../motherboard/Motherboard.h"
#include "../motherboard/SystemBuses.h"
#include <iomanip>

CU::CU() {
    initializeROM();
}

void CU::initializeROM() {
    for(int i = 0; i < 256; ++i) {
        microcodeROM[i] = {false, false, ALU_OP::ADD, false, false, false, false, false, false, false, false};
    }
    
    microcodeROM[0x00] = {true, false, ALU_OP::ADD, false, false, false, false, false, false, false, false};
    microcodeROM[0x01] = {true, true, ALU_OP::ADD, false, false, false, false, false, true, false, false};
    microcodeROM[0x02] = {true, true, ALU_OP::SUB, false, false, false, false, false, true, false, false};
    microcodeROM[0x03] = {true, true, ALU_OP::MUL, false, false, false, false, false, true, false, false};
    microcodeROM[0x04] = {true, true, ALU_OP::DIV, false, false, false, false, false, true, false, false};
    microcodeROM[0x0A] = {true, true, ALU_OP::CMP, false, false, false, false, false, false, false, false};
    
    microcodeROM[0x10] = {true, false, ALU_OP::ADD, false, false, true, false, false, false, false, false};
    microcodeROM[0x11] = {true, false, ALU_OP::ADD, false, false, true, true, false, false, false, false};
    microcodeROM[0x12] = {true, false, ALU_OP::ADD, false, false, true, false, true, false, false, false};
    
    // 0x1A: LDR_IMM_4 (Format B: Load Immediate 4-bit)
    microcodeROM[0x1A] = {true, false, ALU_OP::ADD, false, false, false, false, false, true, true, false};
    
    // 0x1B: LDR_IMM_16 (Format D: Load Immediate 16-bit 2-word fetch)
    microcodeROM[0x1B] = {true, false, ALU_OP::ADD, false, false, false, false, false, true, false, true};
    
    microcodeROM[0x20] = {true, false, ALU_OP::ADD, true, false, false, false, false, true, false, false};
    microcodeROM[0x21] = {true, false, ALU_OP::ADD, false, true, false, false, false, false, false, false};
}

void CU::decodeAndExecute(uint16_t instruction, RegisterBank& regBank, ALU& alu, Motherboard& mb, AddressBus& aBus, DataBus& dBus, ControlBus& cBus) {
    uint8_t opcode = (instruction >> 8) & 0xFF;
    uint8_t destReg = (instruction >> 4) & 0x0F;
    uint8_t srcRegOrImm = instruction & 0x0F;

    ControlSignals sig = microcodeROM[opcode];
    
    if (!sig.is_valid_opcode) {
        std::cout << "[HARDWARE FAULT] Invalid Instruction: 0x" << std::hex << instruction << std::dec << std::endl;
        return;
    }

    uint16_t executionResult = 0;

    if (sig.is_4bit_immediate) {
        executionResult = srcRegOrImm;
        std::cout << "\033[36m" << "  -> Decode: Format B. Opcode: 0x" << std::hex << (int)opcode 
                  << " | Dest: R" << (int)destReg << " | Imm: 0x" << (int)srcRegOrImm << std::dec << "\033[0m" << std::endl;
    } else if (sig.is_16bit_immediate) {
        // Physical 2-byte consecutive Motherboard fetch to pull the 16-bit payload
        uint16_t currentPC = regBank.getPC();
        
        aBus.addressPin = currentPC;
        cBus.readEnable = true;
        mb.pulseClock();
        uint8_t highByte = dBus.dataPin;

        aBus.addressPin = currentPC + 1;
        cBus.readEnable = true;
        mb.pulseClock();
        uint8_t lowByte = dBus.dataPin;

        executionResult = (highByte << 8) | lowByte;
        
        std::cout << "\033[36m" << "  -> Decode: Format D (2-Word). Fetched Immediate: 0x" 
                  << std::hex << std::setw(4) << std::setfill('0') << executionResult 
                  << std::dec << "\033[0m" << std::endl;
                  
        // Fast-forward PC past the 2-byte immediate payload word
        regBank.setPC(currentPC + 2);
    } else if (sig.uses_alu) {
        uint8_t flags = regBank.getFlags();
        uint16_t operand1 = regBank.getGPR(static_cast<RegisterId>(destReg));
        uint16_t operand2 = regBank.getGPR(static_cast<RegisterId>(srcRegOrImm));
        
        std::cout << "\033[36m" << "  -> Decode: ALU Op. R" << (int)destReg << "(" << operand1 << ") and R" 
                  << (int)srcRegOrImm << "(" << operand2 << ")" << "\033[0m" << std::endl;
                  
        executionResult = alu.execute(sig.alu_operation, operand1, operand2, flags);
        regBank.setFlags(flags);
    }

    if (sig.is_memory_read) {
        uint16_t pointerAddress = regBank.getGPR(static_cast<RegisterId>(srcRegOrImm));
        aBus.addressPin = pointerAddress;
        cBus.readEnable = true;
        mb.pulseClock();
        executionResult = dBus.dataPin; 
        std::cout << "\033[36m" << "  -> Exec: Read 0x" << std::hex << executionResult << " from Mem Address 0x" << pointerAddress << std::dec << "\033[0m" << std::endl;
    }

    if (sig.writes_to_register) {
        std::cout << "\033[36m" << "  -> Writeback: R" << (int)destReg << " = " << executionResult << " (0x" << std::hex << executionResult << ")" << std::dec << "\033[0m" << std::endl;
        regBank.setGPR(static_cast<RegisterId>(destReg), executionResult); 
    }

    if (sig.is_memory_write) {
        uint16_t pointerAddress = regBank.getGPR(static_cast<RegisterId>(srcRegOrImm));
        uint16_t valueToWrite = regBank.getGPR(static_cast<RegisterId>(destReg));
        
        std::cout << "\033[36m" << "  -> Exec: Store 0x" << std::hex << valueToWrite << " to Mem Address 0x" << pointerAddress << std::dec << "\033[0m" << std::endl;

        aBus.addressPin = pointerAddress;
        dBus.dataPin = valueToWrite & 0xFF; 
        cBus.writeEnable = true;
        mb.pulseClock();
    }

    if (sig.is_branch) {
        bool shouldBranch = false;
        if (!sig.branch_on_zero && !sig.branch_on_not_zero) {
            shouldBranch = true;
        } else {
            bool isZeroFlag = (regBank.getFlags() & 0x01) != 0;
            if (sig.branch_on_zero && isZeroFlag) shouldBranch = true;
            if (sig.branch_on_not_zero && !isZeroFlag) shouldBranch = true;
        }

        if (shouldBranch) {
            uint16_t targetAddress = regBank.getGPR(static_cast<RegisterId>(srcRegOrImm));
            regBank.setPC(targetAddress);
        }
    }
}

```


**Tool Call: Read file `chips\processor\Processor.cpp`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\processor\Processor.cpp
#include "Processor.h"
#include "../motherboard/Motherboard.h"
#include "../motherboard/SystemBuses.h"
#include <iomanip>

Processor::Processor() 
    : clockSpeed(1), 
      currentTemperature(25.0f), 
      maxSafeTemperature(90.0f), 
      baseVoltage(1.2f),
      addressBus(nullptr), dataBus(nullptr), controlBus(nullptr) {
}

void Processor::connectBuses(AddressBus* aBus, DataBus* dBus, ControlBus* cBus) {
    addressBus = aBus;
    dataBus = dBus;
    controlBus = cBus;
}

void Processor::processCycle(Motherboard& mb, bool debugMode) {
    if (isHalted() || !addressBus || !dataBus || !controlBus) return;

    uint16_t pc = registerBank.getPC();

    // 1. The Fetch Cycle (Strict 16-bit via 2 byte pulls)
    // High Byte
    addressBus->addressPin = pc;
    controlBus->readEnable = true;
    mb.pulseClock();
    uint8_t highByte = dataBus->dataPin;

    // Low Byte
    addressBus->addressPin = pc + 1;
    controlBus->readEnable = true;
    mb.pulseClock();
    uint8_t lowByte = dataBus->dataPin;

    uint16_t instruction = (highByte << 8) | lowByte;
    registerBank.setIR(instruction);

    if (debugMode) {
        std::cout << "\033[33m" << "[CLK TICK] Fetched Instruction 0x" 
                << std::hex << std::setw(4) << std::setfill('0') << instruction 
                << " from Address 0x" << pc << std::dec << "\033[0m" << std::endl;
    }

    // 2. Increment PC by 2 (Word length)
    // Doing it here so relative jumps in decode phase have the correct base
    registerBank.setPC(pc + 2);

    // 3. Decode and Execute
    // The Control Unit Matrix handles all routing natively based on the 16-bit format
    controlUnit.decodeAndExecute(instruction, registerBank, alu, mb, *addressBus, *dataBus, *controlBus);

    // 4. Thermodynamics (Disabled for now)
    // currentTemperature += 2.0f;
    // if (clockSpeed > 1) currentTemperature += 5.0f;
    // 
    // if (currentTemperature > maxSafeTemperature) {
    //     triggerThermalShutdown();
    // }
}

void Processor::triggerThermalShutdown() {
    std::cout << "\n[CRITICAL ERROR] Thermal threshold (" 
              << maxSafeTemperature << " C) exceeded!" << std::endl;
    std::cout << "[SYSTEM HALTED] Processor Lock Engaged." << std::endl;
    
    uint8_t flags = registerBank.getFlags();
    flags |= 0x80; 
    registerBank.setFlags(flags);
}

void Processor::dumpState() const {
    std::cout << "\n=== PROCESSOR STATE DUMP ===" << std::endl;
    std::cout << "Temperature: " << currentTemperature << " C (Max: " << maxSafeTemperature << " C)" << std::endl;
    
    std::cout << "\n--- INTERNAL REGISTERS (16-bit) ---" << std::endl;
    for (int i = 0; i < 8; ++i) {
        std::cout << "R" << i     << ": 0x" 
                  << std::hex << std::setw(4) << std::setfill('0') 
                  << registerBank.getGPR(static_cast<RegisterId>(i)) << std::dec << std::endl;
    }
    
    std::cout << "PC   : 0x" << std::hex << std::setw(4) << std::setfill('0') << registerBank.getPC() << std::dec << std::endl;
    std::cout << "IR   : 0x" << std::hex << std::setw(4) << std::setfill('0') << registerBank.getIR() << std::dec << std::endl;
    std::cout << "FLAGS: 0x" << std::hex << std::setw(2) << std::setfill('0') << (int)registerBank.getFlags() << std::dec << std::endl;
    std::cout << "===========================" << std::endl;
}

```


**Tool Call: Read file `chips\main.cpp`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\main.cpp
#include <iostream>
#include <vector>
#include "processor/Processor.h"
#include "motherboard/Motherboard.h"
#include "motherboard/MemoryModule.h"
#include "motherboard/PowerSupply.h"
#include "motherboard/GraphicsCard.h"
#include "chassis/Monitor.h"
#include "chassis/Keyboard.h"
#include "Interpreter.h"
#include <fstream>
#include <sstream>

int main() {
    std::cout << "--- BOOTING SILICON PROTOCOL: TURING COMPLETE SIMULATION ---" << std::endl;

    // ==========================================================
    // 1. HARDWARE PROCUREMENT (Buying the physical parts)
    // ==========================================================
    Processor cpu;
    MemoryModule ram;
    PowerSupply psu(400.0f); // Standard ATX
    GraphicsCard gpu;
    Monitor display;
    Keyboard ioPanel;
    Motherboard mb;

    // ==========================================================
    // 2. STAGE ASSEMBLY (Plugging components into Motherboard)
    // ==========================================================
    gpu.connectMonitor(&display);
    mb.plugProcessor(&cpu);
    mb.plugRAM(&ram);
    mb.plugPSU(&psu);
    mb.plugGPU(&gpu);
    mb.plugKeyboard(&ioPanel);

    // 3. BIOS BOOT SEQUENCE & COMPILATION
    // ==========================================================
    std::cout << "\n[BIOS] Initializing Custom OS Interpreter..." << std::endl;
    
    std::cout << "--- BOOT MENU (Select OS Program) ---" << std::endl;
    std::cout << "1. Turing Complete Roman Urdu Calculator (programs/calculator.txt)" << std::endl;
    std::cout << "2. 'HELLO WORLD' Urdu Printer (programs/hello.txt)" << std::endl;
    std::cout << "3. Hardware Authentication Firewall (programs/auth.txt)" << std::endl;
    std::cout << "Selection (1-3): ";
    
    int choice;
    std::cin >> choice;
    
    std::cout << "Enable Cycle-by-Cycle Verbose Debug Logging? (Y/N): ";
    char debugChoice;
    std::cin >> debugChoice;
    bool debugMode = (debugChoice == 'Y' || debugChoice == 'y');
    
    std::cin.ignore(); // clear the newline for future getline() IO
    
    std::string filename = "";
    if (choice == 1) filename = "programs/calculator.txt";
    else if (choice == 2) filename = "programs/hello.txt";
    else filename = "programs/auth.txt";
    
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "[BIOS ERROR] Failed to load kernel payload: " << filename << std::endl;
        return 1;
    }
    
    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string targetOS = buffer.str();
    
    Interpreter compiler;
    CompilationResult compiledOS = compiler.compile(targetOS);

    std::cout << "[BIOS] Compiled OS script into " << compiledOS.codeSegment.size() << " native 16-bit instruction words." << std::endl;

    // ==========================================================
    // 4. THE BOOTLOADER (Flashing binary into RAM over physical Bus)
    // ==========================================================
    std::cout << "[BOOTLOADER] Flashing RAM via Motherboard DataBus..." << std::endl;
    uint16_t flashAddress = 0x0000;
    
    // Explicitly pushing bytes over the Motherboard pins exactly how hardware works
    for (uint16_t word : compiledOS.codeSegment) {
        // High Byte
        mb.getAddressBus().addressPin = flashAddress;
        mb.getDataBus().dataPin = (word >> 8) & 0xFF;
        mb.getControlBus().writeEnable = true;
        mb.pulseClock();
        flashAddress++;

        // Low Byte
        mb.getAddressBus().addressPin = flashAddress;
        mb.getDataBus().dataPin = word & 0xFF;
        mb.getControlBus().writeEnable = true;
        mb.pulseClock();
        flashAddress++;
    }
    
    std::cout << "[BOOTLOADER] Flashing Data Variables (.MAWAAD) from Address 0x0800..." << std::endl;
    uint16_t dataFlashAddress = 0x0800; // Byte offset 2048
    for (uint16_t word : compiledOS.dataSegment) {
        // High Byte
        mb.getAddressBus().addressPin = dataFlashAddress;
        mb.getDataBus().dataPin = (word >> 8) & 0xFF;
        mb.getControlBus().writeEnable = true;
        mb.pulseClock();
        dataFlashAddress++;

        // Low Byte
        mb.getAddressBus().addressPin = dataFlashAddress;
        mb.getDataBus().dataPin = word & 0xFF;
        mb.getControlBus().writeEnable = true;
        mb.pulseClock();
        dataFlashAddress++;
    }
    
    std::cout << "[BOOTLOADER] Flash Complete. Executing Processor Master Clock..." << std::endl;
    std::cout << "------------------------------------------------------------\n" << std::endl;

    // ==========================================================
    // 5. NATIVE HARDWARE CLOCK TICK LOOP
    // ==========================================================
    int maxTicks = 50000; // Infinite loop failsafe
    int tickCount = 0;

    // The CPU runs until it hits empty RAM (0x0000 = NOP, simulating EOF) or overheats
    while (!cpu.isHalted() && tickCount < maxTicks) {
        
        // Peek at RAM to ensure we haven't hit the end of the compiled script 
        // to gracefully exit the demonstration
        mb.getAddressBus().addressPin = cpu.getPC();
        mb.getControlBus().readEnable = true;
        mb.pulseClock();
        uint8_t hByte = mb.getDataBus().dataPin;
        
        mb.getAddressBus().addressPin = cpu.getPC() + 1;
        mb.getControlBus().readEnable = true;
        mb.pulseClock();
        uint8_t lByte = mb.getDataBus().dataPin;
        
        if (hByte == 0x00 && lByte == 0x00) {
           std::cout << "\n[PROCESSOR] End-Of-File (0x0000) reached at PC 0x" << std::hex << cpu.getPC() << std::dec << ". Halting." << std::endl;
           break;
        }

        // Pulse the CPU to fetch, decode, and execute natively from RAM!
        // We temporarily silence the CPU's internal clock tick cout if debugMode is off.
        // (A more professional approach would be passing the flag to `cpu.processCycle`, 
        // but for now, we just control the per-cycle dump).
        cpu.processCycle(mb, debugMode);
        
        if (debugMode) {
            cpu.dumpState();
        }
        tickCount++;
    }

    std::cout << "\n------------------------------------------------------------" << std::endl;
    // ==========================================================
    // 6. FINAL STATE DUMP (For Grader Asserts)
    // ==========================================================
    // Always dump the final state regardless of debug mode
    cpu.dumpState();
    
    // Flush buffered UI outputs from the GPU
    display.flushDisplay();

    return 0;
}

```


**Tool Call: Read file `chips\Interpreter.h`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\Interpreter.h
#pragma once
#include <vector>
#include <string>
#include <cstdint>
#include <map>

struct CompilationResult {
    std::vector<uint16_t> codeSegment;
    std::vector<uint16_t> dataSegment;
};

class Interpreter {
public:
    Interpreter() {}
    
    CompilationResult compile(const std::string& sourceCode);
    
private:
    std::map<std::string, uint16_t> labelMap;
    std::vector<uint16_t> parseLine(const std::string& line);
    uint8_t parseRegister(const std::string& regStr);
    
    std::vector<std::string> tokenize(const std::string& line);
};

```


**Tool Call: Read file `chips\programs\calculator.txt`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\programs\calculator.txt
// === TURING COMPLETE 4-OP CALCULATOR (URDU DIALECT) ===
BHARO R5, 0x0FF3   // R5 = Keyboard Int MMIO
BHARO R6, 0x0FF0   // R6 = Keyboard Char MMIO
BHARO R7, 0x0FF2   // R7 = Monitor Int MMIO

// We need a free register for Monitor Char MMIO (0x0FF1)
// R0=temp, R1=num1, R2=num2, R3=operator, R4=MonitorChar, R5=KeyInt, R6=KeyChar, R7=MonInt
BHARO R4, 0x0FF1   // R4 = Monitor Char MMIO

// 1. Read Num1
PARHO R1, [R5]     // Hardware parsing!

// 2. Read Operator
PARHO R3, [R6]         

// 3. Read Num2
PARHO R2, [R5]         

// 4. Output the equation UI: 'NUM1 OP NUM2 = '
RAKHO R1, [R7]         // Print Num1
BHARO R0, 32           // Space
RAKHO R0, [R4]
RAKHO R3, [R4]         // Print Op
RAKHO R0, [R4]
RAKHO R2, [R7]         // Print Num2
RAKHO R0, [R4]
BHARO R0, 61           // '='
RAKHO R0, [R4]
BHARO R0, 32           // Space
RAKHO R0, [R4]

// 5. Evaluate Operator
BHARO R0, 43
MUWAZANA R3, R0
BHARO R0, DO_JAMA
AGAR_SIFAR R0

BHARO R0, 45
MUWAZANA R3, R0
BHARO R0, DO_TAFREEK
AGAR_SIFAR R0

BHARO R0, 42
MUWAZANA R3, R0
BHARO R0, DO_ZARAB
AGAR_SIFAR R0

BHARO R0, 47
MUWAZANA R3, R0
BHARO R0, DO_TAQSEEM
AGAR_SIFAR R0

BHARO R0, KHATAM
CHHALANG R0

DO_JAMA:
JAMA R1, R2
BHARO R0, KHATAM
CHHALANG R0

DO_TAFREEK:
TAFREEK R1, R2
BHARO R0, KHATAM
CHHALANG R0

DO_ZARAB:
ZARAB R1, R2
BHARO R0, KHATAM
CHHALANG R0

DO_TAQSEEM:
TAQSEEM R1, R2

KHATAM:
RAKHO R1, [R7]         // Print final Int result
AARAM

```


**Tool Call: Read file `chips\programs\hello.txt`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\programs\hello.txt
.MAWAAD
MSG: "HELLO WORLD!\nThis is natively printing from the 0x0800 RAM DATA segment!\0"

.HIDAYAT
// R6 = Monitor Character MMIO address
BHARO R6, 0x0FF1 
// R5 = Pointer to string in RAM (Label MSG dynamically maps to 0x0800)
BHARO R5, MSG    
// R7 = Null terminator (0)
BHARO R7, 0      
// R0 = 1 (for incrementing the pointer)
BHARO R0, 1

LOOP:
// Load byte (character) from Motherboard memory at address R5 into R1
PARHO R1, [R5]   
// Compare the loaded character with Null terminator (R7)
MUWAZANA R1, R7  
// If we hit \0 (Equal), Jump to END
BHARO R2, END
AGAR_SIFAR R2   
// Print the character to Monitor
RAKHO R1, [R6]   
// Increment the string pointer (R5 = R5 + 1)
JAMA R5, R0      
// Jump back to the top of the loop
BHARO R2, LOOP
CHHALANG R2      

END:
AARAM

```


**Tool Call: Read file `chips\programs\auth.txt`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\programs\auth.txt
// === HARDWARE AUTHENTICATION FIREWALL ===
// Natively stores the secret PIN inside the 0x0800 ROM
// Scans realtime Keyboard IO and halts upon mismatch.

.MAWAAD
RAAZ: "786\0"
SAHI: "\n[SYSTEM] ACCESS GRANTED! Welcome back.\n\0"
GHALAT: "\n[SYSTEM] ACCESS DENIED! Core locked.\n\0"

.HIDAYAT
BHARO R5, RAAZ
BHARO R6, 0x0FF0 // Keyboard Char MMIO
BHARO R4, 0      // Null check / 0 check register

AGLA_HARF:
// Get character from Keyboard
PARHO R1, [R6]

// If key == 0 (no key), loop back and wait
MUWAZANA R1, R4
BHARO R0, AGLA_HARF
AGAR_SIFAR R0

// Read expected character from RAAZ Memory Block
PARHO R2, [R5]

// Compare key with expected character
MUWAZANA R1, R2
// If it doesn't match, INCORRECT! Jump to FAIL!
BHARO R0, NAKAAM  
AGAR_MAUJOOD R0

// IT MATCHED! Increment RAM offset pointer
BHARO R0, 1
JAMA R5, R0

// Did we hit the \0 in our password array yet?
PARHO R2, [R5]
MUWAZANA R2, R4
// If we hit \0, it means entire password succeeded!
BHARO R0, KAMYAAB 
AGAR_SIFAR R0

// Otherwise, jump back and check the next character
BHARO R0, AGLA_HARF
CHHALANG R0

// ==========================================
// SUCCESS AND FAILURE PRINTER BLOCKS
// ==========================================

NAKAAM:
BHARO R5, GHALAT
BHARO R0, CHHAPO
CHHALANG R0

KAMYAAB:
BHARO R5, SAHI

CHHAPO:
BHARO R6, 0x0FF1 // Monitor Character MMIO
BHARO R0, 1      // Pointer Incrementer

LOOP:
PARHO R1, [R5]
MUWAZANA R1, R4
BHARO R2, KHATAM
AGAR_SIFAR R2 // Exit if string hit \0

RAKHO R1, [R6] // Write to Phosphor Display
JAMA R5, R0    // Increment pointer
BHARO R2, LOOP
CHHALANG R2

KHATAM:
AARAM

```


**Tool Call: Read file `chips\Interpreter.cpp`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\Interpreter.cpp
#include "Interpreter.h"
#include <sstream>
#include <iostream>
#include <algorithm>

std::vector<std::string> Interpreter::tokenize(const std::string& line) {
    std::vector<std::string> tokens;
    std::stringstream ss(line);
    std::string token;
    
    while (ss >> token) {
        if (!token.empty() && token.back() == ',') {
            token.pop_back();
        }
        tokens.push_back(token);
    }
    return tokens;
}

uint8_t Interpreter::parseRegister(const std::string& regStr) {
    std::string cleanReg = regStr;
    if (cleanReg.front() == '[') cleanReg.erase(0, 1);
    if (cleanReg.back() == ']')  cleanReg.pop_back();

    if (cleanReg.size() >= 2 && cleanReg[0] == 'R') {
        int regNum = cleanReg[1] - '0';
        if (regNum >= 0 && regNum < 8) return static_cast<uint8_t>(regNum);
    }
    return 0; 
}

std::vector<uint16_t> Interpreter::parseLine(const std::string& line) {
    size_t commentPos = line.find("//");
    std::string cleanLine = (commentPos != std::string::npos) ? line.substr(0, commentPos) : line;
    
    std::vector<std::string> tokens = tokenize(cleanLine);
    if (tokens.empty()) return {0x0000}; // NOP
    
    std::string mnemonic = tokens[0];
    std::vector<uint16_t> payload;
    
    if (mnemonic == "AARAM" || mnemonic == "NOP") {
        payload.push_back(0x0000);
    }
    else if (mnemonic == "JAMA" || mnemonic == "ADD") { 
        uint8_t dest = parseRegister(tokens[1]);
        uint8_t src  = parseRegister(tokens[2]);
        payload.push_back((0x01 << 8) | ((dest & 0x0F) << 4) | (src & 0x0F));
    }
    else if (mnemonic == "TAFREEK" || mnemonic == "SUB") { 
        uint8_t dest = parseRegister(tokens[1]);
        uint8_t src  = parseRegister(tokens[2]);
        payload.push_back((0x02 << 8) | ((dest & 0x0F) << 4) | (src & 0x0F));
    }
    else if (mnemonic == "ZARAB" || mnemonic == "MUL") { 
        uint8_t dest = parseRegister(tokens[1]);
        uint8_t src  = parseRegister(tokens[2]);
        payload.push_back((0x03 << 8) | ((dest & 0x0F) << 4) | (src & 0x0F));
    }
    else if (mnemonic == "TAQSEEM" || mnemonic == "DIV") { 
        uint8_t dest = parseRegister(tokens[1]);
        uint8_t src  = parseRegister(tokens[2]);
        payload.push_back((0x04 << 8) | ((dest & 0x0F) << 4) | (src & 0x0F));
    }
    else if (mnemonic == "MUWAZANA" || mnemonic == "CMP") { 
        uint8_t dest = parseRegister(tokens[1]);
        uint8_t src  = parseRegister(tokens[2]);
        payload.push_back((0x0A << 8) | ((dest & 0x0F) << 4) | (src & 0x0F));
    }
    else if (mnemonic == "CHHALANG" || mnemonic == "JMP") { 
        uint8_t src  = parseRegister(tokens[1]); 
        payload.push_back((0x10 << 8) | (src & 0x0F));
    }
    else if (mnemonic == "AGAR_SIFAR" || mnemonic == "JZ") { 
        uint8_t src  = parseRegister(tokens[1]);
        payload.push_back((0x11 << 8) | (src & 0x0F));
    }
    else if (mnemonic == "AGAR_MAUJOOD" || mnemonic == "JNZ") { 
        uint8_t src  = parseRegister(tokens[1]);
        payload.push_back((0x12 << 8) | (src & 0x0F));
    }
    else if (mnemonic == "BHARO" || mnemonic == "DAALO" || mnemonic == "LDR_IMM") { 
        uint8_t dest = parseRegister(tokens[1]);
        uint16_t immFull = 0;
        
        bool isNumber = isdigit(tokens[2][0]) || (tokens[2].size() > 1 && tokens[2][1] == 'x');
        if (isNumber) {
            try {
                immFull = std::stoi(tokens[2], nullptr, 0); 
            } catch (...) {
                std::cout << "[COMPILER ERROR] Invalid immediate format: " << tokens[2] << std::endl;
            }
        } else {
            if (labelMap.find(tokens[2]) != labelMap.end()) {
                immFull = labelMap[tokens[2]];
            } else {
                std::cout << "[COMPILER ERROR] Unresolved Label: " << tokens[2] << std::endl;
            }
        }
        
        // If it's a Label, it was tracked as 4 bytes in Pass 1, so we must force Format D
        if (!isNumber || immFull > 0x0F) {
            // Requires 2-word 16-bit payload (Format D)
            payload.push_back((0x1B << 8) | ((dest & 0x0F) << 4)); // Header word
            payload.push_back(immFull);                            // Payload word
        } else {
            // Fits in 4 bits (Format B)
            payload.push_back((0x1A << 8) | ((dest & 0x0F) << 4) | (immFull & 0x0F));
        }
    }
    else if (mnemonic == "PARHO" || mnemonic == "LDR") { 
        uint8_t dest = parseRegister(tokens[1]);
        uint8_t src  = parseRegister(tokens[2]); 
        payload.push_back((0x20 << 8) | ((dest & 0x0F) << 4) | (src & 0x0F));
    }
    else if (mnemonic == "RAKHO" || mnemonic == "STR") { 
        uint8_t srcVal = parseRegister(tokens[1]);
        uint8_t ptrReg = parseRegister(tokens[2]); 
        payload.push_back((0x21 << 8) | ((srcVal & 0x0F) << 4) | (ptrReg & 0x0F));
    }
    else {
        std::cout << "[COMPILER ERROR] Unrecognized Mnemonic: " << mnemonic << std::endl;
    }
    
    return payload;
}

CompilationResult Interpreter::compile(const std::string& sourceCode) {
    CompilationResult result;
    std::stringstream ss(sourceCode);
    std::string line;
    
    // storing pairs of {type, content}
    // type 0 = code, type 1 = data
    std::vector<std::pair<int, std::string>> processLines;
    
    labelMap.clear();
    uint16_t currentCodePC = 0;
    uint16_t currentDataPC = 0x0800;
    bool inDataSection = false;
    
    // Pass 1: PC Tracking and Label Mapping
    while (std::getline(ss, line)) {
        line.erase(0, line.find_first_not_of(" \t\r\n"));
        if (line.empty() || line.find("//") == 0) continue; 
        
        size_t commentPos = line.find("//");
        std::string cleanLine = (commentPos != std::string::npos) ? line.substr(0, commentPos) : line;
        cleanLine.erase(cleanLine.find_last_not_of(" \t\r\n") + 1);
        
        if (cleanLine == ".MAWAAD" || cleanLine == ".DATA" || cleanLine == ".mawaad" || cleanLine == ".data") {
            inDataSection = true;
            continue;
        }
        if (cleanLine == ".HIDAYAT" || cleanLine == ".CODE" || cleanLine == ".hidayat" || cleanLine == ".code") {
            inDataSection = false;
            continue;
        }
        
        if (inDataSection) {
            size_t colonPos = cleanLine.find(':');
            if (colonPos != std::string::npos) {
                std::string labelName = cleanLine.substr(0, colonPos);
                labelName.erase(labelName.find_last_not_of(" \t") + 1);
                labelMap[labelName] = currentDataPC;
                
                std::string valueStr = cleanLine.substr(colonPos + 1);
                valueStr.erase(0, valueStr.find_first_not_of(" \t"));
                
                processLines.push_back({1, valueStr});
                
                if (!valueStr.empty() && valueStr.front() == '"') {
                    // String literal
                    int chars = 0;
                    for (size_t i = 1; i < valueStr.size() && valueStr[i] != '"'; ++i) {
                        if (valueStr[i] == '\\' && i + 1 < valueStr.size()) {
                            i++; // escape sequence
                        }
                        chars++;
                    }
                    int words = (chars + 1) / 2;
                    currentDataPC += words * 2;
                } else {
                    // Integer array or single int
                    int commas = std::count(valueStr.begin(), valueStr.end(), ',');
                    int words = commas + 1;
                    currentDataPC += words * 2;
                }
            }
        } else {
            if (cleanLine.back() == ':') {
                std::string labelName = cleanLine.substr(0, cleanLine.size() - 1);
                labelMap[labelName] = currentCodePC;
                continue; // Label takes 0 bytes
            }
            
            processLines.push_back({0, cleanLine});
            
            std::vector<std::string> tokens = tokenize(cleanLine);
            if (tokens.empty()) continue;
            
            // Calculate instruction byte size
            std::string mnemonic = tokens[0];
            if (mnemonic == "BHARO" || mnemonic == "DAALO" || mnemonic == "LDR_IMM") {
                if (tokens.size() > 2) {
                    bool isNumber = isdigit(tokens[2][0]) || (tokens[2].size() > 1 && tokens[2][1] == 'x');
                    if (isNumber) {
                        try {
                            uint16_t immFull = std::stoi(tokens[2], nullptr, 0); 
                            if (immFull <= 0x0F) currentCodePC += 2;
                            else currentCodePC += 4; // Format D
                        } catch (...) {
                            currentCodePC += 4; // Fallback
                        }
                    } else {
                        currentCodePC += 4; // Labels unconditionally 2 words
                    }
                } else {
                    currentCodePC += 2;
                }
            } else {
                currentCodePC += 2; // Fixed width defaults
            }
        }
    }
    
    // Pass 2: Instruction Generation
    for (const auto& item : processLines) {
        if (item.first == 1) { // DATA
            std::string valueStr = item.second;
            if (!valueStr.empty() && valueStr.front() == '"') {
                std::vector<uint8_t> bytes;
                for (size_t i = 1; i < valueStr.size() && valueStr[i] != '"'; ++i) {
                    if (valueStr[i] == '\\' && i + 1 < valueStr.size()) {
                        i++;
                        if (valueStr[i] == '0') bytes.push_back(0);
                        else if (valueStr[i] == 'n') bytes.push_back('\n');
                        else bytes.push_back(valueStr[i]);
                    } else {
                        bytes.push_back(valueStr[i]);
                    }
                }
                if (bytes.size() % 2 != 0) bytes.push_back(0); // Word alignment
                for (size_t i = 0; i < bytes.size(); i += 2) {
                    result.dataSegment.push_back((bytes[i] << 8) | bytes[i+1]);
                }
            } else {
                std::stringstream vss(valueStr);
                std::string token;
                while (std::getline(vss, token, ',')) {
                    token.erase(0, token.find_first_not_of(" \t"));
                    token.erase(token.find_last_not_of(" \t") + 1);
                    try {
                        uint16_t val = std::stoi(token, nullptr, 0);
                        result.dataSegment.push_back(val);
                    } catch (...) {
                        result.dataSegment.push_back(0);
                    }
                }
            }
        } else { // CODE
            std::vector<uint16_t> words = parseLine(item.second);
            for (uint16_t word : words) {
                result.codeSegment.push_back(word);
            }
        }
    }
    
    return result;
}

```


**Tool Call: Read file `chips\motherboard\PowerSupply.h`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\motherboard\PowerSupply.h
#pragma once
#include <iostream>
#include "processor/Processor.h"
#include "MemoryModule.h"
#include "GraphicsCard.h"

class Motherboard; // Forward decl

class PowerSupply {
private:
    float maxCapacityWatts;
    Motherboard* connectedBoard; // Aggregation back-reference

public:
    PowerSupply(float capacity) : maxCapacityWatts(capacity), connectedBoard(nullptr) {}

    void plugIntoBoard(Motherboard* board) {
        connectedBoard = board;
    }

    // Called every cycle. If the aggregated systems draw too much,
    // the PSU trips the motherboard's breaker.
    void enforcePowerLimits(float currentTotalDraw); 
};

```


**Tool Call: Read file `chips\motherboard\NetworkCard.h`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\motherboard\NetworkCard.h
#pragma once
#include <iostream>
#include <cstdint>

class NetworkSwitch; // Forward Declaration

// An Aggregated Component that plugs into the Motherboard AND the external Network Switch.
class NetworkCard {
private:
    NetworkSwitch* connectedSwitch;
    float wattageActive;
    float wattageIdle;
    bool isActiveTick;
    uint8_t receiveBuffer;
    bool hasData;

public:
    NetworkCard() : connectedSwitch(nullptr), wattageActive(5.0f), wattageIdle(0.5f), 
                    isActiveTick(false), receiveBuffer(0), hasData(false) {}

    // Plugs this PC's card into the central Switch
    void plugIntoSwitch(NetworkSwitch* sw);

    // Called by the Processor -> Motherboard -> NetworkCard
    void transmit(uint8_t data);

    // Called by the NetworkSwitch when another PC broadcasts
    void receive(uint8_t data) {
        receiveBuffer = data;
        hasData = true;
        isActiveTick = true;
    }

    bool hasPendingData() const { return hasData; }

    // Read by the Processor
    uint8_t readBuffer() {
        hasData = false;
        isActiveTick = true;
        return receiveBuffer;
    }

    float pollPowerDraw() {
        float draw = isActiveTick ? wattageActive : wattageIdle;
        isActiveTick = false;
        return draw;
    }
    
    void dumpState() const {
        if (hasData) {
            std::cout << "[NIC] Pending Packet in Buffer: 0x" 
                      << std::hex << (int)receiveBuffer << std::dec << std::endl;
        } else {
            std::cout << "[NIC] Buffer Empty." << std::endl;
        }
    }
};

```


## Assistant

<thinking>
Now I have a thorough understanding of the entire codebase. Let me now synthesize everything into a proper "Hardware Specification Manual" for the assignment docs section.

Key things I need to document:

## Architecture Overview
The Onyx-16 is a 16-bit architecture.

## Components to Document:

### 1. The Storage Cells (RegisterBank → Register class concept)
- 8 General Purpose Registers: R0–R7, each 16-bit wide
- Program Counter (PC): 16-bit, byte address of next instruction
- Instruction Register (IR): 16-bit, currently executing instruction


- FLAGS register: 8-bit with Zero, Negative, Positive, and HALT flags that track comparison results and system state, though these are internally managed and inaccessible from outside the processor

### 2. The ALU
The arithmetic and logic unit supports a full set of operations including addition, subtraction, multiplication, division, bitwise operations, and comparisons, taking two 16-bit operands and producing a 16-bit result that updates the FLAGS register accordingly.

### 3. The Buses
The system uses a 16-bit address bus, an 8-bit data bus for byte-level access, and control lines for read/write signaling—all owned and managed by the motherboard.

### 4. Memory
The system has 3840 bytes of addressable memory from 0x0000 to 0x0EFF, with anything beyond that triggering a segmentation fault, divided into a code segment for the bootloader and additional regions for data and memory-mapped I/O.

### 5. I/O Mapping
The upper memory addresses handle input and output: keyboard and monitor character I/O at 0x0FF0 and 0x0FF1, plus integer variants at 0x0FF3 and 0x0FF2.

### 6. The CPU
The processor manages clock cycles and thermal limits, executing the fetch-decode-execute pipeline while coordinating with the motherboard through its buses and internal components like the register bank, cache, and ALU.

### 7. Control Unit
The control unit contains a 256-entry microcode ROM that decodes instructions...

Now I'm looking at how instructions are structured—there are three main formats depending on whether we're working with two registers, a register with a small immediate value, or a register with a full 16-bit immediate that spans two words.

The L1 cache holds 16 bytes organized as 8 words, mapping to a RAM address and triggering bus transactions on misses. The motherboard ties everything together with its address, data, and control buses.

The graphics card and monitor handle character and integer output to a 32x16 display that buffers and renders in blocks. The keyboard provides input through a queue with methods to fetch the next keystroke or parse integers, plus a pin to check for pending data. I'm now looking at the instruction set table that maps opcodes to mnemonics and their formats. Continuing through the instruction set with conditional jumps based on flag states, then loading operations that handle both immediate values and memory references.

Now I'm thinking about how to structure this as an authentic hardware manual—using physical metaphors like sealed units and etched pathways instead of object-oriented terminology, while still forcing a design that naturally requires encapsulation and controlled access patterns through read/write signals. Writing the manual structure... I'm continuing to map out the I/O address space with the interrupt output lines, then moving into the peripheral architecture—the keyboard with its blocking input behavior, the display unit that handles both character and integer output through separate memory-mapped ports, and finally the processor itself with its 1 MHz clock, internal cache, and requirement to be connected to a mainboard to function.

Now I'm reviewing the complete system architecture: the mainboard's role in managing the physical buses and component sockets, how the clock pulse gets routed through the system, and the way MMIO requests get intercepted. I'm getting a clear sense of how all these pieces fit together, and I'm ready to synthesize this into a cohesive hardware specification document that emphasizes the pedagogical constraints around sealed storage, electrical interfaces, and the physical nature of the components. , no input/output capability on its own. The processor doesn't own the mainboard—it plugs into one, and the mainboard persists independently before and after the CPU is installed. The mainboard also contains a hardware address decoder that inspects bus transactions and routes peripheral addresses to the appropriate device rather than RAM. To establish the single correct answer, I need to clarify the key distinction: components removed from the system must leave others intact, which separates aggregation from composition—the pathways are physically part of the mainboard's substrate, while the CPU merely holds a connector reference to it.

Now I'm planning out the full technical specification as a hardware manual. I'll structure it into major sections covering system architecture, storage, the arithmetic core, buses, memory, address mapping, and peripherals, presenting this as a case study rather than just listing concepts. The Processor Die**
**Section IX: The Mainboard**
**Section X: The Assembly Manual (main.cpp spec)**
**Appendix A: Instruction Set Reference**
**Appendix B: Instruction Encoding Formats**

Let me write this now. I'll be thorough but also make it elegant.

Key design decisions I need to encode:
1. StorageBank (RegisterBank) must be a sealed unit → forces a class with private data
2. ALU must be a sealed execution unit with internal flags mutation → forces ALU class that takes a reference to flags
3. Buses must be owned by Motherboard → forces composition
4. CPU plugs into Motherboard (not the other way) → forces aggregation in CPU
5. MMIO routing happens in Motherboard → forces routing logic in Motherboard class
6. Components are interchangeable (can be swapped) → forces clean interfaces

Now I need to clarify the actual architecture: the RegisterBank owns all registers including FLAGS, and the ALU receives a reference to FLAGS so it can mutate it during execution. This means the FLAGS register physically lives in the RegisterBank, but the ALU has a direct connection to update it. The spec should reflect this borrowing relationship accurately—the ALU seals the computation logic while the FLAGS latch itself remains part of the RegisterBank's sealed storage. Now I'm mapping out the instruction set with the Arabic mnemonics paired to their opcodes—covering arithmetic operations like addition and subtraction, logical comparisons, jump instructions for control flow, and memory operations for loading and storing values.

Looking at the instruction formats, there are three main patterns: a standard format with opcode, destination, and source registers; a variant for 4-bit immediate values; and a 2-word format for 16-bit immediates. The opcode 0x00 serves double duty as both NOP and an implicit halt condition—when the processor encounters 0x0000, it terminates execution. The flags byte tracks conditions like the zero flag to support conditional branching.

Now I'm drafting the full processor architecture reference manual as a formal technical document with hardware-focused language and precise numerical specifications. bits | General-purpose register |
| R1 | 16 bits | General-purpose register |
| R2 | 16 bits | General-purpose register |
| R3 | 16 bits | General-purpose register |
| R4 | 16 bits | General-purpose register |
| R5 | 16 bits | General-purpose register |
| R6 | 16 bits | General-purpose register |
| R7 | 16 bits | General-purpose register |
| R8 | 16 bits | General-purpose register |
| R9 | 16 bits | General-purpose register |
| R10 | 16 bits | General-purpose register |
| R11 | 16 bits | General-purpose register |
| R12 | 16 bits | General-purpose register |
| R13 | 16 bits | General-purpose register |
| R14 | 16 bits | General-purpose register |

The Storage Bank also contains two special-purpose registers that are not directly addressable by user code:

| Cell Name | Width | Purpose |
|-----------|-------|---------|
| PC | 16 bits | Program Counter — holds the address of the next instruction to fetch |
| SR | 16 bits | Status Register — holds processor state flags |

So the processor has fifteen general-purpose registers plus two special registers that track execution state and control flow. Looking at the register architecture and how the FLAGS register works as a status latch with only three defined bits that need to be preserved during any write operations. Now I'm looking at the Arithmetic Execution Core architecture—it's a stateless combinational block that takes a 4-bit operation code and two 16-bit operands, then outputs a result while updating the FLAGS latch directly. The ALU supports various operations like addition and subtraction, each with specific behaviors for writing results and updating flags. Now I'm detailing how CMP works differently from other operations — it sets flags based on the comparison result without writing anything to a register. I should also note that arithmetic operations use unsigned 16-bit math with silent overflow wrapping, and the FLAGS latch gets updated directly by the ALU's internal circuitry rather than being a separate output that the Control Unit reads afterward. The next section is introducing the system's three main buses.

The three System Pathways are physical copper traces on the mainboard itself, not separate components — they can't exist independently of the board. The Address Pathway carries 16-bit addresses, the Data Pathway handles 8-bit transfers, and the Control Pathway manages two signal lines for read and write operations. Every memory transaction follows a standardized three-step protocol that the initiator begins by...

Actually, let me continue with the protocol flow: the initiator places an address on the Address Pathway, then for reads it asserts READ ENABLE and waits for data to appear on the Data Pathway, while for writes it places data on the Data Pathway and asserts WRITE ENABLE to trigger the transfer. Only one transaction happens per clock cycle, and the pathways can't be shared simultaneously.

Now I'm moving into the memory module itself — the ONYX-16 has a single flat, byte-addressable memory array with a total capacity of 3,840 bytes.

Looking at the memory specifications: valid addresses range from 0x0000 to 0x0EFF, each cell holds 8 bits, and everything starts at 0x00 on power-up. Any access beyond 0x0EFF causes a segmentation fault — reads return 0xFF and writes get dropped, but either way a diagnostic message gets logged.

Now I'm examining the hardware address decoder and how the physical memory map is organized across different regions... I see how the memory-mapped I/O works now—when the CPU tries to access addresses 0x0FF0 through 0x0FF3, the mainboard intercepts those transactions before they reach RAM and routes them to the appropriate peripherals instead. The keyboard input port returns ASCII values and blocks execution if the buffer is empty, while the display output ports accept bytes to be rendered as characters or integers. The keyboard suspends execution when its buffer empties, resuming once the user provides input. The mainboard communicates with the keyboard through a PENDING_INPUT pin that signals available data, and READ_CHAR and READ_INT lines that retrieve either individual characters or complete decimal integers from the buffer. The graphics card connects via PCIe and processes byte payloads from the mainboard's MMIO ports to render output on the display. to Mainboard:**
- **CHAR_PAYLOAD line (0x0FF1):** Receives an 8-bit byte and forwards it as-is to the display as an ASCII character.
- **INT_PAYLOAD line (0x0FF2):** Receives an 8-bit byte, converts it to a decimal digit string, and writes each character to the display sequentially.

The graphics card requires a display unit to be physically connected to its output connector. If no display is connected, all output is silently discarded.

### 7.3 The Display Unit (Monitor)

The display unit is a **32-column × 16-row phosphor CRT screen**. It maintains an internal character buffer that stores incoming characters, with text wrapping to the next row after 32 columns and clipping anything beyond 16 rows. The buffer isn't flushed to screen during execution—instead, the display renders everything at program completion within the bordered CRT frame.

---

## CHAPTER 8: THE PROCESSOR

The Processor is a single-chip unit containing four internal sub-units: a Storage Bank for all registers, an Arithmetic Execution Core for computation, an L1 Block Cache for instruction prefetching, and a Control Unit that decodes instructions and orchestrates everything. The Processor connects to the mainboard via three physical bus connector ports on its bottom surface, and without a mainboard connection providing voltage, it cannot execute.The user wants me to continue writing the hardware specification manual. Let me continue from where I left off - I was in the middle of writing the L1 Block Cache section (8.1). Let me continue from there and complete the full document.

Let me recall where I was:

I was writing the full "ONYX-16 PROCESSOR ARCHITECTURE REFERENCE MANUAL" and had gotten through:
- Chapter 1: System Architecture
- Chapter 2: The Storage Bank
- Chapter 3: The Arithmetic Execution Core
- Chapter 4: The System Pathways
- Chapter 5: The Memory Module
- Chapter 6: The Memory Address Map
- Chapter 7: The Peripheral Units


- Chapter 8: The Processor (started, got through sub-unit table and intro, started 8.1 L1 Block Cache but cut off)

Now I need to finish the L1 Block Cache section and move through the Control Unit, Clock Cycle explanation, then tackle the Mainboard chapter, Assembly Sequence, and both appendices on instruction sets and encoding.

For the L1 Cache, I'm focusing on the 16-byte block structure with validity tracking and address mapping—students need to grasp how this optimizes instruction fetching before we layer in the Control Unit's microcode ROM and its 256-entry instruction decoding logic. The Control Unit is where the real complexity lives: mapping instructions to control signals and orchestrating the full decode-and-execute flow.

The processor's clock cycle is straightforward conceptually—fetch two bytes, increment the program counter by 2, then decode and execute through the Control Unit—but I need to make sure the timing and sequencing are crystal clear. The Mainboard chapter ties everything together through composition and aggregation patterns, showing how buses connect components and how the pulseClock() method routes signals throughout the system.

For the Assembly Sequence, the order matters pedagogically: construct components first, then plug the GPU into the Monitor before wiring everything into the Mainboard. The appendices on instruction set reference and encoding formats will serve as lookup tables students reference while implementing, and the optional source language appendix rounds out the learning materials.

Generating the ISA reference table... Looking at the instruction set table continuing with jump and load operations, I'm seeing conditional jumps based on the zero flag and various load instructions that handle both immediate values and memory addresses.

Now I'm clarifying the encoding format for these instructions—the jump operations only use the src field to specify which register holds the target address, while the store instruction packs the value register into the dest nibble and the pointer register into the src nibble.

Looking at the control unit implementation, I can see that for memory writes, the dest register (bits 7:4) holds the value to write and the src register (bits 3:0) holds the pointer address, which confirms the encoding scheme.

For memory reads like PARHO and LDR, the data from memory gets loaded into the destination register, with the source register again providing the address. The assembly syntax maps directly to this: `PARHO R1, [R5]` loads Memory[R5] into R1, while `RAKHO R1, [R6]` stores R1 to Memory[R6].

Now I need to map out the microcode ROM structure for the Control Unit...

Defining the ControlSignals struct...

Now I need to wire up the assembly sequence in main.cpp: instantiate all the hardware components, connect the GPU to the display, plug everything into the motherboard, load the binary through the bus via bootloader, then start the clock loop.

The bootloader handles the actual binary flashing through direct bus transactions.

I'm reconsidering how to structure the documentation—the user wants this framed as a case study, so I should write it as a complete, well-organized spec rather than fragments. Let me continue from where the L1 Block Cache description ended and build out the rest of the document properly.
</thinking>

Let me finish reading the remaining files before writing, to make sure I have everything.

**Tool Call: Read file `chips\motherboard\PowerSupply.cpp`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\motherboard\PowerSupply.cpp
#include "PowerSupply.h"
#include "Motherboard.h"

void PowerSupply::enforcePowerLimits(float currentTotalDraw) {
    if (!connectedBoard) return;
    
    // The Trap: A sudden GPU spike + CPU Overclock will trip this limit.
    if (currentTotalDraw > maxCapacityWatts) {
        std::cout << "\n[CRITICAL WARNING] Power Draw (" << currentTotalDraw 
                  << "W) exceeded PSU Capacity (" << maxCapacityWatts << "W)!" 
                  << std::endl;
        
        // This is where an AI code-gen fails. 
        // A generic AI wouldn't trace the logic back to the Aggregated board pointer to kill the main system loop.
        connectedBoard->killPower();
    }
}

```


**Tool Call: Read file `chips\NetworkLogic.cpp`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\chips\NetworkLogic.cpp
#include "network/NetworkSwitch.h"
#include "motherboard/NetworkCard.h"

void NetworkSwitch::broadcast(uint8_t data, NetworkCard* sender) {
    std::cout << "[SWITCH] Broadcasting 0x" << std::hex << (int)data << std::dec << " to all connected nodes." << std::endl;
    // Route to every attached PC except the one that sent it
    for (auto* node : connectedNodes) {
        if (node != sender) {
            node->receive(data);
        }
    }
}

void NetworkCard::plugIntoSwitch(NetworkSwitch* sw) {
    connectedSwitch = sw;
    sw->plugInNode(this); // Handshake
}

void NetworkCard::transmit(uint8_t data) {
    isActiveTick = true;
    if (connectedSwitch) {
        std::cout << "[NIC] Transmitting: 0x" << std::hex << (int)data << std::dec << std::endl;
        connectedSwitch->broadcast(data, this);
    } else {
        std::cout << "[NIC] Error: No network cable connected." << std::endl;
    }
}

```


**Tool Call: Read file `docs\Assignment_Difficulty_Analysis.md`**
Status: Completed

```D:\WISDOM\TAship\A3\chips\docs\Assignment_Difficulty_Analysis.md
# Project Silicon Protocol: Comprehensive Architecture & Difficulty Analysis

This document serves as an exhaustive breakdown of the Custom Virtual CPU, Motherboard, and Operating System Software stack successfully developed in C++. It is intended to help assess the overall difficulty, scope, and engineering rigor required to complete this assignment.

---

## 1. The Physical Hardware Simulation Layer (C++)
The lowest level of this project is a clock-accurate simulation of hardware components communicating over physical electronic buses.

### 1.1 The Motherboard (`SystemBuses.h`, `Motherboard.h`)
- **Discrete Buses**: Implemented `AddressBus` (16-bit), `DataBus` (16-bit payload), and `ControlBus` (Read/Write Enable booleans) as pure data structs.
- **Clock Pulsing**: The Motherboard acts as the central timing mechanism via `mb.pulseClock()`, coordinating transfers between the CPU and Peripherals.
- **Memory-Mapped I/O (MMIO)**: RAM addresses `0x0FF0` to `0x0FF3` are intercepted in the router logic to pipe data off-board to hardware peripherals (Keyboard/Monitor) instead of standard RAM.

### 1.2 The Central Processing Unit (`Processor.h`, `CPU.cpp`)
- **Register Bank**: Emulates eight 16-bit General Purpose Registers (`R0 - R7`), the Program Counter (`PC`), the Instruction Register (`IR`), and an 8-bit `FLAGS` register for conditional branch states (Zero/Negative).
- **The ALU**: A mathematical logic unit capable of Add, Subtract, Multiply, and Divide. Native conditional flags (Zero `ZF`, Sign `SF`) are accurately set based on ALU calculation limits.
- **The Control Unit (ROM Microcode)**: Rather than massive `switch-case` blocks, the Control Unit utilizes an array-based Microcode ROM that maps dynamic 8-bit opcodes into direct signal flags to flip multiplexer pins (e.g., `aluEnable`, `memoryWrite`). 

### 1.3 The Peripheral Devices
- **Graphics Card & Monitor**: Translates raw bytes from the Motherboard Bus into characters or handles complex integer-to-string multi-digit buffering via MMIO port `0x0FF2` before drawing them to the console in phosphor-green ANSI text.
- **Keyboard CHASSIS**: Buffers real-time string inputs, strips whitespace natively via `cleanWhitespace()` tokenization, and feeds integers or raw bytes sequentially to the CPU over MMIO upon request, deliberately causing `[Hardware Interrupt]` simulation pauses.

----------

## 2. The Custom Instruction Set Architecture (ISA)
A completely original 16-bit Machine Learning Instruction Set Architecture was designed to natively interface with the Control Unit.

- **Native Format B (4-bit payloads)**: Packed instructions holding 8-bit opcode + 4-bit destination + 4-bit source/immediate. Example: `ADD R1, R2`.
- **Extended Format D (2-Word / 32-bit)**: Handles complex immediate values spanning beyond 4 bits (e.g., `LDR_IMM R1, 0x0800`). It utilizes an explicit payload packet design that halts the clock to pull an extra 16 bits off the bus.

----------

## 3. The Two-Pass Software Compiler (`Interpreter.cpp`)
Rather than expecting humans to write raw hex opcodes, a comprehensive C++ string-parsing Compiler was engineered. This is arguably the most algorithmically complex piece of the codebase.

### 3.1 Pass 1: Syntax Analysis & Memory Partitioning
- **Dual Segment Parsing**: Reads `.MAWAAD` (`.DATA`) and `.HIDAYAT` (`.CODE`) scope directives natively.
- **Address Tracking (`currentPC` and `currentDataPC`)**: Measures the exact byte-width of instructions, string literals, and dynamic integer arrays, calculating future physical RAM constraints without generating final binaries.
- **Label Resolution (`std::map`)**: Tracks `JMP` destination anchors and Pointer Variable anchors and calculates their exact physical address starting at `0x0000` (Code) or `0x0800` (Data).

### 3.2 Pass 2: Binary Injection & Explosive Packing
- Generates a `CompilationResult` struct returning a `codeSegment` array and a `dataSegment` array.
- Evaluates string literals (`"HELLO WORLD!\0"`) and explodes them dynamically into 16-bit binary-aligned hex arrays. 
- Resolves Jump Labels to their numeric pointers.

### 3.3 Novelty: Native Roman Urdu Instruction Dialect
The entire string-matching logic in the Assembler was re-mapped to semantic Roman Urdu vocabulary. The compiler natively digests words like `JAMA` (`ADD`), `TAFREEK` (`SUB`), `PARHO` (`LDR`), `AGAR_SIFAR` (`JZ`), and `AARAM` (`NOP`).

----------

## 4. The BIOS Bootloader (`main.cpp`)
The main loop ties the Hardware and Software systems together.
- **Interactive Menu**: Prompts standard `cin` to load custom `.txt` files containing Urdu Assembly programs.
- **Debug Silencing Toggle**: The `debugMode` boolean filters out the immense wall of Clock-Tick logs natively injected into the execution blocks.
- **Multi-Vector Flash Sequence**: Emulates physical CD-ROM spin-up by locking `mb.pulseClock()` loops to push the generated `codeSegment` array byte-by-byte into Address `0x0000`, followed by a separate independent routine pushing the `dataSegment` array to Address `0x0800`.

----------

## 5. Turing-Complete OS Payloads (Roman Urdu Assembly)
To prove the architecture's mathematical and conditional breadth, three vastly different OS scripts were engineered in pure Custom Roman Urdu Assembly:

1. **`calculator.txt`**: A massive 4-Op Mathematical engine that fetches string inputs via MMIO hardware tokens, cascades through conditional branch comparisons to isolate the `+ - * /` operators, evaluates ALU bounds, and fires the result sequentially onto a Graphics Card pixel array.
2. **`hello.txt`**: A raw memory iteration proof-of-concept that demonstrates memory pointers by loading a string array natively constructed in the RAM `.MAWAAD` segment (Address `0x0800`) and loops through it until it hits an explicit `0x00` Null Terminator block.
3. **`auth.txt`**: A live Authentication Firewall. It defines a password stored securely in `.MAWAAD` RAM space and waits for user keyboard strokes. Using nested loops and conditional jumps (`MUWAZANA` + `AGAR_SIFAR`), it simultaneously walks backward and forwards in memory space to intercept mismatches during a physical typing buffer, eventually branching out to highly optimized "SUCCESS" or "FAIL" string print matrices.

---

## 6. Estimated Difficulty and Skill Rating
**Difficulty Scope: Very High / Architect Level**

To recreate this assignment from scratch requires total mastery over:
1. **Low-Level Bitwise Mathematics**: Shifting operations `(instruction >> 8) & 0xFF` and bit-mask engineering. 
2. **Computer Organization & Architecture (COA)**: Strong grasp over CPU datapath routing, Control Signals, fetch-decode-execute lifecycles, and MMIO Bus emulation.
3. **Theory of Computation / Compilers**: Developing lexical analysis, 2-Pass pointer alignment generation, and tokenizers mapping semantic languages to generic machine encodings.
4. **C++ OOP & Memory Mechanics**: The extensive use of pointers, aggregation, composition, dynamic struct routing, and decoupled header designs.

```


## Assistant

<thinking>
Now I have a complete picture of everything. Let me write the full hardware specification manual. I need to continue from where I left off in my previous response (which was cut off mid-sentence at section 8.1 L1 Block Cache).

Let me write the full document now. I'll start from the beginning to give the user a complete, coherent document they can use directly. The document should:

1. Read like an authentic recovered hardware manual
2. Use ZERO OOP terminology (no class, private, public, encapsulation, inheritance, etc.)
3. Be numerically precise (correct sizes, opcodes, addresses)
4. Force exactly ONE correct design through physical constraints


5. Cover every component with sufficient detail to implement

I'm going to write this as a clean, formatted response with all the major sections: system architecture, storage bank, arithmetic core, buses, memory module, address mapping, peripherals, processor details, mainboard, assembly instructions, and the instruction set appendix.

Now I'm thinking through the pedagogical constraints that should be embedded in the hardware design—treating storage as sealed cells with accessors, buses as permanent pathways, components as slotted and removable units, and ensuring the CPU depends on the mainboard without owning it, while the ALU references the flags latch directly and the mainboard handles MMIO routing.

For the assignment to have one correct answer, I need to enforce that buses only exist within the Motherboard, the CPU can't own the Motherboard, components communicate exclusively through signal interfaces, MMIO routing happens in the Mainboard as the address decoder, and instruction decoding belongs in the Control Unit as a sub-component rather than in the CPU itself.

Now I'm framing this as a recovered engineering specification document using physical and electrical metaphors throughout, with precise constraints, tables, and ASCII diagrams that eliminate ambiguity and force a single correct implementation without relying on OOP terminology. it as "The Onyx-16 Technical Reference Manual" recovered by Lazarus Machinae

Let me write this now. It will be quite long. I'll organize it into clearly numbered chapters.

Key insight: The document should be written as if it's a real hardware manual from the 1980s/1990s, like the Intel 8086 datasheet but for a fictional processor. This means:
- Formal, terse writing style
- Specific voltage/signal references as metaphors for code behavior
- Tables for everything
- No hand-holding, but complete information

Here's my plan for what each section needs to accomplish in terms of the OOP "trap":

**Chapter 2 (Storage Bank)** → Forces RegisterBank class with private state + public accessors
- Key sentence: "sealed storage cells...only READ/WRITE signal lines are exposed externally"
- This means students MUST write private variables with public getters/setters

**Chapter 3 (ALU)** → Forces ALU class that takes flags by reference
- Key sentence: "the FLAGS latch connection is passed to the AEC at invocation time; the AEC mutates it internally and returns only the numeric result"
- Students must implement a method where flags are modified in place during execution

**Chapter 4 (Buses)** → Forces Composition (buses in motherboard)
- Key sentence: "etched into the mainboard substrate...physically destroyed along with the mainboard...cannot be manufactured independently"
- Students cannot create standalone Bus objects that exist outside Motherboard

**Chapter 8 (Processor)** → Forces CPU to hold Motherboard pointer (Aggregation)
- Key sentence: "the processor holds a connector port for the mainboard...the mainboard continues to exist independently"
- Students must understand the asymmetry: CPU depends on Motherboard, but Motherboard doesn't depend on CPU

**Chapter 9 (Motherboard)** → Forces Motherboard to own buses + MMIO routing
- Key sentence: "the mainboard's address decoder intercepts all bus transactions...routes peripheral addresses to the appropriate I/O panel"
- Students must put routing logic in Motherboard, not in CPU

**Chapter 10 (Assembly)** → Forces correct instantiation order + dependency injection
- Shows the PCBox/main.cpp assembly sequence that demonstrates why composition/aggregation matter

Now I'm planning the actual writing structure and tone.

Generating technical manual... I need to finalize the terminology mapping so each hardware component has a clear one-to-one relationship with its software counterpart, then write out the complete spec document with thorough detail on each section, starting with the L1 cache specifications. Tracks a base address (which 16-byte aligned block it currently holds)
- isValid flag
- Hit detection: address is within [baseAddress, baseAddress + 16)
- Miss: triggers mainboard bus transaction to fetch the block
- loadBlock: fills the 16-byte cache from a data source

For the Control Unit:
- Microcode ROM: array of 256 entries (one per opcode value)
- Each entry is a "signal vector" with multiple boolean/enum fields
- At decode time: opcode is extracted from bits [15:8] of the instruction word
- The signal vector for that opcode dictates what the execution datapath does
- This eliminates giant switch-case trees (cleaner design)

The Fetch-Decode-Execute cycle reads a 2-byte instruction from the PC into the IR, then increments PC by 2. During decode, I extract the opcode and look up its signal vector in the microcode ROM, which controls how operands route through the ALU, memory, or branch logic during execution. Results write back to the destination register based on what the signal vector specifies. For 2-word instructions, the control unit issues two additional bus reads to fetch a 16-bit immediate value while advancing the PC another 2 bytes. Finally, the mainboard assembly creates all components, connects the GPU to the monitor, plugs the CPU into the motherboard (which then wires up the buses), adds RAM and PSU, and continues with the remaining connections.

Now I'm planning out the document structure with chapters covering system architecture, storage, the execution core, system pathways, memory, address mapping, and peripheral units like the keyboard and graphics adapter.
</thinking>

Now I have a complete picture of every component, every signal path, every opcode, and every behavioral contract. Here is the full draft of the specification document, written as an authentic recovered hardware manual with zero OOP jargon but with every constraint engineered to force exactly one correct design.

---

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

| Pathway             | Width          | Function                                                                  |
| ------------------- | -------------- | ------------------------------------------------------------------------- |
| **Address Pathway** | 16-bit         | Carries the target memory address for the pending transaction             |
| **Data Pathway**    | 8-bit          | Carries the data byte being read from or written to memory                |
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

| Property                | Value                           |
| ----------------------- | ------------------------------- |
| **Total Capacity**      | 3,840 bytes                     |
| **Valid Address Range** | `0x0000` – `0x0EFF` (inclusive) |
| **Cell Width**          | 8 bits (byte-addressed)         |
| **Power-On State**      | All cells initialized to `0x00` |

**Out-of-Bounds Access:** Any read or write targeting an address of `0x0F00` or higher constitutes a **Segmentation Fault**. On an invalid read, the Data Pathway floats to `0xFF`. On an invalid write, the data is discarded. In both cases, a hardware fault diagnostic message is emitted.

The Memory Module does not implement the MMIO address intercept. It only ever sees addresses it is legally authorized to service. The routing decision — whether a given address reaches the Memory Module or not — is made exclusively by the mainboard's address decoder (see Chapter 6).

---

## CHAPTER 6: THE ADDRESS MAP AND MMIO DECODER

The mainboard contains a **hardware address decoder** that inspects every bus transaction before forwarding it. The complete physical address map of the ONYX-16 is as follows:

| Address Range       | Size        | Region                      | Routed To                            |
| ------------------- | ----------- | --------------------------- | ------------------------------------ |
| `0x0000` – `0x07FF` | 2,048 bytes | **Code Segment**            | Memory Module                        |
| `0x0800` – `0x0EFF` | 1,792 bytes | **Data Segment**            | Memory Module                        |
| `0x0F00` – `0x0FEF` | —           | **Fault Zone**              | Segmentation Fault — no valid device |
| `0x0FF0`            | 1 byte      | **Keyboard Character Port** | I/O Panel — READ only                |
| `0x0FF1`            | 1 byte      | **Display Character Port**  | Graphics Adapter — WRITE only        |
| `0x0FF2`            | 1 byte      | **Display Integer Port**    | Graphics Adapter — WRITE only        |
| `0x0FF3`            | 1 byte      | **Keyboard Integer Port**   | I/O Panel — READ only                |

### 6.1 MMIO Interception Rule

When the address decoder detects a transaction targeting addresses `0x0FF0` through `0x0FF3`, **it intercepts the transaction before it reaches the Memory Module.** The Memory Module never sees these addresses. The mainboard redirects the transaction directly to the appropriate peripheral hardware.

This interception is performed inside the mainboard itself. No external circuit, no Processor logic, and no Memory Module logic participates in this decision. The mainboard is the sole authority.

### 6.2 Peripheral Port Contracts

| Port     | Direction | Contract                                                                                                                                                                                                                                                   |
| -------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0x0FF0` | READ      | Returns the ASCII byte value of the next character in the keyboard input buffer. If the buffer is empty, the mainboard suspends the clock and waits for the user to provide input before completing the transaction.                                       |
| `0x0FF1` | WRITE     | The written byte is treated as an ASCII character code and forwarded directly to the display for rendering.                                                                                                                                                |
| `0x0FF2` | WRITE     | The written byte is treated as an unsigned 8-bit integer. The mainboard converts it to its decimal digit string and writes each ASCII character to the display sequentially. Example: writing `0x2A` (decimal 42) renders the characters `'4'` then `'2'`. |
| `0x0FF3` | READ      | Reads and parses a complete decimal integer token from the keyboard buffer. Returns the parsed value as an unsigned 8-bit result. If the buffer is empty, the mainboard suspends the clock and waits for input.                                            |

---

## CHAPTER 7: THE PERIPHERAL UNITS

### 7.1 The I/O Panel (Keyboard)

The keyboard is a separate physical chassis component. It maintains an internal **FIFO input buffer**. When polled and the buffer is empty, the keyboard unit emits a `[Hardware Interrupt]` diagnostic and blocks until the user types a line of text, which it then enqueues into the buffer character by character, followed by a space delimiter.

**Electrical interface exposed to the mainboard:**

| Signal          | Direction              | Behavior                                                                                                                                                                  |
| --------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PENDING_INPUT` | Output pin             | Driven HIGH when the buffer contains at least one non-whitespace character. The mainboard reads this pin before deciding whether to suspend execution.                    |
| `READ_CHAR`     | Triggered by mainboard | Pops and returns the next non-whitespace byte from the buffer as an 8-bit ASCII value.                                                                                    |
| `READ_INT`      | Triggered by mainboard | Parses and consumes the next complete decimal integer token from the buffer. Returns an 8-bit unsigned value. Leading and trailing whitespace is discarded automatically. |
|                 |                        |                                                                                                                                                                           |

### 7.2 The Graphics Adapter

The Graphics Adapter is a separate physical card that plugs into the mainboard's expansion slot. It receives raw byte payloads from the mainboard's MMIO interceptor and translates them for the connected display.

The Graphics Adapter requires a **Display Unit to be physically connected to its output port.** If no display is connected, all received payloads are silently discarded.

**Electrical interface exposed to the mainboard:**

| Signal         | Triggered By      | Behavior                                                                                                   |
| -------------- | ----------------- | ---------------------------------------------------------------------------------------------------------- |
| `CHAR_PAYLOAD` | Write to `0x0FF1` | Forwards the received byte directly to the display as a single ASCII character.                            |
| `INT_PAYLOAD`  | Write to `0x0FF2` | Converts the received byte to a decimal digit string and sends each character to the display sequentially. |

### 7.3 The Phosphor Display

The Phosphor Display is a **32-column × 16-row** CRT screen. It maintains an internal string buffer. Characters accumulate in the buffer as they arrive from the Graphics Adapter during program execution.

The buffer is **not flushed to the screen automatically** during execution. The display renders its entire buffer exactly once — at the explicit conclusion of program execution — inside a bordered phosphor-green terminal frame. Lines longer than 32 characters wrap to the next row. Rows beyond 16 are clipped.

---

## CHAPTER 8: THE PROCESSOR

The Processor is a single-chip unit. It contains four internal sub-units:

| Internal Sub-Unit             | Role                                                                 |
| ----------------------------- | -------------------------------------------------------------------- |
| **Storage Bank**              | Holds all registers (Chapter 2)                                      |
| **Arithmetic Execution Core** | Performs all computation (Chapter 3)                                 |
| **Block Cache**               | 16-byte high-speed prefetch buffer (Section 8.1)                     |
| **Instruction Decode Matrix** | Decodes instructions and drives the execution datapath (Section 8.2) |

### 8.1 Physical Bus Dependency

The Processor has **three physical connector ports** on its underside that mate with the three system pathways on the mainboard. **These ports carry no voltage until the Processor is physically seated in a mainboard socket.** Without a connected mainboard:

- The Processor cannot read from or write to memory.
- The Processor cannot receive input or produce output.
- The Processor cannot execute any instruction.

When the Processor is seated, the mainboard drives the Address, Data, and Control pathway pins into the Processor's connector ports. The Processor then holds a live reference to all three pathways for the duration of its installation. **The Processor does not own these pathways** — they belong to the mainboard and continue to exist if the Processor is removed.

### 8.2 The Block Cache

Embedded in the Processor die is a **16-byte block cache**. It mirrors a single contiguous 16-byte block from main memory to reduce repeated bus transactions during instruction fetching.

| Property                  | Value                                                                 |
| ------------------------- | --------------------------------------------------------------------- |
| **Block size**            | 16 bytes                                                              |
| **Number of blocks**      | 1 (single-block, direct-mapped)                                       |
| **Base address register** | Records the starting address of the block currently loaded            |
| **Valid bit**             | A single flag indicating whether the cache currently holds valid data |

**Cache hit:** A requested byte address falls within `[base, base + 16)` **and** the valid bit is set. The byte is returned directly from the cache without a bus transaction.

**Cache miss:** Either the valid bit is not set, or the requested address falls outside the cached block. The Processor issues a bus read transaction to the mainboard, retrieves the byte, and the cache is updated with a fresh 16-byte block starting at the aligned boundary.

**Cache invalidation:** Any write transaction to an address within the currently cached block immediately clears the valid bit.

### 8.3 The Instruction Decode Matrix

The Instruction Decode Matrix is a fixed 256-entry lookup table burned into the Processor at manufacture time. It is indexed by the 8-bit **opcode** field of an instruction. Each entry in the table is a **signal vector** — a collection of boolean and selector flags that dictates exactly how the execution datapath should behave for that instruction.

The signal vector for any given opcode specifies:

| Signal               | Type | Meaning                                                                                       |
| -------------------- | ---- | --------------------------------------------------------------------------------------------- |
| `IS_VALID`           | bool | Whether this opcode is recognized. Invalid opcodes emit a hardware fault and abort the cycle. |
| `USES_AEC`           | bool | Whether the Arithmetic Execution Core should be invoked.                                      |
| `AEC_OPERATION`      | enum | Which operation the AEC should perform (ADD, SUB, MUL, etc.).                                 |
| `IS_MEMORY_READ`     | bool | Whether the cycle should read a byte from memory via the bus.                                 |
| `IS_MEMORY_WRITE`    | bool | Whether the cycle should write a byte to memory via the bus.                                  |
| `IS_BRANCH`          | bool | Whether the PC should be conditionally or unconditionally redirected.                         |
| `BRANCH_ON_ZERO`     | bool | If branching, only branch when ZF is set.                                                     |
| `BRANCH_ON_NOT_ZERO` | bool | If branching, only branch when ZF is clear.                                                   |
| `WRITES_TO_REGISTER` | bool | Whether the result of this cycle should be written back to the destination register.          |
| `IS_4BIT_IMMEDIATE`  | bool | Whether the operand is a 4-bit immediate packed into the instruction word (Format B).         |
| `IS_16BIT_IMMEDIATE` | bool | Whether the operand is a 16-bit immediate requiring a second word fetch (Format D).           |

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

| Socket                  | Accepts           | Notes                                                                                                                              |
| ----------------------- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **CPU Socket**          | Processor         | Upon insertion, the mainboard immediately drives the Address, Data, and Control pathway pins into the Processor's connector ports. |
| **RAM Slot**            | Memory Module     | The Memory Module receives all standard address-range transactions.                                                                |
| **Expansion Slot**      | Graphics Adapter  | Receives MMIO write payloads from the address decoder.                                                                             |
| **ATX Power Connector** | Power Supply Unit | Without a connected PSU, the system has no power and all clock pulses are suppressed.                                              |
| **I/O Panel Connector** | Keyboard          | Polled by the address decoder on MMIO read transactions.                                                                           |

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

| Opcode | Urdu Mnemonic  | English Mnemonic | Format | Operation Description                                                                                                                                             |
| ------ | -------------- | ---------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0x00` | `AARAM`        | `NOP`            | A      | No operation. A full instruction word of `0x0000` also signals end-of-program to the bootloader.                                                                  |
| `0x01` | `JAMA`         | `ADD`            | A      | `R[dest] = R[dest] + R[src]`. Updates ZF.                                                                                                                         |
| `0x02` | `TAFREEK`      | `SUB`            | A      | `R[dest] = R[dest] - R[src]`. Updates ZF.                                                                                                                         |
| `0x03` | `ZARAB`        | `MUL`            | A      | `R[dest] = R[dest] * R[src]`. Updates ZF.                                                                                                                         |
| `0x04` | `TAQSEEM`      | `DIV`            | A      | `R[dest] = R[dest] / R[src]`. Updates ZF. Result is `0` if `R[src]` is zero.                                                                                      |
| `0x0A` | `MUWAZANA`     | `CMP`            | A      | Compare `R[dest]` against `R[src]`. No register writeback. Updates ZF, NF, and PF.                                                                                |
| `0x10` | `CHHALANG`     | `JMP`            | A      | `PC = R[src]`. Unconditional jump. The dest nibble is unused (set to 0).                                                                                          |
| `0x11` | `AGAR_SIFAR`   | `JZ`             | A      | If `ZF = 1`: `PC = R[src]`. Jump if the last comparison was equal. The dest nibble is unused.                                                                     |
| `0x12` | `AGAR_MAUJOOD` | `JNZ`            | A      | If `ZF = 0`: `PC = R[src]`. Jump if the last comparison was *not* equal. The dest nibble is unused.                                                               |
| `0x1A` | `BHARO`        | `LDR_IMM`        | B      | `R[dest] = imm4`. Loads a 4-bit immediate value (range `0x0` to `0xF`). Single-word instruction.                                                                  |
| `0x1B` | `BHARO`        | `LDR_IMM`        | D      | `R[dest] = imm16`. Loads a full 16-bit immediate value. Two-word instruction (see Appendix B). Used for all values above `0x000F` and for all label addresses.    |
| `0x20` | `PARHO`        | `LDR`            | A      | `R[dest] = Memory[R[src]]`. Loads one byte from the address held in `R[src]` into `R[dest]`.                                                                      |
| `0x21` | `RAKHO`        | `STR`            | A      | `Memory[R[src]] = R[dest]`. Writes the value in `R[dest]` to the address held in `R[src]`. The dest nibble carries the value; the src nibble carries the pointer. |

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

| Section Directive | Urdu       | English | Purpose                                                     |
| ----------------- | ---------- | ------- | ----------------------------------------------------------- |
| Data section      | `.MAWAAD`  | `.DATA` | Static string and integer data loaded into RAM at `0x0800`. |
| Code section      | `.HIDAYAT` | `.CODE` | Executable instructions loaded into RAM at `0x0000`.        |

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

| Fault Message                                              | Trigger Condition                                       | Effect                                                          |
| ---------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------------- |
| `[HARDWARE FAULT] Segmentation Fault: Read out of bounds`  | Memory Module receives a read to address ≥ `0x0F00`     | Returns `0xFF`; execution continues                             |
| `[HARDWARE FAULT] Segmentation Fault: Write out of bounds` | Memory Module receives a write to address ≥ `0x0F00`    | Write discarded; execution continues                            |
| `[MOTHERBOARD FAULT] Invalid Read Address`                 | Address decoder receives a read to an unmapped address  | `0x00` placed on Data Pathway; execution continues              |
| `[MOTHERBOARD FAULT] Invalid Write Address`                | Address decoder receives a write to an unmapped address | Write discarded; execution continues                            |
| `[HARDWARE FAULT] Invalid Instruction`                     | Decode Matrix lookup returns `IS_VALID = false`         | Cycle aborted; execution continues at next PC                   |
| `[CRITICAL WARNING] Power Draw exceeded PSU Capacity`      | Polled wattage exceeds PSU rated capacity               | PSU calls `killPower()` on the Mainboard — **permanent halt**   |
| `[CRITICAL ERROR] Thermal threshold exceeded`              | Processor temperature exceeds `90.0°C`                  | Sets HF bit in FLAGS — **permanent halt**                       |
| `[Hardware Interrupt] Awaiting Keyboard Input`             | MMIO read to `0x0FF0` or `0x0FF3` with empty buffer     | Clock suspended until user types; execution resumes after input |

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

