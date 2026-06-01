(function () {
    const STORAGE_KEY = 'potyk-self-2:new-entry';
    const DEBOUNCE_MS = 400;

    const form = document.getElementById('new-entry-form');
    if (!form) return;

    const titleInput = form.querySelector('[name="title"]');
    const textArea = form.querySelector('[name="text"]');
    const clearBtn = document.getElementById('new-entry-clear');

    function readDraft() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
        } catch {
            return {};
        }
    }

    function writeDraft() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
            title: titleInput.value,
            text: textArea.value,
        }));
    }

    function clearDraft() {
        localStorage.removeItem(STORAGE_KEY);
    }

    let saveTimer;
    function scheduleSave() {
        clearTimeout(saveTimer);
        saveTimer = setTimeout(writeDraft, DEBOUNCE_MS);
    }

    const draft = readDraft();
    if (draft.title) titleInput.value = draft.title;
    if (draft.text) {
        textArea.value = draft.text;
        textArea.dispatchEvent(new Event('input', { bubbles: true }));
    }

    titleInput.addEventListener('input', scheduleSave);
    textArea.addEventListener('input', scheduleSave);

    clearBtn.addEventListener('click', function () {
        textArea.value = '';
        textArea.dispatchEvent(new Event('input', { bubbles: true }));
        writeDraft();
    });

    form.addEventListener('submit', clearDraft);
})();
