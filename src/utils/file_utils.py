def read_file(filepath: str) -> str:
    with open(filepath, 'r') as file:
        return file.read()

def write_file(filepath: str, content: str) -> None:
    with open(filepath, 'w') as file:
        file.write(content)