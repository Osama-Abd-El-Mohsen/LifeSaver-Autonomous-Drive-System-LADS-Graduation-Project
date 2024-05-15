import random
import numpy as np
import cv2
import sys
import keyboard
import carla
import math as mt

############################################################################
########################### Import basic agent #############################
############################################################################
sys.path.insert(0, 'C:\\CARLA_0.9.14\\WindowsNoEditor\\PythonAPI\\carla')
from agents.navigation.basic_agent import BasicAgent


############################################################################
############################### Global Var #################################
############################################################################
hospitals_locations = []
AllSpawndVechilesPositions = []
near_location = []
banned_vehciles = ['vehicle.carlamotors.carlacola','vehicle.tesla.cybertruck','vehicle.carlamotors.european_hgv','vehicle.carlamotors.firetruck','vehicle.mercedes.sprinter','vehicle.volkswagen.t2','vehicle.volkswagen.t2_2021','vehicle.mitsubishi.fusorosa','vehicle.ford.ambulance']
ego_vehicle=''
ego_vehicle_pos=''


############################################################################
############################ Hosbitals Points ##############################
############################################################################
h1 = carla.Transform(carla.Location(x=325.489990, y=273.743317, z=0.300000))
h2 = carla.Transform(carla.Location(x=176.589493, y=123.749130, z=0.300000))
h3 = carla.Transform(carla.Location(x=307.398132, y=5.570724, z=0.300000))
h4 = carla.Transform(carla.Location(x=10.509980, y=190.429993, z=0.300000)) #carla.Rotation(0,90,0)



############################################################################
############################### Functions #################################
############################################################################
def spawn_traffic():
    for x in range(0,50):
        temp_loc = random.choice(spawn_points)
        temp_vech = random.choice(vehicle_blueprints)
        # print(temp_vech.id)

        while temp_loc not in AllSpawndVechilesPositions and  temp_vech.id not in banned_vehciles:
            AllSpawndVechilesPositions.append(temp_loc)
            world.try_spawn_actor(temp_vech,temp_loc)



def spawn_ego_vehicle():
    global ego_vehicle,ego_vehicle_pos
    try :
        ego_vehicle_pos =  random.choice(spawn_points)
        ego_vehicle = world.spawn_actor(vehicle_blueprints.find('vehicle.tesla.cybertruck'), ego_vehicle_pos)
        AllSpawndVechilesPositions.append(ego_vehicle_pos)

    except : 
        spawn_ego_vehicle()



def spawn_hosbitals():
    ambulance_bp  = vehicle_blueprints.find('vehicle.ford.ambulance')

    hospitals_locations.append(h1)
    hospitals_locations.append(h2)
    hospitals_locations.append(h3)
    hospitals_locations.append(h4)

    AllSpawndVechilesPositions.append(h1)
    AllSpawndVechilesPositions.append(h2)
    AllSpawndVechilesPositions.append(h3)
    AllSpawndVechilesPositions.append(h4)

    world.try_spawn_actor(ambulance_bp, h1)
    world.try_spawn_actor(ambulance_bp, h2)
    world.try_spawn_actor(ambulance_bp, h3)
    world.try_spawn_actor(ambulance_bp, h4)



def auto_pilot_vehicles_except_ego_and_embulance():
    for actor in world.get_actors().filter('*vehicle*'):
        if actor.id != ego_vehicle.id and actor.type_id != 'vehicle.ford.ambulance' :
            actor.set_autopilot(True)


def camera_callback(image,data_dict):
    data_dict["image"] = np.reshape(np.copy(image.raw_data),(image.height,image.width,4))




def get_nearest_hospital():
    near_location=[]
    ego_loc = ego_vehicle.get_location()
    # print(f"hospitals_locations = {hospitals_locations}")
    for index,location in enumerate(hospitals_locations) :
        temp_h = location.location
        # print(f"ego_loc-temp_h{index+1} = {ego_loc-temp_h}")
        near_location.append(mt.sqrt(((ego_loc-temp_h).x)**2 + ((ego_loc-temp_h).y)**2 ))
    # print(f'near_location = {near_location}')
    near_hos_loc = min(near_location)
    
    for index,loc in enumerate(near_location) :
        if near_hos_loc == near_location[index]:
            return index







############################################################################
###### Load Client,spawn_points,map,vehicle_blueprints and spectator #######
############################################################################
client = carla.Client("localhost",2000)
client.load_world("Town01")
world = client.get_world()
spectator = world.get_spectator()
vehicle_blueprints = world.get_blueprint_library().filter('*vehicle*')
spawn_points = world.get_map().get_spawn_points()




############################################################################
####################### Spawn Hosbitals ,ego,traffic #######################
############################################################################
spawn_hosbitals()
spawn_traffic()
spawn_ego_vehicle()

auto_pilot_vehicles_except_ego_and_embulance()

# changing spector camera position
ego_vehicle_pos.location.z = ego_vehicle_pos.location.z+2
spectator.set_transform(ego_vehicle_pos)
ego_vehicle.set_autopilot(True)

# Spawn Camera sensor and config
camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '640')
camera_bp.set_attribute('image_size_y', '360')
transform = carla.Transform(carla.Location(x=0.8, z=1.7))
caamera_sensor = world.spawn_actor(camera_bp, transform, attach_to=ego_vehicle)
image_w = camera_bp.get_attribute("image_size_x").as_int()
image_h = camera_bp.get_attribute("image_size_y").as_int()
camera_data = {"image" : np.zeros((image_h,image_w,4))}
caamera_sensor.listen(lambda image :camera_callback(image,camera_data))


# Create a basic agent for the ego vehicle
ego_agent = BasicAgent(ego_vehicle)
h4_location = carla.Location(x=10.509980, y=190.429993, z=0.300000)
ego_agent.set_destination(h1.location)


while True :
    img = camera_data["image"]
    cv2.imshow("RGB Cam",img)
    key = cv2.waitKey(1)
    if key == 27:
        cv2.destroyAllWindows()
        break

    if keyboard.is_pressed('p'):
        near_location = get_nearest_hospital()
        print('='*50)
        print(f"near_location index = {near_location}")
        print('='*50)
        # Set the destination to the h4 point
        print("p pressed")
        print(hospitals_locations[near_location].location)
        ego_agent.set_destination(hospitals_locations[near_location].location)
    ego_vehicle.apply_control(ego_agent.run_step())

    if ego_agent.done():
        from carla import VehicleControl
        # Assuming 'vehicle' is the ego vehicle actor
        control = VehicleControl()
        control.throttle = 0.5  # Example: 50% throttle
        control.brake = 1.0  # Example: no brake applied
        control.reverse = False
        # Apply the control to the vehicle
        ego_vehicle.apply_control(control)
        ego_vehicle.set_autopilot(False)
        print('in hospital rn')