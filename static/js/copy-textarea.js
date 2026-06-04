(function () {
    document.querySelectorAll('.copy-text-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const textarea = btn.closest('form').querySelector('textarea');
            if (!textarea) return;
            navigator.clipboard.writeText(textarea.value);
        });
    });
})();
