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

    // Gestion du mot de passe
    submitBtn.addEventListener('click', () => {
        const password = passwordInput.value.trim();
        if (!password) {
            feedback.textContent = 'Veuillez entrer un mot de passe.';
            feedback.className = '';
            return;
        }

        const strength = evaluatePassword(password);
        resetFortress();
        reinforceFortress(strength);

        feedback.className = strength;
        feedback.textContent = strength === 'weak'
            ? 'Mot de passe faible.'
            : strength === 'medium'
            ? 'Mot de passe moyen.'
            : 'Mot de passe fort. La forteresse est protégée !';

        if (strength === 'strong') successModal.classList.remove('hidden');
    });

    // Modals
    startBtn.addEventListener('click', () => startModal.classList.add('hidden'));
    closeStart.addEventListener('click', () => startModal.classList.add('hidden'));
    closeSuccess.addEventListener('click', () => successModal.classList.add('hidden'));
});
