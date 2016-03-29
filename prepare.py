#!/usr/bin/python2
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import os
import shutil
import imghdr
from PIL import Image


def clean_subdir(save_path, cur_path):
    _, subdirs, files = next(os.walk(cur_path))
    if len(subdirs) > 0:
        subdir_path = os.path.join(cur_path, subdirs[0])
        clean_subdir(save_path, subdir_path)
    elif len(files) > 0:
        clean_file(save_path, os.path.join(cur_path, files[0]))
    shutil.rmtree(cur_path)
    return None


def clean_file(save_path, cur_path):
    print(cur_path, save_path)
    ext = imghdr.what(cur_path)
    if ext is None:
        os.remove(cur_path)
        return None
    save_name = save_path + '.' + ext
    shutil.move(cur_path, save_name)
    return None


def get_clean_name(name):
    return name[:name.index('.')]


def walk_and_clean(root_dir='./'):
    names = next(os.walk(root_dir))[1]
    print(names)
    for name in names:
        cur_path = os.path.join(root_dir, name)
        _, subdirs, files = next(os.walk(cur_path))
        clean_subdirs = map(get_clean_name, subdirs)
        map(lambda s: os.rename(os.path.join(cur_path, s[1]), os.path.join(cur_path, s[0])), zip(clean_subdirs, subdirs))
        map(lambda s: clean_subdir(os.path.join(cur_path, s), os.path.join(cur_path, s)), clean_subdirs)
        clean_files = map(get_clean_name, files)
        map(lambda f: clean_file(os.path.join(cur_path, f[0]), os.path.join(cur_path, f[1])), zip(clean_files, files))


def map_names(filenames):
    idx_map = dict()
    for name in filenames:
        idx_map[int(get_clean_name(name))] = name
    return idx_map


def crop_from_file(filename, images_dir='./', save_dir='./cropped'):
    person = filename[filename.rfind('/')+1:filename.rfind('.')]
    print(person)
    if not os.path.exists(os.path.join(save_dir, person)):
        os.makedirs(os.path.join(save_dir, person))
    img_map = map_names(next(os.walk(os.path.join(images_dir, person)))[2])
    with open(filename, 'r') as f:
        for line in f:
            arguments = map(str.strip, line.split(' '))
            if len(arguments) != 10:
                continue
            img_idx = int(arguments[0])
            bbox = tuple(map(int, map(float, arguments[3:7])))
            if img_idx not in img_map:
                continue
            img_name = img_map[img_idx]
            Image.open(os.path.join(images_dir, person, img_name)).crop(bbox).save(os.path.join(save_dir, person, img_name))
    return None


def walk_and_crop(instr_dir='./', images_dir='./images', save_dir='./cropped'):
    map(lambda f: crop_from_file(os.path.join(instr_dir, f), images_dir, save_dir), next(os.walk(instr_dir))[2])
    return None


if __name__ == '__main__':
    walk_and_clean('./out')
    os.makedirs('./cropped')
    walk_and_crop('./files', './out', './cropped')
