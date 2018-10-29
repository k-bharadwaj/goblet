from socketcan import Can

def adc_to_voltage(adc_value, gain_error, bit_resolution=12, adc_ref_high=5.0, adc_ref_low=0.0):
    volts_per_count = (adc_ref_high - adc_ref_low)/(0x1 << bit_resolution)
    return adc_value * volts_per_count * gain_error

def adc_to_real_world_current_out_lv(adc_value, gain_error, bit_resolution=12, adc_ref_high=5.0, adc_ref_low=0.0):
    volts = adc_to_voltage(adc_value, gain_error, bit_resolution, adc_ref_high, adc_ref_low)
    return (volts - 2.5)/0.05

def adc_to_real_world_current_in_hv(adc_value, gain_error, bit_resolution=12, adc_ref_high=5.0, adc_ref_low=0.0):
    volts = adc_to_voltage(adc_value, gain_error, bit_resolution, adc_ref_high, adc_ref_low)
    return (volts - 2.5)/0.02

def adc_to_real_world_current_bus(adc_value, gain_error, bit_resolution=12, adc_ref_high=5.0, adc_ref_low=0.0):
    volts = adc_to_voltage(adc_value, gain_error, bit_resolution, adc_ref_high, adc_ref_low)
    return (volts - 2.5)/0.01

def adc_to_real_world_voltage_high(adc_value, gain_error, bit_resolution=12, adc_ref_high=5.0, adc_ref_low=0.0):
    VOLTAGE_HIGH_CONVERSION_FACT0R = 100 / 0.4033
    volts = adc_to_voltage(adc_value, gain_error, bit_resolution, adc_ref_high, adc_ref_low)
    return volts * VOLTAGE_HIGH_CONVERSION_FACT0R

def adc_to_real_world_voltage_low(adc_value, gain_error, bit_resolution=12, adc_ref_high=5.0, adc_ref_low=0.0):
    VOLTAGE_LOW_CONVERSION_FACT0R = 100.0 / 4.347
    volts = adc_to_voltage(adc_value, gain_error, bit_resolution, adc_ref_high, adc_ref_low)
    return volts * VOLTAGE_LOW_CONVERSION_FACT0R

GAIN_ERROR = 1.0
# channel ID maps to channel name + conversion function tuple
ADC1_CHANNEL_INFO = {
    0 : ("HVIBus", adc_to_real_world_current_out_lv),
    1 : ("IOutLV1", adc_to_real_world_current_out_lv),
    2 : ("HVIn1", adc_to_real_world_current_in_hv),
    3 : ("LVIBus", adc_to_real_world_current_bus),
    4 : ("VOutLVBus", adc_to_real_world_voltage_low),
    5 : ("IOutLV2", adc_to_real_world_current_out_lv),
    6 : ("IOutLV3", adc_to_real_world_current_out_lv),
    7 : ("IOutLV4", adc_to_real_world_current_out_lv),
    8 : ("VOutHVPostRelay", adc_to_real_world_voltage_high),
    9 : ("VOutHVPreRelay", adc_to_real_world_voltage_high),
    10 : ("HvilI1", adc_to_voltage),
    11 : ("HvilI2", adc_to_voltage),
    12 : ("HVIn2", adc_to_real_world_current_in_hv),
    13 : ("HVIn3", adc_to_real_world_current_in_hv),
    14 : ("HVIn4", adc_to_real_world_current_in_hv),
    15 : ("TempMod11", adc_to_voltage)
}

ADC2_CHANNEL_INFO = {}

def process_adc_data_helper(adc_port, from_channel, to_channel, data, data_len):
    lut = ADC1_CHANNEL_INFO if adc_port == 1 else ADC2_CHANNEL_INFO
    data_list = [(data[i] | (data[i+1] << 8)) for i in range(0, data_len, 2)]
    for data_idx, chan in zip(range(len(data_list)), range(from_channel, to_channel+1)):
        real_world_value = lut[chan][1](data_list[data_idx], GAIN_ERROR)
        print("chan {}: {}".format(lut[chan][0], real_world_value))
    print("\n\n")

def process_adc1_chan0to3(data, data_len):
    if (data_len != 8):
        return
    process_adc_data_helper(1, 0, 3, data, data_len)

def process_adc1_chan4to7(data, data_len):
    if (data_len != 8):
        return
    process_adc_data_helper(1, 4, 7, data, data_len)

def process_adc1_chan8to11(data, data_len):
    if (data_len != 8):
        return
    process_adc_data_helper(1, 8, 11, data, data_len)

def process_adc1_chan12to13(data, data_len):
    if (data_len != 4):
        return
    process_adc_data_helper(1, 12, 13, data, data_len)

def process_adc2_chan0to3(data, data_len):
    pass # TODO

def process_adc2_chan4to7(data, data_len):
    pass # TODO


def process_and_print_can_msg(msg):
    process_functions_list = {
        0x1 : process_adc1_chan0to3,
        0x2 : process_adc1_chan4to7,
        0x3 : process_adc1_chan8to11,
        0x4 : process_adc1_chan12to13,
        0x5 : process_adc2_chan0to3,
        0x6 : process_adc2_chan4to7
    }

    try:
        process_functions_list[msg.arbitration_id](msg.data, msg.dlc)
    except KeyError:
        print("No handler to process msg with id {}".format(msg.arbitration_id))    
    


def dc_dc_poll():
    can = Can()

    while True:
        CAN_MSG_TIMEOUT = 10 #sec
        msg = can.recv(timeout=CAN_MSG_TIMEOUT)

        process_and_print_can_msg(msg)

if __name__ == "__main__":
    dc_dc_poll()
    