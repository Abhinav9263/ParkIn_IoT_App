import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ParkingScreen extends StatefulWidget {
  @override
  _ParkingScreenState createState() => _ParkingScreenState();
}

class _ParkingScreenState extends State<ParkingScreen> {
  final String apiUrl = "http://192.168.31.45:5000/api";
 // Replace with your IP

  Map<String, dynamic> slots = {};
  final vehicleController = TextEditingController();
  final timeInController = TextEditingController();
  final timeOutController = TextEditingController();

  @override
  void initState() {
    super.initState();
    fetchSlots();
  }

  Future<void> fetchSlots() async {
    final res = await http.get(Uri.parse("$apiUrl/slots"));
    if (res.statusCode == 200) {
      setState(() {
        slots = json.decode(res.body);
      });
    }
  }

  Future<void> bookSlot(String slotId) async {
    final res = await http.post(
      Uri.parse("$apiUrl/book_slot"),
      headers: {"Content-Type": "application/json"},
      body: json.encode({
        "slot_id": slotId,
        "vehicle_number": vehicleController.text,
        "time_in": timeInController.text,
        "time_out": timeOutController.text,
      }),
    );

    if (res.statusCode == 200) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("✅ Slot $slotId booked successfully")),
      );
      fetchSlots();
      vehicleController.clear();
      timeInController.clear();
      timeOutController.clear();
    }
  }

  void showBookingDialog(String slotId) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: Text("Book Slot $slotId"),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: vehicleController,
              decoration: InputDecoration(labelText: "Vehicle Number"),
            ),
            TextField(
              controller: timeInController,
              decoration: InputDecoration(labelText: "Time In (e.g., 14:00)"),
            ),
            TextField(
              controller: timeOutController,
              decoration: InputDecoration(labelText: "Time Out (e.g., 15:00)"),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              bookSlot(slotId);
            },
            child: Text("Book"),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("ParkIn - Smart Parking")),
      body: slots.isEmpty
          ? Center(child: CircularProgressIndicator())
          : ListView(
              children: slots.entries.map((entry) {
                String slotId = entry.key;
                String status = entry.value['status'];
                String vehicle = entry.value['vehicle_number'];

                Color color;
                if (status == "Available") color = Colors.green;
                else if (status == "Booked") color = Colors.orange;
                else color = Colors.red;

                return Card(
                  margin: EdgeInsets.all(8),
                  child: ListTile(
                    title: Text("Slot: $slotId"),
                    subtitle: Text("Status: $status\nVehicle: $vehicle"),
                    tileColor: Colors.green.withAlpha((255 * 0.6).toInt()), // or use 153
                    trailing: status == "Available"
                        ? ElevatedButton(
                            onPressed: () => showBookingDialog(slotId),
                            child: Text("Book"),
                          )
                        : null,
                  ),
                );
              }).toList(),
            ),
    );
  }
}
