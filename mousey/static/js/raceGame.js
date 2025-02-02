document.addEventListener('DOMContentLoaded', () => {
    const cybermouse = document.getElementById('cybermouse');
    const snail = document.getElementById('snail');
    const turtle = document.getElementById('turtle');
    const hare = document.getElementById('hare');
    const cheetah = document.getElementById('cheetah');
    const questionBox = document.getElementById('question');
    const optionsBox = document.getElementById('options');
    const finishMessage = document.getElementById('finish-message');
    const restartButton = document.getElementById('restart-button');

    let positions = { cybermouse: 0, snail: 0, turtle: 0, hare: 0, cheetah: 0 };
    const speeds = { snail: 0.2, turtle: 0.5, hare: 0.8, cheetah: 1 }; // Vitesse en pixels par frame
    const cybermouseSpeed = 50; // Avance pour une bonne réponse
    const cybermousePenalty = 30; // Recul pour une mauvaise réponse
    const trackLength = 800; // Longueur totale de la piste


    const questions = [
        { question: "Quel protocole Wi-Fi est le plus sécurisé ?", options: [ { text: "WEP", correct: false }, { text: "WPA2", correct: true }, { text: "Aucun", correct: false } ] },
        { question: "Quel est le risque principal d'un Wi-Fi public ?", options: [ { text: "Temps de latence", correct: false }, { text: "Man-in-the-middle", correct: true }, { text: "Pas d'accès", correct: false } ] },
        { question: "Pourquoi utiliser un VPN sur un Wi-Fi public ?", options: [ { text: "Pour contourner les pare-feu", correct: false }, { text: "Pour sécuriser les données", correct: true }, { text: "Pour accélérer la vitesse", correct: false } ] },
        { question: "Que signifie WPA dans WPA2 ?", options: [ { text: "Wireless Protected Access", correct: true }, { text: "Wide Public Access", correct: false }, { text: "Wireless Public Access", correct: false } ] },
        { question: "Quel protocole est obsolète pour le Wi-Fi ?", options: [ { text: "WEP", correct: true }, { text: "WPA3", correct: false }, { text: "WPA2", correct: false } ] },
        { question: "Un mot de passe Wi-Fi doit contenir ?", options: [ { text: "Seulement des chiffres", correct: false }, { text: "Une combinaison de lettres, chiffres et symboles", correct: true }, { text: "Juste des lettres", correct: false } ] },
        { question: "Qu'est-ce qu'un SSID ?", options: [ { text: "Le nom du réseau Wi-Fi", correct: true }, { text: "Un protocole de sécurité", correct: false }, { text: "Une adresse IP", correct: false } ] },
        { question: "Que faire pour sécuriser votre réseau Wi-Fi ?", options: [ { text: "Désactiver le chiffrement", correct: false }, { text: "Changer le mot de passe par défaut", correct: true }, { text: "Utiliser un réseau ouvert", correct: false } ] },
        { question: "Pourquoi désactiver la diffusion du SSID ?", options: [ { text: "Pour rendre le réseau invisible", correct: true }, { text: "Pour accélérer le Wi-Fi", correct: false }, { text: "Pour permettre plus d'appareils", correct: false } ] },
        { question: "Qu'est-ce qu'un Wi-Fi ouvert ?", options: [ { text: "Un réseau sans mot de passe", correct: true }, { text: "Un réseau sécurisé", correct: false }, { text: "Un réseau rapide", correct: false } ] },
        { question: "Quelle fréquence Wi-Fi est plus rapide ?", options: [ { text: "2.4 GHz", correct: false }, { text: "5 GHz", correct: true }, { text: "1 GHz", correct: false } ] },
        { question: "Pourquoi utiliser WPA3 au lieu de WPA2 ?", options: [ { text: "Pour une meilleure sécurité", correct: true }, { text: "Pour économiser de l'énergie", correct: false }, { text: "Pour plus de vitesse", correct: false } ] },
        { question: "Comment éviter les attaques sur votre Wi-Fi ?", options: [ { text: "Utiliser des mots de passe faibles", correct: false }, { text: "Activer un chiffrement fort comme WPA2", correct: true }, { text: "Désactiver le chiffrement", correct: false } ] },
        { question: "Quelle méthode est utilisée par WPA2 pour sécuriser les données ?", options: [ { text: "Chiffrement AES", correct: true }, { text: "Chiffrement DES", correct: false }, { text: "Aucune", correct: false } ] },
        { question: "Quelle est une bonne pratique pour votre routeur ?", options: [ { text: "Changer régulièrement le mot de passe", correct: true }, { text: "Désactiver le pare-feu", correct: false }, { text: "Garder les paramètres par défaut", correct: false } ] },
        { question: "Que fait un pare-feu sur un réseau Wi-Fi ?", options: [ { text: "Bloque les accès non autorisés", correct: true }, { text: "Augmente la vitesse du réseau", correct: false }, { text: "Désactive les périphériques", correct: false } ] },
        { question: "Comment détecter un réseau non sécurisé ?", options: [ { text: "Il nécessite un mot de passe", correct: false }, { text: "Il ne nécessite pas de mot de passe", correct: true }, { text: "Il est plus rapide", correct: false } ] },
        { question: "Quel est le danger d'utiliser des hotspots publics ?", options: [ { text: "Ils sont coûteux", correct: false }, { text: "Vos données peuvent être interceptées", correct: true }, { text: "Ils sont lents", correct: false } ] },
        { question: "Quel outil peut améliorer la sécurité d'un réseau Wi-Fi ?", options: [ { text: "Un VPN", correct: true }, { text: "Un réseau ouvert", correct: false }, { text: "Aucun mot de passe", correct: false } ] },
    ];

   let currentQuestion = 0;
function restartGame() {
        currentQuestion = 0;
        resetPositions();
        finishMessage.textContent = '';
        askQuestion();
    }
        restartButton.addEventListener('click', restartGame);

    function resetPositions() {
     positions = { cybermouse: -330, snail: -330, turtle: -330, hare: -330, cheetah: -330 };
        updatePositions();
    }

    function startRace() {
        setInterval(() => {
            moveAnimals();
            updatePositions();
            checkIfRaceFinished();
        }, 50); // Mise à jour toutes les 50ms pour un mouvement fluide
    }

    function askQuestion() {
        if (currentQuestion >= questions.length) return endRace();
        const q = questions[currentQuestion];
        questionBox.textContent = q.question;
        optionsBox.innerHTML = '';
        q.options.forEach((opt) => {
            const button = document.createElement('button');
            button.textContent = opt.text;
            button.onclick = () => checkAnswer(opt.correct);
            optionsBox.appendChild(button);
        });
    }

    function checkAnswer(correct) {
        if (correct) {
            positions.cybermouse += cybermouseSpeed; // Avance pour une bonne réponse
        } else {
            positions.cybermouse = Math.max(0, positions.cybermouse - cybermousePenalty); // Recul pour une mauvaise réponse
        }
        currentQuestion++;
        askQuestion();
    }

    function moveAnimals() {
        positions.snail += speeds.snail;
        positions.turtle += speeds.turtle;
        positions.hare += speeds.hare;
        positions.cheetah += speeds.cheetah;
    }

    function updatePositions() {
        cybermouse.style.transform = `translateX(${positions.cybermouse}px)`;
        snail.style.transform = `translateX(${positions.snail}px)`;
        turtle.style.transform = `translateX(${positions.turtle}px)`;
        hare.style.transform = `translateX(${positions.hare}px)`;
        cheetah.style.transform = `translateX(${positions.cheetah}px)`;
    }

    function checkIfRaceFinished() {
        if (positions.cybermouse >= trackLength) {
            endRace();
        }
    }

    function endRace() {
        let rank = 0;
        if (positions.cybermouse > positions.cheetah) rank++;
        if (positions.cybermouse > positions.hare) rank++;
        if (positions.cybermouse > positions.turtle) rank++;
        if (positions.cybermouse > positions.snail) rank++;

        if (rank === 4) finishMessage.textContent = "Or : Vous avez dépassé tous les animaux !";
        else if (rank >= 3) finishMessage.textContent = "Argent : Vous avez dépassé 3 animaux !";
        else if (rank >= 2) finishMessage.textContent = "Bronze : Vous avez dépassé 2 animaux !";
        else finishMessage.textContent = "Vous avez perdu ! Essayez encore !";

        optionsBox.innerHTML = '';

        // Afficher le bouton "Restart"
        const restartButton = document.createElement('button');
        restartButton.textContent = "Restart";
        restartButton.className = "restart-button";
        restartButton.onclick = restartGame;
        finishMessage.appendChild(restartButton);
    }

    function restartGame() {
        currentQuestion = 0;
        resetPositions();
        finishMessage.textContent = '';
        askQuestion();
    }

    // Initialiser la course
    resetPositions();
    startRace();
    askQuestion();
});