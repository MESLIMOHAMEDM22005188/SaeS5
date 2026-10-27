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
                { text: "Limited internet access", correct: false, explanation: "The main risk is security, not limited access." },
                { text: "Attaques de type 'man-in-the-middle'", correct: true, explanation: "Public Wi-Fi traffic can be intercepted by attackers." },
                { text: "High latency", correct: false, explanation: "High latency is not a security issue." }
            ]
        },
        {
            title: "Step 3: Home network",
            question: "Which configuration makes a home network safer?",
            options: [
                { text: "Disable the Wi-Fi password", correct: false, explanation: "This would make your network vulnerable to intrusion." },
                { text: "Enable MAC address filtering", correct: false, explanation: "MAC filtering alone is not enough to secure a network." },
                { text: "Change the router's default password", correct: true, explanation: "Changing default passwords reduces the risk of unauthorized access." }
            ]
        },
        {
            title: "Step 4: Authentication",
            question: "Which authentication method is recommended for Wi-Fi?",
            options: [
                { text: "Simple password", correct: false, explanation: "Simple passwords are easy to guess." },
                { text: "Strong password combined with WPA3", correct: true, explanation: "A strong password and WPA3 improve security." },
                { text: "No authentication", correct: false, explanation: "A connection without authentication exposes the network to intrusion." }
            ]
        },
        {
            title: "Step 5: Guest networks",
            question: "Why configure a guest network on a home router?",
            options: [
                { text: "To increase connection speed", correct: false, explanation: "This does not improve speed, but it does improve security." },
                { text: "To isolate guest devices from the main network", correct: true, explanation: "A guest network prevents guests from accessing devices on the main network." },
                { text: "To avoid changing the main password", correct: false, explanation: "This is not a valid reason to configure a guest network." }
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
            feedback.innerHTML = `<p style="color: green;">Correct answer! ${explanation}</p>`;
            currentStage++;
            setTimeout(() => {
                hideModal();
                showModal();
            }, 2000);
        } else {
            button.classList.add('incorrect');
            feedback.innerHTML = `<p style="color: red;">Incorrect answer. ${explanation}</p>`;
        }
    }

    function endGame() {
        const modalContent = document.createElement('div');
        modalContent.className = 'modal-content';
        modalContent.innerHTML = `
            <header>
                <span>Congratulations!</span>
            </header>
            <p>You completed the internet connection challenge!</p>
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
