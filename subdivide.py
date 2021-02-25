import numpy as np

def variance_jk(samples, mean):
        n = len(samples)
        factor = (n-1.)/n
        x = np.nansum((np.subtract(samples, mean))**2, axis=0)
        x *= factor
        return x

def octants(pos_array, boxsize):
    pos_x = (pos_array[:, 0] < boxsize*0.5); pos_y = (pos_array[:, 1] < boxsize*0.5); pos_z = (pos_array[:, 2] < boxsize*0.5)
    inds_1 = np.array([]); inds_2 = np.array([]); inds_3 = np.array([]); inds_4 = np.array([]) 
    inds_5 = np.array([]); inds_6 = np.array([]); inds_7 = np.array([]); inds_8 = np.array([])

    for i in range(len(pos_array)):
                if (pos_x[i] and pos_y[i] and pos_z[i]):
                        inds_1 = np.append(inds_1, i)
                elif (pos_x[i] and pos_y[i] and not pos_z[i]):
                        inds_2 = np.append(inds_2, i)
                elif (pos_x[i] and not pos_y[i] and pos_z[i]):
                        inds_3 = np.append(inds_3, i)
                elif (pos_x[i] and not pos_y[i] and not pos_z[i]):
                        inds_4 = np.append(inds_4, i)
                elif (not pos_x[i] and pos_y[i] and pos_z[i]):
                        inds_5 = np.append(inds_5, i)
                elif (not pos_x[i] and pos_y[i] and not pos_z[i]):
                        inds_6 = np.append(inds_6, i)
                elif (not pos_x[i] and not pos_y[i] and pos_z[i]):
                        inds_7 = np.append(inds_7, i)
                elif (not pos_x[i] and not pos_y[i] and not pos_z[i]):
                        inds_8 = np.append(inds_8, i)

    return np.array((inds_1, inds_2, inds_3, inds_4, inds_5, inds_6, inds_7, inds_8))


def octants_masters(pos_array, x_y, boxsize):
	x = x_y[0]; y = x_y[1]
	pos_x = (pos_array[:, 0] < boxsize*0.5); pos_y = (pos_array[:, 1] < boxsize*0.5); pos_z = (pos_array[:, 2] < boxsize*0.5)

	pos_1 = []; pos_2 = []; pos_3 = []; pos_4 = []; pos_5 = []; pos_6 = []; pos_7 = []; pos_8 = []
	x_1 = []; x_2 = []; x_3 = []; x_4 = []; x_5 = []; x_6 = []; x_7 = []; x_8 = []
	y_1 = []; y_2 = []; y_3 = []; y_4 = []; y_5 = []; y_6 = []; y_7 = []; y_8 = []	

	for i in range(len(pos_array)):
		if (pos_x[i] and pos_y[i] and pos_z[i]):
			pos_1.append(pos_array[i])
			x_1.append(x[i])
			y_1.append(y[i])
		elif (pos_x[i] and pos_y[i] and not pos_z[i]):
			pos_5.append(pos_array[i])
			x_5.append(x[i])
			y_5.append(y[i])
		elif (pos_x[i] and not pos_y[i] and pos_z[i]):
			pos_3.append(pos_array[i])
			x_3.append(x[i])
			y_3.append(y[i])
		elif (pos_x[i] and not pos_y[i] and not pos_z[i]):
			pos_7.append(pos_array[i])
			x_7.append(x[i])
			y_7.append(y[i])
		elif (not pos_x[i] and pos_y[i] and pos_z[i]):
			pos_2.append(pos_array[i])
			x_2.append(x[i])
			y_2.append(y[i])
		elif (not pos_x[i] and pos_y[i] and not pos_z[i]):
			pos_6.append(pos_array[i])
			x_6.append(x[i])
			y_6.append(y[i])
		elif (not pos_x[i] and not pos_y[i] and pos_z[i]):
			pos_4.append(pos_array[i])
			x_4.append(x[i])
			y_4.append(y[i])
		elif (not pos_x[i] and not pos_y[i] and not pos_z[i]):
			pos_8.append(pos_array[i])
			x_8.append(x[i])
			y_8.append(y[i])

	positions = np.array((np.array(pos_1), np.array(pos_2), np.array(pos_3), np.array(pos_4), 
							np.array(pos_5), np.array(pos_6), np.array(pos_7), np.array(pos_8)))
	x_new = np.array((np.array(x_1), np.array(x_2), np.array(x_3), np.array(x_4), 
								np.array(x_5), np.array(x_6), np.array(x_7), np.array(x_8)))
	y_new = np.array((np.array(y_1), np.array(y_2), np.array(y_3), np.array(y_4), 
								np.array(y_5), np.array(y_6), np.array(y_7), np.array(y_8)))

	return positions, [x_new, y_new]	

def jackknife_masters(pos_array, mass_array, y, boxsize, mass_bins, std=False):

	pos_octs, var_octs = octants_masters(pos_array, [mass_array, y], boxsize)
	mass_octs = var_octs[0]; y_octs = var_octs[1]
	del var_octs

	y_curves = np.zeros((8, len(mass_bins) -1))
	y_std = np.zeros((8, len(mass_bins) -1))
	y_25 = np.zeros((8, len(mass_bins) -1))
	y_75 = np.zeros((8, len(mass_bins) -1))

	for i in range(8):
		mass_using = np.concatenate(np.delete(mass_octs, i))
		y_using = np.concatenate(np.delete(y_octs, i))

		digitized = np.digitize(mass_using, mass_bins)
		binned_y = [y_using[digitized == j] for j in range(1, len(mass_bins))]

		for j in range(len(mass_bins) -1):
			y_curves[i][j] = np.median(binned_y[j])
			y_std[i][j] = np.std(binned_y[j])
			try:
				y_25[i][j] = np.percentile(binned_y[j], 25)
				y_75[i][j] = np.percentile(binned_y[j], 75)
			except IndexError:
				y_25[i][j] = np.nan
				y_75[i][j] = np.nan

	y_mean = np.nanmean(y_curves, axis=0)
	y_std_mean = np.nanmean(y_std, axis=0)
	y_25_mean = np.nanmean(y_25, axis=0)
	y_75_mean = np.nanmean(y_75, axis=0)

	nan_mask = np.logical_not(np.isnan(y_mean))
	mid_bins = np.array([(mass_bins[a] + mass_bins[a+1])/2 for a in range(0, len(mass_bins) -1)])
	mid_bins = mid_bins[nan_mask]
	y_curves = np.transpose(y_curves)[nan_mask]
	y_mean = y_mean[nan_mask]
	y_std_mean = y_std_mean[nan_mask]
	y_25_mean = y_25_mean[nan_mask]
	y_75_mean = y_75_mean[nan_mask]

	nonzero_indices = np.nonzero(y_mean)
	mid_bins = mid_bins[nonzero_indices]
	y_curves = np.transpose(y_curves[nonzero_indices])
	y_mean = y_mean[nonzero_indices]
	y_std_mean = y_std_mean[nonzero_indices]
	y_25_mean = y_25_mean[nonzero_indices]
	y_75_mean = y_75_mean[nonzero_indices]	

	y_var = variance_jk(y_curves, y_mean)

	if not std:
		return mid_bins, y_mean, y_var
	elif std:
		return mid_bins, y_mean, y_var, [y_std_mean, y_25_mean, y_75_mean]
