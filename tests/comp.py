resFiles = ['tests/res1.txt', 
			'tests/res2.txt', 
			'tests/res3.txt']
refFiles = ['./test-files/results1.txt', 
			'./test-files/results2.txt', 
			'./test-files/results3.txt']

for f in range(3):
	print('Round {}.'.format(f+1))
	resFile = resFiles[f]
	refFile = refFiles[f]

	with open(resFile, 'r') as res:
		resLines = res.readlines()
		res.close()

	with open(refFile, 'r') as res:
		refLines = res.readlines()
		res.close()

	# counter = 1
	for i in range(len(refLines)):
		if resLines[i] != refLines[i]:
			print('Line {}: res[{}] != ref[{}]'.format(i, resLines[i].strip(), refLines[i].strip()))
	print('Pass!\n')
