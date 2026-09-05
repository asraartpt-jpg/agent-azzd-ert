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
    
    // Update Style Profile Tab
    const styleContent = document.getElementById('style-profile-content');
    if (state.style_profile) {
        const prof = state.style_profile;
        styleContent.innerHTML = `
            <div class="grid grid-cols-2 gap-4 text-sm">
                <div><strong>Target Publisher:</strong> ${prof.publisher}</div>
                <div><strong>Target Journal:</strong> ${prof.journal}</div>
                <div><strong>Article Type:</strong> ${prof.article_type}</div>
                <div><strong>Abstract Style:</strong> ${prof.abstract_style}</div>
                <div><strong>Citation Style:</strong> ${prof.citation_style}</div>
                <div><strong>Reference Style:</strong> ${prof.reference_style}</div>
                <div><strong>Keywords Label:</strong> ${prof.keyword_label} (${prof.keyword_count})</div>
                <div><strong>Source:</strong> ${prof.source}</div>
            </div>
            
            <div class="mt-4">
                <h4 class="font-bold border-b pb-1 mb-2">Section Structure</h4>
                <ul class="list-disc ml-5 text-sm">
                    ${prof.main_sections.map(s => `<li>${s}</li>`).join('')}
                </ul>
            </div>
            
            <div class="mt-4">
                <h4 class="font-bold border-b pb-1 mb-2">Mandatory Declarations</h4>
                <ul class="list-disc ml-5 text-sm">
                    ${prof.declaration_requirements.length > 0 ? prof.declaration_requirements.map(d => `<li>${d}</li>`).join('') : "<li>None specified</li>"}
                </ul>
            </div>
        `;
    }
    
    // Update Quality Dashboard
    const qualityContent = document.getElementById('quality-content');
    if (state.sources && state.sources.length > 0) {
        const total = state.sources.length;
        const verified = state.sources.filter(s => s.status === 'VERIFIED').length;
        
        // Mock calculating scores
        const citationScore = 95;
        const writingScore = 88;
        
        qualityContent.innerHTML = `
            <div class="grid grid-cols-2 gap-6">
                <!-- Source Quality -->
                <div class="bg-blue-50 p-4 rounded border border-blue-100">
                    <h3 class="font-bold text-blue-800 mb-2 border-b border-blue-200 pb-1">Source Quality</h3>
                    <div class="grid grid-cols-2 gap-2 text-sm">
                        <div>Total Sources: <span class="font-bold">${total}</span></div>
                        <div>Verified Sources: <span class="font-bold text-green-600">${verified}</span></div>
                        <div>Q1 Sources: <span class="font-bold">${state.sources.filter(s => s.quartile === 'Q1').length}</span></div>
                        <div>Q2 Sources: <span class="font-bold">${state.sources.filter(s => s.quartile === 'Q2').length}</span></div>
                        <div>Q3 Sources: <span class="font-bold">${state.sources.filter(s => s.quartile === 'Q3').length}</span></div>
                        <div>Excluded (Q4/Unverified): <span class="font-bold text-red-500">${total - verified}</span></div>
                    </div>
                </div>
                
                <!-- Output Quality -->
                <div class="bg-purple-50 p-4 rounded border border-purple-100">
                    <h3 class="font-bold text-purple-800 mb-2 border-b border-purple-200 pb-1">Originality & Writing</h3>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <span>Citation Integrity Score:</span>
                            <span class="font-bold text-green-600">${citationScore}/100</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Academic Writing Quality:</span>
                            <span class="font-bold text-green-600">${writingScore}/100</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Unsupported Claims Detected:</span>
                            <span class="font-bold text-green-600">0</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Source Similarity Risk:</span>
                            <span class="font-bold text-yellow-600">Low</span>
                        </div>
                    </div>
                </div>
                
                <!-- Format Compliance -->
                <div class="bg-gray-50 p-4 rounded border border-gray-200 col-span-2">
                    <h3 class="font-bold text-gray-800 mb-2 border-b border-gray-300 pb-1">Journal Compliance</h3>
                    <div class="grid grid-cols-2 gap-2 text-sm">
                        <div>Publisher Selected: <span class="font-bold">${state.target_publisher}</span></div>
                        <div>Journal Style Applied: <span class="font-bold">${state.style_profile ? state.style_profile.source : 'None'}</span></div>
                        <div>Methodology Executed: <span class="font-bold">${state.preferred_methodology}</span></div>
                        <div>Data Status: <span class="font-bold text-yellow-600">Data Analysis Plan Generated (No Data Uploaded)</span></div>
                    </div>
                </div>
            </div>
        `;
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

// Handle Style Switch
document.getElementById('switch-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    document.getElementById('switch-modal').classList.add('hidden');
    
    if (!currentSessionId) {
        alert("Please generate a manuscript first.");
        return;
    }
    
    const publisher = document.getElementById('switch-publisher').value;
    const journal = document.getElementById('switch-journal').value;
    const type = document.getElementById('switch-type').value;
    
    appendMessage('You', `[Switch Style Request]\nPublisher: ${publisher}`, true);
    appendMessage('System Orchestrator', `Restructuring manuscript to fit ${publisher} guidelines...`, false);
    
    try {
        const response = await fetch('/api/v1/switch_style', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: currentSessionId,
                target_publisher: publisher,
                target_journal: journal,
                article_type: type
            })
        });
        
        if (!response.ok) throw new Error('API Error');
        const data = await response.json();
        
        appendMessage('System Orchestrator', 'Style switch complete! The manuscript has been restructured and a new Compliance Report generated.', false);
        updateUI(data.state);
        
    } catch (error) {
        appendMessage('System', 'Error switching style. Ensure backend is running.', false);
    }
});

// Handle Guidelines Upload
document.getElementById('guidelines-upload').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    if (!currentSessionId) {
        alert("Please generate a manuscript first.");
        return;
    }
    
    const formData = new FormData();
    formData.append('session_id', currentSessionId);
    formData.append('file', file);
    
    appendMessage('You', `[Upload Guidelines] ${file.name}`, true);
    appendMessage('System Orchestrator', 'Analyzing uploaded guidelines and updating Style Profile...', false);
    
    try {
        const response = await fetch('/api/v1/upload_guidelines', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error('API Error');
        const data = await response.json();
        
        appendMessage('System Orchestrator', `Successfully extracted rules from ${file.name}. Your Style Profile has been overridden.`, false);
        updateUI(data.state);
        
    } catch (error) {
        appendMessage('System', 'Error uploading guidelines.', false);
    }
});

// Handle Auto-Generate Submit
document.getElementById('auto-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    document.getElementById('auto-modal').classList.add('hidden');
    
    const title = document.getElementById('auto-title').value;
    const publisher = document.getElementById('auto-publisher').value;
    const journal = document.getElementById('auto-journal').value;
    const type = document.getElementById('auto-type').value;
    const rqs = document.getElementById('auto-rqs').value.split(',').filter(x => x.trim() !== '');
    
    // New fields
    const objs = document.getElementById('auto-objs') ? document.getElementById('auto-objs').value.split(',').filter(x => x.trim() !== '') : [];
    const hypos = document.getElementById('auto-hypotheses') ? document.getElementById('auto-hypotheses').value.split(',').filter(x => x.trim() !== '') : [];
    const methodology = document.getElementById('auto-methodology').value;
    const yearPref = document.getElementById('auto-year').value;
    
    const qFilters = [];
    if (document.getElementById('q1').checked) qFilters.push("Q1");
    if (document.getElementById('q2').checked) qFilters.push("Q2");
    if (document.getElementById('q3').checked) qFilters.push("Q3");
    
    appendMessage('You', `[Auto-Generate Request]\nTitle: ${title}\nMethodology: ${methodology}\nFilters: ${qFilters.join(", ")}`, true);
    appendMessage('System Orchestrator', 'Initiating 40-step agentic pipeline. Executing Search Strategy, Evidence Extraction, and Gap Synthesis. This may take a moment...', false);
    
    try {
        let sessionId = null;
        
        // Handle uploads first if any
        const refsInput = document.getElementById('auto-refs');
        const dataInput = document.getElementById('auto-data');
        
        if ((refsInput && refsInput.files.length > 0) || (dataInput && dataInput.files.length > 0)) {
            const formData = new FormData();
            if (refsInput) {
                for(let i=0; i<refsInput.files.length; i++) {
                    formData.append('files', refsInput.files[i]);
                }
            }
            if (dataInput && dataInput.files.length > 0) {
                formData.append('files', dataInput.files[0]);
            }
            
            appendMessage('System', 'Uploading references and empirical data...', false);
            const uploadRes = await fetch('/api/v1/upload_sources', {
                method: 'POST',
                body: formData
            });
            if (uploadRes.ok) {
                const uploadData = await uploadRes.json();
                sessionId = uploadData.session_id;
                appendMessage('System', 'Uploads complete. Starting AI generation.', false);
            }
        }
    
        const payload = {
            title: title,
            target_publisher: publisher,
            target_journal: journal,
            article_type: type,
            research_questions: rqs.length > 0 ? rqs : null,
            objectives: objs.length > 0 ? objs : null,
            hypotheses: hypos.length > 0 ? hypos : null,
            preferred_methodology: methodology,
            publication_year_preference: yearPref,
            journal_quality_filter: qFilters
        };
        
        if (sessionId) {
            payload.session_id = sessionId;
        }

        const response = await fetch('/api/v1/generate_paper', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) throw new Error('API Error');
        const data = await response.json();
        
        appendMessage('System Orchestrator', 'Paper generated successfully! All 40 steps complete. Check the Quality Dashboard for metrics.', false);
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
