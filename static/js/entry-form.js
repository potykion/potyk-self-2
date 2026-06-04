(function () {
    const script = document.currentScript;
    const tagOptions = JSON.parse(script.dataset.tagOptions).map((tag) => ({
        value: tag,
        text: tag,
    }));

    function fit(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    }

    function initEntryForm(form) {
        form.querySelectorAll('.tags-input').forEach((el) => {
            el.tomselect?.destroy();
            new TomSelect(el, {
                create: true,
                options: tagOptions,
            });
        });

        form.querySelectorAll('textarea').forEach((textarea) => {
            fit(textarea);
            textarea.addEventListener('input', () => fit(textarea));
        });

        form.querySelectorAll('.copy-text-btn').forEach((btn) => {
            btn.addEventListener('click', () => {
                const textarea = form.querySelector('textarea');
                if (!textarea) return;
                navigator.clipboard.writeText(textarea.value);
            });
        });

        if (form.matches('form[action^="/edit-entry/"]')) {
            form.addEventListener('submit', (e) => {
                if (e.submitter?.value === 'delete' && !confirm('Удалить эту запись?')) {
                    e.preventDefault();
                }
            });
        }
    }

    document.querySelectorAll('form[action^="/edit-entry/"]').forEach((form) => {
        initEntryForm(form);
    });

    const newForm = document.getElementById('new-entry-form');
    if (newForm) {
        initEntryForm(newForm);
    }

    document.body.addEventListener('htmx:afterSwap', (e) => {
        const el = e.detail.elt;
        const form = el.matches?.('form[action^="/edit-entry/"]')
            ? el
            : el.querySelector?.('form[action^="/edit-entry/"]');
        if (form) initEntryForm(form);
    });
})();
