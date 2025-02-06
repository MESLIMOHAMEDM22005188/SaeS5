document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submitBtn');
    const passwordInput = document.getElementById('password');
    const feedback = document.getElementById('feedback');
    const togglePassword = document.getElementById('togglePassword');

    const porte = document.querySelector('#porte img');
    const tourDroite = document.querySelector('#tourDroite img');
    const tourGauche = document.querySelector('#tourGauche img');

    // Vérification du chargement des images
    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('error', () => {
            console.error(`Erreur de chargement : ${img.src}`);
            feedback.textContent = 'Erreur de chargement d\'une image !';
            feedback.className = 'error';
        });
    });

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
        resetFortress();
        if (level === 'medium') porte.classList.remove('close-ico');
        if (level === 'strong') {
            porte.classList.remove('close-ico');
            tourDroite.classList.remove('close-ico');
            tourGauche.classList.remove('close-ico');
        }
    }

    // Gestion de l'envoi du formulaire
    submitBtn.addEventListener('click', () => {
        const password = passwordInput.value.trim();

        if (!password) {
            feedback.textContent = 'Veuillez entrer un mot de passe.';
            feedback.className = 'error';
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
            if (data.error) {
                feedback.textContent = 'Erreur : ' + data.error;
                feedback.className = 'error';
            } else {
                feedback.textContent = data.message || 'Forteresse renforcée avec succès !';
                feedback.className = 'success';
                reinforceFortress(strength);
            }
        })
        .catch(error => {
            feedback.textContent = 'Erreur réseau. Veuillez réessayer.';
            feedback.className = 'error';
            console.error('Erreur:', error);
        });
    });

    // Réinitialisation de la forteresse et des messages au redémarrage
    const restartButton = document.getElementById('restart-button');
    restartButton.addEventListener('click', () => {
        passwordInput.value = '';
        feedback.textContent = '';
        feedback.className = '';
        resetFortress();
    });

    // Redirection vers le menu
    const backToMenuButton = document.getElementById('back-to-menu');
    backToMenuButton.addEventListener('click', () => {
        window.location.href = '/levelTwo/';
    });
});
