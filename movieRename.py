import os
import re

# Hello, Welcome to this script! This script was made by Andreas Eike. This script will rename your movie files and
# directory name for each movie automatically, in the specified path. You can safely run this script without any options
# if this script is placed in a folder which contains folders, each folder with a different movie in it.
# The movie folder can contain multiple files, but the script only renames video files and subtitle files.

# Specify which path your movie folders are in.
path = os.path.dirname(__file__)

# An array which will hold some known illegal words, which will be removed if found in the filename string.
# Only used if no year is found in the string (A movie file without a year)
illegalWordList = []

# this array is used to store the name of files that could not be renamed. Probably because its not the right file type.
renameErrors = []

# Specifies the correct format for the finished movie name.
# Example:
# Correct syntax would be "Some Movie (1980)"
correctWordRegex = "(?! )^(?!.*  ).*[0-9]{3}[)]$"


# split the string into parts, by using regex.
# Returns an array of words, which can then be built together later.
def splitString(string):
    # remove the file extension part of the string
    string = string[:len(string) - 4]

    # remove some specific characters
    string = string.replace("[", "")
    string = string.replace("]", "")

    # Splits the string into parts, uses splitters such as " ", "." and "  "
    stringArr = re.split("\.|\s+|_| ", string)

    # Capitalizes words.
    stringArr = [f.capitalize() for f in stringArr]
    return stringArr


# check if word is illegal and should be removed, returns true or false
def wordIsIllegal(string):
    # sets the string to lower for unified comparison.
    string = string.lower()

    # if the word is illegal, return true.
    for removeWord in illegalWordList:
        if (string.find(removeWord.lower)) != -1:
            return True
        return False


# Removes illegal words.  If a year is found, the function simply removes all text that comes after the year. It also
# sets parenteses around the year string. If no year is found, a illegal word list is used. This is a seperate .txt
# file, called wordlist.
def removeWords(wordArr):
    index = 0
    yearFound = False
    for word in wordArr:

        # Checks is word is a year (and not the first word of the name). If so, sets parenteses around the year,
        # and then removes the rest of the string.
        if ifWordIsYear(word) and index != 0:
            yearFound = True
            if word[0] != "(" and word[len(word) - 1] != ")":
                word = "(" + word + ")"
                wordArr[index] = word
            break
        index += 1
    if yearFound:
        del wordArr[index + 1:len(wordArr)]

    # Else, use wordlist to remove words. Rarely used (only if no year is found in the movie filename).
    else:
        with open("wordlist.txt") as f:
            illegalWordArray = f.readlines()
        illegalWordArray = [x.strip() for x in illegalWordArray]
        illegalWordArray = [x.lower() for x in illegalWordArray]
        wordsToRemove = []
        for word in wordArr:
            if word.lower() in illegalWordArray:
                wordsToRemove.append(word)
        for word in wordsToRemove:
            wordArr.pop(wordArr.index(word))
    return wordArr


# check if word is year, returns true or false
def ifWordIsYear(string):
    if len(string)==4:
        match = re.match(r".*[1-3][0-9]{3}", string)
        if match is not None:
            return True
    return False


# Actually renames the files in your directory.
def renameFile(rootPath, oldFileName, newFileName):
    oldPath = os.path.join(rootPath, oldFileName)
    newPath = os.path.join(rootPath, newFileName)
    os.rename(oldPath, newPath)
    print("Renamed FILE", oldName, "to", newName, ".")


def renameDirectory(oldDirectoryName, newDirectoryName):
    oldPath = os.path.join(oldDirectoryName)
    newPath = os.path.join(newDirectoryName)
    if oldPath!=newPath:
        os.rename(oldPath, newPath)
        print("Renamed DIRECTORY", oldDirectoryName, "to", newDirectoryName)


# Basically os.walk, but with one level of walk to not include subdirectories
# from https://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below
def walkLevel(directory, level=1):
    directory = directory.rstrip(os.path.sep)
    assert os.path.isdir(directory)
    numSep = directory.count(os.path.sep)
    for walkRoot, walkDirs, walkFiles in os.walk(directory):
        yield walkRoot, walkDirs, walkFiles
        numSepThis = root.count(os.path.sep)
        if numSep + level <= numSepThis:
            del dirs[:]

if __name__ == "__main__":
    # For loop that repeats through your specfied directory 'path', assumes that video and subtitle files are stored in
    # seperate folders under your root path. no subdirectories are handled.
    for root, dirs, files in walkLevel(path):
        newName = ""
        oldName = ""
        # repeats for each file in the folder
        for name in files:
            oldName = name
            # Only rename if its a video or subtitle file.
            if name.find(".mkv") != -1 or name.find(".mp4") != -1 or name.find(".avi") != -1 or name.find(".srt") != -1:
                newName = name

                # Checks if the word is properly named. If not, continue and rename it.
                if newName.find("sample") == -1 and re.match(correctWordRegex, newName[:len(newName) - 4]) is None:
                    fileExtension = newName[len(newName) - 4:]

                    # If one file in the directory has already been renamed, no need to rename the second file
                    # (All files should have the same name, apart from the file extension)
                    if len(files) > 1 and re.match(correctWordRegex, files[0][:len(files[0]) - 4]) is not None:
                        newName = files[0][:len(files[0]) - 4] + fileExtension

                    # Else, build the string.
                    else:
                        newNameArr = splitString(newName)
                        newNameArr = removeWords(newNameArr)
                        newName = " ".join(newNameArr) + fileExtension
                    renameFile(root, name, newName)
            else:
                if root not in renameErrors:
                    renameErrors.append(root + "\\" + name)
        if newName != oldName and newName != "":
            joinPath = os.path.join(path, newName[:len(newName) - 4])
            renameDirectory(root, joinPath)
