(function () {

module('Sequence');

var data = {
	// This represents the following sequence.
	// a b
	// |\|
	// c d
	// | |\
	// | e f
	// |/
	// g
	blocks: [
		{ id: 'a' },
		{ id: 'b' },
		{ id: 'c' },
		{ id: 'd' },
		{ id: 'e' },
		{ id: 'f' },
		{ id: 'g' }
	],
	edges: [
		{ id: 1, from: 'a', to: 'c' },
		{ id: 2, from: 'a', to: 'd' },
		{ id: 3, from: 'b', to: 'd' },
		{ id: 4, from: 'd', to: 'e' },
		{ id: 5, from: 'd', to: 'f' },
		{ id: 6, from: 'c', to: 'g' },
		{ id: 7, from: 'e', to: 'g' }
	]
};

test('sequence.get_edges', 3, function () {
	var seq = new Sequence(data);

	deepEqual(seq.get_edges('a'), {
		inputs:[],
		outputs:[
			seq.get_edge(1),
			seq.get_edge(2)
		]
	}, 'No inputs, outputs');

	deepEqual(seq.get_edges('c'), {
		inputs:[seq.get_edge(1)],
		outputs:[seq.get_edge(6)]
	}, 'Inputs and outputs');

	deepEqual(seq.get_edges('g'), {
		inputs:[seq.get_edge(6), seq.get_edge(7)],
		outputs:[]
	}, 'Inputs, no outputs');

});


test('sequence.get_sources', 1, function () {
	var seq = new Sequence(data);

	deepEqual(seq.get_sources(), [
		seq.get_block('a'),
		seq.get_block('b')
	], 'Get 2 sources');
});

test('sequence.sort_blocks', 1, function () {
	var seq = new Sequence(data);

	// time\branch  0 1 2
	//
	// 0.           a b
	//              |\|
	// 1.           c d
	//              | |\
	// 2.           | e f
	//              |/
	// 3.           g

	deepEqual(seq.sort_blocks(), {
		a: { time: 0, branch: 0 },
		b: { time: 0, branch: 1 },
		c: { time: 1, branch: 0 },
		d: { time: 1, branch: 1 },
		e: { time: 2, branch: 1 },
		f: { time: 2, branch: 2 },
		g: { time: 3, branch: 0 }
	}, 'Sort blocks');

});

})();
