import 'package:flutter/material.dart';
import 'package:frontend/data/models/models.dart';
import 'package:frontend/data/providers/providers.dart';

class FormularioTermoScreen extends StatefulWidget {
  const FormularioTermoScreen({super.key});

  @override
  State<FormularioTermoScreen> createState() => _FormularioTermoScreenState();
}

class _FormularioTermoScreenState extends State<FormularioTermoScreen> {
  final _apiService = TermoApiService();

  final _tController = TextEditingController(text: '200');
  final _pController = TextEditingController(text: '10');

  List<String> _componentes = [];
  String? _componenteSelecionado;
  ResultadoTermoModel? _resultado;

  bool _carregandoComponentes = true;
  bool _calculando = false;

  @override
  void initState() {
    super.initState();
    _inicializarBanco();
  }

  void _inicializarBanco() async {
    try {
      final lista = await _apiService.buscarComponentes();
      setState(() {
        _componentes = lista;
        if (lista.isNotEmpty) _componenteSelecionado = lista.first;
        _carregandoComponentes = false;
      });
    } catch (e) {
      setState(() => _carregandoComponentes = false);
      _mostrarErro('Não foi possível conectar ao banco de dados Python.');
    }
  }

  void _executarCalculo() async {
    if (_componenteSelecionado == null) return;
    setState(() => _calculando = true);

    try {
      final res = await _apiService.calcularPitzer(
        _componenteSelecionado!,
        double.parse(_tController.text),
        double.parse(_pController.text),
      );
      setState(() {
        _resultado = res;
        _calculando = false;
      });
    } catch (e) {
      setState(() => _calculando = false);
      _mostrarErro(
        'Erro na conversão matemática. Verifique os valores inseridos.',
      );
    }
  }

  void _mostrarErro(String msg) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Termodinâmica Química - Cap. 3'),
        backgroundColor: Colors.teal,
      ),
      body: _carregandoComponentes
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Text(
                    'Selecione o Componente Químico (do Banco Pickle):',
                  ),
                  DropdownButton<String>(
                    value: _componenteSelecionado,
                    isExpanded: true,
                    items: _componentes.map((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(value),
                      );
                    }).toList(),
                    onChanged: (novoValor) =>
                        setState(() => _componenteSelecionado = novoValor),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: _tController,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(
                      labelText: 'Temperatura T (K)',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: _pController,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(
                      labelText: 'Pressão P (bar)',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 24),
                  ElevatedButton(
                    onPressed: _calculando ? null : _executarCalculo,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.teal,
                      padding: const EdgeInsets.all(16),
                    ),
                    child: _calculando
                        ? const CircularProgressIndicator(color: Colors.white)
                        : const Text(
                            'Calcular Correlação Pitzer',
                            style: TextStyle(fontSize: 16, color: Colors.white),
                          ),
                  ),
                  if (_resultado != null) ...[
                    const Padding(
                      padding: EdgeInsets.symmetric(vertical: 16),
                      child: Divider(),
                    ),
                    Card(
                      elevation: 4,
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Resultados: ${_resultado!.componente}',
                              style: const TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: Colors.teal,
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text('Temp. Reduzida (Tr): ${_resultado!.tr}'),
                            Text('Pressão Reduzida (Pr): ${_resultado!.pr}'),
                            Text(
                              'Z0 (Fluido de Referência): ${_resultado!.z0}',
                            ),
                            Text('Z1 (Fator Corretivo): ${_resultado!.z1}'),
                            const SizedBox(height: 8),
                            Text(
                              'Fator de Compressibilidade (Z): ${_resultado!.zFinal}',
                              style: const TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: Colors.blue,
                              ),
                            ),
                            Text(
                              'Volume Molar (V): ${_resultado!.vMolar} cm³/mol',
                              style: const TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: Colors.deepOrange,
                              ),
                            ),
                          ],
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
