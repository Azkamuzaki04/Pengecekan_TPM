import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:mobile_scanner/mobile_scanner.dart';

import 'services/api_service.dart';

// =========================================================
// COLOR
// =========================================================

const Color hinoBlue = Color(0xFF0066B3);
const Color hinoDarkBlue = Color(0xFF004C8C);
const Color hinoRed = Color(0xFFC8102E);
const Color pageBackground = Color(0xFFF5F7FA);
const Color textDark = Color(0xFF202124);

// =========================================================
// MAIN
// =========================================================

void main() {
  runApp(const ChecksitApp());
}

class ChecksitApp extends StatelessWidget {
  const ChecksitApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'CHECKSHEET WELDING HMMI',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: hinoBlue,
          primary: hinoBlue,
        ),
        scaffoldBackgroundColor: pageBackground,
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.white,
          foregroundColor: textDark,
          elevation: 0,
          centerTitle: false,
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.white,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(14),
            borderSide: BorderSide(
              color: Colors.grey.shade300,
            ),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(14),
            borderSide: BorderSide(
              color: Colors.grey.shade300,
            ),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(14),
            borderSide: const BorderSide(
              color: hinoBlue,
              width: 1.5,
            ),
          ),
        ),
        filledButtonTheme: FilledButtonThemeData(
          style: FilledButton.styleFrom(
            backgroundColor: hinoBlue,
            foregroundColor: Colors.white,
            minimumSize: const Size.fromHeight(52),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(14),
            ),
          ),
        ),
      ),
      home: const LoginPage(),
    );
  }
}

// =========================================================
// LOGIN PAGE
// =========================================================

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController usernameController = TextEditingController();

  final TextEditingController passwordController = TextEditingController();

  bool loading = false;
  bool hidePassword = true;

  // =======================================================
  // API
  // =======================================================

  final ApiService api = ApiService(
    'http://10.162.65.131:8000',
  );

  // =======================================================
  // LOGIN
  // =======================================================

  Future<void> login() async {
    final username = usernameController.text.trim();
    final password = passwordController.text;

    if (username.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'Username dan password wajib diisi.',
          ),
        ),
      );

      return;
    }

    setState(() {
      loading = true;
    });

    try {
      final success = await api.login(
        username,
        password,
      );

      if (!mounted) {
        return;
      }

      if (success) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (_) => HomePage(
              api: api,
            ),
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text(
              'Login gagal. Periksa username dan password.',
            ),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Tidak dapat terhubung ke server.\n$e',
            ),
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          loading = false;
        });
      }
    }
  }

  @override
  void dispose() {
    usernameController.dispose();
    passwordController.dispose();

    super.dispose();
  }

  // =======================================================
  // BUILD
  // =======================================================

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(
            horizontal: 24,
            vertical: 35,
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 30),

              // ------------------------------------------------
              // HINO LOGO
              // ------------------------------------------------

              Center(
                child: Image.asset(
                  'assets/images/hino_logo.jpg',
                  height: 100,
                  fit: BoxFit.contain,
                  errorBuilder: (_, __, ___) {
                    return const Icon(
                      Icons.business,
                      color: hinoBlue,
                      size: 75,
                    );
                  },
                ),
              ),

              const SizedBox(height: 25),

              const Text(
                'CHECKSHEET WELDING',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 26,
                  fontWeight: FontWeight.w800,
                  color: textDark,
                ),
              ),

              const SizedBox(height: 6),

              const Text(
                'HMMI • Welding Inspection',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.grey,
                ),
              ),

              const SizedBox(height: 45),

              // ------------------------------------------------
              // USERNAME
              // ------------------------------------------------

              TextField(
                controller: usernameController,
                textInputAction: TextInputAction.next,
                decoration: const InputDecoration(
                  hintText: 'Username',
                  prefixIcon: Icon(
                    Icons.person_outline,
                  ),
                ),
              ),

              const SizedBox(height: 15),

              // ------------------------------------------------
              // PASSWORD
              // ------------------------------------------------

              TextField(
                controller: passwordController,
                obscureText: hidePassword,
                onSubmitted: (_) {
                  if (!loading) {
                    login();
                  }
                },
                decoration: InputDecoration(
                  hintText: 'Password',
                  prefixIcon: const Icon(
                    Icons.lock_outline,
                  ),
                  suffixIcon: IconButton(
                    onPressed: () {
                      setState(() {
                        hidePassword = !hidePassword;
                      });
                    },
                    icon: Icon(
                      hidePassword
                          ? Icons.visibility_off_outlined
                          : Icons.visibility_outlined,
                    ),
                  ),
                ),
              ),

              const SizedBox(height: 25),

              // ------------------------------------------------
              // LOGIN BUTTON
              // ------------------------------------------------

              SizedBox(
                height: 54,
                child: FilledButton(
                  onPressed: loading ? null : login,
                  child: loading
                      ? const SizedBox(
                          width: 22,
                          height: 22,
                          child: CircularProgressIndicator(
                            strokeWidth: 2.5,
                            color: Colors.white,
                          ),
                        )
                      : const Text(
                          'Masuk',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                ),
              ),

              const SizedBox(height: 25),

              const Text(
                'Gunakan akun yang telah terdaftar untuk melakukan pemeriksaan.',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// =========================================================
// HOME / DASHBOARD
// =========================================================

class HomePage extends StatelessWidget {
  final ApiService api;

  const HomePage({
    super.key,
    required this.api,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: pageBackground,
      appBar: AppBar(
        backgroundColor: hinoBlue,
        foregroundColor: Colors.white,
        title: const Text(
          'CHECKSHEET WELDING',
          style: TextStyle(
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // ------------------------------------------------
              // HEADER CARD
              // ------------------------------------------------

              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withValues(alpha: 0.05),
                      blurRadius: 12,
                      offset: const Offset(0, 5),
                    ),
                  ],
                ),
                child: Row(
                  children: [
                    Container(
                      width: 58,
                      height: 58,
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(14),
                        border: Border.all(
                          color: Colors.grey.shade200,
                        ),
                      ),
                      child: Image.asset(
                        'assets/images/hino_logo.jpg',
                        fit: BoxFit.contain,
                        errorBuilder: (_, __, ___) {
                          return const Icon(
                            Icons.business,
                            color: hinoBlue,
                          );
                        },
                      ),
                    ),
                    const SizedBox(width: 15),
                    const Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Hello Weldpart 👋',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          SizedBox(height: 5),
                          Text(
                            'Siap melakukan pemeriksaan welding hari ini?',
                            style: TextStyle(
                              fontSize: 13,
                              color: Colors.grey,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 25),

              const Text(
                'Menu Utama',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(height: 12),

              // =================================================
              // INSPECTION
              // =================================================

              _MenuCard(
                icon: Icons.fact_check_outlined,
                title: 'INSPECTION',
                subtitle: 'Mulai pemeriksaan welding',
                color: hinoBlue,
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => InspectionMenuPage(
                        api: api,
                      ),
                    ),
                  );
                },
              ),

              const SizedBox(height: 15),

              // =================================================
              // HISTORY
              // =================================================

              _MenuCard(
                icon: Icons.history,
                title: 'HISTORY',
                subtitle: 'Lihat riwayat pemeriksaan',
                color: Colors.green,
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => HistoryPage(
                        api: api,
                      ),
                    ),
                  );
                },
              ),

              const SizedBox(height: 30),

              // ------------------------------------------------
              // INFO
              // ------------------------------------------------

              Container(
                padding: const EdgeInsets.all(15),
                decoration: BoxDecoration(
                  color: hinoBlue.withValues(alpha: 0.06),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(
                    color: hinoBlue.withValues(alpha: 0.12),
                  ),
                ),
                child: const Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Icon(
                      Icons.info_outline,
                      color: hinoBlue,
                    ),
                    SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        'Mulai pemeriksaan dengan scan barcode atau input barcode secara manual. Pastikan setiap item checksheet diperiksa sesuai standar.',
                        style: TextStyle(
                          fontSize: 12.5,
                          color: Colors.black87,
                          height: 1.4,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// =========================================================
// MENU CARD
// =========================================================

class _MenuCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final Color color;
  final VoidCallback onTap;

  const _MenuCard({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(18),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(18),
        child: Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(18),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.05),
                blurRadius: 10,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: Row(
            children: [
              Container(
                width: 58,
                height: 58,
                decoration: BoxDecoration(
                  color: color.withValues(alpha: 0.10),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Icon(
                  icon,
                  color: color,
                  size: 30,
                ),
              ),
              const SizedBox(width: 17),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.bold,
                        color: color,
                      ),
                    ),
                    const SizedBox(height: 5),
                    Text(
                      subtitle,
                      style: const TextStyle(
                        fontSize: 13,
                        color: Colors.grey,
                      ),
                    ),
                  ],
                ),
              ),
              Icon(
                Icons.arrow_forward_ios,
                size: 16,
                color: Colors.grey.shade400,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// =========================================================
// INSPECTION MENU
// =========================================================

class InspectionMenuPage extends StatelessWidget {
  final ApiService api;

  const InspectionMenuPage({
    super.key,
    required this.api,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: pageBackground,
      appBar: AppBar(
        backgroundColor: hinoBlue,
        foregroundColor: Colors.white,
        title: const Text(
          'Inspection',
          style: TextStyle(
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Pilih metode pemeriksaan',
              style: TextStyle(
                fontSize: 23,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 7),

            const Text(
              'Pilih salah satu metode untuk menemukan barang yang akan diperiksa.',
              style: TextStyle(
                fontSize: 13,
                color: Colors.grey,
                height: 1.4,
              ),
            ),

            const SizedBox(height: 25),

            // ------------------------------------------------
            // SCAN
            // ------------------------------------------------

            _InspectionMethodCard(
              icon: Icons.qr_code_scanner,
              title: 'SCAN BARCODE',
              subtitle: 'Gunakan kamera untuk membaca barcode barang',
              color: hinoBlue,
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => ScannerPage(
                      api: api,
                    ),
                  ),
                );
              },
            ),

            const SizedBox(height: 15),

            // ------------------------------------------------
            // MANUAL
            // ------------------------------------------------

            _InspectionMethodCard(
              icon: Icons.keyboard_alt_outlined,
              title: 'INPUT MANUAL',
              subtitle: 'Masukkan kode barcode secara manual',
              color: hinoBlue,
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => ManualPage(
                      api: api,
                    ),
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}

// =========================================================
// INSPECTION METHOD CARD
// =========================================================

class _InspectionMethodCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final Color color;
  final VoidCallback onTap;

  const _InspectionMethodCard({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(18),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(18),
        child: Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(18),
            border: Border.all(
              color: Colors.grey.shade200,
            ),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.04),
                blurRadius: 10,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: Row(
            children: [
              Container(
                width: 60,
                height: 60,
                decoration: BoxDecoration(
                  color: color.withValues(alpha: 0.10),
                  borderRadius: BorderRadius.circular(15),
                ),
                child: Icon(
                  icon,
                  color: color,
                  size: 31,
                ),
              ),
              const SizedBox(width: 17),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: TextStyle(
                        color: color,
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 5),
                    Text(
                      subtitle,
                      style: const TextStyle(
                        color: Colors.grey,
                        fontSize: 13,
                        height: 1.3,
                      ),
                    ),
                  ],
                ),
              ),
              Icon(
                Icons.arrow_forward_ios,
                size: 16,
                color: Colors.grey.shade400,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// =========================================================
// HISTORY PAGE
// =========================================================

class HistoryPage extends StatefulWidget {
  final ApiService api;

  const HistoryPage({
    super.key,
    required this.api,
  });

  @override
  State<HistoryPage> createState() => _HistoryPageState();
}

class _HistoryPageState extends State<HistoryPage> {
  bool loading = true;

  String? error;

  List<Map<String, dynamic>> history = [];

  @override
  void initState() {
    super.initState();

    loadHistory();
  }

  // =======================================================
  // LOAD HISTORY
  // =======================================================

  Future<void> loadHistory() async {
    setState(() {
      loading = true;
      error = null;
    });

    try {
      final result = await widget.api.getHistory();

      if (!mounted) {
        return;
      }

      setState(() {
        history = result;
        loading = false;
      });
    } catch (e) {
      if (!mounted) {
        return;
      }

      setState(() {
        loading = false;
        error = e.toString();
      });
    }
  }

  // =======================================================
  // APPROVAL COLOR
  // =======================================================

  Color approvalColor(String? status) {
    switch (status) {
      case 'APPROVED':
        return Colors.green;

      case 'REJECTED':
        return hinoRed;

      case 'PENDING':
        return Colors.orange;

      default:
        return Colors.grey;
    }
  }

  String approvalText(String? status) {
    switch (status) {
      case 'APPROVED':
        return 'Approved';

      case 'REJECTED':
        return 'Rejected';

      case 'PENDING':
        return 'Pending';

      default:
        return status ?? '-';
    }
  }

  // =======================================================
  // BUILD
  // =======================================================

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: pageBackground,
      appBar: AppBar(
        backgroundColor: hinoBlue,
        foregroundColor: Colors.white,
        title: const Text(
          'History',
          style: TextStyle(
            fontWeight: FontWeight.bold,
          ),
        ),
        actions: [
          IconButton(
            onPressed: loading ? null : loadHistory,
            icon: const Icon(
              Icons.refresh,
            ),
          ),
        ],
      ),
      body: loading
          ? const Center(
              child: CircularProgressIndicator(
                color: hinoBlue,
              ),
            )
          : error != null
              ? _HistoryError(
                  message: error!,
                  onRetry: loadHistory,
                )
              : history.isEmpty
                  ? const _EmptyHistory()
                  : RefreshIndicator(
                      color: hinoBlue,
                      onRefresh: loadHistory,
                      child: ListView.builder(
                        padding: const EdgeInsets.all(16),
                        itemCount: history.length,
                        itemBuilder: (context, index) {
                          final item = history[index];

                          return _HistoryCard(
                            item: item,
                            approvalColor: approvalColor(
                              item['status_approval'],
                            ),
                            approvalText: approvalText(
                              item['status_approval'],
                            ),
                          );
                        },
                      ),
                    ),
    );
  }
}

// =========================================================
// HISTORY CARD
// =========================================================

class _HistoryCard extends StatelessWidget {
  final Map<String, dynamic> item;
  final Color approvalColor;
  final String approvalText;

  const _HistoryCard({
    required this.item,
    required this.approvalColor,
    required this.approvalText,
  });

  @override
  Widget build(BuildContext context) {
    final bool isNG = item['status_hasil'] == 'NG';

    return Card(
      color: Colors.white,
      elevation: 1,
      margin: const EdgeInsets.only(
        bottom: 12,
      ),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // ------------------------------------------------
            // HEADER
            // ------------------------------------------------

            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    color: isNG
                        ? hinoRed.withValues(alpha: 0.10)
                        : Colors.green.withValues(alpha: 0.10),
                    borderRadius: BorderRadius.circular(13),
                  ),
                  child: Icon(
                    isNG
                        ? Icons.warning_amber_rounded
                        : Icons.check_circle_outline,
                    color: isNG ? hinoRed : Colors.green,
                  ),
                ),
                const SizedBox(width: 13),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        item['nama_barang'] ?? 'Barang',
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        item['nomor_laporan'] ?? '-',
                        style: const TextStyle(
                          fontSize: 12,
                          color: Colors.grey,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),

            const SizedBox(height: 15),

            // ------------------------------------------------
            // DATA
            // ------------------------------------------------

            _HistoryInfoRow(
              icon: Icons.qr_code,
              label: 'Barcode',
              value: item['barcode'] ?? '-',
            ),

            const SizedBox(height: 7),

            _HistoryInfoRow(
              icon: Icons.calendar_today_outlined,
              label: 'Tanggal',
              value: item['tanggal_inspeksi'] ?? '-',
            ),

            const SizedBox(height: 7),

            _HistoryInfoRow(
              icon: Icons.person_outline,
              label: 'Petugas',
              value: item['petugas'] ?? '-',
            ),

            const SizedBox(height: 14),

            // ------------------------------------------------
            // STATUS
            // ------------------------------------------------

            Row(
              children: [
                Expanded(
                  child: _StatusBadge(
                    label: 'Hasil: ${item['status_hasil'] ?? '-'}',
                    color: isNG ? hinoRed : Colors.green,
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: _StatusBadge(
                    label: approvalText,
                    color: approvalColor,
                  ),
                ),
              ],
            ),

            // ------------------------------------------------
            // DETAIL HASIL
            // ------------------------------------------------

            if (item['hasil'] is List &&
                (item['hasil'] as List).isNotEmpty) ...[
              const SizedBox(height: 15),
              const Divider(),
              const SizedBox(height: 8),
              const Text(
                'Detail Pemeriksaan',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              ...(item['hasil'] as List).map(
                (hasil) => _ResultRow(
                  hasil: Map<String, dynamic>.from(
                    hasil,
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

// =========================================================
// HISTORY INFO ROW
// =========================================================

class _HistoryInfoRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const _HistoryInfoRow({
    required this.icon,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(
          icon,
          size: 17,
          color: Colors.grey.shade600,
        ),
        const SizedBox(width: 8),
        SizedBox(
          width: 75,
          child: Text(
            label,
            style: const TextStyle(
              fontSize: 12,
              color: Colors.grey,
            ),
          ),
        ),
        const Text(
          ':',
          style: TextStyle(
            color: Colors.grey,
          ),
        ),
        const SizedBox(width: 7),
        Expanded(
          child: Text(
            value,
            style: const TextStyle(
              fontSize: 12.5,
              fontWeight: FontWeight.w500,
            ),
          ),
        ),
      ],
    );
  }
}

// =========================================================
// RESULT ROW
// =========================================================

class _ResultRow extends StatelessWidget {
  final Map<String, dynamic> hasil;

  const _ResultRow({
    required this.hasil,
  });

  @override
  Widget build(BuildContext context) {
    final bool pass = hasil['hasil'] == 'PASS';

    return Container(
      margin: const EdgeInsets.only(
        bottom: 7,
      ),
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: Colors.grey.shade50,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        children: [
          Icon(
            pass ? Icons.check_circle : Icons.cancel,
            size: 18,
            color: pass ? Colors.green : hinoRed,
          ),
          const SizedBox(width: 9),
          Expanded(
            child: Text(
              hasil['parameter'] ?? '-',
              style: const TextStyle(
                fontSize: 12.5,
              ),
            ),
          ),
          Text(
            hasil['hasil'] == 'PASS'
                ? 'OK'
                : hasil['hasil'] == 'FAIL'
                    ? 'NG'
                    : 'SKIP',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 12,
              color: pass ? Colors.green : hinoRed,
            ),
          ),
        ],
      ),
    );
  }
}

// =========================================================
// STATUS BADGE
// =========================================================

class _StatusBadge extends StatelessWidget {
  final String label;
  final Color color;

  const _StatusBadge({
    required this.label,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(
        vertical: 9,
        horizontal: 10,
      ),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(
          color: color.withValues(alpha: 0.20),
        ),
      ),
      child: Text(
        label,
        textAlign: TextAlign.center,
        style: TextStyle(
          color: color,
          fontWeight: FontWeight.bold,
          fontSize: 11.5,
        ),
      ),
    );
  }
}

// =========================================================
// EMPTY HISTORY
// =========================================================

class _EmptyHistory extends StatelessWidget {
  const _EmptyHistory();

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(30),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 90,
              height: 90,
              decoration: BoxDecoration(
                color: hinoBlue.withValues(alpha: 0.08),
                shape: BoxShape.circle,
              ),
              child: const Icon(
                Icons.history,
                size: 45,
                color: hinoBlue,
              ),
            ),
            const SizedBox(height: 18),
            const Text(
              'Belum Ada History',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 7),
            const Text(
              'Riwayat pemeriksaan yang sudah dikirim akan tampil di halaman ini.',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 13,
                color: Colors.grey,
                height: 1.4,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// =========================================================
// HISTORY ERROR
// =========================================================

class _HistoryError extends StatelessWidget {
  final String message;
  final VoidCallback onRetry;

  const _HistoryError({
    required this.message,
    required this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(25),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.cloud_off_outlined,
              size: 65,
              color: hinoRed,
            ),
            const SizedBox(height: 15),
            const Text(
              'Gagal Memuat History',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              message,
              textAlign: TextAlign.center,
              style: const TextStyle(
                color: Colors.grey,
                fontSize: 12,
              ),
            ),
            const SizedBox(height: 18),
            FilledButton.icon(
              onPressed: onRetry,
              icon: const Icon(
                Icons.refresh,
              ),
              label: const Text(
                'Coba Lagi',
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// =========================================================
// SCANNER PAGE
// =========================================================

class ScannerPage extends StatefulWidget {
  final ApiService api;

  const ScannerPage({
    super.key,
    required this.api,
  });

  @override
  State<ScannerPage> createState() => _ScannerPageState();
}

class _ScannerPageState extends State<ScannerPage> {
  bool scanned = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: hinoBlue,
        foregroundColor: Colors.white,
        title: const Text('Scan Barcode'),
      ),
      body: Stack(
        children: [
          Positioned.fill(
            child: MobileScanner(
              onDetect: (capture) {
                if (scanned || !mounted) return;

                final barcode = capture.barcodes.isNotEmpty
                    ? capture.barcodes.first.rawValue
                    : null;

                if (barcode == null || barcode.trim().isEmpty) {
                  return;
                }

                setState(() {
                  scanned = true;
                });

                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(
                    builder: (_) => SummaryPage(
                      api: widget.api,
                      barcode: barcode.trim(),
                    ),
                  ),
                );
              },
            ),
          ),
          Center(
            child: Container(
              width: 280,
              height: 170,
              decoration: BoxDecoration(
                border: Border.all(
                  color: Colors.white,
                  width: 2.5,
                ),
                borderRadius: BorderRadius.circular(18),
              ),
            ),
          ),
          Positioned(
            bottom: 50,
            left: 25,
            right: 25,
            child: Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.65),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Text(
                'Arahkan kamera ke barcode barang.',
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 14,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// =========================================================
// MANUAL PAGE
// =========================================================

class ManualPage extends StatefulWidget {
  final ApiService api;

  const ManualPage({
    super.key,
    required this.api,
  });

  @override
  State<ManualPage> createState() => _ManualPageState();
}

class _ManualPageState extends State<ManualPage> {
  final TextEditingController controller = TextEditingController();

  bool loading = false;

  Future<void> searchBarang() async {
    final barcode = controller.text.trim();

    if (barcode.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'Barcode wajib diisi.',
          ),
        ),
      );

      return;
    }

    setState(() {
      loading = true;
    });

    try {
      await widget.api.barang(
        barcode,
      );

      if (!mounted) {
        return;
      }

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => SummaryPage(
            api: widget.api,
            barcode: barcode,
          ),
        ),
      );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              e.toString(),
            ),
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          loading = false;
        });
      }
    }
  }

  @override
  void dispose() {
    controller.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: pageBackground,
      appBar: AppBar(
        backgroundColor: hinoBlue,
        foregroundColor: Colors.white,
        title: const Text(
          'Input Manual',
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(18),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withValues(alpha: 0.04),
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: Column(
                children: [
                  Container(
                    width: 65,
                    height: 65,
                    decoration: BoxDecoration(
                      color: hinoBlue.withValues(alpha: 0.08),
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: const Icon(
                      Icons.keyboard_alt_outlined,
                      color: hinoBlue,
                      size: 32,
                    ),
                  ),
                  const SizedBox(height: 15),
                  const Text(
                    'Input Barcode',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 7),
                  const Text(
                    'Masukkan kode barcode barang yang akan diperiksa.',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 13,
                      color: Colors.grey,
                    ),
                  ),
                  const SizedBox(height: 20),
                  TextField(
                    controller: controller,
                    textCapitalization: TextCapitalization.characters,
                    decoration: const InputDecoration(
                      hintText: 'Contoh: QRH-02',
                      prefixIcon: Icon(
                        Icons.qr_code,
                      ),
                    ),
                  ),
                  const SizedBox(height: 15),
                  SizedBox(
                    height: 52,
                    width: double.infinity,
                    child: FilledButton.icon(
                      onPressed: loading ? null : searchBarang,
                      icon: loading
                          ? const SizedBox(
                              width: 20,
                              height: 20,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                                color: Colors.white,
                              ),
                            )
                          : const Icon(
                              Icons.search,
                            ),
                      label: Text(
                        loading ? 'Mencari...' : 'Cari Barang',
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// =========================================================
// SUMMARY PAGE
// =========================================================

class SummaryPage extends StatefulWidget {
  final ApiService api;
  final String barcode;

  const SummaryPage({
    super.key,
    required this.api,
    required this.barcode,
  });

  @override
  State<SummaryPage> createState() => _SummaryPageState();
}

class _SummaryPageState extends State<SummaryPage> {
  Map<String, dynamic>? data;

  String? error;

  @override
  void initState() {
    super.initState();

    loadBarang();
  }

  Future<void> loadBarang() async {
    try {
      final result = await widget.api.barang(
        widget.barcode,
      );

      if (!mounted) {
        return;
      }

      setState(() {
        data = result;
      });
    } catch (e) {
      if (!mounted) {
        return;
      }

      setState(() {
        error = e.toString();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (error != null) {
      return Scaffold(
        appBar: AppBar(
          title: const Text(
            'Data Barang',
          ),
        ),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(25),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(
                  Icons.error_outline,
                  color: hinoRed,
                  size: 60,
                ),
                const SizedBox(height: 15),
                Text(
                  error!,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 15),
                FilledButton.icon(
                  onPressed: loadBarang,
                  icon: const Icon(
                    Icons.refresh,
                  ),
                  label: const Text(
                    'Coba Lagi',
                  ),
                ),
              ],
            ),
          ),
        ),
      );
    }

    if (data == null) {
      return const Scaffold(
        body: Center(
          child: CircularProgressIndicator(
            color: hinoBlue,
          ),
        ),
      );
    }

    final List items = data!['items'] ?? [];

    return Scaffold(
      backgroundColor: pageBackground,
      appBar: AppBar(
        backgroundColor: hinoBlue,
        foregroundColor: Colors.white,
        title: const Text(
          'Data Barang',
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // ------------------------------------------------
          // PRODUCT CARD
          // ------------------------------------------------

          Container(
            padding: const EdgeInsets.all(18),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(18),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withValues(alpha: 0.04),
                  blurRadius: 10,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      width: 45,
                      height: 45,
                      decoration: BoxDecoration(
                        color: hinoBlue.withValues(alpha: 0.10),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Icon(
                        Icons.inventory_2_outlined,
                        color: hinoBlue,
                      ),
                    ),
                    const SizedBox(width: 12),
                    const Text(
                      'DATA BARANG',
                      style: TextStyle(
                        color: hinoBlue,
                        fontWeight: FontWeight.bold,
                        fontSize: 14,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 18),
                Text(
                  data!['nama_barang'] ?? '-',
                  style: const TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 12),
                _DataRow(
                  label: 'Kode Barang',
                  value: data!['kode_barang'] ?? '-',
                ),
                _DataRow(
                  label: 'Barcode',
                  value: data!['barcode'] ?? widget.barcode,
                ),
                if (data!['model'] != null)
                  _DataRow(
                    label: 'Model',
                    value: data!['model'].toString(),
                  ),
                if (data!['deskripsi'] != null &&
                    data!['deskripsi'].toString().isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.only(
                      top: 10,
                    ),
                    child: Text(
                      data!['deskripsi'].toString(),
                      style: const TextStyle(
                        fontSize: 13,
                        color: Colors.grey,
                        height: 1.4,
                      ),
                    ),
                  ),
              ],
            ),
          ),

          const SizedBox(height: 15),

          // ------------------------------------------------
          // IMAGE
          // ------------------------------------------------

          if (data!['gambar'] != null)
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(18),
              ),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: Image.network(
                  data!['gambar'],
                  height: 210,
                  fit: BoxFit.contain,
                  errorBuilder: (_, __, ___) {
                    return Container(
                      height: 210,
                      color: Colors.grey.shade100,
                      child: const Center(
                        child: Icon(
                          Icons.image_not_supported_outlined,
                          size: 55,
                          color: Colors.grey,
                        ),
                      ),
                    );
                  },
                ),
              ),
            ),

          const SizedBox(height: 20),

          // ------------------------------------------------
          // INSPECTION ITEM
          // ------------------------------------------------

          const Text(
            'Item Pemeriksaan',
            style: TextStyle(
              fontSize: 19,
              fontWeight: FontWeight.bold,
            ),
          ),

          const SizedBox(height: 10),

          if (items.isEmpty)
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(15),
              ),
              child: const Text(
                'Barang belum memiliki item pemeriksaan.',
                textAlign: TextAlign.center,
              ),
            )
          else
            ...items.map(
              (item) => _SummaryItem(
                item: Map<String, dynamic>.from(
                  item,
                ),
              ),
            ),

          const SizedBox(height: 18),

          // ------------------------------------------------
          // START BUTTON
          // ------------------------------------------------

          SizedBox(
            height: 54,
            child: FilledButton.icon(
              onPressed: items.isEmpty
                  ? null
                  : () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => InspectionPage(
                            api: widget.api,
                            barcode: widget.barcode,
                            items: items,
                          ),
                        ),
                      );
                    },
              icon: const Icon(
                Icons.play_arrow,
              ),
              label: const Text(
                'Lanjut ke Checksheet',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),

          const SizedBox(height: 25),
        ],
      ),
    );
  }
}

// =========================================================
// DATA ROW
// =========================================================

class _DataRow extends StatelessWidget {
  final String label;
  final String value;

  const _DataRow({
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 7),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 105,
            child: Text(
              label,
              style: const TextStyle(
                color: Colors.grey,
                fontSize: 12,
              ),
            ),
          ),
          const Text(
            ': ',
            style: TextStyle(
              color: Colors.grey,
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// =========================================================
// SUMMARY ITEM
// =========================================================

class _SummaryItem extends StatelessWidget {
  final Map<String, dynamic> item;

  const _SummaryItem({
    required this.item,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(15),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(
          color: Colors.grey.shade200,
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 40,
            height: 40,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: hinoBlue.withValues(alpha: 0.10),
              borderRadius: BorderRadius.circular(11),
            ),
            child: Text(
              item['urutan']?.toString().padLeft(2, '0') ?? '00',
              style: const TextStyle(
                color: hinoBlue,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  item['nama'] ?? '-',
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 15,
                  ),
                ),
                const SizedBox(height: 5),
                Text(
                  item['instruksi'] ?? '',
                  style: const TextStyle(
                    fontSize: 12.5,
                    color: Colors.grey,
                    height: 1.3,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  'Standar: ${item['standar'] ?? '-'}',
                  style: const TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// =========================================================
// INSPECTION PAGE
// =========================================================

class InspectionPage extends StatefulWidget {
  final ApiService api;
  final String barcode;
  final List items;

  const InspectionPage({
    super.key,
    required this.api,
    required this.barcode,
    required this.items,
  });

  @override
  State<InspectionPage> createState() => _InspectionPageState();
}

class _InspectionPageState extends State<InspectionPage> {
  // item ID -> OK / NG
  final Map<int, String> values = {};

  // foto_ng_ID -> File
  final Map<String, File> photos = {};

  // item ID -> REPAIRED / NOT_REPAIRED
  final Map<int, String> repairStatus = {};

  final ImagePicker picker = ImagePicker();

  bool busy = false;

  // =======================================================
  // TAKE PHOTO
  // =======================================================

  Future<void> takePhoto(int id) async {
    try {
      final XFile? image = await picker.pickImage(
        source: ImageSource.camera,
        imageQuality: 80,
      );

      if (image == null) {
        return;
      }

      if (!mounted) {
        return;
      }

      setState(() {
        photos['foto_ng_$id'] = File(image.path);
      });
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Gagal mengambil foto: $e',
            ),
          ),
        );
      }
    }
  }

  // =======================================================
  // SET OK
  // =======================================================

  void setOK(int id) {
    setState(() {
      values[id] = 'OK';

      photos.remove(
        'foto_ng_$id',
      );

      repairStatus.remove(id);
    });
  }

  // =======================================================
  // SET NG
  // =======================================================

  void setNG(int id) {
    setState(() {
      values[id] = 'NG';

      repairStatus.remove(id);
    });
  }

  // =======================================================
  // VALIDATION
  // =======================================================

  bool validateInspection() {
    // ------------------------------------------------------
    // Semua item wajib diisi
    // ------------------------------------------------------

    for (final rawItem in widget.items) {
      final item = Map<String, dynamic>.from(
        rawItem,
      );

      final int id = item['id'] as int;

      if (!values.containsKey(id)) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Item "${item['nama']}" belum diperiksa.',
            ),
          ),
        );

        return false;
      }
    }

    // ------------------------------------------------------
    // NG wajib foto + repair status
    // ------------------------------------------------------

    for (final rawItem in widget.items) {
      final item = Map<String, dynamic>.from(
        rawItem,
      );

      final int id = item['id'] as int;

      if (values[id] == 'NG') {
        if (!photos.containsKey(
          'foto_ng_$id',
        )) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(
                'Foto NG wajib untuk "${item['nama']}".',
              ),
            ),
          );

          return false;
        }

        if (!repairStatus.containsKey(
              id,
            ) ||
            repairStatus[id]!.isEmpty) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(
                'Pilih status repair untuk "${item['nama']}".',
              ),
            ),
          );

          return false;
        }
      }
    }

    return true;
  }

  // =======================================================
  // SUBMIT
  // =======================================================

  Future<void> submit() async {
    if (!validateInspection()) {
      return;
    }

    setState(() {
      busy = true;
    });

    try {
      final Map<String, String> fields = {};

      // ----------------------------------------------------
      // HASIL
      // ----------------------------------------------------

      for (final rawItem in widget.items) {
        final item = Map<String, dynamic>.from(
          rawItem,
        );

        final int id = item['id'] as int;

        fields['parameter_$id'] = values[id]!;
      }

      // ----------------------------------------------------
      // REPAIR STATUS
      // ----------------------------------------------------

      for (final rawItem in widget.items) {
        final item = Map<String, dynamic>.from(
          rawItem,
        );

        final int id = item['id'] as int;

        if (values[id] == 'NG' && repairStatus.containsKey(id)) {
          fields['repair_status_$id'] = repairStatus[id]!;
        }
      }

      // ----------------------------------------------------
      // SEND
      // ----------------------------------------------------

      final result = await widget.api.submit(
        widget.barcode,
        fields,
        photos,
      );

      if (!mounted) {
        return;
      }

      // ----------------------------------------------------
      // SUCCESS DIALOG
      // ----------------------------------------------------

      await showDialog(
        context: context,
        barrierDismissible: false,
        builder: (_) {
          return AlertDialog(
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(18),
            ),
            title: const Row(
              children: [
                Icon(
                  Icons.check_circle,
                  color: Colors.green,
                ),
                SizedBox(width: 8),
                Text(
                  'Berhasil',
                ),
              ],
            ),
            content: Text(
              'Laporan: ${result['nomor_laporan'] ?? '-'}\n\n'
              'Hasil: ${result['status_hasil'] ?? '-'}\n'
              'Approval: ${result['status_approval'] ?? 'PENDING'}',
            ),
            actions: [
              FilledButton(
                onPressed: () {
                  Navigator.pop(
                    context,
                  );
                },
                child: const Text(
                  'Selesai',
                ),
              ),
            ],
          );
        },
      );

      if (!mounted) {
        return;
      }

      Navigator.popUntil(
        context,
        (route) => route.isFirst,
      );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Gagal mengirim inspeksi:\n$e',
            ),
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          busy = false;
        });
      }
    }
  }

  // =======================================================
  // ITEM CARD
  // =======================================================

  Widget buildInspectionItem(
    Map<String, dynamic> item,
  ) {
    final int id = item['id'] as int;

    final String? value = values[id];

    final bool isNG = value == 'NG';

    final bool hasPhoto = photos.containsKey(
      'foto_ng_$id',
    );

    final String? repair = repairStatus[id];

    return Container(
      margin: const EdgeInsets.only(bottom: 15),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(17),
        border: Border.all(
          color: value == 'OK'
              ? Colors.green.withValues(alpha: 0.25)
              : value == 'NG'
                  ? hinoRed.withValues(alpha: 0.25)
                  : Colors.grey.shade200,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.03),
            blurRadius: 8,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // ------------------------------------------------
          // ITEM HEADER
          // ------------------------------------------------

          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                width: 42,
                height: 42,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  color: hinoBlue.withValues(alpha: 0.10),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  item['urutan']?.toString().padLeft(2, '0') ?? '00',
                  style: const TextStyle(
                    color: hinoBlue,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  item['nama'] ?? '-',
                  style: const TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),

          const SizedBox(height: 14),

          // ------------------------------------------------
          // INSTRUKSI
          // ------------------------------------------------

          if (item['instruksi'] != null &&
              item['instruksi'].toString().isNotEmpty)
            Text(
              item['instruksi'].toString(),
              style: const TextStyle(
                fontSize: 13,
                height: 1.4,
              ),
            ),

          const SizedBox(height: 9),

          // ------------------------------------------------
          // STANDARD
          // ------------------------------------------------

          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(11),
            decoration: BoxDecoration(
              color: Colors.grey.shade50,
              borderRadius: BorderRadius.circular(10),
            ),
            child: Text(
              'Standar: ${item['standar'] ?? '-'}',
              style: const TextStyle(
                fontSize: 12,
                color: Colors.black87,
              ),
            ),
          ),

          const SizedBox(height: 14),

          // ------------------------------------------------
          // OK / NG
          // ------------------------------------------------

          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: busy
                      ? null
                      : () {
                          setOK(id);
                        },
                  icon: Icon(
                    Icons.check_circle_outline,
                    color: value == 'OK' ? Colors.green : Colors.grey,
                  ),
                  label: Text(
                    value == 'OK' ? '✓ OK' : 'OK',
                  ),
                  style: OutlinedButton.styleFrom(
                    foregroundColor:
                        value == 'OK' ? Colors.green : Colors.black87,
                    side: BorderSide(
                      color:
                          value == 'OK' ? Colors.green : Colors.grey.shade300,
                    ),
                    minimumSize: const Size.fromHeight(
                      48,
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(
                        11,
                      ),
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: busy
                      ? null
                      : () {
                          setNG(id);
                        },
                  icon: Icon(
                    Icons.cancel_outlined,
                    color: value == 'NG' ? hinoRed : Colors.grey,
                  ),
                  label: Text(
                    value == 'NG' ? '✕ NG' : 'NG',
                  ),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: value == 'NG' ? hinoRed : Colors.black87,
                    side: BorderSide(
                      color: value == 'NG' ? hinoRed : Colors.grey.shade300,
                    ),
                    minimumSize: const Size.fromHeight(
                      48,
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(
                        11,
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),

          // ------------------------------------------------
          // NG SECTION
          // ------------------------------------------------

          if (isNG) ...[
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: hinoRed.withValues(alpha: 0.045),
                borderRadius: BorderRadius.circular(13),
                border: Border.all(
                  color: hinoRed.withValues(alpha: 0.20),
                ),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Row(
                    children: [
                      Icon(
                        Icons.warning_amber_rounded,
                        color: hinoRed,
                        size: 21,
                      ),
                      SizedBox(width: 7),
                      Text(
                        'HASIL NG',
                        style: TextStyle(
                          color: hinoRed,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 13),

                  const Text(
                    'Foto Bukti NG',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 13,
                    ),
                  ),

                  const SizedBox(height: 7),

                  SizedBox(
                    width: double.infinity,
                    child: OutlinedButton.icon(
                      onPressed: busy
                          ? null
                          : () {
                              takePhoto(id);
                            },
                      icon: const Icon(
                        Icons.camera_alt_outlined,
                      ),
                      label: Text(
                        hasPhoto ? 'Foto NG ✓' : 'Ambil Foto NG *',
                      ),
                      style: OutlinedButton.styleFrom(
                        minimumSize: const Size.fromHeight(
                          48,
                        ),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(
                            11,
                          ),
                        ),
                      ),
                    ),
                  ),

                  // ------------------------------------------------
                  // PHOTO PREVIEW
                  // ------------------------------------------------

                  if (hasPhoto) ...[
                    const SizedBox(height: 10),
                    ClipRRect(
                      borderRadius: BorderRadius.circular(
                        10,
                      ),
                      child: Image.file(
                        photos['foto_ng_$id']!,
                        width: double.infinity,
                        height: 190,
                        fit: BoxFit.cover,
                      ),
                    ),
                  ],

                  const SizedBox(height: 16),

                  // ------------------------------------------------
                  // REPAIR
                  // ------------------------------------------------

                  const Text(
                    'Status Perbaikan',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 13,
                    ),
                  ),

                  const SizedBox(height: 4),

                  const Text(
                    'Pilih kondisi setelah ditemukan NG.',
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey,
                    ),
                  ),

                  const SizedBox(height: 5),

                  RadioListTile<String>(
                    contentPadding: EdgeInsets.zero,
                    dense: true,
                    title: const Text(
                      'Sudah Repair',
                    ),
                    subtitle: const Text(
                      'Kerusakan sudah diperbaiki',
                    ),
                    value: 'REPAIRED',
                    groupValue: repair,
                    onChanged: busy
                        ? null
                        : (selected) {
                            if (selected == null) {
                              return;
                            }

                            setState(() {
                              repairStatus[id] = selected;
                            });
                          },
                  ),

                  RadioListTile<String>(
                    contentPadding: EdgeInsets.zero,
                    dense: true,
                    title: const Text(
                      'Belum Repair',
                    ),
                    subtitle: const Text(
                      'Kerusakan belum diperbaiki',
                    ),
                    value: 'NOT_REPAIRED',
                    groupValue: repair,
                    onChanged: busy
                        ? null
                        : (selected) {
                            if (selected == null) {
                              return;
                            }

                            setState(() {
                              repairStatus[id] = selected;
                            });
                          },
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  // =======================================================
  // BUILD
  // =======================================================

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: pageBackground,
      appBar: AppBar(
        backgroundColor: hinoBlue,
        foregroundColor: Colors.white,
        title: const Text(
          'Checksheet',
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(
                color: Colors.grey.shade200,
              ),
            ),
            child: const Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Pemeriksaan Kondisi Barang',
                  style: TextStyle(
                    fontSize: 19,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                SizedBox(height: 6),
                Text(
                  'Pilih OK jika kondisi sesuai standar. Jika NG, foto bukti dan status perbaikan wajib diisi.',
                  style: TextStyle(
                    color: Colors.grey,
                    fontSize: 12.5,
                    height: 1.4,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 15),
          ...widget.items.map(
            (item) => buildInspectionItem(
              Map<String, dynamic>.from(
                item,
              ),
            ),
          ),
          const SizedBox(height: 5),
          SizedBox(
            height: 54,
            child: FilledButton.icon(
              onPressed: busy ? null : submit,
              icon: const Icon(
                Icons.send,
              ),
              label: Text(
                busy ? 'Mengirim...' : 'Kirim Hasil Inspeksi',
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
          const SizedBox(height: 25),
        ],
      ),
    );
  }
}
