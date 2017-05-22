#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import sys
import os
import glob
import shutil
import commands
import subprocess
import wikitools
import poster
import time
import datetime
import os
import sys
import logging

ts = time.time()
timestamp  = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

audio = glob.glob("/audio/*.wav")
print audio


if not os.path.isdir("./log"):
            os.mkdir("./log")


# create a file handler
log_file = './log/commons_uploader_' + timestamp + '_log.txt'

handler = logging.FileHandler(log_file)
handler.setLevel(logging.INFO)

# create a logging format

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger

logger.addHandler(handler)



logger.info("Trying to login to commons ")


wiki_url = "https://commons.wikimedia.org/w/api.php"
wiki_username = "USERNAME"
wiki_password = "PASSWORD"

logger.info("Wiki URL = " + wiki_url)


try:
	wiki = wikitools.wiki.Wiki(wiki_url)
except:
	message =  "Can not connect with wiki. Check the URL"
	logger.info(message)




login_result = wiki.login(username=wiki_username,password=wiki_password)
message =  "Login Status = " + str(login_result)
logging.info(message)


if login_result == True:
        message =  "\n\nLogged in to "  +  wiki_url.split('/w')[0]
	logging.info(message)
else:
        message =  "Invalid username or password error"
	logging.info(message)
        sys.exit()




def check_for_bot(username):
            user = wikitools.User(wiki,username)
            if 'bot' in user.groups:
                        return "True"



logging.info("Checking for bot access rights")
bot_flag = check_for_bot(wiki_username)

if bot_flag:
            logging.info("The user " + wiki_username + " has bot access.")
else:
            logging.info("The user " + wiki_username + " does not have bot access")



#############


wikitionary_url = "https://ta.wiktionary.org/w/api.php"


logger.info("Wiki URL = " + wikitionary_url)


try:
	wikitionary = wikitools.wiki.Wiki(wikitionary_url)
except:
	message =  "Can not connect with wiki. Check the URL"
	logger.info(message)




login_result = wikitionary.login(username=wiki_username,password=wiki_password)
message =  "Login Status = " + str(login_result)
logging.info(message)


if login_result == True:
        message =  "\n\nLogged in to "  +  wikitionary_url.split('/w')[0]
	logging.info(message)
else:
        message =  "Invalid username or password error"
	logging.info(message)
        sys.exit()





temp_folder = "./" + "audio_files_" + timestamp 
 
def move_file(file):
        source = file
        destination = temp_folder

        if os.path.isdir(temp_folder):
                shutil.move(source,destination)
        else:
                os.mkdir(temp_folder)
                shutil.move(source,destination)
        message = "Moving the file " + file + " to the folder " + temp_folder + "\n"
	logging.info(message)
                              


def upload_file(file):
	

	file_name = file.split(".ogg")[0]
	
	
	caption = "Audio pronunciation of the term '" + file_name + " 'in Tamil Language. "
	print caption
	
	file_object=open(file,"r")
	audio=wikitools.wikifile.File(wiki=wiki, title=file_name)
       	audio.upload(fileobj=file_object,comment=caption, ignorewarnings=True)
	print "Uploaded the File " + file_name

	page_name = file_name.replace(" ","_")

	page_url = "File:" + page_name

	page = wikitools.Page(wiki, page_url, followRedir=True)

	print page
	print page.title
	print page.namespace

#	wikidata = "=={{int:filedesc}}=={{Information|description={{en|1= " + caption + "}}{{TamilWiki Media Contest}}|source={{own}}|author=[[User:" + wiki_username + "|" + wiki_username + "]]}}=={{int:license-header}}=={{self|cc-by-sa-3.0}}[[Category:" + category + "]] [[Category:Uploaded with MediawikiUploader]]"


	wikidata = " {{Information |Description= " + caption + "|Source= Self |Author= [[User: " +  wiki_username + "|" + wiki_username + " ]] |Permission=Dual licensed per GFDL Version 1.2 or later / Creative Commons Attribution ShareAlike license versions 2.5, 2.0, and 1.0 as noted.}} == {{int:license}} == {{self|GFDL|Cc-by-sa-3.0-migrated|Cc-by-sa-2.5,2.0,1.0}} [[Category:Tamil pronunciation|" +  file_name + "]] "


	page.edit(text=wikidata.encode('utf-8'),summary =caption)

	move_file(file)
		

def link_to_wiktionary(pagename):

   
        logging.info("Wiktionary Page name = " + pagename)

           
        content = "* {{audio|{{PAGENAME}}.oga|பலுக்கல் (ஐ.அ)}}"


        page = wikitools.Page(wikitionary, pagename, followRedir=True)

	edit_summary = "Added audio file for " + pagename

        page.edit(text=content,summary=edit_summary)
        
        message = "Uploaded at https://ta.wikisource.org/wiki/" + pagename + "\n"
	logging.info(message)
        time.sleep(5)
        logging.info("=========")








db = MySQLdb.connect(host="database",    # your host, usually localhost
                     user="lingualibre",         # your username
                     passwd="bienvenue",  # your password
                     db="lingualibre",        # name of the data base
		     charset='utf8',
                     use_unicode=True)

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM sounds")


for row in cur.fetchall():
	print row[3]
	source = "/audio/" + row[3]
	print "source=" + source
	destination = "."
	shutil.copy(source,destination)

	original_sound_text = row[4]
	print original_sound_text
	new_file = destination + "/" + original_sound_text + ".wav"
	print new_file
	shutil.copy(source,new_file)

	convert_command = "oggenc '" + new_file + "'" 
	print convert_command
#	print commands.getstatusoutput(convert_command)
	subprocess.call(['oggenc', new_file, '-o', original_sound_text + ".oga"])
#	subprocess.call(['avconv','-i',source,'-c:a','libvorbis','-qscale','255',original_sound_text + ".ogg"])
	upload_file(original_sound_text + ".oga")
	link_to_wiktionary(original_sound_text)
	
