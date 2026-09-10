/**
 * usesuno.com â€” mobile nav, theme, toast helper
 */
(function () {
    var THEME_STORAGE_KEY = "usesuno-theme";
    var themeMedia = window.matchMedia
        ? window.matchMedia("(prefers-color-scheme: dark)")
        : null;

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

    function resolveTheme(preference) {
        if (preference === "light" || preference === "dark") return preference;
        return themeMedia && themeMedia.matches ? "dark" : "light";
    }

    function getThemePreference() {
        var preference = document.documentElement.dataset.themePreference;
        return preference === "light" || preference === "dark" || preference === "system"
            ? preference
            : "system";
    }

    function updateThemeControl(preference) {
        var trigger = document.querySelector(".theme-control__trigger");
        var labels = {
            system: "Appearance: System",
            light: "Appearance: Light",
            dark: "Appearance: Dark"
        };

        if (trigger) {
            trigger.setAttribute("aria-label", labels[preference]);
            trigger.dataset.label = labels[preference];
        }

        document.querySelectorAll(".theme-choice").forEach(function (choice) {
            choice.setAttribute(
                "aria-checked",
                choice.dataset.themeChoice === preference ? "true" : "false"
            );
        });
    }

    function applyThemePreference(preference, persist) {
        var resolved = resolveTheme(preference);
        document.documentElement.dataset.themePreference = preference;
        document.documentElement.dataset.theme = resolved;
        document.documentElement.style.colorScheme = resolved;

        if (persist) {
            try {
                window.localStorage.setItem(THEME_STORAGE_KEY, preference);
            } catch (error) {
                // Keep the active theme even when storage is restricted.
            }
        }

        updateThemeControl(preference);
    }

    function closeThemeMenu(returnFocus) {
        var trigger = document.querySelector(".theme-control__trigger");
        var menu = document.querySelector(".theme-menu");
        if (!trigger || !menu || menu.hidden) return;
        menu.hidden = true;
        trigger.setAttribute("aria-expanded", "false");
        if (returnFocus) trigger.focus();
    }

    function buildThemeControl() {
        var links = document.getElementById("nav-links");
        if (!links || links.querySelector(".theme-control")) return;

        var control = document.createElement("div");
        control.className = "theme-control";
        control.innerHTML =
            '<button class="theme-control__trigger" type="button" aria-haspopup="menu" aria-expanded="false">' +
            '<span class="theme-control__glyph" aria-hidden="true"></span>' +
            "</button>" +
            '<div class="theme-menu" role="menu" aria-label="Appearance" hidden>' +
            '<button class="theme-choice" type="button" role="menuitemradio" data-theme-choice="system" aria-checked="false">' +
            '<span class="theme-choice__icon" aria-hidden="true">A</span>' +
            '<span class="theme-choice__label">System</span>' +
            '<span class="theme-choice__check" aria-hidden="true">âœ“</span>' +
            "</button>" +
            '<button class="theme-choice" type="button" role="menuitemradio" data-theme-choice="light" aria-checked="false">' +
            '<span class="theme-choice__icon" aria-hidden="true">L</span>' +
            '<span class="theme-choice__label">Light</span>' +
            '<span class="theme-choice__check" aria-hidden="true">âœ“</span>' +
            "</button>" +
            '<button class="theme-choice" type="button" role="menuitemradio" data-theme-choice="dark" aria-checked="false">' +
            '<span class="theme-choice__icon" aria-hidden="true">D</span>' +
            '<span class="theme-choice__label">Dark</span>' +
            '<span class="theme-choice__check" aria-hidden="true">âœ“</span>' +
            "</button>" +
            "</div>";
        links.appendChild(control);

        var trigger = control.querySelector(".theme-control__trigger");
        var menu = control.querySelector(".theme-menu");
        trigger.addEventListener("click", function () {
            var open = menu.hidden;
            menu.hidden = !open;
            trigger.setAttribute("aria-expanded", open ? "true" : "false");
            if (open) {
                var active = menu.querySelector('[aria-checked="true"]');
                (active || menu.querySelector(".theme-choice")).focus();
            }
        });

        menu.querySelectorAll(".theme-choice").forEach(function (choice) {
            choice.addEventListener("click", function () {
                applyThemePreference(choice.dataset.themeChoice, true);
                closeThemeMenu(true);
            });
        });

        menu.addEventListener("keydown", function (event) {
            var choices = Array.prototype.slice.call(menu.querySelectorAll(".theme-choice"));
            var current = choices.indexOf(document.activeElement);
            var next = current;

            if (event.key === "ArrowDown") next = (current + 1) % choices.length;
            if (event.key === "ArrowUp") next = (current - 1 + choices.length) % choices.length;
            if (event.key === "Home") next = 0;
            if (event.key === "End") next = choices.length - 1;

            if (next !== current) {
                event.preventDefault();
                choices[next].focus();
            }
        });

        updateThemeControl(getThemePreference());
    }

    function updateSiteNavSolid() {
        var nav = document.querySelector(".site-nav");
        var links = document.getElementById("nav-links");
        if (!nav) return;
        var y = window.scrollY || document.documentElement.scrollTop || 0;
        var menuOpen = links && links.classList.contains("is-open");
        nav.classList.toggle("is-scrolled", y > 12 || menuOpen);
    }

    function enhancePrimaryLyricMvLink() {
        var links = document.getElementById("nav-links");
        if (!links) return;

        var link = links.querySelector("[data-nav-lyric-mv]");
        if (!link) {
            link = document.createElement("a");
            link.href = "/tools/lyrics-mv/";
            link.setAttribute("data-nav-lyric-mv", "true");
            var tools = links.querySelector(".nav-tools");
            if (tools && tools.parentNode) tools.parentNode.insertBefore(link, tools.nextSibling);
            else links.appendChild(link);
        }
        link.classList.add("nav-lyric-mv");
        link.removeAttribute("target");
        link.removeAttribute("rel");
        link.setAttribute("aria-label", "Lyrics MV Studio â€” make a lyric video");
        link.innerHTML = '<span translate="no">Lyrics MV</span>';
    }

    function enhanceToolsMenus() {
        var LYRIC_MV_URL = "/tools/lyrics-mv/";
        var categories = [
            {
                label: "Create & edit",
                links: [
                    "/tools/builder/",
                    "/tools/diff/",
                    "/tools/lyrics-timestamp/",
                    "/tools/formatter/",
                    "/tools/normalize/",
                    "/tools/random/"
                ]
            },
            {
                label: "Inspect & refine",
                links: [
                    "/tools/parser/",
                    "/tools/timing/",
                    "/tools/cleaner/",
                    "/tools/exclude/"
                ]
            },
            {
                label: "Download & collect",
                links: [
                    "/tools/downloader/",
                    "/tools/batch/",
                    "/tools/cover/",
                    "/tools/playlist/",
                    "/tools/profile-downloader/"
                ]
            }
        ];

        document.querySelectorAll(".nav-tools__menu").forEach(function (menu, index) {
            if (menu.dataset.grouped === "true") return;

            var trigger = menu.parentElement.querySelector(".nav-tools__trigger");
            if (!menu.id) menu.id = index === 0 ? "nav-tools-menu" : "nav-tools-menu-" + (index + 1);
            if (trigger) {
                trigger.setAttribute("aria-haspopup", "true");
                trigger.setAttribute("aria-controls", menu.id);
                trigger.setAttribute("aria-expanded", "false");
            }

            var linksByHref = {};
            Array.prototype.slice.call(menu.children).forEach(function (child) {
                if (child.tagName === "A") linksByHref[child.getAttribute("href")] = child;
            });

            var fragment = document.createDocumentFragment();
            var used = {};

            categories.forEach(function (category) {
                var group = document.createElement("div");
                group.className = "nav-tools__group";

                var heading = document.createElement("span");
                heading.className = "nav-tools__heading";
                heading.setAttribute("role", "heading");
                heading.setAttribute("aria-level", "3");
                heading.textContent = category.label;
                group.appendChild(heading);

                category.links.forEach(function (href) {
                    var link = linksByHref[href];
                    if (!link) return;
                    used[href] = true;
                    group.appendChild(link);
                });

                fragment.appendChild(group);
            });

            var featuredLink = linksByHref[LYRIC_MV_URL];
            if (!featuredLink) {
                featuredLink = document.createElement("a");
                featuredLink.href = LYRIC_MV_URL;
                linksByHref[LYRIC_MV_URL] = featuredLink;
            }
            featuredLink.classList.add("nav-tools__featured");
            featuredLink.removeAttribute("target");
            featuredLink.removeAttribute("rel");
            featuredLink.setAttribute("aria-label", "Lyrics MV Studio â€” make a lyric video");
            featuredLink.innerHTML =
                '<span class="nav-tools__featured-copy"><strong translate="no">Lyrics MV Studio</strong><span>Make a lyric video</span></span>';
            var featuredGroup = document.createElement("div");
            featuredGroup.className = "nav-tools__group nav-tools__group--featured";
            featuredGroup.appendChild(featuredLink);
            used[LYRIC_MV_URL] = true;
            fragment.appendChild(featuredGroup);

            Object.keys(linksByHref).forEach(function (href) {
                if (used[href]) return;
                var fallback = document.createElement("div");
                fallback.className = "nav-tools__group";
                fallback.appendChild(linksByHref[href]);
                fragment.appendChild(fallback);
            });

            menu.textContent = "";
            menu.appendChild(fragment);
            menu.dataset.grouped = "true";
        });
    }

    function setupToolsMenuInteractions() {
        var desktopMedia = window.matchMedia ? window.matchMedia("(min-width: 1151px)") : null;

        document.querySelectorAll(".nav-tools").forEach(function (control) {
            if (control.dataset.interactive === "true") return;

            var trigger = control.querySelector(".nav-tools__trigger");
            var menu = control.querySelector(".nav-tools__menu");
            if (!trigger || !menu) return;

            var triggerRow = trigger.parentElement;
            if (!triggerRow || !triggerRow.classList.contains("nav-tools__trigger-row")) {
                triggerRow = document.createElement("div");
                triggerRow.className = "nav-tools__trigger-row";
                trigger.parentNode.insertBefore(triggerRow, trigger);
                triggerRow.appendChild(trigger);
            }

            var menuToggle = triggerRow.querySelector(".nav-tools__toggle");
            if (!menuToggle) {
                menuToggle = document.createElement("button");
                menuToggle.className = "nav-tools__toggle";
                menuToggle.type = "button";
                menuToggle.setAttribute("aria-label", "Show Tools menu");
                triggerRow.appendChild(menuToggle);
            }
            menuToggle.setAttribute("aria-controls", menu.id);
            menuToggle.setAttribute("aria-expanded", "false");
            control.classList.add("is-mobile-ready");

            var closeTimer = null;

            function setExpanded(open) {
                trigger.setAttribute("aria-expanded", open ? "true" : "false");
                menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
                menuToggle.setAttribute("aria-label", open ? "Hide Tools menu" : "Show Tools menu");
            }

            function cancelClose() {
                if (closeTimer === null) return;
                window.clearTimeout(closeTimer);
                closeTimer = null;
            }

            function openMenu() {
                if (desktopMedia && !desktopMedia.matches) return;
                cancelClose();
                control.classList.add("is-open");
                setExpanded(true);
            }

            function closeMenu(returnFocus) {
                cancelClose();
                control.classList.remove("is-open");
                setExpanded(false);
                if (returnFocus) trigger.focus();
            }

            function scheduleClose() {
                cancelClose();
                closeTimer = window.setTimeout(function () {
                    if (!control.matches(":focus-within")) closeMenu(false);
                }, 220);
            }

            trigger.addEventListener("pointerenter", openMenu);
            trigger.addEventListener("pointerleave", scheduleClose);
            menu.addEventListener("pointerenter", openMenu);
            menu.addEventListener("pointerleave", scheduleClose);
            control.addEventListener("focusin", openMenu);
            control.addEventListener("focusout", function (event) {
                if (!control.contains(event.relatedTarget)) scheduleClose();
            });
            control.addEventListener("keydown", function (event) {
                if (event.key !== "Escape" || !control.classList.contains("is-open")) return;
                event.preventDefault();
                closeMenu(true);
            });

            menuToggle.addEventListener("click", function () {
                if (desktopMedia && desktopMedia.matches) return;
                var open = !control.classList.contains("is-open");
                if (open) {
                    cancelClose();
                    control.classList.add("is-open");
                } else {
                    control.classList.remove("is-open");
                }
                setExpanded(open);
            });

            if (desktopMedia) {
                var syncMenuMode = function () {
                    closeMenu(false);
                };
                if (typeof desktopMedia.addEventListener === "function") {
                    desktopMedia.addEventListener("change", syncMenuMode);
                } else if (typeof desktopMedia.addListener === "function") {
                    desktopMedia.addListener(syncMenuMode);
                }
            }

            control.dataset.interactive = "true";
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        enhancePrimaryLyricMvLink();
        enhanceToolsMenus();
        setupToolsMenuInteractions();
        buildThemeControl();
        var toggle = document.querySelector(".nav-toggle");
        var links = document.getElementById("nav-links");
        if (toggle && links) {
            var nav = toggle.closest(".site-nav") || document.querySelector(".site-nav");
            var backdrop = null;
            if (nav) {
                backdrop = document.createElement("button");
                backdrop.type = "button";
                backdrop.className = "nav-backdrop";
                backdrop.setAttribute("aria-label", "Close menu");
                backdrop.hidden = true;
                nav.appendChild(backdrop);
            }

            function closeToolsMenus() {
                links.querySelectorAll(".nav-tools.is-open").forEach(function (control) {
                    control.classList.remove("is-open");
                    var trigger = control.querySelector(".nav-tools__trigger");
                    var menuToggle = control.querySelector(".nav-tools__toggle");
                    if (trigger) trigger.setAttribute("aria-expanded", "false");
                    if (menuToggle) {
                        menuToggle.setAttribute("aria-expanded", "false");
                        menuToggle.setAttribute("aria-label", "Show Tools menu");
                    }
                });
            }

            function setPrimaryMenu(open, returnFocus) {
                links.classList.toggle("is-open", open);
                if (!open) closeToolsMenus();
                toggle.setAttribute("aria-expanded", open ? "true" : "false");
                toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
                if (backdrop) backdrop.hidden = !open;
                updateSiteNavSolid();
                if (returnFocus) toggle.focus();
            }

            toggle.addEventListener("click", function () {
                setPrimaryMenu(!links.classList.contains("is-open"), false);
            });

            if (backdrop) backdrop.addEventListener("click", function () {
                setPrimaryMenu(false, true);
            });

            links.querySelectorAll("a").forEach(function (a) {
                a.addEventListener("click", function () {
                    setPrimaryMenu(false, false);
                });
            });

            document.addEventListener("keydown", function (event) {
                if (event.key !== "Escape" || !links.classList.contains("is-open")) return;
                event.preventDefault();
                setPrimaryMenu(false, true);
            });
        }
        updateSiteNavSolid();
        window.addEventListener("scroll", updateSiteNavSolid, { passive: true });
        window.addEventListener("resize", updateSiteNavSolid);

        document.addEventListener("click", function (event) {
            var control = document.querySelector(".theme-control");
            if (control && !control.contains(event.target)) closeThemeMenu(false);
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") closeThemeMenu(true);
        });

        if (themeMedia) {
            var syncSystemTheme = function () {
                if (getThemePreference() === "system") {
                    applyThemePreference("system", false);
                }
            };
            if (typeof themeMedia.addEventListener === "function") {
                themeMedia.addEventListener("change", syncSystemTheme);
            } else if (typeof themeMedia.addListener === "function") {
                themeMedia.addListener(syncSystemTheme);
            }
        }
    });
})();