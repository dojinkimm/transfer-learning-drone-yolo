from google_images_download import google_images_download


# class instantiation
response = google_images_download.googleimagesdownload()

# creating list of arguments
# arguments = {"keywords": "DJI phantom 4 real job,DJI  phantom flying,DJI phantom nature,DJI phantom city",
#              "limit": 100, "print_urls": True}

arguments = {"keywords": "parrot drone fly,parrot drone farm,parrot drone city",
             "limit": 100, "print_urls": True}

# passing the arguments to the function
paths = response.download(arguments)
# printing absolute paths of the downloaded images
print(paths)


