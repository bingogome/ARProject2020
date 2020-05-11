# ARProject2020

This project is the course project repository for Augmented Reality at JHU 2020. Author: Yihao Liu

Code structure:

1.0 clientUnity

The visualization. Contains the Unity assets, project settings and packages.

2.0 serverPython

The server written in Python. Communicate with the Unity client using UDP.

	2.1 main.py The main procedure script.
	
		Some default option so that the user can use the data existing.
		loadCalibratedPointer = True
		loadCalibratedHemo = True
		loadCalibratedSkull = True
		loadCollectedImplant = True
		pathMeshFile = 'data/skullRimLeftHand.sur'
		quatSkull = np.array([-0.7071068, 0.0000000, 0.0000000, 0.7071068])
		posSkull = 1000 * np.array([-0.0330000, -0.0658000, -0.0580000])
		quatImplant = np.array([-0.4427488, -0.0442963, 0.1601198, 0.8811204])
		posImplant = 1000 * np.array([-0.0209000, 0.0522000, -0.0153000])

	2.2 util folder. The helper functions.

		2.2.1 octree folder. The data structure script
		2.2.2 polarisUtilityScript.py The customized Polaris interface

	2.3 dataReadHanding.py The data handling script

	2.4 share/roms folder. The .rom definition files for Polaris tracked markers.

	2.5 data folder. The generated data and model place.