document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Update buttons
            tabButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Update content
            tabContents.forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(`${targetTab}-tab`).classList.add('active');
        });
    });

    // Form elements
    const htmlForm = document.getElementById('htmlForm');
    const imageForm = document.getElementById('imageForm');
    const textForm = document.getElementById('textForm');
    
    const htmlFileInput = document.getElementById('htmlFile');
    const imageFileInput = document.getElementById('imageFile');
    const textInput = document.getElementById('textInput');
    
    const resultsSection = document.getElementById('results');
    const errorDiv = document.getElementById('error');
    const brochuresGrid = document.getElementById('brochuresGrid');

    // Update file labels when files are selected
    htmlFileInput.addEventListener('change', function(e) {
        const fileName = e.target.files[0]?.name || 'Choose HTML File';
        const label = htmlForm.querySelector('.file-label-text');
        if (label) label.textContent = fileName;
    });

    imageFileInput.addEventListener('change', function(e) {
        const fileName = e.target.files[0]?.name || 'Choose Image';
        const label = imageForm.querySelector('.file-label-text');
        if (label) label.textContent = fileName;
    });

    // Handle form submissions
    function handleSubmit(form, validateFn) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!validateFn()) {
                return;
            }

            const formData = new FormData(form);
            const submitBtn = form.querySelector('.btn-primary');
            const btnText = submitBtn.querySelector('.btn-text');
            const btnLoader = submitBtn.querySelector('.btn-loader');

            // Show loading state
            submitBtn.disabled = true;
            btnText.style.display = 'none';
            btnLoader.style.display = 'inline';
            resultsSection.style.display = 'none';
            errorDiv.style.display = 'none';

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || 'Failed to generate brochures');
                }

                // Display results
                displayBrochures(data);
                resultsSection.style.display = 'block';
                
            } catch (error) {
                showError(error.message);
            } finally {
                // Reset button state
                submitBtn.disabled = false;
                btnText.style.display = 'inline';
                btnLoader.style.display = 'none';
            }
        });
    }

    // HTML form
    handleSubmit(htmlForm, function() {
        if (!htmlFileInput.files[0]) {
            showError('Please select an HTML file');
            return false;
        }
        return true;
    });

    // Image form
    handleSubmit(imageForm, function() {
        if (!imageFileInput.files[0]) {
            showError('Please select an image file');
            return false;
        }
        return true;
    });

    // Text form
    handleSubmit(textForm, function() {
        if (!textInput.value.trim()) {
            showError('Please enter some text or idea');
            return false;
        }
        return true;
    });

    function displayBrochures(data) {
        brochuresGrid.innerHTML = '';
        
        const audiences = ['customers', 'investors', 'partners'];
        
        audiences.forEach(audience => {
            const brochure = data.brochures[audience];
            const imageUrl = data.images[audience];
            
            if (!brochure) return;

            const card = document.createElement('div');
            card.className = 'brochure-card';
            
            // Convert markdown-like content to HTML (simple conversion)
            const content = convertMarkdownToHtml(brochure);
            
            card.innerHTML = `
                <div class="brochure-header">
                    <img src="${imageUrl}" alt="${audience} brochure background" class="brochure-bg">
                    <div class="brochure-title">${audience.charAt(0).toUpperCase() + audience.slice(1)} Brochure</div>
                </div>
                <div class="brochure-content">
                    ${content}
                </div>
            `;
            
            brochuresGrid.appendChild(card);
        });
    }

    function convertMarkdownToHtml(markdown) {
        let html = markdown;
        
        // Convert headers
        html = html.replace(/^## (.+)$/gm, '<h3>$1</h3>');
        html = html.replace(/^### (.+)$/gm, '<h4>$1</h4>');
        
        // Convert bold
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        
        // Convert lists
        html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
        html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
        
        // Convert paragraphs
        html = html.split('\n\n').map(para => {
            if (!para.trim()) return '';
            if (para.startsWith('<')) return para;
            return `<p>${para}</p>`;
        }).join('');
        
        return html;
    }

    function showError(message) {
        errorDiv.textContent = `Error: ${message}`;
        errorDiv.style.display = 'block';
    }
});
