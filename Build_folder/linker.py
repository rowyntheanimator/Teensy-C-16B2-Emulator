import sys

def flatten(lst: list) -> list:
    flat_list = []
    for i in range(len(lst)):
        if type(lst[i]) == list:
            flat_list += flatten(lst[i])
        else:
            flat_list.append(lst[i])
    return flat_list

def rearange_functions(string: list) -> list:
    lines = []
    for i in range(len(string)):
        lines.append(string[i].rstrip())
    func_lines = []
    code_lines = []
    output = []
    for i in range(len(lines)):
        if lines[i] == "":
            continue
        if lines[i][0] == " " or lines[i][-1] == ":":
            func_lines.append(lines[i])
        else:
            code_lines.append(lines[i])
    output.append(code_lines)
    output.append(func_lines)
    output = flatten(output)
    return output

def remove_comments(code: str) -> list:
    code = code.splitlines()
    lines = ""
    output = []
    for i in range(len(code)):
        line = code[i]
        lines = ""
        for j in range(len(line)):
            if line[j] == ";":
                break
            else:
                lines += line[j]
        output.append(lines)
    return output

def func_name(s: str) -> str:
    i = len(s) - 1
    while i >= 0 and s[i] != '_':
        i -= 1
    if i < 0:
        return ""
    end = i
    i -= 1
    while i >= 0 and s[i] != ' ':
        i -= 1
    start = i
    return s[start + 1 : end]

def neg(x: int) -> int:
    return x-(x*2)

def jump_index(code: list) -> list:
    funcs = {}
    text = []
    text2 = []
    text3 = []
    output = []
    temp = False
    temp2 = ""
    for i in range(len(code)):
        if code[i] == "":
            continue
        if temp:
            temp = False
            continue
        if code[i][-1] == ":":
            text.append(code[i+1]+" "+code[i][:-1]+"_"+"func")
            temp = True
        else:
            text.append(code[i])
    for i in range(len(text)):
        if text[i] == "":
            continue
        if text[i][0] == " ":
            text2.append(text[i][4:])
        else:
            text2.append(text[i])
    for i in range(len(text2)):
        if len(text2[i]) < 7:
            continue
        if text2[i][-4:] == "func":
            funcs[func_name(text2[i])] = i
    for i in range(len(text2)):
        if len(text2[i]) < 7:
            text3.append(text2[i])
            continue
        if text2[i][-4:] == "func":
            temp2 = text2[i][:-5]
            temp2 = temp2[:neg(len(func_name(text2[i])))]
            text3.append(temp2)
        else:
            text3.append(text2[i])
    for i in range(len(text3)):
        line = text3[i]
        if line == "":
            continue
        if len(line) < 3:
            output.append(line)
            continue
        inst = line[:3]
        if inst in ["JMP", "JCZ", "JCN"]:
            target = line[4:].strip()
            if target in funcs:
                output.append(f"{inst} #{funcs[target]*7}")
            else:
                print(f"{target} AT {i} HAS NO LABEL.")
                return
        else:
            output.append(line)

    return output

def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: subcompiler input.obj output.bin")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "rb") as f:
        obj_data = f.read()

    bin_data = process_obj(obj_data)

    with open(output_file, "wb") as f:
        f.write(bin_data)

def process_obj(obj_data: bytes) -> bytes:
    obj_data_str = obj_data.decode('utf-8')
    rearanged = remove_comments(obj_data_str)
    remove = rearange_functions(rearanged)
    out = jump_index(remove)
    out_str = ""
    for i in range(len(out)):
        out_str+=out[i]+"\n"
    return out_str.encode('utf-8')

if __name__ == "__main__":
    main()