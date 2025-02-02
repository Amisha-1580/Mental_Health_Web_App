// quizScript.js

let currentQuestionId = 1; // Start from question ID 1
const answers = {}; // Store user answers
let q_no = 0;
let MAX_QUESTIONS = 7;

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

    // Set question text
    questionContainer.textContent = data.question;

    // Clear and populate options
    optionsContainer.innerHTML = "";
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

// Function to handle option selection and smiley change
const changeSmileyAndSelectOption = function (event) {
    // Deselect all options (uncheck like radio button)
    const options = document.querySelectorAll(".option-box");
    options.forEach(option => {
        option.classList.remove("selected");
        const img = option.querySelector("img");
        img.src = "../images/simple_smiley.png"; // Reset image
        option.style.backgroundColor = ""; // Reset background color
    });

    // Change the background color to blueish for the selected option
    this.style.backgroundColor = "rgba(0, 0, 255, 0.2)"; // Light blue background

    // Find the image inside the clicked option box and change the src
    const img = this.querySelector("img");
    img.src = "../images/opt_img.jpg"; // New image path

    // Mark the current option as selected and store the answer
    const optionIndex = [...this.parentElement.children].indexOf(this);
    this.classList.add("selected");
    answers[currentQuestionId] = optionIndex;  // Store the selected answer
    console.log("Selected Answer for question " + currentQuestionId + ": " + optionIndex);  // Log the selected answer
    updateNavigationButtons(); // Ensure navigation buttons are updated
};

// Update navigation buttons' state
function updateNavigationButtons() {
    const prevButton = document.querySelector(".fa-arrow-left");
    const nextButton = document.querySelector(".fa-arrow-right");

    // Check if the answer is selected before enabling the next button
    nextButton.disabled = answers[currentQuestionId] === undefined;
    prevButton.disabled = currentQuestionId === 1;
}

// Navigate to the previous question
function goToPreviousQuestion() {
    if (currentQuestionId > 1) {
        currentQuestionId--;
        fetchQuestion(currentQuestionId);
    }
}

// Navigate to the next question
function goToNextQuestion() {
    if (answers[currentQuestionId] !== undefined) { // Ensure the answer is selected
        currentQuestionId++;
        fetchQuestion(currentQuestionId);
    } else {
        alert("Please select an option before proceeding.");
    }
}

// Submit the quiz
async function submitQuiz() {
    if (Object.keys(answers).length !== MAX_QUESTIONS) {
        alert("Please answer all the questions before submitting.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/submit-quiz", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ answers }),
        });

        // Hide navigation buttons and show the final submission button
        document.querySelector(".navButtons").style.display = "none";
        document.querySelector(".finalSubmission").style.display = "block";

        const result = await response.json();
        alert(`Your total score is ${result.score} out of ${result.total_questions}.`);
    } catch (error) {
        console.error("Error submitting quiz:", error);
    }
}

// Event listeners for navigation buttons
document.querySelector(".fa-arrow-left").addEventListener("click", goToPreviousQuestion);
document.querySelector(".fa-arrow-right").addEventListener("click", goToNextQuestion);

document.querySelector(".btn-primary").addEventListener("click", () => {
    if (currentQuestionId <= MAX_QUESTIONS) {
        currentQuestionId++;
        goToNextQuestion();
    } else {
        submitQuiz();
    }
});

// Load the first question on page load
fetchQuestion(currentQuestionId);
