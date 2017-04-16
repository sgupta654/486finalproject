# Accept a subreddit name as an argument, and produce a viewer-compatible json file.
# Assume that 
# * there is no need to check for a current version of the json
# * the argument is properly capitalized
#
# Creates a subreddit + ".lock" file to help prevent multiple processes doing the same thing. The file also displays progress.
#

import subprocess
import sys
import os
from threading import Timer
import time

print sys.argv
subreddit = sys.argv[1]
threshold = sys.argv[2]
try:
    algorithm = sys.argv[3]
except:
    algorithm = "openord"

# Create a "lock" file. If it already exists, terminate.
if os.path.isfile("locks/" + subreddit + threshold + algorithm + ".lock"):
    print "For request " + subreddit + threshold + algorithm + ", lock file was found. Terminating."
    quit()

lockfile = open("locks/" + subreddit + threshold + algorithm + ".lock", "w", 0) # Don't buffer
lockfile.write("Created lock file.\n")


# Check if the DB is up-to-date (younger than 1 day). If not, update the archive and the DB.

one_day = time.time() - 60 * 60 * 24 # 24 hours ago.

# if the time the DB was made is older than one day...
dbpath = "DBs/"+ subreddit + "_db.pickle"
if not os.path.isfile(dbpath) or os.path.getmtime(dbpath) <  one_day:
    lockfile.write("Updating r/ archive (this may take up to 4 minutes)\n")
    lockfile.flush()
    lockfile.close()
    print "updating db"
    # Pipe the output into the lock file for better interactivity
    # Update the r/ archive.
    # Using stdbuf to disable buffer
    cmd = subprocess.Popen("stdbuf -oL python commentArchiver.py " + subreddit + ">> locks/" + subreddit + threshold + algorithm + ".lock", shell=True).wait()
    # Update DB
    cmd = subprocess.Popen("python readCommentsAndSave.py " + subreddit, shell=True).wait()
    lockfile = open("locks/" + subreddit + threshold + ".lock", "w", 0)
    lockfile.write("Archive updated\n")
    
print "Gephify"
# Package a file for gephi input.
lockfile.write("Gephifying\n")

csvfile = "out/" + subreddit + threshold + ".csv"
if not os.path.isfile(csvfile) or os.path.getmtime(csvfile) <  one_day:
    cmd = subprocess.Popen("python gephifyer.py " + subreddit + " " + threshold, shell=True).wait()


# Process via Gephi
lockfile.write("Processing with Gephi\n")
cmd = subprocess.Popen("java -jar gephiAutomation.jar " + subreddit + " " + threshold + " " + algorithm, shell=True).wait()

# Jsonify the resulting svg
lockfile.write("Merging graph and data\n")
cmd = subprocess.Popen("python JsonFromSVG.py " + subreddit + " " + threshold + " " + algorithm, shell=True).wait()


lockfile.write("Done.")
# Delete the "lock" file after 11 seconds.
def deleteLock():
    subprocess.Popen(["rm", "locks/" + subreddit + threshold + algorithm + ".lock"], stdout=subprocess.PIPE)
    print "Lock file deleted"
t = Timer(11.0, deleteLock)
t.start()
