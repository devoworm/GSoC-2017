# GSoC-2017

Repository for Google Summer of Code 2017 project

Student: [Siddharth Yadav][0]   
Mentor: [Bradly Alicea][1]

Organisation: [DevoWorm][4], [OpenWorm][5], [INCF][3] 

### About this project:
The aim of this project is to find out a method to segment all the cells that are present in an embryo of c.elegans. We will use the result of this segmentation to collect data about static location after division and vectors that describe shape changes and overall positional changes in the embryo. We have used SPIM microscopy images as out data for this research.

A list of broad techniques we tried:
- Morphological 
- Edge based methods
- Chan Vese
- Motion based detection of cell boundaries
- Gabor Filters
- Several methods for noise removal
- Level Sets algorithms


### About this repo:
This repo basically reflects the research phase of this project. It is not collectively exhaustive and it gives details of a few approaches that were tried during this phase.

A major portion of the code is in src/notebooks and src/python. Validation is still under development. There are some nice examples of Active Contours and Level Sets methods(and methods that are similar to them) being used for our purpose. Thresholding and Morphological approaches also gave some nice results.

Data used during the research process is in src/data. 
You can find some annotated data(labeled data) in form of raw binary images(src/data/Data Annotation) and .arff weka data files(in src/data/Labeled Data/Weka_TWS_Data).
There are also a few Weka classifiers in form of .model files. (in src/data/classifiers)





[0]: https://www.linkedin.com/in/1siddharthyadav/
[1]: https://www.linkedin.com/in/bradlyalicea
[3]: http://incf.org/
[4]: http://devoworm.weebly.com/
[5]: http://www.openworm.org/
