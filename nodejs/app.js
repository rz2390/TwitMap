// express() is a function rather than a method. A method usually refers to a function that is attached to an object, while in JavaScript, methods are just functions that you reference via object properties.
// A constructor in JavaScript is a function you call via the "new" operatior.
// ExpressJS is a NodeJS module, and "express" is the name of that module.
// "require" function is provided by NodeJS to load modules so as to access their exports.

var express = require('express'); //require the express module and puts it in a variable
var app = express(); //call the express function and start a new Express Application (express is like a class and app is like a newly created object here)
var server = require('http').createServer(app); //create a resulting instance of function http.server()
var io = require('socket.io')(server); //add an event listener to "server" - an instance of http.server()

app.use(express.static('public')); //serve images, CSS files and JavaScript files in the public directory
app.get('/', function (req, res) {
    res.sendfile(__dirname + '/public/index.html');
}); //deliver HTML files: "req" is an object obtaining information about HTTP request that raised the event, "res" is to send back desired HTTP request

server.listen(2222); //let the server listen to port 2222 (AWS Linux Virtual Machine does not allow listening to default port 80)

var elasticsearch = require('elasticsearch'); //require the elasticsearch module
var client = new elasticsearch.Client({
    host: ' '
}); //proxy elasticsearch requests; here the host is the endpoint of created domain for storing twitter streaming data + HTTP port 443; alternative form can be composed of four separate sections - protocal, host, port, and path

//socket.IO enables real-time bidirectional event-based communication.
//attaches socket.io to the HTTP server listening on port 2222.
io.on('connection', function (socket) {
    socket.emit('news', {message: 'welcome!', id: socket.id}); //emit events to connected sockets
    socket.on('my other event', function (data) { //listen to the socket
        var key = data.key; //send JSON data
        client.search({
            q: key,
            size: 4000
        }, function (error, body) {
            var result = []; //return elasticsearch results
            var hits = body.hits.hits;
            for (var i = 0; i < hits.length; i++) { //parse the data
                result[i] = hits[i]._source;
            }
            var myObject = {
                "tweet": result
            };
            socket.emit('toggle', myObject);
        });
    });
});
