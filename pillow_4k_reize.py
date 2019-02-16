import os
import glob
import tempfile
import zipfile
import PIL
from PIL import Image


def resize_4k(fp, dir_name):
    im = Image.open(fp, mode='r')

    x, y = im.size
    rey = 2160
    rex = int(x * rey / y)

    out = im.resize((rex, rey), PIL.Image.LANCZOS)

    _, fn = os.path.split(fp)
    name, ext = os.path.splitext(fn)
    out.save(os.path.join(dir_name, name + '_4k' + ext), 'PNG')
    print(f'reszie : {name+ext}')


def dir_fn_ext(file_path):
    dir_name, file_full_name = os.path.split(file_path)
    file_name, file_ext = os.path.splitext(file_full_name)
    return (dir_name, file_name, file_ext)


def remakeZip(zf, func):

    dir_name, file_name, file_ext = dir_fn_ext(zf)

    with tempfile.TemporaryDirectory(dir=dir_name) as tmpdir1:

        with zipfile.ZipFile(zf) as z:
            print(f'압축해제 : {zf}')
            z.extractall(tmpdir1)

        with tempfile.TemporaryDirectory(dir=dir_name) as tmpdir2:
            for f1 in glob.glob(os.path.join(tmpdir1, '*.png')):
                func(f1, tmpdir2)

            rezip_fn = os.path.join(dir_name, file_name + '_4k' + file_ext)
            with zipfile.ZipFile(rezip_fn, 'w') as z:

                for f2 in glob.glob(os.path.join(tmpdir2, '*.png')):
                    _, file_name, file_ext = dir_fn_ext(f2)
                    print(f'파일압축 : {file_name+file_ext}')
                    z.write(f2, file_name+file_ext)


if __name__ == '__main__':

    for f in glob.glob(r'c:\work.scan\*.zip'):
        remakeZip(f, resize_4k)
