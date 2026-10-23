from decimal import Decimal, InvalidOperation
from uuid import uuid4

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from barang.models import Barang, TemplateParameter
from inspection.models import (
    FotoInspeksi,
    HasilInspeksi,
    LaporanInspeksi,
)


# =========================================================
# BARANG BY BARCODE API
# =========================================================

class BarangByBarcodeAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, barcode):

        try:
            barang = Barang.objects.get(
                barcode=barcode,
                status=True,
            )

        except Barang.DoesNotExist:
            return Response(
                {
                    "detail": "Barcode tidak ditemukan."
                },
                status=status.HTTP_404_NOT_FOUND,
            )


        # =====================================================
        # AMBIL TEMPLATE BERDASARKAN
        # JENIS + SUB JENIS
        # =====================================================

        template_parameters = list(
            TemplateParameter.objects.filter(
                jenis_equipment=barang.jenis_equipment,
                sub_jenis_equipment=barang.sub_jenis_equipment,
                aktif=True,
            ).order_by(
                "urutan",
                "id",
            )
        )


        # =====================================================
        # BELUM ADA TEMPLATE
        # =====================================================

        if not template_parameters:
            return Response(
                {
                    "detail": (
                        "Belum ada template pemeriksaan untuk "
                        f"{barang.get_jenis_equipment_display()} "
                        f"/ "
                        f"{barang.get_sub_jenis_equipment_display()}"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


        # =====================================================
        # RESPONSE
        # =====================================================

        return Response(
            {
                "id": barang.id,

                "kode_barang": barang.kode_barang,

                "nama_barang": barang.nama_barang,

                "model": barang.model,

                "deskripsi": barang.deskripsi,

                "gambar": (
                    request.build_absolute_uri(
                        barang.gambar.url
                    )
                    if barang.gambar
                    else None
                ),

                "barcode": barang.barcode,

                "jenis_equipment": barang.jenis_equipment,

                "sub_jenis_equipment": (
                    barang.sub_jenis_equipment
                ),

                "items": [
                    {
                        "id": p.id,

                        "urutan": p.urutan,

                        "nama": p.nama_parameter,

                        "instruksi": p.instruksi,

                        "standar": p.standar,

                        "tipe_input": p.tipe_input,

                        "satuan": p.satuan,

                        "min": (
                            str(p.nilai_min)
                            if p.nilai_min is not None
                            else None
                        ),

                        "max": (
                            str(p.nilai_max)
                            if p.nilai_max is not None
                            else None
                        ),

                        "wajib": p.wajib,

                        "foto_referensi": (
                            request.build_absolute_uri(
                                p.foto_referensi.url
                            )
                            if p.foto_referensi
                            else None
                        ),
                    }

                    for p in template_parameters
                ],
            }
        )
    
# =========================================================
# CREATE INSPECTION API
# =========================================================

class InspectionCreateAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # =====================================================
        # AMBIL BARCODE
        # =====================================================

        barcode = str(
            request.data.get(
                "barcode",
                "",
            )
        ).strip()

        if not barcode:
            return Response(
                {
                    "detail": "Barcode wajib diisi."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # =====================================================
        # CARI BARANG
        # =====================================================

        try:
            barang = Barang.objects.get(
                barcode=barcode,
                status=True,
            )

        except Barang.DoesNotExist:
            return Response(
                {
                    "detail": "Barang tidak ditemukan."
                },
                status=status.HTTP_404_NOT_FOUND,
            )


        # =====================================================
        # AMBIL TEMPLATE PEMERIKSAAN
        # BERDASARKAN JENIS EQUIPMENT
        # =====================================================

        template_parameters = list(
            TemplateParameter.objects
            .filter(
                jenis_equipment=barang.jenis_equipment,
                sub_jenis_equipment=barang.sub_jenis_equipment,
                aktif=True,
            )
            .order_by(
                "urutan",
                "id",
            )
        )


        # =====================================================
        # CEK TEMPLATE
        # =====================================================

        if not template_parameters:
            return Response(
                {
                    "detail": (
                        "Belum ada template pemeriksaan untuk "
                        f"{barang.get_jenis_equipment_display()}."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        # =====================================================
        # SIMPAN LAPORAN
        # =====================================================

        with transaction.atomic():

            nomor = (
                f"INS-{timezone.now():%Y%m%d}-"
                f"{uuid4().hex[:6].upper()}"
            )

            laporan = (
                LaporanInspeksi.objects.create(
                    nomor_laporan=nomor,

                    barang=barang,

                    user=request.user,

                    status_hasil="OK",

                    status_approval="PENDING",

                    catatan=str(
                        request.data.get(
                            "catatan",
                            "",
                        )
                    ).strip(),
                )
            )

            # Default laporan OK
            all_pass = True

            # =================================================
            # PROSES SETIAP PARAMETER
            # =================================================

            for p in template_parameters:

                value = str(
                    request.data.get(
                        f"parameter_{p.id}",
                        "",
                    )
                ).strip().upper()

                # -------------------------------------------------
                # Default
                # -------------------------------------------------

                result = "SKIP"

                # =================================================
                # TIPE INPUT OK / NG
                # =================================================

                if p.tipe_input == "okng":

                    if value == "OK":
                        result = "PASS"

                    elif value == "NG":
                        result = "FAIL"

                    else:
                        result = "SKIP"

                # =================================================
                # TIPE INPUT NUMBER
                # =================================================

                elif p.tipe_input == "number":

                    if not value:

                        result = "SKIP"

                    else:

                        try:

                            number = Decimal(
                                value.replace(
                                    ",",
                                    ".",
                                )
                            )

                            # -------------------------------------
                            # Di bawah minimum
                            # -------------------------------------

                            if (
                                p.nilai_min is not None
                                and number < p.nilai_min
                            ):

                                result = "FAIL"

                            # -------------------------------------
                            # Di atas maksimum
                            # -------------------------------------

                            elif (
                                p.nilai_max is not None
                                and number > p.nilai_max
                            ):

                                result = "FAIL"

                            # -------------------------------------
                            # Dalam range
                            # -------------------------------------

                            else:

                                result = "PASS"

                        except (
                            InvalidOperation,
                            ValueError,
                        ):

                            result = "FAIL"

                # =================================================
                # INPUT LAINNYA
                # =================================================

                elif value:

                    result = "PASS"

                else:

                    result = "SKIP"

                # =================================================
                # JIKA HASIL BUKAN PASS
                # =================================================

                if result != "PASS":

                    if p.wajib:
                        all_pass = False

                    # Jika NG, selalu jadikan laporan NG
                    if result == "FAIL":
                        all_pass = False

                # =================================================
                # STATUS REPAIR
                # =================================================

                repair_status = None

                if result == "FAIL":

                    repair_status = str(
                        request.data.get(
                            f"repair_status_{p.id}",
                            "",
                        )
                    ).strip().upper()

                    # ---------------------------------------------
                    # Validasi status repair
                    # ---------------------------------------------

                    if repair_status not in [
                        "REPAIRED",
                        "NOT_REPAIRED",
                    ]:

                        return Response(
                            {
                                "detail": (
                                    "Status repair wajib "
                                    "untuk NG: "
                                    f"{p.nama_parameter}"
                                )
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                # =================================================
                # SIMPAN HASIL INSPEKSI
                # =================================================

                h = HasilInspeksi.objects.create(
                    laporan=laporan,
                    parameter=None,
                    template_parameter=p,
                    nilai_hasil=value,
                    hasil=result,
                    status_repair=repair_status,
                    catatan=str(
                        request.data.get(
                            f"catatan_{p.id}",
                            ""
                        )
                    ).strip(),
                )

                # =================================================
                # JIKA NG → FOTO WAJIB
                # =================================================

                if result == "FAIL":

                    photo = request.FILES.get(
                        f"foto_ng_{p.id}"
                    )

                    if not photo:

                        return Response(
                            {
                                "detail": (
                                    "Foto wajib untuk NG: "
                                    f"{p.nama_parameter}"
                                )
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    # ---------------------------------------------
                    # SIMPAN FOTO NG
                    # ---------------------------------------------

                    FotoInspeksi.objects.create(

                        laporan=laporan,

                        # PENTING:
                        # gunakan h, bukan hasil
                        hasil_inspeksi=h,

                        jenis_foto="NG",

                        file=photo,
                    )

            # =====================================================
            # STATUS AKHIR LAPORAN
            # =====================================================

            laporan.status_hasil = (
                "OK"
                if all_pass
                else "NG"
            )

            laporan.save(
                update_fields=[
                    "status_hasil",
                    "updated_at",
                ]
            )

        # =====================================================
        # RESPONSE
        # =====================================================

        return Response(
            {
                "nomor_laporan": (
                    laporan.nomor_laporan
                ),

                "status_hasil": (
                    laporan.status_hasil
                ),

                "status_approval": (
                    laporan.status_approval
                ),

                "message": (
                    "Hasil inspeksi berhasil "
                    "disimpan dan menunggu approval."
                ),
            },
            status=status.HTTP_201_CREATED,
        )


# =========================================================
# INSPECTION HISTORY API
# =========================================================

class InspectionHistoryAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # =====================================================
        # QUERY LAPORAN
        # =====================================================

        queryset = (
            LaporanInspeksi.objects

            .select_related(
                "barang",
                "user",
                "approved_by",
            )

            .prefetch_related(
                "hasil_parameter__parameter",
                "hasil_parameter__template_parameter",
                "hasil_parameter__foto_ng",
                "foto",
            )

            .order_by(
                "-tanggal_inspeksi"
            )
        )

        # =====================================================
        # FILTER BERDASARKAN ROLE
        # =====================================================
        #
        # SUPERUSER
        #   → semua history
        #
        # ADMIN
        #   → semua history
        #
        # PETUGAS
        #   → history miliknya sendiri
        #
        # =====================================================

        if not request.user.is_superuser:

            try:
                role = (
                    request
                    .user
                    .userprofile
                    .role
                )

            except Exception:

                role = "PETUGAS"

            if role != "ADMIN":

                queryset = queryset.filter(
                    user=request.user
                )

        # =====================================================
        # RESPONSE DATA
        # =====================================================

        results = []

        # Maksimal 200 history
        for laporan in queryset[:200]:

            hasil_list = []

            # =================================================
            # HASIL PARAMETER
            # =================================================

            for hasil in (
                laporan
                .hasil_parameter
                .all()
            ):

                foto_list = []

                # =============================================
                # FOTO NG
                # =============================================

                for foto in (
                    hasil
                    .foto_ng
                    .all()
                ):

                    if foto.file:

                        foto_list.append(
                            request.build_absolute_uri(
                                foto.file.url
                            )
                        )

                # =============================================
                # DATA HASIL
                # =============================================

                hasil_list.append(
                    {
                        "id": hasil.id,

                        "parameter": (
                            hasil.template_parameter.nama_parameter
                            if hasil.template_parameter
                            else (
                                hasil.parameter.nama_parameter
                                if hasil.parameter
                                else "-"
                            )
                        ),

                        "nilai_hasil": (
                            hasil.nilai_hasil
                        ),

                        "hasil": (
                            hasil.hasil
                        ),

                        "catatan": (
                            hasil.catatan
                            or ""
                        ),

                        "status_repair": (
                            getattr(
                                hasil,
                                "status_repair",
                                None,
                            )
                        ),

                        "foto_ng": (
                            foto_list
                        ),
                    }
                )

            # =================================================
            # DATA LAPORAN
            # =================================================

            results.append(
                {
                    "id": laporan.id,

                    "nomor_laporan": (
                        laporan.nomor_laporan
                    ),

                    "kode_barang": (
                        laporan
                        .barang
                        .kode_barang
                    ),

                    "nama_barang": (
                        laporan
                        .barang
                        .nama_barang
                    ),

                    "barcode": (
                        laporan
                        .barang
                        .barcode
                    ),

                    "petugas": (
                        laporan
                        .user
                        .get_full_name()
                        or laporan
                        .user
                        .username
                    ),

                    "tanggal_inspeksi": (
                        laporan
                        .tanggal_inspeksi
                        .strftime(
                            "%d-%m-%Y %H:%M"
                        )
                    ),

                    "status_hasil": (
                        laporan
                        .status_hasil
                    ),

                    "status_approval": (
                        laporan
                        .status_approval
                    ),

                    "catatan": (
                        laporan.catatan
                        or ""
                    ),

                    "hasil": hasil_list,
                }
            )

        # =====================================================
        # RESPONSE
        # =====================================================

        return Response(
            {
                "count": len(results),

                "results": results,
            }
        )