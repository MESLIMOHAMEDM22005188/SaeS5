// --- GESTION DE L’AFFICHAGE UNE QUESTION À LA FOIS ---
let currentQuestionIndex = 0;
const questions = document.querySelectorAll(".question");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const checkBtn = document.getElementById("checkBtn");

// Fonction qui affiche la question correspondant à currentQuestionIndex
function showQuestion(index) {
  // Masquer toutes les questions
  questions.forEach((q) => {
    q.style.display = "none";
  });

  // Afficher la question voulue
  questions[index].style.display = "block";

  // Gérer l’affichage des boutons
  // Si on est sur la première question, on cache "Précédent"
  if (index === 0) {
    prevBtn.style.display = "none";
  } else {
    prevBtn.style.display = "inline-block";
  }

  // Si on est sur la dernière question, on cache "Suivant" et on montre "Valider"
  if (index === questions.length - 1) {
    nextBtn.style.display = "none";
    checkBtn.style.display = "inline-block";
  } else {
    nextBtn.style.display = "inline-block";
    checkBtn.style.display = "none";
  }
}

// Bouton « Suivant »
function nextQuestion() {
  if (currentQuestionIndex < questions.length - 1) {
    currentQuestionIndex++;
    showQuestion(currentQuestionIndex);
  }
}

// Bouton « Précédent »
function prevQuestion() {
  if (currentQuestionIndex > 0) {
    currentQuestionIndex--;
    showQuestion(currentQuestionIndex);
  }
}

// Au chargement de la page, afficher la première question
showQuestion(currentQuestionIndex);


// --- FONCTION QUI CORRIGE LES RÉPONSES ---
function checkAnswers() {
  // On définit les bonnes réponses (A, B, C, D, etc.)
  const correctAnswers = {
    q1: "B",
    q2: "C",
    q3: "A",
    q4: "C",
    q5: "B"
  };

  let score = 0;
  let totalQuestions = Object.keys(correctAnswers).length;

  // Pour chaque question, on récupère la réponse sélectionnée et on compare
  for (let question in correctAnswers) {
    // Récupère tous les inputs radio de la question
    const radios = document.getElementsByName(question);

    // Parcours des radios pour trouver celle qui est cochée
    for (let i = 0; i < radios.length; i++) {
      if (radios[i].checked) {
        if (radios[i].value === correctAnswers[question]) {
          score++;
        }
        break;
      }
    }
  }

  // Affiche le résultat
  const resultDiv = document.getElementById("result");
  resultDiv.textContent = `Vous avez ${score} bonne(s) réponse(s) sur ${totalQuestions}.`;
}
