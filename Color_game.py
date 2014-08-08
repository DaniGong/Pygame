import pygame,random,sys,time,threading,os
from pygame.locals import *
from random import randint

pygame.init()

RESOLUTION = [360,360]
WELCOME_FONT = pygame.font.Font('freesansbold.ttf', 30)
TIME_FONT = pygame.font.Font('freesansbold.ttf', 30)
STAGE_FONT = pygame.font.Font('freesansbold.ttf', 15)

locationgroup = ([0,0])
y=56
for lo_x in range(1,9):
    x=56
    for lo_y in range(1,9):
        locationgroup.append([x,y])
        x=x+31
    y=y+31    
    
locationgroup.remove(0)
locationgroup.remove(0)

# print locationgroup

def wait_enter_pressed(keys):
    "block the screen to wait a keyborad event"
    while True:
        e = pygame.event.wait()
        if e.type == KEYUP and e.key in keys:
            break
        elif e.type == QUIT:
            pygame.quit()
            sys.exit()
            return

def bingo(e,dif_x,dif_y):
        
        if e.type == MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            mouse_x = pos[0]
            mouse_y = pos[1]
            if mouse_x>dif_x and mouse_x<dif_x+30 and mouse_y>dif_y and mouse_y<dif_y+30:
                print "Bingo"
                return True
            else :
                return False    

def update_highscore(curscore):
    if not os.path.exists('C:\highscore'):
        f0=open('C:\highscore.txt','w')
        f0.close()
    f1=open('C:\highscore.txt','r')             
    content = f1.readline()
    if content == '':
        content = '0'
    highscore = int(content)
    f1.close()
    if highscore < curscore:
        highscore = curscore
        content = str(highscore)
        f2=open('C:\highscore.txt','w')
        f2.write(content)
        f2.close()
        return highscore
    return highscore    


class square(pygame.sprite.Sprite):
    def __init__(self,color,initial_position):
        pygame.sprite.Sprite.__init__(self)
        # self.group=group
        self.image = pygame.Surface([30, 30])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position



class timer(threading.Thread):
    def __init__(self,num,interval,limit):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.limit = limit
        self.thread_stop = False

    def  run(self):
    	
        while not self.thread_stop:
            print str(self.limit)
            time.sleep(self.interval)
            self.limit = self.limit - self.interval

            
    def  stop(self):
        self.thread_stop = True
            


class Game:
    def __init__(self):
        pygame.init()
        dif_x = 0
        dif_y = 0
        cur_stage = 0
        highscore = 0
        screen=pygame.display.set_mode(RESOLUTION,0)
        pygame.display.set_caption('Color Game')
        background=pygame.Surface(screen.get_size())
        background.fill((0,0,0)) 
        self.dif_x = dif_x
        self.dif_y = dif_y
        self.screen = screen
        self.is_started = False
        self.cur_stage = cur_stage
        self.highscore = highscore
        self.background = background
        self.welcome_font = WELCOME_FONT
        self.time_font = TIME_FONT
        self.stage_font = STAGE_FONT
    def create_stage(self):
        main_color_R = randint(1,254)
        main_color_G = randint(1,254)
        main_color_B = randint(1,224)
        dif_color_B = main_color_B+20

        Squaregroup=pygame.sprite.Group()

        rand_a = randint(1,64)

        self.dif_x = rand_a % 8 * 31 + 56

        self.dif_y = rand_a / 8 * 31 + 56

        for a in range(0,64):
            if a==rand_a:
                Squaregroup.add(square([main_color_R,main_color_G,dif_color_B],locationgroup[a]))
            else:
                Squaregroup.add(square([main_color_R,main_color_G,main_color_B],locationgroup[a]))
            
        for squarelist in Squaregroup.sprites():
            self.screen.blit(squarelist.image,squarelist.rect)
        self.cur_stage = self.cur_stage + 1
        stage = self.stage_font.render('Stage:' + str(self.cur_stage) , True , (255,255,255), (0,0,0))
        self.screen.blit(stage , (0,0))
        pygame.display.update()

    def welcome(self):
        self.screen.blit(self.background , (0,0))   
        self._print_message("press Enter to start") 
        pygame.display.flip()

    def _print_message(self,message):
        text = self.welcome_font.render(message , True ,(255,255,255), (0,0,0) )    
        textpos = text.get_rect(centerx=self.background.get_width() / 2, centery=self.background.get_height() / 2)
        self.screen.blit(text , textpos)

    def _print_curscore(self):
        curscore = self.stage_font.render('Your Score: ' + str(self.cur_stage),True,(255,255,255),(0,0,0))
        curscorepos = curscore.get_rect(centerx=self.background.get_width() / 2, centery=self.background.get_height() / 2)
        self.screen.blit(curscore, curscorepos)

    def _print_highscore(self):
        highscore = self.stage_font.render('High Score: ' + str(self.highscore),True,(255,255,255),(0,0,0))
        highscorepos = highscore.get_rect(centerx=self.background.get_width() / 2, centery=self.background.get_height() / 2 + 30)
        self.screen.blit(highscore, highscorepos)    

    def update_time(self,timer):
        time_l = repr(timer.limit)
        limit_num = self.time_font.render(time_l, True, (255,255,255), (0,0,0)) 
        self.screen.blit(limit_num, (165, 10))
        pygame.display.update()

    def start(self):
        self.screen.blit(self.background , (0,0))
        pygame.display.flip()
        self.is_started = True    

    def stop(self):
        self.is_started = False
        self.highscore = update_highscore(self.cur_stage)
        self.screen.blit(self.background , (0,0))
        self._print_highscore()
        self._print_curscore()
        pygame.display.flip()


def main():
    while True:
        game = Game()
        game.welcome()
        wait_enter_pressed((13,K_SPACE))
        timer1 = timer(1,1,30)
        game.start()
        timer1.start()
        game.create_stage()
        while timer1.limit>0:        
            game.update_time(timer1)
            for e in pygame.event.get():
                if bingo(e,game.dif_x,game.dif_y):
                    game.create_stage()
                elif e.type==QUIT:
                    pygame.quit()
                    sys.exit()    
        timer1.stop()
        game.stop() 
        time.sleep(3)    
                 
    
          
  


if __name__ == '__main__':main()
