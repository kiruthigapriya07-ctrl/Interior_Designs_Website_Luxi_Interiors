// ========================================
// INTERIOR DESIGN STUDIO - JAVASCRIPT
// ========================================

document.addEventListener('DOMContentLoaded', function() {

    // ========================================
    // NAVIGATION
    // ========================================
    const navbar = document.querySelector('.navbar');
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('.nav-menu');

    // Scroll effect for navbar
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile menu toggle
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    // Close mobile menu on link click
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            if (mobileToggle) {
                mobileToggle.classList.remove('active');
            }
        });
    });

    // Active nav link
    const currentPage = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });

    // ========================================
    // SMOOTH SCROLLING
    // ========================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // ========================================
    // INTERSECTION OBSERVER FOR ANIMATIONS
    // ========================================
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const animationObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements with animate-on-scroll class
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        animationObserver.observe(el);
    });

    // ========================================
    // STATISTICS COUNTER ANIMATION
    // ========================================
    const statsObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statNumber = entry.target.querySelector('.stat-number');
                if (statNumber) {
                    animateCounter(statNumber);
                }
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.stat-item').forEach(stat => {
        statsObserver.observe(stat);
    });

    function animateCounter(element) {
        const target = parseInt(element.getAttribute('data-target'));
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                element.textContent = target.toLocaleString();
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current).toLocaleString();
            }
        }, 16);
    }

    // ========================================
    // BEFORE/AFTER SLIDER
    // ========================================
    const baSlider = document.querySelector('.ba-slider');
    const baHandle = document.querySelector('.ba-slider-handle');
    const baImageAfter = document.querySelector('.ba-image-after');

    if (baSlider && baHandle && baImageAfter) {
        let isDragging = false;

        baHandle.addEventListener('mousedown', startDrag);
        baHandle.addEventListener('touchstart', startDrag);

        document.addEventListener('mousemove', drag);
        document.addEventListener('touchmove', drag);

        document.addEventListener('mouseup', stopDrag);
        document.addEventListener('touchend', stopDrag);

        function startDrag(e) {
            isDragging = true;
            e.preventDefault();
        }

        function drag(e) {
            if (!isDragging) return;

            const sliderRect = baSlider.getBoundingClientRect();
            let x;

            if (e.type === 'touchmove') {
                x = e.touches[0].clientX - sliderRect.left;
            } else {
                x = e.clientX - sliderRect.left;
            }

            // Constrain within slider bounds
            x = Math.max(0, Math.min(x, sliderRect.width));

            const percentage = (x / sliderRect.width) * 100;

            baHandle.style.left = percentage + '%';
            baImageAfter.style.clipPath = `inset(0 ${100 - percentage}% 0 0)`;
        }

        function stopDrag() {
            isDragging = false;
        }
    }

    // ========================================
    // PROJECT MODAL
    // ========================================
    const modal = document.querySelector('.modal');
    const modalClose = document.querySelector('.modal-close');
    const projectCards = document.querySelectorAll('.project-card');

    projectCards.forEach(card => {
        card.addEventListener('click', function() {
            const projectId = this.getAttribute('data-project-id');
            const projectName = this.getAttribute('data-project-name');
            const projectCategory = this.getAttribute('data-project-category');
            const projectLocation = this.getAttribute('data-project-location');
            const projectDescription = this.getAttribute('data-project-description');
            const projectImage = this.getAttribute('data-project-image');
            const projectArea = this.getAttribute('data-project-area');
            const projectDate = this.getAttribute('data-project-date');

            if (modal) {
                document.querySelector('.modal-image').src = projectImage || 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600"><rect fill="%23F9F8F6" width="800" height="600"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="%239B9B9B" font-size="24">Project Image</text></svg>';
                document.querySelector('.modal-details h3').textContent = projectName;
                document.querySelector('.modal-category').textContent = projectCategory;
                document.querySelector('.modal-location').textContent = projectLocation;
                document.querySelector('.modal-description').textContent = projectDescription;
                document.querySelector('.modal-area').textContent = projectArea ? projectArea + ' sq.ft' : 'N/A';
                document.querySelector('.modal-date').textContent = projectDate || 'N/A';

                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });
    });

    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }

    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });
    }

    function closeModal() {
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    }

    // Close modal on ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
            closeModal();
        }
    });

    // ========================================
// CONSULTATION FORM SUBMISSION + VALIDATION
// ========================================

const consultationForm = document.getElementById('consultationForm');

if (consultationForm) {

    consultationForm.addEventListener('submit', async function(e) {

        e.preventDefault();

        // Get fields
        const nameField = consultationForm.querySelector('[name="name"]');
        const emailField = consultationForm.querySelector('[name="email"]');
        const phoneField = consultationForm.querySelector('[name="phone"]');
        const projectTypeField = consultationForm.querySelector('[name="project_type"]');
        const budgetField = consultationForm.querySelector('[name="budget"]');
        const dateField = consultationForm.querySelector('[name="preferred_date"]');
        const timeField = consultationForm.querySelector('[name="preferred_time"]');
        const messageField = consultationForm.querySelector('[name="message"]');

        // Remove old errors
        consultationForm.querySelectorAll('.consult-error').forEach(error => {
            error.remove();
        });

        consultationForm.querySelectorAll('.input-error').forEach(input => {
            input.classList.remove('input-error');
        });

        let isValid = true;

        // ========================================
        // ERROR FUNCTION
        // ========================================

        function showError(field, message) {

            field.classList.add('input-error');

            const error = document.createElement('small');

            error.className = 'consult-error';
            error.textContent = message;

            field.parentElement.appendChild(error);

            isValid = false;
        }

        // ========================================
        // NAME VALIDATION
        // ========================================

        const name = nameField.value.trim();

        if (name === '') {

            showError(nameField, 'Full Name is required.');

        } else if (name.length < 3) {

            showError(
                nameField,
                'Name must contain at least 3 characters.'
            );

        } else if (!/^[A-Za-z\s]+$/.test(name)) {

            showError(
                nameField,
                'Name should contain only letters.'
            );
        }

        // ========================================
        // EMAIL VALIDATION
        // ========================================

        const email = emailField.value.trim();

        const emailPattern =
            /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

        if (email === '') {

            showError(
                emailField,
                'Email Address is required.'
            );

        } else if (!emailPattern.test(email)) {

            showError(
                emailField,
                'Please enter a valid email address.'
            );
        }

        // ========================================
        // PHONE VALIDATION
        // ========================================

        const phone = phoneField.value.trim();

        if (phone === '') {

            showError(
                phoneField,
                'Phone number is required.'
            );

        } else if (!/^[0-9]{10}$/.test(phone)) {

            showError(
                phoneField,
                'Phone number must contain exactly 10 digits.'
            );
        }

        // ========================================
        // PROJECT TYPE
        // ========================================

        const projectType = projectTypeField.value.trim();

        if (projectType === '') {

            showError(
                projectTypeField,
                'Please select a project type.'
            );
        }

        // ========================================
        // BUDGET
        // ========================================

        const budget = budgetField.value.trim();

        if (budget === '') {

            showError(
                budgetField,
                'Please select your budget.'
            );
        }

        // ========================================
        // PREFERRED DATE
        // ========================================

        const preferredDate = dateField.value.trim();

        if (preferredDate === '') {

            showError(
                dateField,
                'Preferred date is required.'
            );
        }

        // ========================================
        // PREFERRED TIME
        // ========================================

        const preferredTime = timeField
            ? timeField.value.trim()
            : '';

        if (timeField && preferredTime === '') {

            showError(
                timeField,
                'Preferred time is required.'
            );
        }

        // ========================================
        // MESSAGE
        // ========================================

        const message = messageField.value.trim();

        if (message === '') {

            showError(
                messageField,
                'Message is required.'
            );

        } else if (message.length < 10) {

            showError(
                messageField,
                'Message must contain at least 10 characters.'
            );
        }

        // ========================================
        // STOP IF ANY ERROR
        // ========================================

        if (!isValid) {
            return;
        }

        // ========================================
        // SEND ONLY IF EVERYTHING IS CORRECT
        // ========================================

        const submitBtn =
            consultationForm.querySelector('.btn[type="submit"]');

        const originalBtnText = submitBtn.textContent;

        submitBtn.disabled = true;
        submitBtn.textContent = 'Booking...';

        const formData = {
            name: name,
            email: email,
            phone: phone,
            project_type: projectType,
            budget: budget,
            preferred_date: preferredDate,
            preferred_time: preferredTime,
            message: message
        };

        console.log('Consultation Data:', formData);

        try {

            const response = await fetch('/api/consultation', {

                method: 'POST',

                headers: {
                    'Content-Type': 'application/json'
                },

                body: JSON.stringify(formData)

            });

            const result = await response.json();

            if (result.success) {

                showConsultationMessage(
                    'success',
                    result.message ||
                    'Consultation booked successfully!'
                );

                consultationForm.reset();

            } else {

                showConsultationMessage(
                    'error',
                    result.message ||
                    'Failed to book consultation.'
                );
            }

        } catch (error) {

            console.error('Consultation Error:', error);

            showConsultationMessage(
                'error',
                'An error occurred. Please try again.'
            );

        } finally {

            submitBtn.disabled = false;
            submitBtn.textContent = originalBtnText;
        }

    });


    // ========================================
    // PHONE - ONLY NUMBERS + MAX 10 DIGITS
    // ========================================

    const consultationPhone =
        consultationForm.querySelector('[name="phone"]');

    if (consultationPhone) {

        consultationPhone.addEventListener('input', function() {

            this.value = this.value
                .replace(/\D/g, '')
                .slice(0, 10);

        });
    }
}


// ========================================
// CONSULTATION SUCCESS / ERROR MESSAGE
// ========================================

function showConsultationMessage(type, message) {

    const consultationForm =
        document.getElementById('consultationForm');

    let formMessage =
        consultationForm.querySelector('.form-message');

    if (!formMessage) {

        formMessage = document.createElement('div');

        formMessage.className = 'form-message';

        consultationForm.appendChild(formMessage);
    }

    formMessage.className =
        `form-message ${type}`;

    formMessage.textContent = message;

    setTimeout(function() {

        if (formMessage) {
            formMessage.remove();
        }

    }, 5000);
}

// ========================================
// CONSULTATION MESSAGE
// ========================================

function showConsultationMessage(type, message) {

    let formMessage = document.querySelector(
        '#consultationForm .form-message'
    );


    if (!formMessage) {

        formMessage = document.createElement('div');

        formMessage.className = 'form-message';

        consultationForm.appendChild(formMessage);
    }


    formMessage.className =
        `form-message ${type}`;

    formMessage.textContent = message;


    setTimeout(function() {

        if (formMessage) {
            formMessage.remove();
        }

    }, 5000);
}

    // ========================================
    // LAZY LOADING IMAGES
    // ========================================
    const lazyImages = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.getAttribute('data-src');
                img.removeAttribute('data-src');
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    }, { rootMargin: '50px' });

    lazyImages.forEach(img => {
        imageObserver.observe(img);
    });

    // ========================================
    // PARALLAX EFFECT FOR HERO
    // ========================================
    const hero = document.querySelector('.hero');

    if (hero) {
        window.addEventListener('scroll', function() {
            const scrolled = window.scrollY;
            if (scrolled < hero.offsetHeight) {
                hero.style.backgroundPositionY = scrolled * 0.5 + 'px';
            }
        });
    }

    // ========================================
    // TESTIMONIAL SLIDER (AUTO)
    // ========================================
    const testimonials = document.querySelectorAll('.testimonial-card');

    if (testimonials.length > 3) {
        let currentIndex = 0;

        setInterval(() => {
            testimonials.forEach((testimonial, index) => {
                if (index === currentIndex) {
                    testimonial.style.display = 'block';
                    testimonial.style.opacity = '1';
                } else {
                    testimonial.style.opacity = '0.5';
                }
            });

            currentIndex = (currentIndex + 1) % testimonials.length;
        }, 5000);
    }

    // ========================================
    // FORM VALIDATION
    // ========================================
    const requiredInputs = document.querySelectorAll('[required]');

    requiredInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateInput(this);
        });

        input.addEventListener('input', function() {
            if (this.classList.contains('invalid')) {
                validateInput(this);
            }
        });
    });

    function validateInput(input) {
        if (input.hasAttribute('required') && !input.value.trim()) {
            input.classList.add('invalid');
            input.classList.remove('valid');
        } else if (input.type === 'email' && input.value) {
           const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (emailPattern.test(input.value)) {
                input.classList.remove('invalid');
                input.classList.add('valid');
            } else {
                input.classList.add('invalid');
                input.classList.remove('valid');
            }
        } else if (input.type === 'tel' && input.value) {
            const phonePattern = /^[+]?[0-9\s\-()]{10,15}$/;
            if (phonePattern.test(input.value)) {
                input.classList.remove('invalid');
                input.classList.add('valid');
            } else {
                input.classList.add('invalid');
                input.classList.remove('valid');
            }
        } else {
            input.classList.remove('invalid');
            input.classList.add('valid');
        }
    }

    // ========================================
    // SCROLL TO TOP BUTTON
    // ========================================
    const scrollToTop = document.createElement('button');
    scrollToTop.className = 'scroll-to-top';
    scrollToTop.innerHTML = '↑';
    scrollToTop.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: var(--secondary-color);
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 1.5rem;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 999;
    `;

    document.body.appendChild(scrollToTop);

    window.addEventListener('scroll', function() {
        if (window.scrollY > 500) {
            scrollToTop.style.opacity = '1';
            scrollToTop.style.visibility = 'visible';
        } else {
            scrollToTop.style.opacity = '0';
            scrollToTop.style.visibility = 'hidden';
        }
    });

    scrollToTop.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // ========================================
    // PRELOADER
    // ========================================
    window.addEventListener('load', function() {
        const preloader = document.querySelector('.preloader');
        if (preloader) {
            preloader.style.opacity = '0';
            setTimeout(() => {
                preloader.style.display = 'none';
            }, 300);
        }
    });

    console.log('Interior Design Studio - JavaScript Loaded Successfully');
});


//themes//
document.addEventListener("DOMContentLoaded", function () {

    const themeToggle = document.getElementById("themeToggle");

    // If no theme is saved, start with LIGHT theme
    let currentTheme = localStorage.getItem("theme") || "light";

    function applyTheme() {

        // Remove both classes first
        document.body.classList.remove("dark-theme", "light-theme");

        // Add current theme
        document.body.classList.add(currentTheme + "-theme");

        // Change button icon
        if (currentTheme === "light") {

            themeToggle.textContent = "🌙";
            themeToggle.setAttribute(
                "aria-label",
                "Switch to dark theme"
            );

        } else {

            themeToggle.textContent = "☀️";
            themeToggle.setAttribute(
                "aria-label",
                "Switch to light theme"
            );
        }

        // Save theme
        localStorage.setItem("theme", currentTheme);
    }

    // Apply theme when page loads
    applyTheme();


    // Theme switch
    themeToggle.addEventListener("click", function () {

        if (currentTheme === "light") {
            currentTheme = "dark";
        } else {
            currentTheme = "light";
        }

        applyTheme();
    });

});