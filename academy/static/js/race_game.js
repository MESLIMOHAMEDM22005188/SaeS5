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
    const speeds = { snail: 0.2, turtle: 0.5, hare: 0.8, cheetah: 1 }; // Speed in pixels per frame
    const cybermouseSpeed = 50; // Move forward for a correct answer
    const cybermousePenalty = 30; // Move backward for an incorrect answer
    const trackLength = 800; // Total track length


    const questions = [
    {
        question: "What is the role of a firewall in a network?",
        options: [
            { text: "Speed up the internet connection", correct: false },
            { text: "Block unauthorized traffic", correct: true },
            { text: "Assign IP addresses", correct: false }
        ]
    },
    {
        question: "Which protocol secures communications over the internet?",
        options: [
            { text: "HTTP", correct: false },
            { text: "HTTPS", correct: true },
            { text: "FTP", correct: false }
        ]
    },
    {
        question: "Which IP address belongs to a private network?",
        options: [
            { text: "192.168.1.1", correct: true },
            { text: "8.8.8.8", correct: false },
            { text: "172.32.0.1", correct: false }
        ]
    },
    {
        question: "Which device can segment a local network?",
        options: [
            { text: "A switch", correct: true },
            { text: "A router", correct: false },
            { text: "A modem", correct: false }
        ]
    },
    {
        question: "What is the role of a DNS server?",
        options: [
            { text: "Assign IP addresses", correct: false },
            { text: "Translate domain names into IP addresses", correct: true },
            { text: "Filter network traffic", correct: false }
        ]
    },
    {
        question: "Which command tests connectivity between two devices?",
        options: [
            { text: "ping", correct: true },
            { text: "tracert", correct: false },
            { text: "netstat", correct: false }
        ]
    },
    {
        question: "Which attack intercepts communications between two parties?",
        options: [
            { text: "Man-in-the-Middle", correct: true },
            { text: "Phishing", correct: false },
            { text: "DDoS", correct: false }
        ]
    },
    {
        question: "What is the length of an IPv6 address?",
        options: [
            { text: "32 bits", correct: false },
            { text: "64 bits", correct: false },
            { text: "128 bits", correct: true }
        ]
    },
    {
        question: "What is the main function of a router?",
        options: [
            { text: "Connect multiple networks", correct: true },
            { text: "Provide Wi-Fi", correct: false },
            { text: "Assign network ports", correct: false }
        ]
    },
    {
        question: "Which protocol dynamically assigns IP addresses?",
        options: [
            { text: "DNS", correct: false },
            { text: "DHCP", correct: true },
            { text: "ARP", correct: false }
        ]
    },
    {
        question: "What is the benefit of data encryption?",
        options: [
            { text: "Speed up packet transmission", correct: false },
            { text: "Protect data from interception", correct: true },
            { text: "Increase bandwidth", correct: false }
        ]
    },
    {
        question: "Which protocol is used to send email?",
        options: [
            { text: "POP3", correct: false },
            { text: "SMTP", correct: true },
            { text: "IMAP", correct: false }
        ]
    },
    {
        question: "What does NAT mean in networking?",
        options: [
            { text: "Network Access Transfer", correct: false },
            { text: "Network Address Translation", correct: true },
            { text: "New Address Type", correct: false }
        ]
    },
    {
        question: "What is the advantage of IPv6 over IPv4?",
        options: [
            { text: "Higher speed", correct: false },
            { text: "A larger address space", correct: true },
            { text: "Compatibility with all devices", correct: false }
        ]
    },
    {
        question: "How can a Wi-Fi network be secured?",
        options: [
            { text: "By using WPA3", correct: true },
            { text: "By disabling encryption", correct: false },
            { text: "By leaving access open", correct: false }
        ]
    },
    {
        question: "Which tool can analyze network traffic?",
        options: [
            { text: "Wireshark", correct: true },
            { text: "Excel", correct: false },
            { text: "Putty", correct: false }
        ]
    },
    {
        question: "What is the purpose of ICMP?",
        options: [
            { text: "Send email", correct: false },
            { text: "Diagnose and report network errors", correct: true },
            { text: "Assigner des adresses IP", correct: false }
        ]
    },
    {
        question: "Why use a VLAN?",
        options: [
            { text: "To reduce network congestion", correct: true },
            { text: "To increase internet speed", correct: false },
            { text: "To connect two Wi-Fi networks", correct: false }
        ]
    },
    {
        question: "Which protocol establishes a secure remote connection?",
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
        }, 50); // Update every 50 ms for smooth movement
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
            positions.cybermouse += cybermouseSpeed; // Move forward for a correct answer
        } else {
            positions.cybermouse = Math.max(0, positions.cybermouse - cybermousePenalty); // Move backward for an incorrect answer
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

        if (rank === 4) finishMessage.textContent = "Gold: You overtook all opponents!";
        else if (rank >= 3) finishMessage.textContent = "Silver: You overtook 3 animals!";
        else if (rank >= 2) finishMessage.textContent = "Bronze: You overtook 2 animals!";
        else finishMessage.textContent = "You lost! Try again!";

        optionsBox.innerHTML = '';

        // Show the Restart button
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

    // Initialize the race
    resetPositions();
    startRace();
    askQuestion();
});