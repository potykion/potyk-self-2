(function () {
    const STORAGE_KEY = 'potyk-self-2:details-open';

    function readState() {
        try {
            return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
        } catch {
            return {};
        }
    }

    function writeState(state) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    }

    const state = readState();

    document.querySelectorAll('details[data-details-id]').forEach((el) => {
        const id = el.dataset.detailsId;
        if (id in state) {
            el.open = state[id];
        }
        el.addEventListener('toggle', () => {
            state[id] = el.open;
            writeState(state);
        });
    });
})();
