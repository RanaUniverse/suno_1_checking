(function () {

    function getToastEl() {
        var el = document.getElementById("toast") || document.getElementById("global-toast");
        if (!el) {
            el = document.createElement("div");
            el.id = "global-toast";
            el.className = "toast";
            el.setAttribute("role", "status");
            el.setAttribute("aria-live", "polite");
            document.body.appendChild(el);
        }
        return el;
    }

    window.showUsesunoToast = function (message, durationMs) {
        var el = getToastEl();
        var ms = typeof durationMs === "number" ? durationMs : 2000;
        el.textContent = message;
        el.classList.add("show");
        clearTimeout(el._hideTimer);
        el._hideTimer = setTimeout(function () {
            el.classList.remove("show");
        }, ms);
    };

})();