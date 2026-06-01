class ResultadoTermoModel {
  final String componente;
  final double tr;
  final double pr;
  final double z0;
  final double z1;
  final double zFinal;
  final double vMolar;

  ResultadoTermoModel({
    required this.componente,
    required this.tr,
    required this.pr,
    required this.z0,
    required this.z1,
    required this.zFinal,
    required this.vMolar,
  });

  // Converte o mapa JSON vindo da API FastAPI para o objeto Dart
  factory ResultadoTermoModel.fromJson(Map<String, dynamic> json) {
    return ResultadoTermoModel(
      componente: json['componente'] ?? '',
      tr: (json['Tr'] as num?)?.toDouble() ?? 0.0,
      pr: (json['Pr'] as num?)?.toDouble() ?? 0.0,
      z0: (json['Z0'] as num?)?.toDouble() ?? 0.0,
      z1: (json['Z1'] as num?)?.toDouble() ?? 0.0,
      zFinal: (json['Z_final'] as num?)?.toDouble() ?? 0.0,
      vMolar: (json['V_molar'] as num?)?.toDouble() ?? 0.0,
    );
  }

  // CORREÇÃO 1: Em vez de retornar null, aponta direto para a variável vMolar
  double get volumeMolar => vMolar;

  // CORREÇÃO 2: Retorna o valor real de Z calculado
  double get z => zFinal;

  // CORREÇÃO 3: Devolve o nome do método dinamicamente (ou mude para fixo se quiser)
  String get metodo => "Pitzer / Lee-Kesler";
}
