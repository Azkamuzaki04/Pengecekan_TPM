from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [('inspection','0001_initial'), ('barang','0002_checksitemedia')]
    operations = [
        migrations.AddField(model_name='laporaninspeksi', name='approved_at', field=models.DateTimeField(blank=True, null=True)),
        migrations.AddField(model_name='laporaninspeksi', name='approved_by', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='approved_reports', to=settings.AUTH_USER_MODEL)),
        migrations.AddField(model_name='fotoinspeksi', name='hasil_inspeksi', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foto_ng', to='inspection.hasilinspeksi')),
        migrations.AlterField(model_name='hasilinspeksi', name='nilai_hasil', field=models.CharField(blank=True, max_length=100)),
        migrations.AlterField(model_name='hasilinspeksi', name='hasil', field=models.CharField(choices=[('PASS','OK'),('FAIL','NG'),('SKIP','Tidak Diisi')], max_length=10)),
        migrations.AlterField(model_name='fotoinspeksi', name='jenis_foto', field=models.CharField(choices=[('BARCODE','Barcode'),('BARANG','Barang'),('NG','Bukti NG')], max_length=20)),
    ]
