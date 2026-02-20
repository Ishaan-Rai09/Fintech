// Authentication check for feature pages

document.addEventListener('DOMContentLoaded', async () => {
    // Check if user is authenticated
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        // No token, redirect to landing page
        window.location.href = '/';
        return;
    }
    
    try {
        // Verify token with server
        const response = await AuthAPI.getCurrentUser();
        
        if (response.success) {
            // Update user info in navbar
            const userNameElement = document.getElementById('userName');
            if (userNameElement) {
                userNameElement.textContent = response.data.full_name || response.data.username;
            }
        } else {
            // Invalid token, redirect to landing page
            localStorage.removeItem('access_token');
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Auth check failed:', error);
        // Show error but don't redirect - let user stay on page
        const userNameElement = document.getElementById('userName');
        if (userNameElement) {
            userNameElement.textContent = 'User';
        }
    }
});

// Logout functionality
document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove token
            localStorage.removeItem('access_token');
            
            // Redirect to landing page
            window.location.href = '/';
        });
    }
});