var optimist = require('optimist');
var ClientLoop = require('./client.js').ClientLoop;

var argv = optimist.argv._;
var client = new ClientLoop(argv[0], argv[1]);
client.start();
