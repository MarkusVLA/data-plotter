import numpy as np

class Camera:
    def __init__(self, radius, angle_x, angle_y):
        self.radius = radius
        self.angle_x = angle_x
        self.angle_y = angle_y

    def get_camera_position(self):
        camera_x = self.radius * np.sin(np.radians(self.angle_y)) * np.cos(np.radians(self.angle_x))
        camera_y = self.radius * np.sin(np.radians(self.angle_y)) * np.sin(np.radians(self.angle_x))
        camera_z = self.radius * np.cos(np.radians(self.angle_y))
        return np.array([camera_x, camera_y, camera_z])
