from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",  # Adjust URL/port as needed
    api_key="not-needed"
)

def get_llm_response(prompt):
    """Get response from local LLM"""
    try:
        response = client.chat.completions.create(
            model="qwen2.5-coder-14b-instruct",  # Use your local model name
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Create HTML template
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Local LLM Chat</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .container {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            textarea {
                width: 100%;
                height: 100px;
                padding: 10px;
                margin-bottom: 10px;
            }
            button {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            #response {
                white-space: pre-wrap;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                min-height: 100px;
            }
            .loading {
                display: none;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Local LLM Chat</h1>
            <div>
                <textarea id="prompt" placeholder="Enter your prompt here..."></textarea>
                <button onclick="getResponse()">Send</button>
            </div>
            <div id="loading" class="loading">Thinking...</div>
            <div id="response"></div>
        </div>

        <script>
        async function getResponse() {
            const promptElement = document.getElementById('prompt');
            const responseElement = document.getElementById('response');
            const loadingElement = document.getElementById('loading');
            const prompt = promptElement.value;

            if (!prompt) return;

            // Show loading message
            loadingElement.style.display = 'block';
            responseElement.textContent = '';

            try {
                const response = await fetch('/get_response', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ prompt: prompt }),
                });

                const data = await response.json();
                responseElement.textContent = data.response;
            } catch (error) {
                responseElement.textContent = 'Error: Could not get response';
            } finally {
                loadingElement.style.display = 'none';
            }
        }

        // Allow Enter key to submit
        document.getElementById('prompt').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                getResponse();
            }
        });
        </script>
    </body>
    </html>
    '''

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    prompt = data.get('prompt', '')
    response = get_llm_response(prompt)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
