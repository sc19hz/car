import carla
import numpy as np
from newmap import GetMap
from Apath import GetPath
from Graph import View
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
with open("my_file.txt", "w") as file:
    # 将数组写入文件
    for row in coords:
        file.write(" ".join([str(elem) for elem in row]) + "\n")
start=[129,188]
end=[135,192]
# path=GetPath.getPath(coords,start,end)

# print(path)
View.view(coords)