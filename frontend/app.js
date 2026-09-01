let currentSessionId = null;
let currentState = null;

function switchTab(tabId) {
    document.getElementById('tab-draft').classList.add('hidden');
    document.getElementById('tab-sources').classList.add('hidden');
    document.getElementById('tab-json').classList.add('hidden');
    document.getElementById(`tab-${tabId}`).classList.remove('hidden');
}

function formatMarkdown(text) {
    if (!text) return "";
    let html = text.replace(/### (.*)/g, '<h3 class="text-xl font-bold mt-6 mb-2 border-b pb-1">$1</h3>');
    html = html.replace(/#### (.*)/g, '<h4 class="text-lg font-semibold mt-4 mb-2">$1</h4>');
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    html = html.replace(/\n\n/g, '</p><p class="mb-4">');
    html = html.replace(/\n- (.*)/g, '<li class="ml-4 list-disc">$1</li>');
    return `<p class="mb-4">${html}</p>`;
}

function updateUI(state) {
    currentState = state;
    currentSessionId = state.session_id;
    document.getElementById('session-id-display').textContent = currentSessionId.substring(0, 8) + '...';
    document.getElementById('state-json').textContent = JSON.stringify(state, null, 2);
    
    if (state.topic) {
        document.getElementById('doc-title').textContent = state.topic;
    }
    
    const docContent = document.getElementById('doc-content');
    if (Object.keys(state.manuscript_draft).length > 0) {
        let htmlContent = "";
        
        Object.keys(state.manuscript_draft).forEach(section => {
            if (state.manuscript_draft[section]) {
                htmlContent += formatMarkdown(state.manuscript_draft[section]);
            }
        });
        
        docContent.innerHTML = htmlContent;
    }
    
    const sourceList = document.getElementById('source-list');
    if (state.sources && state.sources.length > 0) {
        let htmlSources = "";
        state.sources.forEach(src => {
            let badgeColor = src.status === 'VERIFIED' ? 'bg-green-100 text-green-800' : 
                             src.status === 'REJECTED' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800';
            htmlSources += `
                <div class="bg-white p-4 border border-gray-200 rounded shadow-sm">
                    <div class="flex justify-between items-start">
                        <h4 class="font-semibold text-blue-900">${src.title}</h4>
                        <span class="text-xs px-2 py-1 rounded font-bold ${badgeColor}">${src.status}</span>
                    </div>
                    <p class="text-sm text-gray-600 mt-1">${src.authors.join(', ')} (${src.year}) - <em>${src.journal}</em></p>
                    <div class="mt-2 text-xs text-gray-500 bg-gray-50 p-2 rounded">
                        <strong>Agent Note:</strong> ${src.metadata.verification_note || 'Awaiting verification'}
                    </div>
                </div>
            `;
        });
        sourceList.innerHTML = htmlSources;
    }
}

function appendMessage(sender, text, isUser) {
    const chatBox = document.getElementById('chat-box');
    const alignClass = isUser ? 'items-end' : 'items-start';
    const bgClass = isUser ? 'bg-blue-600 text-white rounded-br-none' : 'bg-gray-100 text-gray-800 rounded-tl-none border border-gray-200';
    const title = isUser ? 'You' : sender;
    
    const msgHtml = `
        <div class="flex flex-col ${alignClass} space-y-1">
            <span class="text-xs text-gray-500 font-bold mx-2">${title}</span>
            <div class="${bgClass} p-3 rounded-lg text-sm inline-block max-w-[90%] shadow-sm">
                ${text}
            </div>
        </div>
    `;
    
    chatBox.insertAdjacentHTML('beforeend', msgHtml);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Handle Auto-Generate Submit
document.getElementById('auto-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    document.getElementById('auto-modal').classList.add('hidden');
    
    const title = document.getElementById('auto-title').value;
    const publisher = document.getElementById('auto-publisher').value;
    const journal = document.getElementById('auto-journal').value;
    const type = document.getElementById('auto-type').value;
    const rqs = document.getElementById('auto-rqs').value.split(',').filter(x => x.trim() !== '');
    const objs = document.getElementById('auto-objs').value.split(',').filter(x => x.trim() !== '');
    
    appendMessage('You', `[Auto-Generate Request]\nTitle: ${title}\nPublisher: ${publisher}\nType: ${type}`, true);
    appendMessage('System Orchestrator', 'Initiating publisher style analysis and generation. This may take a moment...', false);
    
    try {
        const response = await fetch('/api/v1/generate_paper', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: title,
                target_publisher: publisher,
                target_journal: journal,
                article_type: type,
                research_questions: rqs.length > 0 ? rqs : null,
                objectives: objs.length > 0 ? objs : null
            })
        });
        
        if (!response.ok) throw new Error('API Error');
        const data = await response.json();
        
        appendMessage('System Orchestrator', 'Paper generated successfully! All sources checked against Q1-Q3 Scopus/WoS rules. Tone refined for zero AI plagiarism.', false);
        updateUI(data.state);
        
    } catch (error) {
        appendMessage('System', 'Error generating paper. Ensure backend is running.', false);
    }
});

// Original Chat Submit
document.getElementById('chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const inputField = document.getElementById('chat-input');
    const message = inputField.value.trim();
    if (!message) return;
    
    const phase = document.getElementById('agent-selector').value;
    const phaseText = document.getElementById('agent-selector').options[document.getElementById('agent-selector').selectedIndex].text;
    
    appendMessage('You', message, true);
    inputField.value = '';
    
    try {
        const response = await fetch('/api/v1/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: currentSessionId,
                phase: phase,
                message: message
            })
        });
        
        if (!response.ok) throw new Error('API Error');
        const data = await response.json();
        appendMessage(phaseText, data.response, false);
        updateUI(data.state);
    } catch (error) {
        appendMessage('System', 'Error communicating with the backend.', false);
    }
});
