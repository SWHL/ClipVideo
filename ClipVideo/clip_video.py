# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File: clip_video.py
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
import sys
from pathlib import Path

from moviepy import editor
from tqdm import tqdm


def mkdir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


class ClipVideo(object):
    def __call__(self,
                 clip_info_str=None,
                 clip_info_path=None,
                 save_dir=None):
        if clip_info_str is not None:
            split_part = clip_info_str.split(',')
            video_path, clip_info_list = split_part[0], [split_part[1:]]
        elif clip_info_path is not None:
            print('Reading the clip info')
            video_path, clip_info_list = self.read_clip_info(clip_info_path)
        else:
            raise ValueError('Both clip_info_str and clip_info_path can not be all None.')

        if save_dir is None:
            save_dir = Path('video_clip') / Path(video_path).stem
            mkdir(save_dir)

        print(video_path)
        with editor.VideoFileClip(video_path) as cliper:
            for one_clip_info in tqdm(clip_info_list):
                clip_video_name, clip_start, clip_end = one_clip_info

                save_clip_path = str(save_dir / clip_video_name)
                self.save_clip_video(cliper, save_clip_path,
                                     clip_start, clip_end)
        print(f'The cropped video has been saved under {save_dir}')

    @staticmethod
    def read_clip_info(txt_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            clip_info = list(map(lambda x: x.rstrip(), f))

        video_path = clip_info[0]
        clip_info_list = list(map(lambda x: x.split(','), clip_info[1:]))
        return video_path, clip_info_list

    @staticmethod
    def save_clip_video(cliper, clip_video_name, clip_start, clip_end):
        save_suffix = clip_video_name.split('.')[-1]

        clip_video = cliper.subclip(clip_start, clip_end)

        with editor.CompositeVideoClip([clip_video]) as final_video:
            if save_suffix == 'mp4':
                final_video.write_videofile(clip_video_name)
            elif save_suffix == 'gif':
                final_video.write_gif(clip_video_name, fps=8)
            else:
                raise ValueError(f'not support {save_suffix}!')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-str', '--clip_info_str', type=str,
                        default=None,
                        help='Clip information given in string format, which only clip one part at one time.')
    parser.add_argument('-txt', '--clip_info_path', type=str,
                        default='clip_info.txt',
                        help='Clip information given in txt format, which can clip multiple parts at the same time.')
    parser.add_argument('--save_dir', type=str, default=None)
    args = parser.parse_args()

    clip_videoer = ClipVideo()

    if args.clip_info_path is not None:
        if Path(args.clip_info_path).is_file():
            clip_videoer(clip_info_path=args.clip_info_path)
        else:
            print(f'{args.clip_info_path} is not a file!')
            sys.exit(2)
    elif args.clip_info_str is not None:
        clip_videoer(clip_info_str=args.clip_info_str,
                     save_dir=args.save_dir)
    else:
        raise ValueError('Both clip_info_str and clip_info_path can not be all None.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-str', '--clip_info_str', type=str,
                        default=None,
                        help='Clip information given in string format, which only clip one part at one time.')
    parser.add_argument('-txt', '--clip_info_path', type=str,
                        default='clip_info.txt',
                        help='Clip information given in txt format, which can clip multiple parts at the same time.')
    parser.add_argument('--save_dir', type=str, default=None)
    args = parser.parse_args()

    clip_videoer = ClipVideo()

    if args.clip_info_path is not None:
        if Path(args.clip_info_path).is_file():
            clip_videoer(clip_info_path=args.clip_info_path)
        else:
            print(f'{args.clip_info_path} is not a file!')
            sys.exit(2)
    elif args.clip_info_str is not None:
        clip_videoer(clip_info_str=args.clip_info_str,
                     save_dir=args.save_dir)
    else:
        raise ValueError('Both clip_info_str and clip_info_path can not be all None')