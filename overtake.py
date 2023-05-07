import carla
import random
import time
from simple_pid import PID

# PID控制器参数
kp = 1.0
ki = 0.0
kd = 0.0

def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    world = client.get_world()

    blueprint_library = world.get_blueprint_library()

    vehicle_bp = blueprint_library.find('vehicle.tesla.model3')

    spawn_point = carla.Transform(carla.Location(x=100, y=305, z=5), carla.Rotation())
    spawn_point_1 = carla.Transform(carla.Location(x=150, y=305, z=5), carla.Rotation())

    vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    vehicle2 = world.spawn_actor(vehicle_bp, spawn_point_1)

    # 获取并设置 TrafficManager
    traffic_manager = client.get_trafficmanager(8000)
    traffic_manager.global_percentage_speed_difference(0)  # 设置百分比速度差，0 表示正常驾驶模式

    vehicle.set_autopilot(True, tm_port=8000)

    # 创建一个PID控制器来控制车辆的转向
    pid = PID(kp, ki, kd, setpoint=0)

    def on_tick(tick_event):
        # 获取车辆当前位置和方向
        vehicle_location = vehicle.get_location()
        vehicle_yaw = vehicle.get_transform().rotation.yaw

        # 获取前方车辆的位置
        target_location = None
        for other_vehicle in world.get_actors().filter("vehicle.*"):
            if other_vehicle.id != vehicle.id and vehicle_location.distance(other_vehicle.get_location()) < 100:
                target_location = other_vehicle.get_location()
                break

        if target_location is not None:
            # 计算车辆与前方车辆之间的角度差
            relative_location = target_location - vehicle_location
            angle = vehicle_yaw - relative_location.rotation.yaw
            error = (angle + 180) % 360 - 180
        else:
            error = 0        # 使用PID控制器计算转向
        steering = pid(error)

        # 控制车辆
        control = carla.VehicleControl(throttle=0.5, brake=0.0, steer=steering)
        vehicle.apply_control(control)

    world.on_tick(on_tick)

    try:
        time.sleep(60)  # 让车辆在模拟器中行驶 60 秒
    finally:
        vehicle.destroy()

if __name__ == '__main__':
    main()
