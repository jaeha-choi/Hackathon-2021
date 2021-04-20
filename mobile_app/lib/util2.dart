import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:math';
import 'dart:typed_data';




// Byte to unsigned int32
int byteToUint32(Uint8List value) {
  var buffer = value.buffer;
  var byteData = new ByteData.view(buffer);
  return byteData.getUint32(0);
}


// Unsigned int32 to byte
Uint8List uint32ToByte(int value) =>
    Uint8List(4)..buffer.asByteData().setInt32(0, value, Endian.big);

int getPacketSize(RawSocket conn) {
  Uint8List data = conn.read(4);
  print(data);
  // Stream.conn
  // print(data);
  // var data = new StreamController(<List<int>>)();
  // var data;
  // conn.transform(new IntConverter(4)).listen((4) => 4.forEach(print));
  if (data == null) {
    return -1;
  }
  // convert byte to unsigned long
  // return conn.buffer.asInt64List();
  return byteToUint32(data);
}

// Returns [string, status]
List recvStr(RawSocket conn) {
  String string = "";
  try {
    int packetSize = getPacketSize(conn);
    print(packetSize);
    if (packetSize == -1) {
      return [string, false];
    } else {
      Uint8List data = conn.read(packetSize);
      string = utf8.decode(data);
    }
  } catch (error) {
    print("Unknown error in recv_str");
    return [string, false];
  }
  return [string, true];
}

bool sendStr(RawSocket conn, String msg) {
  try {
    // Convert string to byte
    var bytes = utf8.encode(msg);
    // Get size of total bytes to send
    var size = uint32ToByte(bytes.length);
    // print(msg);
    conn.write(size);
    conn.write(bytes);
  } catch (error) {
    return false;
  }
  return true;
}

Future<bool> sendBin(RawSocket conn, File file) async {
  try {
    var sizeInByte = uint32ToByte(await file.length());
    conn.write(sizeInByte);
    conn.write(await file.readAsBytes());
  } catch (error) {
    print("Unknown error in send_bin" + error);
    return false;
  }
  return true;
}

void sendHeartbeat(RawSocket conn) {
  var bytes = utf8.encode('HRB');
  var size = uint32ToByte(bytes.length);
  conn.write(size + bytes);
}

void sendUuid(RawSocket conn, String uid) {
  sendStr(conn, "ADD");
  sendStr(conn, uid);

  // send priv_ip, priv_port
  sendStr(conn, conn.address.toString());
  sendStr(conn, conn.port.toString());
}

Future<bool> sendFileRelay(RawSocket conn, String recvUid, List<File> files,
    List<String> serverSaveNames) async {
  if (files.length != serverSaveNames.length) {
    return false;
  }
  print(conn);

  sendStr(conn, "DRL");
  sendStr(conn, recvUid);

  var res = recvStr(conn);  //TODO Fix this res = [, false]
  print(res);
  int code = int.parse(res[0]);

  // If received code is CONTINUE
  if (code == 2) {
    print("Receiver UUID found.");
    // Send file count
    sendStr(conn, files.length.toString());

    for (int i = 0; i < files.length; i++) {
      // Send name to use when saving
      sendStr(conn, serverSaveNames[i]);
      // Send file
      sendBin(conn, files[i]);
      code = int.parse(recvStr(conn)[0]);
      if (code != 2) {
        return false;
      }
    }
  } else if (code == 3) {
    print("Receiver UUID NOT found.");
    return false;
  }
  return true;
}
