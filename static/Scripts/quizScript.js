let currentQuestionIndex = 0;
let quizQuestionIds = [];
const answers = {}; // Store user answers

// Initial selectors
const questionContainer = document.querySelector(".quiz-container h3");
const optionsContainer = document.getElementById("options");
const prevButton = document.getElementById("prev-btn");
const nextButton = document.getElementById("next-btn");
const submitButton = document.getElementById("final-submit-btn");

// Function to initialize the quiz
async function initQuiz() {
    if (!questionContainer) return;
    
    questionContainer.textContent = "Preparing your personalized quiz...";
    
    try {
        const response = await fetch('/start-quiz');
        const data = await response.json();
        
        if (response.ok && data.question_ids) {
            quizQuestionIds = data.question_ids;
            currentQuestionIndex = 0;
            fetchQuestion(quizQuestionIds[currentQuestionIndex]);
        } else {
            questionContainer.textContent = "Error starting quiz. Please refresh.";
        }
    } catch (error) {
        console.error("Init Error:", error);
        questionContainer.textContent = "Failed to connect to server.";
    }
}

// Function to fetch and display a question
async function fetchQuestion(questionId) {
    if (!questionContainer || !optionsContainer) return;
    
    questionContainer.textContent = "Loading Question...";
    optionsContainer.innerHTML = "";

    try {
        const response = await fetch(`/get-question/${questionId}`);
        const data = await response.json();

        if (response.ok) {
            displayQuestion(data);
        } else {
            console.error("API Error:", data.error);
            questionContainer.textContent = "Error loading question.";
        }
    } catch (error) {
        console.error("Fetch Error:", error);
        questionContainer.textContent = "Connection error.";
    }
}

// Function to display a question
function displayQuestion(data) {
    if (!questionContainer || !optionsContainer) return;

    const questionNum = currentQuestionIndex + 1;
    const totalQuestions = quizQuestionIds.length;
    
    questionContainer.textContent = `${questionNum}. ${data.question}`;
    optionsContainer.innerHTML = ""; 

    const currentQuestionId = quizQuestionIds[currentQuestionIndex];

    data.options.forEach((option) => {
        const optionDiv = document.createElement("div");
        optionDiv.classList.add("option-box");
        if (answers[currentQuestionId] === option.id) {
            optionDiv.classList.add("selected");
        }

        optionDiv.innerHTML = `
            <img src="/static/images/${answers[currentQuestionId] === option.id ? 'opt_img.jpg' : 'simple_smiley.png'}" alt="option-img">
            <label>${option.text}</label>
        `;

        optionDiv.addEventListener("click", () => selectOption(option.id, optionDiv));
        optionsContainer.appendChild(optionDiv);
    });

    updateNavigationButtons();
}

// Handle option selection
function selectOption(optionId, element) {
    const currentQuestionId = quizQuestionIds[currentQuestionIndex];
    answers[currentQuestionId] = optionId;
    
    document.querySelectorAll(".option-box").forEach(box => {
        box.classList.remove("selected");
        box.querySelector("img").src = "/static/images/simple_smiley.png";
    });
    
    element.classList.add("selected");
    element.querySelector("img").src = "/static/images/opt_img.jpg";
    
    updateNavigationButtons();
}

// Update navigation buttons
function updateNavigationButtons() {
    if (!prevButton || !nextButton || !submitButton) return;

    prevButton.disabled = (currentQuestionIndex === 0);
    
    const isLastQuestion = (currentQuestionIndex === quizQuestionIds.length - 1);
    const currentQuestionId = quizQuestionIds[currentQuestionIndex];
    const hasAnswered = (answers[currentQuestionId] !== undefined);

    if (isLastQuestion) {
        nextButton.style.display = "none";
        submitButton.style.display = "block";
        submitButton.disabled = !hasAnswered;
    } else {
        nextButton.style.display = "block";
        submitButton.style.display = "none";
        nextButton.disabled = !hasAnswered;
    }
}

// Navigate to previous question
function goToPreviousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        fetchQuestion(quizQuestionIds[currentQuestionIndex]);
    }
}

// Navigate to next question
function goToNextQuestion() {
    const currentQuestionId = quizQuestionIds[currentQuestionIndex];
    if (answers[currentQuestionId] !== undefined) {
        if (currentQuestionIndex < quizQuestionIds.length - 1) {
            currentQuestionIndex++;
            fetchQuestion(quizQuestionIds[currentQuestionIndex]);
        }
    }
}

// Submit quiz
async function submitQuiz() {
    if (Object.keys(answers).length < quizQuestionIds.length) {
        alert("Please answer all questions.");
        return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "Submitting...";

    try {
        const response = await fetch("/submit-quiz", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ answers }),
        });

        const result = await response.json();
        if (response.ok) {
            localStorage.setItem("finalScore", result.score);
            localStorage.setItem("totalQuestions", result.total_questions);
            window.location.href = "/result";
        } else {
            alert("Submission failed.");
            submitButton.disabled = false;
        }
    } catch (error) {
        console.error("Submit Error:", error);
        submitButton.disabled = false;
    }
}

// Event Listeners
if (prevButton) prevButton.addEventListener("click", goToPreviousQuestion);
if (nextButton) nextButton.addEventListener("click", goToNextQuestion);
if (submitButton) submitButton.addEventListener("click", submitQuiz);

// Initialize on load
document.addEventListener("DOMContentLoaded", () => {
    initQuiz();
});
