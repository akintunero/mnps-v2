import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';

class User {
  final int id;
  final String username;
  final String email;
  final String role;
  final String fullName;

  User({
    required this.id,
    required this.username,
    required this.email,
    required this.role,
    required this.fullName,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      username: json['username'],
      email: json['email'],
      role: json['role'],
      fullName: json['full_name'],
    );
  }
}

class StudentResult {
  final int id;
  final String studentId;
  final String studentName;
  final String className;
  final String session;
  final String term;
  final String subjects;
  final double totalScore;
  final double averageScore;
  final String grade;
  final String? position;
  final String? remarks;

  StudentResult({
    required this.id,
    required this.studentId,
    required this.studentName,
    required this.className,
    required this.session,
    required this.term,
    required this.subjects,
    required this.totalScore,
    required this.averageScore,
    required this.grade,
    this.position,
    this.remarks,
  });

  factory StudentResult.fromJson(Map<String, dynamic> json) {
    return StudentResult(
      id: json['id'],
      studentId: json['student_id'],
      studentName: json['student_name'],
      className: json['class_name'],
      session: json['session'],
      term: json['term'],
      subjects: json['subjects'],
      totalScore: json['total_score'].toDouble(),
      averageScore: json['average_score'].toDouble(),
      grade: json['grade'],
      position: json['position'],
      remarks: json['remarks'],
    );
  }
}

class AuthService extends ChangeNotifier {
  String? _token;
  User? _user;
  List<StudentResult> _results = [];

  String? get token => _token;
  User? get user => _user;
  List<StudentResult> get results => _results;
  bool get isAuthenticated => _token != null && _user != null;

  static const String baseUrl = 'http://localhost:8000'; // Change for production

  Future<void> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username,
          'password': password,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _token = data['access_token'];
        _user = User.fromJson(data['user']);
        
        // Fetch results after successful login
        await fetchResults();
        
        notifyListeners();
      } else {
        throw Exception('Login failed');
      }
    } catch (e) {
      throw Exception('Login error: $e');
    }
  }

  Future<void> fetchResults() async {
    if (_token == null || _user == null) return;

    try {
      final response = await http.get(
        Uri.parse('$baseUrl/results?student_id=${_user!.username}'),
        headers: {
          'Authorization': 'Bearer $_token',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        _results = data.map((json) => StudentResult.fromJson(json)).toList();
        notifyListeners();
      }
    } catch (e) {
      print('Error fetching results: $e');
    }
  }

  void logout() {
    _token = null;
    _user = null;
    _results = [];
    notifyListeners();
  }
}
