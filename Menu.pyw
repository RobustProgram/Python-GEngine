import os, sys, pygame, math

class GMenu:
    def __init__(self,menutype,items,width,height,drawscreen,toplogo=None):
        self.menutype = menutype #menutype means what type the menu will be
        #menutypes
        #0 = mainMenu
        #1 = subMenu
        self.items = items #the menu items/buttons that are added
        self.screen = drawscreen #the screen
        self.width = width #width of the button
        self.height = height #height of the button
        self.button_list = [] #list of the buttons created
        self.text_list = [] #list of texts for the buttons
        self.toplogo = toplogo #the logo that is shown on top of the menu
        self.makeButtons()

    #makeButtons makes the buttons for the menu. It automatically takes in the number of menu items and uses it to dynamically create the menu
    def makeButtons(self):
        if self.menutype == 0:
            if self.toplogo != None:
                self.toplogoimage = pygame.image.load(self.toplogo)
                self.toplogoimage = pygame.transform.scale(self.toplogoimage,(400,100))
            item_no = len(self.items) #the number of menu items
            x,y = self.screen.get_size() #the size of the screen
            button_pos_x = (x/2) - (self.width/2) #the default x coordinates of the button (can be subjected to change)
            button_pos_y = (y/2) - (self.height/2) #the default y coordinates of the button (can be subjected to change)
            button_y_increment_amount = (self.height + 6) #the amount the y coordinates of the button increments by
            button_pos_y -= button_y_increment_amount * math.trunc(item_no/2) #sets the first button's y coordinates

            #loops through all of the menu items and add them to the button list all the while changing their coords
            for a in range(len(self.items)):
                button_Rect = pygame.Rect(button_pos_x,button_pos_y,self.width,self.height)
                self.button_list.append(button_Rect)
                self.text_list.append(self.items[a])
                button_pos_y += button_y_increment_amount
        elif self.menutype == 1:
            item_no = len(self.items)
            x,y = self.screen.get_size()
            button_pos_y  = (y - 20) - (self.height/2)
            button_pos_x = (x/2) - (self.width/2)
            button_x_increment_amount = (self.width + 10)
            button_pos_x -= button_x_increment_amount * int(item_no/2)

            for a in range(len(self.items)):
                button_Rect = pygame.Rect(button_pos_x,button_pos_y,self.width,self.height)
                self.button_list.append(button_Rect)
                self.text_list.append(self.items[a])
                button_pos_x += button_x_increment_amount

    #draws the buttons and adds effect to them (hover over effects)
    def drawButtons(self,event):
        final_button = -1
        mx,my = pygame.mouse.get_pos()
        x,y = self.screen.get_size() #the size of the screen

        if pygame.font:
            font = pygame.font.Font(None, 17)
        #loops through all the buttons
        for a in range(len(self.button_list)):
            button_pos_x,button_pos_y,_,_ = self.button_list[a];
            text_pos_x = button_pos_x + self.width/2
            text_pos_y = button_pos_y + self.height/2
            
            #checks if the mouse is hovering over the button by checking its x and y coordinates
            if((mx < (button_pos_x + self.width)) and (mx > button_pos_x) and (my < (button_pos_y + self.height)) and (my > button_pos_y)):
                button = pygame.draw.rect(self.screen,(200,255,0),self.button_list[a])
                text = font.render(self.text_list[a],1,(0,0,0))
                textpos = text.get_rect(centerx = text_pos_x,centery = text_pos_y)
                self.screen.blit(text,textpos)
                if(event.type == pygame.MOUSEBUTTONUP):
                    final_button = a
            else:
                button = pygame.draw.rect(self.screen,(255,255,255),self.button_list[a])
                text = font.render(self.text_list[a],1,(0,0,0))
                textpos = text.get_rect(centerx = text_pos_x,centery = text_pos_y)
                self.screen.blit(text,textpos)
        if self.toplogo != None:
            toplogoimagepos = self.toplogoimage.get_rect(centerx = x/2,centery = 70) #position of the top logo image
            self.screen.blit(self.toplogoimage,toplogoimagepos)
        return final_button

#BestOCEPlayer
#abcd123
