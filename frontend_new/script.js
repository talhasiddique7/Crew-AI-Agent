// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const messagesArea = document.getElementById('messagesArea');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const chatForm = document.getElementById('chatForm');
const subjectSelect = document.getElementById('subjectSelect');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const charCounter = document.getElementById('charCounter');
const loadingOverlay = document.getElementById('loadingOverlay');

// Application State
let isConnected = false;
let isLoading = false;
let messageHistory = [];

// Initialize Application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    checkBackendHealth();
    loadSubjects();
});

// App Initialization
function initializeApp() {
    console.log('🚀 Academic Chat Agent initialized');
    updateCharCounter();
    autoResizeTextarea();
}

// Event Listeners Setup
function setupEventListeners() {
    // Chat form submission
    chatForm.addEventListener('submit', handleChatSubmit);
    
    // Message input events
    messageInput.addEventListener('input', function() {
        updateCharCounter();
        autoResizeTextarea();
    });
    
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleChatSubmit(e);
        }
    });
    
    // Subject selection
    subjectSelect.addEventListener('change', function() {
        console.log('📚 Subject changed to:', this.value);
    });
    
    // Global error handling
    window.addEventListener('error', function(e) {
        console.error('❌ Global error:', e.error);
        showError('An unexpected error occurred. Please refresh the page.');
    });
}

// Backend Health Check
async function checkBackendHealth() {
    try {
        updateStatus('connecting', 'Connecting...');
        
        const response = await fetch(`${API_BASE_URL}/api/v1/health`);
        
        if (response.ok) {
            const health = await response.json();
            updateStatus('connected', 'Connected');
            isConnected = true;
            console.log('✅ Backend connected:', health);
        } else {
            throw new Error(`Health check failed: ${response.status}`);
        }
    } catch (error) {
        console.error('❌ Backend connection failed:', error);
        updateStatus('error', 'Connection failed');
        isConnected = false;
        showError('Cannot connect to backend. Please ensure the server is running on port 8000.');
    }
}

// Load Available Subjects
async function loadSubjects() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/academic/subjects`);
        
        if (response.ok) {
            const subjects = await response.json();
            populateSubjects(subjects.subjects);
            console.log('📚 Subjects loaded:', subjects.subjects);
        } else {
            console.warn('⚠️ Could not load subjects, using defaults');
        }
    } catch (error) {
        console.warn('⚠️ Failed to load subjects:', error);
        // Keep default subjects
    }
}

// Populate Subject Dropdown
function populateSubjects(subjects) {
    // Clear existing options except "General"
    subjectSelect.innerHTML = '<option value="General">General</option>';
    
    // Add new subjects
    subjects.forEach(subject => {
        if (subject !== 'General') {
            const option = document.createElement('option');
            option.value = subject;
            option.textContent = subject;
            subjectSelect.appendChild(option);
        }
    });
}

// Handle Chat Form Submission
async function handleChatSubmit(e) {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message || isLoading || !isConnected) {
        return;
    }
    
    // Add user message to chat
    addMessage('user', message);
    
    // Clear input and show loading
    messageInput.value = '';
    updateCharCounter();
    autoResizeTextarea();
    setLoading(true);
    
    try {
        // Send message to backend
        const response = await sendChatMessage(message);
        
        // Add assistant response
        addMessage('assistant', response.message);
        
        // Store in history
        messageHistory.push({
            user: message,
            assistant: response.message,
            subject: subjectSelect.value,
            timestamp: new Date().toISOString()
        });
        
    } catch (error) {
        console.error('❌ Chat error:', error);
        addMessage('assistant', 'I apologize, but I encountered an error processing your request. Please try again.');
        showError('Failed to send message. Please check your connection and try again.');
    } finally {
        setLoading(false);
    }
}

// Send Chat Message to Backend
async function sendChatMessage(message) {
    const requestData = {
        message: message,
        subject: subjectSelect.value,
        context: getRecentContext()
    };
    
    const response = await fetch(`${API_BASE_URL}/api/v1/academic/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    });
    
    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText}`);
    }
    
    return await response.json();
}

// Get Recent Context for Better Responses
function getRecentContext() {
    // Return last 3 messages for context
    return messageHistory.slice(-3).map(msg => ({
        user: msg.user,
        assistant: msg.assistant
    }));
}

// Add Message to Chat
function addMessage(sender, text) {
    // Remove welcome message if it exists
    const welcomeMessage = messagesArea.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    // Create message element
    const messageElement = document.createElement('div');
    messageElement.className = `message ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    
    // Format the text for better readability
    if (sender === 'assistant') {
        messageText.innerHTML = formatAIResponse(text);
    } else {
        messageText.textContent = text;
    }
    
    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = formatTime(new Date());
    
    content.appendChild(messageText);
    content.appendChild(messageTime);
    messageElement.appendChild(avatar);
    messageElement.appendChild(content);
    
    // Add to messages area
    messagesArea.appendChild(messageElement);
    
    // Scroll to bottom
    messagesArea.scrollTop = messagesArea.scrollHeight;
    
    console.log(`💬 ${sender}: ${text.substring(0, 50)}${text.length > 50 ? '...' : ''}`);
}

// Format AI Response for Better Display
function formatAIResponse(text) {
    // Convert markdown-like formatting to HTML
    let formatted = text
        // Bold text: **text** -> <strong>text</strong>
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Italic text: *text* -> <em>text</em>
        .replace(/(?<!\*)\*([^*]+?)\*(?!\*)/g, '<em>$1</em>')
        // Code blocks: `code` -> <code>code</code>
        .replace(/`(.*?)`/g, '<code>$1</code>')
        // Chemical equations: Special handling for chemical formulas
        .replace(/(\b[A-Z][a-z]?\d*(?:\([A-Za-z0-9]+\))?(?:\s*[+\-→]?\s*[A-Z][a-z]?\d*(?:\([A-Za-z0-9]+\))?)*\b)/g, '<code>$1</code>')
        // Line breaks: Convert double spaces to line breaks
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n/g, '<br>')
        // Arrows: -> becomes →
        .replace(/->/g, ' → ')
        // Convert numbered lists with better formatting
        .replace(/(\d+\.\s\*\*[^*]+\*\*)/g, '<br><br>$1')
        // Add proper spacing around sections
        .replace(/(\*\*[^*]+\*\*)/g, '<br><br>$1<br>')
        // Clean up excessive line breaks
        .replace(/<br><br><br>/g, '<br><br>')
        .replace(/^<br><br>/, '')
        .replace(/<br>$/, '');
    
    return formatted;
}

// Format Time for Messages
function formatTime(date) {
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
}

// Update Connection Status
function updateStatus(status, text) {
    statusDot.className = `status-dot ${status}`;
    statusText.textContent = text;
}

// Set Loading State
function setLoading(loading) {
    isLoading = loading;
    sendButton.disabled = loading;
    
    if (loading) {
        loadingOverlay.classList.add('show');
        sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    } else {
        loadingOverlay.classList.remove('show');
        sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
    }
}

// Update Character Counter
function updateCharCounter() {
    const length = messageInput.value.length;
    charCounter.textContent = `${length}/2000`;
    
    if (length > 1800) {
        charCounter.style.color = 'var(--error-color)';
    } else if (length > 1500) {
        charCounter.style.color = 'var(--warning-color)';
    } else {
        charCounter.style.color = 'var(--text-muted)';
    }
}

// Auto-resize Textarea
function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}

// Show Error Toast
function showError(message) {
    // Create error toast
    const toast = document.createElement('div');
    toast.className = 'error-toast';
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--error-color);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: var(--radius);
        box-shadow: var(--shadow-lg);
        z-index: 1001;
        max-width: 400px;
        animation: slideInRight 0.3s ease;
    `;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 5000);
}

// Add toast animations to CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Periodic Health Check
setInterval(checkBackendHealth, 30000); // Check every 30 seconds

// Export for debugging
window.academicChat = {
    sendMessage: sendChatMessage,
    addMessage,
    checkHealth: checkBackendHealth,
    getHistory: () => messageHistory,
    clearHistory: () => {
        messageHistory = [];
        messagesArea.innerHTML = '<div class="welcome-message"><div class="welcome-content"><i class="fas fa-robot welcome-icon"></i><h2>Welcome to Academic Chat Agent</h2><p>I\'m your AI-powered academic assistant. Ask me questions about any subject, and I\'ll provide comprehensive, educational answers.</p></div></div>';
    }
};

console.log('🎓 Academic Chat Agent ready!');
