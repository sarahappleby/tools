import h5py
import numpy as np
import os
import caesar

mufasa_snaps = ['070', '085', '095', '105', '125', '126', '135']
simba_snaps = ['078', '090', '105', '125', '145', '151']
simba_snaps = ['078']

data_dir = '/home/sapple/simba_sizes/data/'

model = 'm100n1024'
simba = 's50j7k'
"""
for snap in mufasa_snaps:
        sim = caesar.load('/home/rad/data/'+model+'/fh_qr/Groups/'+model+'_'+snap+'.hdf5')
        #sfr = np.array([i.sfr for i in sim.galaxies])
	#s_mass = np.array([i.masses['stellar'] for i in sim.galaxies])
	central = np.asarray([i.central for i in sim.galaxies])
	#r_l = np.load(data_dir+'halflight_'+model+'_fh_qr_'+snap+'.npy')
        #r_m = np.load(data_dir+'halfmass_'+model+'_fh_qr_'+snap+'.npy')

        with h5py.File(data_dir+model+'_fh_qr_'+snap+'_data.h5', 'a') as hf:
                #hf.create_dataset('sfr', data=np.array(sfr))
		#hf.create_dataset('stellar_mass', data=np.array(s_mass))
		#hf.create_dataset('halflight', data=np.array(r_l))
                #hf.create_dataset('halfmass', data=np.array(r_m))
		hf.create_dataset('central', data=np.array(central))
"""

for snap in simba_snaps:
	sim = caesar.load('/home/rad/data/'+model+'/'+simba+'/Groups/'+model+'_'+snap+'.hdf5')
	s_mass = np.array([i.masses['stellar'] for i in sim.galaxies])
	sfr = np.array([i.sfr for i in sim.galaxies])
	central = np.asarray([i.central for i in sim.galaxies])
	r_l = np.load(data_dir+'halflight_'+model+'_'+simba+'_'+snap+'.npy')
        r_m = np.load(data_dir+'halfmass_'+model+'_'+simba+'_'+snap+'.npy')

	with h5py.File(data_dir+model+'_'+simba+'_'+snap+'_data.h5', 'a') as hf:
		hf.create_dataset('sfr', data=np.array(sfr))
		hf.create_dataset('stellar_mass', data=np.array(s_mass))
                hf.create_dataset('halflight', data=np.array(r_l))
                hf.create_dataset('halfmass', data=np.array(r_m))
		hf.create_dataset('central', data=np.array(central))
