document.addEventListener("DOMContentLoaded", function () {

    console.log("CHECKSHEET script.js berhasil dimuat.");

    // =====================================================
    // AUTO HIDE ALERT
    // =====================================================

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            if (typeof bootstrap !== "undefined") {

                const bsAlert =
                    bootstrap.Alert.getOrCreateInstance(alert);

                bsAlert.close();

            } else {

                alert.remove();

            }

        }, 5000);

    });


    // =====================================================
    // SIDEBAR ACTIVE MENU
    // =====================================================

    const currentPath = window.location.pathname;

    const navLinks =
        document.querySelectorAll(".sidebar-nav .nav-link");

    navLinks.forEach(function (link) {

        const href = link.getAttribute("href");

        if (!href || href === "#") {
            return;
        }

        try {

            const linkURL =
                new URL(href, window.location.origin);

            if (
                linkURL.pathname === currentPath
            ) {

                link.classList.add("active");

            }

        } catch (error) {

            console.warn(
                "Tidak dapat membaca URL:",
                href
            );

        }

    });


    // =====================================================
    // CONFIRM DELETE
    // =====================================================

    const deleteButtons =
        document.querySelectorAll("[data-confirm-delete]");

    deleteButtons.forEach(function (button) {

        button.addEventListener("click", function (event) {

            const message =
                button.getAttribute("data-confirm-delete") ||
                "Apakah Anda yakin ingin menghapus data ini?";

            if (!confirm(message)) {

                event.preventDefault();

            }

        });

    });


    // =====================================================
    // FILE IMAGE PREVIEW
    // =====================================================

    const imageInputs =
        document.querySelectorAll(
            'input[type="file"][accept*="image"]'
        );

    imageInputs.forEach(function (input) {

        input.addEventListener("change", function () {

            const file = input.files[0];

            if (!file) {
                return;
            }

            if (!file.type.startsWith("image/")) {

                alert("File yang dipilih bukan gambar.");

                input.value = "";

                return;
            }

            const previewId =
                input.getAttribute("data-preview");

            if (!previewId) {
                return;
            }

            const preview =
                document.getElementById(previewId);

            if (!preview) {
                return;
            }

            const reader = new FileReader();

            reader.onload = function (event) {

                preview.src =
                    event.target.result;

                preview.style.display =
                    "block";

            };

            reader.readAsDataURL(file);

        });

    });


    // =====================================================
    // TABLE SEARCH
    // =====================================================

    const searchInputs =
        document.querySelectorAll(
            "[data-table-search]"
        );

    searchInputs.forEach(function (input) {

        const tableSelector =
            input.getAttribute("data-table-search");

        const table =
            document.querySelector(tableSelector);

        if (!table) {
            return;
        }

        input.addEventListener("input", function () {

            const keyword =
                input.value.toLowerCase().trim();

            const rows =
                table.querySelectorAll("tbody tr");

            rows.forEach(function (row) {

                const text =
                    row.innerText.toLowerCase();

                row.style.display =
                    text.includes(keyword)
                        ? ""
                        : "none";

            });

        });

    });


    // =====================================================
    // PREVENT DOUBLE SUBMIT
    // =====================================================

    const forms =
        document.querySelectorAll("form[data-prevent-double]");

    forms.forEach(function (form) {

        form.addEventListener("submit", function () {

            const submitButtons =
                form.querySelectorAll(
                    'button[type="submit"]'
                );

            submitButtons.forEach(function (button) {

                button.disabled = true;

                const originalText =
                    button.innerHTML;

                button.innerHTML =
                    '<span class="spinner-border spinner-border-sm me-2"></span>' +
                    'Memproses...';

                setTimeout(function () {

                    button.disabled = false;

                    button.innerHTML =
                        originalText;

                }, 10000);

            });

        });

    });

});