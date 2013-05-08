from bottle import route, run, template

@route('/hello/:name')
def index(name='World'):
	return template('<b>Hello {{name}}</b>!', name=name)

@route('/api/macd')
def macd():
	from Intraday_Marketdata_Extractor_NumpyArray_JSON import mdlist
	import macd_chunker
	import json

	return json.dumps(mdlist)
	return mdlist

run(host='localhost', port=8080)
