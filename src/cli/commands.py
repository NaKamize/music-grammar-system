class Commands:
    def execute_command(self, command_name, *args):
        if command_name == "generate":
            self.generate_music(*args)
        elif command_name == "list":
            self.list_commands()
        else:
            print(f"Unknown command: {command_name}")

    def list_commands(self):
        print("Available commands:")
        print("  generate - Generate MIDI music from grammar")
        print("  list - List available commands")

    def generate_music(self, grammar_file):
        # Placeholder for generating music logic
        print(f"Generating music from grammar file: {grammar_file}")