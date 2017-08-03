from PIL import Image
import os

def listdir(path):
    result = []
    for file in os.listdir(path):
        if file[0] == '.': continue
        temp_path = os.path.join(path, file)
        if os.path.isdir(temp_path): 
            result.extend(listdir(temp_path))
        else:
            result.append(temp_path)
    return result


def ispic(path):
    if path.endswith('png') or path.endswith('jpg') or path.endswith('PNG') or path.endswith('JPG') \
        or path.endswith('jpeg') or path.endswith('JPEG') or path.endswith('gif') or path.endswith('GIF'):
        return True


def shrink(path, savepath = './static/img'):
    if ispic(path):
        try:
            if not os.path.exists(savepath):
                os.mkdir(savepath)
            if os.path.exists('./smallpiclibinfo'):
                with open('./smallpiclibinfo', 'r') as f:
                    count = int(f.readline())
            else:
                count = 0
            im = Image.open(path)
        except IOError:
            print('IOError when making thumb!')
            return ''
        if im.mode not in ('L', 'RGB'):
            im = im.convert('RGB')
        width, height = im.size
        # 裁剪图片成正方形
        if width > height/5*7:
            delta = (width - height/5*7) / 2
            box = (delta, 0, width - delta, height)
            im = im.crop(box)
        elif height/5*7 > width:
            delta = (height - width/7*5) / 2
            box = (0, delta, width, height - delta)
            im = im.crop(box)
        smallpath = os.path.join(savepath, str(count)+os.path.splitext(path)[1])
        im = im.resize((350, 250))
        im.save(smallpath)
        with open('./smallpiclibinfo', 'w') as f:
            f.write(str(count+1))
        return smallpath


def main():
    shrink(os.environ['HOME'] + '/Downloads/desktop.jpg', os.environ['HOME'] + '/smallpics')

if __name__ == '__main__':
    main()