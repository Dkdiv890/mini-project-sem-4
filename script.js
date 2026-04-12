document.addEventListener('DOMContentLoaded', () => {
  const uploadZone = document.getElementById('uploadZone');
  const fileInput = document.getElementById('fileInput');
  const uploadBtn = document.getElementById('uploadBtn');
  const previewZone = document.getElementById('previewZone');
  const previewImg = document.getElementById('previewImg');
  const backBtn = document.getElementById('backBtn');
  const predictBtn = document.getElementById('predictBtn');
  const resultsZone = document.getElementById('resultsZone');
  const retryBtn = document.getElementById('retryBtn');
  const previewOverlay = document.getElementById('previewOverlay');
  const resultClass = document.getElementById('resultClass');
  const resultConfidence = document.getElementById('resultConfidence');
  const resultBars = document.getElementById('resultBars');
  const resultTip = document.getElementById('resultTip');
  const resultIcon = document.getElementById('resultIcon');

  let currentFile = null;

  const tips = {
    'metal': 'Recyclable. Ensure it is clean of food residue.',
    'paper': 'Recyclable. Avoid wet or greasy paper/cardboard.',
    'plastic': 'Recyclable. Check local guidelines for specific plastic types.'
  };

  const icons = {
    'metal': '🔩',
    'paper': '📄',
    'plastic': '🧴'
  };

  uploadBtn.addEventListener('click', () => fileInput.click());

  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      handleFile(e.target.files[0]);
    }
  });

  uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('active');
  });

  uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('active');
  });

  uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('active');
    if (e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  });

  function handleFile(file) {
    if (!file.type.startsWith('image/')) {
      alert('Please upload an image file.');
      return;
    }
    currentFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImg.src = e.target.result;
      uploadZone.classList.add('hidden');
      previewZone.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
  }

  backBtn.addEventListener('click', () => {
    uploadZone.classList.remove('hidden');
    previewZone.classList.add('hidden');
    currentFile = null;
    fileInput.value = '';
  });

  predictBtn.addEventListener('click', async () => {
    if (!currentFile) return;

    previewOverlay.classList.add('active');
    predictBtn.disabled = true;

    const formData = new FormData();
    formData.append('file', currentFile);

    try {
      const response = await fetch('/predict', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      showResults(data);
    } catch (err) {
      alert('Error: ' + err.message);
      previewOverlay.classList.remove('active');
      predictBtn.disabled = false;
    }
  });

  function showResults(data) {
    previewZone.classList.add('hidden');
    resultsZone.classList.remove('hidden');

    resultClass.textContent = data.top_class.charAt(0).toUpperCase() + data.top_class.slice(1);
    resultConfidence.textContent = `${data.confidence}% confidence`;
    resultIcon.textContent = icons[data.top_class] || '🏆';
    resultTip.textContent = tips[data.top_class] || '';

    resultBars.innerHTML = '';
    Object.entries(data.predictions).forEach(([label, value]) => {
      const barWrapper = document.createElement('div');
      barWrapper.className = 'bar-wrapper';

      const barLabel = document.createElement('div');
      barLabel.className = 'bar-metadata';
      barLabel.innerHTML = `<span>${label.charAt(0).toUpperCase() + label.slice(1)}</span><span>${value.toFixed(1)}%</span>`;

      const barContainer = document.createElement('div');
      barContainer.className = 'bar-container';

      const barInner = document.createElement('div');
      barInner.className = 'bar-inner ' + label;
      barInner.style.width = '0%';
      
      barWrapper.appendChild(barLabel);
      barContainer.appendChild(barInner);
      barWrapper.appendChild(barContainer);
      resultBars.appendChild(barWrapper);

      setTimeout(() => {
        barInner.style.width = `${value}%`;
      }, 100);
    });

    previewOverlay.classList.remove('active');
    predictBtn.disabled = false;
  }

  retryBtn.addEventListener('click', () => {
    resultsZone.classList.add('hidden');
    uploadZone.classList.remove('hidden');
    currentFile = null;
    fileInput.value = '';
  });
});
