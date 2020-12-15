import rclpy
import ruamel.yaml as yaml
import pickle
import yaml

def main():
    with open('test.yaml') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        fruits_list = yaml.load(file, Loader=yaml.FullLoader)

        ebat = fruits_list.get(list(fruits_list.keys())[0])
        print(ebat)



if __name__ == "__main__":
    main()