var Typed_sequence = (function (_super_class, Error) {
	'use strict';

	var _super = _super_class.prototype;

	var object_toString = {}.toString;

	function Typed_sequence(options) {
		// TODO - the following line probably not necessary
		this.types = {};

		_super_class.call(this, options);
	}

	Typed_sequence.type_match = function (type, obj) {
		if (type === 'string' || type === 'number') {
			return typeof obj === type;

		} else if (type === 'time') {
			// Example matches:
			//    3m 25s
			//    3.14s
			//    15y 9mon 3d
			return !!obj && /^(\d+(\.\d+)?y)? ?(\d+(\.\d+)?mon)? ?(\d+(\.\d+)?d)? ?(\d+(\.\d+)?h)? ?(\d+(\.\d+)?m)? ?(\d+(\.\d+)?s)? ?(\d+(\.\d+)?ms)?$/.test(obj);

		} else {
			// unknown type
			return false;
		}
	};


	Typed_sequence.prototype = extend(new _super_class(), {
		set: function (sequence) {
			if (sequence.types) {
				this.set_types(sequence.types);
			}

			_super.set.call(this, sequence);
		},

		set_types: function (types) {
			// Target structure:
			// 
			// this.types[type_id] = {
			//   input[port_id] = port_type
			//   output[port_id] = port_type
			//   parameters[parameter_name] = {
			//     type = type
			//     default = default|undefined
			//     required = true|false
			//   }
			// }
			this.types = transform_types(types);

			function transform_types(types) {
				var i;
				var res = {};

				for (i = 0; i < types.length; i++) {
					res[types[i].type] = transform_type(types[i]);
				}
				return res;
			}

			function transform_type(type) {
				var i;
				var res = {
					input: {},
					output: {},
					parameters: {}
				};

				for (i = 0; i < type.input.length; i++) {
					res.input[type.input[i].port] = type.input[i].type;
				}
				for (i = 0; i < type.output.length; i++) {
					res.output[type.output[i].port] = type.output[i].type;
				}
				for (i = 0; i < type.parameters.length; i++) {
					res.parameters[type.parameters[i].name] = {
						type: type.parameters[i].type,
						'default': type.parameters[i]['default'],
						required: !!type.parameters[i].required
					};
				}
				return res;
			}
		},

		assert_valid_block: function (block) {
			if (!block.type) {
				throw new Error('Block type not specified');
			} else if (!this.types[block.type]) {
				throw new Error("Block type '" + block.type + "' is not valid");
			} else {
				// check parameters
				var i, param;
				var params = this.types[block.type].parameters;
				for (i = 0; i < params.length; i++) {
					param = params[i];
					if (block.hasOwnProperty(param.name)) {
						if (!Typed_sequence.type_match(param.type, block[param.name])) {
							throw new Error("Expected parameter '" + param.name + "' to be of type '" + param.type + "'");
						}
					} else if (param.required) {
						throw new Error("Required parameter '" + param.name + "' not given");
					}
				}
			}
			// passed all checks
		},

		is_valid_block: function (block) {
			try {
				this.assert_valid_block(block);
				return true;
			} catch (e) {
				return false;
			}
		},

		set_block: function (block) {
			this.assert_valid_block(block);
			_super.set_block.call(this, block);
		},

		assert_valid_edge: function (edge) {
			if (!edge.from) {
				console.log( edge );
				throw new Error("Expected source block 'from'");
			} else if (!edge.to) {
				throw new Error("Expected destination block 'to'");

			} else if (typeof edge.from !== 'object') {
				throw new Error("Expected source block 'from' as an object {block:<val>, port:<val>}, a " + (typeof edge.from) + " '" + edge.from + "' given");
			} else if (typeof edge.to !== 'object') {
				throw new Error("Expected source block 'to' as an object {block:<val>, port:<val>}, a " + (typeof edge.to) + " '" + edge.to + "' given");

			} else if (edge.from.port == null) {
				throw new Error("Expected source block port 'from.port'");
			} else if (edge.to.port == null) {
				throw new Error("Expected destination block port 'to.port'");
			
			} else if (!this.blocks[edge.from.block]) {
				throw new Error("Source block '" + edge.from.block + "' does not exist");
			} else if (!this.blocks[edge.to.block]) {
				throw new Error("Destination block '" + edge.to.block + "' does not exist");
			}

			var from_block = this.blocks[edge.from.block];
			var to_block = this.blocks[edge.to.block];

			var from_block_type = this.types[from_block.type];
			var to_block_type = this.types[to_block.type];

			var from_port_type = from_block_type.output[edge.from.port];
			var to_port_type = to_block_type.input[edge.to.port];

			if (from_port_type == null) {
				throw new Error("Source block '" + edge.from.block + "' of type '" + from_block.type + "' does not have an output port '" + edge.from.port + "'");
			} else if (to_port_type == null) {
				throw new Error("Destination block '" + edge.to.block + "' of type '" + to_block.type + "' does not have an input port '" + edge.to.port + "'");
			} else if (from_port_type !== to_port_type) {
				throw new Error("Port mismatch: output port is of type '" + from_port_type + "', while the input port is of type '" + to_port_type + "'");
			}

			return true;
		},

		is_valid_edge: function (edge) {
			try {
				this.assert_valid_block(block);
				return true;
			} catch (e) {
				return false;
			}
		},

		set_edge: function (edge) {
			this.assert_valid_edge(edge);
			if (edge.from.toString === object_toString) {
				edge.from.toString = return_block_as_string;
			}
			if (edge.to.toString === object_toString) {
				edge.to.toString = return_block_as_string;
			}
			_super.set_edge.call(this, edge);
		}
	});

	function return_block_as_string() {
		return this.block + '';
	}

	function extend(obj, source) {
		for (var prop in source) {
			obj[prop] = source[prop];
		}
		return obj;
	}

	return Typed_sequence;

}(Sequence, Error));
