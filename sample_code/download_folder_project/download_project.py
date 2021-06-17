# Purpose:
# The purpose of this programm is to automatically clean up your downloads folder

# The very powerful module "os" enables us to work with directories
import os

#--------------------------------------DEFINITIONS / VAIABLES---------------------------------#

# STEP 0:
# Type your path of the folder you want to organise in here
directory = "/Users/matthias/Downloads"
# If you want to extend the path don't use string operations, use the method os.path.join(path1, path2)
# Reason for this is to make sure the right separators are used based on your operating system. E.g. in win10 it would be '\'
path_images = os.path.join(directory, 'images') #the outcome should be /Users/matthias/Downloads/images
path_videos = os.path.join(directory, 'videos')
path_music = os.path.join(directory,  'music')
path_docs = os.path.join(directory, 'documents')
path_zip = os.path.join(directory, 'zips')




#--------------------------------------MAIN Programm---------------------------------------#

# STEP 1:
# If the folders are not created already, create them
if os.path.exists(path_images) is False:
    os.mkdir(path_images)
if os.path.exists(path_zip) == False:
    os.mkdir(path_zip)
if os.path.exists(path_docs) == False:
    os.mkdir(path_docs)
if os.path.exists(path_music) == False:
    os.mkdir(path_music)
if os.path.exists(path_videos) == False:
    os.mkdir(path_videos)

# STEP 2:
# We'll go through all the files in our Downloads folder
for filename in os.listdir(directory):
    # We have to adjust our path therefore we use the os.path.join method/function
    source = os.path.join(directory, filename)
    # print(source) #you can also print it out to display your path/filename.ending

    # Now we have to check which file type the file of this iteration is. Will it be an image, a pdf or something else?

    # If the filname starts with x_ it should not be moved
    if filename.startswith('x_'):
        continue # therefore we will just skip this iteration of the loop

    # photos
    # os.path.splitext will seperate filename into a tuple (similar to a list), we can simply get the last item of the tuple by using the index [-1]. Now that we have the ending of our filename, we can compare it...
    elif os.path.splitext(filename)[-1].lower() in ['.png', '.jpg', '.jpeg', '.gif']: #the string.lower() method/function will lower all the letters. This is important, because it could also be an image.PNG
        # Okay this file is an image, so we will have to define our target which it should be stored in. Remember the os.path.join() function?
        target = os.path.join(path_images, filename)
        # Now we can move the file by renaming its path. Therefore our beloved "os" package comes in handy once again. os.rename(path1, path2) will replace the path1 with path2
        os.rename(source, target)
        # DONE! It's basically copy paste from here.. ;D
    # videos
    elif os.path.splitext(filename)[-1].lower() in ['.mov', '.mp4']:
        target = os.path.join(path_videos, filename)
        os.rename(source, target)
    # music
    elif os.path.splitext(filename)[-1].lower() in['.mp3', '.wav', '.aac' ] :
        target = os.path.join(path_music, filename)
        os.rename(source, target)
    # docs
    elif os.path.splitext(filename)[-1].lower() in [ '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls' , '.xlsx'] :
        target = os.path.join(path_docs, filename)
        os.rename(source, target)
    # zips
    elif os.path.splitext(filename)[-1].lower() in ['.zip', '.tar', '.gz']:
        target = os.path.join(path_zip, filename)
        os.rename(source, target)

    # Lastly, we want to move ANY other file AND DIRECTORY into our documents folder. The only exceptions are the folders we created ourselves.
    # If you don't want the program to do this, you can just delete the next few lines of code.
    elif filename not in ['documents', 'images', 'videos', 'zips', 'music', 'old_stuff']:
        target = os.path.join(path_docs, filename)
        os.rename(source, target)


#---------------------------------------------ADVANCED STUFF----------------------------#
# The code below will add an additional folder called "old_stuff" and will put any files that are older than 31 days into that folder.


# These packages will be used for the advanced stuff
from datetime import datetime # datetime adds functionality for timekeeping - we will use it to determine the date in seconds
from datetime import timezone

# Same as above
path_oldstuff = os.path.join(directory, 'old_stuff')
if os.path.exists(path_oldstuff) == False:
    os.mkdir(path_oldstuff)

#This function will check the age of the file using the path as parameter
def check_age(file):
    # print(os.stat(os.path.join(directory,filename))[8])
    # we will get our current time by using the package datetime.
    dt =datetime.now(timezone.utc) # this method will return the datetime of the given timezone
    utc_time = dt.replace(tzinfo=timezone.utc) # this method will format our datetime to the given timezone
    utc_timestamp = utc_time.timestamp() # now we have our timestamp in seconds based on the UTP(seconds passed since 01.01.1970)
    file_timestamp = os.stat(file)[8] # to get the last modified time of the file, we will use the os.stat(file) which will return a structure of properties, the 8th value of this structur represents the timestamp of the given file
    current_time = utc_timestamp
    time_delay = (current_time - file_timestamp)/(3600 * 24) # the difference of this timestamp is still in seconds, remember! We want all the files older then 1 month to be stored in the old stuff folder
    #print(time_delay)
    # Now that we have the time delay calculated in days, we will return true if its older than 31 days, if not false
    if time_delay >= 31:
        return True
    else:
        return False

# Based on the funcion check_age this function will move a file to the old_stuff folder
def move_old_files(directory):
    # Check all files if they are old, therefore we will once again use a loop
    for filename in os.listdir(directory):
        source = os.path.join(directory, filename) # define our source
        if os.path.isdir(source): #remember, if we have folders, we also have to check the timestamp of the files in there
            subfolder = source
            # now we will iterate through the files in the subfolder
            for subfile in os.listdir(subfolder):
                # we have to change once again our source path and define the target path
                source = os.path.join(subfolder, subfile)
                target = os.path.join(path_oldstuff, subfile)
                if check_age(source):
                    os.rename(source, target)

        elif check_age(source):
            target = os.path.join(path_oldstuff, filename)
            os.rename(source, target)

# this method will check the age of the files, based on their last modified timestamp
move_old_files(directory)
