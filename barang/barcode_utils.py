import os

import barcode
from barcode.writer import ImageWriter

from django.conf import settings


def generate_barcode(barcode_value):
    """
    Membuat gambar barcode berdasarkan nilai barcode.
    Hasil disimpan di MEDIA_ROOT/barcodes/
    """

    barcode_value = str(barcode_value).strip()

    if not barcode_value:
        return None

    # Folder penyimpanan
    output_dir = os.path.join(
        settings.MEDIA_ROOT,
        "barcodes"
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    # Gunakan Code128
    barcode_class = barcode.get_barcode_class("code128")

    barcode_instance = barcode_class(
        barcode_value,
        writer=ImageWriter()
    )

    # Lokasi file tanpa ekstensi
    filename = os.path.join(
        output_dir,
        barcode_value
    )

    # Generate PNG
    generated_file = barcode_instance.save(
        filename,
        options={
            "write_text": True,
            "module_width": 0.4,
            "module_height": 15,
            "font_size": 10,
            "text_distance": 5,
            "quiet_zone": 6,
        }
    )

    return generated_file