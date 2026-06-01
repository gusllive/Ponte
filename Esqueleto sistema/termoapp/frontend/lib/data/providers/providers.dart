import 'dart:convert';
import 'package:frontend/data/models/models.dart';
import 'package:http/http.dart' as http;

class TermoApiService {
  // OBS: Se você rodar no Emulador Android, mude para 'http://10.0.2.2:8000'
  // Para Flutter Web, Linux Desktop ou navegador Chrome, mantenha 127.0.0.1:8000
  final String baseUrl = 'http://127.0.0.1:8000';

  // Busca a lista de componentes cadastrados no Pickle do Python
  Future<List<String>> buscarComponentes() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/componentes'));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return List<String>.from(data['componentes']);
      } else {
        throw Exception(
          'Erro ao carregar lista de componentes do banco (Status: ${response.statusCode}).',
        );
      }
    } catch (e) {
      throw Exception(
        'Não foi possível conectar ao servidor Python. O backend está ligado? Erro: $e',
      );
    }
  }

  // Envia os dados para a rota de cálculo do Pitzer de 2 coeficientes
  Future<ResultadoTermoModel> calcularPitzer(
    String comp,
    double t,
    double p,
  ) async {
    try {
      final url = Uri.parse('$baseUrl/calcular/pitzer?comp=$comp&t=$t&p=$p');
      final response = await http.get(url);

      if (response.statusCode == 200) {
        return ResultadoTermoModel.fromJson(jsonDecode(response.body));
      } else {
        throw Exception(
          'Erro ao processar cálculo no servidor Python (Status: ${response.statusCode}).',
        );
      }
    } catch (e) {
      throw Exception('Falha na comunicação com a API para cálculo: $e');
    }
  }
}
