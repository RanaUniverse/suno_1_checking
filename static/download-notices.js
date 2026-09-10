(function () {
    "use strict";

    var STORAGE_KEY = "usesuno:download-rights-notice:v1";
    var modal = null;
    var dialog = null;
    var confirmPanel = null;
    var successPanel = null;
    var continueButton = null;
    var rememberCheckbox = null;
    var doneButton = null;
    var activeRequest = null;
    var returnFocus = null;

    function hasStoredAcknowledgement() {
        try {
            return window.localStorage.getItem(STORAGE_KEY) === "acknowledged";
        } catch (error) {
            return false;
        }
    }

    function storeAcknowledgement() {
        try {
            window.localStorage.setItem(STORAGE_KEY, "acknowledged");
        } catch (error) {
            // The download still continues when storage is blocked or unavailable.
        }
    }

    function icon(path) {
        return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + path + "</svg>";
    }

    function ensureModal() {
        if (modal) return;
        modal = document.createElement("div");
        modal.className = "usesuno-download-modal";
        modal.hidden = true;
        modal.setAttribute("aria-hidden", "true");
        modal.innerHTML =
            '<div class="usesuno-download-modal__backdrop" data-download-modal-dismiss></div>' +
            '<div class="usesuno-download-modal__dialog" role="dialog" aria-modal="true" tabindex="-1">' +
            '<button type="button" class="usesuno-download-modal__close" aria-label="Close">Ã—</button>' +
            '<section class="usesuno-download-modal__confirm">' +
            '<div class="usesuno-download-modal__mark">' + icon('<path d="M12 3v12"></path><path d="m7 10 5 5 5-5"></path><path d="M5 21h14"></path>') + '</div>' +
            '<p class="usesuno-download-modal__eyebrow">Independent third-party tool</p>' +
            '<h2 id="usesuno-download-confirm-title">Before You Download</h2>' +
            '<div class="usesuno-download-modal__copy" id="usesuno-download-confirm-copy">' +
            '<p>UseSuno lets you select and export files from publicly accessible Suno pages. It is not affiliated with or endorsed by Suno, Inc.</p>' +
            '<p><strong>Downloading a file does not grant any additional copyright or commercial-use rights.</strong></p>' +
            '<p>For commercial use, obtain the appropriate download and usage rights directly through Suno\'s official services. You are responsible for ensuring that you have the necessary rights to access, save and use the selected content.</p>' +
            '</div>' +
            '<div class="usesuno-download-modal__actions">' +
            '<label class="usesuno-download-modal__preference">' +
            '<input class="usesuno-download-modal__preference-input" type="checkbox" data-download-remember>' +
            '<span class="usesuno-download-modal__preference-control" aria-hidden="true"></span>' +
            '<span class="usesuno-download-modal__preference-copy">' +
            '<strong>Skip this notice next time</strong>' +
            '<span>Remember on this device</span>' +
            '</span>' +
            '</label>' +
            '<button type="button" class="usesuno-download-modal__button usesuno-download-modal__button--primary" data-download-continue>Continue download</button>' +
            '</div>' +
            '</section>' +
            '<section class="usesuno-download-modal__success" hidden>' +
            '<div class="usesuno-download-modal__mark">' + icon('<path d="m5 12 4 4L19 6"></path>') + '</div>' +
            '<p class="usesuno-download-modal__eyebrow">Download ready</p>' +
            '<h2 id="usesuno-download-success-title">Downloaded successfully.</h2>' +
            '<div class="usesuno-download-modal__copy" id="usesuno-download-success-copy">' +
            '<p>Please note: having an audio or media file does not itself grant commercial-use rights. For commercial use, obtain the appropriate rights through Suno\'s official channels.</p>' +
            '</div>' +
            '<div class="usesuno-download-modal__actions">' +
            '<button type="button" class="usesuno-download-modal__button usesuno-download-modal__button--primary" data-download-done>Done</button>' +
            '</div>' +
            '</section>' +
            '</div>';

        document.body.appendChild(modal);
        dialog = modal.querySelector(".usesuno-download-modal__dialog");
        confirmPanel = modal.querySelector(".usesuno-download-modal__confirm");
        successPanel = modal.querySelector(".usesuno-download-modal__success");
        continueButton = modal.querySelector("[data-download-continue]");
        rememberCheckbox = modal.querySelector("[data-download-remember]");
        doneButton = modal.querySelector("[data-download-done]");
        modal.querySelector(".usesuno-download-modal__close").addEventListener("click", dismissModal);
        modal.querySelector("[data-download-modal-dismiss]").addEventListener("click", dismissModal);
        continueButton.addEventListener("click", function () {
            continueRequest(Boolean(rememberCheckbox && rememberCheckbox.checked));
        });
        doneButton.addEventListener("click", dismissModal);
        document.addEventListener("keydown", handleKeydown);
    }

    function setMode(mode) {
        var isConfirm = mode === "confirm";
        confirmPanel.hidden = !isConfirm;
        successPanel.hidden = isConfirm;
        dialog.setAttribute("aria-labelledby", isConfirm ? "usesuno-download-confirm-title" : "usesuno-download-success-title");
        dialog.setAttribute("aria-describedby", isConfirm ? "usesuno-download-confirm-copy" : "usesuno-download-success-copy");
    }

    function getFocusableElements() {
        if (!dialog) return [];
        return Array.prototype.filter.call(
            dialog.querySelectorAll('button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'),
            function (element) { return !element.hidden && element.getClientRects().length > 0; }
        );
    }

    function handleKeydown(event) {
        if (!modal || modal.hidden) return;
        if (event.key === "Escape") {
            event.preventDefault();
            dismissModal();
            return;
        }
        if (event.key !== "Tab") return;
        var focusable = getFocusableElements();
        if (!focusable.length) {
            event.preventDefault();
            dialog.focus();
            return;
        }
        var first = focusable[0];
        var last = focusable[focusable.length - 1];
        var active = document.activeElement;
        if (event.shiftKey && (active === first || !dialog.contains(active))) {
            event.preventDefault();
            last.focus();
        } else if (!event.shiftKey && active === last) {
            event.preventDefault();
            first.focus();
        }
    }

    function openModal(mode) {
        ensureModal();
        setMode(mode);
        if (mode === "confirm" && rememberCheckbox) rememberCheckbox.checked = false;
        modal.hidden = false;
        modal.setAttribute("aria-hidden", "false");
        document.body.classList.add("usesuno-download-modal-open");
        window.requestAnimationFrame(function () {
            (mode === "confirm" ? continueButton : doneButton).focus();
        });
    }

    function focusAfterClose() {
        var target = returnFocus;
        returnFocus = null;
        if (target && typeof target.focus === "function" && !target.disabled && target.getClientRects().length) {
            target.focus();
            return;
        }
        var heading = document.querySelector("main h1");
        if (!heading) return;
        var hadTabindex = heading.hasAttribute("tabindex");
        if (!hadTabindex) heading.setAttribute("tabindex", "-1");
        heading.focus({ preventScroll: true });
        if (!hadTabindex) heading.addEventListener("blur", function cleanup() {
            heading.removeAttribute("tabindex");
            heading.removeEventListener("blur", cleanup);
        });
    }

    function closeModal(restoreFocus) {
        if (!modal || modal.hidden) return;
        modal.hidden = true;
        modal.setAttribute("aria-hidden", "true");
        document.body.classList.remove("usesuno-download-modal-open");
        if (restoreFocus !== false) focusAfterClose();
    }

    function dismissModal() {
        if (activeRequest) {
            var request = activeRequest;
            activeRequest = null;
            request.resolve(false);
        }
        closeModal(true);
    }

    function continueRequest(remember) {
        if (!activeRequest) return;
        if (remember) storeAcknowledgement();
        var request = activeRequest;
        activeRequest = null;
        closeModal(false);
        Promise.resolve().then(request.action).then(request.resolve, request.reject);
    }

    function run(action) {
        if (typeof action !== "function") return Promise.resolve(false);
        if (activeRequest || (modal && !modal.hidden)) return Promise.resolve(false);
        returnFocus = document.activeElement;
        if (hasStoredAcknowledgement()) return Promise.resolve().then(action);
        return new Promise(function (resolve, reject) {
            activeRequest = { action: action, resolve: resolve, reject: reject };
            openModal("confirm");
        });
    }

    function showSuccess() {
        if (activeRequest) return;
        if (hasStoredAcknowledgement()) return;
        if (!returnFocus) returnFocus = document.activeElement;
        openModal("success");
    }

    function setupRightsFooters() {
        if (!window.matchMedia || !window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
        var cards = document.querySelectorAll("details.download-rights-footer");
        Array.prototype.forEach.call(cards, function (card) {
            var summary = card.querySelector("summary");
            if (!summary) return;

            card.addEventListener("mouseenter", function () {
                if (card.open) return;
                card.dataset.hoverOpened = "true";
                card.open = true;
            });

            card.addEventListener("mouseleave", function () {
                if (card.dataset.hoverOpened !== "true") return;
                card.open = false;
                delete card.dataset.hoverOpened;
            });

            summary.addEventListener("click", function (event) {
                if (card.dataset.hoverOpened !== "true") return;
                event.preventDefault();
                delete card.dataset.hoverOpened;
                card.open = true;
            });
        });
    }

    setupRightsFooters();

    window.UseSunoDownloadNotices = {
        run: run,
        showSuccess: showSuccess,
        storageKey: STORAGE_KEY,
        hasStoredAcknowledgement: hasStoredAcknowledgement
    };
})();