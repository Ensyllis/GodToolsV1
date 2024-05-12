// script.js
function sendMessage() {
    var input = document.getElementById('chat-input');
    var message = input.value.trim();
    if (message === "") return;

    appendMessage("You", message); // Display the user's message
    input.value = ""; // Clear input field

    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        appendMessage("Bot", data.response, data.documents); // Display the bot's response
    })
    .catch(error => console.error('Error:', error));
}

function appendMessage(sender, message, documents=[]) {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    msgDiv.textContent = sender + ": " + message;
    chatBox.appendChild(msgDiv);

    // Handle and display document links
    documents.forEach(doc => {
        const docDiv = document.createElement('div');
        const link = document.createElement('a');
        link.href = doc.url;
        link.textContent = doc.title;
        link.target = "_blank";  // Opens the link in a new tab
        docDiv.appendChild(link);
        chatBox.appendChild(docDiv);
    });

    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the latest message
}
