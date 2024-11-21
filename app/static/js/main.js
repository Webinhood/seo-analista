document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const statusDiv = document.getElementById('statusMessage');
    const statusText = document.getElementById('currentStatus');
    const progressBar = document.getElementById('progressBar');
    const top3Content = document.getElementById('top3Content');
    const othersContent = document.getElementById('othersContent');

    function updateProgress(progress) {
        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute('aria-valuenow', progress);
    }

    function updateStatus(message, progress) {
        statusText.textContent = message;
        statusDiv.classList.remove('d-none');
        if (progress !== undefined) {
            updateProgress(progress);
        }
    }

    searchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const keyword = document.getElementById('keyword').value;
        const language = document.getElementById('language').value;
        
        // Mostrar loading e status, esconder resultados
        loadingDiv.classList.remove('d-none');
        statusDiv.classList.remove('d-none');
        resultsDiv.classList.add('d-none');
        clearResults();
        updateProgress(0);

        try {
            updateStatus('Iniciando busca no Google...', 10);
            const response = await fetch('/seo/scrape-content', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    keyword: keyword,
                    language: language
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            updateStatus('Processando resultados...', 30);
            const data = await response.json();
            
            updateStatus('Exibindo resultados...', 60);
            displayResults(data);
            
            // Só esconder o status depois que tudo estiver pronto
            if (data.status === "Análise completa") {
                updateStatus('Análise completa!', 100);
                setTimeout(() => {
                    statusDiv.classList.add('d-none');
                }, 2000);
            }
        } catch (error) {
            showError('Erro ao processar a requisição: ' + error.message);
            statusDiv.classList.add('d-none');
        } finally {
            loadingDiv.classList.add('d-none');
        }
    });

    function displayResults(data) {
        // Mostrar div de resultados
        resultsDiv.classList.remove('d-none');

        // Processar top 3 resultados
        let top3Html = '';
        let progress = 60;
        const progressStep = 20 / Object.keys(data.top3_content).length;
        
        for (const [url, content] of Object.entries(data.top3_content)) {
            updateStatus(content.status, progress);
            progress += progressStep;
            top3Html += `
                <div class="mb-4">
                    <h3 class="h5">
                        <a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>
                    </h3>
                    <div class="content-box">
                        ${content.content}
                    </div>
                </div>
            `;
        }
        top3Content.innerHTML = top3Html;

        // Processar outros resultados
        let othersHtml = '';
        const remainingProgressStep = 20 / Object.keys(data.remaining_headings).length;
        
        for (const [url, content] of Object.entries(data.remaining_headings)) {
            updateStatus(content.status, progress);
            progress += remainingProgressStep;
            othersHtml += `
                <div class="mb-4">
                    <h3 class="h5">
                        <a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>
                    </h3>
                    <ul class="list-unstyled">
                        ${content.headings.map(heading => `<li>${heading}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        othersContent.innerHTML = othersHtml;

        // Atualizar status final
        if (data.status) {
            updateStatus(data.status, 100);
        }
    }

    function clearResults() {
        top3Content.innerHTML = '';
        othersContent.innerHTML = '';
    }

    function showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        resultsDiv.classList.remove('d-none');
        top3Content.innerHTML = '';
        top3Content.appendChild(errorDiv);
    }
});
