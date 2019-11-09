import os

label = ['15']


def main():
    path = "/Users/dojinkim/Desktop/dataset_guava/drones/labels/"
    dir_list = os.listdir(path)

    for txt in sorted(dir_list):
        data = []
        with open(path + txt) as file:
            print(txt)
            # txt 파일 내에 labelling 된 부분 나눈다
            for line in file:
                index = line[:1].rstrip()

                if index in label:
                    data.append(line)

        if len(data) > 0:
            with open(path+txt, "w") as file:
                for d in data:
                    file.write(d)


if __name__ == '__main__':
    main()
