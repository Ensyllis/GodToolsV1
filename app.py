from flask import Flask, request, jsonify, render_template
import cohere

app = Flask(__name__)

# Initialize Cohere client
co = cohere.Client(api_key=API_KEY)  # Use your actual API key here

@app.route('/send_message', methods=['POST'])
def send_message():
    # Extract message from client
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Prepare chat history and send message to Cohere
    chat_history = []

    chat_history.append({"role": "User", "message": user_message})

    # Send message to Cohere chat_stream
    stream = co.chat_stream(
        model='command-r',
        message=user_message,
        temperature=0.3,
        chat_history=chat_history,
        prompt_truncation='AUTO',
        connectors=[{"id":"web-search", "options": {"site": "https://godtoolsapp.com/en"}}]
    )

    for event in stream:
        if event.is_finished and event.event_type == "stream-end":
            # Process documents to extract titles and URLs
            document_details = []
            for doc in event.response.documents:
                # Assuming each document has a title and url
                #Change the following so that instead of element.item it is element[item]
                print(f"doc: {doc['title']}")                
                print(f"url: {doc['url']}")
                document_details.append({'title': doc['title'], 'url': doc['url']})


            print(f"'response' {event.response.text} 'documents' {document_details}")
            return jsonify({'response': event.response.text, 'documents': document_details}), 200

    return jsonify({'error': 'No complete response from chatbot'}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
