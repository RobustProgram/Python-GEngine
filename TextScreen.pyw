import Menu
import pygame

class TextScreen(Menu.GMenu):
    def __init__(self,buttonlist,paragraph,screen):
        pygame.font.init()
        self.Menu = Menu.GMenu(1,buttonlist,100,25,screen)
        self.paragraph = paragraph
        self.screen = screen
        self.text = []
        self.FONT = pygame.font.SysFont("Arial",18)
        self.renderParagraph = []
        self.parseText()

    def parseText(self):
        self.text = self.paragraph.split('\n')
        for sentence in self.text:
            if "<b>" in sentence:
                self.FONT.set_bold(True)
                sentence = sentence.replace("<b>","")
            renderSentence = self.FONT.render(sentence,4,(255,255,255))
            self.renderParagraph.append(renderSentence)
            if self.FONT.get_bold:
                self.FONT.set_bold(False)

    def drawText(self,event):
        for x in range(len(self.renderParagraph)):
            self.screen.blit(self.renderParagraph[x],(0,18 * x))
        return self.Menu.drawButtons(event)
