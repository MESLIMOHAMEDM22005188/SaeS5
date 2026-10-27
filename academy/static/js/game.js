// --- SHOW ONE QUESTION AT A TIME ---
let currentQuestionIndex = 0;
const questions = document.querySelectorAll(".question");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const checkBtn = document.getElementById("checkBtn");

// Display the question at currentQuestionIndex
function showQuestion(index) {
  // Hide all questions
  questions.forEach((q) => {
    q.style.display = "none";
  });

  // Show the selected question
  questions[index].style.display = "block";

  // Update button visibility
  // Hide Previous on the first question
  if (index === 0) {
    prevBtn.style.display = "none";
  } else {
    prevBtn.style.display = "inline-block";
  }

  // Hide Next and show Submit on the last question
  if (index === questions.length - 1) {
    nextBtn.style.display = "none";
    checkBtn.style.display = "inline-block";
  } else {
    nextBtn.style.display = "inline-block";
    checkBtn.style.display = "none";
  }
}

// Next button
function nextQuestion() {
  if (currentQuestionIndex < questions.length - 1) {
    currentQuestionIndex++;
    showQuestion(currentQuestionIndex);
  }
}

// Previous button
function prevQuestion() {
  if (currentQuestionIndex > 0) {
    currentQuestionIndex--;
    showQuestion(currentQuestionIndex);
  }
}

// Show the first question when the page loads
showQuestion(currentQuestionIndex);


// --- GRADE THE ANSWERS ---
function checkAnswers() {
  const correctAnswers = {
    q1: "B",
    q2: "C",
    q3: "A",
    q4: "C",
    q5: "B"
  };

  let score = 0;
  let totalQuestions = Object.keys(correctAnswers).length;

  for (let question in correctAnswers) {
    const radios = document.getElementsByName(question);

    // Find the selected radio button
    for (let i = 0; i < radios.length; i++) {
      if (radios[i].checked) {
        if (radios[i].value === correctAnswers[question]) {
          score++;
        }
        break;
      }
    }
  }

  // Display the result
  const resultDiv = document.getElementById("result");
  resultDiv.textContent = `You answered ${score} out of ${totalQuestions} questions correctly.`;
}
