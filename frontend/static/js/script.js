document.addEventListener('DOMContentLoaded', () => {
    // Door animation logic
    const doorContainer = document.getElementById('doorContainer');
    const startButton = document.getElementById('startButton');
    const landingPage = document.getElementById('landingPage');
    
    if (startButton && doorContainer) {
        startButton.addEventListener('click', () => {
            doorContainer.classList.add('open');
            startButton.style.display = 'none';
            
            setTimeout(() => {
                window.location.href = '/portfolio';
            }, 1500);
        });
    }

    // Landing page logic
    if (landingPage) {
        initializeLandingPage();
    }

    function initializeLandingPage() {
        // Smooth scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Contact form handling
        const contactForm = document.querySelector('.contact-form');
        if (contactForm) {
            contactForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const formData = new FormData(contactForm);
                const payload = {
                    name: formData.get('name'),
                    email: formData.get('email'),
                    message: formData.get('message')
                };

                try {
                    const response = await fetch('/api/contact', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${localStorage.getItem('jwt')}`
                        },
                        body: JSON.stringify(payload)
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    showNotification('Mensaje enviado con éxito', 'success');
                    contactForm.reset();
                } catch (error) {
                    console.error('Error:', error);
                    showNotification('Error al enviar el mensaje', 'error');
                }
            });
        }

        // Notification system
        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `notification ${type}`;
            notification.textContent = message;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.opacity = '0';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }

        // Dark mode toggle
        const darkModeToggle = document.createElement('button');
        darkModeToggle.id = 'dark-mode-toggle';
        darkModeToggle.innerHTML = '🌓';
        darkModeToggle.addEventListener('click', toggleDarkMode);
        document.body.appendChild(darkModeToggle);

        function toggleDarkMode() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        }

        // Initialize dark mode
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
        }

        // Loading spinner
        window.addEventListener('beforeunload', () => {
            document.body.innerHTML = '<div class="loading-spinner"></div>';
        });
    }
});

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            observer.unobserve(img);
        }
    });
});

document.querySelectorAll('img.lazy').forEach(img => {
    observer.observe(img);
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        const headerOffset = 100;
        const elementPosition = target.getBoundingClientRect().top;
        const offsetPosition = elementPosition - headerOffset;

        window.scrollBy({
            top: offsetPosition,
            behavior: 'smooth'
        });
    });
});

document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const filter = this.dataset.filter;
        
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        document.querySelectorAll('.project-card').forEach(card => {
            const matches = filter === 'all' || card.dataset.tags.includes(filter);
            card.style.display = matches ? 'block' : 'none';
        });
    });
});