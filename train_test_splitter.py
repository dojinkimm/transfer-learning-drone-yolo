"""
Py file that splits image dataset into test set & training set.
Then, saves the path to images in test.txt and train.txt.
The ratio is defined in variable train_ratio, and can be modified.
"""
import os
import random

train_ratio = 0.8


def main():
    cur_dir = os.getcwd()
    path_image = cur_dir + "/images/"
    dir_image_list = os.listdir(path_image)

    random.shuffle(dir_image_list)
    train_imgs = int(len(dir_image_list) * train_ratio)

    with open(cur_dir + "/train.txt", "w") as file:
        for d in dir_image_list[:train_imgs]:
            file.write(path_image + d + "\n")

    with open(cur_dir + "/test.txt", "w") as file:
        for d in dir_image_list[train_imgs:]:
            file.write(path_image + d + "\n")


if __name__ == '__main__':
    main()
