var conf = {
	"id": "my-sequence",

	"blocks": [
		{
			"id": "g-abc",
			"type": "google",
			
			"symbol": "ABC",
			"exchange": "NYSE",
			"tick": '1m',
			"time_period": '1d'
		},
		{
			"id": "y-def",
			"type": "yahoo",
			
			"symbol": "DEF",
			"exchange": "NYSE",
			"tick": '1m',
			"time_period": '1d'
		},
		// {
		// 	"id": "my-combiner",
		// 	"type": "combiner",
		// },
		{
			"id": "my-macd",
			"type": "macd",
			
			"fast": 35,
			"slow": 5,
			"nema": 10,
		},
		{
			"id": "my-chunker",
			"type": "sign-chunker",
		},
		// {
		// 	"id": "my-output-1",
		// 	"type": "output"
		// },
	],
	"edges": [
		// {
		// 	"id": "edge-1",
		// 	"from": "g-abc",
			
		// 	"to": "my-combiner",
		// 	"input_type": "default",
		// },
		// {
		// 	"id": "edge-2",
		// 	"from": "y-def",
			
		// 	"to": "my-combiner",
		// 	"input_type": "default",
		// },
		{
			"id": "edge-3",
			"from": "g-abc",
			
			"to": "my-macd",
		},
		{
			"id": "edge-4",
			"from": "my-macd",
			"to": "my-chunker",
		},
		// {
		// 	"id": "edge-5",
		// 	"from": "my-chunker",
		// 	"to": "my-output-1",
		// }
	],
	"types": [
		{
			"type": "google",

			"input": [],
			"output": [
				{
					"type": "ohlcvt"
				}
			],

			"parameters": [
				{
					"name": "symbol",
					"type": "string",
					"required": true
				},
				{
					"name": "exchange",
					"type": "string",
					"required": true
				},
				{
					"name": "tick",
					"type": "time",
					"required": false,
					"default": "1m"
				},
				{
					"name": "time_period",
					"type": "time",
					"required": false,
					"default": "1d"
				}
			]
		},

		{
			"type": "yahoo",

			"input": [],
			"output": [
				{
					"type": "ohlcvt"
				}
			],

			"parameters": [
				{
					"name": "symbol",
					"type": "string",
					"required": true
				},
				{
					"name": "exchange",
					"type": "string",
					"required": true
				},
				{
					"name": "tick",
					"type": "time",
					"required": false,
					"default": "1m"
				},
				{
					"name": "time_period",
					"type": "time",
					"required": false,
					"default": "1d"
				}
			]
		},

		{
			"type": "macd",

			"input": [
				{
					"type": "ohlcvt"
				}
			],

			"output": [
				{
					"type": "zeroline-oscillator"
				}
			],

			"parameters": [
				{
					"name": "fast",
					"type": "number",
					"required": false,
					"default": 35
				},
				{
					"name": "slow",
					"type": "number",
					"required": false,
					"default": 5
				},
				{
					"name": "nema",
					"type": "number",
					"required": false,
					"default": 10
				}
			]
		},

		{
			"type": "sign-chunker",

			"input": [
				{
					"type": "zeroline-oscillator"
				}
			],

			"output": [
				{
					"type": "zeroline-oscillator-chunks"
				}
			],

			"parameters": []
		}
	]
};