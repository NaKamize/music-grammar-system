import unittest
from src.cli.commands import Commands

class TestCommands(unittest.TestCase):

    def setUp(self):
        self.commands = Commands()

    def test_execute_command(self):
        # Test a valid command execution
        result = self.commands.execute_command('some_command')
        self.assertEqual(result, 'Expected output for some_command')

    def test_list_commands(self):
        # Test if the command list is not empty
        command_list = self.commands.list_commands()
        self.assertTrue(len(command_list) > 0)

    def test_invalid_command(self):
        # Test execution of an invalid command
        with self.assertRaises(ValueError):
            self.commands.execute_command('invalid_command')

if __name__ == '__main__':
    unittest.main()