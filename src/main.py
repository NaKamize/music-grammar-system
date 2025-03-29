import sys
from cli.commands import Commands

def main():
    commands = Commands()
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <command> [args...]")
        return

    command_name = sys.argv[1]
    args = sys.argv[2:]  # Collect additional arguments

    # Pass the command name and arguments to the Commands class
    commands.execute_command(command_name, *args)

if __name__ == "__main__":
    main()