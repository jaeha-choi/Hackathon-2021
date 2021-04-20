import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:ui';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:path_provider/path_provider.dart';
import 'package:uuid/uuid.dart';

import 'util2.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // Try running your application with "flutter run". You'll see the
        // application has a blue toolbar. Then, without quitting the app, try
        // changing the primarySwatch below to Colors.green and then invoke
        // "hot reload" (press "r" in the console where you ran "flutter run",
        // or simply save your changes to "hot reload" in a Flutter IDE).
        // Notice that the counter didn't reset back to zero; the application
        // is not restarted.
        primarySwatch: Colors.blue,
      ),
      darkTheme: ThemeData(
        brightness: Brightness.dark,
        /* dark theme settings */
      ),
      themeMode: ThemeMode.dark,
      // home: MyHomePage(title: 'connect_ME'),
      home: FrontPage(title: 'connect_ME'),
    );
  }
}

// class MyHomePage extends StatefulWidget {
//   MyHomePage({Key key, this.title}) : super(key: key);
//
//   // This widget is the home page of your application. It is stateful, meaning
//   // that it has a State object (defined below) that contains fields that affect
//   // how it looks.
//
//   // This class is the configuration for the state. It holds the values (in this
//   // case the title) provided by the parent (in this case the App widget) and
//   // used by the build method of the State. Fields in a Widget subclass are
//   // always marked "final".
//
//   final String title;
//
//   @override
//   _MyHomePageState createState() => _MyHomePageState();
// }

class FrontPage extends StatefulWidget {
  FrontPage({Key key, this.title}) : super(key: key);
  final String title;

  @override
  State<StatefulWidget> createState() => _FrontPageState();
}

class _FrontPageState extends State<FrontPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Center(
            child: Container(
      constraints: BoxConstraints.expand(),
      decoration: BoxDecoration(
          image: DecorationImage(
            image: AssetImage("images/spacex.jpg"),
            fit: BoxFit.cover,
          ),
          ),
      child: Column(
        children: <Widget>[
          Spacer(),
          Text(
            'connect_ME',
            style: TextStyle(fontSize: 45),
          ),
          Spacer(),
          Spacer(),
          Spacer(),
          OutlinedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => LoadingPage()),
                );
              },
              child: Text(
                "🚀  Send Files",
                style: TextStyle(fontSize: 20),
              )),
          OutlinedButton(
              onPressed: null,
              child: Text(
                "📋  Send Clipboard",
                style: TextStyle(fontSize: 20),
              )),
          Spacer(),
        ],
      ),
    )));
  }
}

// void connects_to_socket() async {
//   // socket = await RawSocket('143.198.234.58', 1234);
//   RawSocket socket = await RawSocket.connect('143.198.234.58', 1234);
// }

class LoadingPage extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => _LoadingPageState();
}

Future<String> getFilePath() async {
  /*    We call getApplicationDocumentsDirectory. This comes from the path_provider package that we installed earlier. This will get whatever the common documents directory is for the platform that we are using.
    Get the path to the documents directory as a String
    Create the full file path as a String.
   */
  Directory appDocumentsDirectory =
      await getApplicationDocumentsDirectory(); // 1
  String appDocumentsPath = appDocumentsDirectory.path; // 2
  String filePath = '$appDocumentsPath/demoTextFile.txt'; // 3
  return filePath;
}

class _LoadingPageState extends State<LoadingPage> {
  // @override
  // void initState() async {
  //   connects_to_socket();
  //   print("Socket is connected");
  //   uid = genUuid();
  //   sendUuid(socket, uid);
  //   print("Sent uuid to server");
  //
  //   // close();
  //   // print("Closed the socket conn")
  // }

  RawSocket socket ;
  String tempPath;
  List<File> files;
  var uid = "";
  final myController = TextEditingController();

  void connects_to_socket() async {

    if (uid.isEmpty) {
      setState(() {
        uid = genUuid();
      });
    }
    try {
      if (socket == null) {
        // TODO chcek if socket is usable
        socket = await RawSocket.connect('143.198.234.58', 1234);
        sendHeartbeat(socket);
        sendUuid(socket, uid);
        print('connected');
      }
      else{
        print("Already connected");
      }

    } on SocketException catch (e) {
      print("Could not connect to the server:");
      print(e);
    }
  }

  String genUuid() {
    var uuid = Uuid();
    return uuid.v4();
  }

  void close() {
    sendStr(socket, 'EXT');
    socket.close();
  }

  // Future<void> send_bin(RawSocket conn, File file, int buff_size) async {
  //   /*
  //   Send file as binary format. Could return error if folder
  //   permission is incorrect, path does not exist, etc.
  //   :param conn: Connection socket
  //   :param file_n: File name to save as
  //   :param buff_size: Size of a buffer
  //   :return: True if successfully sent, False otherwise.
  //  */ // location , fileN , path
  //   try {
  //     // final path = await _localPath;
  //     // final file = await _localFile;
  //     for (var i = 0; i < files.length; i++) {
  //       send_string('TRF');
  //       String fileName = files[i].toString();
  //       send_string(fileName.substring(
  //           fileName.lastIndexOf('/') + 1, fileName.length - 1));
  //       var image = files[i].readAsBytesSync();
  //       var size = image.length;
  //       socket.write(int32BigEndianBytes(size) + image);
  //       //    size of image(BINARY) and image(BINARY)
  //       // wait 5 seconds
  //       await Future.delayed(Duration(seconds: 5));
  //     }
  //     // var b_msg = send_string(file_n); // send size of the file first
  //     // // conn.add(b_msg);
  //     // while (true) {
  //     //   var bytes_read = await file.readAsBytes();
  //     //   if (bytes_read.isEmpty) {
  //     //     return;
  //     //   } else {
  //     //     conn.add(bytes_read);
  //     //   }
  //     // }
  //   } catch (error) {
  //     print("Unknown error in send_bin" + error);
  //     return false;
  //   }
  //   return true;
  // }

  void getFile() async {
    Directory tempDir = await getTemporaryDirectory();
    tempPath = tempDir.path;
    FilePickerResult result = await FilePicker.platform
        .pickFiles(allowMultiple: true, type: FileType.any);

    if (result != null) {
      files = result.paths.map((path) => File(path)).toList();
      setState(() {});
    } else {
      // User canceled the picker
    }
  }

  Future getImage() async {
    Directory tempDir = await getTemporaryDirectory();
    tempPath = tempDir.path;
    FilePickerResult result = await FilePicker.platform
        .pickFiles(allowMultiple: true, type: FileType.image);
    if (result != null) {
      files = result.paths.map((path) => File(path)).toList();
      setState(() {});
    } else {
      // User canceled the picker
    }
  }

  // Future send_heart_beat() async {
  //   connects_to_socket();
  //   var bytes = utf8.encode('HRB');
  //   var size = uint32ToByte(bytes.length);
  //   print(size + bytes);
  //   socket.write(size + bytes);
  // }

  Future send_file() async {
    /*
    :return: Received data in bytes. None if not all bytes were received.
     */
    connects_to_socket();
    // print(socket);
    // print('connected');

    List<String> serverSaveNames = [];
    String localName;
    for (int i = 0; i < files.length; i++) {
      localName = files[i].path;
      serverSaveNames.add(localName.substring(
          localName.lastIndexOf('/') + 1, localName.length - 1));
    }
    // sendStrTemp("DRL");

    sendFileRelay(socket, myController.text, files, serverSaveNames);
  }
  bool sendStrTemp(String msg) {
    try {
      // Convert string to byte
      var bytes = utf8.encode(msg);
      // Get size of total bytes to send
      var size = uint32ToByte(bytes.length);
      print(msg);
      socket.write(size);
      socket.write(bytes);
    } catch (error) {
      return false;
    }
    return true;
  }

  // void _incrementCounter() {
  //   setState(() {
  //     // This call to setState tells the Flutter framework that something has
  //     // changed in this State, which causes it to rerun the build method below
  //     // so that the display can reflect the updated values. If we changed
  //     // _counter without calling setState(), then the build method would not be
  //     // called again, and so nothing would appear to happen.
  //     _counter++;
  //   });
  // }

  @override
  Widget build(BuildContext context) {
    int itemCount;
    if (files == null) {
      itemCount = 0;
    } else {
      itemCount = files.length;
    }
    connects_to_socket();

    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      // appBar: AppBar(
      // Here we take the value from the MyHomePage object that was created by
      // the App.build method, and use it to set our appbar title.
      // title: Text(widget.title),
      // ),

      body: Container(
        decoration: BoxDecoration(
          color: Colors.black,
        ),
        child: Column(
          // Center is a layout widget. It takes a single child and positions it
          // in the middle of the parent.
          children: <Widget>[
            itemCount > 0
                ? Padding(
                    padding: EdgeInsets.fromLTRB(0, 30, 200, 5),
                    child: Text(
                      'connect_ME',
                      style: TextStyle(fontSize: 30),
                    ))
                : Spacer(),
            Container(
              height: 300,
              width: 400,
              child: itemCount > 0
                  ? ListView.builder(
                      shrinkWrap: true,
                      itemCount: itemCount,
                      itemBuilder: (BuildContext context, int index) {
                        return ListTile(
                            title: Text(files[index].toString().substring(
                                files[index].toString().lastIndexOf('/') + 1,
                                files[index].toString().length - 1)));
                      },
                    )
                  : Center(
                      child: Text(
                      'connect_ME',
                      style: TextStyle(fontSize: 45),
                    )),
            ),
            Center(
                child: Column(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: <Widget>[
                InkWell(
                  child: Text(
                    "Your Unique ID (Tap to copy)",
                    style: TextStyle(fontSize: 17),
                  ),
                  onTap: () {
                    // Copy uuid to clipboard
                    Clipboard.setData(new ClipboardData(text: uid));
                  },
                ),
                Container(
                    child: Padding(
                        padding: EdgeInsets.fromLTRB(0, 5, 0, 5),
                        child: InkWell(
                          child: Text(
                            uid,
                            style: TextStyle(
                                fontSize: 17, backgroundColor: Colors.white12),
                          ),
                          onTap: () {
                            // Copy uuid to clipboard
                            Clipboard.setData(new ClipboardData(text: uid));
                          },
                        ))),
                Padding(
                  padding: EdgeInsets.all(9),
                  child: SizedBox(
                    width: 300.0,
                    height: 80.0,
                    child: TextField(
                      controller: myController,
                      obscureText: false,
                      decoration: InputDecoration(
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.all(
                            const Radius.circular(12.0),
                          ),
                        ),
                        labelText: "Receiver Unique ID",
                        labelStyle:
                            TextStyle(color: Colors.white.withOpacity(0.8)),
                      ),
                    ),
                  ),
                )
              ],
            )),
            Center(
                child: Padding(
              padding: EdgeInsets.fromLTRB(0, 20, 0, 0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: <Widget>[
                  // Spacer(),
                  ElevatedButton(
                    child: Text("Select Files"),
                    onPressed: getFile,
                    style: ElevatedButton.styleFrom(
                        primary: Colors.white12,
                        textStyle: TextStyle(
                            fontSize: 25, fontWeight: FontWeight.bold)),
                  ),
                  ElevatedButton(
                    child: Text("Select Images"),
                    onPressed: getImage,
                    style: ElevatedButton.styleFrom(
                        primary: Colors.white12,
                        textStyle: TextStyle(
                            fontSize: 25, fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
            )),
            ElevatedButton(
              child: Text("Send File"),
              onPressed: send_file,
              style: ElevatedButton.styleFrom(
                  primary: Colors.purple,
                  textStyle:
                      TextStyle(fontSize: 30, fontWeight: FontWeight.bold)),
            ),
            Spacer(),
          ],
        ),
      ),
      resizeToAvoidBottomInset: false,
    );
  }
}
