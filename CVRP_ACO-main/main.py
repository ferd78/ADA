import pygame
from random import randint
import math
import time
from constants import WIDTH, HEIGHT, BACKGROUND_COLOR, MAX_DISTANCE, ANT_COLOR, DEPOT_COLOR, CUSTOMER_COLOR
from utility import distance, draw_node, draw_path
from aco import initialize_pheromones, update_pheromones, simulate_ants, double_bridge
from node import Customer, nodes, calculate_total_distance, Depot


class Window:
    def __init__(self):

        #visulization
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Vehicle Routing Problem with A.C.O")
        self.start_button_rect = pygame.Rect(4, 4, 200, 50) #start_button setup
        self.running = True
        self.simulation_running = False
        self.iteration = 0
        self.pheromone_levels = [[0, 0] for _ in range(len(nodes))]
        self.vehicle_capacity = 10
        self.current_screen = "start"
        self.paused = False

    def run_simulation(self):
        while self.running:
            self.screen.fill(BACKGROUND_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused


                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.current_screen == "start" and self.start_button_rect.collidepoint(mouse_x, mouse_y):
                        self.current_screen = "simulation"
                        self.simulation_running = True
                        self.pheromones = initialize_pheromones(len(nodes))
                        self.best_path = None
                        self.best_distance = MAX_DISTANCE
                        self.start_time = time.time()
                        self.iteration = 0
                        self.pheromone_levels = [[0, 0] for _ in range(len(nodes))]

            if self.current_screen == "start":
                pygame.draw.rect(self.screen, (0, 255, 0),
                                 self.start_button_rect)
                font = pygame.font.Font(None, 32)
                text_surface = font.render("Start Simulation", True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=self.start_button_rect.center)
                self.screen.blit(text_surface, text_rect)



            elif self.current_screen == "simulation" and not self.paused:
                vehicles = simulate_ants(
                    self.pheromones, nodes, self.vehicle_capacity)
                update_pheromones(self.pheromones, vehicles, nodes)

                for customer in nodes:
                    if isinstance(customer, Customer):
                        draw_node(customer, CUSTOMER_COLOR)

                for vehicle in vehicles:
                    double_bridge(vehicle)
                    draw_path(vehicle.route, ANT_COLOR)

                self.iteration += 1
                for i in range(len(nodes)):
                    self.pheromone_levels[i][1] = self.pheromones[0][i]
                    pheromone_text = f"Pheromone Level ({i}): {self.pheromone_levels[i][1]:.2f}"
                    font = pygame.font.Font(None, 20)
                    pheromone_surface = font.render(
                        pheromone_text, True, (0, 0, 0))
                    self.screen.blit(pheromone_surface,
                                     (WIDTH // 2 - 60, 60 + i * 20))
                
                for i, vehicle in enumerate(vehicles):
                    details_text = f"Vehicle {i + 1}: Capacity={self.vehicle_capacity}, Distance={calculate_total_distance(vehicle.route):.2f}"
                    font = pygame.font.Font(None, 20)
                    details_surface = font.render(
                        details_text, True, (0, 0, 0))
                    self.screen.blit(details_surface, (10, 20 + i * 20))


                iteration_text = f"Iteration: {self.iteration}"
                pheromone_text = f"Pheromone Level: {self.pheromone_levels[0][1]:.2f}"
                font = pygame.font.Font(None, 20)
                iteration_surface = font.render(
                    iteration_text, True, (0, 0, 0))
                pheromone_surface = font.render(
                    pheromone_text, True, (0, 0, 0))
                self.screen.blit(iteration_surface, (WIDTH // 2 - 60, 20))
                self.screen.blit(pheromone_surface, (WIDTH // 2 - 60, 40))

                if time.time() - self.start_time > 5:
                    self.simulation_running = False
                    for vehicle in vehicles:
                        ant_distance = calculate_total_distance(vehicle.route )
                        if ant_distance < self.best_distance:
                            self.best_distance = ant_distance
                            self.best_path = vehicle.route[:-1]

                    print("Best Path:", [nodes.index(node)
                          for node in self.best_path])
                    print("Best Distance:", self.best_distance)

                    popup_font = pygame.font.Font(None, 36)
                    popup_text = f"Best Path Length: {self.best_distance:.2f}"
                    popup_surface = popup_font.render(
                        popup_text, True, (0, 0, 0))
                    popup_rect = popup_surface.get_rect(
                        center=(800, 200))
                    self.screen.blit(popup_surface, popup_rect)
                    pygame.display.flip()
                    pygame.time.delay(3000)

            for i, node in enumerate(nodes):
                color = DEPOT_COLOR if isinstance(
                    node, Depot) else CUSTOMER_COLOR
                draw_node(node, color, text=node.demand if isinstance(
                    node, Customer) else None)

            pygame.display.flip()

        pygame.quit()


# Instantiate and run the simulation
if __name__ == "__main__":
    simulation = Window()
    simulation.run_simulation()
