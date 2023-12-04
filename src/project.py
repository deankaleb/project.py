import random
import pygame
import math

class Particle:
    def __init__(self, pos=(0, 0), size=15, life=1000):
        self.pos = pos
        self.size = size
        # Define a list of colors
        colors = [pygame.Color("green"), pygame.Color("purple"), pygame.Color("blue")]
        # Choose a random color from the list
        self.color = random.choice(colors)
        self.age = 0
        self.life = life
        self.dead = False
        self.alpha = 255
        self.surface = self.update_surface()

    def update(self, dt):
        self.age += dt
        if self.age > self.life:
            self.dead = True
        # Fading in and out effect based on particle's age
        if self.age < self.life / 2:  # Fade in
            self.alpha = int((self.age / (self.life / 2)) * 255)
        else:  # Fade out
            self.alpha = int(((self.life - self.age) / (self.life / 2)) * 255)

    def update_surface(self):
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        radius = self.size
        color = self.color
        center = (self.size, self.size)
        pygame.draw.circle(surf, color, center, radius)
        return surf

    def draw(self, surface):
        if self.dead:
            return
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.pos)

class ParticleTrail():
    def __init__(self, origin, num_circles, particles_per_circle, max_size, life):
        self.origin = origin
        self.num_circles = num_circles
        self.particles_per_circle = particles_per_circle
        self.max_size = max_size
        self.life = life
        self.particles = []
        self._init_circles()


    def _init_circles(self):
        for circle in range(1, self.num_circles + 1):
            circle_radius = (circle / self.num_circles) * self.max_size
            for i in range(self.particles_per_circle):
                angle = (2 * math.pi / self.particles_per_circle) * i
                x = self.origin[0] + circle_radius * math.cos(angle)
                y = self.origin[1] + circle_radius * math.sin(angle)
                pos = (int(x), int(y))
                life = random.uniform(500, 3000)
                particle = Particle(pos, size=5, life=life)
                self.particles.append(particle)

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)


class FireworksManager:
    def __init__(self, screen_size, num_fireworks):
        self.screen_size = screen_size
        self.num_fireworks = num_fireworks
        self.fireworks = self._create_fireworks()

    def _create_fireworks(self):
        fireworks = []
        for _ in range(self.num_fireworks):
            origin = (random.randint(0, self.screen_size[0]), random.randint(0, self.screen_size[1]))
            num_circles = random.randint(3, 8)
            particles_per_circle = random.randint(10, 30)
            max_size = random.randint(30, 80)
            life = random.randint(800, 1500)
            fireworks.append(ParticleTrail(origin, num_circles, particles_per_circle, max_size, life))
        return fireworks

    def update(self, dt):
        for firework in self.fireworks:
            firework.update(dt)

    def draw(self, surface):
        for firework in self.fireworks:
            firework.draw(surface)


def main():
    pygame.init()
    pygame.display.set_caption("Fireworks")

    min_resolution = (2880, 1960)
    screen = pygame.display.set_mode(min_resolution)

    clock = pygame.time.Clock()
    dt = 0
    running = True
    creating_firework = False
    particle_trails = []
    last_firework_time = pygame.time.get_ticks()
    firework_delay = 150  # Time delay between each firework in milliseconds

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()

        # Check for mouse movement to create fireworks with a delay
        if pygame.mouse.get_rel() != (0, 0) and current_time - last_firework_time > firework_delay:
            origin = mouse_pos
            num_circles = random.randint(3, 8)
            particles_per_circle = random.randint(10, 30)
            max_size = random.randint(50, 100)
            life = random.randint(800, 1500)
            particle_trails.append(ParticleTrail(origin, num_circles, particles_per_circle, max_size, life))
            last_firework_time = current_time  # Update last firework creation time

        for particle_trail in particle_trails:
            particle_trail.update(dt)
            particle_trail.draw(screen)

        pygame.display.flip()
        dt = clock.tick(30)

    pygame.quit()
if __name__ == "__main__":
    main()
