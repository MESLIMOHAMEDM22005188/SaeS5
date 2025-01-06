document.getElementById("open-email-window").addEventListener("click", function () {
    const emailWindow = document.getElementById("email-window");
    emailWindow.style.display = "block";
});

document.getElementById("close-email-window").addEventListener("click", function () {
    const emailWindow = document.getElementById("email-window");
    emailWindow.style.display = "none";
});

const emails = [
    {
        subject: "Urgent : Mise à jour obligatoire de votre compte RH",
        content: "Bonjour,\n\nVotre compte RH nécessite une mise à jour immédiate..."
    },
    {
        subject: "Mise à jour de votre profil RH",
        content: "Bonjour monsieur Sanchez,\n\nDans le cadre de la mise à jour..."
    },
    {
        subject: "Félicitations pour votre excellent travail !",
        content: "Bonjour Rick Sanchez,\n\nJe tiens à vous féliciter pour votre engagement..."
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
