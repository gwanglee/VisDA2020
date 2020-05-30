# encoding: utf-8
"""
@author:  weijian
@contact: dengwj16@gmail.com
"""

from __future__ import print_function
import sys
sys.path.append("..")
import glob
import re
import os.path as osp

from .bases import BaseImageDataset


class submit_validation(BaseImageDataset):
    """
    personX (source domain): only consains training samples
    Dataset statistics:
    # query_identities: 100
    # query_images: 377
    # gallery_images: 2944
    # cams: 5
    """

    dataset_dir = 'target_validation'

    def __init__(self, root='./challenge_datasets', verbose=True):
        super(submit_validation, self).__init__()
        self.dataset_dir = osp.join(root, self.dataset_dir)

        self.query_dir = osp.join(self.dataset_dir, 'image_query/')
        self.gallery_dir = osp.join(self.dataset_dir, 'image_gallery/')
        self._check_before_run()

        self.path_index_val_gallery = '../submit_val/index_validation_gallery.txt'
        self.path_index_val_query   = '../submit_val/index_validation_query.txt'

        self.query = self._process_dir(self.query_dir, self.path_index_val_query, relabel=False)
        self.gallery = self._process_dir(self.gallery_dir, self.path_index_val_gallery, relabel=False)

        if verbose:
            print("=> target_validation loaded")
            self.print_dataset_statistics_validation(self.query, self.gallery)

    def _check_before_run(self):
        """Check if all files are available before going deeper"""
        if not osp.exists(self.dataset_dir):
            raise RuntimeError("'{}' is not available".format(self.dataset_dir))
        if not osp.exists(self.query_dir):
            raise RuntimeError("'{}' is not available".format(self.query_dir))
        if not osp.exists(self.gallery_dir):
            raise RuntimeError("'{}' is not available".format(self.gallery_dir))

    def _process_dir(self, dir_path, idx_path, relabel=False):
        pid_container = set()
        dataset = []

        with open(idx_path, 'r') as rf:
            lines = rf.readlines()
            for l in lines:
                img_path, camid, pid, idx = l.split(' ')
                pid = int(pid)
                camid = int(camid)

                pid_container.add(pid)

                assert 0 <= pid <= 100
                assert 1 <= camid <= 6
                camid -= 1
                dataset.append((osp.join(dir_path, img_path), pid, camid))

        return dataset