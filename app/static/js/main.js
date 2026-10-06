// Rami Khaled Portfolio - Main JavaScript
document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Lucide Icons
    if (window.lucide) {
        lucide.createIcons();
    }

    // 2. Dark / Light Mode Toggle
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeToggleMobileBtn = document.getElementById('theme-toggle-mobile');

    function toggleTheme() {
        const isDark = document.documentElement.classList.toggle('dark');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        if (window.lucide) {
            lucide.createIcons();
        }
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', toggleTheme);
    }
    if (themeToggleMobileBtn) {
        themeToggleMobileBtn.addEventListener('click', toggleTheme);
    }

    // 3. Mobile Navigation Menu
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuCloseBtn = document.getElementById('mobile-menu-close');

    function toggleMobileMenu() {
        if (!mobileMenu) return;
        const isHidden = mobileMenu.classList.contains('hidden');
        if (isHidden) {
            mobileMenu.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        } else {
            mobileMenu.classList.add('hidden');
            document.body.style.overflow = '';
        }
    }

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', toggleMobileMenu);
    }
    if (mobileMenuCloseBtn) {
        mobileMenuCloseBtn.addEventListener('click', toggleMobileMenu);
    }

    // Close mobile menu on clicking any link
    if (mobileMenu) {
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
                document.body.style.overflow = '';
            });
        });
    }

    // 4. Project Category Filtering (Homepage & Projects gallery)
    const filterButtons = document.querySelectorAll('.project-filter-btn');
    const projectCards = document.querySelectorAll('.project-item');

    if (filterButtons.length > 0 && projectCards.length > 0) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const category = btn.getAttribute('data-category');

                // Update active button state
                filterButtons.forEach(b => {
                    b.classList.remove('active-filter', 'bg-sky-600', 'text-white', 'dark:bg-sky-500');
                    b.classList.add('text-slate-600', 'dark:text-slate-300', 'bg-slate-100', 'dark:bg-slate-800');
                });
                btn.classList.add('active-filter', 'bg-sky-600', 'text-white', 'dark:bg-sky-500');
                btn.classList.remove('text-slate-600', 'dark:text-slate-300', 'bg-slate-100', 'dark:bg-slate-800');

                // Filter cards with smooth opacity transition
                projectCards.forEach(card => {
                    const cardCategory = card.getAttribute('data-category');
                    if (category === 'all' || cardCategory === category) {
                        card.style.display = 'flex';
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, 20);
                    } else {
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(10px)';
                        setTimeout(() => {
                            card.style.display = 'none';
                        }, 200);
                    }
                });
            });
        });
    }

    // 5. Sticky Navbar Shadow Transition on Scroll
    const navbar = document.getElementById('main-navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 20) {
                navbar.classList.add('shadow-md', 'border-b', 'border-slate-200/80', 'dark:border-slate-800/80');
            } else {
                navbar.classList.remove('shadow-md', 'border-b', 'border-slate-200/80', 'dark:border-slate-800/80');
            }
        });
    }

    // 6. Flash Alert Auto Dismiss
    const flashAlerts = document.querySelectorAll('.flash-alert');
    flashAlerts.forEach(alert => {
        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => alert.remove());
        }
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 6000);
    });

    // 7. Clipboard Copy Helper (for email or code)
    window.copyToClipboard = function(text, elementId) {
        navigator.clipboard.writeText(text).then(() => {
            const el = document.getElementById(elementId);
            if (el) {
                const originalText = el.innerText;
                el.innerText = 'Copied!';
                setTimeout(() => {
                    el.innerText = originalText;
                }, 2000);
            }
        });
    };
});
