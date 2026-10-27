document.addEventListener("DOMContentLoaded", () => {
    const answerButtons = document.querySelectorAll('.answer-button');
    const wallContainer = document.getElementById('wall-container');
    const scoreElement = document.getElementById('score');
    const feedbackElement = document.getElementById('feedback');
    const questions = document.querySelectorAll('.question');
    const replayButton = document.getElementById('replay-button');
    const menuButton = document.getElementById('menu-button');
    let currentQuestionIndex = 0;
    let score = 0;
    const totalQuestions = 6;

    // Display the next question
    const showNextQuestion = () => {
        if (currentQuestionIndex < questions.length) {
            questions[currentQuestionIndex].style.display = "none";
            currentQuestionIndex++;
            if (currentQuestionIndex < questions.length) {
                questions[currentQuestionIndex].style.display = "block";
            }
        }
    };

    // Reset the game
    const resetGame = () => {
        currentQuestionIndex = 0;
        score = 0;
        scoreElement.textContent = score;
        feedbackElement.textContent = "";
        wallContainer.innerHTML = "";  // Reset the wall
        generateWall();  // Regenerate the bricks
        document.getElementById('replay-button').style.display = "none"; // Hide the Replay button
        document.getElementById('menu-button').style.display = "none"; // Hide the Back to Menu button
        showNextQuestion(); // Show the first question
    };

    // Generate the wall bricks
    const generateWall = () => {
        for (let i = 0; i < totalQuestions; i++) {
            const brick = document.createElement('div');
            brick.classList.add('brique');
            wallContainer.appendChild(brick);
        }
    };

    generateWall();

    // Check the answer and update the score
    const checkAnswer = (answer) => {
        const correctAnswers = ["B", "B", "C", "B", "A", "A"]; // Correct answers for each question
        const isCorrect = answer === correctAnswers[currentQuestionIndex];

        if (isCorrect) {
            score++;
            feedbackElement.textContent = "Correct answer!";
            wallContainer.children[score - 1].classList.add('correct');
        } else {
            feedbackElement.textContent = "Incorrect answer!";
            wallContainer.children[score].classList.add('incorrect');
        }

        // Update the score
        scoreElement.textContent = score;

        // Display the next question
        showNextQuestion();

        // Check whether all questions have been answered
        if (currentQuestionIndex === totalQuestions) {
            document.getElementById('replay-button').style.display = "inline-block";
            document.getElementById('menu-button').style.display = "inline-block";
        }
    };

    // Add click handlers to the answer buttons
    answerButtons.forEach(button => {
        button.addEventListener('click', () => {
            const answer = button.dataset.answer;
            checkAnswer(answer);
        });
    });

    // Attach a click handler to the Replay button
    replayButton.addEventListener('click', resetGame);
});
