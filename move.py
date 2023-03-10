
from agents.navigation.basic_agent import BasicAgent
from numpy import random
from queue import Queue
from queue import Empty
import carla
import random
import time
import cv2
import logging
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
        #产生点
        #spawn_points = map.get_spawn_points()
        #spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()

        spawn_point = carla.Transform(carla.Location(x=100, y=305, z=5), carla.Rotation())
        # 创建车辆
        vehicle_bp = blueprint_library.find('vehicle.tesla.model3')
        vehicle_bp.set_attribute('role_name', 'autopilot')

        vehicle = world.spawn_actor(vehicle_bp, spawn_point)
        vehicle.set_autopilot(True)
        actor_list.append(vehicle)
        #构造自动驾驶的agent
        #设置目标点
        agent = BasicAgent(vehicle, target_speed=30)
        destination_point=carla.Location(x=150, y=150, z=2)
        destination = carla.Transform(destination_point, carla.Rotation(yaw=180))
        destination_location = (destination.location.x, destination.location.y, destination.location.z)
        agent.set_destination(destination_location)
        # 添加相机
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        # 与车辆相关的摄像头相对位置
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        sensor_list.append(camera)


        while True:
            #agent.update_information()
            control = agent.run_step()

            vehicle.apply_control(control)
            spectator = world.get_spectator()
            transform=vehicle.get_transform()
            spectator.set_transform(carla.Transform(transform.location + carla.Location(z=20),
                                                    carla.Rotation(pitch=-90)))
            # if transform.location.x==destination.location.x:
            #     pass

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