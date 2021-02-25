from readgadget import readsnap
from astropy.cosmology import FlatLambdaCDM

sim =  caesar.load(data_dir+'Groups/'+model+'_'+snap+'.hdf5', LoadHalo=False)

h = sim.simulation.hubble_constant
redshift = sim.simulation.redshift
cosmo = FlatLambdaCDM(H0=100*h, Om0=sim.simulation.omega_matter, Ob0=sim.simulation.omega_baryon, Tcmb0=2.73)
thubble = cosmo.age(redshift).value # in Gyr


star_tform = readsnap(snapfile, 'age', 'star', suppress=1, units=1) # expansion times at time of formation

tform = star_tform[slist]
ages = tage(cosmo, thubble, tform) * 1000. # get star ages in Myr
