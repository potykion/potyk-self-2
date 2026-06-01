(function () {
    document.querySelectorAll('.entries form').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            if (e.submitter?.value === 'delete' && !confirm('Удалить эту запись?')) {
                e.preventDefault();
            }
        });
    });
})();
