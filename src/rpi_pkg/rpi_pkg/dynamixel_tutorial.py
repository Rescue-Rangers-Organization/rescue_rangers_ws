#!/usr/bin/env python3

from dynamixel_sdk import *


# PPR = 607,500

portHandler = PortHandler('/dev/ttyUSB0')
packetHandler = PacketHandler(2.0)

goal_position_address = 116
present_position_address = 132
data_length_4byte = 4
groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, goal_position_address, data_length_4byte)
groupSyncRead  = GroupSyncRead(portHandler, packetHandler, present_position_address, data_length_4byte)

if portHandler.openPort():
  print("Succeeded to open the port!")
else:
  print("Failed to open the port!")
  exit()

if portHandler.setBaudRate(57600):
  print("Succeeded to change the baudrate!")
else:
  print("Failed to change the baudrate!")
  exit()

dxl_id1 = 1
dxl_id2 = 2
torque_on_address = 64
data = 1
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id1, torque_on_address, data)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel#1 has been successfully connected")

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id2, torque_on_address, data)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel#2 has been successfully connected")

dxl_addparam_result = groupSyncRead.addParam(dxl_id1)
if dxl_addparam_result != True:
    print("[ID:%03d] groupSyncRead addparam failed" % dxl_id1)
    exit()

dxl_addparam_result = groupSyncRead.addParam(dxl_id2)
if dxl_addparam_result != True:
    print("[ID:%03d] groupSyncRead addparam failed" % dxl_id2)
    exit()

while True:
    try:
        target_position = int(input("Enter target position (0 ~ 4095, -1 to exit): "))
    except ValueError:
        print("Please enter an integer.")
        continue

    if target_position == -1:
        break
    elif target_position < 0 or target_position > 4095:
        print("Position must be between 0 and 4095.")
        continue

    param_goal_position = [
        DXL_LOBYTE(DXL_LOWORD(target_position)),
        DXL_HIBYTE(DXL_LOWORD(target_position)),
        DXL_LOBYTE(DXL_HIWORD(target_position)),
        DXL_HIBYTE(DXL_HIWORD(target_position))
    ]

    dxl_addparam_result = groupSyncWrite.addParam(dxl_id1, param_goal_position)
    if not dxl_addparam_result:
        print("[ID:%03d] groupSyncWrite addparam failed" % dxl_id1)
        exit()

    dxl_addparam_result = groupSyncWrite.addParam(dxl_id2, param_goal_position)
    if not dxl_addparam_result:
        print("[ID:%03d] groupSyncWrite addparam failed" % dxl_id2)
        exit()

    dxl_comm_result = groupSyncWrite.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

    groupSyncWrite.clearParam()
    while True:
        dxl_comm_result = groupSyncRead.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        dxl_getdata_result = groupSyncRead.isAvailable(dxl_id1, present_position_address, data_length_4byte)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupSyncRead getdata failed" % dxl_id1)
            quit()

        dxl_getdata_result = groupSyncRead.isAvailable(dxl_id2, present_position_address, data_length_4byte)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupSyncRead getdata failed" % dxl_id2)
            quit()
        dxl1_present_position = groupSyncRead.getData(dxl_id1, present_position_address, data_length_4byte)
        dxl2_present_position = groupSyncRead.getData(dxl_id2, present_position_address, data_length_4byte)
        print("[ID:%03d] GoalPos:%03d  PresPos:%03d\t[ID:%03d] GoalPos:%03d  PresPos:%03d" % (dxl_id1, target_position, dxl1_present_position, dxl_id2, target_position, dxl2_present_position))
        if abs(target_position - dxl1_present_position) <= 10 and abs(target_position - dxl2_present_position) <= 10:
            break
portHandler.closePort()