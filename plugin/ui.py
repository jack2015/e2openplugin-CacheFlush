# for localized messages  	 
from . import _

from Screens.Screen import Screen
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.config import ConfigYesNo, ConfigSelection, ConfigInteger, config, getConfigListEntry
from Components.ActionMap import ActionMap
from Components.Label import Label
from os import system
from enigma import eTimer, getDesktop
from Components.ProgressBar import ProgressBar

from plugin import VERSION

FHD = False
if getDesktop(0).size().width() >= 1920:
	FHD = True

config.plugins.CacheFlush.enable = ConfigYesNo(default = False)
config.plugins.CacheFlush.type = ConfigSelection(default = "3", choices = [("1",_("pagecache")),("2",_("dentries and inodes")),("3",_("pagecache, dentries and inodes"))])
config.plugins.CacheFlush.sync = ConfigYesNo(default = False)

NGETTEXT = False
try:	# can be used ngettext ?
	ngettext("%d minute", "%d minutes", 5)
	NGETTEXT = True
except Exception, e:
	print "[CacheFlush] ngettext is not supported:", e
choicelist = []
for i in range(5, 151, 5):
	if NGETTEXT:
		choicelist.append(("%d" % i, ngettext("%d minute", "%d minutes", i) % i))
	else:
		choicelist.append(("%d" % i))
config.plugins.CacheFlush.timeout = ConfigSelection(default = "30", choices = choicelist)
config.plugins.CacheFlush.scrinfo = ConfigYesNo(default = True)
choicelist = []
for i in range(1, 11):
	if NGETTEXT:
		choicelist.append(("%d" % i, ngettext("%d second", "%d seconds", i) % i))
	else:
		choicelist.append(("%d" % i))
config.plugins.CacheFlush.timescrinfo = ConfigSelection(default = "10", choices = choicelist)
choicelist = [("0",_("Default")),]
for i in range(1, 21):
	choicelist.append(("%d" % i, "%d kB" % (1024*i)))
config.plugins.CacheFlush.uncached = ConfigSelection(default = "1", choices = choicelist)
config.plugins.CacheFlush.free_default = ConfigInteger(default = 0, limits=(0,9999999999))
cfg = config.plugins.CacheFlush

# display mem, used, free and progressbar
ALL = 0x17

def dropCache():
	if cfg.sync.value:
		system("sync")
		print "[CacheFlush] sync"
	if cfg.type.value == "1":   # free pagecache
		system("echo 1 > /proc/sys/vm/drop_caches")
		print "[CacheFlush] free pagecache"
	elif cfg.type.value == "2": # free dentries and inodes
		system("echo 2 > /proc/sys/vm/drop_caches")
		print "[CacheFlush] free dentries and inodes"
	elif cfg.type.value == "3": # free pagecache, dentries and inodes
		system("echo 3 > /proc/sys/vm/drop_caches")
		print "[CacheFlush] free pagecache, dentries and inodes"

def getMinFreeKbytes():
	for line in open('/proc/sys/vm/min_free_kbytes','r'):
		line = line.strip()
	print "[CacheFlush] min_free_kbytes is %s kB" % line
	return line

def setMinFreeKbytes(size):
	system("echo %d > /proc/sys/vm/min_free_kbytes" % (size))
	print "[CacheFlush] set min_free_kbytes to %d kB" % size

class CacheFlushSetupMenu(Screen, ConfigListScreen):
	if FHD:
		skin = """
		<screen name="CacheFlush" position="center,center" size="1000,490" title="" backgroundColor="#31000000" >
			<widget name="config" position="10,10" size="980,400" font="Regular;30" itemHeight="38" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
			<ePixmap pixmap="skin_default/div-h.png" position="0,332" zPosition="2" size="1000,2" />
			<widget name="min_free_kb" font="Regular;28" position="20,345" size="960,35" zPosition="2" valign="center" backgroundColor="#31000000" transparent="1" />
			<widget name="memory" position="20,380" zPosition="2" size="960,35" valign="center" halign="left" font="Regular;28" transparent="1" foregroundColor="white" />
			<widget name="slide" position="20,415" zPosition="2" borderWidth="1" size="960,8" backgroundColor="dark" />
			<ePixmap pixmap="skin_default/div-h.png" position="0,435" zPosition="2" size="1000,2" />
			<widget name="key_red" position="0,450" zPosition="2" size="250,30" valign="center" halign="center" font="Regular;25" transparent="1" foregroundColor="red" />
			<widget name="key_green" position="250,450" zPosition="2" size="250,30" valign="center" halign="center" font="Regular;25" transparent="1" foregroundColor="green" />
			<widget name="key_yellow" position="500,450" zPosition="2" size="250,30" valign="center" halign="center" font="Regular;25" transparent="1" foregroundColor="yellow" />
			<widget name="key_blue" position="750,450" zPosition="2" size="250,30" valign="center" halign="center" font="Regular;25" transparent="1" foregroundColor="blue" />
		</screen>"""
	else:
		skin = """
		<screen name="CacheFlush" position="center,center" size="500,315" title="" backgroundColor="#31000000" >
			<widget name="config" position="10,10" size="480,200" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
			<ePixmap pixmap="skin_default/div-h.png" position="0,223" zPosition="2" size="500,2" />
			<widget name="min_free_kb" font="Regular;18" position="10,225" size="480,25" zPosition="2" valign="center" backgroundColor="#31000000" transparent="1" />
			<widget name="memory" position="10,245" zPosition="2" size="480,24" valign="center" halign="left" font="Regular;20" transparent="1" foregroundColor="white" />
			<widget name="slide" position="10,270" zPosition="2" borderWidth="1" size="480,8" backgroundColor="dark" />
			<ePixmap pixmap="skin_default/div-h.png" position="0,283" zPosition="2" size="500,2" />
			<widget name="key_red" position="0,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="red" />
			<widget name="key_green" position="120,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="green" />
			<widget name="key_yellow" position="240,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="yellow" />
			<widget name="key_blue" position="360,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="blue" />
		</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)

		self.onChangedEntry = [ ]
		self.list = [ ]
		ConfigListScreen.__init__(self, self.list, session = session, on_change = self.changedEntry)
		self.setup_title = _("Setup CacheFlush")
		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.keyCancel,
				"green": self.keySave,
				"ok": self.keySave,
				"red": self.keyCancel,
				"blue": self.freeMemory,
				"yellow": self.memoryInfo,
			}, -2)

		self["key_green"] = Label(_("Save"))
		self["key_red"] = Label(_("Cancel"))
		self["key_blue"] = Label(_("Clear Now"))
		self["key_yellow"] = Label(_("Info"))

		self["slide"] = ProgressBar()
		self["slide"].setValue(100)
		self["slide"].hide()
		self["memory"] = Label()
		self["min_free_kb"] = Label(_("Uncached memory: %s kB,   ( default: %s kB )") % ( getMinFreeKbytes(), str(cfg.free_default.value)))

		self.runSetup()
		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.setTitle(_("Setup CacheFlush") + "  " + VERSION)
		self["memory"].setText(self.getMemory(ALL))

	def runSetup(self):
		self.list = [ getConfigListEntry(_("Enable CacheFlush"), cfg.enable) ]
		if cfg.enable.value:
			autotext = _("Auto timeout")
			timetext = _("Time of info message")
			if not NGETTEXT:
				autotext = _("Auto timeout (5-150min)")
				timetext = _("Time of info message (1-10sec)")
			self.list.extend((
				getConfigListEntry(_("Cache drop type"), cfg.type),
				getConfigListEntry(_("Clean \"dirty\" cache too"), cfg.sync),
				getConfigListEntry(autotext, cfg.timeout),
				getConfigListEntry(_("Show info on screen"), cfg.scrinfo),
				getConfigListEntry(timetext, cfg.timescrinfo),
				getConfigListEntry(_("Display plugin in"), cfg.where),
			))
		self.list.extend((getConfigListEntry(_("Uncached memory size"), cfg.uncached),))

		self["config"].list = self.list
		self["config"].setList(self.list)

	def keySave(self):
		for x in self["config"].list:
			x[1].save()
#		configfile.save()
		self.setUncachedMemory()
		self.close()

	def keyCancel(self):
		for x in self["config"].list:
			x[1].cancel()
		self.close()

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		if self["config"].getCurrent()[1] == cfg.enable:
			self.runSetup()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		if self["config"].getCurrent()[1] == cfg.enable:
			self.runSetup()

	def changedEntry(self):
		for x in self.onChangedEntry:
			x()

	def freeMemory(self):
		dropCache()
		self["memory"].setText(self.getMemory(ALL))

	def getMemory(self, par=0x01):
		try:
			mm = mu = mf = 0
			for line in open('/proc/meminfo','r'):
				line = line.strip()
				if "MemTotal:" in line:
					line = line.split()
					mm = int(line[1])
				if "MemFree:" in line:
					line = line.split()
					mf = int(line[1])
					break
			mu = mm - mf
			self["memory"].setText("")
			self["slide"].hide()
			memory = ""
			if par&0x01:
				memory += "".join((_("Memory:")," %d " % (mm/1024),_("MB"),"  "))
			if par&0x02:
				memory += "".join((_("Used:")," %.2f%s" % (100.*mu/mm,'%'),"  "))
			if par&0x04:
				memory += "".join((_("Free:")," %.2f%s" % (100.*mf/mm,'%')))
			if par&0x10:
				self["slide"].setValue(int(100.0*mu/mm+0.25))
				self["slide"].show()
			return memory
		except Exception, e:
			print "[CacheFlush] getMemory FAIL:", e
			return ""

	def memoryInfo(self):
		self.session.openWithCallback(self.afterInfo, CacheFlushInfoScreen)

	def afterInfo(self, answer=False):
		self["memory"].setText(self.getMemory(ALL))

	def setUncachedMemory(self):
		if cfg.uncached.value == "0":
			setMinFreeKbytes(cfg.free_default.value)
		else:
			setMinFreeKbytes(int(cfg.uncached.value)*1024)

class CacheFlushAutoMain():
	def __init__(self):
		self.dialog = None
		if cfg.free_default.value == 0:
			cfg.free_default.value = int(getMinFreeKbytes())
			cfg.free_default.save()

	def startCacheFlush(self, session):
		self.dialog = session.instantiateDialog(CacheFlushAutoScreen)
		self.makeShow()

	def makeShow(self):
		if cfg.scrinfo.value:
			self.dialog.show()
		else:
			self.dialog.hide()

CacheFlushAuto = CacheFlushAutoMain()

class CacheFlushAutoScreen(Screen):
	if FHD:
		skin = """<screen name="CacheFlushAutoScreen" position="830,130" zPosition="10" size="250,30" title="CacheFlush Status" backgroundColor="#31000000" >
				<widget name="message_label" font="Regular;24" position="0,0" zPosition="2" valign="center" halign="center" size="250,30" backgroundColor="#31000000" transparent="1" />
			</screen>"""
	else:
		skin = """<screen name="CacheFlushAutoScreen" position="550,50" zPosition="10" size="150,20" title="CacheFlush Status" backgroundColor="#31000000" >
				<widget name="message_label" font="Regular;16" position="0,0" zPosition="2" valign="center" halign="center" size="150,20" backgroundColor="#31000000" transparent="1" />
			</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.skin = CacheFlushAutoScreen.skin
		self['message_label'] = Label(_("Starting"))
		self.CacheFlushTimer = eTimer()
		self.CacheFlushTimer.timeout.get().append(self.__makeWhatYouNeed)
		self.showTimer = eTimer()
		self.showTimer.timeout.get().append(self.__endShow)
		self.state = None
		self.onLayoutFinish.append(self.__chckState)
 		self.onShow.append(self.__startsuspend)
		self.__setUncachedMemory()

	def __startsuspend(self):
		self.setTitle(_("CacheFlush Status"))
		self.showTimer.start(int(cfg.timescrinfo.value) * 1000)

	def __chckState(self):
		if self.instance and self.state is None:
			if cfg.enable.value:
				self['message_label'].setText(_("Started"))
			else:
				self['message_label'].setText(_("Stopped"))
			self.state = cfg.enable.value
			if cfg.scrinfo.value and CacheFlushAuto.dialog is not None:
				CacheFlushAuto.dialog.show()
		self.CacheFlushTimer.start(int(cfg.timeout.value)*60000)

	def __makeWhatYouNeed(self):
		self.__chckState()
		if cfg.enable.value:
			dropCache()
			if self.instance:
				self['message_label'].setText(_("Mem cleared"))
				if cfg.scrinfo.value and CacheFlushAuto.dialog is not None:
					CacheFlushAuto.dialog.show()

	def __endShow(self):
		CacheFlushAuto.dialog.hide()

	def __setUncachedMemory(self):
		if cfg.uncached.value != "0":
			setMinFreeKbytes(int(cfg.uncached.value)*1024)

class CacheFlushInfoScreen(Screen):
	if FHD:
		skin = """<screen name="CacheFlushInfoScreen" position="center,center" zPosition="2" size="1210,800" title="CacheFlush Info" backgroundColor="#31000000" >
				<widget name="lmemtext" itemHeight="25" font="Regular;23" position="10,10" size="320,800" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
				<widget name="lmemvalue" itemHeight="25" font="Regular;23" position="330,10" size="150,800" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
				<widget name="rmemtext" itemHeight="25" font="Regular;23" position="620,10" size="360,800" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
				<widget name="rmemvalue" itemHeight="25" font="Regular;23" position="970,10" size="150,800" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
				<widget name="pfree" position="510,150" size="76,20" font="Regular;20" zPosition="3" halign="right" backgroundColor="#31000000" transparent="1" />
				<widget name="pused" position="510,500" size="76,20" font="Regular;20" zPosition="3" halign="right" backgroundColor="#31000000" transparent="1" />
				<widget name="slide" position="590,10" size="18,730" render="Progress" zPosition="3" borderWidth="1" orientation="orBottomToTop" />
				<ePixmap pixmap="skin_default/div-h.png" position="0,745" zPosition="1" size="1210,2" />
				<widget name="key_red" position="60,760" zPosition="1" size="130,32" valign="center" halign="center" font="Regular;28" transparent="1" foregroundColor="red" />
				<widget name="key_green" position="460,760" zPosition="1" size="130,32" valign="center" halign="center" font="Regular;28" transparent="1" foregroundColor="green" />
				<widget name="key_blue" position="860,760" zPosition="1" size="130,32" valign="center" halign="center" font="Regular;28" transparent="1" foregroundColor="blue" />
			</screen>"""
	else:
		skin = """<screen name="CacheFlushInfoScreen" position="center,50" zPosition="2" size="540,500" title="CacheFlush Info" backgroundColor="#31000000" >
				<widget name="lmemtext" font="Regular;16" position="10,10" size="120,500" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
				<widget name="lmemvalue" font="Regular;16" position="130,10" size="80,500" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
				<widget name="rmemtext" font="Regular;16" position="330,10" size="120,500" zPosition="2" valign="top" halign="left" backgroundColor="#31000000" transparent="1" />
				<widget name="rmemvalue" font="Regular;16" position="450,10" size="80,500" zPosition="2" valign="top" halign="right" backgroundColor="#31000000" transparent="1" />
				<widget name="pfree" position="200,100" size="70,20" font="Regular;14" zPosition="3" halign="right" backgroundColor="#31000000" transparent="1" />
				<widget name="pused" position="200,370" size="70,20" font="Regular;14" zPosition="3" halign="right" backgroundColor="#31000000" transparent="1" />
				<widget name="slide" position="280,10" size="18,445" render="Progress" zPosition="3" borderWidth="1" orientation="orBottomToTop" />
				<ePixmap pixmap="skin_default/div-h.png" position="0,465" zPosition="2" size="540,2" />
				<widget name="key_red" position="10,472" zPosition="2" size="130,28" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="red" />
				<widget name="key_green" position="130,472" zPosition="2" size="130,28" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="green" />
				<widget name="key_blue" position="390,472" zPosition="2" size="130,28" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="blue" />
			</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.setup_title = _("CacheFlush Info")
		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"blue": self.freeMemory,
				"green": self.getMemInfo,
			}, -2)

		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("Refresh"))
		self["key_blue"] = Label(_("Clear Now"))

		self['lmemtext'] = Label()
		self['lmemvalue'] = Label()
		self['rmemtext'] = Label()
		self['rmemvalue'] = Label()
		self['pfree'] = Label()
		self['pused'] = Label()

		self["slide"] = ProgressBar()
		self["slide"].setValue(100)

		self.setTitle(_("CacheFlush Info") + "  " + VERSION)
		self.onLayoutFinish.append(self.getMemInfo)

	def getMemInfo(self):
		try:
			ltext = rtext = ""
			lvalue = rvalue = ""
			mem = 0
			free = 0
			i = 0
			for line in open('/proc/meminfo','r'):
				( name, size, units ) = line.strip().split()
				if name.find("MemTotal") != -1:
					mem = int(size)
				if name.find("MemFree") != -1:
					free = int(size)
				if i < 28:
					ltext += "".join((name,"\n"))
					lvalue += "".join((size," ",units,"\n"))
				else:
					rtext += "".join((name,"\n"))
					rvalue += "".join((size," ",units,"\n"))
				i += 1
			self['lmemtext'].setText(ltext)
			self['lmemvalue'].setText(lvalue)
			self['rmemtext'].setText(rtext)
			self['rmemvalue'].setText(rvalue)

			self["slide"].setValue(int(100.0*(mem-free)/mem+0.25))
			self['pfree'].setText("%.1f %s" % (100.*free/mem,'%'))
			self['pused'].setText("%.1f %s" % (100.*(mem-free)/mem,'%'))

		except Exception, e:
			print "[CacheFlush] getMemory FAIL:", e

	def freeMemory(self):
		dropCache()
		self.getMemInfo()

	def cancel(self):
		self.close()
