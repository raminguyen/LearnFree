import pygame
import time
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 250

PLAYER_HEIGTH = 20

PLAYER_VEL = 5

FONT = pygame.font.SysFont("Lora", 50)

STAR_WIDTH = 10

STAR_HEIGTH = 20

STAR_VEL = 3


""" Load music """

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(1.0)

""" Background """
def draw(player, elapsed_time, stars, lives, points):

    WIN.blit(BG, (0,0)) #draw surface on the screen

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white") #    render the time 
    lives_text = FONT.render(f"Lives: {lives}", 1, "white") #    render the lives
    points_text = FONT.render(f"Points: {points}", 1, "white") #    render the points

    #1: antialiasing

    WIN.blit(time_text, (10, 10)) #draw time 
    lives_x = WIDTH - lives_text.get_width() - 10 #padding from the right
    lives_y = 10
    WIN.blit(lives_text, (lives_x, lives_y))
    WIN.blit(points_text, (10, 60))

    pygame.draw.rect(WIN, "green", player)

    for star, color in stars:
        pygame.draw.rect(WIN, color, star)

    pygame.display.update()

def main():

    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGTH, PLAYER_WIDTH, PLAYER_HEIGTH)
    #left, top, width, height

    clock = pygame.time.Clock()

    start_time = time.time() #current time when the game started

    elapsed_time = 0 

    star_add_increment = 2000 #time between each star

    star_count = 0 #number of stars

    star_colors = ["white","red", "green", "blue", "yellow"]

    stars = [] # list of stars

    lives = 3 #Start with 3 lives

    points = 0

    """ Start playing music with only one """

    pygame.mixer.music.play()

    while run:

        star_count += clock.tick(60) #60 frames per second

        if star_count > star_add_increment:
            for _ in range(1):
                star_x = random.randint(0, WIDTH - STAR_WIDTH) #random x position
                star = pygame.Rect(star_x, -STAR_HEIGTH, STAR_WIDTH, STAR_HEIGTH) #random y position
                color = random.choice(star_colors) #Assign a random color
                stars.append((star, color))

            star_add_increment = max (200, star_add_increment - 50) #decrease the time between each star
        
            star_count = 0

        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        
        #Move the player
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
            
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL


        hit = False 
        for star, color in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove((star,color))
                lives -= 1 #Decrease lives 

                if lives <= 0:
                    lost_text = FONT.render("You Lost!", 1, "white")
                    WIN.blit (
                        lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2)
                    )
                    pygame.display.update() #update the display
                    pygame.time.delay(4000) #wait for 4 seconds
                    run = False
                    break
        
            elif star.y + star.height >= player.y and star.colliderect(player):  # Collision check
                stars.remove((star,color))  # Remove the star (but no penalty)

                points += 1 #Increase points
                if points >= 10:

                    win_text = FONT.render("YEAH! You DID IT!", 1, "green")

                    WIN.blit(
                        win_text, (WIDTH / 2 - win_text.get_width() / 2, HEIGHT / 2 - win_text.get_height() / 2)
                    )

                    pygame.display.update()
                    pygame.time.delay(4000)
                    run = False
                    break

        draw(player, elapsed_time, stars, lives, points)

    pygame.quit() 

if __name__ == "__main__":
    main()

""" I learn the code from this youtube: https://www.youtube.com/watch?v=RuTmd4g5K8Q&t=1206s"""