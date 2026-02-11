document.addEventListener('DOMContentLoaded', () => {
    const triggers = document.querySelectorAll('.help-trigger');

    // Toggle Function
    triggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();

            const isExpanded = trigger.getAttribute('aria-expanded') === 'true';

            // Close all others first
            closeAllTooltips();

            if (!isExpanded) {
                trigger.setAttribute('aria-expanded', 'true');
                // Optional: positioning logic if boundary detection is needed
                adjustTooltipPosition(trigger);
            }
        });
    });

    // Close on Outside Click
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.help-trigger') && !e.target.closest('.tooltip-content')) {
            closeAllTooltips();
        }
    });

    // Close on ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAllTooltips();
        }
    });

    function closeAllTooltips() {
        triggers.forEach(t => t.setAttribute('aria-expanded', 'false'));
    }

    function adjustTooltipPosition(trigger) {
        // Simple logic to prevent overflow on mobile right edge
        const tooltip = trigger.nextElementSibling;
        if (!tooltip) return;

        // Reset styling
        tooltip.style.left = '0';
        tooltip.style.right = 'auto';

        const rect = tooltip.getBoundingClientRect();
        const viewportWidth = window.innerWidth;

        if (rect.right > viewportWidth) {
            tooltip.style.left = 'auto';
            tooltip.style.right = '0';
        }
    }
});