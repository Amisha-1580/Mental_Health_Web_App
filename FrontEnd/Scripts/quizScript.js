let currentQuestionId = 1;
const answers = {}; // Store user answers
let q_no = 0;
const MAX_QUESTIONS = 7;

// Function to fetch and display a question
async function fetchQuestion(questionId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/get-question/${questionId}`);
        const data = await response.json();

        if (response.ok) {
            displayQuestion(data);
        } else {
            alert(data.error || "Failed to load question.");
        }
    } catch (error) {
        console.error("Error fetching question:", error);
    }
}

// Function to display a question
function displayQuestion(data) {
    const questionContainer = document.querySelector(".quiz-container h3");
    const optionsContainer = document.getElementById("options");

    questionContainer.textContent = data.question;
    optionsContainer.innerHTML = ""; // Clear previous options

    data.options.forEach((option, index) => {
        const optionDiv = document.createElement("div");
        optionDiv.classList.add("container-row", "option-box");
        optionDiv.dataset.optionId = option.id;

        optionDiv.innerHTML = `
            <img src="../images/simple_smiley.png" alt="option-img" height="60px" width="60px">
            <label>${option.text}</label>
        `;

        optionDiv.addEventListener("click", changeSmileyAndSelectOption);
        optionsContainer.appendChild(optionDiv);
    });

    updateNavigationButtons();
}

// Handle option selection
const changeSmileyAndSelectOption = function () {
    document.querySelectorAll(".option-box").forEach(option => {
        option.classList.remove("selected");
        option.style.backgroundColor = "";
        option.querySelector("img").src = "../images/simple_smiley.png";
    });

    this.style.backgroundColor = "rgba(0, 0, 255, 0.2)";
    this.querySelector("img").src = "../images/opt_img.jpg";
    
    const optionIndex = [...this.parentElement.children].indexOf(this);
    answers[currentQuestionId] = optionIndex;
    updateNavigationButtons();
};

// Update navigation buttons
function updateNavigationButtons() {
    const prevButton = document.querySelector(".fa-arrow-left");
    const nextButton = document.querySelector(".fa-arrow-right");
    const finalSubmitButton = document.querySelector(".finalSubmission");

    prevButton.disabled = currentQuestionId === 1;
    nextButton.disabled = answers[currentQuestionId] === undefined;

    if (q_no === MAX_QUESTIONS - 1) {
        nextButton.style.display = "none";
        finalSubmitButton.style.display = "block";
    } else {
        nextButton.style.display = "inline-block";
        finalSubmitButton.style.display = "none";
    }
}

// Navigate to previous question
function goToPreviousQuestion() {
    if (currentQuestionId > 1) {
        currentQuestionId--;
        q_no--;
        fetchQuestion(currentQuestionId);
    }
}

// Navigate to next question
function goToNextQuestion() {
    if (answers[currentQuestionId] !== undefined) {
        q_no++;
        if (q_no < MAX_QUESTIONS) {
            currentQuestionId++;
            fetchQuestion(currentQuestionId);
        } else {
            submitQuiz();
        }
    } else {
        alert("Please select an option before proceeding.");
    }
}

// Submit quiz and redirect to result page
async function submitQuiz() {
    if (Object.keys(answers).length !== MAX_QUESTIONS) {
        alert("Please answer all the questions before submitting.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/submit-quiz", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ answers }),
        });

        const result = await response.json();
        const finalScore = result.score;

        // Save score in localStorage to access in result page
        localStorage.setItem("finalScore", finalScore);
        localStorage.setItem("totalQuestions", result.total_questions);

        window.location.href = "resultPage.html"; // Redirect to results page
    } catch (error) {
        console.error("Error submitting quiz:", error);
    }
}

// Event listeners for navigation buttons
document.querySelector(".fa-arrow-left").addEventListener("click", goToPreviousQuestion);
document.querySelector(".fa-arrow-right").addEventListener("click", goToNextQuestion);

document.querySelector(".btn-primary").addEventListener("click", () => {
    if (q_no < MAX_QUESTIONS) {
        goToNextQuestion();
    } else {
        submitQuiz();
    }
});

// Load first question
fetchQuestion(currentQuestionId);
