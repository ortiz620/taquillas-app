// Box office calculator JavaScript enhancements

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            // Add loading state to submit button
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Procesando...';
                
                // Re-enable button after 3 seconds (fallback)
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 3000);
            }
        });
    });

    // Real-time form validation for add taquilla form
    const addForm = document.getElementById('addTaquillaForm');
    if (addForm) {
        const nombreInput = addForm.querySelector('#nombre');
        const precioInput = addForm.querySelector('#precio');

        // Nombre validation
        nombreInput.addEventListener('input', function() {
            const value = this.value.trim();
            if (value.length === 0) {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            } else if (value.length > 50) {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });

        // Precio validation
        precioInput.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (isNaN(value) || value <= 0) {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
    }

    // Real-time form validation for add gasto form
    const addGastoForm = document.getElementById('addGastoForm');
    if (addGastoForm) {
        const descripcionInput = addGastoForm.querySelector('#descripcion');
        const montoInput = addGastoForm.querySelector('#monto');

        // Descripción validation
        descripcionInput.addEventListener('input', function() {
            const value = this.value.trim();
            if (value.length === 0) {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            } else if (value.length > 100) {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });

        // Monto validation
        montoInput.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (isNaN(value) || value <= 0) {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
    }

    // Calculation form validation
    const calcForms = document.querySelectorAll('form[action*="/calcular/"]');
    calcForms.forEach(form => {
        const inicialInput = form.querySelector('input[name="inicial"]');
        const finalInput = form.querySelector('input[name="final"]');

        function validateCalculationInputs() {
            const inicial = parseInt(inicialInput.value);
            const final = parseInt(finalInput.value);
            
            let isValid = true;
            
            // Reset validation classes
            [inicialInput, finalInput].forEach(input => {
                input.classList.remove('is-invalid', 'is-valid');
            });

            // Validate inicial
            if (isNaN(inicial) || inicial < 0) {
                inicialInput.classList.add('is-invalid');
                isValid = false;
            } else {
                inicialInput.classList.add('is-valid');
            }

            // Validate final
            if (isNaN(final) || final < 0) {
                finalInput.classList.add('is-invalid');
                isValid = false;
            } else if (!isNaN(inicial) && final <= inicial) {
                finalInput.classList.add('is-invalid');
                isValid = false;
            } else if (!isNaN(inicial) && (final - inicial) < 2) {
                finalInput.classList.add('is-invalid');
                isValid = false;
            } else {
                finalInput.classList.add('is-valid');
            }

            // Update submit button state
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = !isValid;
            }

            return isValid;
        }

        inicialInput.addEventListener('input', validateCalculationInputs);
        finalInput.addEventListener('input', validateCalculationInputs);
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Smooth scroll to results after calculation
    if (window.location.hash) {
        const target = document.querySelector(window.location.hash);
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    }

    // Format currency inputs
    const currencyInputs = document.querySelectorAll('input[type="number"][step="0.01"]');
    currencyInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value && !isNaN(this.value)) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(event) {
        // Ctrl/Cmd + Enter to submit the first form on the page
        if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
            const firstForm = document.querySelector('form');
            if (firstForm) {
                firstForm.requestSubmit();
            }
        }
    });

    // Add confirmation for dangerous actions
    const dangerousActions = document.querySelectorAll('form[action*="/eliminar/"], form[action*="/limpiar"]');
    dangerousActions.forEach(form => {
        form.addEventListener('submit', function(event) {
            const action = this.action;
            let confirmMessage = '¿Está seguro de que desea realizar esta acción?';
            
            if (action.includes('/eliminar/')) {
                confirmMessage = '¿Está seguro de que desea eliminar esta taquilla?';
            } else if (action.includes('/limpiar')) {
                confirmMessage = '¿Está seguro de que desea eliminar todas las taquillas? Esta acción no se puede deshacer.';
            }
            
            if (!confirm(confirmMessage)) {
                event.preventDefault();
            }
        });
    });

    // Initialize any popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    console.log('Calculadora de Taquillas initialized successfully');
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN'
    }).format(amount);
}

function showNotification(message, type = 'info') {
    // Create a temporary alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }
    }, 3000);
}
