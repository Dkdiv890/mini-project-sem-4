const uploadZone = document.getElementById('uploadZone');
const uploadBtn = document.getElementById('uploadBtn');
const fileInput = document.getElementById('fileInput');
const previewZone = document.getElementById('previewZone');
const previewImg = document.getElementById('previewImg');
const previewOverlay = document.getElementById('previewOverlay');
const predictBtn = document.getElementById('predictBtn');
const predictBtnText = document.getElementById('predictBtnText');
const resultsZone = document.getElementById('resultsZone');
const backBtn = document.getElementById('backBtn');
const retryBtn = document.getElementById('retryBtn');
const resultIcon = document.getElementById('resultIcon');
const resultClass = document.getElementById('resultClass');
const resultConfidence = document.getElementById('resultConfidence');
const resultBars = document.getElementById('resultBars');
const resultTip = document.getElementById('resultTip');

let selectedFile = null;

const CLASS_ICONS = { metal: '🔩', paper: '📄', plastic: '🧴' };
const CLASS_TIPS = {
  metal: '♻️ Metal is 100% recyclable! Take it to a metal recycling bin or scrap dealer. Recycling aluminium saves up to 95% of the energy needed to make new metal.',
  paper: '📦 Paper is easily recyclable! Ensure it is dry and uncontaminated. Recycling paper saves trees and reduces landfill waste significantly.',
  plastic: '🪣 Plastic recycling depends on the type. Check the recycling number on the item. Avoid single-use plastics and prefer reusable alternatives!'
};

function showSection(zone) {
  uploadZone.classList.add('hidden');
  previewZone.classList.add('hidden');
  resultsZone.classList.add('hidden');
  zone.classList.remove('hidden');
}

function handleFile(file) {
  if (!file || !file.type.startsWith('image/')) return;
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    showSection(previewZone);
  };
  reader.readAsDataURL(file);
}

uploadZone.addEventListener('click', () => fileInput.click());
uploadBtn.addEventListener('click', (e) => { e.stopPropagation(); fileInput.click(); });
fileInput.addEventListener('change', (e) => { if (e.target.files[0]) handleFile(e.target.files[0]); });

uploadZone.addEventListener('dragover', (e) => { e.preventDefault(); uploadZone.classList.add('drag-over'); });
uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('drag-over'));
uploadZone.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadZone.classList.remove('drag-over');
  if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
});

backBtn.addEventListener('click', () => {
  selectedFile = null;
  fileInput.value = '';
  showSection(uploadZone);
});

retryBtn.addEventListener('click', () => {
  selectedFile = null;
  fileInput.value = '';
  previewOverlay.classList.remove('active');
  predictBtn.disabled = false;
  predictBtnText.textContent = '🔍 Classify Waste';
  showSection(uploadZone);
});

predictBtn.addEventListener('click', async () => {
  if (!selectedFile) return;
  predictBtn.disabled = true;
  predictBtnText.textContent = 'Analyzing...';
  previewOverlay.classList.add('active');

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const response = await fetch('/predict', { method: 'POST', body: formData });
    const data = await response.json();
    if (data.error) throw new Error(data.error);
    renderResults(data);
  } catch (err) {
    alert('Error: ' + err.message);
    predictBtn.disabled = false;
    predictBtnText.textContent = '🔍 Classify Waste';
    previewOverlay.classList.remove('active');
  }
});

function renderResults(data) {
  resultIcon.textContent = CLASS_ICONS[data.top_class] || '🏆';
  resultClass.textContent = data.top_class.charAt(0).toUpperCase() + data.top_class.slice(1);
  resultConfidence.textContent = `${data.confidence}% confidence`;
  resultTip.textContent = CLASS_TIPS[data.top_class] || '';

  resultBars.innerHTML = '';
  const sorted = Object.entries(data.predictions).sort((a, b) => b[1] - a[1]);
  sorted.forEach(([cls, pct]) => {
    const row = document.createElement('div');
    row.className = `bar-row`;
    row.innerHTML = `
      <div class="bar-label">
        <span>${CLASS_ICONS[cls]} ${cls.charAt(0).toUpperCase() + cls.slice(1)}</span>
        <span>${pct.toFixed(1)}%</span>
      </div>
      <div class="bar-track">
        <div class="bar-fill bar-${cls}" style="width:0%"></div>
      </div>`;
    resultBars.appendChild(row);
  });

  showSection(resultsZone);
  previewOverlay.classList.remove('active');
  predictBtn.disabled = false;
  predictBtnText.textContent = '🔍 Classify Waste';

  requestAnimationFrame(() => {
    sorted.forEach(([cls, pct]) => {
      const fill = resultBars.querySelector(`.bar-${cls}`);
      if (fill) fill.style.width = pct + '%';
    });
  });
}
