# filepath: /multigenerative-grammar-cli/multigenerative-grammar-cli/src/main.py

import sys
from cli.commands import Commands

def main():
    commands = Commands()
    if len(sys.argv) < 2:
        print("No command provided. Use 'list' to see available commands.")
        return
    
    command_name = sys.argv[1]
    commands.execute_command(command_name)

if __name__ == "__main__":
    main()