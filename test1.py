import carla
import numpy
import numpy as np
from newmap import GetMap
dotmap = np.zeros((350, 350))
# Connect to the Carla server
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Load the desired map
world = client.load_world('Town02')
mpt=GetMap(world)
coords=mpt.get_map_matrix()

for coord in coords:
    a=coord[0]
    b=coord[1]
    dotmap[a][b]=1
print(dotmap)