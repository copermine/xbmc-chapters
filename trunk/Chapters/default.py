import sys
import os
import xbmc
import string

__scriptname__ = "Chapters"
__author__ = "Turhan Aydin"
__url__ = "http://code.google.com/p/xbmc-chapters/"
__svn_url__ = "http://xbmc-chapters.googlecode.com/svn/trunk/"
__credits__ = ""
__version__ = "1.52"
__XBMC_Revision__ = "22240"
BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append ( BASE_RESOURCE_PATH )

__language__ = xbmc.Language( os.getcwd() ).getLocalizedString
_ = sys.modules[ "__main__" ].__language__
__settings__ = xbmc.Settings( path=os.getcwd() )

import gui
#############-----------------Is script runing from OSD? -------------------------------###############

if not xbmc.getCondVisibility('videoplayer.isfullscreen') :
    __settings__.openSettings()
else:
    window = False
    skin = "main"
    skin1 = str(xbmc.getSkinDir().lower())
    skin1 = skin1.replace("-"," ")
    skin1 = skin1.replace("."," ")
    skin1 = skin1.replace("_"," ")
    if ( skin1.find( "g720" ) > -1 ):
         skin = "g720"
    if ( skin1.find( "confluence" ) > -1 ):
         skin = "confluence"     
  
    try: xbox = xbmc.getInfoLabel( "system.xboxversion" )
    except: xbox = ""
    if xbox != "" and len(skin) > 13:
      skin = skin.ljust(13)

    if __settings__.getSetting( "debug" ) == "true":     
        print "Chapters version [" +  __version__ +"]"
        print "Skin Folder: [ " + skin1 +" ]"
        print "Chapters skin XML: [ " + skin +" ]"
        debug = True
    else:
        debug = False   
    debug = True
 
    #splitlist = "foo.helloworld.exe".split(".")
    #>>> splitlist[len(splitlist) - 1]
    # '.'.join(splitlist[0: len(splitlist) - 1])
    mediafolder = xbmc.translatePath("special://home/scripts/" + __scriptname__ + "/resources/skins/Default/media")

    
    """
        path            - Full Path to Movie File (excluding filename)
        movieFullPath   - Full Path to Movie File (including filename)
        movieHalfPath   - Full Path to Movie File without extension
    """

    if ( __name__ == "__main__" ):   
        path = ""
        chaptersFile = ""
     
        movieFullPath = xbmc.Player().getPlayingFile()
        
        path = os.path.dirname( movieFullPath )
        passChapters = False
        xbmc.output( "%s: %s\n" % ( "INFO", "NOW PLAYING: " + movieFullPath  ) )
        
        # 16:30:42 T:1044 M:373161984  NOTICE: INFO: NOW PLAYING: stack://G:\data\babytv\The Cars\The Cars.CD1.avi , G:\data\babytv\The Cars\The Cars.CD2.avi
#16:30:42 T:1044 M:373002240  NOTICE: INFO: setParameters : [stack://G:\data\babytv\The Cars\The Cars.CD1.avi , G:\data\babytv\The Cars\The Cars.CD2.chapter.xml]
#16:30:42 T:1848 M:372908032   ERROR: XFILE::CDirectory::GetDirectory - Error getting ?
#16:30:42 T:1848 M:372903936   ERROR: CGUIMediaWindow::GetDirectory(?) failed
#16:30:42 T:1044 M:372330496   ERROR: CThread::staticThread : Access violation at 0x1e080ca8: Reading location 0x00000020
        
        # Pass Chapter search for particular locations
        
        if (movieFullPath.find("http://") > -1 ):
            passChapters = True

        if (movieFullPath.find("rar://") > -1 ):
            passChapters = True
        
        if (movieFullPath.find("stack://") > -1 ):
            movieFullPath = movieFullPath.replace('stack://', '').split(' , ')
            movieFullPath = movieFullPath[0]
                
        splitlist = movieFullPath.split(".")
        movieHalfPath = '.'.join(splitlist[0: len(splitlist) - 1])
#### ------------------------------ Get the main window going ---------------------------#####
        chapter_data = ""
        chaptersPath = movieFullPath + ".chapter.xml"
        # Look for XML Filees
        if os.path.exists(movieHalfPath + ".chapter.xml"):
            chaptersFile = movieHalfPath + ".chapter.xml"
        elif os.path.exists(movieFullPath + ".chapter.xml"):
            chaptersFile = movieFullPath + ".chapter.xml"
        elif os.path.exists(str(path) + "chapter.xml"):
            chaptersFile = str(path) + "chapter.xml"
        
        #Look For TXT Files
        elif os.path.exists(movieHalfPath + ".chapter.txt"):
            chaptersFile = movieHalfPath + ".chapter.txt"
        elif os.path.exists(movieFullPath + ".chapter.txt"):
            chaptersFile = movieFullPath + ".chapter.txt"
        elif os.path.exists(str(path) + "/chapter.txt"):
            chaptersFile = str(path) + "/chapter.txt"
        else :
            passChapters = True
        
        # Show Chapters Window if find some chapters
        if not passChapters:
            if not xbmc.getCondVisibility('Player.Paused') : 
                xbmc.Player().pause() # Pause Player if not paused
            
            ui = gui.GUI( "main.xml" , os.getcwd(), "Default")
            service_present = ui.setParameters ( movieFullPath, chaptersFile,  debug )
            if service_present > -1 : ui.doModal()
            #xbmc.executebuiltin('XBMC.ActivateWindow(20000)' )
            if xbmc.getCondVisibility('Player.Paused'): 
                xbmc.Player().pause() # Start Playing if Paused
            del ui
        else :
            xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s)' % ( "No Chapters", "No chapters available for video", 2000) )
        sys.modules.clear()
