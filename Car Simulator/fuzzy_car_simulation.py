import pygame
import math
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyCarAvoidance:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Fuzzy Car Obstacle Avoidance")
        
        # Main settings
        self.center_x, self.center_y = 400, 300
        self.track_radius = 200
        
        # Car state
        self.car_angle = 0
        self.car_radius = self.track_radius
        self.speed = 30
        
        # Obstacles (2 simple obstacles)
        self.obstacles = [
            {'angle': math.pi/3, 'size': 20},
            {'angle': 4*math.pi/3, 'size': 20}
        ]
        
        self.setup_fuzzy_system()
        self.clock = pygame.time.Clock()
        
    def setup_fuzzy_system(self):
        # Input: distance to obstacle
        self.distance = ctrl.Antecedent(np.arange(0, 150, 1), 'distance')
        self.distance['close'] = fuzz.trimf(self.distance.universe, [0, 0, 60])
        self.distance['far'] = fuzz.trimf(self.distance.universe, [40, 150, 150])
        
        # Output: avoidance level
        self.avoidance = ctrl.Consequent(np.arange(0, 101, 1), 'avoidance')
        self.avoidance['low'] = fuzz.trimf(self.avoidance.universe, [0, 0, 40])
        self.avoidance['high'] = fuzz.trimf(self.avoidance.universe, [60, 100, 100])
        
        # Simple rules
        rule1 = ctrl.Rule(self.distance['close'], self.avoidance['high'])
        rule2 = ctrl.Rule(self.distance['far'], self.avoidance['low'])
        
        self.control_system = ctrl.ControlSystem([rule1, rule2])
        self.simulator = ctrl.ControlSystemSimulation(self.control_system)
    
    def get_distance_to_nearest_obstacle(self):
        car_x = self.center_x + self.car_radius * math.cos(self.car_angle)
        car_y = self.center_y + self.car_radius * math.sin(self.car_angle)
        
        min_distance = 150
        for obstacle in self.obstacles:
            obs_x = self.center_x + self.track_radius * math.cos(obstacle['angle'])
            obs_y = self.center_y + self.track_radius * math.sin(obstacle['angle'])
            # calculate the euclidean distance between the car and the obstacle
            distance = math.sqrt((car_x - obs_x)**2 + (car_y - obs_y)**2)
            if distance < min_distance:
                min_distance = distance
        
        return min_distance
    
    def update_car_movement(self, dt):
        distance = self.get_distance_to_nearest_obstacle()
        
        # Use fuzzy logic
        self.simulator.input['distance'] = distance
        self.simulator.compute()
        avoidance_level = self.simulator.output['avoidance']
        
        # Adjust radius based on avoidance level
        target_radius = self.track_radius + (avoidance_level * 0.5)
        self.car_radius += (target_radius - self.car_radius) * dt * 3
        
        # Limit radius
        self.car_radius = max(150, self.car_radius)
        
        # Circular movement
        angular_speed = self.speed / self.car_radius * dt
        self.car_angle += angular_speed
        self.car_angle = self.car_angle % (2 * math.pi)
    
    def draw(self):
        self.screen.fill((30, 40, 50))
        
        # Main track
        pygame.draw.circle(self.screen, (100, 100, 100), 
                         (self.center_x, self.center_y), self.track_radius, 2)
        
        # Obstacles
        for obstacle in self.obstacles:
            x = self.center_x + self.track_radius * math.cos(obstacle['angle'])
            y = self.center_y + self.track_radius * math.sin(obstacle['angle'])
            pygame.draw.circle(self.screen, (255, 100, 100), (int(x), int(y)), obstacle['size'])
        
        # Car
        car_x = self.center_x + self.car_radius * math.cos(self.car_angle)
        car_y = self.center_y + self.car_radius * math.sin(self.car_angle)
        
        # Change color based on distance
        distance = self.get_distance_to_nearest_obstacle()
        if distance < 60:
            car_color = (255, 150, 100)  # Orange
        else:
            car_color = (100, 200, 255)  # Blue
            
        pygame.draw.circle(self.screen, car_color, (int(car_x), int(car_y)), 12)
        
    def run(self):
        running = True
        print("Starting simulation")
        
        while running:
            dt = self.clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
            
            self.update_car_movement(dt)
            self.draw()
            pygame.display.flip()
        
        pygame.quit()

# Run simulation
if __name__ == "__main__":
    FuzzyCarAvoidance().run()
