import 'package:assincronismo/models/account.dart';

double calculateTaxesByAccount({
  required Account sender,
  required double amount,
}) {
  if (amount < 5000) return 0;
  if (sender.accountType != null) {
    if (sender.accountType!.toUpperCase() == "AMBROSIA") {
      return amount * 0.005;
    } else if (sender.accountType!.toUpperCase() == "CANJICA") {
      return amount * 0.0033;
    } else if (sender.accountType!.toUpperCase() == "PUDIM") {
      return amount * 0.0025;
    } else {
      return amount * 0.0001; // É BRIGADEIRO
    }
  } else {
    return 0;
  }
}
