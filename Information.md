## Opcodes, Operands, and Descriptions:
- Hex 0x00 Decimal 0 HLT: Halts the program.
- Hex 0x01 Decimal 1 PUA operand: Sets the A Register to the operand.
- Hex 0x02 Decimal 2 PUB operand: Sets the B Register to the operand.
- Hex 0x03 Decimal 3 PUC operand: Sets the C Register to the operand.
- Hex 0x04 Decimal 4 PUM operand: Sets the M Register to the operand.
- Hex 0x05 Decimal 5 INA: Increments the A Register by 1.
- Hex 0x06 Decimal 6 INB: Increments the B Register by 1.
- Hex 0x07 Decimal 7 INC: Increments the C Register by 1.
- Hex 0x08 Decimal 8 DEA: Decrements the A Register by 1.
- Hex 0x09 Decimal 9 DEB: Decrements the B Register by 1.
- Hex 0x0A Decimal 10 DEC: Decrements the C Register by 1.
- Hex 0x0B Decimal 11 JMP operand: Sets the program counter to the operand, appends the operand to the stack, and increments the stack pointer by 1.
- Hex 0x0C Decimal 12 ADD operand operand: Adds operands together and stores the result in the N Register.
- Hex 0x0D Decimal 13 SUB operand operand: Subtracts operands and stores the result in the N Register.
- Hex 0x0E Decimal 14 MUL operand operand: Multiplies operands together and stores the result in the N Register.
- Hex 0x0F Decimal 15 DIV operand operand: Divides operands and stores the result in the N Register.
- Hex 0x10 Decimal 16 JCZ operand: Checks if the Z Register is equal to 1. If so, sets the program counter to the operand, appends the operand to the stack, and increments the stack pointer by 1.
- Hex 0x11 Decimal 17 JCN operand: Checks if the Z Register is equal to 0. If so, sets the program counter to the operand, appends the operand to the stack, and increments the stack pointer by 1.
- Hex 0x12 Decimal 18 CMB operand: Checks if the A Register is equal to the operand. If so, sets the Z Register to 1.
- Hex 0x13 Decimal 19 MEM operand1 operand2: Computes operand1 modulo 256 and stores the result at the memory location given by operand2 in the array specified by the M register (0 = general memory, 1 = program memory, 2 = permanent memory).
- Hex 0x14 Decimal 20 RTS: Sets the program counter to the top element of the stack, deletes the top element of the stack, and decrements the stack pointer by 1.
- Hex 0x15 Decimal 21 PUSH operand: Appends the operand to the stack, and increments the stack pointer by 1.
- Hex 0x16 Decimal 22 POP operand: If the operand is not ##xxx, #xxxxx, or $xxxxx, sets the register specified by the operand to the top element of the stack, removes element, and decrements the stack pointer.
- Hex 0x17 Decimal 23 SNA: Set the A Register to the N Register.
- Hex 0x18 Decimal 24 DES: Set the Z Register to 0.
- Hex 0x19 Decimal 25 AND operand1 operand2: Sets the register of choice determined by operand1 to itself logical and operand2.
- Hex 0x20 Decimal 26 OR operand1 operand2: Sets the register of choice determined by operand1 to itself logical or operand2.
- Hex 0x21 Decimal 27 NOT operand: Sets the register of choice determined by operand1 to logical not itself.
- Hex 0x22 Decimal 28 XOR operand1 operand2: Sets the register of choice determined by operand1 to itself logical xor operand2.
- Hex 0x23 Decimal 29 SHR operand: Shifts right the register of choice determined by operand1 by one bit.
- Hex 0x24 Decimal 30 SHL operand: Shifts left the register of choice determined by operand1 by one bit.
- Hex 0x25 Decimal 31 NOP: Does nothing.

## The Syntax of Instructions.

Opcode Operand Operand

##xxx is for immediate 8 bit values.

#xxxxx is for immediate 16 bit values.

$xxxxx is for immediate 16 bit memory requests.

A, B, and C are for accessing registers.

**Note**: The MEM instruction should only be written as `MEM <operand1> #xxxxx` for a fixed memory address.

## Registers, and Memory Arrays.

There are three general purpose registers, A, B, and C.

There are also three memory arrays: General memory, program memory and permanent memory.

**Note**: Permanent memory sticks around even if the emulator has been shut down.

How Instruction Bytecode is Structured.

Every instruction in bytecode is always going to be seven bytes long, no matter the instruction. And those 7 bytes are structured like:

- Byte 1: Opcode
- Byte 2: Operand1 type (## is 0, $ is 1, # is 2, A is 3, B is 4, C is 5, M is 6)
- Byte 3: Operand2 type
- Byte 4: Operand1 byte 1
- Byte 5: Operand1 byte 2
- Byte 6: Operand2 byte 1
- Byte 7: Operand2 byte 2
