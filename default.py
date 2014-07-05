'''
    ustvnow XBMC Plugin
    Copyright (C) 2011 t0mm0

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

from resources.lib import Addon, ustvnow
from resources.lib import ustvnowPlayer
from resources.lib import tvWindow

import sys
import urllib
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

Addon.plugin_url = sys.argv[0]
Addon.plugin_handle = int(sys.argv[1])
Addon.plugin_queries = Addon.parse_query(sys.argv[2][1:])

email = Addon.get_setting('email')
password = Addon.get_setting('password')
ustv = ustvnow.Ustvnow(email, password)

Addon.log('plugin url: ' + Addon.plugin_url)
Addon.log('plugin queries: ' + str(Addon.plugin_queries))
Addon.log('plugin handle: ' + str(Addon.plugin_handle))

mode = Addon.plugin_queries['mode']

settingMode = Addon.get_setting('settingMode')
controlMode = Addon.get_setting('controlMode')


addon = xbmcaddon.Addon(id='plugin.video.ustvnow')


#added by ddurdle
try:

    remote_debugger = Addon.get_setting('remote_debugger')
    remote_debugger_host = Addon.get_setting('remote_debugger_host')

    # append pydev remote debugger
    if remote_debugger == 'true':
        # Make pydev debugger works for auto reload.
        # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
        import pysrc.pydevd as pydevd
        # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace(remote_debugger_host, stdoutToServer=True, stderrToServer=True)
except ImportError:
    log(Addon.get_string(30016), True)
    sys.exit(1)
except :
    pass


if mode == 'main':
    Addon.log(mode)

    if settingMode == 'true':
        stream_type = ['rtmp', 'rtsp'][int(Addon.get_setting('stream_type'))]
        channels = ustv.get_channels(int(Addon.get_setting('quality')),
                                     stream_type)

        player = ustvnowPlayer.ustvnowPlayer()
        player.setChannels(channels)

        w = tvWindow.tvWindow("tvWindow.xml",addon.getAddonInfo('path'),"Default")
        w.setPlayer(player)
        w.doModal()


    Addon.add_directory({'mode': 'live'}, Addon.get_string(30001))
    Addon.add_directory({'mode': 'recordings'}, Addon.get_string(30002))

elif mode == 'live':
    Addon.log(mode)
    stream_type = ['rtmp', 'rtsp'][int(Addon.get_setting('stream_type'))]
    channels = ustv.get_channels(int(Addon.get_setting('quality')),
                                     stream_type)
    if controlMode == 'true':

        for c in channels:
            Addon.add_directory({'mode': 'play', 'name': c['name']},
                             '%s - %s' % (c['name'], c['now']['title']))


    else:
        for c in channels:
            Addon.add_video_item(c['url'],
                             {'title': '%s - %s' % (c['name'],
                                                    c['now']['title']),
                              'plot': c['now']['plot']},
                             img=c['icon'])

elif mode == 'recordings':
    Addon.log(mode)
    stream_type = ['rtmp', 'rtsp'][int(Addon.get_setting('stream_type'))]
    recordings = ustv.get_recordings(int(Addon.get_setting('quality')),
                                     stream_type)
    for r in recordings:
        cm_del = (Addon.get_string(30003),
                  'XBMC.RunPlugin(%s/?mode=delete&del=%s)' %
                       (Addon.plugin_url, urllib.quote(r['del_url'])))
        title = '%s (%s on %s)' % (r['title'], r['rec_date'], r['channel'])
        Addon.add_video_item(r['stream_url'], {'title': title,
                                               'plot': r['plot']},
                             img=r['icon'], cm=[cm_del], cm_replace=True)

elif mode == 'delete':
    dialog = xbmcgui.Dialog()
    ret = dialog.yesno(Addon.get_string(30000), Addon.get_string(30004),
                       Addon.get_string(30005))
    if ret == 1:
        ustv.delete_recording(Addon.plugin_queries['del'])

elif mode=='play':
    name = Addon.plugin_queries['name']
    try:
       stream_type = 'rtmp'
       channels = []
       quality = int(Addon.get_setting('quality'))
       channels = ustv.get_channels(quality,stream_type)

       if controlMode == 'true':

         count = -1
         for c in channels:
           count += 1

           Addon.add_directory({'mode': 'play', 'name': c['name']},
                             '%s - %s' % (c['name'], c['now']['title']))
           if c['name'] == name:

                 player = ustvnowPlayer.ustvnowPlayer()
                 player.setChannels(channels)
                 player.setCurrent(count)

                 w = tvWindow.tvWindow("tvWindow.xml",addon.getAddonInfo('path'),"Default")
                 w.setPlayer(player)
                 w.doModal()
       else:
           for c in channels:
            if c['name'] == name:
                 print "URL = "+c['url']
                 print "setResolvedUrl"
                 item = xbmcgui.ListItem(path=c['url'])
                 xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    except:
      pass

Addon.end_of_directory()


