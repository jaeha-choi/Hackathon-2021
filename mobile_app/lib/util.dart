import 'dart:typed_data';
import 'package:path_provider/path_provider.dart';
import 'dart:io';
import 'main.dart';
import 'dart:io';


Socket socket;
Future<String> getFilePath() async {
  /*    We call getApplicationDocumentsDirectory. This comes from the path_provider package that we installed earlier. This will get whatever the common documents directory is for the platform that we are using.
    Get the path to the documents directory as a String
    Create the full file path as a String.
   */
  Directory appDocumentsDirectory = await getApplicationDocumentsDirectory(); // 1
  String appDocumentsPath = appDocumentsDirectory.path; // 2
  String filePath = '$appDocumentsPath/demoTextFile.txt'; // 3

  return filePath;
}

Uint64List int8BigEndianBytes(var value) =>
    Uint64List(64)..buffer.asByteData().setInt64(0, value, Endian.big);

Uint8List _recv_n_byte(RawSocket socket, packet_size) {
  /*                                   # int
    Private function to receive n amount of bytes
    :param conn: Connection socket
    :param packet_size: Total size of a packet to receive
    :return: Received data in bytes. None if not all bytes were received.
    */
  var data;
  // var socket1 = Socket.connect('143.198.234.58', 1234);
  while (data.length < packet_size){
    var packet  = socket.read(packet_size -data.length);
    if (packet == null) {
      return null; // TODO not sure
    }
    else {
      data += packet;
    }
    return data;
        // read raw data up to 4 byte
  }
}

Uint64List _get_pkt_size(RawSocket socket) {
  //Receive first four bytes
  var b_pkt_len = _recv_n_byte(socket, 4);
  if (b_pkt_len == null){
    return null;
  }
  else{
    //convert byte to unsigned long
    return int8BigEndianBytes(b_pkt_len);
  }

}

Future<bool> recv_bin(RawSocket socket, file_name)async {
  /*
    Receive file as binary format
    :param conn: Connection socket
    :param file_n: File name to save as
    :return: True if successfully received, False otherwise.
    */

  Uint64List packet_size = _get_pkt_size(socket);
  if (packet_size = null) {
    return false;
  } else {
    File file = File(await getFilePath());
    var data = _recv_n_byte(socket, packet_size);
    file.writeAsBytes(data);
    return true;
  }
}



