from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("barang", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="barang",
            name="gambar",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="barang/",
            ),
        ),

        migrations.AddField(
            model_name="parameter",
            name="urutan",
            field=models.PositiveIntegerField(default=1),
        ),

        migrations.AddField(
            model_name="parameter",
            name="instruksi",
            field=models.TextField(
                blank=True,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name="parameter",
            name="standar",
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name="parameter",
            name="opsi_pilihan",
            field=models.CharField(
                blank=True,
                help_text="Pisahkan pilihan dengan koma.",
                max_length=255,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name="parameter",
            name="foto_referensi",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="parameter_reference/",
            ),
        ),

        migrations.AlterField(
            model_name="parameter",
            name="tipe_input",
            field=models.CharField(
                choices=[
                    ("okng", "OK / NG"),
                    ("number", "Nilai Angka"),
                    ("text", "Teks"),
                    ("select", "Pilihan"),
                ],
                default="okng",
                max_length=20,
            ),
        ),

        migrations.AlterModelOptions(
            name="parameter",
            options={
                "ordering": ["barang", "urutan", "id"],
            },
        ),
    ]