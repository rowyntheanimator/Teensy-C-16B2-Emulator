import sys

bytecode = ""
tbytecode = ""
def get_tokens(text: list) -> list:
    out = ""
    list_out = []
    for i in range(len(text)):
        if text[i] != " ":
            out += text[i]
        else:
            list_out.append(out)
            out = ""
    if out:
        list_out.append(out)
    return list_out

def get_lines(text: list) -> list:
    out = ""
    list_out = []
    for i in range(len(text)):
        if text[i] != "\n":
            out += text[i]
        else:
            list_out.append(out.strip())
            out = ""
    if out:
        list_out.append(out.strip())
    return list_out

def split_into_bytes(num):
    high_byte = (num >> 8) & 0xFF
    low_byte = num & 0xFF
    return high_byte, low_byte

def do_input_s1(token, line, inst):
    global bytecode

    if not token:
        print(f'AT LINE {line} THERE IS A EMPTY INPUT')

    if token[:2] == "##":
        bytecode += "00 "
        bytecode += str(hex(int(token[2:])))[2:] + " "
    elif token[0] == "#":
        bytecode += "02 "
        byte, byte2 = split_into_bytes(int(token[1:]))
        bytecode += str(hex(byte))[2:] + " "
        bytecode += str(hex(byte2))[2:] + " "
    elif token[0] == "$":
        bytecode += "01 "
        byte, byte2 = split_into_bytes(int(token[1:]))
        bytecode += str(hex(byte))[2:] + " "
        bytecode += str(hex(byte2))[2:] + " "
    elif token == "A":
        bytecode += "03 00 "
    elif token == "B":
        bytecode += "04 00 "
    elif token == "C":
        bytecode += "05 00 "
    elif token == "M":
        bytecode += "06 00 "
    else:
        print(f'AT LINE {line} THERE IS A INVALID INPUT TYPE {token}')



def do_input_s2(token, token2, line, inst):
    global bytecode
    tokenAL = ""
    tokenBL = ""
    if not token or not token2:
        print(f'AT LINE {line} THERE IS A EMPTY INPUT')
        return

    if token[:2] == "##":
        bytecode += "00 "
        tokenAL += str(hex(int(token[2:])))[2:] + " "
    elif token[0] == "#":
        bytecode += "02 "
        byte, byte2 = split_into_bytes(int(token[1:]))
        tokenAL += str(hex(byte))[2:] + " "
        tokenAL += str(hex(byte2))[2:] + " "
    elif token[0] == "$":
        bytecode += "01 "
        byte, byte2 = split_into_bytes(int(token[1:]))
        tokenAL += str(hex(byte))[2:] + " "
        tokenAL += str(hex(byte2))[2:] + " "
    elif token == "A":
        bytecode += "03 "
        tokenAL += "00 "
    elif token == "B":
        bytecode += "04 "
        tokenAL += "00 "
    elif token == "C":
        bytecode += "05 "
        tokenAL += "00 "
    elif token == "M":
        bytecode += "06 "
        tokenAL += "00 "
    else:
        print(f'AT LINE {line} THERE IS A INVALID INPUT TYPE {token}')
    
    if token2[:2] == "##":
        bytecode += "00 "
        tokenBL += str(hex(int(token2[2:])))[2:] + " "
    elif token2[:1] == "#":
        bytecode += "02 "
        byte, byte2 = split_into_bytes(int(token2[1:]))
        tokenBL += str(hex(byte))[2:] + " "
        tokenBL += str(hex(byte2))[2:] + " "
    elif token2[:1] == "$":
        bytecode += "01 "
        byte, byte2 = split_into_bytes(int(token2[1:]))
        tokenBL += str(hex(byte))[2:] + " "
        tokenBL += str(hex(byte2))[2:] + " "
    elif token2 == "A":
        bytecode += "03 "
        tokenBL += "00 "
    elif token2 == "B":
        bytecode += "04 "
        tokenBL += "00 "
    elif token2 == "C":
        bytecode += "05 "
        tokenBL += "00 "
    elif token2 == "M":
        bytecode += "06 "
        tokenBL += "00 "
    else:
        print(f'AT LINE {line} THERE IS A INVALID INPUT TYPE {token2}')
    bytecode += tokenAL
    bytecode += tokenBL

def asm(text):
    global bytecode, tbytecode
    lines = get_lines(text)
    print(lines)
    tokens = []
    for i in range(len(lines)):
        bytecode = ""
        tokens = get_tokens(lines[i])
        if len(tokens) > 0:
            if tokens[0] == "HLT":
                bytecode += "00 "
            elif tokens[0] == "PUA":
                bytecode += "01 "
                if len(tokens) == 2:
                    do_input_s1(tokens[1], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 1 INPUT')
                    return
            elif tokens[0] == "PUB":
                bytecode += "02 "
                if len(tokens) == 2:
                    do_input_s1(tokens[1], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 1 INPUT')
                    return
            elif tokens[0] == "PUC":
                bytecode += "03 "
                if len(tokens) == 2:
                    do_input_s1(tokens[1], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 1 INPUT')
                    return
            elif tokens[0] == "PUM":
                bytecode += "04 "
                if len(tokens) == 2:
                    do_input_s1(tokens[1], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 1 INPUT')
                    return
            elif tokens[0] == "INA":
                bytecode += "05 "
            elif tokens[0] == "INB":
                bytecode += "06 "
            elif tokens[0] == "INC":
                bytecode += "07 "
            elif tokens[0] == "DEA":
                bytecode += "08 "
            elif tokens[0] == "DEB":
                bytecode += "09 "
            elif tokens[0] == "DEC":
                bytecode += "0A "
            elif tokens[0] == "JMP":
                bytecode += "0B "
                if len(tokens) == 2:
                    do_input_s1(tokens[1], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 1 INPUT')
                    return
            elif tokens[0] == "ADD":
                bytecode += "0C "
                if len(tokens) == 3:
                    do_input_s2(tokens[1], tokens[2], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 2 INPUT')
                    return
            elif tokens[0] == "SUB":
                bytecode += "0D "
                if len(tokens) == 3:
                    do_input_s2(tokens[1], tokens[2], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 2 INPUT')
                    return
            elif tokens[0] == "MUL":
                bytecode += "0E "
                if len(tokens) == 3:
                    do_input_s2(tokens[1], tokens[2], i, tokens[0])
                    print(tokens[1], tokens[2], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 2 INPUT')
                    return
            elif tokens[0] == "DIV":
                bytecode += "0F "
                if len(tokens) == 3:
                    do_input_s2(tokens[1], tokens[2], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 2 INPUT')
                    return
            elif tokens[0] == "JCZ":
                bytecode += "10 "
                if len(tokens) == 2:
                    do_input_s1(tokens[1], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 1 INPUT')
                    return
            elif tokens[0] == "JCN":
                bytecode += "11 "
                if len(tokens) == 2:
                    do_input_s1(tokens[1], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 1 INPUT')
                    return
            elif tokens[0] == "CMB":
                bytecode += "12 "
                if len(tokens) == 2:
                    do_input_s1(tokens[1], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 1 INPUT')
                    return
            elif tokens[0] == "MEM":
                bytecode += "13 "
                if len(tokens) == 3:
                    do_input_s2(tokens[1], tokens[2], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 1 INPUT')
                    return
            elif tokens[0] == "RTS":
                bytecode += "14 "
            elif tokens[0] == "PUSH":
                bytecode += "15 "
                if len(tokens) == 2:
                    do_input_s1(tokens[1], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 1 INPUT')
                    return
            elif tokens[0] == "POP":
                bytecode += "16 "
                if len(tokens) == 2:
                    do_input_s1(tokens[1], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 1 INPUT')
                    return
            elif tokens[0] == "SNA":
                bytecode += "17 "
            elif tokens[0] == "DES":
                bytecode += "18 "
            elif tokens[0] == "AND":
                bytecode += "19 "
                if tokens[1] == "A":
                    bytecode+="03 "
                elif tokens[1] == "B":
                    bytecode+="04 "
                elif tokens[1] == "C":
                    bytecode+="05 "
                if len(tokens) == 3:
                    do_input_s1(tokens[2], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 2 INPUT')
                    return
            elif tokens[0] == "OR":
                bytecode += "19 "
                if tokens[1] == "A":
                    bytecode+="03 "
                elif tokens[1] == "B":
                    bytecode+="04 "
                elif tokens[1] == "C":
                    bytecode+="05 "
                if len(tokens) == 3:
                    do_input_s1(tokens[2], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 2 INPUT')
                    return
            elif tokens[0] == "NOT":
                bytecode += "19 "
                if tokens[1] == "A":
                    bytecode+="03 "
                elif tokens[1] == "B":
                    bytecode+="04 "
                elif tokens[1] == "C":
                    bytecode+="05 "
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 2 INPUT')
                    return
            elif tokens[0] == "XOR":
                bytecode += "1A "
                if tokens[1] == "A":
                    bytecode+="03 "
                elif tokens[1] == "B":
                    bytecode+="04 "
                elif tokens[1] == "C":
                    bytecode+="05 "
                if len(tokens) == 3:
                    do_input_s1(tokens[2], i, tokens[0])
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 2 INPUT')
                    return
            elif tokens[0] == "SHR":
                bytecode += "1B "
                if tokens[1] == "A":
                    bytecode+="03 "
                elif tokens[1] == "B":
                    bytecode+="04 "
                elif tokens[1] == "C":
                    bytecode+="05 "
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 2 INPUT')
                    return
            elif tokens[0] == "SHL":
                bytecode += "1C "
                if tokens[1] == "A":
                    bytecode+="03 "
                elif tokens[1] == "B":
                    bytecode+="04 "
                elif tokens[1] == "C":
                    bytecode+="05 "
                else:
                    print(f'AT LINE {i} {tokens[0]} EXPECTS 2 INPUT')
                    return
            elif tokens[0] == "NOP":
                bytecode += "1D "
            else:
                print(f'AT LINE {i} {tokens[0]} IS A INVALID INST')
                return
            padding_length = 7 - len(bytecode.split())
            bytecode += "00 " * padding_length
            tbytecode += bytecode
        else:
            continue


def insert_bytes_at_start(hex_string, filename="PROGMEM.bin", max_size=65536):
    new_bytes = bytes(int(b, 16) for b in hex_string.split())
    n = len(new_bytes)
    
    with open(filename, "rb") as f:
        content = f.read()
        
    if len(content) != max_size:
        raise ValueError(f"File size is {len(content)}, expected {max_size}")
    
    remaining = content[n:]
    new_content = new_bytes + remaining
    new_content = new_content[:max_size]
    
    with open(filename, "wb") as f:
        f.write(new_content)

    print(f"Inserted {n} bytes at start of {filename} and maintained file size {max_size} bytes.")

def main():
    if len(sys.argv) != 3:
        print("Usage: subcompiler input.bin")
        return
    input_file = sys.argv[1]
    with open(input_file, "rb") as f:
        obj_data = f.read()
    print(obj_data.decode('utf-8'))
    asm(obj_data.decode('utf-8'))
    print(tbytecode)
    with open("PROGMEM.bin", "wb") as file_pro:
        file_pro.write(b"\x00" * 65536)

        insert_bytes_at_start(tbytecode)

if __name__ == "__main__":
    main()