import carla

# Connect to the Carla server

class GetMap():
    def __init__(self,world):
        self.world=world



    def get_map_matrix(self):
        carla_map = self.world.get_map()
        waypoints = carla_map.generate_waypoints(distance=2.0)
        junctions = []
        for waypoint in waypoints:
            if waypoint.is_junction:
                junctions.append(waypoint)
        junction_coords = []
        for junction in junctions:
            junction_location = junction.transform.location
            junction_x = round(junction_location.x)
            junction_y = round(junction_location.y)
            junction_coords.append((junction_x, junction_y))

        return junction_coords
