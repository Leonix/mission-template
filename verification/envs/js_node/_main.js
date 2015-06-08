var net = require('net');
var optimist = require('optimist');
var vm = require('vm');

var sandbox = {
	'console': console
}
var context = vm.createContext(sandbox);
var ACTIONS = {
	'run_code': function(data) {
		result = vm.runInContext(data['code'], context);
		return {
			'status': 'success',
			'result': result
		}
	},
	'run_function': function(data) {
		result = context[data['function_name']](data['function_args'])
		return {
			'status': 'success',
			'result': result
		}
	},
	'stop': function(data) {
		client.destroy()
	},
	'config': function(data) {
		return {
			'status': 'success'
		}
	}
};

var argv = optimist.argv._;
var PORT = argv[0];
var ENV_ID = argv[1];
var current_command = '';

var client = new net.Socket();

function cl_write(data) {
	client.write(JSON.stringify(data) + '\0')
}

function process_data(data) {
	data = JSON.parse(data)
	result = ACTIONS[data['action']](data)
	if(result){
		cl_write(ACTIONS[data['action']](data))
	}
}

client.connect(PORT, '127.0.0.1', function() {
	cl_write({
		'status': 'connected',
		'environment_id': ENV_ID,
		'pid': process.pid
	})
});
client.on('data', function(data) {
	data = String(data);
	for(var i=0; i<data.length; i++) {
		var c = data.charAt(i);
		if(c == '\0'){
			process_data(current_command)
			current_command = ''
		} else {
			current_command+=c
		}
	}
});
 
client.on('close', function() {
	console.log('Connection closed');
});