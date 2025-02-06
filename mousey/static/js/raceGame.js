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
    {
        question: "Quel est le rôle d'un pare-feu dans un réseau ?",
        options: [
            { text: "Accélérer la connexion Internet", correct: false },
            { text: "Bloquer le trafic non autorisé", correct: true },
            { text: "Attribuer des adresses IP", correct: false }
        ]
    },
    {
        question: "Quel protocole est utilisé pour sécuriser les communications sur Internet ?",
        options: [
            { text: "HTTP", correct: false },
            { text: "HTTPS", correct: true },
            { text: "FTP", correct: false }
        ]
    },
    {
        question: "Quelle adresse IP appartient à un réseau privé ?",
        options: [
            { text: "192.168.1.1", correct: true },
            { text: "8.8.8.8", correct: false },
            { text: "172.32.0.1", correct: false }
        ]
    },
    {
        question: "Quel appareil permet de segmenter un réseau local ?",
        options: [
            { text: "Un commutateur (switch)", correct: true },
            { text: "Un routeur", correct: false },
            { text: "Un modem", correct: false }
        ]
    },
    {
        question: "Quel est le rôle d'un serveur DNS ?",
        options: [
            { text: "Attribuer des adresses IP", correct: false },
            { text: "Convertir les noms de domaine en adresses IP", correct: true },
            { text: "Filtrer le trafic réseau", correct: false }
        ]
    },
    {
        question: "Quelle commande permet de tester la connectivité entre deux appareils ?",
        options: [
            { text: "ping", correct: true },
            { text: "tracert", correct: false },
            { text: "netstat", correct: false }
        ]
    },
    {
        question: "Quel type d'attaque consiste à intercepter les communications entre deux parties ?",
        options: [
            { text: "Man-in-the-Middle", correct: true },
            { text: "Phishing", correct: false },
            { text: "DDoS", correct: false }
        ]
    },
    {
        question: "Quelle est la longueur d'une adresse IPv6 ?",
        options: [
            { text: "32 bits", correct: false },
            { text: "64 bits", correct: false },
            { text: "128 bits", correct: true }
        ]
    },
    {
        question: "Quelle est la fonction principale d'un routeur ?",
        options: [
            { text: "Relier plusieurs réseaux entre eux", correct: true },
            { text: "Fournir du Wi-Fi", correct: false },
            { text: "Attribuer des ports réseau", correct: false }
        ]
    },
    {
        question: "Quel protocole permet d'attribuer dynamiquement des adresses IP ?",
        options: [
            { text: "DNS", correct: false },
            { text: "DHCP", correct: true },
            { text: "ARP", correct: false }
        ]
    },
    {
        question: "Quel est l'avantage du chiffrement des données ?",
        options: [
            { text: "Accélérer la transmission des paquets", correct: false },
            { text: "Protéger les données contre l'interception", correct: true },
            { text: "Augmenter la bande passante", correct: false }
        ]
    },
    {
        question: "Quel protocole est utilisé pour envoyer des emails ?",
        options: [
            { text: "POP3", correct: false },
            { text: "SMTP", correct: true },
            { text: "IMAP", correct: false }
        ]
    },
    {
        question: "Que signifie NAT en réseau ?",
        options: [
            { text: "Network Access Transfer", correct: false },
            { text: "Network Address Translation", correct: true },
            { text: "New Address Type", correct: false }
        ]
    },
    {
        question: "Quel est l'avantage d'utiliser IPv6 par rapport à IPv4 ?",
        options: [
            { text: "Une meilleure vitesse", correct: false },
            { text: "Un plus grand espace d'adressage", correct: true },
            { text: "Une compatibilité avec tous les équipements", correct: false }
        ]
    },
    {
        question: "Comment un réseau Wi-Fi peut-il être sécurisé ?",
        options: [
            { text: "En utilisant WPA3", correct: true },
            { text: "En désactivant le chiffrement", correct: false },
            { text: "En laissant un accès ouvert", correct: false }
        ]
    },
    {
        question: "Quel outil permet d'analyser le trafic réseau ?",
        options: [
            { text: "Wireshark", correct: true },
            { text: "Excel", correct: false },
            { text: "Putty", correct: false }
        ]
    },
    {
        question: "Quel est l'objectif du protocole ICMP ?",
        options: [
            { text: "Envoyer des emails", correct: false },
            { text: "Diagnostiquer et signaler des erreurs réseau", correct: true },
            { text: "Assigner des adresses IP", correct: false }
        ]
    },
    {
        question: "Pourquoi utiliser un VLAN ?",
        options: [
            { text: "Pour réduire la congestion réseau", correct: true },
            { text: "Pour augmenter la vitesse Internet", correct: false },
            { text: "Pour connecter deux réseaux Wi-Fi", correct: false }
        ]
    },
    {
        question: "Quel protocole permet d'établir une connexion sécurisée à distance ?",
        options: [
            { text: "FTP", correct: false },
            { text: "SSH", correct: true },
            { text: "Telnet", correct: false }
        ]
    }
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