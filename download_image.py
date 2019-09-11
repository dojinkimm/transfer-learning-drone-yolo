from google_images_download import google_images_download

# class instantiation
response = google_images_download.googleimagesdownload()

# creating list of arguments
arguments = {"keywords":"DJI, DJI phantom, DJI phantom nature", "limit": 20, "print_urls": True}
# passing the arguments to the function
paths = response.download(arguments)
# printing absolute paths of the downloaded images
print(paths)
