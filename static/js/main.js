document.addEventListener('DOMContentLoaded', function() {
    // SMS character counter
    const textarea = document.getElementById('message-textarea');
    if (textarea) {
        const counter = document.getElementById('char-counter');
        function updateCounter() {
            const len = textarea.value.length;
            const parts = len === 0 ? 1 : Math.ceil(len / 160);
            const remaining = parts * 160 - len;
            if (counter) {
                counter.textContent = len + ' characters | ' + parts + ' SMS part(s) | ' + remaining + ' remaining';
            }
        }
        textarea.addEventListener('input', updateCounter);
        updateCounter();
    }

    // Recipient type toggle
    const recipientRadios = document.querySelectorAll('input[name="recipient_type"]');
    const groupsSection = document.getElementById('groups-section');
    const manualSection = document.getElementById('manual-section');
    if (recipientRadios.length) {
        function toggleRecipients() {
            const val = document.querySelector('input[name="recipient_type"]:checked');
            if (val) {
                if (groupsSection) groupsSection.style.display = val.value === 'groups' ? 'block' : 'none';
                if (manualSection) manualSection.style.display = val.value === 'manual' ? 'block' : 'none';
            }
        }
        recipientRadios.forEach(r => r.addEventListener('change', toggleRecipients));
        toggleRecipients();
    }

    // Send option toggle
    const sendRadios = document.querySelectorAll('input[name="send_option"]');
    const scheduleSection = document.getElementById('schedule-section');
    if (sendRadios.length) {
        function toggleSendOption() {
            const val = document.querySelector('input[name="send_option"]:checked');
            if (val && scheduleSection) {
                scheduleSection.style.display = val.value === 'schedule' ? 'block' : 'none';
            }
        }
        sendRadios.forEach(r => r.addEventListener('change', toggleSendOption));
        toggleSendOption();
    }

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        document.querySelectorAll('.alert').forEach(function(alert) {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        });
    }, 5000);

    // Sidebar toggle
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
        });
    }

    // Copy API key
    const copyBtn = document.getElementById('copy-api-key');
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            const apiKey = document.getElementById('api-key-value');
            if (apiKey) {
                navigator.clipboard.writeText(apiKey.value || apiKey.textContent.trim()).then(function() {
                    copyBtn.innerHTML = '<i class="bi bi-check"></i> Copied!';
                    setTimeout(function() {
                        copyBtn.innerHTML = '<i class="bi bi-clipboard"></i> Copy';
                    }, 2000);
                });
            }
        });
    }
});
