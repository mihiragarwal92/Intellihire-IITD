document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#make-quiz').addEventListener('click', () => make_quiz());
    document.querySelector('#username').addEventListener('click', () => load_quizzes('own'));
    document.querySelector('#display-scores').addEventListener('click', () => display_scores_view());

    load_quizzes('all');

    document.querySelector('#quiz-form').addEventListener('submit', event => {
        event.preventDefault();
        let quizId = 0;
        try {
            quizId = document.getElementById('quizId').innerHTML;
        }
        catch (e) {
            console.log('New quiz is being saved.')
        }
        finally  {
            save_quiz(quizId);
        }
    });

    document.querySelector('#question-form').addEventListener('submit', event => {
        event.preventDefault();
        let questionId = 0;
        try {
            questionId = document.getElementById('questionId').innerHTML;
        }
        catch (e) {
            console.log('New question is being saved.')
        }
        finally  {
            save_question(questionId);
        }
    });
});

function load_quizzes (category) {   
    document.querySelector('#add-quiz').style.display = 'none';
    document.querySelector('#quiz-dashboard').style.display = 'none';
    document.querySelector('#take-quiz').style.display = 'none';
    document.querySelector('#scores').style.display = 'none';

    const titleContainer = document.querySelector('#title');
    const title = category === 'all' ? 'ALL QUIZZES' : 'YOUR QUIZZES';
    titleContainer.innerHTML = title;

    const container = document.querySelector('#quizzes');
    container.innerHTML = '';

    const user = document.querySelector('#username').innerHTML;

    fetch(`/quizzes/${category}`)
        .then(response => response.json())
        .then(response => {

            response.forEach((quiz, i) => {
                const element = document.createElement('div');
                element.classList.add('col-sm-4', 'p-2');

                let takeOrEdit = `id="take-${quiz.id}" onClick="take_quiz(${quiz.id})">take`;
                if (quiz.author == user) takeOrEdit = `id="edit-${quiz.id}" onClick="load_quiz_dashboard(${quiz.id})">edit`;

                element.innerHTML = `
                    <div class='card ${quiz.colour_class}' style='height: 100%;'>
                        <div class="card-body d-flex flex-column">
                            <div class="header">
                                <a class="text-reset text-decoration-none"><h5><strong id="title-${quiz.id}">${quiz.title}</strong></h5></a>
                            </div>
                            <div class="content">
                                <p id="post-${quiz.id}">${quiz.description}</p>
                            </div> 
                            <div class="footer">
                                <a class="btn btn-light align-self-end button" style='width: 100%;' ${takeOrEdit}</a>
                            </div>
                        </div>
                    </div>
                `;
                container.append(element);
            });

            if (response.length === 0) {
                const element = document.createElement('div');
                element.innerHTML = 'There are no quizzes here at the moment.';
                container.append(element);
            }
        });
}


function take_quiz (quizId) {
    document.querySelector('#take-quiz').style.display = 'block';

    document.querySelector('#add-quiz').style.display = 'none';
    document.querySelector('#quiz-dashboard').style.display = 'none';
    document.querySelector('#scores').style.display = 'none';
    document.querySelector('#quizzes').innerHTML = '';

    fetch(`/quiz/${quizId}`)
        .then(response => response.json())
        .then(response => {
            quiz = response.quiz;
            questions = response.questions;

            document.querySelector('#title').innerHTML = `
                ${quiz.title}
                <h5><small class="text-muted d-block mb-3">${quiz.description}</small></h5>
            `;

            display_question(-1, questions, quiz, 0);
        })
}


function display_question (n, questions, quiz, score) {
    let container = document.querySelector('#take-quiz');
    let color = quiz.colour_class;

    const next = document.createElement('button');
    next.classList.add('btn', 'btn-light', color);
    next.addEventListener('click', function() {
        display_question(n+1, questions, quiz, score);
    });

    if (n === questions.length) {
        container.innerHTML = `
            Congratulations! You finished the quiz!<br>
          
        `;

        fetch(`/score/save/${quiz.id}`, {
            method: 'POST',
            body: JSON.stringify({
            'quiz': quiz.id,
            'score': score,
            })
        })
            .then(response => response.json())
            .then(result => {
                console.log(result);
            });

        const scores = document.createElement('button');
        scores.innerHTML = 'See top scores';
        scores.classList.add('btn', 'btn-light', color);
        scores.addEventListener('click', function() {
            display_scores_view();
        });
        container.append(scores);
        return score;
    }
    else if (n === -1) {
        next.innerHTML = 'Start the quiz!';
        next.classList.add('btn-lg', color);
        container.append(next);
    }
    else {
        next.innerHTML = 'Next question';
        let question = questions[n];
        container.innerHTML = `
            Question #${n+1}:<br>
            ${question.text}<br>
        `;

        if (question.image) {
            const image = document.createElement('img');
            image.classList.add('img-fluid', 'mx-auto', 'question-img');
            image.src = question.image;
            container.append(image);
        }

        const answers_div = document.createElement('div');

        switch (question.type) {
            case 'type_answer':
                answers_div.innerHTML = `
                    <div class="form-group"><br>
                        Type your answer: <input id="answer-type" class="form-control mx-auto" style="max-width: 80%;">
                    </div>
                `;
                const check = document.createElement('button');
                check.classList.add('btn', 'btn-light', color);
                check.innerHTML = 'Check';
                answers_div.append(check);
                container.append(answers_div);

                check.addEventListener('click', function() {
                    let inputField = document.getElementById('answer-type');
                    let value = inputField.value
                        .replace(/[.:\-*+?^${}()|[\]\\]/g, '')
                        .trim()
                        .toUpperCase();
                    let right_answer = question.right_answer
                        .replace(/[.:\-*+?^${}()|[\]\\]/g, '')
                        .trim()
                        .toUpperCase();
                    check.remove();

                    if (value === right_answer) {
                        inputField.classList.add('right');
                        score += 1;
                    } else {
                        inputField.classList.add('wrong');
                        const answer = document.createElement('div');
                        answer.innerHTML = `The right answer is: ${question.right_answer}<br><br>`;
                        container.append(answer);
                    }
                    container.append(next);
                });
                break; 

            case 'multi_choice':
                let answers = [question.right_answer, question.wrong_answer1, question.wrong_answer2, question.wrong_answer3];
                answers.sort(() => Math.random() - 0.5);
                let buttonStyle = `<div class="answer col-sm btn btn-light m-1">`;
                answers_div.innerHTML = `
                    <div class="container m-2 mx-auto">
                        <div class="row">
                            ${buttonStyle} ${answers[0]} </div>
                            ${buttonStyle} ${answers[1]} </div>
                        </div>
                        <div class="row">
                            ${buttonStyle} ${answers[2]} </div>
                            ${buttonStyle} ${answers[3]} </div>
                        </div>
                    </div>
                `;
                container.append(answers_div);
                
                let buttons = document.getElementsByClassName('answer');
                let check_multiple = once(check_answer);
                Array.prototype.forEach.call(buttons, el => {
                    el.addEventListener('click', e => {
                        score += check_multiple(e.target, question.right_answer, buttons);
                        container.append(next);
                    });
                });
                break;

            case 'true_or_false':
                answers_div.innerHTML = `
                    <div class="container m-2 mx-auto">
                        <div class="row">
                            <div id="answer-true" class="answer col-sm btn btn-light m-1">Yes</div>
                            <div id="answer-false" class="answer col-sm btn btn-light m-1">No</div>
                        </div>
                    </div>
                `;
                container.append(answers_div);
                
                let buttons_true = document.getElementsByClassName('answer');
                let check_true = once(check_answer);
                Array.prototype.forEach.call(buttons_true, el => {
                    let answer = question.isTrue ? 'True' : 'False';
                    el.addEventListener('click', e => {
                        score += check_true(e.target, answer, buttons_true);
                        container.append(next);
                    });
                });
                break;
        }     
    }
}


function once (func) {
    let called = false;
    let result;
    return function () {
      if (!called) {
        called = true;
        result = func.apply(this, arguments);
      }
      return result;
    };
}


function check_answer (clicked, answer, buttons) {
    if (clicked.innerText === answer) {
        clicked.classList.add('right');
        return 1;
    } else {
        clicked.classList.add('wrong');
        Array.prototype.forEach.call(buttons, el => {
            if (el.innerText === answer) el.classList.add('right');
        });
        return 0;
    }
}


function load_quiz_dashboard (quizId) {
    document.querySelector('#quiz-dashboard').style.display = 'block';
    document.querySelector('#add-question').style.display = 'none';

    document.querySelector('#add-quiz').style.display = 'none';
    document.querySelector('#take-quiz').style.display = 'none';
    document.querySelector('#scores').style.display = 'none';
    document.querySelector('#quizzes').innerHTML = '';

    document.querySelector('#title').innerHTML = 'QUIZ DASHBOARD';

    fetch(`/quiz/${quizId}`)
        .then(response => response.json())
        .then(response => {
            quiz = response.quiz;
            questions = response.questions;

            let div_quiz = document.querySelector('#quiz-info');
            let div_questions = document.querySelector('#questions-info');
            let isPublic = quiz.public ? 'public' : 'private';

            div_quiz.innerHTML = `
                <h5>
                    ${quiz.title}
                    <a class="badge badge-light" id="edit" onClick="edit_quiz(${quiz.id})">edit</a>
                    <a class="badge badge-light" id="remove" onClick="remove_quiz(${quiz.id})">remove</a>
                </h5>
                <p>${quiz.description}</p>
                <p>This quiz is now ${isPublic}.</p>
                <small class="text-muted">Created on: ${quiz.timestamp}</small>
                <br><br>
            `;

            div_questions.innerHTML = '<h5>Questions</h5>';

            questions.forEach((question, index) => {
                const element = document.createElement('div');
                element.classList.add('card','mt-2', quiz.colour_class);

                let type = question.type.split('_').join(' ');
                type = type.charAt(0).toUpperCase() + type.slice(1);

                element.innerHTML = `
                    <div class="card-body">
                        <strong>#${index+1} - ${type}</strong>
                        <a class="badge badge-light button" id="edit-q-${question.id}" onClick="edit_question(${question.id}, ${quiz.id})">edit</a>
                        <a class="badge badge-light button" id="remove-q-${question.id}" onClick="remove_question(${question.id}, ${quiz.id})">remove</a>
                        <br>
                        ${question.text}
                    </div>
                `;
                div_questions.append(element);
            });

            if (questions.length === 0) {
                const element = document.createElement('div');
                element.classList.add('card','mt-2', quiz.colour_class);
                element.innerHTML = '<div class="card-body">There are no questions at the moment.</div>';
                div_questions.append(element);
            }

            const element = document.createElement('div');
            element.classList.add('card','mt-2', quiz.colour_class);
            element.innerHTML = `
                <div class="card-body">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-plus" viewBox="0 0 16 16">
                        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                    </svg>
                    Add question
                </div>
            `;
            element.addEventListener('click', function() {
                add_question(quiz.id);
            });
            div_questions.append(element);
        });
}

function add_question (quizId) {
    document.querySelector('#questions-info').innerHTML = `
        <h5>
            Add a question
            <a class="badge badge-light" id="cancel" onClick="load_quiz_dashboard(${quizId})">cancel</a>
        </h5>
    `;
    document.querySelector('#add-question').style.display = 'block';
    document.querySelector('#question-form').style.display = 'none';

    clear_question_form();

    let typeSelector = document.querySelector('#question-form-type');
    typeSelector.addEventListener('change', () => {
        display_question_form(quizId, typeSelector.value);
    });
}


function display_question_form (quizId, type) {
    document.querySelector('#question-form').style.display = 'block';
    document.querySelector('#question-form-quizId').value = quizId;
    document.querySelector('#statement').innerHTML = 'Question:';

    let taForm = document.querySelector('#ta-form');
    taForm.style.display = 'none';

    let mcForm = document.querySelector('#mc-form');
    mcForm.style.display = 'none';

    let tfForm = document.querySelector('#tf-form');
    tfForm.style.display = 'none';

    switch (type) {
        case 'type_answer':
            taForm.style.display = 'block';
            break; 
        case 'multi_choice':
            taForm.style.display = 'block';
            mcForm.style.display = 'block';
            break;
        case 'true_or_false':
            document.querySelector('#statement').innerHTML = 'Statement:';
            tfForm.style.display = 'block';
            break;
    }
}


function clear_question_form () {
    document.querySelector('#question-form-type').value = '';
    document.querySelector('#question-form-text').value = '';
    document.querySelector('#question-form-image').value = '';
    document.querySelector('#question-form-answer').value = '';
    document.querySelector('#question-form-wrong1').value = '';
    document.querySelector('#question-form-wrong2').value = '';
    document.querySelector('#question-form-wrong3').value = '';
}


function edit_question (questionId, quizId) {
    document.querySelector('#questions-info').innerHTML = `<h5>Edit a question #<span id="questionId">${questionId}</span></h5>`;
    document.querySelector('#add-question').style.display = 'block';
    document.querySelector('#question-form').style.display = 'none';

    clear_question_form();

    fetch(`/question/${questionId}`)
        .then(response => response.json())
        .then(response => {
            question = response.question;

            document.querySelector('#question-form-type').value = question.type;
            document.querySelector('#question-form-text').value = question.text;
            document.querySelector('#question-form-image').value = question.image;
            document.querySelector('#question-form-answer').value = question.right_answer;
            document.querySelector('#question-form-wrong1').value = question.wrong_answer1;
            document.querySelector('#question-form-wrong2').value = question.wrong_answer2;
            document.querySelector('#question-form-wrong3').value = question.wrong_answer3;
            if (question.type === 'true_or_false') {
                if (question.isTrue) document.querySelector('#question-form-true').checked = true;
                else document.querySelector('#question-form-false').checked = true
            }

            display_question_form(quizId, question.type);
            let typeSelector = document.querySelector('#question-form-type');
            typeSelector.addEventListener('change', () => {
                display_question_form(quizId, typeSelector.value);
            });
        });
}


function save_question (questionId) {
    let isTrue = (document.querySelector('#question-form-true').checked === true) ? true : false;
    quizId = document.querySelector('#question-form-quizId').value

    fetch(`/question/${questionId}`, {
        method: 'POST',
        body: JSON.stringify({
        'quiz': quizId,
        'text': document.querySelector('#question-form-text').value,
        'image': document.querySelector('#question-form-image').value,
        'type': document.querySelector('#question-form-type').value,
        'right_answer': document.querySelector('#question-form-answer').value,
        'wrong_answer1': document.querySelector('#question-form-wrong1').value,
        'wrong_answer2': document.querySelector('#question-form-wrong2').value,
        'wrong_answer3': document.querySelector('#question-form-wrong3').value,
        'isTrue': isTrue
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            load_quiz_dashboard(quizId);
        });
}


function remove_question (questionId, quizId) {
    fetch(`/remove_question/${questionId}`)
        .then(response => response.json())
        .then(result => {
            console.log(result);
            load_quiz_dashboard(quizId);
        });
}


function make_quiz () {
    document.querySelector('#add-quiz').style.display = 'block';

    document.querySelector('#quiz-dashboard').style.display = 'none';
    document.querySelector('#take-quiz').style.display = 'none';
    document.querySelector('#scores').style.display = 'none';
    document.querySelector('#quizzes').innerHTML = '';

    document.querySelector('#title').innerHTML = 'NEW QUIZ';

    document.querySelector('#quiz-form-title').value = '';
    document.querySelector('#quiz-form-description').value = '';
}


function edit_quiz (quizId) {
    make_quiz ()

    fetch(`/quiz/${quizId}`)
        .then(response => response.json())
        .then(response => {
            quiz = response.quiz;

            document.querySelector('#title').innerHTML = `Edit Quiz #<span id="quizId">${quiz.id}</span>`;
            document.querySelector('#quiz-form-title').value = quiz.title;
            document.querySelector('#quiz-form-description').value = quiz.description;
            if (quiz.public) document.querySelector('#quiz-form-public').checked = true;
            else document.querySelector('#quiz-form-private').checked = true;
        });
}


function save_quiz (quizId) {
    fetch(`/quiz/${quizId}`, {
        method: 'POST',
        body: JSON.stringify({
        title: document.querySelector('#quiz-form-title').value,
        description: document.querySelector('#quiz-form-description').value,
        visibility: document.querySelector('input[name="visibility"]:checked').value
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            load_quiz_dashboard(result.quiz);
        });
}


function remove_quiz (quizId) {
    fetch(`/remove_quiz/${quizId}`)
        .then(response => response.json())
        .then(result => {
            console.log(result);
            load_quizzes('own');
        });
}


function display_scores_view() {
    document.querySelector('#add-quiz').style.display = 'none';
    document.querySelector('#quiz-dashboard').style.display = 'none';
    document.querySelector('#take-quiz').style.display = 'none';
    document.querySelector('#quizzes').innerHTML = '';

    document.querySelector('#title').innerHTML = 'TOP SCORES';

    document.querySelector('#scores').style.display = 'block';
    document.querySelector('#scores-result').innerHTML = '';
    document.querySelector('#scores-category').style.display = 'block';
    document.querySelector('#scores-quiz').style.display = 'none';

    let categoryField = document.querySelector('#scores-category-choice');
    categoryField.addEventListener('change', () => {
        let quizField = document.querySelector('#scores-quiz-choice');
        quizField.innerHTML = '';
        let category = categoryField.value;
        let quizId = 0;

        if (category === 'quiz') {
            document.querySelector('#scores-result').innerHTML = '';
            const emptyOption = document.createElement('option');
            emptyOption.disabled = true;
            emptyOption.selected = true;
            emptyOption.value = true;
            emptyOption.innerHTML = `-- select an option --`;
            quizField.append(emptyOption);

            fetch('/quizzes/all')
                .then(response => response.json())
                .then(response => {
                    response.forEach(quiz => {
                        const option = document.createElement('option');
                        option.value = quiz.id;
                        option.innerHTML = `${quiz.title}`;
                        quizField.append(option);
                    })
                });

            document.querySelector('#scores-quiz').style.display = 'block';
            quizField.addEventListener('change', () => {
                let category = categoryField.value;
                display_scores(category, quizField.value);
            });
        } else {
            document.querySelector('#scores-quiz').style.display = 'none';
            document.querySelector('#scores-no-result').innerHTML = '';
            display_scores(category, quizId);
        }
    });
}


function display_scores (category, quizId) {
    fetch(`/score/${category}/${quizId}`)
        .then(response => response.json())
        .then(response => {

            let div = document.querySelector('#scores-result');
            div.innerHTML = '';

            response.forEach(score => {
                const li = document.createElement('li');
                li.classList.add('mb-2');

                // Create a new Date object from the timestamp
                const timestampDate = new Date(score.timestamp);

                // Format date and time separately
                const formattedDate = timestampDate.toLocaleDateString();
                const formattedTime = timestampDate.toLocaleTimeString();

                li.innerHTML = `
                    <h6>
                    User: ${score.user} &nbsp;  
                    <strong>Quiz: ${score.quiz_title}</strong> &nbsp;
                    Score: ${score.score}/${score.total} (${score.score_percent}%) &nbsp;
                    <small class="text-muted">${formattedDate} ${formattedTime}</small>
                    </h6>
                `;
                div.append(li);
            });

            const message = document.querySelector('#scores-no-result');
            if (response.length) {
                message.innerHTML = '';
            } else {
                message.innerHTML = 'There are no scores in this category yet.';
            }
        });
}
