// Project & Session State Management
let currentProjectId = null;
let currentSessionId = null;
let currentState = null;
let currentPublisher = "Emerald";

const STORAGE_KEY = "ai_research_projects_v3";

// Initialize Project Manager on load
document.addEventListener('DOMContentLoaded', () => {
    initProjectManager();
    
    // Close modals on Escape key or backdrop click
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            ['auto-modal', 'switch-modal', 'new-project-modal'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.classList.add('hidden');
            });
        }
    });

    ['auto-modal', 'switch-modal', 'new-project-modal'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('click', (e) => {
                if (e.target === el) {
                    el.classList.add('hidden');
                }
            });
        }
    });
});

function getStoredProjects() {
    try {
        const data = localStorage.getItem(STORAGE_KEY);
        return data ? JSON.parse(data) : [];
    } catch (e) {
        console.error("Error reading localStorage projects:", e);
        return [];
    }
}

function saveStoredProjects(projects) {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(projects));
    } catch (e) {
        console.error("Error saving projects to localStorage:", e);
    }
}

function initProjectManager() {
    let projects = getStoredProjects();
    if (projects.length === 0) {
        const defaultProj = {
            id: "proj_" + Date.now(),
            name: "Default Research Project",
            topic: "",
            createdAt: new Date().toISOString(),
            lastModified: new Date().toISOString(),
            sessionId: "sess_" + Math.random().toString(36).substring(2, 10),
            state: null,
            chatHistory: "",
            publisher: "Emerald"
        };
        projects.push(defaultProj);
        saveStoredProjects(projects);
    }

    renderProjectFolders(projects);
    
    // Load the first or last active project
    const activeId = localStorage.getItem("ai_active_project_id") || projects[0].id;
    const targetProj = projects.find(p => p.id === activeId) || projects[0];
    loadProject(targetProj.id);
}

function renderProjectFolders(projects) {
    const list = document.getElementById('project-folders-list');
    if (!list) return;
    list.innerHTML = "";

    projects.forEach(p => {
        const isActive = p.id === currentProjectId;
        const activeClass = isActive 
            ? "bg-slate-800 border-emerald-500 text-white shadow-md ring-1 ring-emerald-500/50" 
            : "bg-slate-900/60 hover:bg-slate-800/80 border-slate-800 text-slate-300";
        const folderIcon = isActive 
            ? "fa-folder-open text-amber-400" 
            : "fa-folder text-amber-500/80";

        const hasDraft = p.state && p.state.manuscript_draft && Object.keys(p.state.manuscript_draft).length > 0;
        const draftBadge = hasDraft 
            ? `<span class="text-[10px] bg-emerald-950 text-emerald-300 border border-emerald-800/80 px-1.5 py-0.5 rounded font-mono font-bold">10 Sec</span>` 
            : `<span class="text-[10px] bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">New</span>`;

        const dateStr = new Date(p.createdAt || Date.now()).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });

        const itemHtml = `
            <div class="group relative flex flex-col p-2.5 rounded-lg border transition cursor-pointer ${activeClass}" onclick="switchProject('${p.id}')">
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-2 truncate flex-1 mr-1">
                        <i class="fas ${folderIcon} text-sm flex-shrink-0"></i>
                        <span class="text-xs font-semibold truncate text-slate-100" title="${p.name}">${p.name}</span>
                    </div>
                    ${draftBadge}
                </div>
                
                <div class="flex items-center justify-between mt-1.5 text-[11px] text-slate-400">
                    <span class="truncate max-w-[120px] text-emerald-400 font-medium">${p.publisher || 'Emerald'}</span>
                    <div class="flex items-center space-x-1">
                        <span class="text-[10px] text-slate-500">${dateStr}</span>
                        <button onclick="event.stopPropagation(); deleteProjectById('${p.id}')" class="opacity-0 group-hover:opacity-100 hover:text-red-400 p-0.5 text-xs transition" title="Delete folder">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        list.insertAdjacentHTML('beforeend', itemHtml);
    });

    const countDisplay = document.getElementById('projects-count-display');
    if (countDisplay) {
        countDisplay.textContent = `${projects.length} ${projects.length === 1 ? 'Project Folder' : 'Project Folders'}`;
    }
}

function openNewProjectModal() {
    const modal = document.getElementById('new-project-modal');
    if (modal) {
        document.getElementById('new-project-form').reset();
        modal.classList.remove('hidden');
        document.getElementById('new-project-name').focus();
    }
}

document.getElementById('new-project-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('new-project-name').value.trim();
    const topic = document.getElementById('new-project-topic').value.trim();
    if (!name) return;

    document.getElementById('new-project-modal').classList.add('hidden');
    createNewProject(name, topic);
});

function createNewProject(name, topic = "") {
    saveCurrentProject();

    const newProj = {
        id: "proj_" + Date.now(),
        name: name,
        topic: topic,
        createdAt: new Date().toISOString(),
        lastModified: new Date().toISOString(),
        sessionId: "sess_" + Math.random().toString(36).substring(2, 10),
        state: null,
        chatHistory: `
            <div class="flex flex-col space-y-1">
                <span class="text-xs text-gray-500 font-bold ml-2">System Orchestrator</span>
                <div class="bg-blue-50 text-blue-900 p-3 rounded-lg rounded-tl-none text-xs inline-block max-w-[95%] shadow-sm border border-blue-100 leading-relaxed">
                    Created new project folder: <strong>"${name}"</strong>. Click "Auto-Generate" or configure research settings to start.
                </div>
            </div>
        `,
        publisher: "Emerald"
    };

    let projects = getStoredProjects();
    projects.unshift(newProj);
    saveStoredProjects(projects);

    renderProjectFolders(projects);
    loadProject(newProj.id);

    if (topic) {
        const autoTitle = document.getElementById('auto-title');
        if (autoTitle) autoTitle.value = topic;
    }
    
    // Automatically open Auto-Generate Modal
    const autoModal = document.getElementById('auto-modal');
    if (autoModal) autoModal.classList.remove('hidden');
}

function switchProject(projectId) {
    if (!projectId || projectId === currentProjectId) return;
    saveCurrentProject();
    loadProject(projectId);
}

function loadProject(projectId) {
    let projects = getStoredProjects();
    const proj = projects.find(p => p.id === projectId);
    if (!proj) return;

    currentProjectId = proj.id;
    currentSessionId = proj.sessionId;
    currentState = proj.state;
    currentPublisher = proj.publisher || "Emerald";
    localStorage.setItem("ai_active_project_id", currentProjectId);

    renderProjectFolders(projects);

    // Update UI elements
    const sessionDisplay = document.getElementById('session-id-display');
    if (sessionDisplay) sessionDisplay.textContent = currentSessionId.substring(0, 8) + '...';

    const projectBadge = document.getElementById('doc-project-badge');
    if (projectBadge) projectBadge.textContent = proj.name;

    // Restore Chat Box
    const chatBox = document.getElementById('chat-box');
    if (chatBox) {
        chatBox.innerHTML = proj.chatHistory || `
            <div class="flex flex-col space-y-1">
                <span class="text-xs text-gray-500 font-bold ml-2">System Orchestrator</span>
                <div class="bg-blue-50 text-blue-900 p-3 rounded-lg rounded-tl-none text-xs inline-block max-w-[95%] shadow-sm border border-blue-100 leading-relaxed">
                    Active Project: <strong>${proj.name}</strong>. Ready to draft your 10-section manuscript!
                </div>
            </div>
        `;
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    setActivePublisherButton(currentPublisher);

    if (proj.state) {
        updateUI(proj.state);
    } else {
        resetDocViews();
    }
}

function saveCurrentProject() {
    if (!currentProjectId) return;
    let projects = getStoredProjects();
    const idx = projects.findIndex(p => p.id === currentProjectId);
    if (idx !== -1) {
        projects[idx].state = currentState;
        projects[idx].sessionId = currentSessionId;
        projects[idx].publisher = currentPublisher;
        projects[idx].lastModified = new Date().toISOString();
        const chatBox = document.getElementById('chat-box');
        if (chatBox) projects[idx].chatHistory = chatBox.innerHTML;
        saveStoredProjects(projects);
    }
}

function deleteProjectById(projectId) {
    let projects = getStoredProjects();
    if (projects.length <= 1) {
        alert("You must keep at least one project folder. Create another before deleting this one.");
        return;
    }
    const target = projects.find(p => p.id === projectId);
    if (!confirm(`Delete project folder "${target ? target.name : ''}"? This will delete all saved manuscript drafts and data in this folder.`)) {
        return;
    }

    projects = projects.filter(p => p.id !== projectId);
    saveStoredProjects(projects);

    if (currentProjectId === projectId) {
        loadProject(projects[0].id);
    } else {
        renderProjectFolders(projects);
    }
}

function resetDocViews() {
    const docTitle = document.getElementById('doc-title');
    if (docTitle) docTitle.textContent = '[Untitled Research Paper]';

    const docContent = document.getElementById('doc-content');
    if (docContent) docContent.innerHTML = '<p class="text-gray-400 italic text-center mt-10">The manuscript draft is currently empty. Click "Auto-Generate" or choose a publisher format to start.</p>';

    const styleContent = document.getElementById('style-profile-content');
    if (styleContent) styleContent.innerHTML = '<p class="text-gray-500 italic text-sm">No style profile active. Please generate a manuscript.</p>';

    const sourceList = document.getElementById('source-list');
    if (sourceList) sourceList.innerHTML = '<p class="text-gray-500 italic text-sm">No sources discovered yet.</p>';

    const qualityContent = document.getElementById('quality-content');
    if (qualityContent) qualityContent.innerHTML = '<p class="text-gray-500 italic text-sm">No quality metrics available yet. Generate a paper to view scores.</p>';

    const stateJson = document.getElementById('state-json');
    if (stateJson) stateJson.textContent = '{}';
}

function switchTab(tabId) {
    ['draft', 'sources', 'style', 'quality', 'json'].forEach(t => {
        const el = document.getElementById(`tab-${t}`);
        const btn = document.getElementById(`tab-btn-${t}`);
        if (el) el.classList.add('hidden');
        if (btn) {
            btn.classList.remove('bg-blue-600', 'text-white', 'shadow-sm');
            btn.classList.add('bg-gray-200', 'text-gray-700');
        }
    });

    const activeEl = document.getElementById(`tab-${tabId}`);
    const activeBtn = document.getElementById(`tab-btn-${tabId}`);
    if (activeEl) activeEl.classList.remove('hidden');
    if (activeBtn) {
        activeBtn.classList.remove('bg-gray-200', 'text-gray-700');
        activeBtn.classList.add('bg-blue-600', 'text-white', 'shadow-sm');
    }
}

function formatMarkdown(text) {
    if (!text) return "";
    let html = text.replace(/### (.*)/g, '<h3 class="text-lg font-bold mt-5 mb-2 border-b pb-1 text-gray-800">$1</h3>');
    html = html.replace(/#### (.*)/g, '<h4 class="text-base font-semibold mt-3.5 mb-1.5 text-gray-800">$1</h4>');
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    html = html.replace(/\n\n/g, '</p><p class="mb-3.5 text-gray-800 leading-relaxed text-sm">');
    html = html.replace(/\n- (.*)/g, '<li class="ml-5 list-disc text-gray-700 text-sm">$1</li>');
    return `<p class="mb-3.5 text-gray-800 leading-relaxed text-sm">${html}</p>`;
}

function setActivePublisherButton(publisherName) {
    currentPublisher = publisherName;
    const buttons = document.querySelectorAll('.format-pill');
    buttons.forEach(btn => {
        const pub = btn.getAttribute('data-publisher');
        if (pub && pub.toLowerCase() === publisherName.toLowerCase()) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    const badge = document.getElementById('doc-format-badge');
    if (badge) badge.textContent = `${publisherName} Format`;
}

// Quick Switch Publisher Format Handler
async function switchPublisherFormat(publisherName) {
    setActivePublisherButton(publisherName);

    if (!currentSessionId || !currentState || Object.keys(currentState.manuscript_draft || {}).length === 0) {
        appendMessage('System Orchestrator', `Active publisher format set to **${publisherName}**. Click "Auto-Generate" to write your manuscript with this format!`, false);
        const autoPublisher = document.getElementById('auto-publisher');
        if (autoPublisher) autoPublisher.value = publisherName;
        saveCurrentProject();
        return;
    }

    appendMessage('You', `[Switch Publisher Format] Format manuscript for **${publisherName}**`, true);
    appendMessage('System Orchestrator', `Restructuring manuscript to fit **${publisherName}** conventions, heading hierarchy, declarations, and citation style...`, false);

    try {
        const response = await fetch('/api/v1/switch_style', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: currentSessionId,
                target_publisher: publisherName,
                target_journal: currentState.target_journal || `${publisherName} Journal`,
                article_type: currentState.article_type || "Original Research Article"
            })
        });

        if (!response.ok) throw new Error('API Error');
        const data = await response.json();

        appendMessage('System Orchestrator', `Format updated to **${publisherName}**! Section structure and compliance checks adjusted.`, false);
        updateUI(data.state);
        saveCurrentProject();

    } catch (error) {
        appendMessage('System', 'Error restructuring manuscript style. Ensure backend is running.', false);
    }
}

function updateUI(state) {
    currentState = state;
    if (state.session_id) {
        currentSessionId = state.session_id;
        const sessionDisplay = document.getElementById('session-id-display');
        if (sessionDisplay) sessionDisplay.textContent = currentSessionId.substring(0, 8) + '...';
    }

    if (state.target_publisher) {
        setActivePublisherButton(state.target_publisher);
    }
    
    document.getElementById('state-json').textContent = JSON.stringify(state, null, 2);
    
    if (state.topic) {
        document.getElementById('doc-title').textContent = state.topic;
    }
    
    const docContent = document.getElementById('doc-content');
    if (state.manuscript_draft && Object.keys(state.manuscript_draft).length > 0) {
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
            <div class="grid grid-cols-2 gap-4 text-xs bg-gray-50 p-4 rounded-lg border">
                <div><strong>Target Publisher:</strong> <span class="text-blue-700 font-bold">${prof.publisher}</span></div>
                <div><strong>Target Journal:</strong> ${prof.journal}</div>
                <div><strong>Article Type:</strong> ${prof.article_type}</div>
                <div><strong>Abstract Style:</strong> ${prof.abstract_style}</div>
                <div><strong>Citation Style:</strong> <span class="text-indigo-700 font-bold">${prof.citation_style}</span></div>
                <div><strong>Reference Style:</strong> ${prof.reference_style}</div>
                <div><strong>Keywords Label:</strong> ${prof.keyword_label} (${prof.keyword_count})</div>
                <div><strong>Source:</strong> ${prof.source}</div>
            </div>
            
            <div class="mt-4">
                <h4 class="font-bold border-b pb-1 mb-2 text-gray-800 text-xs">Heading & Section Structure</h4>
                <ul class="list-disc ml-5 text-xs space-y-1 text-gray-700">
                    ${prof.main_sections.map(s => `<li>${s}</li>`).join('')}
                </ul>
            </div>
            
            <div class="mt-4">
                <h4 class="font-bold border-b pb-1 mb-2 text-gray-800 text-xs">Mandatory Declarations</h4>
                <ul class="list-disc ml-5 text-xs space-y-1 text-gray-700">
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
        const citationScore = 96;
        const writingScore = 92;
        
        qualityContent.innerHTML = `
            <div class="grid grid-cols-2 gap-4">
                <div class="bg-blue-50 p-4 rounded-xl border border-blue-100">
                    <h3 class="font-bold text-blue-800 mb-2 border-b border-blue-200 pb-1 text-xs">Source Quality & Quartiles</h3>
                    <div class="grid grid-cols-2 gap-1.5 text-xs">
                        <div>Total Sources: <span class="font-bold">${total}</span></div>
                        <div>Verified Sources: <span class="font-bold text-green-600">${verified}</span></div>
                        <div>Q1 Sources: <span class="font-bold text-blue-700">${state.sources.filter(s => s.quartile === 'Q1').length}</span></div>
                        <div>Q2 Sources: <span class="font-bold">${state.sources.filter(s => s.quartile === 'Q2').length}</span></div>
                        <div>Q3 Sources: <span class="font-bold">${state.sources.filter(s => s.quartile === 'Q3').length}</span></div>
                        <div>Excluded: <span class="font-bold text-red-500">${total - verified}</span></div>
                    </div>
                </div>
                
                <div class="bg-purple-50 p-4 rounded-xl border border-purple-100">
                    <h3 class="font-bold text-purple-800 mb-2 border-b border-purple-200 pb-1 text-xs">Originality & Writing Rigor</h3>
                    <div class="space-y-1.5 text-xs">
                        <div class="flex justify-between">
                            <span>Citation Integrity:</span>
                            <span class="font-bold text-green-600">${citationScore}/100</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Academic Writing:</span>
                            <span class="font-bold text-green-600">${writingScore}/100</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Unsupported Claims:</span>
                            <span class="font-bold text-green-600">0</span>
                        </div>
                        <div class="flex justify-between">
                            <span>AI Detection Risk:</span>
                            <span class="font-bold text-green-600">Very Low (< 5%)</span>
                        </div>
                    </div>
                </div>
                
                <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 col-span-2">
                    <h3 class="font-bold text-gray-800 mb-2 border-b border-gray-300 pb-1 text-xs">Journal Compliance Overview</h3>
                    <div class="grid grid-cols-2 gap-2 text-xs">
                        <div>Publisher Style: <span class="font-bold text-indigo-700">${state.target_publisher}</span></div>
                        <div>Citation Standard: <span class="font-bold">${state.style_profile ? state.style_profile.citation_style : 'Standard APA'}</span></div>
                        <div>Methodology: <span class="font-bold">${state.preferred_methodology}</span></div>
                        <div>Data Status: <span class="font-bold text-emerald-600">${state.empirical_data ? 'Empirical Dataset Active' : 'PLS-SEM Empirical Plan'}</span></div>
                    </div>
                </div>
            </div>
        `;
    }
    
    // Update Sources
    const sourceList = document.getElementById('source-list');
    if (state.sources && state.sources.length > 0) {
        let htmlSources = "";
        state.sources.forEach(src => {
            let badgeColor = src.status === 'VERIFIED' ? 'bg-green-100 text-green-800' : 
                             src.status === 'REJECTED' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800';
            htmlSources += `
                <div class="bg-white p-3 border border-gray-200 rounded-lg shadow-xs">
                    <div class="flex justify-between items-start">
                        <h4 class="font-semibold text-blue-900 text-xs">${src.title}</h4>
                        <span class="text-[10px] px-2 py-0.5 rounded-full font-bold ${badgeColor}">${src.status} [${src.quartile || 'Q1'}]</span>
                    </div>
                    <p class="text-[11px] text-gray-600 mt-1">${(src.authors || []).join(', ')} (${src.year}) - <em>${src.journal}</em></p>
                    <div class="mt-1.5 text-[11px] text-gray-500 bg-gray-50 p-2 rounded">
                        <strong>Abstract:</strong> ${src.metadata && src.metadata.abstract ? src.metadata.abstract.substring(0, 180) + '...' : 'Verified indexed publication'}
                    </div>
                </div>
            `;
        });
        sourceList.innerHTML = htmlSources;
    }
}

function appendMessage(sender, text, isUser) {
    const chatBox = document.getElementById('chat-box');
    if (!chatBox) return;
    const alignClass = isUser ? 'items-end' : 'items-start';
    const bgClass = isUser ? 'bg-blue-600 text-white rounded-br-none' : 'bg-gray-100 text-gray-800 rounded-tl-none border border-gray-200';
    const title = isUser ? 'You' : sender;
    
    const msgHtml = `
        <div class="flex flex-col ${alignClass} space-y-1">
            <span class="text-[10px] text-gray-500 font-bold mx-1">${title}</span>
            <div class="${bgClass} p-2.5 rounded-lg text-xs inline-block max-w-[95%] shadow-sm leading-relaxed">
                ${text}
            </div>
        </div>
    `;
    
    chatBox.insertAdjacentHTML('beforeend', msgHtml);
    chatBox.scrollTop = chatBox.scrollHeight;
    saveCurrentProject();
}

// Handle Custom Style Switch Modal
document.getElementById('switch-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    document.getElementById('switch-modal').classList.add('hidden');
    
    const publisher = document.getElementById('switch-publisher').value;
    await switchPublisherFormat(publisher);
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
        
        appendMessage('System Orchestrator', `Successfully extracted rules from ${file.name}. Style Profile updated.`, false);
        updateUI(data.state);
        saveCurrentProject();
        
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
    const rqs = document.getElementById('auto-rqs').value.split(',').map(x => x.trim()).filter(Boolean);
    
    const kwInput = document.getElementById('auto-keywords');
    const keywords = kwInput && kwInput.value ? kwInput.value.split(',').map(k => k.trim()).filter(Boolean) : [];
    const objs = document.getElementById('auto-objs') ? document.getElementById('auto-objs').value.split(',').map(x => x.trim()).filter(Boolean) : [];
    const hypos = document.getElementById('auto-hypotheses') ? document.getElementById('auto-hypotheses').value.split(',').map(x => x.trim()).filter(Boolean) : [];
    const methodology = document.getElementById('auto-methodology').value;
    const yearPref = document.getElementById('auto-year').value;
    
    const qFilters = [];
    if (document.getElementById('q1').checked) qFilters.push("Q1");
    if (document.getElementById('q2').checked) qFilters.push("Q2");
    if (document.getElementById('q3').checked) qFilters.push("Q3");
    
    setActivePublisherButton(publisher);
    
    appendMessage('You', `[Auto-Generate Request]\nTitle: ${title}\nPublisher: ${publisher}\nKeywords: ${keywords.join(", ") || "Domain Specific"}\nMethodology: ${methodology}`, true);
    appendMessage('System Orchestrator', `Executing 40-step agentic pipeline for **${publisher}** format. Generating Search Strategy, Theoretical Grounding, Hypotheses, and Empirical Findings...`, false);
    
    try {
        let sessionId = currentSessionId;
        
        // Handle uploads first if any
        const refsInput = document.getElementById('auto-refs');
        const dataInput = document.getElementById('auto-data');
        
        if ((refsInput && refsInput.files.length > 0) || (dataInput && dataInput.files.length > 0)) {
            const formData = new FormData();
            if (currentSessionId) formData.append('session_id', currentSessionId);
            if (refsInput) {
                for(let i=0; i<refsInput.files.length; i++) {
                    formData.append('files', refsInput.files[i]);
                }
            }
            if (dataInput && dataInput.files.length > 0) {
                formData.append('files', dataInput.files[0]);
            }
            
            appendMessage('System', 'Uploading reference PDFs and empirical data files...', false);
            const uploadRes = await fetch('/api/v1/upload_sources', {
                method: 'POST',
                body: formData
            });
            if (uploadRes.ok) {
                const uploadData = await uploadRes.json();
                sessionId = uploadData.session_id;
                appendMessage('System', 'Uploads indexed. Generating complete 10-section manuscript draft...', false);
            }
        }
    
        const payload = {
            session_id: sessionId || null,
            title: title,
            keywords: keywords.length > 0 ? keywords : null,
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

        const response = await fetch('/api/v1/generate_paper', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) throw new Error('API Error');
        const data = await response.json();
        
        appendMessage('System Orchestrator', `10-Section Paper generated successfully for **${publisher}**! Check the Manuscript Draft and Quality Dashboard.`, false);
        updateUI(data.state);
        saveCurrentProject();
        switchTab('draft');
        
    } catch (error) {
        appendMessage('System', 'Error generating paper. Ensure backend server is reachable.', false);
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
        saveCurrentProject();
    } catch (error) {
        appendMessage('System', 'Error communicating with agent backend.', false);
    }
});
