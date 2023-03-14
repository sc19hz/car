
from agents.navigation.basic_agent import BasicAgent
import math
from numpy import random
from queue import Queue
from queue import Empty
import carla
import random
import time
import cv2
import logging
def setRotation(target_point , vehicle_location):
    # 计算目标点与小车初始位置之间的方向向量
    direction_vector = target_point - vehicle_location
    direction_vector = direction_vector / math.sqrt(
        direction_vector.x ** 2 + direction_vector.y ** 2 + direction_vector.z ** 2)

    # 将小车的初始方向设置为目标点与小车初始位置之间的方向向量

    rot= carla.Rotation(yaw=math.degrees(math.atan2(direction_vector.y, direction_vector.x)))
    return rot
def main():
    actor_list = []
    sensor_list = []
    try:
        # 首先，我们需要创建发送请求的客户端
        client = carla.Client('localhost', 2000)
        client.set_timeout(8.0)
        # 检索当前正在运行的世界
        world = client.load_world('Town02')
        map = world.get_map()
        blueprint_library = world.get_blueprint_library()
        #灯
        traffic_lights = world.get_actors().filter('traffic.traffic_light')

        #产生点
        #spawn_points = map.get_spawn_points()
        #spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
        startpoint=carla.Location(x=100, y=305, z=5)
        destination_point = carla.Location(x=150, y=305, z=2)
        startRotation=setRotation(destination_point,startpoint)
        spawn_point = carla.Transform(carla.Location(x=100, y=305, z=5), startRotation)
        # 创建车辆
        vehicle_bp = blueprint_library.find('vehicle.tesla.model3')
        vehicle_bp.set_attribute('role_name', 'autopilot')

        vehicle = world.spawn_actor(vehicle_bp, spawn_point)
        vehicle.set_autopilot(False)
        actor_list.append(vehicle)
        #构造自动驾驶的agent
        #设置目标点
        agent = BasicAgent(vehicle, target_speed=100)

        destination = carla.Transform(destination_point, carla.Rotation())
        destination_location = (destination.location.x, destination.location.y, destination.location.z)
        agent.set_destination(destination_location)
        # 添加相机
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        # 与车辆相关的摄像头相对位置
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        sensor_list.append(camera)

        prex=0
        prey=0
        while True:
            #agent.update_information()
            for traffic_light in traffic_lights:
                traffic_light.set_state(carla.TrafficLightState.Green)
            control = agent.run_step()

            vehicle.apply_control(control)
            spectator = world.get_spectator()
            transform=vehicle.get_transform()
            spectator.set_transform(carla.Transform(transform.location + carla.Location(z=20),
                                                    carla.Rotation(pitch=-90)))
            if (prex!=round(transform.location.x) or prey!=round(transform.location.y)):
                print(f'{round(transform.location.x)},{round(transform.location.y)}')
            prex=round(transform.location.x)
            prey = round(transform.location.y)

            # if (abs(transform.location.x-destination.location.x)<=10 and abs(transform.location.y-destination.location.y)<=10):
            #     print("finished")
            #     time.sleep(10)
            #     break;

    finally:
        print('destroying actors')
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
        for sensor in sensor_list:
            sensor.destroy()
        print('done.')
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(' - Exited by user.')