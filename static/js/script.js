// Form Validation and Submission handling
document.addEventListener("DOMContentLoaded", function() {
    console.log("Flood Prediction Frontend Loaded");

    const form = document.getElementById('predictionForm');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                // Show loading state
                const btn = document.getElementById('submitBtn');
                const btnText = document.getElementById('btnText');
                const btnSpinner = document.getElementById('btnSpinner');
                
                if(btn && btnText && btnSpinner) {
                    btnText.textContent = 'Analyzing Data...';
                    btnSpinner.classList.remove('d-none');
                    btn.classList.add('disabled');
                }
            }
            form.classList.add('was-validated');
        }, false);
    }
});
