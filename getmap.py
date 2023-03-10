import carla

# Connect to the Carla server
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Load the desired map
world = client.load_world('Town02')
carla_map = world.get_map()

# Get all waypoints in the map
waypoints = carla_map.generate_waypoints(distance=2.0)

# Find all junctions in the map
junctions = []
for waypoint in waypoints:
    if waypoint.is_junction:
        junctions.append(waypoint)

# Get the coordinates of all junctions
junction_coords = []
for junction in junctions:
    junction_location = junction.transform.location
    junction_x = junction_location.x
    junction_y = junction_location.y
    junction_z = junction_location.z
    junction_coords.append((junction_x, junction_y, junction_z))

print(junction_coords)
