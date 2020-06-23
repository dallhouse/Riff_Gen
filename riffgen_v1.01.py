#!/usr/bin/env python3

import re
from numpy.random import choice
import random
from AppKit import NSSound
from tkinter import *
import math
from pysine import sine
import time
from tkinter import messagebox
import os
import subprocess
import platform
from itertools import islice
from Cocoa import NSRunningApplication, NSApplicationActivateIgnoringOtherApps
import sys
# import warnings




# with warnings.catch_warnings():
#     warnings.filterwarnings('ignore',category=DeprecationWarning, module="tkinter")
# supposedly filters the tkinter Deprecation warning --NOT WORKING--




# home_path = os.path.expanduser("~")
# os.chdir(os.path.join(home_path, "Desktop/python_scripts/rhythm_generator/riffgen"))
os.chdir(os.path.dirname(sys.argv[0]))



# drawing focus to the tk window
# worked fine until it randomly didn't
# source code: https://stackoverflow.com/questions/1892339/how-to-make-a-tkinter-window-jump-to-the-front
# def raise_app(root: Tk):
#     root.attributes("-topmost", True)
#     if platform.system() == 'Darwin':
#         tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is {} to true'
#         script = tmpl.format(os.getpid())
#         output = subprocess.check_call(['/usr/bin/osascript', '-e', script])
#     root.after(0, lambda: root.attributes("-topmost", False))
def raise_app():
	if platform.system() != 'Darwin':
		root.lift()
		root.call('wm', 'attributes', '.', '-topmost', True)
		root.after_idle(root.call, 'wm', 'attributes', '.', '-topmost', False)
	else:
		app = NSRunningApplication.runningApplicationWithProcessIdentifier_(os.getpid())
		app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)




# for pyinstaller to find the files it packs
# https://www.reddit.com/r/learnpython/comments/4kjie3/how_to_include_gui_images_with_pyinstaller/
# def resource_path(relative_path):
# 	if hasattr(sys, '_MEIPASS'):
# 		return os.path.join(sys._MEIPASS, relative_path)
# 	return os.path.join(os.path.abspath("."), relative_path)

###########################################################################################################################################################

# splash screen
splash = Tk()
splash.overrideredirect(True)
width = 605
height = 361
swidth = splash.winfo_screenwidth()
sheight = splash.winfo_screenheight()
splash.geometry('%dx%d+%d+%d' % (width*.98, height*1.025, \
	(swidth-width)/2, ((sheight-height)/2)*.7))
image_file = "assets/images/splashpage_logo.gif"
image = PhotoImage(file=image_file)
splash_canvas = Canvas(splash, height=height, width=width, bg="white")
splash_canvas.create_image((width/2)*.98, (height/2)*1.025, image=image)
splash_canvas.pack()
splash.after(2400, splash.destroy)
# raise_app(splash)
splash.lift()
splash.attributes('-topmost',True)
splash.after_idle(splash.attributes,'-topmost',False)
splash.mainloop()

###########################################################################################################################################################

# tkinter GUI
root = Tk(className=" Riff Gen")
root.focus_force()

# setting color variables
bg_color = "#262626"
border_color = "#dfdfdf"
labelframe_color = "#292929"
blue_color = "#007aff"
green_color = "#28cd41"
rollover_color = "#d9d9d9"
rollover_color2 = "#5c5c5c"
throughcolor = "#acacac"
tooltip_color = "#ffffe0"
root.configure(bg=border_color)

# configuring root geometry
w = 486
h = 359
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d'%(w,h,x,y*.7)) 
root.resizable(0, 0)

###########################################################################################################################################################

# declaring notes and their corresponding 
note1 = "O" # (input("") or "O")
silence = "-" # (input("") or "-")
sustain = "o" # (input("") or "o")
note2 = "1" # (input("") or "1")
mute = "X" # (input("") or "X")
pmute = "p" 

# declaring all tk variables
# slider variabels
note1_var = IntVar()
silence_var = IntVar()
sustain_var = IntVar()
note2_var = IntVar()
mute_var = IntVar()
pmute_var = IntVar()
flair_var = IntVar()
repeat_var = IntVar()
note1_var.set(50)
silence_var.set(50)
sustain_var.set(50)
note2_var.set(0)
mute_var.set(0)
pmute_var.set(0)
flair_var.set(50)
repeat_var.set(50)
checkbutton2_var = IntVar()
checkbutton2_var.set(0)
checkbutton3_var = IntVar()
checkbutton3_var.set(0)
checkbutton4_var = IntVar()
checkbutton4_var.set(0)
checkbutton5_var = IntVar()
checkbutton5_var.set(0)
checkbutton6_var = IntVar()
checkbutton6_var.set(0)
checkbutton7_var = IntVar()
checkbutton7_var.set(0)
checkbutton8_var = IntVar()
checkbutton8_var.set(0)
# spinbox variables
division_var = IntVar()
measures_var = IntVar()
# result box variables
message_box_var = StringVar()
triplet_box_var = StringVar()
result_box_var = StringVar()
# sound bar variables
play_pause_var = StringVar()
looping_var = StringVar()
play_pause_var.set("Play")
looping_var.set("Loop")
pitch_var = IntVar()
tempo_var = IntVar()
pitch_var.set(50)
tempo_var.set(50)

# declaring note weights
note1_weight = note1_var.get()
silence_weight = silence_var.get()
sustain_weight = sustain_var.get()
note2_weight = note2_var.get()
mute_weight = mute_var.get()
pmute_weight = pmute_var.get()
flair_weight = flair_var.get()
repeat_weight = repeat_var.get()
# dynamic lists
weight_list = [] # converted weights
bar = [] # contains a list of every separate note to be displayed
bars_final = []
# declaring error messages
msg1 = "INVALID NOTE DIVISION"
msg2 = "ENTER A LOWER DIVISION"
msg3 = "LIMIT SET TO 32 NOTES"
msg4 = "ENTER A NUMERIC VALUE"
msg5 = "ENTER A POSTIVE INTEGER"
msg6 = "INCOMPLETE MEASURES PRESENT"
msg7 = "MUST BE MORE THAN 4 NOTES"
msg8 = "UNKNOWN ERROR. TRY AGAIN"
msg9 = "ONE NOTE MUST BE WEIGHTED"
msg10 = "NONDIGIT INPUTS"
# miscellaneous declarations
triplet_nums = (3, 6, 12)
accepted_divs = [1, 2, 3, 4, 6, 8, 12, 16]


# various functions
def invalid_div():
	message_box_var.set("")
	result_box_var.set("")
	triplet_box_var.set("")
	message_box_var.set(msg1)
	root.after(4000, clear_message_box)

def too_fast():
	message_box_var.set("")
	result_box_var.set("")
	triplet_box_var.set("")
	message_box_var.set(msg2)
	root.after(4000, clear_message_box)

def too_long():
	message_box_var.set("")
	result_box_var.set("")
	triplet_box_var.set("")
	message_box_var.set(msg3)
	root.after(4000, clear_message_box)

def non_int():
	message_box_var.set("")
	result_box_var.set("")
	triplet_box_var.set("")
	message_box_var.set(msg4)
	root.after(4000, clear_message_box)

def positive_int():
	message_box_var.set("")
	result_box_var.set("")
	triplet_box_var.set("")
	message_box_var.set(msg5)
	root.after(4000, clear_message_box)

def incomplete_bar():
	message_box_var.set("")
	message_box_var.set(msg6)
	root.after(4000, clear_message_box)

def too_short():
	message_box_var.set("")
	result_box_var.set("")
	triplet_box_var.set("")
	message_box_var.set(msg7)
	root.after(4000, clear_message_box)

def misfire():
	message_box_var.set("")
	result_box_var.set("")
	triplet_box_var.set("")
	message_box_var.set(msg8)
	root.after(4000, clear_message_box)

def all_zeroes():
	message_box_var.set("")
	result_box_var.set("")
	triplet_box_var.set("")
	message_box_var.set(msg9)
	root.after(4000, clear_message_box)

def nondigit():
	message_box_var.set("")
	triplet_box_var.set("")
	message_box_var.set(msg10)
	root.after(4000, clear_message_box)

def add_silence():
	values1.insert(1, silence)
	values2.insert(1, silence)
	weights_to_be_converted1.insert(1, silence_weight)
	weights_to_be_converted2.insert(1, silence_weight)

def add_note2():
	values1.insert(2, note2)
	values2.insert(2, note2)
	weights_to_be_converted1.insert(2, note2_weight)
	weights_to_be_converted2.insert(2, note2_weight)

def add_mutes():
	values1.insert(3, mute)
	values2.insert(3, mute)
	weights_to_be_converted1.insert(3, mute_weight)
	weights_to_be_converted2.insert(3, mute_weight)

def add_sustain():
	values2.insert(4, sustain)
	weights_to_be_converted2.insert(4, sustain_weight)

def clear_result_box():
	result_box_var.set("")

def clear_message_box():
	message_box_var.set("")

def clear_triplet_box():
	triplet_box_var.set("")

def pop():
	pop = NSSound.alloc()
	pop.initWithContentsOfFile_byReference_('assets/audio/Pop.aiff', True)
	pop.play()

def glass():
	glass = NSSound.alloc()
	glass.initWithContentsOfFile_byReference_('assets/audio/Glass.aiff', True)
	glass.play()

def hero():
	hero = NSSound.alloc()
	hero.initWithContentsOfFile_byReference_('assets/audio/Hero.aiff', True)
	hero.play()

###########################################################################################################################################################

# widget functions
def weight_conversion(*args):
	summ = 0
	# global weight_list
	weight_list = []
	# add an input filter here instead of this (bool(re.search(rf'[^0-9]+', str(num))): # catches non-digits and non-periods)
	for num in args:
		if num == note1:
			summ += int(note1_var.get())
		if num == silence:
			summ += int(silence_var.get())
		if num == sustain:
			summ += int(sustain_var.get())
		if num == note2:
			summ += int(note2_var.get())
		if num == mute:
			summ += int(mute_var.get())
	if summ == 0:
		all_zeroes()
	for num in args:
		if num == note1:
			weight_list.insert(0, (int((note1_var.get()))/summ))
		if num == silence:
			weight_list.insert(1, (int((silence_var.get()))/summ))
		if num == note2:
			weight_list.insert(2, (int((note2_var.get()))/summ))
		if num == mute:
			weight_list.insert(3, (int((mute_var.get()))/summ))
		if num == sustain:
			weight_list.insert(4, (int((sustain_var.get()))/summ))
	if sum(weight_list) != 1: # giving note1 the difference in case of rounding errors
		weight_list[0] = weight_list[0] + (1-sum(weight_list))
	return weight_list

def build_riff(var):
	global bars_final
	notes = division_var.get()
	phrase = measures_var.get()
	notes_int = int(notes)
	phrase_int = int(phrase)
	total = notes_int*phrase_int
	sub_notes_list = []
	bars_final = []
	for i in range((len(var))):
		sub_final = var[i * notes_int : (i +1) * notes_int]
		sub_notes_list.append(sub_final)
	n = 0
	for n in range(phrase_int):
		single_bar = sub_notes_list[n]
		single_bar = "".join(single_bar)
		bars_final.append(single_bar + "   ")
		n += 1
	bars_final = "".join(bars_final)
	bars_final = bars_final.replace("][", "")
	return(bars_final)

def build_and_print(var):
	build_riff(var)
	result_box_var.set(bars_final)

def clear_command():
	message_box_var.set("")
	result_box_var.set("")
	triplet_box_var.set("")
	message_box_var.set("RIFF CLEARED")
	root.after(4000, clear_message_box)
	longer_measures.configure(state=DISABLED)
	shorter_measures.configure(state=DISABLED)
	clear_button.configure(state=DISABLED)
	add_gen.configure(state=DISABLED)
	play_button.configure(state=DISABLED)
	loop_button.configure(state=DISABLED)
	save_menu.configure(state=DISABLED)
	hero()

def longer_bars():
	shorter_measures.configure(state=NORMAL)
	clear_triplet_box()
	sub_notes_list = []
	final_riff = []
	notes = division_var.get()
	phrase = measures_var.get()
	notes_int = int(notes)
	phrase_int = int(phrase)
	total = notes_int*phrase_int
	next_div = accepted_divs.index(notes_int)
	notes_int = int(accepted_divs[next_div+1])
	division_var.set(accepted_divs[next_div+1])
	if accepted_divs[next_div+1] in triplet_nums:
		triplet_box_var.set("*triplets*")
		root.after(4000, clear_triplet_box)
	for i in range((total)):
		sub_final = bar[i * notes_int : (i +1 ) * notes_int]
		sub_notes_list.append(sub_final)
	sample_val = 0
	for n in range(phrase_int):
		if sample_val < phrase_int:
			single_bar = sub_notes_list[sample_val]
			single_bar = "".join(single_bar)
			final_riff.append(single_bar + "   ")
			sample_val += 1
		elif sample_val >= phrase_int:
			break
	final_riff = "".join(final_riff)
	final_riff = final_riff.replace("][", "")
	incomplete_bar()
	result_box_var.set(final_riff)
	if notes_int == 16:
		longer_measures.configure(state=DISABLED)
	return bar
	
def shorter_bars(): 
	longer_measures.configure(state=NORMAL)
	clear_triplet_box()
	sub_notes_list = []
	final_riff = []
	notes = division_var.get()
	phrase = measures_var.get()
	notes_int = int(notes)
	phrase_int = int(phrase)
	total = notes_int*phrase_int
	next_div = accepted_divs.index(notes_int)
	notes_int = int(accepted_divs[next_div-1])
	division_var.set(accepted_divs[next_div-1])
	if accepted_divs[next_div-1] in triplet_nums:
		triplet_box_var.set("*triplets*")
		root.after(4000, clear_triplet_box)
	for i in range((total)):
		sub_final = bar[i * notes_int : (i+1) * notes_int]
		sub_notes_list.append(sub_final)
	sample_val = 0
	for n in range(round(phrase_int)): 
		if sample_val < phrase_int*2: 
			single_bar = sub_notes_list[sample_val]
			single_bar = "".join(single_bar)
			final_riff.append(single_bar + "   ")
			sample_val += 1
		elif sample_val >= phrase_int:
			break
	final_riff = "".join(final_riff)
	final_riff = final_riff.replace("][", "")
	incomplete_bar()
	result_box_var.set(final_riff)
	if notes_int == 1:
		shorter_measures.configure(state=DISABLED)
	return bar

def random_rhythm():
	global key_contents
	global key_message
	key_contents = []
	key_contents.append(key_message)
	silence_button.deselect()
	note2_button.deselect()
	mute_button.deselect()
	sustain_button.deselect()
	pmute_button.deselect()
	flair_button.deselect()
	repeat_button.deselect()
	result_box_var.set("")
	message_box_var.set("")
	note1_weight = random.randrange(0,100) 
	note1_var.set(note1_weight)
	silence_weight = random.randrange(1,100)
	sustain_weight = random.randrange(1,100)
	note2_weight = random.randrange(1,100)
	mute_weight = random.randrange(1,100)
	pmute_weight = random.randrange(1,100)
	flair_weight = random.randrange(1,100)
	repeat_weight = random.randrange(1,100)
	notes = random.choice(accepted_divs)
	division_var.set(notes)
	phrase = random.randrange(1,12,2)
	measures_var.set(phrase)
	total = int(notes)*int(phrase)
	values1 = [note1]
	values2 = [note1]
	weights_to_be_converted1 = [note1]
	weights_to_be_converted2 = [note1] 
	global bar
	bar = []
	longer_measures.configure(state=NORMAL)
	shorter_measures.configure(state=NORMAL)
	add_gen.configure(state=NORMAL)
	clear_button.configure(state=NORMAL)
	play_button.configure(state=NORMAL)
	loop_button.configure(state=NORMAL)
	save_menu.configure(state=NORMAL)
	try: 
		notes_int = int(division_var.get())
		phrase_int = int(measures_var.get())
		total = phrase_int * notes_int
	except:
		non_int() 
		random_rhythm()
		return
	if note1_weight+note2_weight+mute_weight+silence_weight+sustain_weight == 0:
		all_zeroes()
		random_rhythm()
		return
	elif notes_int > 16:
		too_fast()
		random_rhythm()
		return
	elif notes_int%2 != 0 and notes_int != 1 and notes_int not in triplet_nums:
		invalid_div()
		random_rhythm()
		return
	elif total > 32:
		too_long()
		random_rhythm()
		return
	elif total < 4:
		too_short()
		random_rhythm()
		return
	elif notes_int in triplet_nums:
		triplet_box_var.set("*triplets*")
	else:
		triplet_box_var.set("")
	# creating button dynamics  
	if total > 22:			
		add_gen.configure(state=DISABLED)
	if phrase_int + total > 32:
		longer_measures.configure(state=DISABLED)
	if notes_int == 1:
		shorter_measures.configure(state=DISABLED)
	try:
		rando1 = random.randint(0,1)
		rando2 = random.randint(0,1)
		rando3 = random.randint(0,1)
		rando4 = random.randint(0,1)
		if rando1 != 0:
			silence_button.invoke()
			silence_var.set(silence_weight)
			weights_to_be_converted1.insert(1, silence)
			weights_to_be_converted2.insert(1, silence)
			values1.insert(1, silence)
			values2.insert(1, silence)
		else:
			silence_var.set(0)
			silence_entry.configure(state=DISABLED)
		if rando2 != 0:
			note2_button.invoke()
			note2_var.set(note2_weight)
			weights_to_be_converted1.insert(2, note2)
			weights_to_be_converted2.insert(2, note2)
			values1.insert(3, note2)
			values2.insert(3, note2)
		else:
			note2_var.set(0)
			note2_entry.configure(state=DISABLED)
		if rando3 != 0:
			mute_button.invoke()
			mute_var.set(mute_weight)
			weights_to_be_converted1.insert(3, mute)
			weights_to_be_converted2.insert(3, mute)
			values1.insert(4, mute)
			values2.insert(4, mute)
		else:
			mute_var.set(0)
			mute_entry.configure(state=DISABLED)
		if rando4 != 0:
			sustain_button.invoke()
			sustain_var.set(sustain_weight)
			weights_to_be_converted2.insert(4, sustain)
			values2.insert(4, sustain)
		else:
			sustain_var.set(0)
			sustain_entry.configure(state=DISABLED)

		# actual generator
		while len(bar) < round(total*1.85): # the multiplier corresponds to buffer length
			new_weights = weight_conversion(*weights_to_be_converted1)
			global weight_list
			x = choice(values1, 1, p=new_weights) 
			bar.append(x[0])
			if x == note1 or x == note2:
				new_weights = weight_conversion(*weights_to_be_converted2)
				x = choice(values2, 1, p=new_weights) 
				bar.append(x[0])
				if x == sustain:
					x = choice(values2, 1, p=new_weights) 
					bar.append(x[0])

		rando5 = random.randint(0,1)
		rando6 = random.randint(0,1)
		rando7 = random.randint(0,1)
		if rando5 != 0:
			pmute_button.invoke()
			pmute_var.set(pmute_weight)
			palm_mute()
			bar = palm_mute()
		else:
			pmute_var.set(0)
			pmute_entry.configure(state=DISABLED)
		if rando6 != 0:
			flair_button.invoke()
			flair_var.set(flair_weight)
			add_flair()
			bar = add_flair()
		else:
			flair_var.set(0)
			flair_entry.configure(state=DISABLED)
		if rando7 != 0:
			repeat_button.invoke()
			repeat_var.set(repeat_weight)
			repeats()
			bar = repeats()
		else:
			repeat_var.set(0)
			repeat_entry.configure(state=DISABLED)
		key_contents_split = '\n'.join(map(str, key_contents))
		key_var.set(key_contents_split)
		build_and_print(bar)
		pop()
		return bar
		return key_contents
	except ValueError:
		misfire()
		random_rhythm()
		return

def add_flair(): 
	notes = division_var.get()
	phrase = measures_var.get()
	notes_int = int(notes)
	phrase_int = int(phrase)
	total = notes_int*phrase_int
	values2 = [note1]
	flair_weight = flair_var.get()
	global bar
	chars_to_flair = [note1, silence, sustain, note2, mute, ("p"+note1), ("p"+note2), ("p"+mute)]
	if flair_weight == 0:
		return bar
	elif flair_weight != 0:
		if flair_weight == 100:
			flair_weight = 99     
		old_range = (1 - 100)
		new_range = (total - 0) # multiply total to increase max flair
		flair_weight = (((flair_weight - 100) * new_range) / old_range) + 0
		# NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
		flair_amount = float(len(bar))/flair_weight

		if checkbutton2_var.get() != 0:
			values2.append(silence)
		if checkbutton4_var.get() != 0:
			values2.append(note2)
		if checkbutton5_var.get() != 0:
			values2.append(mute)

		for i in range(round(flair_amount)): 
			random_index = random.randint(1, int(len(bar))-1)
			index_choice = bar[random_index]
			# make sure it you prevent flairing notes before a sustain
			if index_choice in chars_to_flair:
				try:
					if sustain not in bar[random_index+1]:
						if index_choice == note1 or index_choice == ("p"+note1):
							new_flair = random.choice(values2)
							bar[random_index] = "[" + bar[random_index] + new_flair + "]"
						elif index_choice == silence or index_choice == ("p"+silence):
							values2.remove(silence)
							new_flair = random.choice(values2)
							values2.append(silence)
							bar[random_index] = "[" + bar[random_index] + new_flair + "]"
						elif index_choice == sustain or index_choice == ("p"+sustain):
							new_flair = random.choice(values2)
							bar[random_index] = "[" + bar[random_index] + new_flair + "]"
						elif index_choice == note2 or index_choice == ("p"+note2):
							new_flair = random.choice(values2)
							bar[random_index] = "[" + bar[random_index] + new_flair + "]"
						elif index_choice == mute or index_choice == ("p"+mute):
							new_flair = random.choice(values2)
							bar[random_index] = "[" + bar[random_index] + new_flair + "]"
					else:
						continue
				except IndexError:
					pass
			else:
				continue
	return bar

def palm_mute():
	notes = division_var.get()
	phrase = measures_var.get()
	notes_int = int(notes)
	phrase_int = int(phrase)
	total = notes_int*phrase_int
	pmute_weight = pmute_var.get()
	pmutable_notes = [note1, note2]
	if pmute_weight != 0:
		old_range = (1 - 100)  
		new_range = (1 - total*.7) # decreasing total's multiplier decreases the amount of pmutes 
		new_value = (((pmute_weight - 100) * new_range) / old_range) + total*.7
		# NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
		for i in range(round(new_value)):
			random_index = random.randint(1, int(len(bar))-1)
			index_choice = bar[random_index]
			if index_choice in pmutable_notes:
				bar[random_index] = "p" + bar[random_index]
			else:
				continue
	elif pmute_weight == 0:
		return bar
	return bar

def repeats():
	notes = division_var.get()
	phrase = measures_var.get()
	notes_int = int(notes)
	phrase_int = int(phrase)
	total = notes_int*phrase_int
	global repeat_weight
	global bar
	repeat_chunk = []
	n = 0
	if repeat_weight == 0:
		return bar
	elif repeat_weight != 0:
		rep_length = random.choice([notes_int, notes_int/2]) #choose chunk size: half or whole measure. rounds up.
		if rep_length == notes_int:
			for i in range(rep_length):	
				repeat_chunk.append(bar[n])
				n += 1
		if rep_length == notes_int/2:
			rep_length = math.ceil(rep_length)
			for i in range(rep_length):	
				repeat_chunk.append(bar[n])
				n += 1
	length_range1 = (1 - 100)  
	length_range2 = round(0 - phrase_int/2)
	new_value = (((repeat_weight - 100) * length_range2) / length_range1) + phrase_int/2
	new_value = round(new_value)
	# # NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
	for i in range(new_value): # how many times to paste
		random_index = random.randint(notes_int+1, int(round(total*1.35)-notes_int))
		index_choice = bar[random_index]
		if bar[random_index+len(range(new_value-1))] != sustain:
			bar[random_index:random_index+len(repeat_chunk)] = repeat_chunk
		if bar[random_index+len(range(new_value-1))] == sustain:
			continue
	return(bar)

def sub_gen_for_addition():
	result_box_chars = result_box_var.get()
	result_len = len(result_box_chars)
	message_box_var.set("")
	values1 = [note1]
	values2 = [note1]
	weights_to_be_converted1 = [note1] #feeds the conversion function
	weights_to_be_converted2 = [note1] 
	# filtering the inputs
	global bar
	bar = []
	try:
		notes_int = int(division_var.get())
		phrase_int = int(measures_var.get())
		total = phrase_int * notes_int
	except:
		non_int()
		return
	if note1_weight+note2_weight+mute_weight+silence_weight+sustain_weight == 0:
		all_zeroes()
		return
	elif notes_int > 16:
		too_fast()
		return
	elif notes_int%2 != 0 and notes_int != 1 and notes_int not in triplet_nums:
		invalid_div()
		return
	elif total+result_len> 60:
		too_long()
		return
	elif notes_int in triplet_nums:
		triplet_box_var.set("*triplets*")
	else:
		pass
	# actual generator
	if checkbutton2_var.get() != 0:
		weights_to_be_converted1.insert(1, silence)
		weights_to_be_converted2.insert(1, silence)
		values1.insert(1, silence)
		values2.insert(1, silence)
	if checkbutton4_var.get() != 0:
		weights_to_be_converted1.insert(2, note2)
		weights_to_be_converted2.insert(2, note2)
		values1.insert(2, note2)
		values2.insert(2, note2)
	if checkbutton5_var.get() != 0:
		weights_to_be_converted1.insert(3, mute)
		weights_to_be_converted2.insert(3, mute)
		values1.insert(3, mute)
		values2.insert(3, mute)
	if checkbutton3_var.get() != 0:
		weights_to_be_converted2.insert(4, sustain)
		values2.insert(4, sustain)
	while len(bar) < round(total*1.85): # the multiplier corresponds to buffer length
		new_weights = weight_conversion(*weights_to_be_converted1)
		global weight_list
		x = choice(values1, 1, p=new_weights) 
		bar.append(x[0])
		if x == values1[0]:
			new_weights = weight_conversion(*weights_to_be_converted2)
			x = choice(values2, 1, p=new_weights) 
			bar.append(x[0])
			if x == values2[0] or values2[1]:
				continue
			else:
				continue
	if checkbutton6_var.get() != 0:
		palm_mute()
		bar = palm_mute()
	if checkbutton7_var.get() != 0:
		add_flair()
		bar = add_flair()
	if checkbutton8_var.get() != 0:
		repeats()
		bar = repeats()
	return bar
	return bars_final

def add_rhythm_gen():
	shorter_measures.configure(state=DISABLED)
	longer_measures.configure(state=DISABLED)
	play_button.configure(state=DISABLED)
	loop_button.configure(state=DISABLED)
	global bars_final
	# global bar
	old_bar_list = bar
	old_bar = result_box_var.get()
	mid_bar = sub_gen_for_addition()
	# if any errors were thrown on the addition gen, it will return none above
	if mid_bar != None: 
		mid_bar = build_riff(mid_bar)
	elif mid_bar == None:
		result_box_var.set(old_bar)
		return
	new_bar = old_bar + "   " + mid_bar
	result_box_var.set(new_bar)
	bars_final = new_bar
	# bar = bar + old_bar_list
	# return bar
	return bars_final

# actual generator function
def sub_rhythm_gen():
	result_box_var.set("")
	message_box_var.set("")
	values1 = [note1]
	values2 = [note1]
	weights_to_be_converted1 = [note1] #feeds the conversion function
	weights_to_be_converted2 = [note1] 
	# filtering the inputs
	global bar
	bar = []
	try:
		notes_int = int(division_var.get())
		phrase_int = int(measures_var.get())
		total = phrase_int * notes_int
	except:
		non_int() 
		return
	if note1_weight+note2_weight+mute_weight+silence_weight+sustain_weight == 0:
		all_zeroes()
		return
	elif notes_int > 16:
		too_fast()
		return
	elif notes_int%2 != 0 and notes_int != 1 and notes_int not in triplet_nums:
		invalid_div()
		return
	elif total > 32:
		too_long()
		return
	elif total < 4:
		too_short()
		return
	elif notes_int in triplet_nums:
		triplet_box_var.set("*triplets*")
	else:
		None	
	# actual generator
	if checkbutton2_var.get() != 0:
		weights_to_be_converted1.insert(1, silence)
		weights_to_be_converted2.insert(1, silence)
		values1.insert(1, silence)
		values2.insert(1, silence)
	if checkbutton4_var.get() != 0:
		weights_to_be_converted1.insert(2, note2)
		weights_to_be_converted2.insert(2, note2)
		values1.insert(2, note2)
		values2.insert(2, note2)
	if checkbutton5_var.get() != 0:
		weights_to_be_converted1.insert(3, mute)
		weights_to_be_converted2.insert(3, mute)
		values1.insert(3, mute)
		values2.insert(3, mute)
	if checkbutton3_var.get() != 0:
		weights_to_be_converted2.insert(4, sustain)
		values2.insert(4, sustain)
	while len(bar) < round(total*1.85): # the multiplier corresponds to buffer length
		new_weights = weight_conversion(*weights_to_be_converted1)
		global weight_list
		x = choice(values1, 1, p=new_weights) 
		bar.append(x[0])
		if x == note1 or x == note2:
			new_weights = weight_conversion(*weights_to_be_converted2)
			x = choice(values2, 1, p=new_weights) 
			bar.append(x[0])
			if x == sustain:
				x = choice(values2, 1, p=new_weights) 
				bar.append(x[0])
	if checkbutton6_var.get() != 0:
		palm_mute()
		bar = palm_mute()
	if checkbutton7_var.get() != 0:
		add_flair()
		bar = add_flair()
	if checkbutton8_var.get() != 0:
		repeats()
		bar = repeats()
	# creating note dynamics
	longer_measures.configure(state=NORMAL)
	shorter_measures.configure(state=NORMAL)
	clear_button.configure(state=NORMAL)
	add_gen.configure(state=NORMAL)
	play_button.configure(state=NORMAL)
	loop_button.configure(state=NORMAL)
	save_menu.configure(state=NORMAL)
	if total > 22:			
		add_gen.configure(state=DISABLED)
	if phrase_int + total > 32:
		longer_measures.configure(state=DISABLED)
	if notes_int == 1:
		shorter_measures.configure(state=DISABLED)
	return bar
	return bars_final

def rhythm_gen():
	sub_rhythm_gen()
	build_and_print(bar)
	pop()
	return bar
	return bars_final

###########################################################################################################################################################

# music player
def build_and_play():
	notes = division_var.get()
	phrase = measures_var.get()
	notes_int = int(notes)
	phrase_int = int(phrase)
	total = notes_int*phrase_int
	sub_notes_list = []
	bars_final = []
	global bar

	master_tuning = pitch_var.get()
	old_pitch_range = (100 - 1)  
	new_pitch_range = (810- 280)
	master_tuning = (((master_tuning - 1) * new_pitch_range) / old_pitch_range) + 280
	# NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
	n1f = master_tuning
	n2f = master_tuning-40
	mutef = master_tuning-136

	speed_val = tempo_var.get()
	old_speed_range = (100 - 1)  
	new_speed_range = (.18 - .55)
	# ending multiplier (below) corresponds to overall effect of divisons on speed
	speed_val = ((((speed_val - 1) * new_speed_range) / old_speed_range) + .55)/(notes_int*.20)
	# # NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
	sleep_time = (speed_val*.2)

	for i in range((len(bar))):
		sub_final = bar[i * notes_int : (i +1) * notes_int]
		sub_notes_list.append(sub_final)
	n = 0
	for n in range(phrase_int):
		single_bar = sub_notes_list[n]
		single_bar = "".join(single_bar)
		bars_final.append(single_bar)
		n += 1
	riff_final = "".join(bars_final)
	riff_final = riff_final.replace("][", "")
	n = 0
	for i in bar[:division_var.get()*measures_var.get()]:
		# print("Sound " + str((n+1)) + ": " + i) # troubleshooting tool
		i = (list(i))
		for numb in i:
			if numb == "[":
				speed_val = speed_val/2
			elif numb == "]":
				speed_val = speed_val*2
			elif numb == sustain or numb == "p":
				pass
			elif numb == note2: 
				mult_val = 1
				if len(bar[n]) >= 3: # current note is from a flaired note
					inner_notes = re.findall(r'[^\[\]\'\, p]', str(i))
					if inner_notes[0] == note2: # if last in list
						sine(frequency=n1f, duration=speed_val)
						time.sleep(sleep_time)
					elif inner_notes[1] == note2: # if second flair is n2
						next_inotes = re.findall(r'[^\[\]\'\, p]', str(bar[n+mult_val]))
						if len(next_inotes) >= 2: # if next note has flair 
							if next_inotes[0] == sustain: # with first note sustain
								mult_val += 1.5
								sine(frequency=n1f, duration=((speed_val*mult_val)+((sleep_time*mult_val)-sleep_time)))
								time.sleep(sleep_time)
							else:
								sine(frequency=n1f, duration=speed_val)
								time.sleep(sleep_time)					
							continue
						elif len(next_inotes) == 1 and next_inotes[0] == sustain: # if next note is straight sustain
							mult_val += 1.5
							sine(frequency=n1f, duration=((speed_val*mult_val)+((sleep_time*mult_val)-sleep_time)))
							time.sleep(sleep_time)
						elif len(next_inotes) == 1 and next_inotes[0] != sustain: # if next note is solid note but sustain
							sine(frequency=n1f, duration=speed_val)
							time.sleep(sleep_time)
				elif len(bar[n]) < 3:
					if n+1 == len(bar):
						sine(frequency=n1f, duration=speed_val)
						time.sleep(sleep_time)
					else:
						try:
							while sustain in bar[n+mult_val]: # while theres a sustain in the next note
								if len(bar[n+mult_val]) == 1: # if its a single sustain
									mult_val += 1
								next_inotes = re.findall(r'[^\[\]\'\, p]', str(bar[n+mult_val]))
								if "[" in bar[n+mult_val] and next_inotes[0] == sustain: # looks for flair with sustain at beginning
									mult_val += .5
									sine(frequency=n1f, duration=((speed_val*mult_val)+((sleep_time*mult_val)-sleep_time)))
									time.sleep(sleep_time)	
									break
						except IndexError:
							pass
						finally:
							if sustain not in bar[int(n+mult_val)]:
								sine(frequency=n1f, duration=((speed_val*mult_val)+((sleep_time*mult_val)-sleep_time)))
								time.sleep(sleep_time)						
						continue
			elif numb == note1: 
				mult_val = 1
				if len(bar[n]) >= 3: # current note is from a flaired note
					inner_notes = re.findall(r'[^\[\]\'\, p]', str(i))
					if inner_notes[0] == note1: # if last in list
						sine(frequency=n2f, duration=speed_val)
						time.sleep(sleep_time)
					elif inner_notes[1] == note1: # if second flair is n2
						next_inotes = re.findall(r'[^\[\]\'\, p]', str(bar[n+mult_val]))
						if len(next_inotes) >= 2: # if next note has flair 
							if next_inotes[0] == sustain: # with first note sustain
								mult_val += 1.5
								sine(frequency=n2f, duration=((speed_val*mult_val)+((sleep_time*mult_val)-sleep_time)))
								time.sleep(sleep_time)
							else:
								sine(frequency=n2f, duration=speed_val)
								time.sleep(sleep_time)					
							continue
						elif len(next_inotes) == 1 and next_inotes[0] == sustain: # if next note is straight sustain
							mult_val += 1.5
							sine(frequency=n2f, duration=((speed_val*mult_val)+((sleep_time*mult_val)-sleep_time)))
							time.sleep(sleep_time)
						elif len(next_inotes) == 1 and next_inotes[0] != sustain: # if next note is solid note but sustain
							sine(frequency=n2f, duration=speed_val)
							time.sleep(sleep_time)
				elif len(bar[n]) < 3:
					if n+1 == len(bar):
						sine(frequency=n2f, duration=speed_val)
						time.sleep(sleep_time)
					else:
						try:
							while sustain in bar[n+mult_val]: # while theres a sustain in the next note
								if len(bar[n+mult_val]) == 1: # if its a single sustain
									mult_val += 1
								next_inotes = re.findall(r'[^\[\]\'\, p]', str(bar[n+mult_val]))
								if "[" in bar[n+mult_val] and next_inotes[0] == sustain: # looks for flair with sustain at beginning
									mult_val += .5
									sine(frequency=n2f, duration=((speed_val*mult_val)+((sleep_time*mult_val)-sleep_time)))
									time.sleep(sleep_time)	
									break
						except IndexError:
							pass
						finally:
							if sustain not in bar[int(n+mult_val)]:
								sine(frequency=n2f, duration=((speed_val*mult_val)+((sleep_time*mult_val)-sleep_time)))
								time.sleep(sleep_time)						
						continue
			elif numb == mute:
				sine(frequency=mutef, duration=speed_val-(speed_val*.2))
				time.sleep(sleep_time + speed_val*.2)
			elif numb == silence:
				time.sleep(speed_val)
				time.sleep(sleep_time)
		n += 1

###########################################################################################################################################################

# values that will be added to the dynamic on-screen key
key_note1 = note1 + " = Note 1"
key_silence = silence + " = Silence"
key_sustain = sustain + " = Sustain"
key_note2 = note2 + " = Note 2"
key_mute = mute + " = Mute"
key_pmute = "p = Palm Mute"
key_flair = "[] = Flair"
key_repeat = "R = Repetition"
key_contents = []
key_contents_split = '\n'.join(map(str, key_contents))

# top-level frame
master_frame = Frame(root, bg=bg_color)
master_frame.grid(padx=(2,0), pady=(0,0))
# creating master frames
top_frame = Frame(master_frame, bg=bg_color)
top_frame.grid(row="0", ipady=5)
bottom_frame = Frame(master_frame, bg=bg_color)
bottom_frame.grid(row="1")
# creating sub-frames
slider_frame = LabelFrame(top_frame, bg=bg_color, text="Note Weights", fg="white", labelanchor="ne", bd="2", font=(None, 12))
slider_frame.grid(row="0", column="1", rowspan="2", padx=(5,7), pady=(12,0), ipady=5)
left_side = Frame(top_frame, bg=bg_color)
left_side.grid(row="0", column="0", rowspan="2", padx=(0,5), pady=(12,0))
message_frame = Frame(bottom_frame, bg=bg_color)
message_frame.grid(row="0", columnspan="2", padx=(10,10))
results_frame = Frame(bottom_frame, bg=bg_color)
results_frame.grid(row="1", columnspan="2", padx=(10,10))
sound_frame = Frame(bottom_frame, bg=bg_color)
sound_frame.grid(row="2", columnspan="2", padx=(11,12), pady=(6,8))
# creating sub sub frames
form_frame = Frame(left_side, bg=bg_color)
form_frame.grid(row="0", column="0", columnspan="2")
extra_frame = Frame(left_side, bg=bg_color)
extra_frame.grid(row="1", column="0", sticky="s")
button_frame = Frame(left_side, bg=bg_color)
button_frame.grid(row="1", column="1", sticky="s")




# logic for the checkboxes
def slider2_state():
	global key_contents
	if checkbutton2_var.get() == 0:
		silence_scale.configure(state = DISABLED)
		silence_entry.configure(state = DISABLED)
		silence_var.set(0)
		key_contents.remove(key_silence)
		key_contents_split = '\n'.join(map(str, key_contents))
		key_var.set(key_contents_split)
		return key_contents 

	if checkbutton2_var.get() == 1:
		silence_scale.configure(state = NORMAL)
		silence_entry.configure(state = NORMAL)
		silence_var.set(50)
		key_contents.append(key_silence)
		key_contents_split = '\n'.join(map(str, key_contents))
		key_var.set(key_contents_split)
		return key_contents

def slider3_state():
	global key_contents
	if checkbutton3_var.get() == 0:
		sustain_scale.configure(state = DISABLED)
		sustain_entry.configure(state = DISABLED)
		sustain_var.set(0)
		key_contents.remove(key_sustain)
		key_contents_split = '\n'.join(map(str, key_contents))
		key_var.set(key_contents_split)
		return key_contents 

	if checkbutton3_var.get() == 1:
		sustain_scale.configure(state = NORMAL)
		sustain_entry.configure(state = NORMAL)
		sustain_var.set(50)
		key_contents.append(key_sustain)
		key_contents_split = '\n'.join(map(str, key_contents))
		key_var.set(key_contents_split)
		return key_contents

def slider4_state():
	global key_contents
	if checkbutton4_var.get() == 0:
		note2_scale.configure(state = DISABLED)
		note2_entry.configure(state = DISABLED)
		note2_var.set(0)
		key_contents.remove(key_note2)
		key_contents_split = '\n'.join(map(str, key_contents))
		key_var.set(key_contents_split)
		return key_contents 

	if checkbutton4_var.get() == 1:
		note2_scale.configure(state = NORMAL)
		note2_entry.configure(state = NORMAL)
		note2_var.set(50)
		key_contents.append(key_note2)
		key_contents_split = '\n'.join(map(str, key_contents))
		key_var.set(key_contents_split)
		return key_contents

def slider5_state():
	global key_contents
	if checkbutton5_var.get() == 0:
		mute_scale.configure(state = DISABLED)
		mute_entry.configure(state = DISABLED)
		mute_var.set(0)
		key_contents.remove(key_mute)
		key_contents_split = '\n'.join(map(str, key_contents))
		key_var.set(key_contents_split)
		return key_contents 

	if checkbutton5_var.get() == 1:
		mute_scale.configure(state = NORMAL)
		mute_entry.configure(state = NORMAL)
		mute_var.set(50)
		key_contents.append(key_mute)
		key_contents_split = '\n'.join(map(str, key_contents))
		key_var.set(key_contents_split)
		return key_contents

def slider6_state():
	global key_contents
	if checkbutton6_var.get() == 0:
		pmute_scale.configure(state = DISABLED)
		pmute_entry.configure(state = DISABLED)
		pmute_var.set(0)
		key_contents.remove(key_pmute)
		key_contents_split = '\n'.join(map(str, key_contents))
		key_var.set(key_contents_split)
		return key_contents 

	if checkbutton6_var.get() == 1:
		pmute_scale.configure(state = NORMAL)
		pmute_entry.configure(state = NORMAL)
		pmute_var.set(50)
		key_contents.append(key_pmute)
		key_contents_split = '\n'.join(map(str, key_contents))
		key_var.set(key_contents_split)
		return key_contents

def slider7_state():
	global key_contents
	if checkbutton7_var.get() == 0:
		flair_scale.configure(state = DISABLED)
		flair_entry.configure(state = DISABLED)
		flair_var.set(0)
		key_contents.remove(key_flair)
		key_contents_split = '\n'.join(map(str, key_contents))
		key_var.set(key_contents_split)
		return key_contents 

	if checkbutton7_var.get() == 1:
		flair_scale.configure(state = NORMAL)
		flair_entry.configure(state = NORMAL)
		flair_var.set(50)
		key_contents.append(key_flair)
		key_contents_split = '\n'.join(map(str, key_contents))
		key_var.set(key_contents_split)
		return key_contents

def slider8_state():
	global key_contents
	if checkbutton8_var.get() == 0:
		repeat_scale.configure(state = DISABLED)
		repeat_entry.configure(state = DISABLED)
		repeat_var.set(0)
		key_contents.remove(key_repeat)
		key_contents_split = '\n'.join(map(str, key_contents))
		key_var.set(key_contents_split)
		return key_contents 

	if checkbutton8_var.get() == 1:
		repeat_scale.configure(state = NORMAL)
		repeat_entry.configure(state = NORMAL)
		repeat_var.set(50)
		key_contents.append(key_repeat)
		key_contents_split = '\n'.join(map(str, key_contents))
		key_var.set(key_contents_split)
		return key_contents




# misc tkinter button functions
def play_to_pause():
	loop_num = 4
	if play_pause_var.get() == "Pause":
		play_pause_var.set("Play")
	if play_pause_var.get() == "Play":
		play_pause_var.set("Pause")
		root.update()
		if looping_var.get() == "Loop":
			build_and_play()
		elif looping_var.get() == "Loop ":
			for i in range(loop_num):
				build_and_play()
		play_pause_var.set("Play")

def loop_to_looping():
	if looping_var.get() == "Loop":
		looping_var.set("Loop ")
		loop_button.config(highlightbackground=green_color)
	elif looping_var.get() == "Loop ":
		looping_var.set("Loop")
		loop_button.config(highlightbackground=bg_color)

def info_window():
	info_width = 446
	info_height = 680
	ws = root.winfo_screenwidth()
	hs = root.winfo_screenheight()
	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)
	iwindow = Toplevel(bg=border_color)
	iwindow.geometry('%dx%d+%d+%d'%(info_width+24,info_height-41,x+7,(y*.2)))
	iwindow.resizable(0, 0) # prevent any resizing
	iwindow.lift()
	iwindow.focus_force()
	iwindow.grab_set()
	iwindow.grab_release()
	logo_path = "assets/images/infopage_logo.gif"
	rg_logo = PhotoImage(file=logo_path)
	# doc_path = "riffgen_docs.txt"
	# info_text = open(doc_path)
	# info_contents = info_text.readlines()[5:]
	# info_final = "".join(info_contents)
	# info_text.close()
	info_contents = \
	"Riff Gen is a random guitar riff generator different from any others that\
	 may exist. This is due to the program's flexibility and simplistic feature-set.\
	 Not only this, but Riff Gen was built with guitarists in mind, so the\n\
generation process, while still truly 'random,' restricts patterns that are\
	 clunky or non-musical, while allowing room for the spacey, non-repetitive\
	 goodness. Simply determine the base note division for each measure, the\
	 number of measures you want, configure your desired note weights and\
	 generate a new riff!\
\n\
\n\
Keep in mind that Riff Gen limits riff generation length to a minimum of 4\
	 and a maximum of 32. You can use whole notes or triplets for your base,\
	 however, the longest acceptable note division are 16th notes. In addition,\
	 a division base of '4' would refer to quarter-notes, '8' to eighth-notes,\
	 and so on. Unless another input is provided, Riff Gen will use a default\
	 value of '4' when calculating its next riff. Note 1, sustain, silence, repetition,\
	 and flair sliders are set to a value of 50, while the rest of the weights are\
	 disabled.\
\n\
\n\
\n\
_________________________________WEIGHTS______________________________________\
	 Each note weight is represented by a slider. A checkbox is used to set its\
	 respective slider value to zero and disable the slider. Note 1 is the only\
	 “note” that must always be present. The entry field below the slider reads\
	 and writes to/from the slider value. In other words, these two are\n\
bi-directional and one will dynamically update if the other is changed. Each\
	 slider starts at 0 and ends at a 100, however, this is an arbitrary range and\
	 these weight values are being used in different ways (read below.) Note\
	 abbreviations are displayed above each slider. See the on-screen key for\
	 meanings of these abbreviations as any notes with a non-zero weight will\
	 be automatically loaded into it.\
\n\
\n\
Among the notes represented by the weight sliders, there are five note\
	 types: note 1 (N1), note 2 (N2), sustain (o)(must come after Note 1 or\
	 Note 2), silence (-), and mute (X). Remember that Note 2 is not meant to\
	 represent any single note, but rather any note other than the base Note 1,\
	 which is generally thought of as an open-fret strum. There are three\n\
additional modifiers: palm mute (p), 'flair' ([]), and repetition (R). Riff\
	 Gen uses these note types when randomly generating the base riff. Each\
	 fundamental note weight is compared to the sum of the weights in order to\
	 calculate what percentage of the riff should contain the note in question.\
	 In this case, note weights directly correspond to the likelihood of that\
	 note being selected.\
\n\
\n\
Once generated, the notes are modified, first by adding palm mutes\n\
(displayed right before either N1 or N2), followed by ‘flair’ and then\n\
repetition. ‘Flair’ represents notes played twice as fast as the base riff\
	 (i.e. eighth notes played during a quarter-note base riff). A maximum flair\
	 weight will flair up to about 75% of the riff. Repetition simply uses its\
	 respective weight to determine the size of the chunk to repeat (between\
	 half the current measure length and a full measure) and how many times\
	 to repeat it (this depends on the overall length of the riff.) This function\
	 may often seem unnoticeable, but is there to provide an element thats less\
	 random, and more human.\
\n\
\n\
\n\
__________________________________BUTTONS______________________________________\
	 The arrow buttons refer to size changes to the note division of the current\
	 riff. The ‘Decrease Division’ button (left) will redistribute the notes in\
	 your riff so that its note division is one value less than its original\
	 designation, while still maintaining the original number of measures thanks\
	 to the hidden riff cache. This means that you cannot generate a measure\
	 with six notes and decrease to a five-note measure.\
\n\
\n\
The ‘Increase Division’ button works the exact same, but increases the\
	 notes per measure rather than decreases.\
\n\
\n\
'Random' generates random values for every possible variable and\n\
generates a new riff, while 'Add' simply appends a new riff to the end of\
	 the current one - while both maintaining Riff Gen's note limits. That being\
	 said, v1.01.01 does not support the playback or division alteration of riffs\
	 once the add function has been performed.\
\n\
\n\
\n\
__________________________________RESULTS___________________________________\
	 The black message bar above the result box will display any messages or\
	 errors on the left. If the current riff has any measure with a triplet note\
	 division, the word 'triplets' will appear on the right side of the message\
	 box until the riff is changed to an even base.\
\n\
\n\
\n\
_________________________________PLAYBACK____________________________________\
	 The playback menu beneath the result box is for both the audio and the\
	 save functions. The play function will generate sine waves to represent\
	 each note in the riff. Keep in mind that the play function will stall all\n\
pending processes! This is Riff Gen's greatest weakness, so use with\
	 precaution, because once it's playing, you can only mute your computer.\
	 It is because of this that the loop function will loop the current riff only\
	 four times. Eventually, you will be able to save this sine wave riff as a\
	 WAV file, but for now the only option is to save as a .TXT to your\n\
downloads folder with the name 'my_riff_' followed by an incremental save\
	 identifier. The black message bar will the live-update with the exact file\
	 path.\
\n\
\n\
The two sliders in the playback menu correspond to 'Speed,' and 'Pitch'.\
	 As of now, 'Speed' does not quite equate to tempo, however, the tempo\
	 does change slightly depending on the current note division. The pitch\
	 of each of the three different note frequencies (note1, note2, and mute)\
	 are all fixed to one another - so changing the 'Pitch' slider adjusts all\
	 values at once.\
\n\
\n\
\n\
________________________________SHORTCUTS___________________________________\
	 Return.......................New Riff\n\
Shift-Return..............Random Riff\n\
Option-Left...............Decrease Division\n\
Option-Right.............Increase Division\n\
Control-I....................Open/Close Info\n\
Command-P..............Play\n\
Command-Shift-P.....Loop and Play\n\
Command-S..............Save to .TXT\n\
Escape.......................Clear Riff and Notifications\n\
Shift-Escape..............Quit\n\
\n\
\n\
\n\
If at any time you feel confused, remember that most widgets will reveal\
	 a brief tooltip descriptor when the cursor is above it. For more information,\
	 check back here. Please enjoy Riff Gen and feel free to contact me\n\
with suggestions and improvements!"
	# sub-frame allowing for defining border
	info_frame = Frame(iwindow, bg=bg_color)
	info_frame.grid(padx=(3,0), pady=(0,3))
	# top bar
	info_title_var = StringVar()
	info_title_var.set("RIFF GEN")
	info_version_var = StringVar()
	info_version_var.set("v1.01.01")
	info_creator_var = StringVar()
	info_creator_var.set("Developed by Alex Bredall")
	header_frame = Frame(info_frame, bg=bg_color)
	header_frame.grid()
	header_image = Label(header_frame, bg=bg_color, width="82", height="52", image=rg_logo, \
		justify=LEFT)
	header_image.image = rg_logo # required or else the image is garbage collected!
	header_image.grid(row="0", column="0", rowspan="3", pady=(0,0), padx=(0,0), sticky="w")
	info_title = Label(header_frame, fg="white", bg=bg_color, textvariable=info_title_var, justify=CENTER, \
		font=("Friz Quadrata", 20, "bold"), width="19")
	info_version = Label(header_frame, fg="white", bg=bg_color, textvariable=info_version_var, justify=CENTER, \
		font=(None, 8), width="19")
	info_creator = Label(header_frame, fg="white", bg=bg_color, textvariable=info_creator_var, justify=CENTER, \
		font=(None, 9), width="19")
	info_title.grid(row="0", column="1", pady=(1,0), padx=(0,18))
	info_version.grid(row="1", column="1", pady=(0,0), padx=(0,18))	
	info_creator.grid(row="2", column="1", pady=(0,4), padx=(0,18))
	blank_frame = Frame(header_frame, bg=bg_color, width="72")
	blank_frame.grid(row="0", column="2")
	# # canvas info and close button
	canvas_frame = Frame(info_frame, bd="0")
	canvas_frame.grid(sticky="ns", row="1", padx=(14,14))
	canvas = Canvas(canvas_frame, width=info_width-16, height=info_height-175, bd="0")
	canvas.grid(padx=(0,0), pady=8, row="0", column="0", sticky="nes")
	canvas.create_text(350, 0 ,fill="black", text=info_contents, font=(None, 12), anchor="n", justify="left", 
		width=info_width)
	scroll_bar = Scrollbar(canvas_frame, orient="vertical", background=bg_color, command=canvas.yview, width="13")
	scroll_bar.grid(row="0", column="0", sticky="nes")
	canvas.configure(yscrollcommand=scroll_bar.set, scrollregion=canvas.bbox("all"))
	button_close = Button(info_frame, text="Close", command=iwindow.destroy, takefocus=True, \
		highlightbackground=bg_color, width="7", height="1")
	button_close.focus_set()
	button_close.grid(sticky="s", row="2", pady=(5,6))
	def mouse_wheel(event):
	# translating scrollpad
		canvas.yview_scroll(-1*(event.delta), "units")
	canvas.bind("<MouseWheel>", mouse_wheel)
	# command-i to open info
	def commandi_callback(event=None):
		button_close.configure(highlightbackground=blue_color)
		iwindow.destroy()
	iwindow.bind('<Command-i>', commandi_callback)
	# shift-escape to quit
	def shiftescape_callback(event=None):
		root.destroy()
	iwindow.bind('<Shift-Escape>', shiftescape_callback)
	def bgcolor_button_enter():
		button_close.configure(highlightbackground=bg_color)
	def enter_callback(event=None):
		button_close.configure(highlightbackground=blue_color)
		iwindow.after(250, bgcolor_button_enter)
		button_close.invoke()
	iwindow.bind('<Return>', enter_callback)




start_save_val = 0
start_folder_val = 0
def save_text():
	global start_folder_val
	global start_save_val
	home_path = os.path.expanduser("~")
	os.chdir(os.path.join(home_path, "Downloads"))
	starting_save = "{}_{}{}".format("my_riff", start_save_val, ".txt")
	# new_folder = "{}_{}".format("Riff_sesh_", start_folder_val)
	# full_folder = os.path.join(home_path, "Downloads", new_folder)
	# if os.path.isdir(full_folder):
	# 	start_folder_val += 1
	# 	new_folder = "{}_{}".format("Riff_sesh", start_folder_val)
	# 	os.mkdir(os.path.join(home_path, "Downloads", new_folder))
	# 	os.chdir(os.path.join(home_path, "Downloads", new_folder))
	# else:
	# 	os.mkdir(os.path.join(home_path, "Downloads", new_folder))
	# 	os.chdir(os.path.join(home_path, "Downloads", new_folder))
	if os.path.exists(starting_save):
		start_save_val = start_save_val + 1
		save_text()
	else:
		f = open(starting_save, "w+")
		f.write(result_box_var.get())
		f.close()
		save_message = home_path + "/Downloads/my_riff_" + str(start_save_val)
		message_box_var.set("SAVED: " + save_message.lower())
		root.after(3200, clear_message_box)
		os.chdir(os.path.dirname(sys.argv[0]))
		glass()
		return start_save_val




# spinboxes
# validating user inputs
def validate_entry(entry_input):
	if entry_input.isdigit() or entry_input == "":
		return True
	else:
		return False
def invalid_entry():
	nondigit()
reg = root.register(validate_entry)
notes_label = Label(form_frame, text="Notes per measure:", bg=bg_color, fg="white", font=(None, 12, "bold"))
notes_label.grid(row="0", sticky="se")
measure_label = Label(form_frame, text="Number of measures:", bg=bg_color, fg="white", font=(None, 12, "bold"))
measure_label.grid(row="1", sticky="se")
# spinboxes
notes_input = Spinbox(form_frame, bd="0", width="2", values=(1,2,3,4,6,8,12,16), takefocus=True, \
	bg="white", textvariable=division_var)
measure_input = Spinbox(form_frame, bd="0", from_="1", to="32", width="2", takefocus=True, textvariable=measures_var\
	, values=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32))
division_var.set(4)
measures_var.set(4)
notes_input.grid(row="0", column="1", padx=(6,0), pady=(8,3), sticky="e")
notes_input.focus_set()
notes_input.icursor(1)
measure_input.grid(row="1", column="1", padx=(6,0), pady=(0,0), sticky="e")
notes_input.configure(validate="all", vcmd=(reg, '%P'), invcmd=invalid_entry)
measure_input.configure(validate="all", vcmd=(reg, '%P'), invcmd=invalid_entry)




# buttons
shorter_measures = Button(button_frame, text="<", justify="center", fg="black", activebackground="white", \
	width="1", highlightbackground=bg_color, pady="0", takefocus=False, command=shorter_bars, \
	font=(None, 20))
longer_measures = Button(button_frame, text=">", justify="center", fg="black", activebackground="white", \
	width="1", highlightbackground=bg_color, pady="0", takefocus=False, command=longer_bars, \
	font=(None, 20))
clear_button = Button(button_frame, text="Clear", fg="black", anchor="e", activebackground=rollover_color, \
	width="7", height="1", bd="0", highlightbackground=bg_color, takefocus=False, command=clear_command)
add_gen = Button(button_frame, text="Add", fg="black", anchor="e", activebackground=rollover_color, \
	width="7", height="1", highlightbackground=bg_color, takefocus=False, command=add_rhythm_gen)
random_button = Button(button_frame, text="Random", fg="black", anchor="e", activebackground=rollover_color, \
	width="7", height="1", bd="0", highlightbackground=bg_color, takefocus=False, command=random_rhythm)
new_gen = Button(button_frame, text="New", fg="black", anchor="e", activebackground=rollover_color, \
	width="7", height="1", highlightbackground=bg_color, takefocus=False, command=rhythm_gen)
info_button = Button(extra_frame, text="Info", fg="black", anchor="e", activebackground=rollover_color, \
	justify=CENTER, width="7", height="1", highlightbackground=bg_color, takefocus=False, command=info_window)
shorter_measures.grid(row="1", column="4", pady=(3,2))
longer_measures.grid(row="1", column="5", pady=(3,2))
clear_button.grid(row="2", column="4", columnspan="2", pady=(3,0))
add_gen.grid(row="3", column="4", columnspan="2", pady=(3,0))
random_button.grid(row="4", column="4", columnspan="2", pady=(3,0))
new_gen.grid(row="5", column="4", columnspan="2", pady=(3,0))
info_button.grid(row="1", column="0", pady=(3,0))
longer_measures.configure(state=DISABLED)
shorter_measures.configure(state=DISABLED)
clear_button.configure(state=DISABLED)
add_gen.configure(state=DISABLED)




# checkboxes
silence_button = Checkbutton(slider_frame, bg=bg_color, \
	justify=CENTER, variable=checkbutton2_var, command=slider2_state, takefocus=False)
sustain_button = Checkbutton(slider_frame, bg=bg_color, \
	justify=CENTER, variable=checkbutton3_var, command=slider3_state, takefocus=False)
note2_button = Checkbutton(slider_frame, bg=bg_color, \
	justify=CENTER, variable=checkbutton4_var, command=slider4_state, takefocus=False)
mute_button = Checkbutton(slider_frame, bg=bg_color, \
	justify=CENTER, variable=checkbutton5_var, command=slider5_state, takefocus=False)
pmute_button = Checkbutton(slider_frame, bg=bg_color, \
	justify=CENTER, variable=checkbutton6_var, command=slider6_state, takefocus=False)
flair_button = Checkbutton(slider_frame, bg=bg_color, \
	justify=CENTER, variable=checkbutton7_var, command=slider7_state, takefocus=False)
repeat_button = Checkbutton(slider_frame, bg=bg_color, \
	justify=CENTER, variable=checkbutton8_var, command=slider8_state, takefocus=False)
silence_button.grid(column="1", row="0", sticky="s")
sustain_button.grid(column="2", row="0", sticky="s")
note2_button.grid(column="3", row="0", sticky="s")
mute_button.grid(column="4", row="0", sticky="s")
pmute_button.grid(column="5", row="0", sticky="s")
flair_button.grid(column="6", row="0", sticky="s")
repeat_button.grid(column="7", row="0", sticky="s")
# slider labels
note1_label = Label(slider_frame, text="O", font=(None, 14), bg=bg_color, fg="white", width="3", takefocus=False)
silence_label = Label(slider_frame, text="-", font=(None, 14), bg=bg_color, fg="white", width="3", takefocus=False)
sustain_label = Label(slider_frame, text="o", font=(None, 14), bg=bg_color, fg="white", width="3", takefocus=False)
note2_label = Label(slider_frame, text="1", font=(None, 14), bg=bg_color, fg="white", width="3", takefocus=False)
mute_label = Label(slider_frame, text="X", font=(None, 14), bg=bg_color, fg="white", width="3", takefocus=False)
pmute_label = Label(slider_frame, text="p", font=(None, 14), bg=bg_color, fg="white", width="3", takefocus=False)
flair_label = Label(slider_frame, text="[]", font=(None, 14), bg=bg_color, fg="white", width="3", takefocus=False)
repeat_label = Label(slider_frame, text="R", font=(None, 14), bg=bg_color, fg="white", width="3", takefocus=False)
note1_label.grid(column="0", row="1", sticky="s")
silence_label.grid(column="1", row="1", sticky="s")
sustain_label.grid(column="2", row="1", sticky="s")
note2_label.grid(column="3", row="1", sticky="s")
mute_label.grid(column="4", row="1", sticky="s")
pmute_label.grid(column="5", row="1", sticky="s")
flair_label.grid(column="6", row="1", sticky="s")
repeat_label.grid(column="7", row="1", sticky="s")
# creating sliders
note1_scale = Scale(slider_frame, from_="100", to="1", resolution="1", showvalue="0", \
	bg=bg_color, length="118", variable=note1_var, sliderlength="15", \
	troughcolor=throughcolor, activebackground=rollover_color2, width="22", takefocus=False)
silence_scale = Scale(slider_frame, from_="100", to="0", resolution="1", showvalue="0", \
	bg=bg_color, length="118", variable=silence_var, sliderlength="15", \
	troughcolor=throughcolor, activebackground=rollover_color2, width="22", takefocus=False)
sustain_scale = Scale(slider_frame, from_="100", to="0", resolution="1", showvalue="0", \
	bg=bg_color, length="118", variable=sustain_var, sliderlength="15", \
	troughcolor=throughcolor, activebackground=rollover_color2, width="22", takefocus=False)
note2_scale = Scale(slider_frame, from_="100", to="0", resolution="1", showvalue="0", \
	bg=bg_color, length="118", variable=note2_var, sliderlength="15", state=DISABLED, \
	troughcolor=throughcolor, activebackground=rollover_color2, width="22", takefocus=False)
mute_scale = Scale(slider_frame, from_="100", to="0", resolution="1", showvalue="0", \
	bg=bg_color, length="118", variable=mute_var, sliderlength="15", state=DISABLED, \
	troughcolor=throughcolor, activebackground=rollover_color2, width="22", takefocus=False)
pmute_scale = Scale(slider_frame, from_="100", to="0", resolution="1", showvalue="0", \
	bg=bg_color, length="118", variable=pmute_var, sliderlength="15", state=DISABLED, \
	troughcolor=throughcolor, activebackground=rollover_color2, width="22", takefocus=False)
flair_scale = Scale(slider_frame, from_="100", to="0", resolution="1", showvalue="0", \
	bg=bg_color, length="118", variable=flair_var, sliderlength="15", \
	troughcolor=throughcolor, activebackground=rollover_color2, width="22", takefocus=False)
repeat_scale = Scale(slider_frame, from_="100", to="0", resolution="1", showvalue="0", \
	bg=bg_color, length="118", variable=repeat_var, sliderlength="15", \
	troughcolor=throughcolor, activebackground=rollover_color2, width="22", takefocus=False)
note1_scale.grid(column="0", row="2")
silence_scale.grid(column="1", row="2")
sustain_scale.grid(column="2", row="2")
note2_scale.grid(column="3", row="2")
mute_scale.grid(column="4", row="2")
pmute_scale.grid(column="5", row="2")
flair_scale.grid(column="6", row="2")
repeat_scale.grid(column="7", row="2")
# entries for sliders
note1_entry = Entry(slider_frame, justify="center", bd="0", width="3", font=(None, 8), takefocus=True, \
	textvariable=note1_var)
silence_entry = Entry(slider_frame, justify="center", bd="0", width="3", font=(None, 8), takefocus=True, \
	textvariable=silence_var)
sustain_entry = Entry(slider_frame, justify="center", bd="0", width="3", font=(None, 8), takefocus=True, \
	textvariable=sustain_var)
note2_entry = Entry(slider_frame, justify="center", bd="0", width="3", font=(None, 8), takefocus=True, \
	textvariable=note2_var)
mute_entry = Entry(slider_frame, justify="center", bd="0", width="3", font=(None, 8), takefocus=True, \
	textvariable=mute_var)
pmute_entry = Entry(slider_frame, justify="center", bd="0", width="3", font=(None, 8), takefocus=True, \
	textvariable=pmute_var)
flair_entry = Entry(slider_frame, justify="center", bd="0", width="3", font=(None, 8), takefocus=True, \
	textvariable=flair_var)
repeat_entry = Entry(slider_frame, justify="center", bd="0", width="3", font=(None, 8), takefocus=True, \
	textvariable=repeat_var)
note1_entry.grid(column="0", row="3", sticky="s", pady=(3, 0))
silence_entry.grid(column="1", row="3", sticky="s", pady=(3, 0))
sustain_entry.grid(column="2", row="3", sticky="s", pady=(3, 0))
note2_entry.grid(column="3", row="3", sticky="s", pady=(3, 0))
mute_entry.grid(column="4", row="3", sticky="s", pady=(3, 0))
pmute_entry.grid(column="5", row="3", sticky="s", pady=(3, 0))
flair_entry.grid(column="6", row="3", sticky="s", pady=(3, 0))
repeat_entry.grid(column="7", row="3", sticky="s", pady=(3, 0))
# validating slider inputs
note1_entry.configure(validate="all", vcmd=(reg, '%P'), invcmd=invalid_entry)
silence_entry.configure(validate="all", vcmd=(reg, '%P'), invcmd=invalid_entry)
sustain_entry.configure(validate="all", vcmd=(reg, '%P'), invcmd=invalid_entry)
note2_entry.configure(validate="all", vcmd=(reg, '%P'), invcmd=invalid_entry, state=DISABLED)
mute_entry.configure(validate="all", vcmd=(reg, '%P'), invcmd=invalid_entry, state=DISABLED)
pmute_entry.configure(validate="all", vcmd=(reg, '%P'), invcmd=invalid_entry, state=DISABLED)
flair_entry.configure(validate="all", vcmd=(reg, '%P'), invcmd=invalid_entry)
repeat_entry.configure(validate="all", vcmd=(reg, '%P'), invcmd=invalid_entry)




# key/legend
key_var = StringVar()
key_message = note1 + " = Note 1"
key_frame = LabelFrame(extra_frame, bg=bg_color, text="Key", fg="white", font=(None, 12))
key_frame.grid(row="0", column="0", padx="7", pady=(8,0), sticky="s")
key = Label(key_frame, bg="white", height="8", width="12", padx="0", \
	font=(None, 10), textvariable=key_var, justify="left", takefocus=False)
key.grid(column="0", row="0")
key_contents.append(key_message)
key_var.set(key_contents)
silence_button.invoke()
sustain_button.invoke()
flair_button.invoke()
repeat_button.invoke()




# result and message boxes
message_box = Label(results_frame, bg="black", fg="white", width="36", height="1", \
	anchor="w", textvariable=message_box_var, takefocus=False, font=("Helvetica", 13))
triplet_box = Label(results_frame, bg="black", fg="white", width="20", height="1", \
	anchor="e", textvariable=triplet_box_var, takefocus=False, font=("Helvetica", 13))
result_box = Label(results_frame, bg="white", fg="black", width="37", \
	height="2", textvariable=result_box_var, wraplength="400", font=(None, 20), takefocus=False)
message_box.grid(row="0", column="0", padx=(1,0))
triplet_box.grid(row="0", column="1", padx=(0,1))
result_box.grid(row="1", column="0", columnspan="2", padx=(1,0))




# sound bar
#buttons
play_button = Button(sound_frame, fg="black", activebackground=rollover_color, \
	width="3", highlightbackground=bg_color, textvariable=play_pause_var, \
	command=play_to_pause, font=(None, 12), justify="center", padx="13", takefocus=False) 
loop_button = Button(sound_frame, fg="black", activebackground=rollover_color, \
	width="3", highlightbackground=bg_color, command=loop_to_looping, \
	font=(None, 12), textvariable=looping_var, justify="center", takefocus=False)
save_menu = Menubutton(sound_frame, text="Save", bg=bg_color, direction="above", \
	justify=LEFT, width="7", font=(None, 12), padx="0", takefocus=False)
save_menu.menu = Menu(save_menu, tearoff = 0)
save_menu["menu"] = save_menu.menu
save_menu.menu.add_command(label=".WAV", state=DISABLED)
save_menu.menu.add_command(label=".TXT", command=save_text)
play_button.grid(row="0", column="6", sticky="e", padx=(0, 0))
loop_button.grid(row="0", column="5", sticky="e")
save_menu.grid(row="0", column="4", sticky="se")
play_button.configure(state=DISABLED)
loop_button.configure(state=DISABLED)
save_menu.configure(state=DISABLED)
# sliders
pitch_slider = Scale(sound_frame, orient="horizontal", from_="0", to="100", resolution="1", showvalue="0", \
	bg=bg_color, length="90", width="13", variable=pitch_var, sliderlength="13", bd="0", \
	troughcolor=throughcolor, activebackground=rollover_color2, takefocus=False)
tempo_slider = Scale(sound_frame, orient="horizontal", from_="0", to="100", resolution="1", showvalue="0", \
	bg=bg_color, length="90", width="13", variable=tempo_var, sliderlength="13", bd="0", \
	troughcolor=throughcolor, activebackground=rollover_color2, takefocus=False)
pitch_slider.grid(row="0", column="1", sticky="w", padx=(0, 12))
tempo_slider.grid(row="0", column="3", sticky="e", padx=(0, 12))
# labels
pitch_label = Label(sound_frame, text="Pitch", bg=bg_color, fg="white", width="3", \
	font=(None, 12, "bold"), takefocus=False)
tempo_label = Label(sound_frame, text="Speed", bg=bg_color, fg="white", width="4", \
	font=(None, 12, "bold"), takefocus=False)
pitch_label.grid(row="0", column="0", sticky="w", padx=(4, 4))
tempo_label.grid(row="0", column="2", sticky="e", padx=(0, 4))




# tooltip time
# http://www.voidspace.org.uk/python/weblog/arch_d7_2006_07_01.shtml for code tbh
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT, background=tooltip_color, borderwidth=1, \
        	font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
        root.after(4000, toolTip.hidetip) # my own code that waits two seconds and deletes message
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

createToolTip(new_gen, "Replace current riff with a new riff\nShortcut: 'Return'")
createToolTip(add_gen, "Attempt to add a new riff to the end of the old riff")
createToolTip(shorter_measures, "Decrease the note division. This action\nwill not affect the number of measures")
createToolTip(longer_measures, "Increase the note division. This action\nwill not affect the number of measures")
createToolTip(random_button, "Replace current riff with a riff\nwith every parameter randomized\n\
Shortcut: 'Shift+Return'")
createToolTip(clear_button, "Clear current riff and any error messages")
createToolTip(play_button, "Play current riff with sine waves\nAs of now, all commands are void \n\
during playback. Shortcut: 'Command+P'")
createToolTip(info_button, "Press Command+i to view the documentation")
createToolTip(loop_button, "Once pressed, play will loop four times\n'Shift+Space+P' will also trigger the loop ")
createToolTip(save_menu, "Save current riff as a text file named 'My_Riff' saved\nto your downloads folder. \
Saving to WAV is still a WIP")
createToolTip(pitch_label, "Change the pitch of the notes, which\nare fixed in relation to each other")
createToolTip(tempo_label, "Change the speed the riff is played back at")
createToolTip(pitch_slider, "Change the pitch of the notes, which\nare fixed in relation to each other")
createToolTip(tempo_slider, "Change the speed the riff is played back at")
createToolTip(notes_label, "Choose note division")
createToolTip(slider_frame, "Each slider represents the likelihood of it's respective note appearing \
in the\n riff. Unchecking a checkbox is the same as setting a slider to zero. See the Key\n\
for abbreviation meanings. See 'Info' under options for further documentation.")
createToolTip(message_box, "Error notifications will appear here")
createToolTip(triplet_box, "Triplet declarations will appear here")
	



# event binding
# enter to control new_gen
def bgcolor_button_enter():
	new_gen.configure(highlightbackground=bg_color)
def enter_callback(event=None):
	new_gen.configure(highlightbackground=blue_color)
	root.after(250, bgcolor_button_enter)
	new_gen.invoke()
root.bind('<Return>', enter_callback)
# shift return to control random button
def bgcolor_button_shiftenter():
	random_button.configure(highlightbackground=bg_color)
def shiftenter_callback(event=None):
	random_button.configure(highlightbackground=blue_color)
	root.after(250, bgcolor_button_shiftenter)
	random_button.invoke()
root.bind('<Shift-Return>', shiftenter_callback)
# command p to control play
def bgcolor_button_commandp():
	play_button.configure(highlightbackground=bg_color)
def commandp_callback(event=None):
	if play_button['state'] == NORMAL:
		play_button.configure(highlightbackground=blue_color)
		root.after(250, bgcolor_button_commandp)
		play_button.invoke()
	if play_button['state'] == DISABLED:
		pass
root.bind('<Command-p>', commandp_callback)
# shift-space-p to control loop playback
def bgcolor_button_command_p():
	play_button.configure(highlightbackground=bg_color)
def command_p_callback(event=None):
	if play_button['state'] == NORMAL:
		play_button.configure(highlightbackground=blue_color)
		root.after(250, bgcolor_button_command_p)
		loop_button.invoke()
		play_button.invoke()
	if play_button['state'] == DISABLED:
		pass
root.bind('<Command-P>', command_p_callback)
# command-i to open info
def bgcolor_button_commandi():
	info_button.configure(highlightbackground=bg_color)
def commandi_callback(event=None):
	info_button.configure(highlightbackground=blue_color)
	root.after(250, bgcolor_button_commandi)
	info_button.invoke()
root.bind('<Command-i>', commandi_callback)
# escape key to clear everything
def bgcolor_button_escape():
	clear_button.configure(highlightbackground=bg_color)
def escape_callback(event=None):
	if clear_button['state'] == NORMAL:
		clear_button.configure(highlightbackground=blue_color)
		root.after(250, bgcolor_button_escape)
		clear_button.invoke()
	if play_button['state'] == DISABLED:
		pass
root.bind('<Escape>', escape_callback)
# cmd-leftarrow to decrease division
def bgcolor_button_commandleft():
	shorter_measures.configure(highlightbackground=bg_color)
def commandleft_callback(event=None):
	state = str(shorter_measures['state'])
	if state == "normal":
		shorter_measures.configure(highlightbackground=blue_color)
		root.after(250, bgcolor_button_commandleft)
		shorter_measures.invoke()
	if state == 'disabled':
		pass
root.bind('<Option-Left>', commandleft_callback)
# cmd-rightarrow to increase division
def bgcolor_button_commandright():
	longer_measures.configure(highlightbackground=bg_color)
def commandright_callback(event=None):
	state = str(longer_measures['state'])
	if state == "normal":
		longer_measures.configure(highlightbackground=blue_color)
		root.after(250, bgcolor_button_commandright)
		longer_measures.invoke()
	if state == 'disabled':
		pass
root.bind('<Option-Right>', commandright_callback) 
# control-s to save
def bgcolor_button_commands():
	save_menu.configure(bg=bg_color)
def commands_callback(event=None):
	if save_menu['state'] == NORMAL:
		save_menu.configure(bg=blue_color)
		root.after(250, bgcolor_button_commands)
		root.after(500, save_text)
	if save_menu['state'] == DISABLED:
		pass
root.bind('<Command-s>', commands_callback)
# shift-escape to quit
def shiftescape_callback(event=None):
	root.destroy()
root.bind('<Shift-Escape>', shiftescape_callback)
# turns left clicks over sliders into right clicks so the slider jumps
def s1_callback(event=None):
	note1_scale.event_generate('<Button-2>', x=event.x, y=event.y)
note1_scale.bind('<Button-1>', s1_callback)
def s1_callback(event=None):
	silence_scale.event_generate('<Button-2>', x=event.x, y=event.y)
silence_scale.bind('<Button-1>', s1_callback)
def s1_callback(event=None):
	sustain_scale.event_generate('<Button-2>', x=event.x, y=event.y)
sustain_scale.bind('<Button-1>', s1_callback)
def s1_callback(event=None):
	note2_scale.event_generate('<Button-2>', x=event.x, y=event.y)
note2_scale.bind('<Button-1>', s1_callback)
def s1_callback(event=None):
	mute_scale.event_generate('<Button-2>', x=event.x, y=event.y)
mute_scale.bind('<Button-1>', s1_callback)
def s1_callback(event=None):
	pmute_scale.event_generate('<Button-2>', x=event.x, y=event.y)
pmute_scale.bind('<Button-1>', s1_callback)
def s1_callback(event=None):
	flair_scale.event_generate('<Button-2>', x=event.x, y=event.y)
flair_scale.bind('<Button-1>', s1_callback)
def s1_callback(event=None):
	repeat_scale.event_generate('<Button-2>', x=event.x, y=event.y)
repeat_scale.bind('<Button-1>', s1_callback)
def s1_callback(event=None):
	tempo_slider.event_generate('<Button-2>', x=event.x, y=event.y)
tempo_slider.bind('<Button-1>', s1_callback)
def s1_callback(event=None):
	pitch_slider.event_generate('<Button-2>', x=event.x, y=event.y)
pitch_slider.bind('<Button-1>', s1_callback)




raise_app()
root.mainloop()
###########################################################################################################################################################

"""
___________________________________________________FUTURE UPDATES__________________________________

FUNCTIONALALITY/BUGS/IMPROVEMENTS/GUI/UPDATES:
- add error message when trying to command-s while there is no loaded riff

NEXT RELEASE:
- make any shortcut using ESCAPE be activated ONLY on key UP
- allow closing from right clicking on the dashboard icon
- remove limitations created by the add function
- save all riffs to a cache or temp text file and add a back button in case someone misses their old riff
- change info to "options" menubar with a 'preferences' tab that leads to a pop-up allowing
	you to change the note symbols, shortcuts, and amount of loop reps
- add a tab to switch between results and custom riff with editable canvas to allow riff creation
	(opened text files will also appear here)
- Save Function
	- make cascading directories for saving?
	- make a save text template with Rhygen info and datetime printed on it?
	- allow .TXT files to be played back
- Playback
	- add a save audio function (multiple formats)
	- convince audio player to not stall the app
	- add metronome
	- add spacebar playability

- add additional strings?
- animate splash screen?
- audio player plays too longs sometimes when just just single notes?
- suppress deprecation warning?
"""


