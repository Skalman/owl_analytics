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
