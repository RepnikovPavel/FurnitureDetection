import os
import shutil

import numpy as np
import torch
import itertools
import matplotlib.pyplot as plt
import torchvision


def create_dir_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


def delete_abs_path_and_data(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def load_all_intermediate_data(base_path):
    intermediate_list = []
    for filename in os.listdir(base_path):
        abs_filepath = os.path.join(base_path, filename)
        intermediate_list.append(torch.load(abs_filepath))
    return intermediate_list


def load_part_of_intermediate_data(base_path, number_of_elements_to_load):
    intermediate_dict = []
    file_index = 1
    for filename in os.listdir(base_path):
        if file_index > number_of_elements_to_load:
            break
        abs_filepath = os.path.join(base_path, filename)
        intermediate_dict.append(torch.load(abs_filepath))
        file_index += 1
    return intermediate_dict


def get_number_of_keys_in_dict(dict):
    return len(dict)


def get_source_label_from_mapped_label(mappped_label, mapping_to_source_dict):
    return mapping_to_source_dict[mappped_label]


def map_list_of_labels(list_of_labels, dict_for_map):
    new_list = np.ndarray(shape=(len(list_of_labels),), dtype=np.int64)
    for i in range(len(list_of_labels)):
        new_list[i] = dict_for_map[list_of_labels[i]]
    return new_list


def remove_file_if_exists(abs_path):
    if os.path.exists(abs_path):
        os.remove(abs_path)


def intersect_dicts_by_values(d_1, d_2):
    '''
    :param d_1:
    :param d_2:
    :return: возвращает [дублирующееся значение str] если два словаря имеют непустое пересечение по значениям
    '''
    vs_1 = list(itertools.chain.from_iterable(d_1.values()))
    vs_2 = list(itertools.chain.from_iterable(d_2.values()))
    return np.intersect1d(vs_1, vs_2)


def intersect_lists_by_values(l1, l2):
    return np.intersect1d(l1, l2)


def delete_values_in_dict(dict, list_of_values_to_delete):
    output = {}
    for key in dict:
        vs = dict[key]
        output.update({key: np.setdiff1d(vs, list_of_values_to_delete).tolist()})
    return output


def delete_values_in_list(list, list_of_values_to_delete):
    return np.setdiff1d(list, list_of_values_to_delete)


def delete_duplicates_in_dicts_with_priority(list_of_dicts_inverse_sorted_by_priority_to_delete):
    '''

    :param list_of_dicts_inverse_sorted_by_priority_to_delete: приоритет к удалению от наибольшего к наименьшему
    :return: словари в списке остаются в том же порядке после удаления дублированных элементов
    '''
    output_list_of_dicts = []
    for i in range(len(list_of_dicts_inverse_sorted_by_priority_to_delete) - 1):
        d1 = list_of_dicts_inverse_sorted_by_priority_to_delete[i]
        for j in range(i + 1, len(list_of_dicts_inverse_sorted_by_priority_to_delete)):
            d2 = list_of_dicts_inverse_sorted_by_priority_to_delete[j]
            duplicated_values = intersect_dicts_by_values(d1, d2)
            d1 = delete_values_in_dict(d1, duplicated_values)
            d1_tmp = {}
            for keyofd1 in d1:
                if not (len(d1[keyofd1]) == 0 and (keyofd1 in d2.keys())):
                    d1_tmp.update({keyofd1: d1[keyofd1]})
            d1 = d1_tmp

        output_list_of_dicts.append(d1)

    output_list_of_dicts.append(list_of_dicts_inverse_sorted_by_priority_to_delete[-1])
    return output_list_of_dicts


def show_imgs(imgs):
    if not isinstance(imgs, list):
        imgs = [imgs]
    fig, axs = plt.subplots(ncols=len(imgs), squeeze=False)
    for i, img in enumerate(imgs):
        img = img.detach()
        img = torchvision.transforms.functional.to_pil_image(img)
        axs[0, i].imshow(np.asarray(img))
        axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])
    plt.show(block=True)

def list_of_tensors_to_list_of_np_arrays(list_of_tensors):
    for i in range(len(list_of_tensors)):
        list_of_tensors[i] = list_of_tensors[i].to(device='cpu').detach().numpy()


def delete_all_data_from_directory(directory: str):
    if not os.path.exists(directory):
        return
    if not os.path.isdir(directory):
        return
    for filename in os.listdir(directory):
        os.remove(os.path.join(directory, filename))


def create_if_not_exists_and_clear_if_exists(directory: str):
    if os.path.exists(directory):
        if not os.path.isdir(directory):
            return
    if not os.path.exists(directory):
        os.makedirs(directory)
        return
    if os.path.exists(directory):
        delete_all_data_from_directory(directory)

