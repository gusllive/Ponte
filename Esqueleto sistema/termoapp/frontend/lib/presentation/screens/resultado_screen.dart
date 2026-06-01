import 'package:flutter/material.dart';
import 'package:frontend/data/models/models.dart';

class ResultadoScreen extends StatelessWidget {
  final ResultadoTermoModel resultado;
  final String componente;

  const ResultadoScreen({
    Key? key,
    required this.resultado,
    required this.componente,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Resultados: $componente'),
        backgroundColor: Colors.teal,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Card(
          elevation: 4,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Fator de Compressibilidade (Z)',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.teal),
                ),
                Divider(),
                const SizedBox(height: 10),
                
                // Exemplo de exibição dos dados da sua Model (Ajuste conforme suas variáveis reais)
                _buildResultRow('Z Calculado:', resultado.z.toStringAsFixed(4)), 
                _buildResultRow('Volume Molar (V):', '${resultado.volumeMolar.toStringAsFixed(2)} cm³/mol'),
                _buildResultRow('Método Utilizado:', resultado.metodo),
                
                const SizedBox(height: 20),
                Center(
                  child: ElevatedButton.icon(
                    onPressed: () => Navigator.pop(context),
                    icon: Icon(Icons.arrow_back),
                    label: Text('Calcular Novamente'),
                    style: ElevatedButton.styleFrom(backgroundColor: Colors.teal),
                  ),
                )
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildResultRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500)),
          Text(value, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.black87)),
        ],
      ),
    );
  }
}