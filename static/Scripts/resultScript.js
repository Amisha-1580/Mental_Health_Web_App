document.addEventListener("DOMContentLoaded", function () {
    // Get stored score and total questions from localStorage
    const finalScore = localStorage.getItem("finalScore") || 0;
    const totalQuestions = 10 ;//localStorage.getItem("totalQuestions") || 10;

    // DOM Elements
    const scoreBox = document.querySelector(".score");
    const gradeBox = document.querySelector(".grade-box span");
    const smiley = document.querySelector(".grade-box img");
    const tipsContainer = document.querySelector(".tips");

    // Update score display
    // scoreBox.textContent = `${finalScore}/${totalQuestions*10}`;
    mental_health_grade = Math.floor((finalScore/(totalQuestions*10))*10);
    scoreBox.textContent = `${mental_health_grade}/10`;

    // Assign grade, emoji, and tips based on score
    let grade, emojiSrc, tipsHtml;

    if (mental_health_grade >= 8) {
        grade = "Excellent!";
        emojiSrc = "../images/happy-face.png";
        tipsHtml = `
            <div class="tip"><p>Keep up the great work!</p>
            <img src="../static/images/great_work.avif" alt="great work"></div>

            <div class="tip"><p>Try mindfulness exercises.</p>
            <img src="../static/images/meditation_tip.jpg" alt="meditation tip"></div>
        `;
    } else if (mental_health_grade >= 5) {
        grade = "Good Job!";
        emojiSrc = "../static/images/smile.png";
        tipsHtml = `
            <div class="tip"><p>Practice gratitude daily.</p>
            <img src="../static/images/gratitude.jpeg" alt="gratitude">
            </div>
            <div class="tip"><p>Take deep breaths and relax.</p>
              <img src="../static/images/deep_breath.jpeg" alt="deep breath">
            </div>
        `;
    } else {
        grade = "Needs Improvement!";
        emojiSrc = "../static/images/sad.png";
        tipsHtml = `
            <div class="tip"><p>Try meditation.</p>
              <img src="../static/images/meditation_tip.jpg" alt="meditation tip"></div>
            <div class="tip"><p>Listen to calming music.</p>
             <img src="../static/images/music_listen_tip.png" alt="listen to music"></div>
        `;
    }

    // Apply updates to the page
    gradeBox.textContent = grade;
    smiley.src = emojiSrc;
    tipsContainer.innerHTML = tipsHtml;
});
