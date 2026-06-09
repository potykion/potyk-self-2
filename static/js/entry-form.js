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

    function initEntryFormsIn(root) {
        if (!root?.querySelectorAll) return;

        if (root.matches?.('form[action^="/edit-entry/"]') || root.id === 'new-entry-form') {
            initEntryForm(root);
            return;
        }

        root.querySelectorAll('form[action^="/edit-entry/"]').forEach(initEntryForm);
        const newForm = root.querySelector('#new-entry-form');
        if (newForm) initEntryForm(newForm);
    }

    if (typeof htmx !== 'undefined') {
        htmx.onLoad(initEntryFormsIn);
    } else {
        initEntryFormsIn(document.body);
    }
})();
