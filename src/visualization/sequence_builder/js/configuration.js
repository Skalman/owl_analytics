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
	],
	"edges": [
		{
			"id": "edge-3",

			"from": {
				"block": "g-abc",
				"port": "market_data",
			},
			"to": {
				"block": "my-macd",
				"port": "market_data"
			}
		},
		{
			"id": "edge-4",
			"from": {
				"block": "my-macd",
				"port": "indicator",
			},
			"to": {
				"block": "my-chunker",
				"port": "data"
			}
		},
	],
	"types": [
		{
			"type": "google",

			"input": [],
			"output": [
				{
					"port": "market_data",
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
					"port": "market_data",
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
					"port": "market_data",
					"type": "ohlcvt"
				}
			],

			"output": [
				{
					"port": "macd",
					"type": "moving-average"
				},
				{
					"port": "signal",
					"type": "moving-average"
				},
				{
					"port": "indicator",
					"type": "zeroline-oscillator"
				},
				{
					"port": "indicator_inverse",
					"type": "zeroline-oscillator"
				}
			],

			"parameters": [
				{
					"name": "price",
					"type": ["open", "high", "low", "close"],
					"default": "close"
				},
				{
					"name": "fast",
					"type": "number",
					"default": 35
				},
				{
					"name": "slow",
					"type": "number",
					"default": 5
				},
				{
					"name": "nema",
					"type": "number",
					"default": 10
				}
			]
		},

		{
			"type": "sign-chunker",

			"input": [
				{
					"port": "data",
					"type": "zeroline-oscillator"
				}
			],

			"output": [
				{
					"port": "chunks",
					"type": "zeroline-oscillator-chunks"
				}
			],

			"parameters": []
		}
	]
};