document.addEventListener("DOMContentLoaded", function () {
    // Get stored score and total questions from localStorage
    // finalScore is already scaled to 0-10 by the backend
    const finalScore = parseInt(localStorage.getItem("finalScore")) || 0;
    
    // DOM Elements
    const scoreBox = document.querySelector(".score");
    const gradeBox = document.querySelector(".grade-box span");
    const smiley = document.querySelector(".smiley");
    const tipsContainer = document.querySelector(".tips");

    if (!scoreBox || !gradeBox || !smiley || !tipsContainer) return;

    // Update score display
    scoreBox.textContent = `${finalScore}/10`;

    // Assign grade, emoji, and tips based on score
    let grade, emojiSrc, tipsHtml;

    if (finalScore >= 8) {
        grade = "Excellent! You're doing great.";
        emojiSrc = "/static/images/happy-face.png";
        tipsHtml = `
            <div class="tip">
                <p>Maintain your positive momentum!</p>
                <img src="/static/images/great_work.avif" alt="great work">
            </div>
            <div class="tip">
                <p>Help others stay positive too.</p>
                <img src="/static/images/meditation_tip.jpg" alt="meditation tip">
            </div>
        `;
    } else if (finalScore >= 5) {
        grade = "Good Job! Keep focusing on yourself.";
        emojiSrc = "/static/images/smile.png";
        tipsHtml = `
            <div class="tip">
                <p>Practice gratitude daily.</p>
                <img src="/static/images/gratitude.jpeg" alt="gratitude">
            </div>
            <div class="tip">
                <p>Take deep breaths and relax.</p>
                <img src="/static/images/deep_breath.jpeg" alt="deep breath">
            </div>
        `;
    } else {
        grade = "Take care! You might need some rest.";
        emojiSrc = "/static/images/sad.png";
        tipsHtml = `
            <div class="tip">
                <p>Try guided meditation.</p>
                <img src="/static/images/meditation_tip.jpg" alt="meditation tip">
            </div>
            <div class="tip">
                <p>Listen to calming music.</p>
                <img src="/static/images/music_listen_tip.png" alt="listen to music">
            </div>
        `;
    }

    // Apply updates to the page
    gradeBox.textContent = grade;
    smiley.src = emojiSrc;
    tipsContainer.innerHTML = tipsHtml;
});
