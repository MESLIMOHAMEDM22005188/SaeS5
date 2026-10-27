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

    // Fonction pour afficher la prochaine question
    const showNextQuestion = () => {
        if (currentQuestionIndex < questions.length) {
            questions[currentQuestionIndex].style.display = "none";
            currentQuestionIndex++;
            if (currentQuestionIndex < questions.length) {
                questions[currentQuestionIndex].style.display = "block";
            }
        }
    };

    // Fonction pour réinitialiser le jeu
    const resetGame = () => {
        currentQuestionIndex = 0;
        score = 0;
        scoreElement.textContent = score;
        feedbackElement.textContent = "";
        wallContainer.innerHTML = "";  // Réinitialiser le mur
        generateWall();  // Régénérer les briques
        document.getElementById('replay-button').style.display = "none"; // Masquer le bouton "Rejouer"
        document.getElementById('menu-button').style.display = "none"; // Masquer le bouton "Retourner au Menu"
        showNextQuestion(); // Afficher la première question
    };

    // Générer les briques du mur
    const generateWall = () => {
        for (let i = 0; i < totalQuestions; i++) {
            const brick = document.createElement('div');
            brick.classList.add('brique');
            wallContainer.appendChild(brick);
        }
    };

    generateWall();

    // Vérifier la réponse et mettre à jour le score
    const checkAnswer = (answer) => {
        const correctAnswers = ["B", "B", "C", "B", "A", "A"]; // Les bonnes réponses de chaque question
        const isCorrect = answer === correctAnswers[currentQuestionIndex];

        if (isCorrect) {
            score++;
            feedbackElement.textContent = "Bonne réponse!";
            wallContainer.children[score - 1].classList.add('correct');
        } else {
            feedbackElement.textContent = "Mauvaise réponse!";
            wallContainer.children[score].classList.add('incorrect');
        }

        // Mise à jour du score
        scoreElement.textContent = score;

        // Afficher la prochaine question
        showNextQuestion();

        // Si toutes les questions ont été répondues
        if (currentQuestionIndex === totalQuestions) {
            document.getElementById('replay-button').style.display = "inline-block";
            document.getElementById('menu-button').style.display = "inline-block";
        }
    };

    // Ajouter un événement au clic sur les boutons de réponse
    answerButtons.forEach(button => {
        button.addEventListener('click', () => {
            const answer = button.dataset.answer;
            checkAnswer(answer);
        });
    });

    // Ajouter un événement au clic sur le bouton "Rejouer"
    replayButton.addEventListener('click', resetGame);
});
