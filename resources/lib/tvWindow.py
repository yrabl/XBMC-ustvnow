'''
    ustvnow XBMC Plugin
    Copyright (C) 2013 ddurdle

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import re
import urllib, urllib2

import xbmc, xbmcaddon, xbmcgui, xbmcplugin

addon = xbmcaddon.Addon(id='plugin.video.ustvnow')

def log(msg, err=False):
    if err:
        xbmc.log(addon.getAddonInfo('name') + ': ' + msg.encode('utf-8'), xbmc.LOGERROR)
    else:
        xbmc.log(addon.getAddonInfo('name') + ': ' + msg.encode('utf-8'), xbmc.LOGDEBUG)


class tvWindow(xbmcgui.WindowXMLDialog):


    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs)
        self.isVisible = False


    def setPlayer(self, player):
        self.player = player

    def onAction(self, action):
        actionID = action.getId()

        #backout
        if actionID in (9, 10, 92, 216, 247, 257, 275, 61467, 61448):
            prompt = xbmcgui.Dialog()

            if prompt.yesno("USTVNOW", "Exit?"):
                self.player.setIsExit(1)
                self.player.stop()
                self.close()
                return
            del prompt

        #pause/unpause
        elif actionID == 12:
            self.pause()

        #up arrow
        elif actionID == 3:
#            self.getControl(100).setVisible(True)
            print "PLAYER UP\n"
            self.close()

            #self.player.up()
            print "PLAYER UP\n"
#            self.getControl(103).setLabel(self.player.getChannelName())
#            self.getControl(104).setLabel(self.player.getShowName())
#            while not self.player.isPlaying():
#                xbmc.sleep(1000)
#            self.getControl(100).setVisible(False)
#            self.getControl(101).setVisible(True)
#            self.close()

        #down arrow
        elif actionID == 4:
            self.getControl(100).setVisible(True)
            self.player.down()
            self.getControl(103).setLabel(self.player.getChannelName())
            self.getControl(104).setLabel(self.player.getShowName())
            while not self.player.isPlaying():
                xbmc.sleep(1000)
            self.getControl(100).setVisible(False)
            self.getControl(101).setVisible(True)

        elif actionID == 7:
            self.isVisible = not self.isVisible
            self.getControl(101).setVisible(self.isVisible)
        print "XXXX UP\n"

        #self.show()
#        self.doModal()

 #       return

    def onInit(self):
        self.isVisible = False
        self.getControl(101).setVisible(self.isVisible)
        self.getControl(100).setVisible(self.isVisible)
        self.player.playChannel()
        self.getControl(103).setLabel(self.player.getChannelName())
        self.getControl(104).setLabel(self.player.getShowName())
        while not self.player.isPlaying():
                xbmc.sleep(1000)

