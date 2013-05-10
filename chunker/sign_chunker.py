
def sign(num, zero):
	if num > 0:
		return 1
	elif num < 0:
		return -1
	else:
		return zero

def sign_chunker(data, return_data = None, include_last = False):
	"""
	Chunks a list by the sign.

	>>> sign_chunker([1, 2, -3, -4, 5])
	[{'data': [1, 2],   'sign':  1},
	 {'data': [-3, -4], 'sign': -1}]
	>>> sign_chunker([0, 0, -1, 0, 2])
	[{'data': [0, 0, -1, 0], 'sign': -1}]
	>>> sign_chunker([5, -5], include_last = True)
	[{'data': [5],  'sign':  1},
	 {'data': [-5], 'sign': -1}]
	>>> sign_chunker([], include_last = True)
	[]
	"""
	if return_data == None:
		return_data = data

	chunks = []

	begin_index = 0
	cur_sign = 0
	last_sign = 0

	for x in range(len(data)):
		cur_sign = sign(data[x], zero = last_sign)

		if cur_sign != last_sign:
			if last_sign != 0:
				chunks.append({
					'sign': -cur_sign,
					'data': return_data[begin_index:x],
				})
				begin_index = x
			last_sign = cur_sign

	if include_last and len(data) > 0:
		chunks.append({
			'sign': cur_sign,
			'data': return_data[begin_index:]
		})

	return chunks

if __name__ == '__main__':
	import doctest
	doctest.testmod(optionflags = doctest.NORMALIZE_WHITESPACE)
