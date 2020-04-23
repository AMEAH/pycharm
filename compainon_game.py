import pygame

pygame.init()
win = pygame.display.set_mode((800, 480))
pygame.display.set_caption("Companionship")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')
clock = pygame.time.Clock()

food_sound = pygame.mixer.Sound('shoot.wav')
hit_sound = pygame.mixer.Sound('hit.wav')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

score = 0


class player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.hitbox = (self.x + 18, self.y + 10, 29, 52)
        self.player_health = 10

    def draw(self, win):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                win.blit(walkRight[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 18, self.y + 10, 29, 52)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


class projectile:
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class cat:
    walkRight = [pygame.image.load('R1C.png'), pygame.image.load('R2C.png'), pygame.image.load('R3C.png'),
                 pygame.image.load('R4C.png'), pygame.image.load('R5C.png'), pygame.image.load('R6C.png'),
                 pygame.image.load('R7C.png'), pygame.image.load('R8C.png'), pygame.image.load('R9C.png'),
                 pygame.image.load('R10C.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walk_count = 0
        self.vel = 2
        self.hitbox = (self.x + 6, self.y - 2, 28, 40)
        self.cat_health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walk_count + 1 >= 30:
                self.walk_count = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            else:
                pass
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0] - 8, self.hitbox[1] - 10, 50, 10))
            pygame.draw.rect(win, (255, 0, 0),
                             (self.hitbox[0] - 8, self.hitbox[1] - 10, 50 - (5 * (10 - self.cat_health)), 10))
            self.hitbox = (self.x + 6, self.y - 2, 28, 40)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x = -2
            else:
                self.vel = self.vel * -1
                self.walk_count = 0

    def hit(self):
        if self.cat_health > 0:
            self.cat_health -= 3
        else:
            self.visible = False


class dog:
    walkRight = [pygame.image.load('R1D.png'), pygame.image.load('R2D.png'), pygame.image.load('R3D.png'),
                 pygame.image.load('R4D.png'), pygame.image.load('R5D.png'), pygame.image.load('R6D.png'),
                 pygame.image.load('R7D.png'), pygame.image.load('R8D.png'), pygame.image.load('R9D.png'),
                 pygame.image.load('R10D.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walk_count = 0
        self.vel = 3
        self.hitbox = (self.x + 6, self.y - 2, 28, 40)
        self.dog_health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walk_count + 1 >= 30:
                self.walk_count = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            else:
                pass
            # pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0] - 8, self.hitbox[1] - 10, 50, 10))
            # pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0] - 8, self.hitbox[1] - 10, 50 - (5 * (10 - self.dog_health)), 10))
            self.hitbox = (self.x + 6, self.y - 2, 28, 40)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x = -2
            else:
                self.vel = self.vel * -1
                self.walk_count = 0

    def hit(self):
        if self.dog_health > 0:
            self.dog_health -= 3
        else:
            self.visible = False


class bird:
    walkRight = [pygame.image.load('RU.png'), pygame.image.load('RM.png'), pygame.image.load('RD.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walk_count = 0
        self.vel = 5

    def draw(self, win):
        self.move()
        if self.walk_count + 1 >= 9:
            self.walk_count = 0

        if self.vel > 0:
            win.blit(self.walkRight[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
        else:
            pass

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0


def redraw_game_window():
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    text2 = font.render('Arrow keys to move', 1, (0, 0, 0))
    text3 = font.render('Space to feed cat', 1, (0, 0, 0))
    win.blit(text, (380, 10))
    win.blit(text2, (10, 10))
    win.blit(text3, (10, 30))
    character.draw(win)
    happy.draw(win)
    charlie.draw(win)
    fluffy.draw(win)
    for food in foods:
        food.draw(win)
    pygame.display.update()


font = pygame.font.SysFont('comicsans', 30, True)
happy = cat(100, 410, 64, 64, 790)
character = player(0, 400, 64, 64)
charlie = bird(5, 100, 64, 64, 790)
fluffy = dog(150, 410, 64, 64, 790)
foods = []
food_loop = 0
run = True
while run:
    clock.tick(27)

    if happy.visible:
        if character.hitbox[1] < happy.hitbox[1] + happy.hitbox[3] and character.hitbox[1] + character.hitbox[3] > \
                happy.hitbox[1]:
            if character.hitbox[0] + character.hitbox[2] > happy.hitbox[0]:
                if character.hitbox[0] < happy.hitbox[0] + happy.hitbox[2]:
                    score += 1

    if fluffy.visible:
        if character.hitbox[1] < fluffy.hitbox[1] + fluffy.hitbox[3] and character.hitbox[1] + character.hitbox[3] > \
                fluffy.hitbox[1]:
            if character.hitbox[0] + character.hitbox[2] > fluffy.hitbox[0]:
                if character.hitbox[0] < fluffy.hitbox[0] + fluffy.hitbox[2]:
                    score += 1

    if food_loop > 0:
        food_loop += 1
    if food_loop > 1:
        food_loop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for food in foods:
        if food.y - food.radius < happy.hitbox[1] + happy.hitbox[3] and food.y + food.radius > happy.hitbox[1]:
            if food.x - + food.radius > happy.hitbox[0] and food.x - food.radius < happy.hitbox[0] + happy.hitbox[2]:
                hit_sound.play()
                happy.hit()
                score += 1
                foods.pop(foods.index(food))
        if 800 > food.x > 0:
            food.x += food.vel
        else:
            foods.pop(foods.index(food))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and food_loop == 0:
        food_sound.play()
        if character.left:
            facing = -1
        else:
            facing = 1
        if len(foods) < 1:
            foods.append(projectile(character.x + character.width // 2, round(character.y + character.height // 2), 6,
                                    (210, 105, 30), facing))
            food_loop = 1
    if keys[pygame.K_LEFT] and character.x > character.vel:
        character.x -= character.vel
        character.left = True
        character.right = False
        character.standing = False
    elif keys[pygame.K_RIGHT] and character.x < 800 - character.width:
        character.x += character.vel
        character.right = True
        character.left = False
        character.standing = False
    else:
        character.standing = True
        character.walk_count = 0
    if not character.is_jump:
        if keys[pygame.K_UP]:
            character.is_jump = True
            character.right = False
            character.left = False
            character.walk_count = 0
    else:
        if character.jump_count >= -10:
            neg = 1
            if character.jump_count < 0:
                neg = -1
            character.y -= (character.jump_count ** 2) * 0.5 * neg
            character.jump_count -= 1
        else:
            character.is_jump = False
            character.jump_count = 10

    redraw_game_window()

pygame.quit()
