// ===================== QUIZ =====================
    const questions = [
        {
            q: "周波数 5 Hz、波長 2 m の波がある。この波の伝播速度はいくらか？",
            opts: ["2.5 m/s", "10 m/s", "7 m/s", "0.4 m/s"],
            correct: 1,
            explanation: "v = f × λ = 5 Hz × 2 m = 10 m/s"
        },
        {
            q: "周波数 20 Hz の波の周期はどれか？",
            opts: ["0.02 s", "0.05 s", "0.5 s", "20 s"],
            correct: 1,
            explanation: "T = 1/f = 1/20 = 0.05 s"
        },
        {
            q: "横波では、媒質の粒子の振動方向は波の進行方向に対してどうなっているか？",
            opts: ["平行", "垂直", "45°の角度", "反対方向"],
            correct: 1,
            explanation: "横波では、粒子の振動方向は波の進行方向に垂直である。"
        },
        {
            q: "波の式 y = 0.02 sin(4πx - 20πt) において、x と y はメートル、t は秒である。波長はいくらか？",
            opts: ["0.5 m", "1 m", "2 m", "4 m"],
            correct: 0,
            explanation: "k = 4π、λ = 2π/k = 2π/(4π) = 0.5 m"
        },
        {
            q: "音波は次のうちどの種類の波か？",
            opts: ["横波", "縦波", "電磁波", "定常波"],
            correct: 1,
            explanation: "音波は粒子の振動方向が進行方向と平行な縦波である。"
        },
        {
            q: "y = 3 sin(0.5πx - 4πt) の式から、この波の周波数はいくつか？",
            opts: ["0.5 Hz", "2 Hz", "4 Hz", "8 Hz"],
            correct: 1,
            explanation: "ω = 4π、f = ω/(2π) = 4π/(2π) = 2 Hz"
        },
        {
            q: "定常波で常に変位がゼロになる点を何と呼ぶか？",
            opts: ["腹", "節", "振幅", "最大ノード"],
            correct: 1,
            explanation: "節（ノード）は定常波で常に変位がゼロになる点である。"
        },
        {
            q: "振幅 A = 4 cm と A = 3 cm の2つの波が同位相で干渉したとき、合成振幅はいくらか？",
            opts: ["1 cm", "5 cm", "7 cm", "12 cm"],
            correct: 2,
            explanation: "同位相干渉では A_resultan = A₁ + A₂ = 4 + 3 = 7 cm である。"
        }
    ];

    let score = 0;
    let answered = new Array(questions.length).fill(false);

    function buildQuiz() {
        let container = document.getElementById('quizContainer');
        container.innerHTML = '';
        questions.forEach((q, i) => {
            let card = document.createElement('div');
            card.className = 'question-card';
            card.id = 'qcard-' + i;

            let qText = `<div class="question-text"><span class="q-num">${i + 1}</span>${q.q}</div>`;
            let optsHTML = '<div class="options">';
            q.opts.forEach((opt, j) => {
                optsHTML += `<button class="option-btn" id="opt-${i}-${j}" onclick="checkAnswer(${i}, ${j})">${opt}</button>`;
            });
            optsHTML += '</div>';
            let explHTML = `<div class="explanation" id="expl-${i}">💡 <b>解説:</b> ${q.explanation}</div>`;

            card.innerHTML = qText + optsHTML + explHTML;
            container.appendChild(card);
        });
    }

    function checkAnswer(qIndex, optIndex) {
        if (answered[qIndex]) return;
        answered[qIndex] = true;

        let q = questions[qIndex];
        let card = document.getElementById('qcard-' + qIndex);

        // Highlight selected
        let selectedBtn = document.getElementById(`opt-${qIndex}-${optIndex}`);

        if (optIndex === q.correct) {
            score++;
            selectedBtn.classList.add('selected-correct');
            card.classList.add('correct');
        } else {
            selectedBtn.classList.add('selected-wrong');
            card.classList.add('wrong');
            // Show correct
            document.getElementById(`opt-${qIndex}-${q.correct}`).classList.add('show-correct');
        }

        // Disable all buttons
        q.opts.forEach((_, j) => {
            document.getElementById(`opt-${qIndex}-${j}`).style.pointerEvents = 'none';
        });

        // Show explanation
        document.getElementById(`expl-${qIndex}`).classList.add('show');

        // Update score
        document.getElementById('scoreNum').textContent = score;
        let pct = (score / questions.length) * 100;
        document.getElementById('progressFill').style.width = pct + '%';
    }

    function resetQuiz() {
        score = 0;
        answered = new Array(questions.length).fill(false);
        document.getElementById('scoreNum').textContent = 0;
        document.getElementById('progressFill').style.width = '0%';
        buildQuiz();
    }

    // Init quiz on load
    buildQuiz();
    document.getElementById('totalQ').textContent = questions.length;