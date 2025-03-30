document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const make = this.querySelector('input[name="make"]');
            const model = this.querySelector('input[name="model"]');
            const year = this.querySelector('input[name="year"]');
            if (!make.value || !model.value || !year.value || year.value < 1900 || year.value > new Date().getFullYear()) {
                alert('Please fill all fields correctly. Year must be between 1900 and current year.');
                event.preventDefault();
            }
        });
    });

    // Dynamic image preview
    const imageInput = document.querySelector('input[name="image"]');
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.style.maxWidth = '200px';
                    img.style.marginTop = '10px';
                    const previewDiv = document.createElement('div');
                    previewDiv.appendChild(img);
                    this.parentElement.appendChild(previewDiv);
                };
                reader.readAsDataURL(file);
            }
        });
    }
});