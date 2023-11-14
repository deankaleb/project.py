import random
import pygame

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
    def __init__(self, screen_width, screen_height, size, life):
        self.size = size
        self.life = life
        self.particles = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self._init_origin()

    def _init_origin(self):
        self.origin = (random.uniform(0, self.screen_width), random.uniform(0, self.screen_height))

    def update(self, dt):
        colors = [pygame.Color(0, 255, 0), pygame.Color(128, 0, 128)]  # Green and Purple
        color = random.choice(colors)
        particle = Particle(self.origin, size=self.size, life=self.life, color=color)
        self.particles.insert(0, particle)
        self._update_particles(dt)

    def _update_particles(self, dt):
        for idx, particle in enumerate(self.particles):
            particle.update(dt)
            if particle.dead:
                del self.particles[idx]

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

class Fireworks():
    def __init__(self, screen_res):
        self.screen_res = screen_res
        self.particle_size = 15
        self.birth_rate = 1  # bursts per frame
        self.bursts = []

    def update(self, dt):
        self._launch_new_bursts()
        self._update_bursts(dt)

    def _update_bursts(self, dt):
        for idx, burst in enumerate(self.bursts):
            burst.update(dt)
            if self._burst_is_offscreen(burst):
                del self.bursts[idx]

    def _burst_is_offscreen(self, burst):
        if not burst.particles:
            return True  # If the particles list is empty, consider it offscreen

        tail_is_offscreen = burst.particles[-1].pos[1] > self.screen_res[1]
        return tail_is_offscreen

    def _launch_new_bursts(self):
        for count in range(self.birth_rate):
            burst = ParticleTrail(self.screen_res[0], self.screen_res[1], size=self.particle_size, life=random.uniform(500, 3000))
            self.bursts.insert(0, burst)

    def draw(self, surface):
        for burst in self.bursts:
            burst.draw(surface)

def main():
    pygame.init()
    pygame.display.set_caption("Fireworks")

    min_resolution = (2880, 1920)
    screen = pygame.display.set_mode(min_resolution, pygame.FULLSCREEN)

    clock = pygame.time.Clock()
    dt = 0
    fireworks = Fireworks(screen.get_size())
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False


        fireworks.update(dt)
        screen.fill((0, 0, 0))
        fireworks.draw(screen)
        pygame.display.flip()

        dt = clock.tick(12)  # Adjust the frame rate

    pygame.quit()

if __name__ == "__main__":
    main()
