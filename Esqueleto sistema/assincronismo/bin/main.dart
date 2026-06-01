import 'package:assincronismo/exceptions/transaction_exceptions.dart';
import 'package:assincronismo/screens/account_screen.dart';
import 'package:assincronismo/services/transaction_service.dart';

void main() {
  TransactionService()
      .makeTransaction(idSender: "ID001", idReceiver: "ID002", amount: 5000)
      .catchError((e) {
        print(e.message);
        print(
          "${e.cause.name} possui saldo ${e.cause.balance} que é menor que ${e.amount + e.taxes}",
        );
      }, test: (error) => error is InsufficientFundsException)
      .then((value) {});

  AccountScreen accountScreen = AccountScreen();
  accountScreen.initializeStream();
  accountScreen.runChatBot();
}
