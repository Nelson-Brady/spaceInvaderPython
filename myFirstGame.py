"""
 Show how to fire bullets.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/PpdJjaiLX6A
"""
import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (136, 93, 158)

# --- Classes
class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        #   TODO add life to enemies
        #   self.life = 3

      #Set bad guy image
        self.image = pygame.image.load("enemyBlack2.png").convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        #testing life
        self.life = 5

    def update(self):
        """ Called each frame. """

        if self.rect.x >920:
            self.rect.x = 20
            self.rect.y += 60
        else:
            self.rect.x +=2


class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load("playerShip2_red.png").convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.life = 5

    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Set the player x position to the mouse x position
        self.rect.x = pos[0] - 28
        self.rect.y = 500

#TODO make bases and meteors.
class Meteor(pygame.sprite.Sprite):
    """ This class represents the meteors .   """
    # For now, they are meteors in space.

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load("meteorBrown_small1.png").convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.life = 10

    # meteor does not move...
   # def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.


class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([4, 10])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 5
        # self.rect.x += 4


# --- Create the window
# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 980
screen_height = 560
screen = pygame.display.set_mode([screen_width, screen_height])

# Get images
backGndImg = pygame.image.load("purple.png").convert()


# Get sounds
pygame.mixer.music.load("bg_music.ogg")
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
pygame.mixer.music.play()
ship_laser = pygame.mixer.Sound("laser5.ogg")

#Game level setup
level = 1

# --- Sprite lists

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# List of each block in the game
enemy_list = pygame.sprite.Group()

# List of each bullet
bullet_list = pygame.sprite.Group()

# Not Sure this is needed
# List of Player
player_list = pygame.sprite.Group()

# List of each base
#TODO fix to have meteor and base lists
meteor_list = pygame.sprite.Group()
#base_list = pygame.sprite.Group()

# --- Create the sprites

# --- Enemies
# should start with 98.
enemyCount = 0
for i in range(8 + (level * 2)):
    # This represents a enemy
    # enemy = Enemy(BLUE)
    enemy = Enemy()

    # Set starting location for the enemy
    enemy.rect.x = i * -70
    enemy.rect.y = 50

    # Add the enemy to the list of objects
    enemy_list.add(enemy)
    all_sprites_list.add(enemy)

    #Keep track of enemies
    enemyCount += 1

# --- Meteors
for i in range(8):
    # This represents a Meteor
    rock = Meteor()

    # Set locations for bases
    rock.rect.x = random.randrange(screen_width)
    rock.rect.y = random.randrange(110, 375)

    # Add meteors to list of objects
    meteor_list.add(rock)
    all_sprites_list.add(rock)


# Create a red player
player = Player()
player_list.add(player)
all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Keep score of units killed
myFont = pygame.font.SysFont('Calibri', 25, True, False)
score = 0
enemyKilled = 0
myLives = 3


#player.rect.y = 370


# Pause function

try:
    # while
    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if enemyCount < 1:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Fire a bullet if the user clicks the mouse button
                bullet = Bullet()
                ship_laser.play()
                # Set the bullet so it is where the player is
                bullet.rect.x = player.rect.x + 40
                bullet.rect.y = player.rect.y
                # Add the bullet to the lists
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)

        # --- Game logic

        # Call the update() method on all the sprites
        all_sprites_list.update()

        # Calculate mechanics for enemy/meteor collisions
        for rock in meteor_list:

            # See if an enemy hits a meteor
            e_hit_list = pygame.sprite.spritecollide(rock, enemy_list, True)

            for enemy in e_hit_list:
                enemy_list.remove(enemy)
                all_sprites_list.remove(enemy)
                meteor_list.remove(rock)
                all_sprites_list.remove(rock)
                enemyCount -= 1


        # Calculate mechanics for each bullet
        for bullet in bullet_list:

            # TODO Trying to subtract life from enemy here????

            # TODO if it hit a enemy - Give enemy 3 life?
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)

            # TODO on base life - Give base 10 life
            meteor_hit_list = pygame.sprite.spritecollide(bullet, meteor_list, True)

            # For each enemy hit, remove the bullet and add to the score
            for enemy in enemy_hit_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                enemyKilled += 1
                score += 1
                enemyCount -= 1
                # print(score, enemyKilled)

            # For each base hit, remove the bullet and damage base
            for rock in meteor_hit_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)


            # Remove the bullet if it flies up off the screen
            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)

        # See if enemy hits player ship
        for enemy in enemy_list:

            # Enemy hits, kills, player ship
            p_hit_list = pygame.sprite.spritecollide(enemy, player_list, True)

            for player in p_hit_list:
                myLives -= 1

        # --- Draw a frame

        # Clear the screen
        # screen.fill(WHITE)

        screen.blit(backGndImg, [0, 0])

        #Update current score
        scoreBoard = myFont.render("Score = " + str(score), 1, (0, 0, 0))
        screen.blit(scoreBoard, (5, 10))

        #Remaining enemies
        enemyBoard = myFont.render("Enemies = " + str(enemyCount), 1, (0, 0, 0))
        screen.blit(enemyBoard, (250, 10))

        #Remaining Lives
        liveBoard = myFont.render("Life = " + str(myLives), 1, (0, 0, 0))
        screen.blit(liveBoard, (450, 10))

        # Draw all the spites
        all_sprites_list.draw(screen)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Start at 125 frames per second  -- Change when testing
        clock.tick(490)

    pygame.quit()

except levelException
    pass