// Form Validation and Submission handling
document.addEventListener("DOMContentLoaded", function() {
    console.log("Rising Waters Frontend Loaded");

    // --- Location Mode Toggle ---
    const autoBtn = document.getElementById('autoLocationBtn');
    const manualBtn = document.getElementById('manualLocationBtn');
    const autoSection = document.getElementById('autoLocationSection');
    const manualSection = document.getElementById('manualLocationSection');

    if (autoBtn && manualBtn) {
        autoBtn.addEventListener('change', function() {
            autoSection.classList.remove('d-none');
            manualSection.classList.add('d-none');
        });
        manualBtn.addEventListener('change', function() {
            manualSection.classList.remove('d-none');
            autoSection.classList.add('d-none');
        });
    }

    // --- Helper: Populate weather fields with animation ---
    function fillWeatherFields(data) {
        const tempField = document.getElementById('temperature');
        const humField = document.getElementById('humidity');
        const visField = document.getElementById('cloud_visibility');

        tempField.value = data.temperature;
        humField.value = data.humidity;
        visField.value = data.cloud_visibility;

        // Flash green highlight on auto-filled fields
        [tempField, humField, visField].forEach(field => {
            field.classList.add('field-synced');
            setTimeout(() => field.classList.remove('field-synced'), 2000);
        });
    }

    // --- Auto-Detect Location (Browser Geolocation) ---
    const detectBtn = document.getElementById('detectLocationBtn');
    if (detectBtn) {
        detectBtn.addEventListener('click', function() {
            const messageDiv = document.getElementById('weatherMessage');

            if (!navigator.geolocation) {
                messageDiv.innerHTML = '<span class="text-danger">Geolocation is not supported by your browser.</span>';
                return;
            }

            // Loading state
            document.getElementById('detectBtnText').textContent = 'Detecting location...';
            document.getElementById('detectBtnSpinner').classList.remove('d-none');
            detectBtn.disabled = true;

            navigator.geolocation.getCurrentPosition(
                function(position) {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;

                    messageDiv.innerHTML = '<span class="text-muted">📡 Location found! Fetching weather data...</span>';

                    fetch('/fetch_weather_coords', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ lat: lat, lon: lon })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            fillWeatherFields(data);
                            messageDiv.innerHTML = `<span class="text-success fw-bold">✓ Live weather synced for <strong>${data.city}</strong> — Temperature: ${data.temperature}°C, Humidity: ${data.humidity}%</span>`;
                        } else {
                            messageDiv.innerHTML = `<span class="text-danger">Error: ${data.error}</span>`;
                        }
                    })
                    .catch(() => {
                        messageDiv.innerHTML = '<span class="text-danger">Network error occurred.</span>';
                    })
                    .finally(() => {
                        document.getElementById('detectBtnText').textContent = '📍 Detect My Location & Fetch Weather';
                        document.getElementById('detectBtnSpinner').classList.add('d-none');
                        detectBtn.disabled = false;
                    });
                },
                function(error) {
                    let errorMsg = 'Could not detect location.';
                    if (error.code === 1) errorMsg = 'Location access denied. Please allow location in your browser settings.';
                    if (error.code === 2) errorMsg = 'Location unavailable.';
                    if (error.code === 3) errorMsg = 'Location request timed out.';
                    messageDiv.innerHTML = `<span class="text-danger">${errorMsg}</span>`;
                    document.getElementById('detectBtnText').textContent = '📍 Detect My Location & Fetch Weather';
                    document.getElementById('detectBtnSpinner').classList.add('d-none');
                    detectBtn.disabled = false;
                }
            );
        });
    }

    // --- Manual City Fetch ---
    const fetchWeatherBtn = document.getElementById('fetchWeatherBtn');
    if (fetchWeatherBtn) {
        fetchWeatherBtn.addEventListener('click', function() {
            const city = document.getElementById('cityInput').value.trim();
            const messageDiv = document.getElementById('weatherMessage');
            
            if (!city) {
                messageDiv.innerHTML = '<span class="text-danger">Please enter a city name first.</span>';
                return;
            }

            // Loading state
            document.getElementById('fetchBtnText').textContent = 'Fetching...';
            document.getElementById('fetchBtnSpinner').classList.remove('d-none');
            fetchWeatherBtn.disabled = true;

            fetch('/fetch_weather', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ city: city })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    fillWeatherFields(data);
                    messageDiv.innerHTML = `<span class="text-success fw-bold">✓ Live weather synced for <strong>${data.city}</strong> — Temperature: ${data.temperature}°C, Humidity: ${data.humidity}%</span>`;
                } else {
                    messageDiv.innerHTML = `<span class="text-danger">Error: ${data.error}</span>`;
                }
            })
            .catch(() => {
                messageDiv.innerHTML = '<span class="text-danger">Network error occurred.</span>';
            })
            .finally(() => {
                document.getElementById('fetchBtnText').textContent = 'Fetch Weather';
                document.getElementById('fetchBtnSpinner').classList.add('d-none');
                fetchWeatherBtn.disabled = false;
            });
        });
    }

    // --- Prediction Form Validation ---
    const form = document.getElementById('predictionForm');
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                const btn = document.getElementById('submitBtn');
                const btnText = document.getElementById('btnText');
                const btnSpinner = document.getElementById('btnSpinner');
                
                if (btn && btnText && btnSpinner) {
                    btnText.textContent = 'Analyzing Data...';
                    btnSpinner.classList.remove('d-none');
                    btn.classList.add('disabled');
                }
            }
            form.classList.add('was-validated');
        }, false);
    }

    // --- Chart.js on Dashboard ---
    if (document.getElementById('rainfallChart') && typeof chartData !== 'undefined') {
        const ctx = document.getElementById('rainfallChart').getContext('2d');
        let currentChart = null;

        function renderChart(type) {
            if (currentChart) {
                currentChart.destroy();
            }

            const chartConfig = {
                type: type,
                data: {
                    labels: ['Annual Rainfall', 'Seasonal Rainfall'],
                    datasets: [{
                        label: 'Input Data (mm)',
                        data: [chartData.annual_rainfall, chartData.seasonal_rainfall],
                        backgroundColor: [
                            'rgba(13, 110, 253, 0.7)',
                            'rgba(13, 202, 240, 0.7)'
                        ],
                        borderColor: [
                            'rgb(13, 110, 253)',
                            'rgb(13, 202, 240)'
                        ],
                        borderWidth: 1,
                        borderRadius: type === 'bar' ? 6 : 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: { color: 'rgba(255, 255, 255, 0.8)' }
                        }
                    },
                    scales: (type === 'pie' || type === 'doughnut') ? {} : {
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            ticks: { color: 'rgba(255, 255, 255, 0.6)' }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { color: 'rgba(255, 255, 255, 0.6)' }
                        }
                    }
                }
            };

            currentChart = new Chart(ctx, chartConfig);
        }

        // Initialize default chart
        renderChart('bar');

        // Event listeners for chart type toggle
        const chartTypeRadios = document.querySelectorAll('input[name="chartType"]');
        chartTypeRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.checked) {
                    renderChart(this.value);
                }
            });
        });
    }
});
