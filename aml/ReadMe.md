

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
    mAP = \frac{1}{n} \sum_{}^{}{AP_{i}}
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
graph TD
title[<u>CollectingADataset</u>]
3DScene --- Blender
Blender --- ManualLabeling
3DScene --- UnrealEngine
UnrealEngine --- ManualLabeling
UnrealEngine --- AutomaticLabeling
AutomaticLabeling --- Dataset
ManualLabeling ---Dataset
RealImages --- ManualLabeling
ManualLabeling --- Dataset
```  
___

```mermaid
graph TD
title[<u>Segmentation</u>]
Dataset --- RowImages
Dataset --- TrueSegmentationMasks
RowImages --- TrainSegmentationModel
TrueSegmentationMasks --- TrainSegmentationModel
```
___

```mermaid
graph TD
title[<u>Detection</u>]
Dataset --- RowImages
Dataset --- TrueBoundingBoxes,LabesOfClasses,DifficultiesOfDetection
RowImages --- TrainDetectionModel
 TrueBoundingBoxes,LabesOfClasses,DifficultiesOfDetection --- TrainDetectionModel
```


# list of tutorials
1. [the best introductory lecture](https://www.youtube.com/watch?v=r2KA99ThEH4&list=PL5FkQ0AF9O_o2Eb5Qn8pwCDg7TniyV1Wb&index=7)
2. [object detection tutorial on github](https://github.com/sgrvinod/a-PyTorch-Tutorial-to-Object-Detection/blob/master/README.md)
  



# list of articles  
1. [scalable object detection using deep neural networks (2013)](https://arxiv.org/pdf/1312.2249.pdf)


<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
</script>

<style>
    .customtable {
        width:100%;
    }
    table {
    width: 100%;
    }
</style>
