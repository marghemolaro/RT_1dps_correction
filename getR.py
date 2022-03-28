import numpy as np
from scipy import interpolate

#------------------------------------
#Routine to calculate the patchy correction R_zR(z_dash,k) as defined in Eqn. 2, Molaro et al. in prep, for EoR history models ending at redshift zR (defined as redshift at which the neutral hydrogen fraction first falls below 10^-3) in observational redshift bin z_dash
#User-defined parameters: Range of EoR history models zR for which R_zR(z_dash,k) is calculated can be selected through the user-defined range limits and interval zRmin, zRmax, and dzR respectively, while k values at which R_zR(z_dash,k) is calculated can be selected using logkmin, logkmax, and dlogk. Ranges of zR and logk for which this approximation safely holds are 5.3<=zR<=6.7 and -2.9<=log10k<=-0.7 (see Molaro et al. in prep for further details). 
#Outputs: 
#log10k_range.dat: log10k values considered:
#zR_range.dat: zR models considered;  
#R_correction.dat: R_zR(z_dash,k) values, with each column referring to values for a different zR model;

#If you use this script for your scientific work, we kindly ask you to please reference: Molaro et al. in prep (https://arxiv.org/abs/2109.06897) 

#User-defined parameters
z_dash 	= 5 #Observational redshift bin
zRmin 	= 6.0 #Minimum zR considered
zRmax 	= 6.3 #Maximum zR considered
dzR 	= 0.1 #Interval at which zR models are selected in zR range
logkmin = -2.35 #Minimum log10k considered 
logkmax = -1.25 #Maximum log10k considered
dlogk 	= 0.1 #Interval at which k values are selected in log10k range
#------------------------------------

#Check user parameter range
if zRmin < 5.3 or zRmax < 5.3 or zRmin > 6.7 or zRmax >  6.7:
	print("WARNING: Extrapolating outside of zR range")

#Convert to arrays
NzR		= 1+int((zRmax - zRmin)/dzR)
Nlogk		= 1+int((1000.*logkmax - 1000.*logkmin)/(1000.*dlogk))
zR       	= np.linspace(zRmin,zRmax,NzR, endpoint=True)
logk_out 	= np.linspace(logkmin,logkmax,Nlogk, endpoint=True)

# log10(k) and z coordinates used in Table 2
X = np.linspace(4.1,5.4,14,endpoint=True)
Y = np.linspace(-2.9,-0.7,23,endpoint=True)
x,y = np.meshgrid(X,Y)
R = np.array([[	1.10912, 1.12574, 1.14715, 1.16714, 1.19071, 1.23308, 1.26416, 1.29471, 1.32443, 1.35452, 1.39394, 1.43150, 1.46571, 1.50668],
  [ 1.09169, 1.10540, 1.12236, 1.13833, 1.15698, 1.18211, 1.20497, 1.22800, 1.25009, 1.27185, 1.30036, 1.32809, 1.35318, 1.38304],
  [ 1.07316, 1.08382, 1.09613, 1.10798, 1.12157, 1.13862, 1.15470, 1.17159, 1.18748, 1.20257, 1.22232, 1.24216, 1.25991, 1.28090],
  [ 1.05679, 1.06498, 1.07371, 1.08250, 1.09234, 1.10384, 1.11566, 1.12830, 1.14026, 1.15172, 1.16712, 1.18325, 1.19828, 1.21642],
  [ 1.04749, 1.05457, 1.06150, 1.06818, 1.07524, 1.08495, 1.09483, 1.10345, 1.11221, 1.12152, 1.13506, 1.14909, 1.16268, 1.17976],
  [ 1.03916, 1.04507, 1.05044, 1.05550, 1.06096, 1.06884, 1.07687, 1.08412, 1.09235, 1.10084, 1.11335, 1.12593, 1.13872, 1.15346],
  [ 1.03214, 1.03671, 1.04058, 1.04434, 1.04872, 1.05392, 1.05942, 1.06571, 1.07251, 1.07869, 1.08780, 1.09668, 1.10535, 1.11666],
  [ 1.02688, 1.02905, 1.03060, 1.03283, 1.03501, 1.03775, 1.04116, 1.04507, 1.04953, 1.05417, 1.06157, 1.07122, 1.08058, 1.09328],
  [ 1.02082, 1.02325, 1.02456, 1.02651, 1.02794, 1.02942, 1.03202, 1.03504, 1.03795, 1.04002, 1.04452, 1.05122, 1.05955, 1.07140],
  [ 1.01856, 1.02016, 1.02147, 1.02274, 1.02467, 1.02548, 1.02773, 1.03025, 1.03311, 1.03577, 1.04033, 1.04725, 1.05504, 1.06438],
  [ 1.01498, 1.01571, 1.01662, 1.01799, 1.01873, 1.01977, 1.02254, 1.02443, 1.02685, 1.03077, 1.03632, 1.04330, 1.04989, 1.05743],
  [ 1.01217, 1.01405, 1.01497, 1.01653, 1.01828, 1.02081, 1.02301, 1.02447, 1.02425, 1.02449, 1.02703, 1.03328, 1.04078, 1.05185],
  [ 1.01167, 1.01233, 1.01392, 1.01569, 1.01705, 1.01731, 1.01782, 1.01974, 1.02449, 1.02834, 1.03189, 1.03837, 1.04821, 1.06228],
  [ 1.00941, 1.01082, 1.01255, 1.01443, 1.01712, 1.01866, 1.02016, 1.02073, 1.02244, 1.02416, 1.02625, 1.03145, 1.03781, 1.04733],
  [ 1.00337, 1.00384, 1.00520, 1.00690, 1.00999, 1.01183, 1.01431, 1.01511, 1.01850, 1.02315, 1.02834, 1.03497, 1.04191, 1.04999],
  [ 0.989389, 0.990349, 0.993301, 0.995784, 0.998043, 1.00077, 1.00307, 1.00317, 1.00695, 1.01288, 1.01762, 1.02425, 1.03085, 1.03564],
  [ 0.974580, 0.975293, 0.976186, 0.978158, 0.978790, 0.980251, 0.983049, 0.987076, 0.990957, 0.993502, 0.995111, 0.998664, 1.00275, 1.01124],
  [ 0.945941, 0.948871, 0.954222, 0.954665, 0.956260, 0.959815, 0.963778, 0.967657, 0.968394, 0.971948, 0.975906, 0.977863, 0.983393, 0.992043],
  [ 0.923842, 0.923357, 0.923680, 0.923106, 0.929661, 0.934573, 0.938455, 0.939623, 0.940766, 0.946125, 0.949797, 0.954328, 0.959693, 0.965907],
  [ 0.908901, 0.908871, 0.907347, 0.910547, 0.924120, 0.918598, 0.921065, 0.920659, 0.928884, 0.927596, 0.927254, 0.923673, 0.930919, 0.935438],
  [ 0.907836, 0.913351, 0.914918, 0.916223, 0.921810, 0.917193, 0.919275, 0.914920, 0.915018, 0.913759, 0.906307, 0.909118, 0.913770, 0.913555],
  [ 0.899729, 0.913425, 0.912138, 0.909014, 0.912819, 0.912620, 0.903737, 0.903384, 0.908673, 0.904995, 0.900418, 0.886183, 0.883490, 0.884748],
  [ 0.869178, 0.861596, 0.876427, 0.869691, 0.877194, 0.878800, 0.882308, 0.885625, 0.883147, 0.883400, 0.881848, 0.877351, 0.868798, 0.864382]])

f=interpolate.interp2d(x,y,R,kind='linear') #Default is linear, change if required

#Calculate z_mid using Eqn. 3 
z_mid = [0]*NzR
for i in range(NzR):
	z_mid[i] = z_dash - 0.390*zR[i]+2.31

Ru = f(z_mid,logk_out)
print(Ru)

R_file = open("R_correction.dat", "w")
k_file = open("log10k_range.dat", "w")
zR_file = open("zR_range.dat", "w")
np.savetxt(k_file, logk_out, delimiter=' ',newline='\n ', fmt='%1.3f')
np.savetxt(zR_file, zR, delimiter=' ',newline='\n ', fmt='%1.3f')
np.savetxt(R_file, Ru,delimiter=' ',newline='\n ', fmt='%1.3f')
R_file.close()
k_file.close()
zR_file.close()


