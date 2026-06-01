(function () {
    function fit(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    }

    document.querySelectorAll('textarea').forEach(function (textarea) {
        fit(textarea);
        textarea.addEventListener('input', function () {
            fit(textarea);
        });
    });
})();
