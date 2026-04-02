#include <EEPROM.h>
#include <SD.h>

int A = 0;
int B = 0;
int C = 0;
int M = 0;
int N = 0;
int Z = 0;
uint16_t PC = 0;
unsigned char MEM[65536] = {0};
unsigned char PERM_MEM[65536] = {0};
unsigned char PROG_MEM[65536] = {0};
int STACK[255] = {0};
int sp = 0;
int RUNNING = 1;
int main_byte = 0;
int b0 = 0;
int b1 = 0;
int b2 = 0;
int b3 = 0;
int b4 = 0;
int b5 = 0;

void pua(int val_in) {
  A = val_in;
}

void pub(int val_in) {
  B = val_in;
}

void puc(int val_in) {
  C = val_in;
}

void pum(int val_in) {
  M = val_in;
}

void ina() {
    A += 1;
}
void inb() {
    B += 1;
}
void inc() {
    C += 1;
}
void dea() {
    A -= 1;
}
void deb() {
    B -= 1;
}
void dec() {
    C -= 1;
}

int stack_size() {
  for (int i = 0; i < 255; i++) {
    if (STACK[i] == 0) {
      return i;
    }
  }
  return 255;
}

void stack_append(int val) {
    if (sp < 255) {
        STACK[sp++] = val;
    } else {
        Serial.println("STACK OVERFLOW");
        while (1==1) {}
    }
}

void jmp(int val) {
    stack_append(val);
    PC = val;
}

int parse_operand(int type, int operand, int operandb2) {
    int ex = 0;
    ex = (operand << 8) | operandb2;
    switch (type) {
      case 0:
          return operand;
      case 1:
          if (M == 0) {
              return MEM[ex];
          } else if (M == 1) {
            return PERM_MEM[ex];
          }
      case 2:
          return ex;
      case 3:
          return A;
      case 4:
          return B;
      case 5:
          return C;
      case 6:
          return M;
    }

    Serial.print("Invalid operand: ");
    Serial.println(operand);
    while (1==1) {}
}

void add(int valA, int valB) {
    N = valA + valB;
}
void sub(int valA, int valB) {
    N = valA - valB;
}
void DIV(int valA, int valB) {
    if (valB == 0) {
      Serial.print("DIVISION BY ZERO AT LINE ");
      Serial.println(PC);
    }
    N = valA / valB;
}
void mul(int valA, int valB) {
    N = valA * valB;
}
void cmb(int val) {
    if (val == A) {
        Z = 1;
    } else {
        Z = 0;
    }
}
void mem(uint8_t valA, uint16_t valB) {
    valA = valA % 256;
    switch (M) {
      case 0:
        MEM[valB] = valA;
      case 1:
        PERM_MEM[valB] = valA;
        savePERMEM(valB, valA);
      case 2:
        PROG_MEM[valB] = valA;
        savePROGMEM(valB, valA);
    }
}
int stack_pop() {
    if (sp > 0) {
        return STACK[--sp];
    } else {
        Serial.println("STACK UNDERFLOW");
        while (1==1) {}
    }
}
void rts() {
    PC = stack_pop();
}
void sna() {
    A = N;
}
void des() {
    Z = 0;
}
void and_op(int val1, int val2) {
    switch (val1) {
      case 3:
          A = A & val2;
          return;
      case 4:
          B = B & val2;
          return;
      case 5:
          C = C & val2;
          return;
    }
}
void or_op(int val1, int val2) {
    switch (val1) {
      case 3:
          A = A | val2;
          return;
      case 4:
          B = B | val2;
          return;
      case 5:
          C = C | val2;
          return;
    }
}
void not_op(int val1) {
    switch (val1) {
      case 3:
          A = ~A;
          return;
      case 4:
          B = ~B;
          return;
      case 5:
          C = ~C;
          return;
    }
}
void xor_op(int val1, int val2) {
    switch (val1) {
      case 3:
          A = A ^ val2;
          return;
      case 4:
          B = B ^ val2;
          return;
      case 5:
          C = C ^ val2;
          return;
    }
}
void shr(int val) {
  switch (val) {
    case 3:
        A = A >> 1;
        return;
    case 4:
        B = B >> 1;
        return;
    case 5:
        C = C >> 1;
        return;
  }
}
void shl(int val) {
  switch (val) {
    case 3:
        A = A << 1;
        return;
    case 4:
        B = B << 1;
        return;
    case 5:
        C = C << 1;
        return;
  }
}

void PoP(char inp) {
    if (inp == ' ') {
        return;
    } else if (inp == 'A') {
        A = STACK[stack_size() - 1];
    } else if (inp == 'B') {
        B = STACK[stack_size() - 1];
    } else if (inp == 'C') {
        C = STACK[stack_size() - 1];
    }
}


void printState() {
    Serial.print("A: ");
    Serial.print(A);
    Serial.print(", B: ");
    Serial.print(B);
    Serial.print(", C: ");
    Serial.print(C);
    Serial.print(", M: ");
    Serial.print(M);
    Serial.print(", N: ");
    Serial.print(N);
    Serial.print(", Z: ");
    Serial.print(Z);
    Serial.print(", PC: ");
    Serial.print(PC / 7);
    Serial.print("/");
    Serial.println(PC);
}

void execute() {
    while (1==1) {
        //printState();
        b0 = PROG_MEM[PC + 1];
        b1 = PROG_MEM[PC + 2];
        b2 = PROG_MEM[PC + 3];
        b3 = PROG_MEM[PC + 4];
        b4 = PROG_MEM[PC + 5];
        b5 = PROG_MEM[PC + 6];
        main_byte = PROG_MEM[PC];
        switch (main_byte) {
            case 0:
                return;
            case 1:
                if (b0 == 1 or b0 == 2) {
                    pua(parse_operand(b0, b1, b2));
                } else {
                    pua(parse_operand(b0, b1, 0));
                }
                PC += 7;
                break;
            case 2:
                if (b0 == 1 or b0 == 2) {
                    pub(parse_operand(b0, b1, b2));
                } else {
                    pub(parse_operand(b0, b1, 0));
                }
                PC += 7;
                break;
            case 3:
                if (b0 == 1 or b0 == 2) {
                    puc(parse_operand(b0, b1, b2));
                } else {
                    puc(parse_operand(b0, b1, 0));
                }
                PC += 7;
                break;
            case 4:
                if (b0 == 1 or b0 == 2) {
                    pum(parse_operand(b0, b1, b2));
                } else {
                    pum(parse_operand(b0, b1, 0));
                }
                PC += 7;
                break;
            case 5:
                ina();
                PC += 7;
                break;
            case 6:
                inb();
                PC += 7;
                break;
            case 7:
                inc();
                PC += 7;
                break;
            case 8:
                dea();
                PC += 7;
                break;
            case 9:
                deb();
                PC += 7;
                break;
            case 10:
                dec();
                PC += 7;
                break;
            case 11:
                jmp(parse_operand(b0, b1, b2));
                break;
            case 12:
                if ((b0 == 1 or b0 == 2) && (b1 != 1 or b1 != 2)) {
                    add(parse_operand(b0, b2, b3), parse_operand(b1, b4, 0));
                } else if ((b0 != 1 or b0 != 2) && (b1 == 1 or b1 == 2)) {
                    add(parse_operand(b0, b2, 0), parse_operand(b1, b3, b4));
                } else if ((b0 == 1 or b0 == 2) && (b1 == 1 or b1 == 2)) {
                    add(parse_operand(b0, b2, b3), parse_operand(b1, b4, b5));
                } else {
                    add(parse_operand(b0, b2, 0), parse_operand(b1, b3, 0));
                }
                PC += 7;
                break;
            case 13:
                if ((b0 == 1 or b0 == 2) && (b1 != 1 or b1 != 2)) {
                    sub(parse_operand(b0, b2, b3), parse_operand(b1, b4, 0));
                } else if ((b0 != 1 or b0 != 2) && (b1 == 1 or b1 == 2)) {
                    sub(parse_operand(b0, b2, 0), parse_operand(b1, b3, b4));
                } else if ((b0 == 1 or b0 == 2) && (b1 == 1 or b1 == 2)) {
                    sub(parse_operand(b0, b2, b3), parse_operand(b1, b4, b5));
                } else {
                    sub(parse_operand(b0, b2, 0), parse_operand(b1, b3, 0));
                }
                PC += 7;
                break;
            case 14:
                if ((b0 == 1 or b0 == 2) && (b1 != 1 or b1 != 2)) {
                    mul(parse_operand(b0, b2, b3), parse_operand(b1, b4, 0));
                } else if ((b0 != 1 or b0 != 2) && (b1 == 1 or b1 == 2)) {
                    mul(parse_operand(b0, b2, 0), parse_operand(b1, b3, b4));
                } else if ((b0 == 1 or b0 == 2) && (b1 == 1 or b1 == 2)) {
                    mul(parse_operand(b0, b2, b3), parse_operand(b1, b4, b5));
                } else {
                    mul(parse_operand(b0, b2, 0), parse_operand(b1, b3, 0));
                }
                PC += 7;
                break;
            case 15:
                if ((b0 == 1 or b0 == 2) && (b1 != 1 or b1 != 2)) {
                    DIV(parse_operand(b0, b2, b3), parse_operand(b1, b4, 0));
                } else if ((b0 != 1 or b0 != 2) && (b1 == 1 or b1 == 2)) {
                    DIV(parse_operand(b0, b2, 0), parse_operand(b1, b3, b4));
                } else if ((b0 == 1 or b0 == 2) && (b1 == 1 or b1 == 2)) {
                    DIV(parse_operand(b0, b2, b3), parse_operand(b1, b4, b5));
                } else {
                    DIV(parse_operand(b0, b2, 0), parse_operand(b1, b3, 0));
                }
                PC += 7;
                break;
            case 16:
                    if (Z == 1) {
                        PC = parse_operand(b0, b2, b3);
                        stack_append(parse_operand(b0, b2, b3));
                    } else {
                    PC += 7;
                    }
                    break;
            case 17:
                    if (Z != 1) {
                        PC = parse_operand(b0, b2, b3);
                        stack_append(parse_operand(b0, b2, b3));
                    } else {
                    PC += 7;
                    }
                    break;
            case 18:
                if (b0 == 1 or b0 == 2) {
                    cmb(parse_operand(b0, b1, b2));
                } else {
                    cmb(parse_operand(b0, b1, 0));
                }
                PC += 7;
                break;
            case 19:
                if ((b0 == 1 or b0 == 2) && (b1 != 1 or b1 != 2)) {
                    mem(parse_operand(b0, b2, b3), parse_operand(b1, b4, 0));
                } else if ((b0 != 1 or b0 != 2) && (b1 == 1 or b1 == 2)) {
                    mem(parse_operand(b0, b2, 0), parse_operand(b1, b3, b4));
                } else if ((b0 == 1 or b0 == 2) && (b1 == 1 or b1 == 2)) {
                    mem(parse_operand(b0, b2, b3), parse_operand(b1, b4, b5));
                } else {
                    mem(parse_operand(b0, b2, 0), parse_operand(b1, b3, 0));
                }
                PC+=7;
                break;
            case 20:
                rts();
                PC += 7;
                break;
            case 21:
                if (b0 == 1 or b0 == 2) {
                    stack_append(parse_operand(b0, b1, b2));
                } else {
                    stack_append(parse_operand(b0, b1, 0));
                }
                PC += 7;
                break;
            case 22:
                switch (b1) {
                    case 0:
                        PoP(' ');
                        break;
                    case 3:
                        PoP('A');
                        break;
                    case 4:
                        PoP('B');
                        break;
                    case 5:
                        PoP('C');
                        break;
                }
                PC += 7;
                break;
            case 23:
                sna();
                PC += 7;
                break;
            case 24:
                des();
                PC += 7;
                break;
            case 25:
                if (b0 != 1 or b0 != 2) {
                    and_op(b0, parse_operand(b1, b2, 0));
                } else {
                    and_op(b0, parse_operand(b1, b2, b3));
                }
                PC += 7;
                break;
            case 26:
                if (b0 != 1 or b0 != 2) {
                    or_op(b0, parse_operand(b1, b2, 0));
                } else {
                    or_op(b0, parse_operand(b1, b2, b3));
                }
                PC += 7;
                break;
            case 27:
                not_op(b0);
                PC += 7;
                break;
            case 28:
                if (b0 != 1 or b0 != 2) {
                    xor_op(b0, parse_operand(b1, b2, 0));
                } else {
                    xor_op(b0, parse_operand(b1, b2, b3));
                }
                PC += 7;
                break;
            case 29:
                shr(b0);
                PC += 7;
                break;
            case 30:
                shl(b0);
                PC += 7;
                break;
            case 31:
                PC += 7;
                break;
            default:
                Serial.print("INVALID INST AT ");
                Serial.println(PC);
                while (1==1) {}
        }
        A &= 0xFFFF;
        B &= 0xFFFF;
        C &= 0xFFFF;
    }
}

uint8_t inst[7] = {0};


void load_PROG_PERM() {
    File f1 = SD.open("PROGMEM.BIN", FILE_READ);
    File f2 = SD.open("PERMEM.BIN", FILE_READ);

    if (!f1 || !f2) {
        if (f1) f1.close();
        if (f2) f2.close();
        Serial.println("LOADING FAILED. PLEASE CHECK MICRO SD CARD");
        while (1) {}  // halt
    }

    // --- Load PROG_MEM ---
    size_t totalRead = 0;
    while (totalRead < sizeof(PROG_MEM)) {
        size_t r = f1.read(PROG_MEM + totalRead, sizeof(PROG_MEM) - totalRead);
        if (r == 0) {
            Serial.println("ERROR: Unexpected EOF while loading PROG_MEM");
            while (1) {}
        }
        totalRead += r;
    }

    // --- Load PERM_MEM ---
    totalRead = 0;
    while (totalRead < sizeof(PERM_MEM)) {
        size_t r = f2.read(PERM_MEM + totalRead, sizeof(PERM_MEM) - totalRead);
        if (r == 0) {
            Serial.println("ERROR: Unexpected EOF while loading PERM_MEM");
            while (1) {}
        }
        totalRead += r;
    }

    f1.close();
    f2.close();

    Serial.println("LOADING COMPLETE");
}

void savePROGMEM(uint16_t addr, uint8_t wchar) {
    File f = SD.open("PROGMEM.BIN", FILE_WRITE);
    if (!f) {Serial.printf("PROGMEM.BIN IS MISSING\n"); while (1==1) {}}
    f.seek(addr);
    f.write(wchar);
    f.close();
}

void savePERMEM(uint16_t addr, uint8_t wchar) {
    File f = SD.open("PERMEM.BIN", FILE_WRITE);
    if (!f) {Serial.printf("PERMEM.BIN IS MISSING\n"); while (1==1) {}}
    f.seek(addr);
    f.write(wchar);
    f.close();
}

void setup() {
  Serial.begin(9600);
  while (!Serial);
  if (!SD.begin(BUILTIN_SDCARD)) {
    Serial.println("SD init failed!");
    return;
  }
  load_PROG_PERM();
  Serial.println("Begining...");
  execute();
  Serial.println("Stopped");
}

void loop() {

}
