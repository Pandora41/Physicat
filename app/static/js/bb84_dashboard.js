// static/js/bb84_dashboard.js

let chart = null;

function updateAttackParams() {
    const attackType = document.getElementById('attack-type').value;
    const paramsDiv = document.getElementById('attack-params');
    const paramInput = document.getElementById('attack-param-value');
    const description = document.getElementById('param-description');

    if (attackType === 'none' || attackType === 'intercept_resend') {
        paramsDiv.style.display = 'none';
        return;
    }

    paramsDiv.style.display = 'block';

    if (attackType === 'partial_intercept') {
        paramInput.min = 0;
        paramInput.max = 1;
        paramInput.step = 0.05;
        paramInput.value = 0.2;
        description.textContent = 'Eveが傍受する光子の割合 (0.0 ~ 1.0)';
    } else if (attackType === 'pns') {
        paramInput.min = 0.01;
        paramInput.max = 1;
        paramInput.step = 0.01;
        paramInput.value = 0.1;
        description.textContent = '平均光子数 μ (0.01 ~ 1.0)';
    }
}

async function runSimulation() {
    const nPhotons = parseInt(document.getElementById('n-photons').value);
    const noise = parseFloat(document.getElementById('noise').value);
    const attackType = document.getElementById('attack-type').value;
    const paramValue = parseFloat(document.getElementById('attack-param-value').value);

    const payload = {
        n_photons: nPhotons,
        noise: noise,
        attack_type: attackType,
        attack_params: {}
    };

    if (attackType === 'partial_intercept') {
        payload.attack_params.rate = paramValue;
    } else if (attackType === 'pns') {
        payload.attack_params.mu = paramValue;
    }

    try {
        // Show loading
        const btn = document.getElementById('run-btn');
        btn.disabled = true;
        btn.textContent = '⏳ 実行中...';

        const response = await fetch('/api/v1/bb84/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        // Reset button
        btn.disabled = false;
        btn.textContent = '🚀 シミュレーション実行';

        if (result.success) {
            displayResults(result);
            
            // ✅ SELALU jalankan sweep untuk tampilkan chart
            await runSweep(attackType, noise);
        } else {
            alert('シミュレーション失敗: ' + result.error);
        }
    } catch (error) {
        alert('エラー: ' + error.message);
        document.getElementById('run-btn').disabled = false;
        document.getElementById('run-btn').textContent = '🚀 シミュレーション実行';
    }
}

function displayResults(result) {
    document.getElementById('results-panel').style.display = 'grid';
    
    document.getElementById('qber-value').textContent = 
        (result.qber * 100).toFixed(2) + '%';
    document.getElementById('key-length').textContent = 
        result.sifted_key_length;
    document.getElementById('eve-info').textContent = 
        result.eve_information.toFixed(4) + ' bits';
    document.getElementById('n-errors').textContent = 
        result.n_errors || 0;

    const detectionDiv = document.getElementById('detection-result');
    
    if (result.qber > 0.11) {
        detectionDiv.innerHTML = `
            <div class="bb84-detection danger">
                <div class="bb84-detection-title">⚠️ 盗聴検出！</div>
                <p>QBERが11%を超えています。Eveが通信を盗聴している可能性が高いです。鍵を破棄してください。</p>
            </div>
        `;
    } else {
        detectionDiv.innerHTML = `
            <div class="bb84-detection safe">
                <div class="bb84-detection-title">✅ 安全！</div>
                <p>QBERが許容範囲内です。盗聴の兆候は見られません。安全な鍵が生成されました。</p>
            </div>
        `;
    }
}

async function runSweep(attackType, baseNoise) {
    const paramValues = [];
    let paramLabel = '';
    
    if (attackType === 'none' || attackType === 'intercept_resend') {
        for (let i = 0; i <= 10; i++) paramValues.push(i / 100);
        paramLabel = 'ノイズ率';
    } else if (attackType === 'partial_intercept') {
        for (let i = 0; i <= 10; i++) paramValues.push(i / 10);
        paramLabel = '傍受率';
    } else if (attackType === 'pns') {
        for (let i = 1; i <= 10; i++) paramValues.push(i / 10);
        paramLabel = '平均光子数';
    }

    // ✅ Tampilkan chart container + loading
    const container = document.getElementById('chart-container');
    const loading = document.getElementById('chart-loading');
    const canvas = document.getElementById('qber-chart');
    
    container.style.display = 'block';
    loading.style.display = 'flex';
    canvas.style.display = 'none';

    try {
        const response = await fetch('/api/v1/bb84/sweep', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                attack_type: attackType,
                param_values: paramValues,
                base_noise: baseNoise
            })
        });

        const result = await response.json();

        if (result.success) {
            displayChart(result.results, attackType, paramLabel);
        }
    } catch (error) {
        console.error('[BB84] Sweep error:', error);
        loading.style.display = 'none';
    }
}

function displayChart(results, attackType, paramLabel) {
    // ✅ Hide loading, show canvas
    document.getElementById('chart-loading').style.display = 'none';
    document.getElementById('qber-chart').style.display = 'block';
    
    const ctx = document.getElementById('qber-chart').getContext('2d');
    
    if (chart) {
        chart.destroy();
    }

    const labels = results.map(r => r.param.toFixed(2));
    const qberData = results.map(r => r.qber * 100);
    const eveInfoData = results.map(r => r.eve_info);

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'QBER (%)',
                    data: qberData,
                    borderColor: '#a89bc8',
                    backgroundColor: 'rgba(168, 155, 200, 0.15)',
                    yAxisID: 'y',
                    tension: 0.35,
                    fill: true,
                    borderWidth: 2.5,
                    pointBackgroundColor: '#a89bc8',
                    pointRadius: 4
                },
                {
                    label: 'Eveの情報量 (bits)',
                    data: eveInfoData,
                    borderColor: '#f5a8d4',
                    backgroundColor: 'rgba(245, 168, 212, 0.15)',
                    yAxisID: 'y1',
                    tension: 0.35,
                    fill: true,
                    borderWidth: 2.5,
                    pointBackgroundColor: '#f5a8d4',
                    pointRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#5a5a6e', font: { size: 12 } }
                },
                title: {
                    display: true,
                    text: `${paramLabel} vs QBER & Eve情報量`,
                    color: '#7c6394',
                    font: { size: 15, weight: '600' }
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    position: 'left',
                    title: { display: true, text: 'QBER (%)', color: '#8b7a9e' },
                    ticks: { color: '#8b7a9e' }
                },
                y1: {
                    type: 'linear',
                    position: 'right',
                    title: { display: true, text: 'Eve情報量 (bits)', color: '#8b7a9e' },
                    ticks: { color: '#8b7a9e' },
                    grid: { drawOnChartArea: false }
                },
                x: {
                    title: { display: true, text: paramLabel, color: '#8b7a9e' },
                    ticks: { color: '#8b7a9e' }
                }
            }
        }
    });
}