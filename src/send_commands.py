
from __future__ import print_function

import time
import numpy as np
import traceback

import robobo
import cv2
import sys
import signal
import prey
from states import Agent
from actions import*

def terminate_program(signal_number, frame):
        print("Ctrl-C received, terminating program")
        rob.stop_world()
        sys.exit(1)

def simulation(rob):
    agent = Agent(rob=rob, n_episodes = 2, max_steps = 10)
    agent.train()
    # rob.stop_world()
    # rob.play_simulation()
    # state = State(stuck_threshold=0.05, debug_print=False)
    # for i in range(20):
    #         # print("robobo is at {}".format(rob.position()))
    #         action = 0
    #         selectMove(rob, action=action)
    #         # selectMove(rob, action=4)
    #         # time.sleep(5)
    #         # selectMove(rob, action=6)
    #         # time.sleep(5)
    #         # selectMove(rob, action=3)
    #         # time.sleep(5)
    #         # selectMove(rob,action=5)
    #         # hardRight(rob)
    #         # backward(rob)
    #         # softLeft(rob)
            
    #         # softRight(rob)
            
    #         sensor_data = rob.read_irs()[3:]
    #         # sensor_input = state.createSensorState(sensor_data)
    #         current_state = {'robot_position':rob.position(),
    #                         # 'sensor_state':sensor_input,
    #                         'sensor_data':sensor_data,
    #                         'action':action
    #                         }
    #         state.updateState(**current_state)


    #         # print(f'Sensor:{rob.read_irs()}')
    #         print(f'Robot data: {state.current_data}\nRobot state: {state.current_state}\nReward: {state.current_reward}')
    #         print(f'state action value in q table: {state.q_table[tuple(state.current_state)]}')
    #         # if state.current_data['stuck_state']:
    #         #     print('stuck')
    #         #     rob.stop_world()
                
    #         #     sys.exit(1)

    # rob.stop_world()


def main():
    signal.signal(signal.SIGINT, terminate_program)

    # rob = robobo.HardwareRobobo(camera=True).connect(address="192.168.1.7")
    global rob
    rob = robobo.SimulationRobobo().connect(address='127.0.0.1', port=19997)
    
    try:
        simulation(rob)
    except Exception as e:
        print(e)
        traceback.print_exc()
        rob.stop_world()

    

    # Following code moves the robot

   
    # print("robobo is at {}".format(rob.position()))
    # # rob.sleep(1)

    # # # Following code moves the phone stand
    # # rob.set_phone_pan(343, 100)
    # # rob.set_phone_tilt(109, 100)
    # # time.sleep(1)
    # # rob.set_phone_pan(11, 100)
    # # rob.set_phone_tilt(26, 100)

    # # Following code makes the robot talk and be emotional
    # # rob.set_emotion('happy')
    # # rob.talk('Hi, my name is Robobo')
    # # rob.sleep(1)
    # # rob.set_emotion('sad')

    # # Following code gets an image from the camera
    # # image = rob.get_image_front()
    # # cv2.imwrite("test_pictures.png",image)

    # # time.sleep(0.1)

    # # IR reading
    # for i in range(2):
    #     print(rob.read_irs())
    #     # print("ROB Irs: {}".format(np.log(np.array(rob.read_irs()))/10))
    #     time.sleep(0.1)

    # # pause the simulation and read the collected food
    # # rob.pause_simulation()
    
    # # Stopping the simualtion resets the environment
    # rob.stop_world()


if __name__ == "__main__":
    main()
