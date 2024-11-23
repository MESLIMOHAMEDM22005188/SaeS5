// Liste d'emails fictive
const emails = [
    { id: 1, sender: "exemple1@mail.com", subject: "Gagnez une tablette", body: "Félicitations ! Vous avez gagné une tablette." },
    { id: 2, sender: "exemple2@mail.com", subject: "Problème de sécurité", body: "Attention aux liens suspects." },
    { id: 3, sender: "exemple3@mail.com", subject: "Formation phishing", body: "Inscrivez-vous à notre formation." }
];

// Fonction pour afficher la fenêtre d'email
function openEmailWindow() {
    document.getElementById('email-window').style.display = 'block';
    loadEmailTitles();
}

// Fonction pour fermer la fenêtre d'email
document.getElementById('close-email-window').addEventListener('click', () => {
    document.getElementById('email-window').style.display = 'none';
});

// Charger les titres d'emails
function loadEmailTitles() {
    const emailTitles = document.getElementById('email-titles');
    emailTitles.innerHTML = ''; // Réinitialiser
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
        <p><strong>De :</strong> ${email.sender}</p>
        <p><strong>Objet :</strong> ${email.subject}</p>
        <p>${email.body}</p>
    `;
}
