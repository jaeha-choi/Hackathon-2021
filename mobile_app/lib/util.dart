import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:uuid/uuid.dart';
import 'package:open_file/open_file.dart';
import 'dart:convert';
import 'dart:typed_data';
import 'package:path_provider/path_provider.dart';
import 'dart:io';

Socket socket;
String tempPath;
List<File> files;
final myController = TextEditingController();

// SKIP validate()
//

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

int _get_pkt_size(RawSocket socket) {
  //Receive first four bytes
  var b_pkt_len = _recv_n_byte(socket, 4);
  if (b_pkt_len == null){
    return null;
  }
  else{
    //convert byte to unsigned long
    return int8bytes(b_pkt_len);
  }
}

bool passthrough(send_conn, recv_conn) {
  /*
    Get file from sender and pass it to the receiver.
    Both connection must be alive
    :param send_conn: Sender socket
    :param recv_conn: Receiver socket
    :return: True if successfully passed a file, False if not.
   */
  int total_received;
  try {
     int packet_size = _get_pkt_size(send_conn);
    if (packet_size == null) {
      return false;
    }
    // # Server sends length of bytes to expect to the receiver
    recv_conn.send_string(packet_size);

    while (total_received < packet_size) {
          var packet = send_conn(packet_size - total_received);
          if (packet == null ){
            return false;
          } else{
            total_received += packet.length;
            recv_conn.add(int32BigEndianBytes(packet_size));
          }
    }
  } catch (error) {
    print("Unknown error in passthrough");
    return false;
  }
  return true;
}

 List recv_str(conn, text) {
   /*
    Receive text as string format. If packet is not being sent, raises exception.
    :param conn: Connection socket
    :param encoding: Encoding to use for string
    :return: Tuple of received string and Boolean indicating the receive status.
    */
   String string = '';
   try {
     var packet_size = _get_pkt_size(conn);
     if (packet_size == null) {
       return [string, false];
     }
     else {
       var data = _recv_n_byte(conn, packet_size);
       string = utf8.decode(data);
     }
   } catch (error) {
     print("Unknown error in recv_str");
     return [string, false];
   }
   return [string, true];
 }

bool send_bin(conn, file_n, buff_size) {
  /*
    Send file as binary format. Could return error if folder
    permission is incorrect, path does not exist, etc.
    :param conn: Connection socket
    :param file_n: File name to save as
    :param buff_size: Size of a buffer
    :return: True if successfully sent, False otherwise.

   */
  try{
    var file = OpenFile.open(file_n);
  }
}


Future<bool> recv_bin(RawSocket socket, file_name)async {
  /*
    Receive file as binary format
    :param conn: Connection socket
    :param file_n: File name to save as
    :return: True if successfully received, False otherwise.
    */

  int packet_size = _get_pkt_size(socket);

  if (packet_size = null) {
    return false;
  } else {
    // TODO
    File file = File(await getFilePath());
    var data = _recv_n_byte(socket, packet_size);
    file.writeAsBytes(data);
    return true;
  }
}

// Done with util.py

Future send_string(String str) async {
  /*
     Function to receive String str
     :para str: String variable
     :return: Socket.add(size + bytes)
    */
  // switch string to bytes
  var bytes = utf8.encode(str);
  // switch len(var bytes) to binary and store to size
  var size = int32BigEndianBytes(bytes.length);
  socket.add(size + bytes);
}

void connects_to_socket() async {
  socket = await Socket.connect('143.198.234.58', 1234);
}

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

// chang byte to long (64bits unsigned
// Uint64List int8BigEndianBytes(var value) =>
//     Uint64List(64)..buffer.asInt64List().setInt64(0, value, Endian.big);
int int8bytes(Uint8List value) {
  var buffer = value.buffer;
  var bdata = new ByteData.view(buffer);
  return bdata.getUint32(0);
}


// change signed integer to binary
Uint8List int32BigEndianBytes(int value) =>
    Uint8List(4)..buffer.asByteData().setInt32(0, value, Endian.big);

Future send_heart_beat() async {
  var bytes = utf8.encode('HRB');
  var size = int32BigEndianBytes(bytes.length);
  print(size + bytes);
  socket.add(size + bytes);
}





Future connect(){
  connects_to_socket();
  print('Connected to a server ' );
  return send_heart_beat();
}



Future getFile() async {
  Directory tempDir = await getTemporaryDirectory();
  tempPath = tempDir.path;
  FilePickerResult result =
  await FilePicker.platform.pickFiles(allowMultiple: true, type: FileType.any);

  if (result != null) {
    files = result.paths.map((path) => File(path)).toList();
    // LoadingPage.setState(() {});
  } else {
    // User canceled the picker
  }
}

Future getImage() async {
  Directory tempDir = await getTemporaryDirectory();
  tempPath = tempDir.path;
  FilePickerResult result =
  await FilePicker.platform.pickFiles(allowMultiple: true, type: FileType.image);
  if (result != null) {
    files = result.paths.map((path) => File(path)).toList();
    // setState(() {});
  } else {
    // User canceled the picker
  }
}
Future send_file() async {
  /*
    :return: Received data in bytes. None if not all bytes were received.
     */
  connects_to_socket();
  print(socket);
  print('connected');
  //listen to the received data event stream
  // socket.listen((List<int> event) {
  //   print(utf8.decode(event));
  // });

  // send picture
  // convert 3 to bytes take string trf convert to bytes and append in addhere
  //   find len(TRF) convert to byte
  for (var i = 0; i < files.length; i++) {
    send_string('TRF');
    String fileName = files[i].toString();
    send_string(fileName.substring(fileName.lastIndexOf('/') + 1, fileName.length - 1));
    var image = files[i].readAsBytesSync();
    var size = image.length;
    socket.add(int32BigEndianBytes(size) + image);
    //    size of image(BINARY) and image(BINARY)
    // wait 5 seconds
    await Future.delayed(Duration(seconds: 5));
  }
}


Future close() {
  send_string('EXT');
  socket.close();
}

var my_uuid = get_uuid();

void send_uuid() {
  send_string('ADD');
  // send vvid
  send_string(my_uuid);

  // send priv_ip
  send_string(socket.address.toString());
  // send priv_port
  send_string(socket.port.toString());
}
// getting Uuid ();
String get_uuid() {
  var uuid = Uuid();
  return uuid.v4();
}
// send_uuid register your uuid to server
// and then run recv_file_relay
// get size first
void send_file_relay (recv_uid, file_n, server_save_n) {
  //Send dest uid
  send_string('DRL');
  // if (code -== int)
  // send uid to server
  //send file name to use for saving on server_side
  send_string(server_save_n);

  //send file
  send_string(file_n);
  send_file();



}
