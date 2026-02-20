let currentNodeUrl = 'http://localhost:8000';
let pollInterval = null;

const elements = {
    nodeUrlInput: document.getElementById('node-url'),
    peerUrlInput: document.getElementById('peer-url'),
    msgContent: document.getElementById('msg-content'),
    btnConnect: document.getElementById('btn-connect'),
    btnAddPeer: document.getElementById('btn-add-peer'),
    btnSend: document.getElementById('btn-send'),
    statusBadge: document.getElementById('connection-status'),
    peerList: document.getElementById('peer-list'),
    logContainer: document.getElementById('log-container')
};

// --- API Functions ---

async function fetchStatus() {
    try {
        const response = await fetch(`${currentNodeUrl}/status`);
        const data = await response.json();
        updateUIStatus(true, data);
        updatePeerList(data.peers);
    } catch (error) {
        updateUIStatus(false);
    }
}

async function fetchHistory() {
    try {
        const response = await fetch(`${currentNodeUrl}/history`);
        const history = await response.json();
        updateLogFeed(history);
    } catch (error) {
        console.error("Failed to fetch history", error);
    }
}

async function addPeer() {
    const peerUrl = elements.peerUrlInput.value.trim();
    if (!peerUrl) return;

    try {
        await fetch(`${currentNodeUrl}/connect`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ address: peerUrl })
        });
        elements.peerUrlInput.value = '';
        fetchStatus();
    } catch (error) {
        alert("Failed to add peer. Is the node running?");
    }
}

async function broadcastMessage() {
    const content = elements.msgContent.value.trim();
    if (!content) return;

    try {
        await fetch(`${currentNodeUrl}/send`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sender: "Web-UI", content: content })
        });
        elements.msgContent.value = '';
        fetchHistory();
    } catch (error) {
        alert("Failed to broadcast message.");
    }
}

// --- UI Updates ---

function updateUIStatus(online, data = null) {
    if (online) {
        elements.statusBadge.textContent = `Online: Node-${data.node_id}`;
        elements.statusBadge.classList.remove('offline');
        elements.statusBadge.classList.add('online');
    } else {
        elements.statusBadge.textContent = 'Disconnected';
        elements.statusBadge.classList.remove('online');
        elements.statusBadge.classList.add('offline');
        elements.peerList.innerHTML = ''; // Clear peers if disconnected
    }
}

async function updatePeerList(peers) {
    elements.peerList.innerHTML = '';

    for (const peer of peers) {
        const li = document.createElement('li');
        li.className = 'peer-item';
        li.innerHTML = `
            <span class="peer-url">${peer}</span>
            <div class="status-indicator"></div>
        `;
        elements.peerList.appendChild(li);

        // Check health
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 1000);

            const response = await fetch(`${peer}/status`, {
                signal: controller.signal
            });
            clearTimeout(timeoutId);

            if (response.ok) {
                li.classList.add('active');
            }
        } catch (e) {
            // Offline
        }
    }
}

const seenMsgIds = new Set();

function updateLogFeed(history) {
    history.forEach(msg => {
        if (!seenMsgIds.has(msg.msg_id)) {
            seenMsgIds.add(msg.msg_id);
            const entry = document.createElement('div');
            entry.className = 'log-entry';

            const time = new Date(msg.timestamp).toLocaleTimeString();

            entry.innerHTML = `
                <div class="meta">
                    <span class="sender">${msg.sender}</span>
                    <span class="time">${time}</span>
                </div>
                <div class="content">${msg.content}</div>
            `;

            elements.logContainer.prepend(entry);
        }
    });
}

// --- Event Listeners ---

elements.btnConnect.addEventListener('click', () => {
    currentNodeUrl = elements.nodeUrlInput.value.trim();
    if (pollInterval) clearInterval(pollInterval);

    // Initial fetch
    fetchStatus();
    fetchHistory();

    // Start polling
    pollInterval = setInterval(() => {
        fetchStatus();
        fetchHistory();
    }, 2000);
});

elements.btnAddPeer.addEventListener('click', addPeer);
elements.btnSend.addEventListener('click', broadcastMessage);

// Initialize on load
elements.btnConnect.click();
