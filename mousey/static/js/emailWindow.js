function openEmailWindow() {
    const emailWindow = document.getElementById("email-window");
    emailWindow.style.display = "block";
}
document.getElementById("close-email-window").addEventListener("click", function () {
    const emailWindow = document.getElementById("email-window");
    emailWindow.style.display = "none";
});
const emails = [
    { subject: "...", content: "Bonjour, merci d'avoir choisi Outlook." },
    { subject: "Mise à jour de votre compte", content: "Votre compte a été mis à jour avec succès." },
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