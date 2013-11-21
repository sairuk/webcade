#!/usr/bin/env python

import cherrypy
import os
import glob
import re
import subprocess
from subprocess import Popen


USER_DIR = '.wahcade'
IMAGE_FILETYPES= ['jpg', 'jpeg', 'png', 'bmp', 'gif','svg']

class WebCade(object):		
	@cherrypy.expose
	def launch(self, r=None):
		if r:
			self.wc_launch(r)

	@cherrypy.expose
	def index(self):
		self.current_dir = os.path.dirname(os.path.abspath(__file__))
		self.wahcade_ini = self.wc_ini_read('%s/wahcade.ini' % USER_DIR)
		self.emulator_ini = self.wc_ini_read('%s/ini/%s.ini' % (USER_DIR, self.wahcade_ini['current_emulator']))
		self.layouts = glob.glob(os.path.join(USER_DIR,'layouts',self.wahcade_ini['layout'],'*'))
		self.layout_file = self.wc_lay_file('%s/layouts/%s/' % (USER_DIR, self.wahcade_ini['layout']),self.wahcade_ini['current_emulator'])
		self.layout = self.wc_lay2css3(self.layout_file)
		self.template = self.read_file('layout.html')
		self.gamesdetail = self.wc_gl_read('%s/files/%s-0.lst' % (USER_DIR, self.wahcade_ini['current_emulator']))
		self.gameslist = self.wc_gl_options(self.gamesdetail)
		
		# REPLACE TAGS IN TEMPLATE
		replaced = self.replace_template(self.template,"%css3",self.layout)
		replaced = self.replace_template(replaced,"%gameslist",self.gameslist)
			
		return replaced
		
	def wc_ini_read(self, ini_file):
		''' process wahcade_ini format and return dict '''
		d = {}
		f = self.read_file(ini_file)
		for l in f:
				z = l.split()
				if not len(z) < 1 and not '#' in z[0]:
					if len(z) > 1:
						z_val = z[1]
					else:
						z_val = ""
					d[z[0]] = z_val
		return d

	def replace_template(self,template,pattern,replace):
		for idx, i in enumerate(template):
			if pattern in i:
				template[idx] = i.replace(pattern,replace)
		return template
		
	def read_file(self,file):
		''' read file into list '''
		f = open(file)
		return f.readlines()
	
	def wc_lay_file(self,lay_dir,emulator):
		''' process layout file '''
		layout_emu = os.path.join(lay_dir,emulator+'.lay')
		layout = os.path.join(lay_dir,'layout.lay')
		if os.path.exists(layout_emu):
			layout = layout_emu
		else:
			layout = layout
		lay = self.read_file(layout)
		return lay
		
	def wc_col2html(self, wc_colour):
		if len(wc_colour) > 0:
			return hex(int(wc_colour))[2:].zfill(6)
		return 

	def wc_lay_ext(self, lay_arr, item_idx_name):		
		for ext in IMAGE_FILETYPES:
			lay_art_emulator = os.path.join(USER_DIR,'layouts',self.wahcade_ini['layout'],self.wahcade_ini['current_emulator']+'-'+item_idx_name+'.'+ext)
			lay_global = os.path.join(USER_DIR,'layouts',self.wahcade_ini['layout'],item_idx_name+'.'+ext)
			if lay_art_emulator in self.layouts:
				return lay_art_emulator
			elif lay_global in self.layouts:
				return lay_global
			else:
				continue
		return ""
		
	def wc_lay2css3(self,lay_arr):
		lay_item = '%s'*44 % ( self.wc_lay2css3_header(0, 'main', 'games_list_indicator', lay_arr),
		self.wc_lay2css3_item(7, 'main_logo', lay_arr),
		self.wc_lay2css3_item(20, 'game_list_indicator', lay_arr),
		self.wc_lay2css3_item(33, 'emulator_name', lay_arr),
		self.wc_lay2css3_item(46, 'game_list .gl_select', lay_arr),
		self.wc_lay2css3_item(59, 'game_selected', lay_arr),
		self.wc_lay2css3_item(72, 'artwork1', lay_arr),
		self.wc_lay2css3_item(85, 'artwork2', lay_arr),
		self.wc_lay2css3_item(98, 'artwork3', lay_arr),
		self.wc_lay2css3_item(111, 'artwork4', lay_arr),
		self.wc_lay2css3_item(124, 'artwork5', lay_arr),
		self.wc_lay2css3_item(137, 'artwork6', lay_arr),
		self.wc_lay2css3_item(150, 'artwork7', lay_arr),
		self.wc_lay2css3_item(163, 'artwork8', lay_arr),
		self.wc_lay2css3_item(176, 'artwork9', lay_arr),
		self.wc_lay2css3_item(189, 'artwork10', lay_arr),
		self.wc_lay2css3_item(202, 'game_description', lay_arr),
		self.wc_lay2css3_item(215, 'rom_name', lay_arr),
		self.wc_lay2css3_item(228, 'year_manufacturer', lay_arr),
		self.wc_lay2css3_item(241, 'screen_type', lay_arr),
		self.wc_lay2css3_item(254, 'controller_type', lay_arr),
		self.wc_lay2css3_item(267, 'driver_status', lay_arr),
		self.wc_lay2css3_item(280, 'catver', lay_arr),
		self.wc_lay2css3_header(293, 'options', 'options_list_indicator', lay_arr),
		self.wc_lay2css3_item(300, 'options_heading', lay_arr),
		self.wc_lay2css3_item(313, 'options_list', lay_arr),
		self.wc_lay2css3_item(326, 'options_current_setting', lay_arr),
		self.wc_lay2css3_item(339, 'options_current_value', lay_arr),
		self.wc_lay2css3_header(352, 'message', 'options_list_indicator', lay_arr),
		self.wc_lay2css3_item(356, 'message_heading', lay_arr),
		self.wc_lay2css3_item(369, 'message_text', lay_arr),
		self.wc_lay2css3_item(382, 'message_prompt', lay_arr),
		self.wc_lay2css3_item(395, 'ss_artwork1', lay_arr),
		self.wc_lay2css3_item(408, 'ss_artwork2', lay_arr),
		self.wc_lay2css3_item(421, 'ss_artwork3', lay_arr),
		self.wc_lay2css3_item(434, 'ss_artwork4', lay_arr),
		self.wc_lay2css3_item(447, 'ss_artwork5', lay_arr),
		self.wc_lay2css3_item(460, 'ss_artwork6', lay_arr),
		self.wc_lay2css3_item(473, 'ss_artwork7', lay_arr),
		self.wc_lay2css3_item(486, 'ss_artwork8', lay_arr),
		self.wc_lay2css3_item(499, 'ss_artwork9', lay_arr),
		self.wc_lay2css3_item(512, 'ss_artwork10', lay_arr),
		self.wc_lay2css3_item(525, 'ss_game_description', lay_arr),
		self.wc_lay2css3_item(538, 'ss_mp3name', lay_arr))
		return '<style>\n%s\n</style>' % lay_item		
		
	def wc_lay2css3_item(self,item_idx,item_idx_name,lay_arr):
		# Process Image types
		item_idx_short = item_idx_name
		if item_idx_name[:3] == 'art':
			item_idx_short = item_idx_name.replace("work","")
		art_url = self.wc_lay_ext(lay_arr, item_idx_short).replace('\\','/')

		# Convert display property to block/none
		display_block = "none"
		if lay_arr[item_idx+0].strip() == "True":
			display_block = "block";
			
		# Convert Transparency Property
		if lay_arr[item_idx+2] == 0:
			bg_c = '#%s' % self.wc_col2html(lay_arr[item_idx+3])
		else:
			bg_c = "transparent"

		# Convert Font Style
		if lay_arr[item_idx+5] == "True":
			font_style = 'bold'
		elif lay_arr[item_idx+6].strip() == "True":
			font_style = 'italic'
		else:
			font_style = 'none'

		# Convert Text Align
		if lay_arr[item_idx+8].strip() == 2:
			text_align = "center"
		elif lay_arr[item_idx+8].strip() == 1:
			text_align = "right"
		else:
			text_align = "left"

		lay_item = '#%s\n' % item_idx_name
		lay_item = lay_item + '{\n'
		lay_item = lay_item + 'position:absolute;\n'
		lay_item = lay_item + 'display:%s;\n' % display_block
		lay_item = lay_item + 'background:%s url("%s") top left no-repeat;\n' % (bg_c,art_url)
		lay_item = lay_item + 'background-clip:content-box;\n'
		lay_item = lay_item + 'color:#%s;\n' % self.wc_col2html(lay_arr[item_idx+3].strip())
		lay_item = lay_item + 'font-family:%s;\n' % lay_arr[item_idx+4].strip()
		lay_item = lay_item + 'font-style:%s;\n' % font_style
		lay_item = lay_item + 'font-size:%spx;\n' % lay_arr[item_idx+7].strip()
		lay_item = lay_item + 'text-align:%s;\n' % text_align
		lay_item = lay_item + 'left:%spx;\n' % lay_arr[item_idx+9].strip()
		lay_item = lay_item + 'top:%spx;\n' % lay_arr[item_idx+10].strip()
		lay_item = lay_item + 'width:%spx;\n' % lay_arr[item_idx+11].strip()
		lay_item = lay_item + 'height:%spx;\n' % lay_arr[item_idx+12].strip()
		lay_item = lay_item + '}\n'
		return lay_item
		
	def wc_lay2css3_header(self,item_idx,item_idx_name,item_selector_name,lay_arr):
		bg_url = self.wc_lay_ext(lay_arr, item_idx_name).replace('\\','/');
		lay_header = '#%s\n' % item_idx_name
		lay_header = lay_header + '{\n'
		lay_header = lay_header + 'background-color: #%s;\n' % self.wc_col2html(lay_arr[item_idx+2].strip())
		lay_header = lay_header + 'background-image: url("%s");\n' % bg_url
		lay_header = lay_header + 'background-repeat: no-repeat;\n'
		lay_header = lay_header + 'background-position: top left;\n'
		lay_header = lay_header + 'background-clip: content-box;\n'
		lay_header = lay_header + 'width:%spx;\n' % lay_arr[item_idx].strip()
		lay_header = lay_header + 'height:%spx;\n' % lay_arr[item_idx+1].strip()
		lay_header = lay_header + 'overflow: hidden;\n'
		lay_header = lay_header + '}\n'
		lay_header = lay_header + '#%s .h_bar { #%s; }\n' % (item_selector_name, self.wc_col2html(lay_arr[item_idx+5].strip()))
		lay_header = lay_header + '#%s .h_item { #%s; }\n' % (item_selector_name, self.wc_col2html(lay_arr[item_idx+6].strip()))
		return lay_header
		
	def wc_launch(self,item):
		'''Launch item, pass item as sequence ['exec','args']'''
		if os.path.exists(self.emulator_ini['emulator_executable']):
			cmdline = self.emulator_ini['emulator_executable'], item
			p = Popen(cmdline, shell=True, cwd=os.path.dirname(self.emulator_ini['emulator_executable']))
		else:
			print "Could not find %s" % self.emulator_ini['emulator_executable']
		return

	def wc_gl_options(self, dict):
		myopts = ""
		optlist = []
		for key, value in dict.iteritems():
			optlist.append([key,'<option value="%s">%s</option>' % (value[0], key)])
		for g in sorted(optlist, key=lambda optlist: optlist[0]):
			myopts += g[1]
		return myopts
		
	def wc_gl_read(self,glist):
		gl = {}
		with open(glist, 'r') as f:
			for index, value in enumerate(f):
				gldet = []
				gldet.append(value.strip())
				for idx in range(12):
					gldet.append(f.next().strip())
				if len(gldet):
					gl[gldet[1]] = gldet
		return gl
		
if __name__ == "__main__":
	current_dir = os.path.dirname(os.path.abspath(__file__))
	cherrypy.config.update({'server.socket_host': '127.0.0.1',
							'server.socket_port': 8888,
							'cherrypy._cplogging': True,
							'log.access_file': 'access.log',
							'log.error_file': 'error.log',
						})	
						
	config = {
	 '/': {
	   'tools.staticdir.root': current_dir,
	  },
	 '/.wahcade': {
	   'tools.staticdir.on': True,
	   'tools.staticdir.dir': ".wahcade",
	   },
	 '/css': {
	   'tools.staticdir.on': True,
	   'tools.staticdir.dir': "css",
	   },
	 '/js': {
	   'tools.staticdir.on': True,
	   'tools.staticdir.dir': "js",
	   },
	   
	}


	app = cherrypy.tree.mount(WebCade(), "/", config)
	cherrypy.engine.start()
	cherrypy.engine.block()