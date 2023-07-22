import json
import conf as dconf
import sqlite3
import os
import torch
import aml.time_mesuarment as tm
from pprint import pprint as Print
import numpy as np
from sklearn.preprocessing import LabelEncoder


def make_sql_tables_from_COCO_annotation():
    sqlite_connection = sqlite3.connect(dconf.sqlannotationsdb)
    cursor = sqlite_connection.cursor()

    # images indexofentry file_name
    # images indexofentry id
    # images indexofentry width
    # images indexofentry height
    schema_images = '''
        create table if not exists images(
            IdxOfEntry int primary key,
            filename text,
            id int,
            width int,
            height int
        );
    '''

    # INSERT INTO table1 (column1,column2 ,..)
    # VALUES 
    #    (value1,value2 ,...),
    #    (value1,value2 ,...),
    #     ...
    #    (value1,value2 ,...);

    insert_into_images = '''
        insert into images (IdxOfEntry,filename,id,width,height)
        values 
        (?,?,?,?,?);
    '''

    # categories indexofentry supercategory
    # categories indexofentry id
    # categories indexofentry name
    schema_categories = '''
        create table if not exists categories(
            IdxOfEntry int primary key,
            supercategory text,
            id int,
            name text
        );
    '''
    insert_into_categories = '''
        insert into categories (IdxOfEntry,supercategory,id,name)
        values 
        (?,?,?,?);
    '''
    # annotations indexofentry bbox postuple
    # annotations indexofentry segmentation image_id
    # annotations indexofentry segmentation iscrowd
    # annotations indexofentry segmentation area    
    # annotations indexofentry category_id
    # annotations indexofentry id
    schema_annotations = '''
        create table if not exists annotations(
            IdxOfEntry int primary key,
            x real,
            y real,
            w real,
            h real,
            id int,
            category_id int,
            image_id int
        );
    ''' 
    insert_into_annotations = '''
        insert into annotations (IdxOfEntry,x,y,w,h,id,category_id,image_id)
        values 
        (?,?,?,?,?,?,?,?);
    '''



    cursor.execute(schema_images)
    cursor.execute(schema_categories)
    cursor.execute(schema_annotations)


    with open(dconf.all_lables_location,'r') as annnotations:
        json_annotations = json.load(annnotations)
        # images indexofentry file_name
        # images indexofentry id
        # images indexofentry width
        # images indexofentry height
        data1 = []
        i_ = 0
        # (IdxOfEntry,filename,id,width,height)
        for ImageEntry in json_annotations['images']:

            data1.append(
                [
                    i_,
                    ImageEntry['file_name'],
                    ImageEntry['id'],
                    ImageEntry['width'],
                    ImageEntry['height']
                ]
            )
            i_ += 1
        cursor.executemany(insert_into_images, data1)
        sqlite_connection.commit()
        # categories indexofentry supercategory
        # categories indexofentry id
        # categories indexofentry name
        data2 = []
        i_ = 0
        # (IdxOfEntry,supercategory,id,name)
        for CategoryEntry in json_annotations['categories']:
            data2.append(
                [
                    i_,
                    CategoryEntry['supercategory'],
                    CategoryEntry['id'],
                    CategoryEntry['name']
                ]
            )
            i_ +=1
        cursor.executemany(insert_into_categories,data2)
        sqlite_connection.commit() 
        # annotations indexofentry bbox postuple
        # annotations indexofentry segmentation image_id
        # annotations indexofentry segmentation iscrowd
        # annotations indexofentry segmentation area    
        # annotations indexofentry category_id
        # annotations indexofentry id
        data3 = []
        i_ = 0
        # (IdxOfEntry,x,y,w,h,id,category_id)
        for AnnotationEntry in json_annotations['annotations']:
            data3.append(
                [
                    i_,
                    AnnotationEntry['bbox'][0],
                    AnnotationEntry['bbox'][1],
                    AnnotationEntry['bbox'][2],
                    AnnotationEntry['bbox'][3],
                    AnnotationEntry['id'],
                    AnnotationEntry['category_id'],
                    AnnotationEntry['image_id']
                ]
            )
            i_ += 1 
        cursor.executemany(insert_into_annotations,data3)
        sqlite_connection.commit()

    cursor.close()
    sqlite_connection.close()

@tm.timeit
def get_detection_annotations():
    q0 = '''
        select images.filename, annotations.category_id,
        annotations.x,annotations.y,annotations.w,annotations.h 
        from images 
        join annotations 
        on images.id = annotations.image_id;
    '''

    connection = sqlite3.connect(dconf.sqlannotationsdb)
    cursor = connection.cursor()
    cursor.execute(q0)
    response = cursor.fetchall()

    # q1 = '''
    #     select count(images.filename) from images
    #     join annotations
    #     on images.id = annotations.image_id and annotations.category_id <=3
    #     ;
    # '''
    filepaths = np.unique([el[0] for el in response])
    lables = np.unique([el[1] for el in response])
    #   DetectionDataNav[ImageFullPath]
    #       bboxes list
    #       lalels list
    BoxLabelByImgPath = {os.path.join(dconf.all_images_folder,fp):{'boxes':[],'labels':[]} for fp in filepaths}
    le = LabelEncoder()
    le.fit(lables)


    for r in response:
        fp = os.path.join(dconf.all_images_folder,r[0])
        label = r[1]
        bbox = r[2:6]
        x_ = bbox[0]
        y_ = bbox[1]
        w_ = bbox[2]
        h_ = bbox[3]
        if((y_ + h_-1 >= 520) or (x_+w_-1 >= 1101) or (w_<=0)or(h_<=0)):
            print('error: W={} H={}  xywh box={}'.format(1101,520,bbox))
            continue

        
        BoxLabelByImgPath[fp]['boxes'].append(bbox)
        BoxLabelByImgPath[fp]['labels'].append(le.transform([label])[0])
    Print({
        'size of dataset': len(BoxLabelByImgPath),
        'number of classes without background': len(lables),
    })
    torch.save(BoxLabelByImgPath, dconf.BoxesLabelsByPath_filename)
    torch.save(le, dconf.imgs_labels_encoder_filename)

    cursor.close()
    connection.close()

def get_class_distrib():
    q0 = '''
        select annotations.category_id as cid, categories.name as cname, count(categories.name) as namecount
        from annotations join categories on
        cid = categories.id
        group by cname
        order by namecount;
    '''
    connection = sqlite3.connect(dconf.sqlannotationsdb)
    cursor = connection.cursor()
    cursor.execute(q0)
    response = cursor.fetchall()
    o_counts = []
    o_labels= []
    for r in response:
        o_counts.append(r[2])
        o_labels.append(r[1])
    cursor.close()
    connection.close()
    return o_labels,o_counts

if __name__ == '__main__':
    make_sql_tables_from_COCO_annotation()
    get_detection_annotations()