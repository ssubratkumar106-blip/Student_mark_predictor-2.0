document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initPredictForm();
    initCounters();
});

function initTheme() {
    const toggle = document.getElementById('themeToggle');
    const html = document.documentElement;
    const saved = localStorage.getItem('theme') || 'dark';
    html.setAttribute('data-theme', saved);
    updateThemeIcon(saved);

    toggle?.addEventListener('click', () => {
        const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        updateThemeIcon(next);
    });
}

function updateThemeIcon(theme) {
    const icon = document.querySelector('#themeToggle i');
    if (icon) icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
}

function initPredictForm() {
    const form = document.getElementById('predictForm');
    const input = document.getElementById('study_hours');
    const btn = document.getElementById('predictBtn');
    if (!form || !input) return;

    form.addEventListener('submit', (e) => {
        const value = parseFloat(input.value);
        if (isNaN(value) || value <= 0 || value > 24) {
            e.preventDefault();
            alert('Enter study hours between 0 and 24.');
            return;
        }
        btn.querySelector('.btn-text')?.classList.add('hidden');
        btn.querySelector('.btn-loader')?.classList.remove('hidden');
        btn.disabled = true;
    });
}

function initCounters() {
    document.querySelectorAll('.counter').forEach((el) => {
        const target = parseFloat(el.dataset.target) || 0;
        let current = 0;
        const step = target / 40;
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                el.textContent = Number.isInteger(target) ? target : target.toFixed(2);
                clearInterval(timer);
            } else {
                el.textContent = current.toFixed(2);
            }
        }, 30);
    });
}

function renderPredictionChart(data) {
    const canvas = document.getElementById('predictionChart');
    if (!canvas || typeof Chart === 'undefined') return;

    new Chart(canvas, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Training Data',
                    data: data.train_hours.map((h, i) => ({ x: h, y: data.train_marks[i] })),
                    backgroundColor: 'rgba(99, 102, 241, 0.7)',
                    pointRadius: 4,
                },
                {
                    label: 'Regression Line',
                    data: data.line_x.map((x, i) => ({ x, y: data.line_y[i] })),
                    type: 'line',
                    borderColor: '#a78bfa',
                    backgroundColor: 'transparent',
                    pointRadius: 0,
                    borderWidth: 2,
                    tension: 0.1,
                },
                {
                    label: 'Your Prediction',
                    data: [{ x: data.pred_hours, y: data.pred_marks }],
                    backgroundColor: '#34d399',
                    borderColor: '#10b981',
                    pointRadius: 9,
                    pointHoverRadius: 11,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { labels: { color: '#cbd5e1' } },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `${ctx.dataset.label}: (${ctx.parsed.x}h, ${ctx.parsed.y} marks)`,
                    },
                },
            },
            scales: {
                x: {
                    title: { display: true, text: 'Study Hours', color: '#94a3b8' },
                    ticks: { color: '#94a3b8' },
                    grid: { color: 'rgba(148,163,184,0.15)' },
                },
                y: {
                    title: { display: true, text: 'Marks', color: '#94a3b8' },
                    min: 0,
                    max: 100,
                    ticks: { color: '#94a3b8' },
                    grid: { color: 'rgba(148,163,184,0.15)' },
                },
            },
        },
    });
}
