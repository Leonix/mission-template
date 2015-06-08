var vm = require('vm');
var util = require('util');

function ClientLoop(port, environment_id){
	this.is_checking = false;
	this.connection_port = port;
	this.environment_id = environment_id;
	this.callActions = this.getCallActions();
	this.connection = this.getConnection();
	this.traceError();
}

ClientLoop.prototype.consoleErrorTraceback = function(err){
	var lines = err.stack.split('\n');
	var from_vm = false;
    for(var i=0; i<lines.length; i++){
    	var l = lines[i].trim();
    	if(l.slice(0, 3) == 'at ') {
    		if(l.slice(0, 15) == 'at evalmachine.'){
    			console.error(lines[i]);
    			from_vm = true;
    		}
    	} else {
    		console.error(lines[i])
    	}
    }
    return from_vm
}

ClientLoop.prototype.traceError = function() {
	process.on('uncaughtException', (function(err) {
	    this.consoleErrorTraceback(err)

	}).bind(this))
}

ClientLoop.prototype.getVMContext = function() {
	return vm.createContext(this.getVMSandbox());
}

ClientLoop.prototype.getVMSandbox = function() {
	var ret = {
		'console': console,
		'require': require,
		'setTimeout': setTimeout,
		'clearTimeout': clearTimeout,
		'setInterval': setInterval,
		'clearInterval': clearInterval
	}
	if (this.is_checking) {
		ret['__is_checking'] = true;
	}
	ret['global'] = ret;
	ret['require'] = require;
	ret['setTimeout'] = setTimeout;
	return ret
}

ClientLoop.prototype.getConnection = function() {
	var net = require('net');
	var client = new net.Socket();
	client.connect(this.connection_port, '127.0.0.1', this.onClientConnected.bind(this));

	(function(loop) {
		var current_command = '';
		client.on('data', function(data) {
			data = String(data);
			for(var i=0; i<data.length; i++) {
				var c = data.charAt(i);
				if(c == '\0'){
					loop.onClientData(JSON.parse(current_command));
					current_command = '';
				} else {
					current_command+=c;
				}
			}
		});
	})(this);
	return client
}

ClientLoop.prototype.clientWrite = function(data) {
	this.connection.write(JSON.stringify(data) + '\0')
}

ClientLoop.prototype.onClientData = function(data) {
	result = this.callActions[data['action']](data)
	if(result){
		this.clientWrite(result)
	}
}

ClientLoop.prototype.onClientConnected = function() {
	this.clientWrite({
		'status': 'connected',
		'environment_id': this.environment_id,
		'pid': process.pid
	})
}

ClientLoop.prototype.getCallActions = function() {
	return {
		'run_code': this.actionRunCode.bind(this),
		'run_function': this.actionRunFunction.bind(this),
		'stop': this.actionStop.bind(this),
		'config': this.actionConfig.bind(this)
	}
}

ClientLoop.prototype.actionRunCode = function(data) {
	this.vmContext = this.getVMContext();
	var result;
	try{
		result = vm.runInContext(data['code'], this.vmContext);
	}catch(err){
		this.consoleErrorTraceback(err)
		return {
			'status': 'fail'
		}
	}
	return {
		'status': 'success',
		'result': result
	}
}

ClientLoop.prototype.actionRunFunction = function(data) {
	var result;
	try{
		result = this.vmContext[data['function_name']](data['function_args']);
	}catch(err){
		this.consoleErrorTraceback(err)
		return {
			'status': 'fail'
		}

	}
	return {
		'status': 'success',
		'result': result
	}
}

ClientLoop.prototype.actionStop = function(data) {
	this.connection.destroy();
}

ClientLoop.prototype.actionConfig = function(data) {
	var config = data.env_config;
	if (config.is_checking) {
		this.is_checking = true;
	}
	return {
		'status': 'success'
	}
}

exports.ClientLoop = ClientLoop