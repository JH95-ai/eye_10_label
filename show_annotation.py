# python
import os
import numpy as np
import json
import xml.dom.minidom
import cv2

DefectImagePath = '/home/ts-liqing/Downloads/智能视觉-李晴'


def eachFiles(file_path):
    files = []
    jsons = []
    file_names = os.listdir(file_path)
    for file in file_names:
        path = file_path + '/' + file
        if os.path.isfile(path):
            items = os.path.splitext(path)
            if items[1] == ".jpg" or items[1] == ".JPG" or items[1] == ".png":
                files.append(path)
                jsons.append(items[0] + ".json")
        else:
            eachFiles(path)
    return files, jsons


def doJsonResult(img, file):
    json_data = None
    with open(file, 'r', encoding='utf8')as fp:
        json_data = json.load(fp)

    print(json_data)
    mark = json_data["markResult"]
    info = json_data["options"]
    width = info["imgWidth"]
    height = info["imgHeight"]

    features = mark["features"]
    for feat in features:
        geometry = feat["geometry"]
        coord = geometry["coordinates"]
        x = coord[0]
        y = coord[1]
        # print("(%.3f, %.3f)" % (x, y))
        cv2.circle(img, (int(x), int(y)), 1, (0, 200, 0), -1)


def showOneImage():
    # imgs, jsons = eachFiles(DefectImagePath)

    img = cv2.imread('/home/ts/Documents/DMS/eye_10_label/images/images/000019.jpg')

    doJsonResult(img, '/home/ts/Documents/DMS/eye_10_label/images/vals/000019.json')

    img = cv2.resize(img, (600, 800))
    # cv2.imwrite("./temp.jpg", img)
    cv2.imshow("input image", img)
    key = cv2.waitKey(0)
    print(key)
    if key == 110:
        print('next')
    elif key == 27:
        return

    # for index, im in enumerate(imgs):
    #     img = cv2.imread(im)
    #
    #     doJsonResult(img, jsons[index])
    #
    #     cv2.imshow("input image", img)
    #     key = cv2.waitKey(0)
    #     print(key)
    #     if key == 110:
    #         print('next')
    #         continue
    #     elif key == 27:
    #         break
    # destory all windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    showOneImage()