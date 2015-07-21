
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


class ustvnowPlayer(xbmc.Player):


    def __init__( self, *args, **kwargs ):
        xbmc.Player.__init__( self )
        self.isExit = 0

    def setChannels(self, channels):
        self.channels = channels
        self.current = 1

    def setCurrent(self, current):
        self.current = current

    def up(self):
        print "PLAYER UPX\n"
        self.stop()
        self.play(self.channels[self.current]['url'])

        return
    #    if self.current == len(self.channels) -1:
   #         self.current = 1
  #      else:
 #           self.current += 1

#        self.playChannel()

    def down(self):
        if self.current == 1:
            self.current = len(self.channels) -1
        else:
            self.current -= 1

        self.playChannel()

    def getChannelName(self):
        return self.channels[self.current]['name']

    def getShowName(self):
        return self.channels[self.current]['now']['title']

    def playChannel(self):
        self.play(self.channels[self.current]['url'])

    def setIsExit(self,value):
        self.isExit = value

    def onPlayBackStarted(self):
        print "PLAYBACK STARTED"

    def onPlayBackEnded(self):
        print "PLAYBACK ENDED"
        xbmc.sleep(1000)
        if self.isExit == 0:
            self.playChannel()

    def onPlayBackStopped(self):
        print "PLAYBACK STOPPED"
        xbmc.sleep(1000)
#        if self.isExit == 0:
#            self.playChannel()
        return

    def onPlayBackPaused(self):
        print "PLAYBACK Paused"

