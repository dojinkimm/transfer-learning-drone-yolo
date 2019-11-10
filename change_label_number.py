"""
Py file that changes originally labelled numbers to number I want to change.
e.g. 15 0.xx 0.xx 0.xx 0.xx -> 0 0.xx 0.xx 0.xx 0.xx
"""
import os

label_to_change = ['15']
new_label = "0"


def main():
    path = "PATH/TO/LABELS"
    dir_list = os.listdir(path)

    for txt in sorted(dir_list):
        data = []
        with open(path + txt) as file:
            print(txt)

            for line in file:
                index = line[:2].rstrip()

                # changes label number if in variable label_to_change
                if index in label_to_change:
                    data.append(new_label+line[2:])

        if len(data) > 0:
            with open(path+txt, "w") as file:
                for d in data:
                    file.write(d)


if __name__ == '__main__':
    main()
