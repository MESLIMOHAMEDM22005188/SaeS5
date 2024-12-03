//liste des emails
const emails = [
    {
        id: 1,
        sender: "ruuqn44Jrf@gmiel.com",
        subject: "Gagnez une tablette Apple !",
        body: "Félicitations ! Vous avez été sélectionné parmis 100000 candidats pour gagner une tablette Apple. Cliquez ici pour retirer votre gain : <a href='http://win-free-apple-not-v1ru5.co'>http://win-free-apple-not-v1ru5.co</a>",
    },
    {
        id: 2,
        sender: "secretaire-cybermouse@gmiel.com",
        subject: "Attention : Problème de sécurité",
        body: "Bonjour,<br><br>De nombreux élèves ont été victimes de phishing récemment. Veuillez redoubler de vigilence et évitez au maximum les liens suspects.<br><br>Merci, la secrétaire."
    },
    {
        id: 3,
        sender: "secreta1re-cybermouse@gmiel.com",
        subject: "Formation : Apprendre a détecter le phishing",
        body: "Bonjour,<br><br>Voici le lien pour accéder à une formation sur le phishing : <a href='http://formation-phishing-1.com'>http://formation-phishing-1.com</a>"
    }
]

function openEmailWindow() {
    document.getElementById('email-window').style.display = 'block';
    loadEmailTitles();
}

//femer fenêtre
document.getElementById('close-email-window').addEventListener('click', () => {
    document.getElementById('email-window').style.display = 'none';
});

function loadEmailTitles() {
    const emailTitles = document.getElementById('email-titles');
    emailTitles.innerHTML = '';
    emails.forEach(email => {
        const listItem = document.createElement('li');
        listItem.textContent = `${email.sender} - ${email.subject}`;
        listItem.setAttribute('data-id', email.id);
        listItem.addEventListener('click', () => displayEmailContent(email.id));
        emailTitles.appendChild(listItem);
    });
}

// Afficher le contenu d'un email
function displayEmailContent(emailId) {
    const email = emails.find(e => e.id === emailId);
    const emailContent = document.getElementById('email-content');
    emailContent.innerHTML = `
        <p class="email-Plus">
            <img src="/static/image/plusOption.png" class="plus-Option" onclick="openMoreOption(event)">
        </p>
        <p class="email-Sender"><strong>De :</strong> ${email.sender}</p>
        <p class="email-Object"><strong>Objet :</strong> ${email.subject}</p>
        <p>${email.body}</p>
    `;
}