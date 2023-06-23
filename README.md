# Persona Manager

Persona Manager is a command-line tool for managing personas - fictional characters used for various purposes such data anonymization. It allows you to create, view, modify, and delete personas.

## Features

- Create a new persona with randomized data.
- View all existing personas with their details.
- Modify an existing persona by specifying the persona ID and updated fields.
- Delete a persona by ID or delete all personas.

## Installation

1. Clone the repository:

```git clone https://github.com/nicolasawelsh/persona-manager.git```

2. Change into the project directory:

```cd persona-manager```

3. Install the required dependencies:

```pip install -r requirements.txt```

## Usage

To use the Persona Manager, run the persona-cli.py script with the desired command and options.

```python persona-cli.py <command> [options]```

### Available Commands

- ```create```: Create a new persona
- ```view```: View all personas
- ```delete```: Delete a persona by ID or delete all personas
- ```modify```: Modify an existing persona

### Examples

Create a new randomized persona:

```python persona-cli.py create```

View all personas:

```python persona-cli.py view```

Delete a persona by ID (ex: delete persona 5):
```python persona-cli.py delete 5```

Delete all personas:
```python persona-cli.py delete --all```

Modify a persona (ex: change persona 2's last name to Doe):

```python persona-cli.py modify 2 --lastname Doe```

## License

This project is licensed under the MIT License.
