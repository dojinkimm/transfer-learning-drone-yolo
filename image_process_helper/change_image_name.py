from os import listdir, rename

for index, filename in enumerate(listdir("images/")):
    src = 'images/' + filename
    dst = 'images/' + str(index+703) + ".jpg"

    rename(src, dst)
