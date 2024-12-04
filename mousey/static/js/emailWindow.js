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
    localStorage.setItem('points', points);
}

function loadPoints() {
    const savedPoints = localStorage.getItem('points');
    points = savedPoints !== null ? parseInt(savedPoints, 10) : 0;
}

function updatePointsDisplay() {
    const pointsDisplay = document.querySelector('.points-display');
    pointsDisplay.textContent = `Points: ${points}`;
}


// Fonctions liées à la gestion des données

function loadEmails() {
    const savedEmails = JSON.parse(localStorage.getItem('emails'));
    if (savedEmails) {
        emails.length = 0;
        emails.push(...savedEmails);
    }
}

function saveEmails() {
    localStorage.setItem('emails', JSON.stringify(emails));
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


// Initialisation et gestion des événements

document.getElementById('close-email-window').addEventListener('click', closeEmailWindow);

document.addEventListener('DOMContentLoaded', () => {
    loadEmails();
    loadPoints();
    loadEmailTitles();
    updatePointsDisplay();
});

document.addEventListener('click', () => {
    document.querySelectorAll('.email-options.visible').forEach(menu => {
        menu.classList.remove('visible');
        menu.style.left = '';
        menu.style.top = '';
    });
});