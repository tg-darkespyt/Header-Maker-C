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

banner()
