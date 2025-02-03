document.addEventListener("DOMContentLoaded", function () {
    // Get stored score and total questions from localStorage
    const finalScore = localStorage.getItem("finalScore") || 0;
    const totalQuestions = localStorage.getItem("totalQuestions") || 10;

    // DOM Elements
    const scoreBox = document.querySelector(".score");
    const gradeBox = document.querySelector(".grade-box span");
    const smiley = document.querySelector(".grade-box img");
    const tipsContainer = document.querySelector(".tips");

    // Update score display
    scoreBox.textContent = `${finalScore}/${totalQuestions}`;

    // Assign grade, emoji, and tips based on score
    let grade, emojiSrc, tipsHtml;

    if (finalScore >= 8) {
        grade = "Excellent!";
        emojiSrc = "../images/happy_smiley.png";
        tipsHtml = `
            <div class="tip"><p>Keep up the great work!</p></div>
            <div class="tip"><p>Try mindfulness exercises.</p></div>
        `;
    } else if (finalScore >= 5) {
        grade = "Good Job!";
        emojiSrc = "../images/neutral_smiley.png";
        tipsHtml = `
            <div class="tip"><p>Practice gratitude daily.</p></div>
            <div class="tip"><p>Take deep breaths and relax.</p></div>
        `;
    } else {
        grade = "Needs Improvement!";
        emojiSrc = "../images/sad_smiley.png";
        tipsHtml = `
            <div class="tip"><p>Try meditation.</p></div>
            <div class="tip"><p>Listen to calming music.</p></div>
        `;
    }

    // Apply updates to the page
    gradeBox.textContent = grade;
    smiley.src = emojiSrc;
    tipsContainer.innerHTML = tipsHtml;
});
