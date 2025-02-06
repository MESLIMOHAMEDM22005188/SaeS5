document.addEventListener('DOMContentLoaded', () => {
    const modalWindow = document.getElementById('modalWindow');
    const internetIcon = document.getElementById('internetIcon');
    let currentStage = 0;

    if (!modalWindow || !internetIcon) {
        console.error('Élément(s) introuvable(s) dans le DOM.');
        return;
    }


    const stages = [
        {
            title: "Étape 1 : Sécurité Wi-Fi",
            question: "Quel protocole Wi-Fi offre le meilleur niveau de sécurité ?",
            options: [
                { text: "WEP", correct: false, explanation: "WEP est obsolète et présente de nombreuses failles de sécurité." },
                { text: "WPA", correct: false, explanation: "WPA est une amélioration, mais WPA2 ou WPA3 sont plus sûrs." },
                { text: "WPA3", correct: true, explanation: "WPA3 est le protocole le plus sécurisé actuellement disponible." }
            ]
        },
        {
            title: "Étape 2 : Connexion publique",
            question: "Quel est le principal risque d'utiliser une connexion Wi-Fi publique ?",
            options: [
                { text: "Accès limité à Internet", correct: false, explanation: "Le risque principal n'est pas la limitation de l'accès, mais l'insécurité." },
                { text: "Attaques de type 'man-in-the-middle'", correct: true, explanation: "Les connexions Wi-Fi publiques peuvent être interceptées par des attaquants." },
                { text: "Temps de latence élevé", correct: false, explanation: "Un temps de latence élevé n'est pas un problème de sécurité." }
            ]
        },
        {
            title: "Étape 3 : Réseau domestique",
            question: "Quelle configuration rend un réseau domestique plus sûr ?",
            options: [
                { text: "Désactiver le mot de passe Wi-Fi", correct: false, explanation: "Cela rendrait votre réseau vulnérable aux intrusions." },
                { text: "Activer le filtrage d'adresses MAC", correct: false, explanation: "Le filtrage MAC n'est pas suffisant pour protéger un réseau." },
                { text: "Changer le mot de passe par défaut du routeur", correct: true, explanation: "Changer les mots de passe par défaut réduit les risques d'accès non autorisé." }
            ]
        },
        {
            title: "Étape 4 : Authentification",
            question: "Quel type d'authentification est recommandé pour une connexion Wi-Fi ?",
            options: [
                { text: "Mot de passe simple", correct: false, explanation: "Les mots de passe simples sont faciles à deviner." },
                { text: "Mot de passe complexe combiné à WPA3", correct: true, explanation: "Un mot de passe complexe et WPA3 renforcent la sécurité." },
                { text: "Aucune authentification", correct: false, explanation: "Une connexion sans authentification expose le réseau à des intrusions." }
            ]
        },
        {
            title: "Étape 5 : Réseaux invités",
            question: "Pourquoi configurer un réseau invité sur un routeur domestique ?",
            options: [
                { text: "Pour augmenter la vitesse de la connexion", correct: false, explanation: "Cela n'améliore pas la vitesse, mais la sécurité." },
                { text: "Pour isoler les appareils des invités du réseau principal", correct: true, explanation: "Un réseau invité empêche les invités d'accéder aux appareils sur le réseau principal." },
                { text: "Pour éviter de changer le mot de passe principal", correct: false, explanation: "Ce n'est pas une raison valable pour configurer un réseau invité." }
            ]
        }
    ];


    function createModalContent(stageIndex) {
        const stage = stages[stageIndex];
        const modalContent = document.createElement('div');
        modalContent.className = 'modal-content';
        modalContent.innerHTML = `
            <header>
                <span>${stage.title}</span>
                <button class="close-btn" onclick="hideModal()">×</button>
            </header>
            <p>${stage.question}</p>
            <div class="options">
                ${stage.options
                    .map((option, index) => `
                        <button class="option" data-correct="${option.correct}" data-explanation="${option.explanation}">
                            ${option.text}
                        </button>
                    `)
                    .join("")}
            </div>
            <p id="feedback"></p>
        `;
        modalWindow.innerHTML = '';
        modalWindow.appendChild(modalContent);

        const buttons = modalContent.querySelectorAll('.option');
        buttons.forEach((button) => {
            button.addEventListener('click', (event) => checkAnswer(event, stageIndex));
        });
    }

    function showModal() {
        if (currentStage < stages.length) {
            createModalContent(currentStage);
            modalWindow.classList.remove('hidden');
        } else {
            endGame();
        }
    }

    function hideModal() {
        modalWindow.classList.add('hidden');
    }

    function checkAnswer(event, stageIndex) {
        const button = event.target.closest('.option');
        const isCorrect = button.getAttribute('data-correct') === 'true';
        const explanation = button.getAttribute('data-explanation');
        const feedback = document.getElementById('feedback');

        if (isCorrect) {
            button.classList.add('correct');
            feedback.innerHTML = `<p style="color: green;">Bonne réponse ! ${explanation}</p>`;
            currentStage++;
            setTimeout(() => {
                hideModal();
                showModal();
            }, 2000);
        } else {
            button.classList.add('incorrect');
            feedback.innerHTML = `<p style="color: red;">Mauvaise réponse. ${explanation}</p>`;
        }
    }

    function endGame() {
        const modalContent = document.createElement('div');
        modalContent.className = 'modal-content';
        modalContent.innerHTML = `
            <header>
                <span>Félicitations !</span>
            </header>
            <p>Vous avez complété le défi des connexions Internet !</p>
            <p>Redirection en cours...</p>
        `;
        modalWindow.innerHTML = '';
        modalWindow.appendChild(modalContent);
        modalWindow.classList.remove('hidden');

        setTimeout(() => {
            window.location.href = "/levelTwo";
        }, 3000);
    }

    internetIcon.addEventListener('click', showModal);
});
