import 'package:flutter/material.dart';
import 'parking_screen.dart';

void main() {
  runApp(ParkInApp());
}

class ParkInApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ParkIn',
      debugShowCheckedModeBanner: false,
      home: ParkingScreen(),
    );
  }
}
  /*flutter clean 
    flutter pub get 
    flutter run -d chrome*/
