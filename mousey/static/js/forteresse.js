document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submitBtn');
    const passwordInput = document.getElementById('password');
    const feedback = document.getElementById('feedback');
    const togglePassword = document.getElementById('togglePassword');

    const startModal = document.getElementById('startModal');
    const successModal = document.getElementById('successModal');
    const startBtn = document.getElementById('startBtn');
    const closeStart = document.getElementById('closeStart');
    const closeSuccess = document.getElementById('closeSuccess');

    const modal = document.getElementById('gameModal');
    const closeModalBtn = document.getElementById('closeModal');
    const startGameBtn = document.getElementById('startGameBtn');

    const porte = document.querySelector('#porte img');
    const tourDroite = document.querySelector('#tourDroite img');
    const tourGauche = document.querySelector('#tourGauche img');

    // Toggle mot de passe
    togglePassword.addEventListener('click', () => {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        togglePassword.textContent = type === 'password' ? 'Afficher' : 'Masquer';
    });

    // Évaluation du mot de passe
    function evaluatePassword(password) {
        let score = 0;
        if (password.length >= 8) score++;
        if (/[A-Z]/.test(password)) score++;
        if (/[a-z]/.test(password)) score++;
        if (/[0-9]/.test(password)) score++;
        if (/[\W]/.test(password)) score++;
        return score <= 2 ? 'weak' : score === 3 || score === 4 ? 'medium' : 'strong';
    }

    // Réinitialisation de la forteresse
    function resetFortress() {
        porte.classList.add('close-ico');
        tourDroite.classList.add('close-ico');
        tourGauche.classList.add('close-ico');
    }

    // Renforcement de la forteresse
    function reinforceFortress(level) {
        if (level === 'medium') porte.classList.remove('close-ico');
        if (level === 'strong') {
            porte.classList.remove('close-ico');
            tourDroite.classList.remove('close-ico');
            tourGauche.classList.remove('close-ico');
        }
    }

    submitBtn.addEventListener('click', () => {
    const password = passwordInput.value.trim();
    if (!password) {
        feedback.textContent = 'Veuillez entrer un mot de passe.';
        feedback.className = '';
        return;
    }

    const strength = evaluatePassword(password);

    fetch('/save-password/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: `password=${encodeURIComponent(password)}&strength=${encodeURIComponent(strength)}`
    })
    .then(response => response.json())
    .then(data => {
        feedback.textContent = data.message || 'Erreur lors de l’enregistrement.';
    })
    .catch(error => {
        feedback.textContent = 'Erreur réseau.';
        console.error('Erreur:', error);
    });
});
    // Modals
    startBtn.addEventListener('click', () => startModal.classList.add('hidden'));
    closeStart.addEventListener('click', () => startModal.classList.add('hidden'));
    closeSuccess.addEventListener('click', () => successModal.classList.add('hidden'));

    // Game Modal
    modal.style.display = 'flex';

    closeModalBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    startGameBtn.addEventListener('click', () => {
        modal.style.display = 'none';
        // Ajoutez ici le code pour démarrer le jeu
    });

    // Restart button logic
    const restartButton = document.getElementById('restart-button');
    restartButton.addEventListener('click', () => {
        // Effacer la zone de texte du mot de passe
        passwordInput.value = '';

        // Effacer le feedback
        feedback.textContent = '';
        feedback.className = '';

        // Réinitialiser la forteresse en supprimant les éléments (porte et tours)
        porte.classList.add('close-ico');
        tourDroite.classList.add('close-ico');
        tourGauche.classList.add('close-ico');
    });

    // Retour au menu button logic
    const backToMenuButton = document.getElementById('back-to-menu');
    backToMenuButton.addEventListener('click', () => {
        // Rediriger vers /levelTwo/
        window.location.href = '/levelTwo/';
    });

    document.querySelectorAll('img').forEach(img => {
    img.addEventListener('error', () => {
        console.error(`Erreur de chargement : ${img.src}`);
    });
});

});
