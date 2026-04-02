import subprocess
import sys
import os

def run_subcompiler(input_file, output_file):
    subprocess.run([sys.executable, "build/linker.py", input_file, output_file], check=True)

def run_assembler(input_file, output_file):
    subprocess.run([sys.executable, "build/assembler.py", input_file, output_file], check=True)

def main():
    if len(sys.argv) != 2:
        print("Usage: python build.py <input_file>")
        return

    input_file = sys.argv[1]

    base_name = os.path.splitext(input_file)[0]
    bin_file = base_name + ".bin"
    final_file = base_name + ".mem"

    print(f"Running subcompiler: {input_file} -> {bin_file}")
    run_subcompiler(input_file, bin_file)

    print(f"Running assembler: {bin_file} -> PROGMEM.bin")
    run_assembler(bin_file, final_file)

    print(f"Build complete! Final output: PROGMEM.bin")

if __name__ == "__main__":
    main()
