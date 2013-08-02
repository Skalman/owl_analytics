var Typed_sequence = (function (_super_class, Error) {
	'use strict';

	var _super = _super_class.prototype;

	function Typed_sequence(options) {
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
			console.log( 'types', types );
			var i;
			this.types = {};
			for (i = 0; i < types.length; i++) {
				this.types[types[i].type] = types[i];
			}
			console.log( 'this.types', this.types );
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


			// TODO
			block = {
				"id": "g-abc",
				"type": "google",
				
				"symbol": "ABC",
				"exchange": "NYSE",
				"minutes": 1,
				"days": 1
			}
			return true;
		},

		set_block: function (block) {
			this.assert_valid_block(block);
			_super.set_block.call(this, block);
		},

		is_valid_edge: function (edge) {
			// TODO
			edge = {
				"id": "edge-1",
				"from": "g-abc",
				
				"to": "my-combiner",
				"input_type": "default",
			}

			return true;
		},

		set_edge: function (edge) {
			if (this.is_valid_edge(edge)) {
				_super.set_edge.call(this, edge);
			} else {
				throw new Error('Edge input and output type error: missing, do not match the block types, or do not match each other');
			}
		}
	});




	function extend(obj, source) {
		for (var prop in source) {
			obj[prop] = source[prop];
		}
		return obj;
	}

	return Typed_sequence;

}(Sequence, Error));
