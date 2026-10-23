document.addEventListener("DOMContentLoaded", function () {

    console.log("================================");
    console.log("CHECKSHEET SCANNER");
    console.log("scanner.js berhasil dimuat");
    console.log("================================");


    // =====================================================
    // ELEMENT
    // =====================================================

    const startButton =
        document.getElementById("startScanner");

    const stopButton =
        document.getElementById("stopScanner");

    const video =
        document.getElementById("scannerVideo");

    const placeholder =
        document.getElementById("scannerPlaceholder");

    const frame =
        document.querySelector(".scan-frame");


    // =====================================================
    // VALIDASI ELEMENT
    // =====================================================

    if (!startButton) {

        console.error(
            "ERROR: #startScanner tidak ditemukan."
        );

        return;
    }

    if (!video) {

        console.error(
            "ERROR: #scannerVideo tidak ditemukan."
        );

        return;
    }


    console.log(
        "Element scanner berhasil ditemukan."
    );


    // =====================================================
    // VARIABLE
    // =====================================================

    let codeReader = null;

    let controls = null;

    let scanning = false;


    // =====================================================
    // RESET UI
    // =====================================================

    function resetScannerUI() {

        video.style.display = "none";

        if (placeholder) {

            placeholder.style.display =
                "flex";

        }

        if (frame) {

            frame.style.display =
                "none";

        }

        startButton.disabled = false;

        if (stopButton) {

            stopButton.disabled = true;

        }

    }


    // =====================================================
    // STOP CAMERA
    // =====================================================

    function stopScanner() {

        console.log(
            "Menghentikan kamera..."
        );

        scanning = false;


        // Stop ZXing
        if (controls) {

            try {

                controls.stop();

            } catch (error) {

                console.warn(
                    "ZXing stop error:",
                    error
                );

            }

            controls = null;

        }


        // Stop camera
        if (video.srcObject) {

            const tracks =
                video.srcObject.getTracks();

            tracks.forEach(function (track) {

                track.stop();

            });

            video.srcObject = null;

        }


        try {

            video.pause();

        } catch (error) {

            console.warn(error);

        }


        resetScannerUI();

    }


    // =====================================================
    // START SCANNER
    // =====================================================

    startButton.addEventListener(
        "click",
        async function () {

            console.log(
                "Tombol Aktifkan Kamera ditekan."
            );


            // =============================================
            // CEK ZXING
            // =============================================

            if (
                typeof ZXingBrowser ===
                "undefined"
            ) {

                console.error(
                    "ZXingBrowser tidak ditemukan."
                );

                alert(
                    "Library scanner ZXing belum berhasil dimuat."
                );

                return;

            }


            console.log(
                "ZXingBrowser tersedia."
            );


            // =============================================
            // CEK CAMERA API
            // =============================================

            if (
                !navigator.mediaDevices ||
                !navigator.mediaDevices.getUserMedia
            ) {

                alert(
                    "Browser tidak mendukung kamera."
                );

                return;

            }


            // =============================================
            // STOP JIKA ADA CAMERA LAMA
            // =============================================

            stopScanner();


            // =============================================
            // TAMPILKAN VIDEO
            // =============================================

            video.style.display =
                "block";

            if (placeholder) {

                placeholder.style.display =
                    "none";

            }

            if (frame) {

                frame.style.display =
                    "block";

            }

            startButton.disabled =
                true;

            if (stopButton) {

                stopButton.disabled =
                    false;

            }


            // =============================================
            // BUAT READER
            // =============================================

            try {

                codeReader =
                    new ZXingBrowser.BrowserMultiFormatReader();

                console.log(
                    "ZXing Reader berhasil dibuat."
                );

            } catch (error) {

                console.error(
                    "Gagal membuat ZXing Reader:",
                    error
                );

                alert(
                    "Scanner gagal dibuat."
                );

                resetScannerUI();

                return;

            }


            // =============================================
            // MULAI SCAN
            // =============================================

            scanning = true;

            try {

                controls =
                    await codeReader.decodeFromVideoDevice(
                        undefined,
                        video,
                        function (
                            result,
                            error
                        ) {

                            // =================================
                            // BARCODE TERBACA
                            // =================================

                            if (
                                result &&
                                scanning
                            ) {

                                const barcode =
                                    result
                                    .getText()
                                    .trim();


                                console.log(
                                    "================================"
                                );

                                console.log(
                                    "BARCODE TERDETEKSI:",
                                    barcode
                                );

                                console.log(
                                    "================================"
                                );


                                if (!barcode) {
                                    return;
                                }


                                scanning =
                                    false;


                                // =============================
                                // STOP CAMERA
                                // =============================

                                if (controls) {

                                    try {

                                        controls.stop();

                                    } catch (e) {

                                        console.warn(e);

                                    }

                                    controls =
                                        null;

                                }


                                if (
                                    video.srcObject
                                ) {

                                    video.srcObject
                                        .getTracks()
                                        .forEach(
                                            function (
                                                track
                                            ) {

                                                track.stop();

                                            }
                                        );

                                    video.srcObject =
                                        null;

                                }


                                // =============================
                                // REDIRECT
                                // =============================

                                const encodedBarcode =
                                    encodeURIComponent(
                                        barcode
                                    );


                                const url =
                                    "/barang/cari/?barcode=" +
                                    encodedBarcode;


                                console.log(
                                    "Redirect:",
                                    url
                                );


                                window.location.href =
                                    url;

                            }

                        }
                    );


                console.log(
                    "Kamera berhasil dijalankan."
                );


            } catch (error) {

                console.error(
                    "Gagal menjalankan kamera:",
                    error
                );

                scanning =
                    false;

                stopScanner();


                if (
                    error &&
                    error.name ===
                    "NotAllowedError"
                ) {

                    alert(
                        "Akses kamera ditolak.\n\n" +
                        "Silakan izinkan kamera pada browser."
                    );

                } else if (
                    error &&
                    error.name ===
                    "NotFoundError"
                ) {

                    alert(
                        "Kamera tidak ditemukan."
                    );

                } else {

                    alert(
                        "Kamera tidak dapat digunakan.\n\n" +
                        "Periksa izin kamera dan koneksi."
                    );

                }

            }

        }
    );


    // =====================================================
    // STOP BUTTON
    // =====================================================

    if (stopButton) {

        stopButton.addEventListener(
            "click",
            function () {

                stopScanner();

            }
        );

    }


    // =====================================================
    // SAAT MENINGGALKAN HALAMAN
    // =====================================================

    window.addEventListener(
        "beforeunload",
        function () {

            stopScanner();

        }
    );


    // =====================================================
    // INITIAL STATE
    // =====================================================

    resetScannerUI();


});