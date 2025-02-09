<<<<<<< HEAD
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
=======
// Predefined question-answer set related to mental health
const mentalHealthQA = [
    {
      keywords: ["restless", "lack of focus", "difficulty concentrating"],
      response: "It seems like you might be experiencing anxiety or stress.",
      tips: [
        "Try practicing mindfulness or meditation.",
        "Take short breaks during your work or study sessions.",
        "Engage in physical activities to release tension."
      ],
    },
    {
      keywords: ["sad", "down", "hopeless", "crying"],
      response: "It sounds like you may be feeling symptoms of depression.",
      tips: [
        "Consider talking to someone you trust about your feelings.",
        "Engage in activities you enjoy or try something new.",
        "Make sure you're getting enough sleep and eating healthy meals."
      ],
    },
    {
      keywords: ["angry", "irritable", "frustrated"],
      response: "You might be feeling overwhelmed or dealing with anger issues.",
      tips: [
        "Practice deep breathing exercises to calm down.",
        "Identify the root cause of your anger and address it step by step.",
        "Engage in hobbies or activities that bring you peace."
      ],
    },
    {
      keywords: ["tired", "exhausted", "burnt out", "low energy"],
      response: "You might be experiencing burnout or fatigue.",
      tips: [
        "Ensure you're taking breaks and not overworking yourself.",
        "Prioritize your tasks and delegate when possible.",
        "Stay hydrated and eat energy-boosting foods."
      ],
    },
    {
      keywords: ["sleep", "insomnia", "trouble sleeping"],
      response: "It seems like you might be dealing with sleep-related issues.",
      tips: [
        "Avoid screens at least an hour before bedtime.",
        "Create a calming bedtime routine to help you relax.",
        "Consider maintaining a consistent sleep schedule."
      ],
    },

{
  keywords: ["burnout", "work stress", "overwhelm"],
  response: "It seems like you're dealing with burnout or work-related stress.",
  tips:[
  
  "Take regular breaks throughout your workday to avoid exhaustion.",
  "Set clear boundaries between work and personal life.",
  "Delegate tasks where possible and seek support from colleagues.",
  ],
  },

{
  keywords: ["loneliness", "isolation", "feeling disconnected"],
response: "It seems like you're feeling lonely or disconnected.",
tips:[

"Reach out to friends or family, even for a simple chat.",
"Join a group or community activity to meet new people with similar interests.",
"Volunteer for a cause that matters to you to build connections.",
],
},
    {
      keywords: ["overwhelmed", "panic", "fear"],
      response: "It sounds like you might be experiencing panic or anxiety attacks.",
      tips: [
        "Focus on your breathing—inhale for 4 seconds, hold for 4 seconds, exhale for 4 seconds.",
        "Try grounding techniques like identifying 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
        "Seek support from a trusted friend or professional."
      ],
    },
    // Add more Q&A sets as needed
  ];
  
  // Reference DOM elements
  const chatDisplay = document.getElementById("chat-display");
  const chatInput = document.getElementById("chat-input");
  const sendBtn = document.getElementById("send-btn");
  
  // Function to append messages to the chat window
  function appendMessage(sender, message) {
    const messageDiv = document.createElement("div");
    messageDiv.className = sender === "user" ? "user-message" : "bot-message";
    messageDiv.textContent = message;
    chatDisplay.appendChild(messageDiv);
    chatDisplay.scrollTop = chatDisplay.scrollHeight; // Auto-scroll to the latest message
  }
  
  // Function to process user input and find the appropriate response
  function processUserInput(input) {
    // Convert input to lowercase for matching
    const lowerInput = input.toLowerCase();
  
    // Search through the predefined Q&A set
    for (const item of mentalHealthQA) {
      for (const keyword of item.keywords) {
        if (lowerInput.includes(keyword)) {
          // If a match is found, return the response and tips
          return {
            response: item.response,
            tips: item.tips,
          };
        }
      }
    }
  
    // Default response if no keywords match
    return {
      response: "I'm sorry, I couldn't identify your concern. Can you provide more details?",
      tips: ["Consider describing your feelings or symptoms more specifically."],
    };
  }
  
  // Function to handle user message
  function handleUserMessage() {
    const userMessage = chatInput.value.trim();
    if (!userMessage) return; // Ignore empty input
  
    // Display the user's message
    appendMessage("user", userMessage);
  
    // Clear the input field
    chatInput.value = "";
  
    // Process the input to get the chatbot's response
    const botResponse = processUserInput(userMessage);
  
    // Display the chatbot's response
    appendMessage("bot", botResponse.response);
  
    // Display tips one by one
    botResponse.tips.forEach((tip) => {
      appendMessage("bot", `Tip: ${tip}`);
    });
  }
  
  // Add event listeners
  sendBtn.addEventListener("click", handleUserMessage);
  chatInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      handleUserMessage();
    }
  });
  
>>>>>>> 480664d (chatbot working added)
