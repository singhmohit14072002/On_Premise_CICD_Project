# Simple Python Application

A simple Python application that takes user input and outputs it back. Available in both terminal and web versions.

## Features

- **Terminal Version**: Simple command-line interface
- **Web Version**: Beautiful web interface with modern UI
- Takes user input and outputs it back
- History tracking (web version)
- Responsive design (web version)

## How to Run

### Terminal Version

#### Local Python
```bash
python simple_app.py
```

#### Docker
```bash
# Build the container
docker build -t simple-python-app .

# Run the container
docker run -it simple-python-app
```

### Web Version

#### Local Python
```bash
# Install Flask
pip install Flask

# Run the web application
python simple_web_app.py
```

Then open your browser and go to: `http://localhost:5000`

#### Docker
```bash
# Build the container
docker build -t simple-web-app .

# Run the container
docker run -p 5000:5000 simple-web-app
```

Then open your browser and go to: `http://localhost:5000`

## Usage

### Terminal Version
1. Run the application
2. Enter any text when prompted
3. See the output
4. Type 'quit' to exit

### Web Version
1. Open the application in your browser
2. Enter text in the input field
3. Click "Submit" or press Enter
4. See the output displayed below
5. View history of previous inputs
6. Clear history if needed

## Example

### Terminal Output
```
==================================================
Simple Python Application
==================================================

Enter something (or 'quit' to exit): hello
Output: hello

Enter something (or 'quit' to exit): world
Output: world

Enter something (or 'quit' to exit): quit
Goodbye!
```

### Web Interface
- Beautiful gradient background
- Modern card-based design
- Real-time input/output
- History tracking
- Responsive mobile design

## Requirements

- Python 3.6+
- Flask (for web version)
- Docker (optional)

## Files

- `simple_app.py` - Terminal version
- `simple_web_app.py` - Web version with Flask
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration 