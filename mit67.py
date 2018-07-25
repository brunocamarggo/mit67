import config
from os import listdir
from os.path import join
from classes import MIT67Annotation
from skimage import io
from utils import imshow

if __name__ == '__main__':
    annotations_path = config.paths['ANNOTATIONS']
    images_path = config.paths['IMAGES']
    dirs = [dir_ for dir_ in listdir(annotations_path)]
    for i, val in enumerate(dirs):
        for xml in listdir(annotations_path+dirs[i]):
            f = annotations_path + dirs[i] + '/' + xml
            img = io.imread(join(join(images_path, dirs[i]), xml.replace('.xml', '.jpg')))
            ann = MIT67Annotation(xml=f)
            imshow(name=ann.filename, image=img)
            for obj in ann.objects:
                bb = obj['bound_box']
                cropped = img[bb['min_y']:bb['max_y'], bb['min_x']:bb['max_x']]
                imshow(name=obj['name'], image=cropped)
                print(bb)


