document.addEventListener('DOMContentLoaded', () => {
    const modalWindow = document.getElementById('modalWindow');
    const internetIcon = document.getElementById('internetIcon');
    let currentStage = 0;

    if (!modalWindow || !internetIcon) {
        console.error('Required element(s) not found in the DOM.');
        return;
    }


    const stages = [
        {
            title: "Step 1: Wi-Fi security",
            question: "Which Wi-Fi protocol offers the strongest security?",
            options: [
                { text: "WEP", correct: false, explanation: "WEP is obsolete and has many security vulnerabilities." },
                { text: "WPA", correct: false, explanation: "WPA is an improvement, but WPA2 or WPA3 are safer." },
                { text: "WPA3", correct: true, explanation: "WPA3 is currently the most secure option." }
            ]
        },
        {
            title: "Step 2: Public Wi-Fi",
            question: "What is the main risk of using public Wi-Fi?",
            options: [
                { text: "Accès limité à Internet", correct: false, explanation: "The main risk is security, not limited access." },
                { text: "Attaques de type 'man-in-the-middle'", correct: true, explanation: "Public Wi-Fi traffic can be intercepted by attackers." },
                { text: "Temps de latence élevé", correct: false, explanation: "High latency is not a security issue." }
            ]
        },
        {
            title: "Step 3: Home network",
            question: "Which configuration makes a home network safer?",
            options: [
                { text: "Disable the Wi-Fi password", correct: false, explanation: "This would make your network vulnerable to intrusion." },
                { text: "Activer le filtrage d'adresses MAC", correct: false, explanation: "Le filtrage MAC n'est pas suffisant pour protéger un réseau." },
                { text: "Change the router's default password", correct: true, explanation: "Changing default passwords reduces the risk of unauthorized access." }
            ]
        },
        {
            title: "Step 4: Authentication",
            question: "Which authentication method is recommended for Wi-Fi?",
            options: [
                { text: "Simple password", correct: false, explanation: "Simple passwords are easy to guess." },
                { text: "Strong password combined with WPA3", correct: true, explanation: "A strong password and WPA3 improve security." },
                { text: "Aucune authentification", correct: false, explanation: "Une connexion sans authentification expose le réseau à des intrusions." }
            ]
        },
        {
            title: "Step 5: Guest networks",
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
