import h5py

def save_h5(data, labels, filename):
	"""
	Save data in h5py .h5 format
	Args: 
		data(ndarray): array of data arrays to write to file.
		labels(list of strings): names of variables, used to label data arrays
		filename(str): name of .h5 file
	e.g. 
		data = array([[x1, x2, x3, ...], 
			      [y1, y2, y3, ...], ...])
		labels = ['x', 'y', ...]
	"""
	with h5py.File('{}.h5'.format(filename), 'w') as f:
		for i in range(len(data)):
			f.create_dataset(labels[i], data=np.array(data[i]))
	print('Data saved as '+ filename)
	return
	
