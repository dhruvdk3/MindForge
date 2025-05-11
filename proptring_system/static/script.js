document.addEventListener("DOMContentLoaded", function() {
    const questionContainer = document.getElementById("question-container");
    const questionText = document.getElementById("question-text");
    const answerList = document.getElementById("answer-list");
    const scoreElement = document.getElementById("score");

    let currentQuestionIndex = 0;
    let score = 0;

    function showQuestion() {
        if (currentQuestionIndex < questions.length) {
            const question = questions[currentQuestionIndex];
            questionText.innerHTML = (currentQuestionIndex + 1) + " : " + question.question;
            answerList.innerHTML = "";

            question.incorrect_answers.forEach(function(incorrectAnswer) {
                const button = document.createElement("button");
                button.textContent = incorrectAnswer;
                button.addEventListener("click", function() {
                    checkAnswer(false);
                });
                answerList.appendChild(document.createElement("li")).appendChild(button);
            });

            const correctButton = document.createElement("button");
            correctButton.textContent = question.correct_answer;
            correctButton.addEventListener("click", function() {
                checkAnswer(true);
            });
            answerList.appendChild(document.createElement("li")).appendChild(correctButton);
        } else {
            // Quiz completed
            questionContainer.innerHTML = `<h2 style="font-size: 1.5em; color: white;">Quiz Completed!</h2><p style="font-size: 1.5em; color: white;">Your score: ${score} out of ${questions.length}</p>`;
        }
    }

    function checkAnswer(isCorrect) {
        if (isCorrect) {
            score++;
        }
        currentQuestionIndex++;
        scoreElement.textContent = `Score: ${score}`;
        showQuestion();
    }

    // Load questions from the Flask route
    let questions;
    fetch("/get_questions")
        .then(response => response.json())
        .then(data => {
            questions = data;
            showQuestion();
        })
        .catch(error => {
            console.error("Error loading questions: " + error);
        });
});
