// Homepage Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 CrewAI Agents Dashboard loaded');
    
    // Initialize dashboard
    initializeDashboard();
    
    // Add smooth animations
    animateCards();
});

// Initialize Dashboard
function initializeDashboard() {
    // Check if academic agent is available
    checkAgentStatus();
    
    // Add click effects
    addClickEffects();
    
    // Initialize tooltips or other interactive elements
    initializeInteractivity();
}

// Check agent status
async function checkAgentStatus(agentType) {
    try {
        const response = await fetch('/api/v1/health');
        const data = await response.json();
        return data.status === 'healthy';
    } catch (error) {
        console.error(`Error checking ${agentType} status:`, error);
        return false;
    }
}

// Update Agent Status
function updateAgentStatus(agentType, status) {
    const statusIndicator = document.querySelector('.status-indicator .status-dot');
    const statusText = document.querySelector('.status-indicator span');
    
    if (status === 'online') {
        statusIndicator.classList.add('active');
        statusText.textContent = 'All Systems Online';
    } else {
        statusIndicator.classList.remove('active');
        statusText.textContent = 'Some Services Offline';
    }
}

// Add Click Effects
function addClickEffects() {
    const cards = document.querySelectorAll('.agent-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        card.addEventListener('mousedown', function() {
            this.style.transform = 'translateY(-4px) scale(0.98)';
        });
        
        card.addEventListener('mouseup', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
    });
}

// Animate Cards on Load
function animateCards() {
    const cards = document.querySelectorAll('.agent-card');
    
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 150); // Stagger animation
    });
}

// Initialize Interactivity
function initializeInteractivity() {
    // Add keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.target.classList.contains('agent-card')) {
            e.target.click();
        }
    });
    
    // Make cards focusable
    const cards = document.querySelectorAll('.agent-card');
    cards.forEach(card => {
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
    });
}

// Open Agent Functions
function openAgent(agentType) {
    console.log(`Opening ${agentType} agent...`);
    
    // Add click animation
    const agentCard = event.target.closest('.agent-card');
    if (agentCard) {
        agentCard.style.transform = 'scale(0.95)';
        setTimeout(() => {
            agentCard.style.transform = '';
        }, 150);
    }
    
    switch(agentType) {
        case 'academic':
            // Navigate to academic agent
            window.location.href = '/academic';
            break;
        case 'youtube':
        case 'code':
        case 'business':
        case 'data':
        case 'custom':
            // Show coming soon modal
            showComingSoonModal(agentType);
            break;
        default:
            console.log('Unknown agent type');
    }
}

// Open Academic Agent
function openAcademicAgent() {
    // Add loading state
    const academicCard = document.querySelector('.agent-card.featured');
    const launchBtn = academicCard.querySelector('.launch-btn');
    
    // Show loading state
    const originalContent = launchBtn.innerHTML;
    launchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Launching...';
    launchBtn.disabled = true;
    
    // Add visual feedback
    academicCard.style.transform = 'translateY(-12px) scale(1.05)';
    academicCard.style.boxShadow = '0 25px 50px -12px rgba(59, 130, 246, 0.25)';
    
    // Navigate to academic agent with a slight delay for effect
    setTimeout(() => {
        window.location.href = '/academic';
    }, 800);
}

// Show Coming Soon Modal
function showComingSoon(agentType) {
    const modal = document.getElementById('comingSoonModal');
    const modalBody = modal.querySelector('.modal-body');
    
    // Customize message based on agent type
    let message = getComingSoonMessage(agentType);
    modalBody.innerHTML = message;
    
    // Show modal with animation
    modal.classList.add('show');
    
    // Add shake effect to the card
    const card = event.currentTarget;
    card.style.animation = 'shake 0.5s ease-in-out';
    
    setTimeout(() => {
        card.style.animation = '';
    }, 500);
}

// Get Coming Soon Message
function getComingSoonMessage(agentType) {
    const messages = {
        youtube: `
            <h4><i class="fab fa-youtube" style="color: #ff0000;"></i> YouTube Content Assistant</h4>
            <p>This powerful agent will help you:</p>
            <ul style="margin: 1rem 0; padding-left: 1.5rem;">
                <li>Analyze video content and engagement</li>
                <li>Generate optimized titles and descriptions</li>
                <li>Create video scripts and thumbnails</li>
                <li>Provide SEO recommendations</li>
            </ul>
            <p><strong>Expected Release:</strong> Coming Soon</p>
        `,
        code: `
            <h4><i class="fas fa-code" style="color: #333;"></i> Code Development Assistant</h4>
            <p>This technical agent will provide:</p>
            <ul style="margin: 1rem 0; padding-left: 1.5rem;">
                <li>Code review and optimization</li>
                <li>Debugging assistance</li>
                <li>Architecture recommendations</li>
                <li>Multi-language support</li>
            </ul>
            <p><strong>Expected Release:</strong> Coming Soon</p>
        `,
        business: `
            <h4><i class="fas fa-briefcase" style="color: #10b981;"></i> Business Strategy Assistant</h4>
            <p>This strategic agent will offer:</p>
            <ul style="margin: 1rem 0; padding-left: 1.5rem;">
                <li>Market analysis and insights</li>
                <li>Business plan development</li>
                <li>Competitive research</li>
                <li>Growth strategy recommendations</li>
            </ul>
            <p><strong>Expected Release:</strong> Coming Soon</p>
        `,
        data: `
            <h4><i class="fas fa-chart-area" style="color: #8b5cf6;"></i> Data Analysis Assistant</h4>
            <p>This analytical agent will provide:</p>
            <ul style="margin: 1rem 0; padding-left: 1.5rem;">
                <li>Data processing and cleaning</li>
                <li>Statistical analysis</li>
                <li>Data visualization</li>
                <li>Predictive insights</li>
            </ul>
            <p><strong>Expected Release:</strong> Coming Soon</p>
        `
    };
    
    return messages[agentType] || `
        <h4>New Agent Coming Soon!</h4>
        <p>We're working hard to bring you this new AI assistant.</p>
        <p>Stay tuned for updates!</p>
    `;
}

// Show Create Agent Modal
function showCreateAgent() {
    // For now, show a coming soon message
    const modal = document.getElementById('comingSoonModal');
    const modalBody = modal.querySelector('.modal-body');
    
    modalBody.innerHTML = `
        <h4><i class="fas fa-plus" style="color: #f59e0b;"></i> Create Custom Agent</h4>
        <p>Soon you'll be able to create your own custom AI agents!</p>
        <p>Features will include:</p>
        <ul style="margin: 1rem 0; padding-left: 1.5rem;">
            <li>Custom prompts and behavior</li>
            <li>Specialized knowledge bases</li>
            <li>Integration with your tools</li>
            <li>Custom UI and branding</li>
        </ul>
        <p><strong>This feature is in development.</strong></p>
    `;
    
    modal.classList.add('show');
}

// Close Modal
function closeModal() {
    const modal = document.getElementById('comingSoonModal');
    modal.classList.remove('show');
}

// Close modal when clicking outside
window.addEventListener('click', function(e) {
    const modal = document.getElementById('comingSoonModal');
    if (e.target === modal) {
        closeModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// Add shake animation to CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
`;
document.head.appendChild(style);

// Periodic status check
setInterval(checkAgentStatus, 30000); // Check every 30 seconds

console.log('✨ Dashboard fully initialized!');
