import 'package:flutter/material.dart';
import 'package:frontend/presentation/screens/screens.dart';

void main() {
  runApp(const EngenhariaTermoApp());
}

class EngenhariaTermoApp extends StatelessWidget {
  const EngenhariaTermoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Termodinâmica Aplicada',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(primarySwatch: Colors.teal, useMaterial3: true),
      home: const FormularioTermoScreen(),
    );
  }
}
