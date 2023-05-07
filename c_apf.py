import carla
import numpy as np
import time

# APF参数
K_att = 0.5
K_rep = 2000.0
d0 = 5.0

# 连接Carla服务器
client = carla.Client("localhost", 2000)
client.set_timeout(5.0)

# 获取世界对象
world = client.get_world()

# 获取车辆蓝图
blueprint_library = world.get_blueprint_library()
vehicle_bp = blueprint_library.filter("vehicle.*")[0]

# 设置起点和终点
spawn_point = carla.Transform(carla.Location(x=100, y=305, z=5))
spawn_point2=carla.Transform(carla.Location(x=150, y=305, z=5))
destination = carla.Location(x=200, y=305, z=2)

# 创建车辆
vehicle = world.spawn_actor(vehicle_bp, spawn_point)
vehicle2=world.spawn_actor(vehicle_bp, spawn_point2)
# 势场计算函数
def potential_field(position, destination, obstacles):
    att_force = K_att * (destination - position)
    rep_force = np.zeros(2)

    for obs in obstacles:
        obs_vec = position - obs
        distance = np.linalg.norm(obs_vec)

        if distance <= d0:
            rep_force += (K_rep * (1 / distance - 1 / d0) * (1 / (distance ** 2)) * (obs_vec / distance))

    total_force = att_force + rep_force
    return total_force

# 获取动态障碍物的位置
def get_dynamic_obstacles_positions(world):
    obstacles = []
    for actor in world.get_actors():
        if actor.type_id.startswith("vehicle.") or actor.type_id.startswith("walker."):
            location = actor.get_location()
            if actor.id != vehicle.id:
                obstacles.append(np.array([location.x, location.y]))
    return obstacles

# 控制车辆移动
while True:
    vehicle_pos = np.array([vehicle.get_location().x, vehicle.get_location().y])
    destination_np = np.array([destination.x, destination.y])

    # 获取动态障碍物
    obstacles = get_dynamic_obstacles_positions(world)

    # 计算合成势场
    force = potential_field(vehicle_pos, destination_np, obstacles)

    # 计算速度和方向
    speed = np.linalg.norm(force)
    direction = np.arctan2(force[1], force[0]) - vehicle.get_transform().rotation.yaw * np.pi / 180.0

    # 将速度和方向设置为车辆控制命令
    control = carla.VehicleControl()
    control.throttle = min(speed / 10, 1)
    control.steer = np.clip(direction, -1, 1)
    vehicle.apply_control(control)

    # 判断是否到达目标
    if np.linalg.norm(vehicle_pos - destination_np) < 2.0:
        print("到达目标！")
        break

    # 暂停以允许模拟更新
    time.sleep(0.1)
