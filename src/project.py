import random
import pygame
import math

class Particle:
    def __init__(self, pos=(0, 0), size=8, life=1000):
        self.pos = pos
        self.size = size
        # Define a function to generate random shades of green or purple
        def random_color(base_color):
            variance = 50  # You can adjust this value for more or less variation
            r = base_color.r + random.randint(-variance, variance)
            g = base_color.g + random.randint(-variance, variance)
            b = base_color.b + random.randint(-variance, variance)
            return pygame.Color(min(255, max(0, r)), min(255, max(0, g)), min(255, max(0, b)))

        # Define base colors for green and purple
        base_green = pygame.Color(0, 255, 0)  # Green
        base_purple = pygame.Color(128, 0, 128)  # Purple

        # Choose a random shade of green or purple for each particle
        base_colors = [base_green, base_purple]
        base_color = random.choice(base_colors)
        self.color = random_color(base_color)

        # Remaining initialization code remains unchanged
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


def main():
    pygame.init()
    pygame.display.set_caption("Fireworks")

    min_resolution = (800, 600)
    screen = pygame.display.set_mode(min_resolution)

    clock = pygame.time.Clock()
    dt = 0
    particle_trail = ParticleTrail((400, 300), num_circles=5, particles_per_circle=20, max_size=50, life=1000)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        particle_trail.update(dt)
        particle_trail.draw(screen)
        pygame.display.flip()

        dt = clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
