/**
 * Return empty link-entry tools to the paste area after a browser reload.
 * Link-bearing query parameters keep their normal auto-load behavior.
 */
(function () {
    "use strict";

    var navigation = null;
    if (window.performance && typeof window.performance.getEntriesByType === "function") {
        var entries = window.performance.getEntriesByType("navigation");
        if (entries && entries.length) navigation = entries[0];
    }

    var isReload = navigation
        ? navigation.type === "reload"
        : Boolean(window.performance && window.performance.navigation && window.performance.navigation.type === 1);
    if (!isReload) return;

    var params = new URLSearchParams(window.location.search);
    var hasAutoLink = ["url", "id", "profile"].some(function (key) {
        var value = params.get(key);
        return Boolean(value && value.trim());
    });
    if (hasAutoLink) return;

    var previousScrollRestoration = null;
    if (window.history && "scrollRestoration" in window.history) {
        previousScrollRestoration = window.history.scrollRestoration;
        window.history.scrollRestoration = "manual";
    }

    function snapToTop() {
        var root = document.documentElement;
        var previousBehavior = root.style.scrollBehavior;
        root.style.scrollBehavior = "auto";
        window.scrollTo(0, 0);
        root.style.scrollBehavior = previousBehavior;
    }

    function settleAtTop() {
        snapToTop();
        if (window.requestAnimationFrame) window.requestAnimationFrame(snapToTop);
    }

    function restoreScrollRestoration() {
        if (previousScrollRestoration !== null) {
            window.history.scrollRestoration = previousScrollRestoration;
        }
    }

    settleAtTop();
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", settleAtTop, { once: true });
    } else {
        settleAtTop();
    }
    window.addEventListener("load", function () {
        settleAtTop();
        window.setTimeout(function () {
            snapToTop();
            restoreScrollRestoration();
        }, 0);
    }, { once: true });
})();