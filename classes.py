import xml.etree.ElementTree as ET
import config
from os import listdir
from os.path import join

from skimage import io
from skimage import transform
import cv2

class MIT67Annotation:

    def __init__(self, xml):
        ann = None
        try:
            root = ET.parse(xml).getroot()

            folder = root.find('folder').text.strip()
            filename = root.find('filename').text.strip()

            source_image = root.find('source').find('sourceImage').text.strip()
            source_annotation = root.find('source').find('sourceAnnotation').text.strip()
            source = {
                'sourceImage': source_image,
                'sourceAnnotation': source_annotation
            }
            object_list = []
            id = None
            scenedescription = None
            for object_ in root.findall('object'):
                name = object_.find('name').text.strip()
                deleted = object_.find('deleted').text.strip()
                date = object_.find('date').text.strip()

                try:
                    id = object_.find('id').text.strip()
                    scenedescription = root.find('scenedescription').text.strip()
                except:
                    id = None
                    scenedescription = None

                username = object_.find('polygon').find('username').text.strip()
                pts = []
                for pt in object_.find('polygon').findall('pt'):
                    x = int(pt.find('x').text.strip())
                    y = int(pt.find('y').text.strip())
                    pts.append((x, y))

                polygon = {
                    'username': username,
                    'pts': pts
                }

                min_x = min(pts, key=lambda item: item[0])[0]
                min_y = min(pts, key=lambda item: item[1])[1]
                max_x = max(pts, key=lambda item: item[0])[0]
                max_y = max(pts, key=lambda item: item[1])[1]

                bound_box = {
                    'min_x': min_x,
                    'min_y': min_y,
                    'max_x': max_x,
                    'max_y': max_y
                }

                obj = {
                    'name': name,
                    'deleted': deleted,
                    'date': date,
                    'id': id,
                    'polygon': polygon,
                    'bound_box': bound_box
                }

                object_list.append(obj)

            self.folder = folder
            self.filename = filename
            self.source = source
            self.objects = object_list
            self.scenedescription = scenedescription

        except Exception as e:
            s = str(e)
            print(s)



    def __str__(self):
        str_ = '--- MIT67 Annotation ---\nFolder: {}\nFilename: {}\nSource: {}, Objects: {}, Scenedescription: {}'.\
            format(self.folder, self.filename, self.source, self.objects, self.scenedescription)
        return str_

if __name__ == '__main__':
    ann = MIT67Annotation(xml='/home/bruno/Documents/MIT67/Annotations/airport_inside/airport_inside_0001.xml')
    print(ann)
