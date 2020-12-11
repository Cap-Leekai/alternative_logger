import rclpy
import ruamel.yaml as yaml
import pickle
directory_path = '/home/leekai/dev_ws/src/alternative_logger/alternative_logger/11.12.2020-13:21:44_yaml/11.12.2020-13:21:44_rtp_1_imu.txt'

dict_data = {}

def main():
            with open(directory_path) as file:
                for line in file:
                    data = line.find(':')
                    dict_data[line[:data]] = line[data + 1:]
                    # print(line)

            data_pars = dict_data[list(dict_data.keys())[0]].split(':')

            for i in data_pars:
                print(i)


if __name__ == "__main__":
    main()