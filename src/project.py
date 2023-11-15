import random
import pygame
import math

class Particle():
    def __init__(self, pos=(0, 0), size=15, life=1000, color=pygame.Color(0, 255, 0)):
        self.pos = pos
        self.size = size
        self.color = color
        self.age = 0
        self.life = life
        self.dead = False
        self.alpha = 255
        self.surface = self.update_surface()

    def update(self, dt):
        self.age += dt
        if self.age > self.life:
            self.dead = True
        self.alpha = 255 * (1 - (self.age / self.life))

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
    def __init__(self, origin, num_particles, size, life):
        self.origin = origin
        self.num_particles = num_particles
        self.size = size
        self.life = life
        self.particles = []
        self._init_circle()

    def _init_circle(self):
        for i in range(self.num_particles):
            angle = (2 * math.pi / self.num_particles) * i
            x = self.origin[0] + self.size * math.cos(angle)
            y = self.origin[1] + self.size * math.sin(angle)
            pos = (int(x), int(y))
            life = random.uniform(500, 3000)
            particle = Particle(pos, size=self.size, life=life)
            self.particles.append(particle)

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

def main():
    pygame.init()
    pygame.display.set_caption("Spiral of Circles")

    min_resolution = (800, 600)
    screen = pygame.display.set_mode(min_resolution)

    clock = pygame.time.Clock()
    dt = 0
    particle_trail = ParticleTrail((400, 300), num_particles=20, size=10, life=1000)  # Circular origin at (400, 300)
  # Circular origin at (400, 300)
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
