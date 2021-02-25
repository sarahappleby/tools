import numpy as np


def read_data(filename):

    data = np.genfromtxt(filename,names=True,dtype=None) #dtype=None to be able to read mixed data types form the file
    return data

def recentre_pos(x,y,z,mass,r_max):
    """compute center of mass within r_max and recentre
    """
    mask = (x**2 + y**2 + z**2) < r_max**2
    mass_tot = np.sum(mass[mask])
    x_cm = np.sum(x[mask]*mass[mask])/mass_tot
    y_cm = np.sum(y[mask]*mass[mask])/mass_tot
    z_cm = np.sum(z[mask]*mass[mask])/mass_tot
    return x-x_cm,y-y_cm,z-z_cm

def recentre_pos_and_vel(x,y,z,vx,vy,vz,mass,r_max):
    """compute center of mass and mass weighted velocity center within r_max and recentre position and velocity
    """
    mask = (x**2 + y**2 + z**2) < r_max**2
    mass_tot = np.sum(mass[mask])
    x_cm = np.sum(x[mask]*mass[mask])/mass_tot
    y_cm = np.sum(y[mask]*mass[mask])/mass_tot
    z_cm = np.sum(z[mask]*mass[mask])/mass_tot
    vx_cm = np.sum(vx[mask]*mass[mask])/mass_tot
    vy_cm = np.sum(vy[mask]*mass[mask])/mass_tot
    vz_cm = np.sum(vz[mask]*mass[mask])/mass_tot
    return x-x_cm,y-y_cm,z-z_cm,vx-vx_cm,vy-vy_cm,vz-vz_cm


def compute_rotation_to_vec(x,y,z,vx,vy,vz,mass,vec):
    """compute rotation axis and anglr to vector vec
    """
    Lxtot = np.sum(y*vz*mass - z*vy*mass)
    Lytot = np.sum(z*vx*mass - x*vz*mass)
    Lztot = np.sum(x*vy*mass - y*vx*mass)
    
    L = np.zeros(3)
    L = np.hstack([Lxtot,Lytot,Lztot])

    L = L/np.linalg.norm(L)
    vec = vec/np.linalg.norm(vec)
    
    axis = np.zeros(3)
    axis = np.cross(L,vec)
    axis = axis/np.linalg.norm(axis)

    c = np.dot(L,vec)                 # cosine of the angle
    angle = np.arccos(np.clip(c, -1, 1)) # angle between L and vec
    #@@@angle = np.arccos(c) # angle between L and vec

    return axis, angle


def rotate2(x,y,z,axis,angle):
    x_rot=x
    y_rot=y
    z_rot=z
    axisx=axis[0]*np.ones(len(x))
    axisy=axis[1]*np.ones(len(x))
    axisz=axis[2]*np.ones(len(x))

    dot=x*axisx+y*axisy+z*axisz

    crossx=axisy*z-axisz*y
    crossy=axisz*x-axisx*z
    crossz=axisx*y-axisy*x

    cosa=np.cos(angle)
    sina=np.sin(angle)

    x_rot=x*cosa+crossx*sina+axis[0]*dot*(1-cosa)
    y_rot=y*cosa+crossy*sina+axis[1]*dot*(1-cosa)
    z_rot=z*cosa+crossz*sina+axis[2]*dot*(1-cosa)
   
    return x_rot,y_rot,z_rot

def rotate(x,y,z,axis,angle):
    mat_rot_x = np.array([np.cos(angle)+axis[0]**2.*(1-np.cos(angle)),axis[0]*axis[1]*(1-np.cos(angle))-axis[2]*np.sin(angle),axis[0]*axis[2]*(1-np.cos(angle))+axis[1]*np.sin(angle)]) 
    mat_rot_y = np.array([axis[1]*axis[0]*(1-np.cos(angle))+axis[2]*np.sin(angle),np.cos(angle)+axis[1]**2.*(1-np.cos(angle)),axis[1]*axis[2]*(1-np.cos(angle))-axis[0]*np.sin(angle)]) 
    mat_rot_z = np.array([axis[2]*axis[0]*(1-np.cos(angle))-axis[1]*np.sin(angle),axis[2]*axis[1]*(1-np.cos(angle))+axis[2]*np.sin(angle),np.cos(angle)+axis[2]**2.*(1-np.cos(angle))]) 

    x_rot = mat_rot_x[0]*x + mat_rot_x[1]*y +mat_rot_x[2]*z
    y_rot = mat_rot_y[0]*x + mat_rot_y[1]*y +mat_rot_y[2]*z
    z_rot = mat_rot_z[0]*x + mat_rot_z[1]*y +mat_rot_z[2]*z

    return x_rot,y_rot,z_rot

def fit_exp(x, a, b):
   return a * np.exp(-b * x)

def fit_vac(x, a, b, r0):
    return a * np.exp(-b*(x/r0)**0.25)    

def fit_sersic(x, a, b, r0, n):
    return a * np.exp(-b*(x/r0)**(1./n))

def fit_exp_sersic(x, a1, b1, a2, b2, r0, n):
    return a1 * np.exp(-b1 * x) + a2 * np.exp(-b2*(x/r0)**(1./n))

def fit_exp_vac(x, a1, b1, a2, b2, r0):
    return a1 * np.exp(-b1 * x) + a2 * np.exp(-b2*(x/r0)**0.25)
