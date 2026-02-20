// Authentication Logic

// Check if user is already logged in
function checkAuth() {
    const token = getToken();
    const currentPath = window.location.pathname;
    
    // Allow access to landing page
    if (currentPath === '/') {
        return;
    }
    
    // If logged in and on landing, redirect to dashboard
    if (token && currentPath === '/') {
        window.location.href = '/dashboard';
    } 
    // If not logged in and not on landing, redirect to landing
    else if (!token && currentPath !== '/') {
        window.location.href = '/';
    }
}

// Login Form Handler
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await AuthAPI.login({ username, password });
                
                if (response.success && response.data.access_token) {
                    setToken(response.data.access_token);
                    showMessage('message', 'Login successful! Redirecting...', 'success');
                    setTimeout(() => {
                        window.location.href = 'index.html';
                    }, 1000);
                } else {
                    showMessage('message', response.message || 'Login failed', 'error');
                }
            } catch (error) {
                showMessage('message', error.message || 'Login failed', 'error');
            }
        });
    }
    
    // Register Form Handler
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            const fullName = document.getElementById('fullName').value;
            const phone = document.getElementById('phone').value;
            
            // Validate password match
            if (password !== confirmPassword) {
                showMessage('message', 'Passwords do not match', 'error');
                return;
            }
            
            // Validate password length
            if (password.length < 8) {
                showMessage('message', 'Password must be at least 8 characters', 'error');
                return;
            }
            
            try {
                const response = await AuthAPI.register({
                    email,
                    username,
                    password,
                    full_name: fullName,
                    phone
                });
                
                if (response.success) {
                    showMessage('message', 'Registration successful! Redirecting to login...', 'success');
                    setTimeout(() => {
                        window.location.href = 'login.html';
                    }, 2000);
                } else {
                    showMessage('message', response.message || 'Registration failed', 'error');
                }
            } catch (error) {
                showMessage('message', error.message || 'Registration failed', 'error');
            }
        });
    }
    
    // Logout Handler
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            removeToken();
            window.location.href = 'login.html';
        });
    }
    
    // Check authentication on page load
    checkAuth();
});
