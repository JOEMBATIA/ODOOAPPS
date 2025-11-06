document.addEventListener('DOMContentLoaded', function() {
const form = document.getElementById('volunteerForm');
const today = new Date().toISOString().split('T')[0];

// Set minimum date for start date (today)
document.getElementById('start_date').setAttribute('min', today);

// Function to show error
function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorDiv = document.getElementById(fieldId + '-error');
    field.classList.add('error');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }
}

// Function to hide error
function hideError(fieldId) {
    const field = document.getElementById(fieldId);
    const errorDiv = document.getElementById(fieldId + '-error');
    field.classList.remove('error');
    if (errorDiv) {
        errorDiv.style.display = 'none';
    }
}

// Validate age (minimum 16 years)
function validateAge(birthDate) {
    const today = new Date();
    const birth = new Date(birthDate);
    const age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
        return age - 1;
    }
    return age;
}

// Validate email format
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Validate phone number (basic validation)
function validatePhone(phone) {
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    return phoneRegex.test(phone.replace(/\s+/g, ''));
}

// Date validation
document.getElementById('date_of_birth').addEventListener('change', function() {
    const birthDate = this.value;
    if (birthDate) {
        const age = validateAge(birthDate);
        if (age < 16) {
            showError('date_of_birth', 'You must be at least 16 years old to volunteer.');
        } else {
            hideError('date_of_birth');
        }
    }
});

// Start date validation
document.getElementById('start_date').addEventListener('change', function() {
    const startDate = new Date(this.value);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (startDate < today) {
        showError('start_date', 'Start date cannot be in the past.');
    } else {
        hideError('start_date');
        // Update minimum end date
        document.getElementById('end_date').setAttribute('min', this.value);
    }
});

// End date validation
document.getElementById('end_date').addEventListener('change', function() {
    const startDate = new Date(document.getElementById('start_date').value);
    const endDate = new Date(this.value);

    if (endDate <= startDate) {
        showError('end_date', 'End date must be after the start date.');
    } else {
        hideError('end_date');
    }
});

// Email validation
document.getElementById('email').addEventListener('blur', function() {
    if (this.value && !validateEmail(this.value)) {
        showError('email', 'Please enter a valid email address.');
    } else {
        hideError('email');
    }
});

// Phone validation
document.getElementById('phone').addEventListener('blur', function() {
    if (this.value && !validatePhone(this.value)) {
        showError('phone', 'Please enter a valid phone number.');
    } else {
        hideError('phone');
    }
});

// Emergency phone validation
document.getElementById('emergency_phone').addEventListener('blur', function() {
    if (this.value && !validatePhone(this.value)) {
        showError('emergency_phone', 'Please enter a valid emergency contact phone number.');
    } else {
        hideError('emergency_phone');
    }
});

// Form submission validation
form.addEventListener('submit', function(e) {
    let hasErrors = false;

    // Check all required fields
    const requiredFields = [
        'identification', 'name', 'date_of_birth', 'email', 'phone',
        'gender', 'mode', 'start_date', 'end_date', 'emergency_name',
        'emergency_relationship', 'emergency_phone'
    ];

    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (!field.value.trim()) {
            showError(fieldId, 'This field is required.');
            hasErrors = true;
        }
    });

    // Additional validations
    const birthDate = document.getElementById('date_of_birth').value;
    if (birthDate && validateAge(birthDate) < 16) {
        showError('date_of_birth', 'You must be at least 16 years old to volunteer.');
        hasErrors = true;
    }

    const email = document.getElementById('email').value;
    if (email && !validateEmail(email)) {
        showError('email', 'Please enter a valid email address.');
        hasErrors = true;
    }

    const phone = document.getElementById('phone').value;
    if (phone && !validatePhone(phone)) {
        showError('phone', 'Please enter a valid phone number.');
        hasErrors = true;
    }

    const emergencyPhone = document.getElementById('emergency_phone').value;
    if (emergencyPhone && !validatePhone(emergencyPhone)) {
        showError('emergency_phone', 'Please enter a valid emergency contact phone number.');
        hasErrors = true;
    }

    const startDate = new Date(document.getElementById('start_date').value);
    const endDate = new Date(document.getElementById('end_date').value);
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (startDate < today) {
        showError('start_date', 'Start date cannot be in the past.');
        hasErrors = true;
    }

    if (endDate <= startDate) {
        showError('end_date', 'End date must be after the start date.');
        hasErrors = true;
    }

    if (hasErrors) {
        e.preventDefault();
        // Scroll to first error
        const firstError = document.querySelector('.form-control.error');
        if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
});
});