// ===================== P5.JS SIMULATION =====================
    let A = 50, f = 1.0, lambda = 200, v = 200;
    let waveType = 'transversal';
    let time = 0;
    let canvasW = 800, canvasH = 300;
    let particles = [];

    function setup() {
        let container = document.getElementById('canvas-container');
        let canvas = createCanvas(canvasW, canvasH);
        canvas.parent(container);
        textFont('Segoe UI');

        // Init particles for longitudinal
        for (let i = 0; i < 60; i++) {
            particles.push({
                baseX: (canvasW / 60) * i + 5,
                x: 0,
                y: canvasH / 2
            });
        }
    }

    function draw() {
        background(245, 243, 248);
        time += 1 / 60;

        // Grid
        drawGrid();

        if (waveType === 'transversal') drawTransversal();
        else if (waveType === 'longitudinal') drawLongitudinal();
        else if (waveType === 'standing') drawStanding();
        else if (waveType === 'superposition') drawSuperposition();

        // Labels on canvas
        drawLabels();
    }

    function drawGrid() {
        stroke(212, 197, 226, 100);
        strokeWeight(0.5);
        for (let x = 0; x < canvasW; x += 50) line(x, 0, x, canvasH);
        for (let y = 0; y < canvasH; y += 50) line(0, y, canvasW, y);

        // Axis
        stroke(168, 155, 200, 150);
        strokeWeight(1);
        line(0, canvasH / 2, canvasW, canvasH / 2);
    }

    function drawTransversal() {
        // Main wave
        noFill();
        strokeWeight(3);

        // Glow effect
        for (let g = 3; g >= 0; g--) {
            let alpha = map(g, 0, 3, 255, 60);
            stroke(168, 155, 200, alpha);
            strokeWeight(g === 0 ? 3 : g * 2);
            beginShape();
            for (let x = 0; x < canvasW; x += 2) {
                let k = TWO_PI / lambda;
                let omega = TWO_PI * f;
                let y = canvasH / 2 + A * sin(k * x - omega * time);
                vertex(x, y);
            }
            endShape();
        }

        // Amplitude line
        stroke(245, 168, 212, 200);
        strokeWeight(2);
        let ampX = 100;
        let ampYmid = canvasH / 2;
        let ampYtop = canvasH / 2 - A;
        line(ampX, ampYmid, ampX, ampYtop);
        // Arrow
        fill(245, 168, 212);
        noStroke();
        triangle(ampX - 6, ampYtop + 10, ampX + 6, ampYtop + 10, ampX, ampYtop);
        // Label
        fill(168, 155, 200);
        noStroke();
        textSize(13);
        textAlign(CENTER, CENTER);
        text('A = ' + nf(A, 1, 0) + ' px', ampX, ampYmid - A / 2);

        // Wavelength indicator
        stroke(177, 156, 217, 180);
        strokeWeight(2);
        let wlY = canvasH / 2 + A + 30;
        line(0, wlY, lambda, wlY);
        // Arrows
        fill(177, 156, 217);
        noStroke();
        triangle(0, wlY - 5, 0, wlY + 5, 10, wlY);
        triangle(lambda, wlY - 5, lambda, wlY + 5, lambda - 10, wlY);
        // End caps
        stroke(177, 156, 217, 180);
        strokeWeight(2);
        line(0, wlY - 8, 0, wlY + 8);
        line(lambda, wlY - 8, lambda, wlY + 8);
        // Label
        fill(177, 156, 217);
        noStroke();
        textSize(14);
        textAlign(CENTER, TOP);
        text('λ = ' + nf(lambda, 1, 0) + ' px', lambda / 2, wlY + 10);

        // Moving point on wave
        let ptX = (canvasW / 2) % lambda;
        let k = TWO_PI / lambda;
        let omega = TWO_PI * f;
        let ptY = canvasH / 2 + A * sin(k * ptX - omega * time);

        noStroke();
        for (let r = 15; r > 0; r -= 3) {
            fill(168, 155, 200, map(r, 0, 15, 200, 30));
            ellipse(ptX, ptY, r * 2, r * 2);
        }
        fill(255);
        ellipse(ptX, ptY, 6, 6);

        // Velocity arrow on point
        let vel = A * omega * cos(k * ptX - omega * time);
        let arrowLen = vel * 0.3;
        stroke(200, 150, 180, 200);
        strokeWeight(2);
        line(ptX, ptY, ptX, ptY - arrowLen);
        if (abs(arrowLen) > 5) {
            fill(200, 150, 180);
            noStroke();
            let dir = arrowLen > 0 ? -1 : 1;
            triangle(ptX - 4, ptY - arrowLen + dir * 8, ptX + 4, ptY - arrowLen + dir * 8, ptX, ptY - arrowLen);
        }
    }

    function drawLongitudinal() {
        let k = TWO_PI / lambda;
        let omega = TWO_PI * f;
        let midY = canvasH / 2;

        // Draw particles
        noStroke();
        for (let p of particles) {
            let displacement = A * 0.5 * sin(k * p.baseX - omega * time);
            p.x = p.baseX + displacement;

            let density = cos(k * p.baseX - omega * time);
            let sz = map(density, -1, 1, 4, 14);
            let col = map(density, -1, 1, color(100, 100, 255), color(255, 80, 80));

            fill(col);
            ellipse(p.x, midY, sz, sz);
        }

        // Density curve overlay
        noFill();
        stroke(168, 155, 200, 150);
        strokeWeight(2);
        beginShape();
        for (let x = 0; x < canvasW; x += 3) {
            let val = cos(k * x - omega * time);
            let y = midY + val * A * 0.6;
            vertex(x, y);
        }
        endShape();

        // Labels
        fill(177, 156, 217);
        noStroke();
        textSize(13);
        textAlign(CENTER, TOP);
        text('密な部分 (圧縮) ↔ 疎な部分 (希薄)', canvasW / 2, 20);
        fill(168, 155, 200);
        textSize(12);
        text('λ = ' + nf(lambda, 1, 0) + ' px', canvasW / 2, 42);

        // Wavelength bracket
        stroke(177, 156, 217, 150);
        strokeWeight(1.5);
        let wlY = midY + A + 40;
        line(0, wlY, lambda, wlY);
        line(0, wlY - 5, 0, wlY + 5);
        line(lambda, wlY - 5, lambda, wlY + 5);
        fill(177, 156, 217);
        noStroke();
        textSize(12);
        text('λ', lambda / 2, wlY + 12);
    }

    function drawStanding() {
        let k = TWO_PI / lambda;
        let omega = TWO_PI * f;
        let midY = canvasH / 2;

        // Draw multiple time snapshots (ghost waves)
        noFill();
        for (let t = 0; t < 8; t++) {
            let phase = t * PI / 8;
            let alpha = map(t, 0, 8, 180, 20);
            stroke(168, 155, 200, alpha);
            strokeWeight(1.5);
            beginShape();
            for (let x = 0; x < canvasW; x += 2) {
                let y = midY + A * sin(k * x) * cos(omega * time + phase);
                vertex(x, y);
            }
            endShape();
        }

        // Main wave (current)
        stroke(168, 155, 200, 255);
        strokeWeight(3);
        beginShape();
        for (let x = 0; x < canvasW; x += 2) {
            let y = midY + A * sin(k * x) * cos(omega * time);
            vertex(x, y);
        }
        endShape();

        // Envelope
        noFill();
        stroke(177, 156, 217, 120);
        strokeWeight(1.5);
        strokeDash(5);
        beginShape();
        for (let x = 0; x < canvasW; x += 2) {
            vertex(x, midY + A * abs(sin(k * x)));
        }
        endShape();
        beginShape();
        for (let x = 0; x < canvasW; x += 2) {
            vertex(x, midY - A * abs(sin(k * x)));
        }
        endShape();
        noDash();

        // Nodes
        noStroke();
        for (let x = 0; x < canvasW; x += 2) {
            if (abs(sin(k * x)) < 0.03) {
                fill(200, 150, 180);
                ellipse(x, midY, 10, 10);
                fill(210, 165, 195);
                textSize(9);
                textAlign(CENTER);
                text('節', x, midY + 20);
            }
        }

        // Antinodes
        for (let x = 0; x < canvasW; x += 2) {
            if (abs(sin(k * x)) > 0.995) {
                fill(168, 155, 200);
                ellipse(x, midY, 10, 10);
                fill(185, 175, 215);
                textSize(9);
                textAlign(CENTER);
                text('腹', x, midY + 20);
            }
        }

    }

    function drawSuperposition() {
        let k = TWO_PI / lambda;
        let omega = TWO_PI * f;
        let midY = canvasH / 2;

        // Wave 1 (rightward)
        noFill();
        stroke(168, 161, 226, 200);
        strokeWeight(2);
        strokeDash(8);
        beginShape();
        for (let x = 0; x < canvasW; x += 2) {
            let y = midY + A * sin(k * x - omega * time);
            vertex(x, y);
        }
        endShape();

        // Wave 2 (leftward, half amplitude)
        stroke(245, 168, 212, 200);
        strokeWeight(2);
        beginShape();
        for (let x = 0; x < canvasW; x += 2) {
            let y = midY + A * 0.6 * sin(k * x + omega * time);
            vertex(x, y);
        }
        endShape();
        noDash();

        // Resultant
        stroke(177, 156, 217, 255);
        strokeWeight(3);
        beginShape();
        for (let x = 0; x < canvasW; x += 2) {
            let y1 = A * sin(k * x - omega * time);
            let y2 = A * 0.6 * sin(k * x + omega * time);
            let y = midY + y1 + y2;
            vertex(x, y);
        }
        endShape();

        // Legend
        noStroke();
        fill(168, 161, 226);
        textSize(12);
        textAlign(LEFT, TOP);
        text('━ y₁ (右方向)', 15, 15);
        fill(245, 168, 212);
        text('━ y₂ (左方向)', 15, 35);
        fill(177, 156, 217);
        text('━ y₁ + y₂ (合成波)', 15, 55);
    }

    function drawLabels() {
        // Info overlay
        noStroke();
        fill(90, 90, 110, 180);
        textSize(11);
        textAlign(RIGHT, BOTTOM);
        let T = (1 / f).toFixed(3);
        let kNum = (TWO_PI / lambda).toFixed(3);
        let omega = (TWO_PI * f).toFixed(3);
        let info = 'T=' + T + 's | k=' + kNum + ' | ω=' + omega + ' rad/s';
        text(info, canvasW - 10, canvasH - 10);
    }

    function strokeDash(d) {
        drawingContext.setLineDash([d, d]);
    }
    function noDash() {
        drawingContext.setLineDash([]);
    }

    // ===================== CONTROLS =====================
    function updateParam() {
        A = parseFloat(document.getElementById('amplitude').value);
        f = parseFloat(document.getElementById('frequency').value);
        lambda = parseFloat(document.getElementById('wavelength').value);
        v = parseFloat(document.getElementById('speed').value);

        document.getElementById('ampVal').textContent = A;
        document.getElementById('freqVal').textContent = f.toFixed(1);
        document.getElementById('waveVal').textContent = lambda;
        document.getElementById('speedVal').textContent = v;

        let calcV = f * lambda;
        document.getElementById('calcDisplay').innerHTML =
            `v = ${f.toFixed(1)} × ${lambda} = <b>${calcV.toFixed(0)}</b> px/s`;
    }

    function setWaveType(type) {
        waveType = type;
        document.querySelectorAll('.wave-type-btn').forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');
    }

    function switchTab(tabName) {
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('tab-' + tabName).classList.add('active');
        event.target.classList.add('active');
    }