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

    function parseTagsValue(raw) {
        return raw
            .split(',')
            .map((tag) => tag.trim())
            .filter(Boolean);
    }

    function ensureTagOptions(tags) {
        const seen = new Set(tagOptions.map((option) => option.value));
        tags.forEach((tag) => {
            if (seen.has(tag)) return;
            tagOptions.push({ value: tag, text: tag });
            seen.add(tag);
        });
    }

    function copyViaExecCommand(textarea) {
        textarea.focus();
        const wasReadOnly = textarea.readOnly;
        textarea.readOnly = true;
        textarea.select();
        textarea.setSelectionRange(0, textarea.value.length);
        const copied = document.execCommand('copy');
        textarea.readOnly = wasReadOnly;
        return copied;
    }

    async function copyTextarea(textarea) {
        if (copyViaExecCommand(textarea)) return;

        if (navigator.clipboard?.writeText) {
            try {
                await navigator.clipboard.writeText(textarea.value);
            } catch {
                // ignore
            }
        }
    }

    function initEntryFormMore(form) {
        const more = form.querySelector('.entry-form-more');
        if (!more) return;

        more.querySelectorAll('.entry-form-more__menu button').forEach((btn) => {
            btn.addEventListener('click', () => {
                more.open = false;
            });
        });

        form.querySelectorAll('textarea').forEach((textarea) => {
            textarea.addEventListener('focus', () => {
                more.open = false;
            });
        });
    }

    function initEntryForm(form) {
        form.querySelectorAll('.tags-input').forEach((el) => {
            const tags = parseTagsValue(el.value);
            ensureTagOptions(tags);
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
                copyTextarea(textarea);
            });
        });

        if (form.matches('form[action^="/edit-entry/"]')) {
            initEntryFormMore(form);
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
