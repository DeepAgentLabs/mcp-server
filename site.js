/* =========================================================
   DeepAgentLabs MCP Server
   Landing Page JavaScript
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  setupMobileMenu();
  setupCopyButtons();
  setupScrollReveal();
});


/* =========================================================
   MOBILE MENU
   ========================================================= */

function setupMobileMenu() {
  const menuButton = document.getElementById("mobile-menu-button");
  const mobileNav = document.getElementById("mobile-nav");

  if (!menuButton || !mobileNav) {
    return;
  }

  menuButton.addEventListener("click", () => {
    mobileNav.classList.toggle("open");

    const isOpen = mobileNav.classList.contains("open");

    menuButton.setAttribute(
      "aria-label",
      isOpen ? "Close navigation" : "Open navigation"
    );

    const icon = menuButton.querySelector(".material-symbols-outlined");

    if (icon) {
      icon.textContent = isOpen ? "close" : "menu";
    }
  });

  // Close mobile menu after clicking a navigation link
  mobileNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      mobileNav.classList.remove("open");

      const icon = menuButton.querySelector(".material-symbols-outlined");

      if (icon) {
        icon.textContent = "menu";
      }

      menuButton.setAttribute(
        "aria-label",
        "Open navigation"
      );
    });
  });
}


/* =========================================================
   COPY BUTTONS
   ========================================================= */

function setupCopyButtons() {
  const copyButtons = document.querySelectorAll(
    ".copy-button[data-copy]"
  );

  copyButtons.forEach((button) => {
    button.addEventListener("click", async () => {
      const text = button.getAttribute("data-copy");

      if (!text) {
        return;
      }

      try {
        await copyText(text);

        showCopyToast();

        const icon = button.querySelector(
          ".material-symbols-outlined"
        );

        if (icon) {
          const originalIcon = icon.textContent;

          icon.textContent = "check";

          setTimeout(() => {
            icon.textContent = originalIcon;
          }, 1500);
        }

      } catch (error) {
        console.error("Copy failed:", error);
      }
    });
  });
}


/* =========================================================
   CLIPBOARD
   ========================================================= */

async function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return;
  }

  // Fallback for local HTTP development
  const textarea = document.createElement("textarea");

  textarea.value = text;

  textarea.style.position = "fixed";
  textarea.style.left = "-9999px";
  textarea.style.top = "-9999px";

  document.body.appendChild(textarea);

  textarea.focus();
  textarea.select();

  document.execCommand("copy");

  textarea.remove();
}


/* =========================================================
   COPY TOAST
   ========================================================= */

let toastTimeout;

function showCopyToast() {
  const toast = document.getElementById("copy-toast");

  if (!toast) {
    return;
  }

  toast.classList.add("show");

  clearTimeout(toastTimeout);

  toastTimeout = setTimeout(() => {
    toast.classList.remove("show");
  }, 1800);
}


/* =========================================================
   SCROLL REVEAL
   ========================================================= */

function setupScrollReveal() {
  const elements = document.querySelectorAll(
    ".capability-card, " +
    ".service-card, " +
    ".workflow-step, " +
    ".developer-stat, " +
    ".travel-node, " +
    ".travel-result, " +
    ".code-block"
  );

  if (!elements.length) {
    return;
  }

  // Respect reduced-motion preference
  if (
    window.matchMedia &&
    window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches
  ) {
    return;
  }

  elements.forEach((element) => {
    element.style.opacity = "0";
    element.style.transform = "translateY(18px)";
    element.style.transition =
      "opacity 600ms ease, transform 600ms ease";
  });

  const observer = new IntersectionObserver(
    (entries, observerInstance) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";

        observerInstance.unobserve(entry.target);
      });
    },
    {
      threshold: 0.12
    }
  );

  elements.forEach((element) => {
    observer.observe(element);
  });
}