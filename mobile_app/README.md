# CHECKSIT Welding HMMI - Mobile Petugas

Folder ini adalah source Flutter untuk APK petugas. Alur: Login → Scan Barcode → Summary Barang → OK/NG → Foto wajib bila NG → Submit ke Django.

## Sebelum menjalankan
1. Jalankan Django di komputer/server.
2. Ubah `ApiService('http://10.0.2.2:8000')` di `lib/main.dart` sesuai IP server. `10.0.2.2` hanya untuk Android Emulator.
3. Jalankan `flutter pub get` lalu `flutter run`.
4. Untuk APK: `flutter build apk --release`.

## Permission kamera
Tambahkan permission kamera Android pada `android/app/src/main/AndroidManifest.xml` jika belum otomatis oleh plugin.
