#!/usr/bin/env python3
"""
Simple Web Application
Takes user input and outputs it back via web interface
"""

from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Python Web App</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            padding: 40px;
            max-width: 500px;
            width: 100%;
            text-align: center;
        }
        
        .header {
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .input-section {
            margin-bottom: 30px;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        
        button:hover {
            transform: translateY(-2px);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .output-section {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            min-height: 100px;
            text-align: left;
        }
        
        .output-section h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        
        .output-text {
            color: #666;
            font-size: 1.1em;
            line-height: 1.6;
            word-wrap: break-word;
        }
        
        .history {
            margin-top: 20px;
            text-align: left;
        }
        
        .history h4 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .history-item {
            background: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 5px;
            border-left: 4px solid #667eea;
        }
        
        .clear-btn {
            background: #dc3545;
            margin-top: 10px;
        }
        
        .clear-btn:hover {
            background: #c82333;
        }
        
        .footer {
            margin-top: 30px;
            color: #666;
            font-size: 0.9em;
        }
        
        @media (max-width: 600px) {
            .container {
                padding: 20px;
            }
            
            .input-group {
                flex-direction: column;
            }
            
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Simple Web App</h1>
            <p>Enter text and see it displayed below</p>
        </div>
        
        <div class="input-section">
            <form id="inputForm">
                <div class="input-group">
                    <input type="text" id="userInput" placeholder="Enter something here..." required>
                    <button type="submit">Submit</button>
                </div>
            </form>
        </div>
        
        <div class="output-section">
            <h3>Output:</h3>
            <div id="output" class="output-text">
                Enter text above to see the output here...
            </div>
        </div>
        
        <div class="history">
            <h4>History:</h4>
            <div id="history"></div>
            <button class="clear-btn" onclick="clearHistory()">Clear History</button>
        </div>
        
        <div class="footer">
            <p>Simple Python Web Application</p>
        </div>
    </div>

    <script>
        let history = [];
        
        document.getElementById('inputForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const input = document.getElementById('userInput').value.trim();
            if (input) {
                // Add to history
                history.push(input);
                updateHistory();
                
                // Update output
                document.getElementById('output').textContent = input;
                
                // Clear input
                document.getElementById('userInput').value = '';
                
                // Send to server
                fetch('/process', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({input: input})
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Server response:', data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        });
        
        function updateHistory() {
            const historyDiv = document.getElementById('history');
            historyDiv.innerHTML = '';
            
            history.slice(-5).reverse().forEach((item, index) => {
                const historyItem = document.createElement('div');
                historyItem.className = 'history-item';
                historyItem.textContent = `${history.length - index}: ${item}`;
                historyDiv.appendChild(historyItem);
            });
        }
        
        function clearHistory() {
            history = [];
            updateHistory();
            document.getElementById('output').textContent = 'Enter text above to see the output here...';
        }
        
        // Allow Enter key to submit
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                document.getElementById('inputForm').dispatchEvent(new Event('submit'));
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/process', methods=['POST'])
def process_input():
    """Process user input"""
    try:
        data = request.get_json()
        user_input = data.get('input', '')
        
        # Simple processing - just echo back the input
        output = f"Output: {user_input}"
        
        return jsonify({
            'success': True,
            'input': user_input,
            'output': output
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Simple Web App is running!'
    })

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    print("=" * 60)
    print("Simple Web Application")
    print("=" * 60)
    print(f"Starting server on port {port}...")
    print(f"Open your browser and go to: http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=port, debug=True) 