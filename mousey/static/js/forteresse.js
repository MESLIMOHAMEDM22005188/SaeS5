// Sélection des éléments DOM
const submitBtn = document.getElementById('submitBtn');
const passwordInput = document.getElementById('password');
const feedback = document.getElementById('feedback');

// Parties de la forteresse
const porte = document.getElementById('porte'); // Porte
const tourDroite = document.getElementById('tourDroite'); // Tour droite
const tourGauche = document.getElementById('tourGauche'); // Tour gauche

// Modals et boutons de contrôle
const startModal = document.getElementById('startModal');
const successModal = document.getElementById('successModal');
const startBtn = document.getElementById('startBtn');

const closeStart = document.getElementById('closeStart');
const closeSuccess = document.getElementById('closeSuccess');

// Fonction pour évaluer la force du mot de passe
function evaluatePassword(password) {
    let score = 0;

    // Critères de force
    if (password.length >= 8) score++; // Longueur minimale
    if (/[A-Z]/.test(password)) score++; // Contient une majuscule
    if (/[a-z]/.test(password)) score++; // Contient une minuscule
    if (/[0-9]/.test(password)) score++; // Contient un chiffre
    if (/[\W]/.test(password)) score++; // Contient un caractère spécial

    // Retourner le niveau de force
    if (score <= 2) return 'weak';
    if (score === 3 || score === 4) return 'medium';
    if (score === 5) return 'strong';
}

// Fonction pour réinitialiser la forteresse
function resetFortress() {
    // Ajouter la classe 'close-ico' pour cacher les parties
    porte.querySelector('img').classList.add('close-ico');
    tourDroite.querySelector('img').classList.add('close-ico');
    tourGauche.querySelector('img').classList.add('close-ico');
}

// Fonction pour renforcer la forteresse
function reinforceFortress(level) {
    // Afficher les parties en fonction du niveau
    if (level === 'medium') {
        porte.querySelector('img').classList.remove('close-ico'); // Afficher la porte
    } else if (level === 'strong') {
        porte.querySelector('img').classList.remove('close-ico'); // Afficher la porte
        tourDroite.querySelector('img').classList.remove('close-ico'); // Afficher la tour droite
        tourGauche.querySelector('img').classList.remove('close-ico'); // Afficher la tour gauche
    }
}

// Gestion de l'événement pour démarrer le jeu
startBtn.addEventListener('click', () => {
    startModal.classList.add('hidden');
});

// Gestion de l'événement pour fermer la fenêtre de départ
closeStart.addEventListener('click', () => {
    startModal.classList.add('hidden');
});

// Gestion de l'événement pour fermer la fenêtre de succès
closeSuccess.addEventListener('click', () => {
    successModal.classList.add('hidden');
});

// Gestion de l'événement de clic sur le bouton "Renforcer la Forteresse"
submitBtn.addEventListener('click', () => {
    const password = passwordInput.value.trim();

    // Vérification si le mot de passe est vide
    if (password === '') {
        feedback.textContent = 'Veuillez entrer un mot de passe.';
        feedback.className = '';
        return;
    }

    // Évaluer la force du mot de passe
    const strength = evaluatePassword(password);

    // Réinitialiser la forteresse avant de renforcer
    resetFortress();

    // Renforcer la forteresse en fonction de la force
    reinforceFortress(strength);

    // Afficher le feedback
    if (strength === 'weak') {
        feedback.textContent = 'Mot de passe faible. La forteresse est vulnérable !';
        feedback.className = 'weak';
    } else if (strength === 'medium') {
        feedback.textContent = 'Mot de passe moyen. La porte est renforcée.';
        feedback.className = 'medium';
    } else if (strength === 'strong') {
        feedback.textContent = 'Mot de passe fort. La forteresse est totalement protégée !';
        feedback.className = 'strong';

        // Afficher le modal de réussite
        successModal.classList.remove('hidden');
    }
});
