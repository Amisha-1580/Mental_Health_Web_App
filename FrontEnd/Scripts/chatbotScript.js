// Backend API URL
const API_URL = "http://127.0.0.1:5000/chat"; // Update with your backend URL if hosted elsewhere

const chatWindow = document.getElementById("chat-display");
const chatInput = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

// Function to append messages to the chat window
function appendMessage(sender, message) {
    const messageElement = document.createElement("div");
    messageElement.classList.add(sender === "user" ? "user-message" : "bot-message");
    messageElement.textContent = message;
    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Event listener for send button
sendBtn.addEventListener("click", async () => {
    const userMessage = chatInput.value.trim();
    if (!userMessage) return;

    // Display user's message
    appendMessage("user", userMessage);
    chatInput.value = "";

    try {
        // Send query to the backend
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query: userMessage }),
        });

        if (!response.ok) {
            throw new Error("Failed to fetch response from backend.");
        }

        const data = await response.json();

        // Display bot's response
        const botResponse = `Condition: ${data.condition}\nSentiment: ${data.sentiment}\nTips: ${data.tips}`;
        appendMessage("bot", botResponse);
    } catch (error) {
        appendMessage("bot", "Sorry, I couldn't process your request. Please try again later.");
        console.error("Error:", error);
    }
});