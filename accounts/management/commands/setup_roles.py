from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = "Membuat contoh akun role CHECKSIT tanpa menghapus user lama."
    def add_arguments(self, parser):
        parser.add_argument('--password', default='Checksit123!')
    def handle(self, *args, **opts):
        password=opts['password']
        samples=[('petugas','PETUGAS','Petugas Welding','Inspector'),('admin_checksit','ADMIN','Admin CHECKSIT','Administrator'),('server_checksit','SERVER','Server CHECKSIT','IT / Server')]
        for username, role, nama, jabatan in samples:
            user, created=User.objects.get_or_create(username=username)
            if created: user.set_password(password); user.save()
            profile,_=UserProfile.objects.get_or_create(user=user)
            profile.role=role; profile.nama=nama; profile.jabatan=jabatan; profile.save()
            if role=='ADMIN': user.is_staff=True; user.save(update_fields=['is_staff'])
            self.stdout.write(self.style.SUCCESS(f'{username}: {role}'))
