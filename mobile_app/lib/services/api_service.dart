import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  final String baseUrl;

  ApiService(this.baseUrl);

  // =========================================================
  // TOKEN
  // =========================================================

  Future<String?> token() async {
    final prefs = await SharedPreferences.getInstance();

    return prefs.getString('token');
  }

  Future<void> saveToken(String value) async {
    final prefs = await SharedPreferences.getInstance();

    await prefs.setString(
      'token',
      value,
    );
  }

  // =========================================================
  // LOGIN
  // =========================================================

  Future<bool> login(
    String username,
    String password,
  ) async {
    final response = await http.post(
      Uri.parse(
        '$baseUrl/api/auth/token/',
      ),
      body: {
        'username': username,
        'password': password,
      },
    ).timeout(
      const Duration(
        seconds: 10,
      ),
    );

    if (response.statusCode != 200) {
      return false;
    }

    final data = jsonDecode(response.body);

    if (data['token'] == null) {
      return false;
    }

    await saveToken(
      data['token'].toString(),
    );

    return true;
  }

  // =========================================================
  // BARANG BY BARCODE
  // =========================================================

  Future<Map<String, dynamic>> barang(
    String barcode,
  ) async {
    final response = await http.get(
      Uri.parse(
        '$baseUrl/api/barang/$barcode/',
      ),
      headers: {
        'Authorization': 'Token ${await token()}',
      },
    );

    final body = _decodeResponse(response);

    if (response.statusCode != 200) {
      throw Exception(
        body['detail'] ?? 'Barang tidak ditemukan.',
      );
    }

    return body;
  }

  // =========================================================
  // SUBMIT INSPECTION
  // =========================================================

  Future<Map<String, dynamic>> submit(
    String barcode,
    Map<String, String> fields,
    Map<String, File> photos,
  ) async {
    final request = http.MultipartRequest(
      'POST',
      Uri.parse(
        '$baseUrl/api/inspections/',
      ),
    );

    request.headers['Authorization'] = 'Token ${await token()}';

    request.fields['barcode'] = barcode;

    request.fields.addAll(
      fields,
    );

    // -------------------------------------------------------
    // FOTO NG
    // -------------------------------------------------------

    for (final entry in photos.entries) {
      request.files.add(
        await http.MultipartFile.fromPath(
          entry.key,
          entry.value.path,
        ),
      );
    }

    final streamedResponse = await request.send();

    final response = await http.Response.fromStream(
      streamedResponse,
    );

    final body = _decodeResponse(response);

    if (response.statusCode >= 300) {
      throw Exception(
        body['detail'] ?? 'Gagal mengirim inspeksi.',
      );
    }

    return body;
  }

  // =========================================================
  // HISTORY
  // =========================================================

  Future<List<Map<String, dynamic>>> getHistory() async {
    final response = await http.get(
      Uri.parse(
        '$baseUrl/api/inspections/history/',
      ),
      headers: {
        'Authorization': 'Token ${await token()}',
      },
    );

    final body = _decodeResponse(response);

    if (response.statusCode != 200) {
      throw Exception(
        body['detail'] ?? 'Gagal mengambil history.',
      );
    }

    final List data = body['results'] is List ? body['results'] : body;

    return data
        .map(
          (item) => Map<String, dynamic>.from(
            item,
          ),
        )
        .toList();
  }

  // =========================================================
  // RESPONSE DECODER
  // =========================================================

  Map<String, dynamic> _decodeResponse(
    http.Response response,
  ) {
    try {
      final decoded = jsonDecode(response.body);

      if (decoded is Map<String, dynamic>) {
        return decoded;
      }

      return {
        'data': decoded,
      };
    } catch (_) {
      return {
        'detail': response.body.isEmpty
            ? 'Server memberikan response kosong.'
            : response.body,
      };
    }
  }
}
