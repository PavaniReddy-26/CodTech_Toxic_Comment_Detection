const commentInput = document.getElementById('commentInput');
const charCount = document.getElementById('charCount');
const scanBtn = document.getElementById('scanBtn');
const scanLine = document.getElementById('scanLine');
const errorMsg = document.getElementById('errorMsg');
const resultList = document.getElementById('resultList');
const resultHint = document.getElementById('resultHint');
const verdict = document.getElementById('verdict');

const TIER_ORDER = { high: 0, mid: 1, safe: 2 };

commentInput.addEventListener('input', () => {
  charCount.textContent = commentInput.value.length;
});

commentInput.addEventListener('keydown', (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
    runScan();
  }
});

scanBtn.addEventListener('click', runScan);

async function runScan() {
  const comment = commentInput.value.trim();
  errorMsg.textContent = '';

  if (!comment) {
    errorMsg.textContent = 'Please enter a comment to analyze.';
    return;
  }

  setLoading(true);

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comment })
    });

    const data = await response.json();

    if (!response.ok) {
      errorMsg.textContent = data.error || 'Something went wrong. Please try again.';
      setLoading(false);
      return;
    }

    renderResults(data.results);
  } catch (err) {
    errorMsg.textContent = 'Could not reach the server. Please try again.';
  } finally {
    setLoading(false);
  }
}

function setLoading(isLoading) {
  scanBtn.disabled = isLoading;
  scanBtn.querySelector('.scan-btn-label').textContent = isLoading ? 'Analyzing…' : 'Analyze comment';
  scanLine.classList.toggle('active', isLoading);
}

function renderResults(results) {
  resultHint.style.display = 'none';
  resultList.innerHTML = '';

  const highestNonNeutral = results
    .filter(r => r.key !== 'neutral')
    .reduce((max, r) => Math.max(max, r.score), 0);

  const flagged = highestNonNeutral >= 50;
  verdict.textContent = flagged ? 'Flagged' : 'Looks safe';
  verdict.classList.toggle('is-flagged', flagged);
  verdict.classList.toggle('is-safe', !flagged);

  results.forEach((item, i) => {
    const row = document.createElement('div');
    row.className = 'result-row';
    row.innerHTML = `
      <span class="result-label">${item.label}</span>
      <span class="result-track"><span class="result-fill tier-${item.tier}"></span></span>
      <span class="result-score">${item.score.toFixed(1)}%</span>
    `;
    resultList.appendChild(row);

    const fill = row.querySelector('.result-fill');
    setTimeout(() => {
      fill.style.width = `${item.score}%`;
    }, 60 + i * 70);
  });
}
