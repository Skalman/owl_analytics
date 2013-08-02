var Sequence = (function (undefined) {
	'use strict';

	function Sequence(options) {
		// blocks[block_id] = block
		this.blocks = {};

		// edges[edge_id] = edge
		this.edges = {};

		if (options) {
			this.set(options);
		}
	}



	Sequence.prototype = {
		set: function (sequence) {
			var i;

			if (sequence.blocks) {
				for (i = 0; i < sequence.blocks.length; i++) {
					this.set_block(sequence.blocks[i])
				}
			}

			if (sequence.edges) {
				for (i = 0; i < sequence.edges.length; i++) {
					this.set_edge(sequence.edges[i])
				}
			}
		},

		set_block: function (block) {
			this.blocks[block.id] = block;
		},

		get_block: function (block_id) {
			return this.blocks[block_id];
		},

		delete_block: function (block_id) {
			delete this.blocks[block_id];
		},

		set_edge: function (edge) {
			this.edges[edge.id] = edge;
		},

		get_edge: function (edge_id) {
			return this.edges[edge_id];
		},

		delete_edge: function (edge_id) {
			delete this.edges[edge_id];
		},

		// O(n)
		get_edges: function (block_id) {
			var i, edge;
			var inputs = [];
			var outputs = [];

			// Loop over the edges, add any that match the `block_id` to the result
			for (i in this.edges) {
				edge = this.edges[i];

				if (edge.from === block_id) {
					outputs.push(edge);
				} else if (edge.to === block_id) {
					inputs.push(edge);
				}
			}

			return {
				inputs: inputs,
				outputs: outputs,
			};
		},

		// O(n)
		get_sources: function () {
			// Each edge without a `from` represents a source
			var i;
			var sources = [];

			// Keep a map of blocks that do have inputs, i.e. they are not sources
			var not_sources = {};

			for (i in this.edges) {
				not_sources[this.edges[i].to] = true;
			}

			for (i in this.blocks) {
				if (!not_sources[i]) {
					sources.push(this.blocks[i]);
				}
			}

			return sources;
		},

		sort_blocks: function () {
			var i;
			var self = this;
			var sources = self.get_sources();
			var graph = {
				num_branches: 1,

				// matrix[branch][time] = block
				matrix: [[]],
			};

			// block_info[block_id] = {inputs_left: number_of_inputs, suggested_next: {branch:x, time:x}}
			var block_info = get_block_info(self);

			for (i = 0; i < sources.length; i++) {
				add_block(sources[i].id, 0, 0);
			}

			function get_block_info(self) {
				var i;
				var info = {};

				for (i in self.blocks) {
					info[self.blocks[i].id] = {
						inputs_left: 0,

						// `time` and `branches` will be refined until one combination is
						// finally chosen.
						time: 0,
						branches: []
					};
				}

				for (i in self.edges) {
					info[self.edges[i].to].inputs_left++;
				}

				return info;
			}

			function add_block(block_id, branch, time) {
				var info = block_info[block_id];
				info.inputs_left--;
				info.branches.push(branch);

				if (info.time < time) {
					info.time = time;
				}

				// Are there any more inputs to wait for?
				if (0 < info.inputs_left) {
					return;
				}

				// add this block to the graph now
				var i;
				var branches = info.branches;
				time = info.time;

				// Go through the suggested branches to find an unused at the current time
				branch = undefined;
				for (i = 0; i < branches.length; i++) {
					if (!graph.matrix[branches[i]][time]) {
						branch = branches[i];
						break;
					}
				}
				if (branch === undefined) {
					branch = graph.num_branches++;
					graph.matrix[branch] = [];
				}

				graph.matrix[branch][time] = block_id;
				
				var outputs = self.get_edges(block_id).outputs;

				for (i = 0; i < outputs.length; i++) {
					add_block(outputs[i].to, branch, time + 1);
				}
			}

			function transform_graph(graph) {
				var branch, time;
				var result = {};

				for (branch in graph.matrix) {
					for (time in graph.matrix[branch]) {
						result[graph.matrix[branch][time]] = {
							branch: +branch,
							time: +time
						};
					}
				}

				return result;
			}

			return transform_graph(graph);
		}
	};

	return Sequence;
}());
