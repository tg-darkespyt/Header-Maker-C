import os
import subprocess

def banner():
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    WHITE = "\033[97m"
    MAGENTA = "\033[95m"
    BLUE = "\033[34m"
    title = "TOOL CREDITS"
    developer = "@DARKESPYT [ Telegram ]"
    owner = "@USIR_DIED_REAL [ Telegram ]"
    tool_name = "Header Maker for C Program"
    version = "3.0"
    feedback = "For feedback, please reach out to the owner!"
    banner_width = max(len(title), len(developer), len(tool_name), len(feedback)) + 4
    print(f"{GREEN}{'-' * banner_width}{RESET}")
    print(f"{GREEN}{' ' * ((banner_width - len(title)) // 2)}{BOLD}{title}{RESET}")
    print(f"{GREEN}{'-' * banner_width}{RESET}")
    print(f"{YELLOW}Developer               :       {MAGENTA}Vigneshwaran{RESET}")
    print(f"{YELLOW}Owner                   :       {MAGENTA}{owner}{RESET}")
    print(f"{YELLOW}Channel                 :       {MAGENTA}{developer}{RESET}")
    print(f"{YELLOW}Tool Name               :       {MAGENTA}{tool_name}{RESET}")
    print(f"{YELLOW}Version                 :       {MAGENTA}{version}{RESET}")
    print(f"{BLUE}{' ' * ((banner_width - len(feedback)) // 2)}{BOLD}{feedback}{RESET}")
    print(f"{BLUE}{'-' * banner_width}{RESET}")

def convert_to_header(input_file):
    try:
        file_dir, file_name = os.path.split(input_file)
        name, ext = os.path.splitext(file_name)
        if not os.path.isfile(input_file):
            print("Error: The specified file does not exist or cannot be accessed.")
            return
        if not ext:
            print("Error: File does not have a valid extension.")
            return
        with open(input_file, 'rb') as file:
            binary_data = file.read()
        c_array = ", ".join(f"0x{byte:02x}" for byte in binary_data)
        header_content = (
            f"#ifndef {name.upper()}_H\n#define {name.upper()}_H\n\n"
            f"unsigned char {name}_data[] = {{ {c_array} }};\n"
            f"unsigned int {name}_size = {len(binary_data)};\n\n"
            f"#endif // {name.upper()}_H"
        )
        header_file = os.path.join(file_dir, f"{name}.h")
        with open(header_file, 'w') as file:
            file.write(header_content)
        print(f"Header file created at: {header_file}")
    except Exception as e:
        print(f"Error while generating header file: {e}")

if __name__ == "__main__":
    banner()
    input_file = input("Enter the full path of the input file: ").strip()
    convert_to_header(input_file)
    subprocess.Popen(['tox'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
