// Variables

let points = 0;

const emails = [
    {
        id: 1,
        sender: "ruuqn44Jrf@gmiel.com",
        subject: "Gagnez une tablette Apple !",
        body: "Félicitations ! Vous avez été sélectionné parmis 100000 candidats pour gagner une tablette Apple. Cliquez ici pour retirer votre gain : <a href='http://win-free-apple-not-v1ru5.co'>http://win-free-apple-not-v1ru5.co</a>",
        isPhishing: true,
        reported: false
    },
    {
        id: 2,
        sender: "secretaire-cybermouse@gmiel.com",
        subject: "Attention : Problème de sécurité",
        body: "Bonjour,<br><br>De nombreux élèves ont été victimes de phishing récemment. Veuillez redoubler de vigilance et évitez au maximum les liens suspects.<br><br>Merci, la secrétaire.",
        isPhishing: false,
        reported: false
    },
    {
        id: 3,
        sender: "secretalre-cybermouse@gmiel.com",
        subject: "Formation : Apprendre à détecter le phishing",
        body: "Bonjour,<br><br>Voici le lien pour accéder à une formation sur le phishing : <a href='http://formation-phishing-1.com'>http://formation-phishing-1.com</a>",
        isPhishing: true,
        reported: false
    }
];

// Pour faire réapparaître les mails et mettre à 0 les points :
// saveEmails();
// savePoints();


// Fonctions liées à l'affichage des emails (UI/DOM)

function openEmailWindow() {
    document.getElementById('email-window').style.display = 'block';
    loadEmailTitles();
}

function closeEmailWindow() {
    document.getElementById('email-window').style.display = 'none';
}

function loadEmailTitles() {
    const emailTitles = document.getElementById('email-titles');
    emailTitles.innerHTML = '';

    emails.forEach(email => {
        const listItem = document.createElement('li');
        listItem.textContent = `${email.sender} - ${email.subject}`;
        listItem.setAttribute('data-id', email.id);

        if (email.reported) {
            listItem.style.backgroundColor = email.isPhishing ? 'green' : 'red';
        }

        listItem.addEventListener('click', () => displayEmailContent(email.id));
        emailTitles.appendChild(listItem);
    });
}

function displayEmailContent(emailId) {
    const email = emails.find(e => e.id === emailId);
    const emailContent = document.getElementById('email-content');
    emailContent.innerHTML = `
        <p class="email-Plus">
            <img src="/static/image/plusOption.png" class="plus-Option" onclick="openMoreOption(event, ${email.id})">
        </p>
        <p class="email-Sender"><strong>De :</strong> ${email.sender}</p>
        <p class="email-Object"><strong>Objet :</strong> ${email.subject}</p>
        <p>${email.body}</p>
        <div id="email-options-${email.id}" class="email-options">
            <button onclick="markAsUnread(${email.id})">Marquer comme non-lu</button>
            <button onclick="deleteEmail(${email.id})">Supprimer</button>
            <button onclick="reportEmail(${email.id})">Signaler</button>
        </div>
    `;

    // Gérer les clics sur les liens suspects
    const links = emailContent.querySelectorAll('a');
    links.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            event.stopImmediatePropagation();
            console.log('Lien cliqué !');
            if (email.isPhishing) {
                triggerPhishingPopups(emailId);
            } else {
                alert("Lien légitime. Aucune action nécessaire.");
            }
        });
    });
}


function triggerPhishingPopups(emailId) {
    if (document.querySelector('.hacked-message')) return;
    points -= 100;
    savePoints();

    document.body.style.pointerEvents = 'none';

    const popupContainer = document.createElement('div');
    popupContainer.classList.add('popup-container');
    document.body.appendChild(popupContainer);

    let delay = 500;
    const minDelay = 30;
    let count = 0;
    const maxPopups = 100;

    function getRandomPosition() {
        const top = Math.random() * 90 - 5;
        const left = Math.random() * 90 - 5;
        return { top: `${top}%`, left: `${left}%` };
    }

    function createPopup() {
        const popup = document.createElement('div');
        popup.classList.add('popup');
        const { top, left } = getRandomPosition();
        popup.style.top = top;
        popup.style.left = left;
        popup.innerHTML = `
            <h1>Piratage en cours...</h1>
            <p>Veuillez ne pas éteindre votre ordinateur.</p>
        `;
        popupContainer.appendChild(popup);

        delay = Math.max(minDelay, delay * 0.9);
        count++;

        if (count < maxPopups) {
            setTimeout(createPopup, delay);
        }
    }

    createPopup();

    setTimeout(() => {
        const blueScreen = document.createElement('div');
        blueScreen.style.position = 'fixed';
        blueScreen.style.top = '0';
        blueScreen.style.left = '0';
        blueScreen.style.width = '100vw';
        blueScreen.style.height = '100vh';
        blueScreen.style.backgroundImage = 'url("/static/image/bluescreen.png")';
        blueScreen.style.backgroundSize = 'cover';
        blueScreen.style.zIndex = '9999';
        blueScreen.classList.add('blue-screen');
        document.body.appendChild(blueScreen);

        setTimeout(() => {
            blueScreen.remove();
            popupContainer.remove();
            document.body.innerHTML = `
                <div class="hacked-message" style="text-align: center; padding: 50px;">
                    <h1>Session Rebootée</h1>
                    <p>Vous vous êtes fait hacker ! Ne cliquez pas sur des liens suspects.</p>
                    <p><strong>Indice :</strong> Vérifiez l'adresse email de l'expéditeur et l'URL.</p>
                    <button onclick="reloadSession()" style="padding: 10px 20px; font-size: 16px;">Réessayer</button>
                </div>
            `;
            document.body.style.pointerEvents = 'auto';
        }, 3000);
    }, 6800);
}

function reloadSession() {
    location.reload();
    updatePointsDisplay();
}


// Fonctions liées à la gestion des emails

function reportEmail(emailId) {
    const email = emails.find(e => e.id === emailId);
    const emailElement = document.querySelector(`[data-id="${emailId}"]`);

    if (email.reported) {
        alert("Cet email a déjà été signalé.");
        return;
    }

    email.reported = true;

    if (email.isPhishing) {
        emailElement.style.backgroundColor = 'green';
        alert("Bravo ! Vous avez signalé un email de phishing. Vous pouvez maintenant le supprimer.");
        points += 100;
    } else {
        emailElement.style.backgroundColor = 'red';
        alert("Vous avez signalé un vrai email. Votre crédibilité diminue.");
        points -= 100;
    }

    savePoints();
    saveEmails();
    updatePointsDisplay();
    checkAllPhishingReported();
}

function deleteEmail(emailId) {
    const emailIndex = emails.findIndex(e => e.id === emailId);

    if (emails[emailIndex].reported && emails[emailIndex].isPhishing) {
        emails.splice(emailIndex, 1);
        const emailElement = document.querySelector(`[data-id="${emailId}"]`);
        emailElement.remove();
        document.getElementById('email-content').innerHTML = '';
        alert("L'email a été supprimé avec succès.");
        saveEmails();
    } else if (emails[emailIndex].reported && !emails[emailIndex].isPhishing) {
        alert("Cet email est légitime. Vous ne pouvez pas le supprimer.");
    } else {
        alert("Vous devez d'abord signaler correctement cet email avant de pouvoir le supprimer.");
    }
}


// Fonctions liées aux points

function savePoints() {
    sessionStorage.setItem('points', points);
}

function loadPoints() {
    const savedPoints = sessionStorage.getItem('points');
    points = savedPoints !== null ? parseInt(savedPoints, 10) : 0;
}

function updatePointsDisplay() {
    const pointsDisplay = document.querySelector('.points-display');
    pointsDisplay.textContent = `Points: ${points}`;
}


// Fonctions liées à la gestion des données

function loadEmails() {
    const savedEmails = JSON.parse(sessionStorage.getItem('emails'));
    if (savedEmails) {
        emails.length = 0;
        emails.push(...savedEmails);
    }
}

function saveEmails() {
    sessionStorage.setItem('emails', JSON.stringify(emails));
}


// Gestion des options supplémentaires

function openMoreOption(event, emailId) {
    event.stopPropagation();
    const options = document.getElementById(`email-options-${emailId}`);

    if (options.classList.contains('visible')) {
        options.classList.remove('visible');
        options.style.left = '';
        options.style.top = '';
        return;
    }

    const rect = event.target.getBoundingClientRect();

    options.style.position = 'fixed';
    options.style.left = `${rect.left - options.offsetWidth - 135}px`;
    options.style.top = `${rect.bottom + 3}px`;
    options.classList.add('visible');
}


// Gestion reussite à signaler les mails de phishing

function checkAllPhishingReported() {
    const allReported = emails.every(email => !email.isPhishing || email.reported);
    if (allReported) {
        sendCongratulationsMail();
    }
}

function sendCongratulationsMail() {
    const congratulationsEmail = {
        id: 4,
        sender: "admin@cybersecure.com",
        subject: "Félicitations pour votre vigilance !",
        body: `
            Bravo, vous avez signalé tous les emails de phishing avec succès !<br>
            Vous pouvez maintenant passer au quiz final pour tester vos connaissances.<br>
            Cliquez ici pour commencer : <a href="browser/quiz" onclick="openFirefoxWindow()">Commencer le quiz</a>
        `,
        read: false,
        isPhishing: false,
        reported: false
    };

    emails.push(congratulationsEmail);
    saveEmails();
    loadEmailTitles();
}


// Initialisation et gestion des événements

document.getElementById('close-email-window').addEventListener('click', closeEmailWindow);

document.addEventListener('DOMContentLoaded', () => {
    loadEmails();
    loadPoints();
    loadEmailTitles();
    updatePointsDisplay();

    setTimeout(() => {
        const phishingMessage = document.getElementById('phishing-message');
        phishingMessage.style.display = 'block';
    }, 30000);
});


document.addEventListener('click', () => {
    document.querySelectorAll('.email-options.visible').forEach(menu => {
        menu.classList.remove('visible');
        menu.style.left = '';
        menu.style.top = '';
    });
});