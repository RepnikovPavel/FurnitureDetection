

# Metrics 

jacard index  

$$
    JI = \frac{|A B|}{|A + B|}
$$

jacard coefficient

$$
 JC = \frac{|AB|}{|A|+|B|-|AB|}
$$

**detection metrics**  

mAP (mean Average Precision)

$$
    mAP = \frac{1}{n} \sum_{i=1}^{n}{AP_{i}}
$$  

where $AP_{i}$ is the average precision for class $c_{i}$ and $n$ is the number of classes  

AP (Average Precision)  

$$
    AP = \sum_{i=1}^{n}{(R_{i}-R_{i-1})P_{i}} = \int_{0}^{1}{precision(recall)d(recall)}
$$


mAR (mean Average Recall)


# general scheme  

<!--  -->
<!-- graph TD -->
<!-- graph LR -->
<!--  -->
```mermaid
graph LR
title[<u>CollectingADataset</u>]
3DScene --- Blender
Blender --- ManualLabeling
3DScene --- UnrealEngine
UnrealEngine --- ManualLabeling
UnrealEngine --- AutomaticLabeling
RealImages --- ManualLabeling
AnyImage --- LabelingByML
```  

___

```mermaid
graph LR
title[<u>Segmentation</u>]
Dataset --- RowImages
Dataset --- TrueSegmentationMasks
TrainPipeline --- TrainSegmentationModel
RowImages --- TrainSegmentationModel
TrueSegmentationMasks --- TrainSegmentationModel
```
___

```mermaid
graph LR
title[<u>Detection</u>]
Dataset --- RowImages
Dataset --- TrueBoundingBoxes,LabesOfClasses
RowImages --- TrainDetectionModel
TrainPipeline --- TrainDetectionModel
TrueBoundingBoxes,LabesOfClasses --- TrainDetectionModel
```

___

# The way to solve the test problem

```mermaid
graph TD

COCO2017 --> MakeCOCOFormatPipiline
MakeCOCOFormatPipiline --> COCOFormatPipeline 
COCOFormatPipeline --> TestAFewModels
TrainPipeline --> TestAFewModels -->Model
TrainPipeline --> TargetModel
TargetDataset --> TargetModel
RealImages --> AssessmentOfTheAbilityToGeneralize
TargetModel --> AssessmentOfTheAbilityToGeneralize
```

# list of tutorials
1. [the best introductory lecture](https://www.youtube.com/watch?v=r2KA99ThEH4&list=PL5FkQ0AF9O_o2Eb5Qn8pwCDg7TniyV1Wb&index=7)
2. [object detection tutorial on github](https://github.com/sgrvinod/a-PyTorch-Tutorial-to-Object-Detection/blob/master/README.md)
3. [COCO dataset overview](https://www.youtube.com/watch?v=h6s61a_pqfM)  
4. [MIPT Computer Vision](https://www.youtube.com/watch?v=-lIVq52AAPc&list=PL4_hYwCyhAvZeq93ssEUaR47xhvs7IhJM&index=12)  
5. [ssd300 article](https://arxiv.org/pdf/1512.02325.pdf)

# list of articles  
1. [scalable object detection using deep neural networks (2013)](https://arxiv.org/pdf/1312.2249.pdf)
