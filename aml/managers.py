import pprint
import random

import PIL.Image
import numpy as np
import torch
import os
import aml.img_processing as img_processing
from PIL import Image
import pandas as pd

import typing
from typing import Any
from typing import Callable

class ModelsManager:

    def __load_model_from_int(self, repo, model_name, weights):
        # model = torch.hub.load("pytorch/vision", "resnet18", pretrained=True)
        # 
        model = torch.hub.load(repo, model_name, weights=weights)
        return model

    def load_model(self, description_of_the_model, reload_from_internet=False):
        # {
        #     'pytorch_model_name': 'resnet50',
        #     'start_weights': 'ResNet50_Weights.IMAGENET1K_V1',
        #     'repo': 'pytorch/vision',
        #     'local_path': os.path.join(models_for_img_base_path, 'resnet50'),
        #     'filename': 'model.txt'
        # }
        repo = description_of_the_model['repo']
        weights = description_of_the_model['start_weights']
        local_path = description_of_the_model['local_path']
        model_name = description_of_the_model['pytorch_model_name']
        filename = description_of_the_model['filename']
        full_path = os.path.join(local_path, filename)

        if not os.path.exists(local_path):
            os.makedirs(local_path)

        if reload_from_internet == True:
            model = self.__load_model_from_int(repo, model_name, weights)
            torch.save(model, full_path)
            return model

        if reload_from_internet == False:
            if os.path.isfile(full_path):
                model = torch.load(full_path)
                return model
            else:
                model = self.__load_model_from_int(repo, model_name, weights)
                torch.save(model, full_path)
                return model


def get_image_ifstream(filename: str):
    return PIL.Image.open(filename)


class ImgsDatasetManager:
    base_path = ''
    attrs_batches_path = None
    number_of_batches = 0

    def init_a_data_source(self, base_path_):
        self.base_path = base_path_
        if os.path.exists(base_path_):
            database_info = torch.load(os.path.join(base_path_, 'database_info.txt'))
            num_of_batches = database_info['num_of_batches']
            attrs = database_info['attrs']
            self.attrs_batches_path = {attr: [] for attr in attrs}
            for attr_name in self.attrs_batches_path:
                for i in range(num_of_batches):
                    # attrname_batch_indexofbatch.txt
                    path_to_batch_of_attr = os.path.join(base_path_, '{}_batch_{}.txt'.format(attr_name, i))
                    self.attrs_batches_path[attr_name].append(path_to_batch_of_attr)
            self.number_of_batches = num_of_batches

    def get_number_of_batches(self):
        return self.number_of_batches

    def load_batch_by_attr_name(self, attr_name, batch_index):
        attr_name_batch = torch.load(self.attrs_batches_path[attr_name][batch_index])
        return attr_name_batch

    def load_all_by_attr_name(self, attr_name):
        attr_name_all_data = []
        for batch_index in range(self.number_of_batches):
            attr_name_all_data += torch.load(self.attrs_batches_path[attr_name][batch_index])
        return attr_name_all_data

    # def load_attr_by_primary_key(self, attr_name:str, primary_keys:list):
    #     all_paths_to_attr = self.attrs_batches_path[attr_name]
    #     all_paths_to_primary_keys = self.attrs_batches_path[self.pr_key_name]

    @staticmethod
    def make_intermediate_train_dataset_for_images(intermediate_XY, path_of_source, path_to_save,
                                                   batch_size=100):
        '''
        запись на диск в формате:
        uid_batch_indexofbatch.txt
        X_batch_indexofbatch.txt
        Y_batch_indexofbatch.txt
        '''
        if len(intermediate_XY) == 0:
            return

        random.shuffle(intermediate_XY)
        image_handler = img_processing.ImageHandler()

        N = len(intermediate_XY)
        num_of_batches = N // batch_size
        last_batch_size = N % batch_size

        for i in range(num_of_batches):
            uid_batch = []
            X_batch = []
            Y_batch = []
            for j in range(batch_size):
                uid = intermediate_XY[i * batch_size + j]['x_UID']
                label = intermediate_XY[i * batch_size + j]['y_numeric']
                filename = os.path.join(path_of_source, str(uid) + '.jpg')
                img = Image.open(filename)
                preprocessed_img_as_tensor = image_handler.prepare_row_PIL_image_to_work_with_resnet(img)
                uid_batch.append(uid)
                X_batch.append(preprocessed_img_as_tensor)
                Y_batch.append(label)
            torch.save(uid_batch, os.path.join(path_to_save, 'uid_batch_' + str(i) + '.txt'))
            torch.save(X_batch, os.path.join(path_to_save, 'X_batch_' + str(i) + '.txt'))
            torch.save(Y_batch, os.path.join(path_to_save, 'Y_batch_' + str(i) + '.txt'))
        if last_batch_size > 0:
            last_batch_uid = []
            last_batch_X = []
            last_batch_Y = []
            for j in range(last_batch_size):
                uid = intermediate_XY[num_of_batches * batch_size + j]['x_UID']
                label = intermediate_XY[num_of_batches * batch_size + j]['y_numeric']
                filename = os.path.join(path_of_source, str(uid) + '.jpg')
                img = Image.open(filename)
                preprocessed_img_as_tensor = image_handler.prepare_row_PIL_image_to_work_with_resnet(img)
                last_batch_uid.append(uid)
                last_batch_X.append(preprocessed_img_as_tensor)
                last_batch_Y.append(label)
            torch.save(last_batch_uid, os.path.join(path_to_save, 'uid_batch_' + str(num_of_batches) + '.txt'))
            torch.save(last_batch_X, os.path.join(path_to_save, 'X_batch_' + str(num_of_batches) + '.txt'))
            torch.save(last_batch_Y, os.path.join(path_to_save, 'Y_batch_' + str(num_of_batches) + '.txt'))

        is_last_batch_exists = True if last_batch_size > 0 else False
        num_of_batches_in_dataset = num_of_batches
        if is_last_batch_exists:
            num_of_batches_in_dataset += 1
        database_info = {
            'num_of_batches': num_of_batches_in_dataset,
            'attrs': ['uid', 'X', 'Y']
        }
        torch.save(database_info, os.path.join(path_to_save, 'database_info.txt'))

    @staticmethod
    def select_as_from_pd(select_args: list, as_args: list, from_arg: str)->dict[str, Any]:
        if len(select_args) != len(as_args):
            return
        if not os.path.isfile(from_arg):
            return
        file_extension = os.path.splitext(from_arg)[-1]
        if file_extension == '.parquet':
            table = pd.read_parquet(from_arg, engine='pyarrow')
            values = [table[attr].tolist() for attr in select_args]
            keys = [key for key in as_args]
            response = {key: value for key, value in zip(keys, values)}
            return response

    @staticmethod
    def select_images_from_dir_by_id(directory: str, img_format: str,
                                     ids: list[int]) -> list[str]:
        if not os.path.isdir(directory):
            return
        if img_format == 'jpg':
            return [os.path.join(directory, str(id) + '.' + img_format) for id in ids]


    @staticmethod
    def load_img_by_path(filename: str, stream_to_img_transformer):
        ifstream = get_image_ifstream(filename)
        return stream_to_img_transformer.transform(ifstream)

    @staticmethod
    def group_by(select_args: list[str], as_args, from_arg: dict[str, Any],
                 group_by_arg: str) -> dict[str, Any]:
        if len(select_args)>2:
            return
        if len(as_args)>2:
            return
        if len(select_args) != len(as_args):
            return
        map_keys = {select_args[i]: as_args[i] for i in range(len(select_args))}
        columns = {key: value for key, value in from_arg.items() if key in select_args}
        unique_attr_values = np.unique(columns[group_by_arg])
        other_attr = np.setdiff1d(select_args, group_by_arg)[0]
        values_to_process = columns[other_attr]
        response = {map_keys[key]: [] for key, value in columns.items()}
        for ref_attr in unique_attr_values:
            # get all positions of ref_attr
            positions = np.where(columns[group_by_arg] == ref_attr)[0]
            response[map_keys[group_by_arg]].append(ref_attr)
            response[map_keys[other_attr]].append([values_to_process[i] for i in positions])

        return response

    @staticmethod
    def update_from_using_mapping(update_arg: dict[str, list[list[Any]]],
                                  set_arg: str,
                                  mapping: Callable[[list[Any]], list[Any]]):
        attr_name = set_arg
        for list_index in range(len(update_arg[attr_name])):
            update_arg[attr_name][list_index] = mapping(update_arg[attr_name][list_index])