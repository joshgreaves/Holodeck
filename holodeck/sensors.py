"""Definition of all of the sensor information"""
import numpy as np


class Sensor(object):

    def __init__(self, client, name="DefaultSensor"):
        self.name = name
        self._client = client

        self._on_bool_buffer = self._client.malloc(name + "_teleport_flag", [1], np.uint8)
        self._sensor_data_buffer = self._client.malloc(name, self.data_shape, self.dtype)

    @property
    def dtype(self):
        """The type of data in the sensor

        Returns:
            numpy dtype of sensor data
        """
        raise NotImplementedError("Child class must implement this property")

    @property
    def data_shape(self):
        """The shape of the sensor data

        Returns:
            tuple representing sensor data shape
        """
        raise NotImplementedError("Child class must implement this property")


class Terminal(Sensor):

    @property
    def dtype(self):
        return np.bool

    @property
    def data_shape(self):
        return [1]


class Reward(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [1]


class ViewportCapture(Sensor):

    def __init__(self, client, name="ViewportCapture", shape=(512, 512, 4)):
        super(ViewportCapture, self).__init__(client, name=name)
        self.shape = shape

    @property
    def dtype(self):
        return np.uint8

    @property
    def data_shape(self):
        return self.shape


class RGBCamera(Sensor):

    def __init__(self, client, name="ViewportCapture", shape=(256, 256, 4)):
        super(RGBCamera, self).__init__(client, name=name)
        self.shape = shape

    @property
    def dtype(self):
        return np.uint8

    @property
    def data_shape(self):
        return self.shape


class OrientationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3, 3]


class IMUSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2, 3]


class JointRotationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [94]


class RelativeSkeletalPositionSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [67, 4]


class LocationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class RotationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class VelocitySensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class CollisionSensor(Sensor):

    @property
    def dtype(self):
        return np.bool

    @property
    def data_shape(self):
        return [1]


class PressureSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [48*(3+1)]





class Sensors:
    """Class information of sensor data with mappings from names to corresponding numbers

    Attributes:
        TERMINAL (int): Index for terminal sensor output. Value is 1.
        REWARD (int): Index for reward sensor output. Value is 2.
        VIEWPORT_CAPTURE (int): Deprecated. Index for primary player camera sensor. Value is 3.
        RGB_CAMERA (int): Index for pixel camera sensor. Value is 4.
        ORIENTATION_SENSOR (int): Index for orientation sensor. Value is 5.
        IMU_SENSOR (int): Index for IMU sensor. Value is 6.
        JOINT_ROTATION_SENSOR (int): Index for joint rotation sensor. Value is 7.
        RELATIVE_SKELETAL_POSITION_SENSOR (int): Index for relative skeletal position sensor. Value is 8.
        LOCATION_SENSOR (int): Index for location sensor. Value is 9.
        VELOCITY_SENSOR (int): Index for velocity sensor. Value is 10.
        ROTATION_SENSOR (int): Index for rotation sensor. Value is 11.
        COLLISION_SENSOR (int): Index for collision sensor. Value is 12.
        PRESSURE_SENSOR (int): Index for pressure sensor. Value is 13.
    """
    TERMINAL = 1
    REWARD = 2
    VIEWPORT_CAPTURE = 3  # default is 512 x 512 RGBA
    RGB_CAMERA = 4  # default is 512 x 512 RGBA
    ORIENTATION_SENSOR = 5
    IMU_SENSOR = 6
    JOINT_ROTATION_SENSOR = 7
    RELATIVE_SKELETAL_POSITION_SENSOR = 8
    LOCATION_SENSOR = 9
    VELOCITY_SENSOR = 10
    ROTATION_SENSOR = 11
    COLLISION_SENSOR = 12
    PRESSURE_SENSOR = 13

    # Sizes are the number of entries in the numpy array
    _shape_dict = {
        TERMINAL: [1],
        REWARD: [1],
        VIEWPORT_CAPTURE: [512, 512, 4],
        RGB_CAMERA: [256, 256, 4],
        ORIENTATION_SENSOR: [3, 3],
        IMU_SENSOR: [2, 3],
        JOINT_ROTATION_SENSOR: [94],
        RELATIVE_SKELETAL_POSITION_SENSOR: [67, 4],
        LOCATION_SENSOR: [3],
        VELOCITY_SENSOR: [3],
        ROTATION_SENSOR: [3],
        COLLISION_SENSOR: [1],
        PRESSURE_SENSOR: [48*(3+1)],
    }

    _type_dict = {
        TERMINAL: np.bool,
        REWARD: np.float32,
        VIEWPORT_CAPTURE: np.uint8,
        RGB_CAMERA: np.uint8,
        ORIENTATION_SENSOR: np.float32,
        IMU_SENSOR: np.float32,
        JOINT_ROTATION_SENSOR: np.float32,
        RELATIVE_SKELETAL_POSITION_SENSOR: np.float32,
        LOCATION_SENSOR: np.float32,
        VELOCITY_SENSOR: np.float32,
        ROTATION_SENSOR: np.float32,
        COLLISION_SENSOR: np.bool,
        PRESSURE_SENSOR: np.float32,
    }

    _name_dict = {
        TERMINAL: "Terminal",
        REWARD: "Reward",
        VIEWPORT_CAPTURE: "ViewportCapture",
        RGB_CAMERA: "RGBCamera",
        ORIENTATION_SENSOR: "OrientationSensor",
        IMU_SENSOR: "IMUSensor",
        JOINT_ROTATION_SENSOR: "JointRotationSensor",
        RELATIVE_SKELETAL_POSITION_SENSOR: "RelativeSkeletalPositionSensor",
        LOCATION_SENSOR: "LocationSensor",
        VELOCITY_SENSOR: "VelocitySensor",
        ROTATION_SENSOR: "RotationSensor",
        COLLISION_SENSOR: "CollisionSensor",
        PRESSURE_SENSOR: "PressureSensor"
    }

    _reverse_name_dict = {v: k for k, v in _name_dict.items()}

    @staticmethod
    def shape(sensor_type):
        """Gets the shape of a particular sensor.

        Args:
            sensor_type (int): The type of the sensor.

        Returns:
            List of int: The shape of the sensor data.
        """
        return Sensors._shape_dict[sensor_type] if sensor_type in Sensors._shape_dict else None

    @staticmethod
    def name(sensor_type):
        """Gets the human readable name for a sensor.

        Args:
            sensor_type (int): The type of the sensor.

        Returns:
            str: The name of the sensor.
        """
        return Sensors._name_dict[sensor_type] if sensor_type in Sensors._name_dict else None

    @staticmethod
    def dtype(sensor_type):
        """Gets the data type of the sensor data (the dtype of the numpy array).

        Args:
            sensor_type (int): The type of the sensor.

        Returns:
            type: The type of the sensor data.
        """
        return Sensors._type_dict[sensor_type] if sensor_type in Sensors._type_dict else None

    @staticmethod
    def name_to_sensor(sensor_name):
        """Gets the index value of a sensor from its human readable name.

        Args:
            sensor_name (str): The human readable name of the sensor.

        Returns:
            int: The index value for the sensor.
        """
        return Sensors._reverse_name_dict[sensor_name] if sensor_name in Sensors._reverse_name_dict else None

    @staticmethod
    def set_primary_cam_size(height, width):
        """Sets the primary camera size for this world. Should only be called by environment.

        Args:
            height (int): New height value.
            width (int): New width value.
        """
        Sensors._shape_dict[Sensors.VIEWPORT_CAPTURE] = [height, width, 4]

    @staticmethod
    def set_pixel_cam_size(height, width):
        """Sets the pixel camera size for this world. Should only be called by Environment.

        Args:
            height (int): New height value.
            width (int): New width value.
        """
        Sensors._shape_dict[Sensors.RGB_CAMERA] = [height, width, 4]

    def __init__(self):
        print("No point in instantiating an object.")
