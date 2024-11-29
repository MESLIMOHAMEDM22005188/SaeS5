function openEmailWindow() {
    const emailWindow = document.getElementById("email-window");
    emailWindow.style.display = "block";
}
document.getElementById("close-email-window").addEventListener("click", function () {
    const emailWindow = document.getElementById("email-window");
    emailWindow.style.display = "none";
});

const emails = [
    {
        subject: "Urgent : Mise à jour obligatoire de votre compte RH",
        content: "Bonjour,\n\nVotre compte RH nécessite une mise à jour immédiate pour se conformer aux
        "nouvelles réglementations. Veuillez cliquer sur le lien ci-dessous pour valider vos informations
        ":\n\n[http://faux-site-rh.com/mise-a-jour]\n\nSi vous ne le faites pas sous 24 heures, votre compte sera suspendu.
        "\n\nCordialement,\nÉquipe RH"
    },
    {
        subject: "Mise à jour de votre profil RH",
        content: "Bonjour monsieur Sanchez,\n\nDans le cadre de la mise à jour de nos données internes,
        "nous vous invitons à vérifier et, si nécessaire, à actualiser vos informations personnelles via votre portail RH.
        "\n\nVous pouvez accéder à votre compte en toute sécurité à l'adresse suivante :
        "\n[https://intranet.entreprise.com/moncompte]\n\nSi vous avez des questions ou rencontrez des problèmes,
        "n'hésitez pas à nous contacter à cette adresse : rh@entreprise.com.\n\nCordialement,\n[Nom et prénom]\nResponsable RH\n[Entreprise]"
    },
    {
        subject: "Félicitations pour votre excellent travail !",
        content: "Bonjour Rick Sanchez,\n\nJe tiens à vous féliciter pour votre engagement et votre contribution exceptionnelle
        "au projet NavalTravel. Votre travail a été remarqué et apprécié par l’ensemble de l’équipe dirigeante.\n
        "\nContinuez sur cette lancée, votre implication est précieuse pour l’entreprise.\n\nCordialement,\n Alexis Delin\n
        "Directeur Général\n LeviatorGroup"
    }
];

function loadEmails() {
    const emailList = document.getElementById("email-titles");
    emails.forEach((email, index) => {
        const li = document.createElement("li");
        li.textContent = email.subject;
        li.classList.add("email-item");
        li.onclick = () => displayEmailContent(index);
        emailList.appendChild(li);
    });
}

function displayEmailContent(index) {
    const emailContent = document.getElementById("email-content");
    emailContent.textContent = emails[index].content;
}

document.addEventListener("DOMContentLoaded", loadEmails);