import configparser

""" VARIABLES """
config_Path = "EngineDataFile\EngineConfig\GEngineSettings.ini"

class GEngineConfig:
    def __init__(self):
        try:
            with open(config_Path):
                print("File exists")
        except IOError:
            print("Error opening " + str(config_Path) + ", creating new one")
            config = configparser.ConfigParser()
            config['DEFAULT'] = {
                    'GRAVITY':'True',
                    'GRAVITY_AMOUNT':'3',
                    'SHOOT':'True',
                    'SHOOT_SPEED':'1',
                    'BLOCK_SIZE':'32',
                    'HORIZONTAL_SPEED:':'4',
                    'VERTICAL_SPEED:':'8'
                }
            with open(config_Path,'w') as configfile:
                config.write(configfile)
            print("File successfully written.")
                
    def ReturnData(self,data):
        config = configparser.ConfigParser()
        try:
            with open(config_Path): pass
            config.read(config_Path)
        except IOError:
            print("Error opening " + str(config_Path))
        try:
            returndata = (config['DEFAULT'][data]).replace('=','').strip()
            return returndata
        except KeyError:
            print(str(data) + " wasn't in the configuration data")
        return 0
