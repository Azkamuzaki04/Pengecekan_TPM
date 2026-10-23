from django.db import migrations, models
import django.db.models.deletion

def create_profiles(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    Profile = apps.get_model("accounts", "Profile")

    for user in User.objects.all():

        # Ambil nama jika field tersedia.
        nama = ""

        if hasattr(user, "nama"):
            nama = user.nama or ""

        # Jika nama kosong, gunakan username.
        if not nama and hasattr(user, "username"):
            nama = user.username or ""

        # Tentukan role awal.
        role = "USER"

        if getattr(user, "is_superuser", False):
            role = "ADMIN"

        elif getattr(user, "is_staff", False):
            role = "ADMIN"

        Profile.objects.get_or_create(
            user_id=user.id,
            defaults={
                "role": role,
                "nama": nama,
            }
        )

class Migration(migrations.Migration):
    dependencies = [("accounts", "0001_initial")]
    operations = [migrations.CreateModel(name="UserProfile", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("role", models.CharField(choices=[("PETUGAS", "Petugas / User"), ("ADMIN", "Admin"), ("SERVER", "Server / Monitoring")], default="PETUGAS", max_length=20)),
        ("nama", models.CharField(blank=True, max_length=150)),
        ("jabatan", models.CharField(blank=True, max_length=100)),
        ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to="auth.user")),
    ]), migrations.RunPython(create_profiles, migrations.RunPython.noop)]
