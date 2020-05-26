from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from .forms import UserForm
import matplotlib.pyplot as plt
from pandas_datareader import data
import pandas as pd
import numpy as np
import yfinance as yahoo
from matplotlib import pyplot as plt
from .forms import ContactForm


def myView(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            Ticker1 = form.cleaned_data.get("Ticker1")
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")

            # Boomsblerg formatting
            plt.style.use(['dark_background'])
            # plt.rcParams['axes.facecolor'] = 'navy'
            # 1st ticker
            var1 = str(Ticker1)[1:-1]
            g1 = var1.strip('"\'')
            lable1 = yahoo.Ticker(g1)
            panel_data1 = data.DataReader(
                Ticker1, 'yahoo', start_date, end_date)
            panel_data1.head()
            close1 = panel_data1['Close']
            all_weekdays = pd.date_range(
                start=start_date, end=end_date, freq='B')
            close1 = close1.reindex(all_weekdays)
            close1 = close1.fillna(method='ffill')

            listToStr = ' '.join([str(elem) for elem in Ticker1])
            # company_name1 = lable1.info['longName']
            bbf = yahoo.Ticker(Ticker1)
            ffb = bbf.info['longName']

            # Define Variables
            # Define Variables
            d = panel_data1['Volume']
            c = panel_data1['Adj Close']
            t = panel_data1['High']
            s = panel_data1['Low']
            vol = panel_data1['Volume']
            vol3 = (vol/1000000)  # Trading volume graph adjustment
            vol2 = vol3.values.tolist()
            y = np.array(vol2)
            bg = c.values.tolist()
            big = np.array(bg)
            x = np.array(panel_data1.index)

            # Percent Change Box
            pc = panel_data1['Adj Close'].pct_change()
            bc = pc.cumsum()
            g = (bc.iloc[-1])
            j = (g*100)
            pchange = round(j, 1)
            plt.text(.83, .40, "Percent Change: {}%".format(pchange),
                     bbox={'facecolor': 'k', 'pad': 5, },
                     ha="left", va="bottom", color='limegreen' if pchange >= 0 else 'r',
                     transform=plt.gca().transAxes)

            # Plotting

            plt.plot(x, big, label='Adjusted Close Price',
                     color='lime', linewidth=1.50)
            plt.plot(t, linestyle='--', label="Day High",
                     color='deeppink', linewidth=0.75)
            plt.plot(s, linestyle='--', label="Day Low", linewidth=0.75)
            plt.bar(x, y, color='darkturquoise', label='Trading Volume (Millions)',
                    alpha=0.8)

            # Formatting
            plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)
            plt.grid(linestyle='--', linewidth=0.5, color='#2A3459')
            plt.locator_params(axis='x', nbins=10)
            linestyle_tuple = [('dotted',                (0, (1, 1))), ]
            plt.fill_between(x, big, alpha=0.15, color='pink')
            plt.ylim(auto=True)
            plt.ylabel('Share Value ($)')
            plt.title(ffb, fontname='bold')

            plt.show()

    form = UserForm()

    if request.method == "POST" and 'run_script' in request.POST:
        import pygame
        from random import randint
        import math
        import sys

        pygame.init()

        # Define some colors
        GRASS = (102, 205, 0)
        WHITE = (255, 255, 255)
        GREY = (100, 100, 100)
        BLACK = (0, 0, 0)

        class Paddle(pygame.sprite.Sprite):
            # This class represents a paddle. It derives from the "Sprite" class in Pygame.

            def __init__(self, color, width, height):
                # Call the parent class (Sprite) constructor
                super().__init__()

                # Pass in the color of the paddle, and its x and y position, width and height.
                # Set the background color and set it to be transparent
                self.image = pygame.Surface([width, height])
                self.image.fill(BLACK)
                self.image.set_colorkey(BLACK)

                # Draw the paddle (a rectangle!)
                pygame.draw.rect(self.image, color, [0, 0, width, height])

                # Fetch the rectangle object that has the dimensions of the image.
                self.rect = self.image.get_rect()

            def moveUp(self, pixels):
                self.rect.y -= pixels
                # Check that you are not going too far (off the screen)
                if self.rect.y < 0:
                    self.rect.y = 0

            def moveDown(self, pixels):
                self.rect.y += pixels
                # Check that you are not going too far (off the screen)
                if self.rect.y > 400:
                    self.rect.y = 400

            def moveLEFT(self, pixels):
                self.rect.x -= pixels
                # Check that you are not going too far (off the screen)
                if self.rect.x < 0:
                    self.rect.x = 0

            def moveRIGHT(self, pixels):
                self.rect.x += pixels
                # Check that you are not going too far (off the screen)
                if self.rect.x > 690:
                    self.rect.x = 690

        class Ball(pygame.sprite.Sprite):
            # This class represents a ball. It derives from the "Sprite" class in Pygame.

            def __init__(self, color, width, height):
                # Call the parent class (Sprite) constructor
                super().__init__()

                # Pass in the color of the ball, its width and height.
                # Set the background color and set it to be transparent
                self.image = pygame.Surface([width, height])
                self.image.fill(BLACK)
                self.image.set_colorkey(BLACK)

                # Draw the ball (a rectangle!)
                pygame.draw.rect(self.image, color, [0, 0, width, height])

                self.velocity = [randint(4, 8), randint(-8, 8)]

                # Fetch the rectangle object that has the dimensions of the image.
                self.rect = self.image.get_rect()

            def update(self):
                self.rect.x += self.velocity[0]
                self.rect.y += self.velocity[1]

            def bounce(self):
                self.velocity[0] = -self.velocity[0]
                self.velocity[1] = randint(-8, 8)

        # Open a new window
        size = (700, 500)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Pong Soccer")

        paddleA = Paddle(WHITE, 10, 90)
        paddleA.rect.x = 20
        paddleA.rect.y = 200

        paddleB = Paddle(WHITE, 10, 90)
        paddleB.rect.x = 670
        paddleB.rect.y = 200

        ball = Ball(WHITE, 10, 10)
        ball.rect.x = 345
        ball.rect.y = 195

        game_over = False
        # This will be a list that will contain all the sprites we intend to use in our game.
        all_sprites_list = pygame.sprite.Group()

        # Add the car to the list of objects
        all_sprites_list.add(paddleA)
        all_sprites_list.add(paddleB)
        all_sprites_list.add(ball)

        # The loop will carry on until the user exit the game (e.g. clicks the close button).
        carryOn = True

        # The clock will be used to control how fast the screen updates
        clock = pygame.time.Clock()

        # Initialise player scores
        scoreA = 0
        scoreB = 0

        # -------- Main Program Loop -----------
        while carryOn:
            # --- Main event loop
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    carryOn = False  # Flag that we are done so we exit this loop
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                        carryOn = False

            # Moving the paddles when the use uses the arrow keys (player A) or "W/S" keys (player B)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                paddleA.moveUp(5)
            if keys[pygame.K_s]:
                paddleA.moveDown(5)
            if keys[pygame.K_UP]:
                paddleB.moveUp(5)
            if keys[pygame.K_DOWN]:
                paddleB.moveDown(5)
            if keys[pygame.K_a]:
                paddleA.moveLEFT(5)
            if keys[pygame.K_d]:
                paddleA.moveRIGHT(5)
            if keys[pygame.K_LEFT]:
                paddleB.moveLEFT(5)
            if keys[pygame.K_RIGHT]:
                paddleB.moveRIGHT(5)

            # --- Game logic should go here
            all_sprites_list.update()

            # define game reset
            def resetBall():
                ball.rect.x = 350
                ball.rect.y = 250
                ballAngle = math.radians(0)
                ballSpeed = 10
                ballDirection = -1

            # Set walls and goals, set score and game reset:
            if ball.rect.x >= 690:
                ball.velocity[0] = -ball.velocity[0]
            if ball.rect.x <= 0:
                ball.velocity[0] = -ball.velocity[0]
            if ball.rect.y > 490:
                ball.velocity[1] = -ball.velocity[1]
            if ball.rect.y < 0:
                ball.velocity[1] = -ball.velocity[1]
            if ball.rect.x >= 690 and ball.rect.y >= 150 and ball.rect.y <= 350:
                scoreA += 1
                resetBall()
            if ball.rect.x <= 0 and ball.rect.y >= 150 and ball.rect.y <= 350:
                scoreB += 1
                resetBall()
            # Detect collisions between the ball and the paddles
            if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
                ball.bounce()
            if scoreA >= 10 or scoreB >= 10:
                game_over = True
            # --- Drawing code should go here
            # First, clear the screen to black.
            screen.fill(GRASS)
            # Draw the field
            pygame.draw.line(screen, WHITE, [350, 0], [350, 500], 5)
            pygame.draw.line(screen, WHITE, [5, 0], [5, 500], 5)
            pygame.draw.line(screen, WHITE, [695, 0], [695, 500], 5)
            pygame.draw.circle(screen, WHITE, [350, 250], 68, 5)
            pygame.draw.rect(screen, WHITE, (5, 90, 125, 310), 5)
            pygame.draw.rect(screen, WHITE, (570, 90, 125, 310), 5)
            pygame.draw.line(screen, GREY, [695, 150], [695, 350], 8)
            pygame.draw.line(screen, GREY, [5, 150], [5, 350], 8)
            # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
            all_sprites_list.draw(screen)

            # Display scores:
            font = pygame.font.Font(None, 74)
            text = font.render(str(scoreA), 1, WHITE)
            screen.blit(text, (250, 10))
            text = font.render(str(scoreB), 1, WHITE)
            screen.blit(text, (420, 10))

            if game_over:
                # If game over is true, draw game over
                text = font.render("Game Over", True, BLACK)
                text_rect = text.get_rect()
                text_x = screen.get_width() / 2 - text_rect.width / 2
                text_y = screen.get_height() / 2 - text_rect.height / 2
                screen.blit(text, [text_x, text_y])
                pygame.time.delay(100)

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            clock = pygame.time.Clock()
            clock.tick(100)

        # Once we have exited the main program loop we can stop the game engine:
        pygame.quit()

    return render(request, 'Home.css', {'form': form})
