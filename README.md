
# Multigenerative Grammar CLI

This project implements a command line application that utilizes a multigenerative grammar system with scattered context grammars to produce MIDI music files.

## Installation
Activate virtual environment and then activate it:
```
python3 -m venv music-env
source music-env/bin/activate
```
To install the required dependencies, run:

```
pip install -r requirements.txt
```


## Examples

1. **Generating MIDI Music**: 
   ```
   python3 src/main.py generate src/examples/basic/GS1.json 3  example.mid
   python3 src/main.py generate src/examples/iterative/GS5.json
   python3 src/main.py generate src/examples/iterative/GS5.json 3  example.mid
   ```

2. **Available commands**:
   ```
   python3 src/main.py list
   ```
   
3. **Available instruments for input file**:
	```
	python3 src/main.py instruments
	```
