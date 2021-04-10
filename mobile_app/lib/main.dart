import 'dart:io';
import 'dart:convert';
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:path_provider/path_provider.dart';

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
      appBar: AppBar(
        title: Text('First Route'),
      ),
      body: Column(children: <Widget>[
        Spacer(),
        Center(
            child: Text(
          'connect_ME',
          style: TextStyle(fontSize: 45),
        )),
        Spacer(),
        ElevatedButton(
          child: Text(
            "Select Files to Send",
            style: TextStyle(fontSize: 30),
          ),
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => LoadingPage()),
            );
          },
        ),
        ElevatedButton(
          child: Text(
            "Send Clipboard",
            style: TextStyle(fontSize: 30),
          ),
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => LoadingPage()),
            );
          },
        ),
        Spacer(),
      ]),
    );
  }
}

class LoadingPage extends StatefulWidget {
  // initialize (send packet)
  @override
  State<StatefulWidget> createState() => _LoadingPageState();
}

class _LoadingPageState extends State<LoadingPage> {
  // pick file
  String tempPath;
  List<File> files;
  final myController = TextEditingController();

  Future getFile() async {
    print(myController.text);
    Directory tempDir = await getTemporaryDirectory();
    tempPath = tempDir.path;
    FilePickerResult result =
        await FilePicker.platform.pickFiles(allowMultiple: true, type: FileType.any);

    if (result != null) {
      files = result.paths.map((path) => File(path)).toList();
    } else {
      // User canceled the picker
    }
    // print('this is temp path' + tempPath);
    //  print(await files[0].readAsBytesSync());
  }

  Future getImage() async {
    Directory tempDir = await getTemporaryDirectory();
    tempPath = tempDir.path;
    FilePickerResult result =
        await FilePicker.platform.pickFiles(allowMultiple: true, type: FileType.image);
    if (result != null) {
      files = result.paths.map((path) => File(path)).toList();
      setState(() {});
    } else {
      // User canceled the picker
    }
  }

  // void state() {
  //   setState(() {
  //     // This call to setState tells the Flutter framework that something has
  //     // changed in this State, which causes it to rerun the build method below
  //     // so that the display can reflect the updated values. If we changed
  //     // _counter without calling setState(), then the build method would not be
  //     // called again, and so nothing would appear to happen.
  //   });
  // }

  Future send() async {
    Socket socket = await Socket.connect('143.198.234.58', 1234);
    print('connected');

    // listen to the received data event stream
    socket.listen((List<int> event) {
      print(utf8.decode(event));
    });

    // send picture
    for (var i = 0; i < files.length; i++) {
      socket.add(await files[i].readAsBytesSync());
      // wait 5 seconds
      print(files[i]);
      await Future.delayed(Duration(seconds: 5));
    }

    // .. and close the socket
    socket.close();
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
    String file_name;

    if (files == null) {
      itemCount = 0;
    } else {
      itemCount = files.length;
    }
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
      body: Column(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        children: <Widget>[
          itemCount > 0
              ? ListView.builder(
                  shrinkWrap: true,
                  itemCount: itemCount,
                  itemBuilder: (BuildContext context, int index) {
                    return ListTile(
                      title: Text(files[index].toString().substring(files[index].toString().lastIndexOf('/')+1)),
                    );
                  },
                )
              : Center(child: const Text('No items')),
          //
          //   ListView.builder(
          //   padding: const EdgeInsets.all(8),
          //     itemCount: entries.length,
          //     shrinkWrap: true,
          //     itemBuilder: (BuildContext context, int index) {
          //       return Container(
          //         height: 50,
          //         color: Colors.amber[colorCodes[index]],
          //         child: Center(child: Text('Entry ${entries[index]}')),
          //
          //       );
          //     }
          // ),
          Spacer(),
          Center(
              child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              Text(
                'Host Label',
                style: TextStyle(fontSize: 20),
              ),
              // Text(
              //   '',
              //   style: TextStyle(fontSize: 18),
              // ),
              SizedBox(
                width: 150.0,
                height: 70.0,

                child: TextField(
                  // controller: _textEditingController,
                  controller: myController,
                  obscureText: false,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.all(
                        const Radius.circular(12.0),
                      ),
                    ),
                    labelText: 'Type Host Field',
                    labelStyle: TextStyle(color: Colors.white.withOpacity(0.8)),
                  ),
                ),

                // Text(host_field.text)
                //   decoration: InputDecoration(
                //       border: OutlineInputBorder(), labelText: 'Enter Host Field'),
                // )
              )
            ],
          )),

          Spacer(),

          Center(
              child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: <Widget>[
              // Spacer(),
              ElevatedButton(
                child: Text("Select Files"),
                onPressed: getFile,
                style: ElevatedButton.styleFrom(
                    primary: Colors.purple,
                    textStyle: TextStyle(fontSize: 25, fontWeight: FontWeight.bold)),
              ),
              ElevatedButton(
                child: Text("Select Images"),
                onPressed: getImage,
                style: ElevatedButton.styleFrom(
                    primary: Colors.purple,
                    textStyle: TextStyle(fontSize: 25, fontWeight: FontWeight.bold)),
              ),
            ],
          )),
          ElevatedButton(
            child: Text("Send File"),
            onPressed: send,
            style: ElevatedButton.styleFrom(
                primary: Colors.purple,
                textStyle: TextStyle(fontSize: 30, fontWeight: FontWeight.bold)),
          ),
          Spacer(),

          // TODO need to change files index (show error msg)
        ],
      ),
    );
  }
}
