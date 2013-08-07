(function () {

module('Typed sequence');

var conf = {
	blocks: [
		{ id: 'block-google', type: 'google',
			symbol: 'ABC',
			exchange: 'NYSE',
			tick: '1m',
			time_period: '1d'
		},
		{ id: 'block-yahoo', type: 'yahoo',
			symbol: 'DEF',
			exchange: 'NYSE',
			tick: '1m',
			time_period: '1d'
		},
		{ id: 'block-macd', type: 'macd',
			fast: 35,
			slow: 5,
			nema: 10,
		},
		{ id: 'block-chunker', type: 'sign-chunker'
		}
	],
	edges: [
		{ id: 'google > macd',
			from: { block: 'block-google', port: 'market_data', },
			to: { block: 'block-macd', port: 'market_data' }
		},
		{ id: 'yahoo > macd',
			from: { block: 'block-yahoo', port: 'market_data' },
			to: { block: 'block-macd', port: 'market_data' }
		},
		{ id: 'macd > chunker',
			from: { block: 'block-macd', port: 'indicator' },
			to: { block: 'block-chunker', port: 'data' }
		}
	],
	types: [
		{ type: 'google',
			input: [],
			output: [ { port: 'market_data', type: 'ohlcvt' } ],
			parameters: [
				{ name: 'symbol', type: 'string', required: true },
				{ name: 'exchange', type: 'string', required: true },
				{ name: 'tick', type: 'time', required: false, default: '1m' },
				{ name: 'time_period', type: 'time', required: false, default: '1d' }
			]
		},

		{ type: 'yahoo',
			input: [],
			output: [ { port: 'market_data', type: 'ohlcvt' } ],
			parameters: [
				{ name: 'symbol', type: 'string', required: true },
				{ name: 'exchange', type: 'string', required: true },
				{ name: 'tick', type: 'time', default: '1m' },
				{ name: 'time_period', type: 'time', default: '1d' }
			]
		},

		{ type: 'macd',
			input: [ { port: 'market_data', type: 'ohlcvt' } ],
			output: [
				{ port: 'macd', type: 'moving-average' },
				{ port: 'signal', type: 'moving-average' },
				{ port: 'indicator', type: 'zeroline-oscillator' },
				{ port: 'indicator_inverse', type: 'zeroline-oscillator' }
			],
			parameters: [
				{ name: 'price', type: ['open', 'high', 'low', 'close'], default: 'close' },
				{ name: 'fast', type: 'number', default: 35 },
				{ name: 'slow', type: 'number', default: 5 },
				{ name: 'nema', type: 'number', default: 10 }
			]
		},

		{
			type: 'sign-chunker',
			input: [ { port: 'data', type: 'zeroline-oscillator' } ],
			output: [ { port: 'chunks', type: 'zeroline-oscillator-chunks' } ],
			parameters: []
		}
	]
};

test('sequence.get_edges', 3, function () {
	var seq = new Typed_sequence(conf);
	window.seq = seq;

	deepEqual(seq.get_edges('block-google'), {
		inputs:[],
		outputs:[seq.get_edge('google > macd')]
	}, 'No inputs, outputs');

	deepEqual(seq.get_edges('block-macd'), {
		inputs:[
			seq.get_edge('google > macd'),
			seq.get_edge('yahoo > macd')
		],
		outputs:[seq.get_edge('macd > chunker')]
	}, 'Inputs and outputs');

	deepEqual(seq.get_edges('block-chunker'), {
		inputs:[seq.get_edge('macd > chunker')],
		outputs:[]
	}, 'Inputs, no outputs');

});


test('sequence.get_sources', 1, function () {
	var seq = new Typed_sequence(conf);

	deepEqual(seq.get_sources(), [
		seq.get_block('block-google'),
		seq.get_block('block-yahoo')
	], 'Get 2 sources');
});

test('sequence.sort_blocks', 1, function () {
	var seq = new Typed_sequence(conf);

	// time\branch  0       1
	//
	// 0.           google  yahoo
	//              |      /
	// 1.           macd--´
	//              |
	// 2.           chunker

	deepEqual(seq.sort_blocks(), {
		'block-google': { time: 0, branch: 0 },
		'block-yahoo': { time: 0, branch: 1 },
		'block-macd': { time: 1, branch: 0 },
		'block-chunker': { time: 2, branch: 0 },
	}, 'Sort blocks');

});

})();
