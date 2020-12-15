import rclpy
import ruamel.yaml as yaml
import pickle
directory_path = '/home/leekai/dev_ws/src/alternative_logger/alternative_logger/15.12.2020-10:39:43_yaml/15.12.2020-10:39:43_rtp_1_imu.txt'

clean_data_dict = {}
raw_data_dict = {}

def main():
    # открываем текстовый файл и считываем его по строчно занося в словарь сырых данных
    with open(directory_path) as file:
        for line in file:
            data = line.find(':')
            raw_data_dict[line[:data]] = line[data + 2:][:-2]
            # print(line)

    # создаем словарь для чистых данных первой ступени
    dict_data = {}
    for g in range(len(list(raw_data_dict.keys()))):
        key_msg = list(raw_data_dict.keys())[g]
        # разделяем всю строку по подстроке "'&" и получаем разделенные элементы словаря
        data_from_msg = raw_data_dict[key_msg].replace('"', '\'').split(', \'&')
        # убираем первый элемент из списка, так как заранее знаем, что он пустой
        data_from_msg = data_from_msg[1:]

        print(data_from_msg)

        dict_one_msg = {}   # словарь одного msg

        for i in data_from_msg:
            key = i[:i.find(':')][1:]
            key = key[:-1]
            dict_one_msg[key] = i[i.find(':') + 2:]

        dict_data[key_msg] = dict_one_msg
        # print(index_msg, data_pars)


    # for j in range(len(list(dict_data.keys()))):
    #     print(dict_data[list(dict_data.keys())[j]])

    file = open('test.yaml'.format(), 'w')
    yaml.dump(dict_data, file, default_flow_style=False, allow_unicode=True)
    file.close()

if __name__ == "__main__":
    main()