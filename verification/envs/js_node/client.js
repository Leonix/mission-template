"use strict";
var vm = require('vm');
var util = require('util');

function ClientLoop(port, environment_id) {
    this.connection_port = port;
    this.environment_id = environment_id;
    this.debug = false;
    this.TMP_VAR = '__TMP_DATA';
}

ClientLoop.prototype.start = function () {
    this.is_checking = false;
    this.callActions = this.getCallActions();
    this.connection = this.getConnection();
    this.traceError();
    this.coverCode = function cover(func, data, ctx) {
        ctx = ctx || this;
        return func.apply(ctx, [data]);
    };
};

ClientLoop.prototype.prepareCoverCode = function (code) {
    var context = vm.createContext();
    vm.runInContext(code, context);
    this.coverCode = context.cover;
};

ClientLoop.prototype.consoleErrorTraceback = function (err) {
    var lines = err.stack.split('\n'),
        i = 0,
        line,
        from_vm = false;

    for (i = 0; i < lines.length; i += 1) {
        line = lines[i].trim();
        if (line.slice(0, 3) === 'at ') {
            if (line.search('evalmachine') !== -1) {
                console.error(lines[i]);
                from_vm = true;
            } else if (this.debug) {
                console.error(lines[i]);
            }
        } else {
            console.error(lines[i]);
        }
    }
    return from_vm;
};


ClientLoop.prototype.traceError = function () {
    process.on('uncaughtException', function (err) {
        this.consoleErrorTraceback(err);

    }.bind(this));
};

ClientLoop.prototype.getVMContext = function () {
    return vm.createContext(this.getVMSandbox());
};

ClientLoop.prototype.getVMSandbox = function () {
    var ret = {
        'console': console,
        'require': require,
        'setTimeout': setTimeout,
        'clearTimeout': clearTimeout,
        'setInterval': setInterval,
        'clearInterval': clearInterval,
        'setImmediate': setImmediate,
        'clearImmediate': clearImmediate
    };
    if (this.is_checking) {
        ret.is_checking = true;
    }
    ret.global = ret;
    return ret;
};

ClientLoop.prototype.getConnection = function () {
    var net = require('net'),
        client = new net.Socket();
    client.connect(this.connection_port, '127.0.0.1', this.onClientConnected.bind(this));

    (function (loop) {
        var current_command = '';
        client.on('data', function (data) {
            var i = 0,
                iChar;
            data = String(data);
            for (i = 0; i < data.length; i += 1) {
                iChar = data.charAt(i);
                if (iChar === '\u0000') {
                    loop.onClientData(JSON.parse(current_command));
                    current_command = '';
                } else {
                    current_command += iChar;
                }
            }
        });
    }(this));
    return client;
};

ClientLoop.prototype.clientWrite = function (data) {
    this.connection.write(JSON.stringify(data) + '\u0000');
};

ClientLoop.prototype.onClientData = function (data) {
    var result = this.callActions[data.action](data);
    if (result) {
        this.clientWrite(result);
    }
};

ClientLoop.prototype.onClientConnected = function () {
    this.clientWrite({
        'status': 'connected',
        'environment_id': this.environment_id,
        'pid': process.pid
    });
};

ClientLoop.prototype.getCallActions = function () {
    return {
        'run_code': this.actionRunCode.bind(this),
        'run_function': this.actionRunFunction.bind(this),
        'stop': this.actionStop.bind(this),
        'config': this.actionConfig.bind(this)
    };
};

ClientLoop.prototype.actionRunCode = function (data) {
    this.vmContext = this.getVMContext();
    var result;
    try {
        result = vm.runInContext(data.code, this.vmContext);
    } catch (err) {
        this.consoleErrorTraceback(err);
        return {
            'status': 'fail'
        };
    }
    return {
        'status': 'success',
        'result': result
    };
};

ClientLoop.prototype.actionRunFunction = function (data) {
    var result, var_result;
    try {
        vm.runInContext(this.TMP_VAR + ' = ' + JSON.stringify(data.function_args), this.vmContext);
        var_result = this.vmContext[this.TMP_VAR];
        delete this.vmContext[this.TMP_VAR];
        result = this.coverCode(this.vmContext[data.function_name], var_result);
    } catch (err) {
        this.consoleErrorTraceback(err);
        return {
            'status': 'fail'
        };
    }
    return {
        'status': 'success',
        'result': result
    };
};

ClientLoop.prototype.actionStop = function () {
    this.connection.destroy();
};

ClientLoop.prototype.actionConfig = function (data) {
    var config = data.env_config;
    if (config.is_checking) {
        this.is_checking = true;
    }
    if (config.cover_code) {
        this.prepareCoverCode(config.cover_code);
    }
    return {
        'status': 'success'
    };
};

exports.ClientLoop = ClientLoop;
