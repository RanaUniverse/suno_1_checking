/**
 * Resolve the saved appearance before the page is painted.
 * Keep this file tiny and load it from <head> without defer.
 */
// Currently i will not use this, later if i will use bs5 i will use this

(function () {
    var STORAGE_KEY = "usesuno-theme";
    var preference = "system";

    try {
        var saved = window.localStorage.getItem(STORAGE_KEY);
        if (saved === "light" || saved === "dark" || saved === "system") {
            preference = saved;
        }
    } catch (error) {
        // Storage can be unavailable in private or restricted browsing contexts.
    }

    var prefersDark = window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches;
    var resolved = preference === "system"
        ? (prefersDark ? "dark" : "light")
        : preference;

    document.documentElement.dataset.theme = resolved;
    document.documentElement.dataset.themePreference = preference;
    document.documentElement.style.colorScheme = resolved;
})();