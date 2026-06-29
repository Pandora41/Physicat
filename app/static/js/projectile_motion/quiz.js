// ===================== QUIZ =====================
    const questions = [
        {
            q: "v₀ = 30 m/s で角度 30° で発射された弾丸の垂直速度成分を求めよ。 (g = 10 m/s²)",
            opts: ["15 m/s", "26 m/s", "30 m/s", "10 m/s"],
            correct: 0,
            explanation: "v₀ᵧ = v₀·sinθ = 30 × sin(30°) = 30 × 0.5 = 15 m/s"
        },
        {
            q: "放物運動の最高点において、垂直速度はいくつか？",
            opts: ["最大", "初速度と同じ", "ゼロ", "最小だがゼロではない"],
            correct: 2,
            explanation: "最高点では、垂直速度成分 (vᵧ) = 0 である。水平成分 (vₓ) のみが残る。"
        },
        {
            q: "同じ初速度で、1つは角度 30°、もう1つは角度 60° で発射された2つの弾丸のうち、どちらが遠くまで飛ぶか？ (h₀ = 0)",
            opts: ["30°", "60°", "同じ距離", "決定できない"],
            correct: 2,
            explanation: "h₀ = 0 の場合、角度 θ と (90°-θ) は同じ飛距離を与える。R ∝ sin(2θ) であり、sin(60°) = sin(120°) だからである。"
        },
        {
            q: "放物運動で最高点に達するまでの時間はいくつか？",
            opts: ["t = v₀/g", "t = v₀·sinθ/g", "t = 2v₀·sinθ/g", "t = v₀·cosθ/g"],
            correct: 1,
            explanation: "tₘₐₓ = v₀ᵧ/g = (v₀·sinθ)/g である。最高点では vᵧ = 0 = v₀ᵧ - gt だからである。"
        },
        {
            q: "ある惑星の重力が地球の4倍である場合、同じパラメータでの飛行時間はどうなるか？",
            opts: ["4倍長い", "2倍長い", "半分短い", "4分の1短い"],
            correct: 3,
            explanation: "h₀=0 の場合 t ∝ 1/√g、または一般に t ∝ 1/g である。g が4倍なら、t は4分の1になる。"
        },
        {
            q: "高さ 5 m から水平方向に v₀ = 10 m/s でボールを投げた。地面に落ちるまでの時間はいくらか？ (g = 10 m/s²)",
            opts: ["0.5 s", "1.0 s", "1.4 s", "2.0 s"],
            correct: 1,
            explanation: "垂直運動: h = ½gt² → 5 = ½×10×t² → t² = 1 → t = 1 s (水平運動は落下時間に影響しない)"
        },
        {
            q: "水平面 (h₀ = 0) で最大飛距離を得る最適発射角度はいくつか？",
            opts: ["30°", "45°", "60°", "90°"],
            correct: 1,
            explanation: "R = (v₀²·sin(2θ))/g である。sin(2θ) = 1 のとき最大 → 2θ = 90° → θ = 45°"
        },
        {
            q: "地面に到達した瞬間 (h₀ = 0) の全体の速度は、初速度と比較してどうなるか？",
            opts: ["より大きい", "より小さい", "同じ大きさ", "ゼロ"],
            correct: 2,
            explanation: "空気抵抗がなければ、力学的エネルギーは保存される。初期高さ = 終了高さ → 全体の速度は等しい (向きは異なる)。"
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