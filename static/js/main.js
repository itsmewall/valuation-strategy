document.addEventListener('DOMContentLoaded', () => {

    // Global click delegate for tools
    document.body.addEventListener('click', (e) => {
        // 1. Handle Help Button Click
        const trigger = e.target.closest('.help-btn');

        if (trigger) {
            e.preventDefault();
            e.stopPropagation();

            const bubble = trigger.nextElementSibling;
            const isActive = trigger.classList.contains('active');

            // Close all other tooltips first
            closeAll();

            // If clicked one wasn't active, open it
            if (!isActive && bubble) {
                trigger.classList.add('active');
                bubble.classList.add('visible');
                reposition(trigger, bubble);
            }
            return;
        }

        // 2. Ignore clicks inside the bubble itself (allow text selection)
        if (e.target.closest('.help-bubble')) {
            return;
        }

        // 3. Otherwise (clicked outside), close all
        closeAll();
    });

    // Handle ESC key to close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeAll();
    });

    // Reposition active tooltip on window resize
    window.addEventListener('resize', () => {
        const activeBtn = document.querySelector('.help-btn.active');
        if (activeBtn) {
            reposition(activeBtn, activeBtn.nextElementSibling);
        }
    });

    // Helper: Close all tooltips
    function closeAll() {
        document.querySelectorAll('.help-btn.active').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.help-bubble.visible').forEach(b => b.classList.remove('visible'));
    }

    // Helper: Position tooltip (Flip logic)
    function reposition(trigger, bubble) {
        if (!trigger || !bubble) return;

        // Reset to default (Right side placement)
        bubble.classList.remove('left');

        const bubbleRect = bubble.getBoundingClientRect();
        const viewportWidth = window.innerWidth;

        // If text goes off-screen right, flip to left
        // 20px buffer for scrollbars/margins
        if (bubbleRect.right + 20 > viewportWidth) {
            bubble.classList.add('left');
        }

        // Mobile safety check: if flip causes left overflow (very small screens)
        // We could add logic here, but CSS width restriction usually handles it.
    }

});