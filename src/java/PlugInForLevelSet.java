import ij.IJ;
import ij.ImagePlus;
import ij.ImageStack;
import ij.gui.Roi;
import ij.measure.Measurements;
import ij.measure.ResultsTable;
import ij.plugin.Duplicator;
import ij.plugin.ImageCalculator;
import ij.plugin.filter.ParticleAnalyzer;
import ij.plugin.filter.PlugInFilter;
import ij.plugin.frame.RoiManager;
import ij.process.ImageProcessor;
import levelsets.algorithm.ActiveContours;
import levelsets.algorithm.LevelSetImplementation;
import levelsets.ij.ImageContainer;
import levelsets.ij.ImageProgressContainer;
import levelsets.ij.StateContainer;
import trainableSegmentation.WekaSegmentation;

public class PlugInForLevelSet implements PlugInFilter {

    String classiferFileAddress = "F:\\FijiDev\\TryGlobal\\src\\fast.model";
    boolean isDataFine = false;

    //automate
    double lowerThreshold = 175.0;
    double upperThreshold = 255.0;

    @Override
    public int setup(String s, ImagePlus imagePlus) {

        // TODO: Check what kind of images can be given. Make it Robust
        return DOES_ALL;
    }

    @Override
    public void run(ImageProcessor imageProcessor) {

        //ImagePlus object of the original image. Weka Segmentation is performed on it.
        ImagePlus imagePlusOrignal = new ImagePlus("Original Input Image", imageProcessor);
        //copy is a duplicate of the original image. It is used in later part of the program to refine edges using LevelSet
        ImagePlus copy = new Duplicator().run(imagePlusOrignal);

        //this the outer boundary of the embryo. Used to neglect/remove regions we get outside the embryo
        ImagePlus cellMask = getWholeCellMask(imagePlusOrignal);

        //stores the classifies Image
        ImagePlus imagePlus = getClassifiedImage(imagePlusOrignal);
        IJ.log("Image Classified");

        imagePlus = smooth(imagePlus);
        imagePlus = threshold(imagePlus);
        imagePlus = refineMask(imagePlus, cellMask);
        imagePlus = morph(imagePlus);


        //Declare ROI Manager for Particle Analyzer
        RoiManager rm = new RoiManager();
        ParticleAnalyzer.setRoiManager(rm);

        //ParticleAnalyzer obtained
        ParticleAnalyzer pa = getParticleAnalyzer();
        pa.analyze(imagePlus);

        int numberOfRoi = rm.getCount();
        Roi finalRoi[] = new Roi[numberOfRoi];
        for (int i = 0; i < numberOfRoi; i++) {

            rm.select(i);
            Roi roi = rm.getRoi(i);
            copy.setRoi(roi);

            ImagePlus seg = getSegmentedImage(copy);
            IJ.run(seg, "Create Selection", "");
            finalRoi[i] = seg.getRoi();

        }

        // deletes the previous ROIs.
        rm.deselect();
        rm.close();

        // new ROI Manager for displaying the finalRoi. Implies contours after using LevelSets
        rm = new RoiManager();
        for (int j = 0; j < numberOfRoi; j++) {
            rm.addRoi(finalRoi[j]);
        }

    }//run ends

    private ImagePlus refineMask(ImagePlus imagePlus, ImagePlus restrictions) {
        IJ.run(restrictions, "Dilate", "");
        IJ.run(restrictions, "Dilate", "");
        IJ.run(restrictions, "Dilate", "");
        IJ.run(restrictions, "Dilate", "");
        ImageCalculator imageCalculator = new ImageCalculator();
        return imageCalculator.run("and create", imagePlus, restrictions);
    }

    /**
     * @param imagePlus the ImagePlus object of the very original input image.
     *                  For excellent performance ensure that region around the embryo has almost no whitish features.
     * @return A binary image where white represents the embryonic region
     */
    private ImagePlus getWholeCellMask(ImagePlus imagePlus) {

        //TODO: Automate the creation of initial contour in getWholeCellMask or put restrictions on data received.
        if(isDataFine) {
            Roi roi = new Roi(1, 1, imagePlus.getWidth()-3, imagePlus.getHeight()-3);
            return getSegImage(imagePlus, roi, 0.0030, 1.0, 1.0, 1, true, 50, 100);
        }
        else
        {
            /*
                CHANGE THIS if data is not up to the mark.
                Set ROI such that whitish features, which doesn't represents embryonic features, is not present in the ROI.
             */
            Roi roi = new Roi(10, 10, 360, 603);
            return getSegImage(imagePlus, roi, 0.0030, 1.0, 1.0, 1, true, 50, 100);
        }
    }

    private ImagePlus getClassifiedImage(ImagePlus imagePlus) {

        //Trainable Weka Segmentation
        WekaSegmentation wekaSegmentator = new WekaSegmentation(imagePlus);
        //Classifier Model file Loaded. TODO: Decide the path
        wekaSegmentator.loadClassifier(classiferFileAddress);
        //true means probability map will be given
        wekaSegmentator.applyClassifier(true);
        ImagePlus classifiedImage = wekaSegmentator.getClassifiedImage();
        classifiedImage.show();

        //TODO: Figure out a better way to do the below. This DIRTY CODE. Deal with Slices.
        //IJ.run(classifiedImage, "Next Slice [>]", "");
        IJ.run(classifiedImage, "Delete Slice", "");

        IJ.saveAsTiff(classifiedImage, "ProbMap");
        IJ.run(classifiedImage, "8-bit", "");

        return classifiedImage;
    }

    private ImagePlus smooth(ImagePlus imagePlus) {
        //smoothing TODO: Improve Smoothing functions
        IJ.run(imagePlus, "Smooth", "");
        IJ.run(imagePlus, "Smooth", "");
        IJ.run(imagePlus, "Smooth", "");

        return imagePlus;
    }

    /**
     * This function is meant to threshold the probability map.
     * We chose a lower limit such that we get significant portion of inner cell
     * @param imagePlus We expect a smoothed image of the probability map
     * @return A binary mask such that black color represents the interior of the cell
     *          This output will require post processing.
     *          Problems: The following regions can be black:
     *              - region outside the embryo -> To be solved used Cell Mask
     *              - small portions of cell membrane -> partly solved by morph functions
     *              - TODO: multiple region in single cell(gives multiple overlapping final result)
     *              - multiple granular region due to noise -> part solved using morph functions
     */
    private ImagePlus threshold(ImagePlus imagePlus) {

        // TODO: Automatically decide the lower limit
        IJ.setThreshold(imagePlus, lowerThreshold, upperThreshold, "Black & White");
        IJ.run(imagePlus, "Convert to Mask", "");
        return imagePlus;
    }

    private ImagePlus morph(ImagePlus imagePlus) {
        //Morphological Operations TODO: Improve
        IJ.run(imagePlus, "Close-", "");
        IJ.run(imagePlus, "Close-", "");
        IJ.run(imagePlus, "Erode", "");
        IJ.run(imagePlus, "Erode", "");
        IJ.run(imagePlus, "Close-", "");
        IJ.run(imagePlus, "Close-", "");
        IJ.run(imagePlus, "Dilate", "");
        IJ.run(imagePlus, "Dilate", "");
        IJ.run(imagePlus, "Dilate", "");

        return imagePlus;
    }

    private ParticleAnalyzer getParticleAnalyzer() {
        //Parameters for ParticleAnalyzer TODO: Research about them
        int opts = ParticleAnalyzer.ADD_TO_MANAGER;
        int meas = Measurements.ALL_STATS;
        double minSize = Math.PI * Math.pow((10.0 / 2), 2.0);
        double maxSize = Math.PI * Math.pow((300.0 / 2), 2.0);

        return new ParticleAnalyzer(opts, meas, new ResultsTable(), minSize, maxSize);
    }

    //originalImage must have an roi selected in it
    private ImagePlus getSegmentedImage(ImagePlus originalImage) {

        //roi for LS
        Roi roi = originalImage.getRoi();

        // parameters
        double convergence = 0.0050;
        double advection = 1.0;
        double curvature = 1.0;
        double grey_tol = 1.0;
        boolean expandToInside = false;
        int max_iteration = 25;
        int step_iteration = 100;

        return getSegImage(originalImage, roi, convergence, advection, curvature, grey_tol, expandToInside, max_iteration, step_iteration);
    }

    private ImagePlus getSegImage(ImagePlus originalImage, Roi roi, double convergence, double advection, double curvature, double grey_tol, boolean expandToInside, int max_iteration, int step_iteration) {
        originalImage.setRoi(roi);

        //creating ImageContainer
        ImageContainer ic = new ImageContainer(originalImage);

//        Creating ImageProgressContainer
//        If we don't want the progress report of level set algorithm
        ImageProgressContainer progressImage = null;

//        For progress report uncomment the code below
//        ImageProgressContainer progressImage = new ImageProgressContainer();
//        progressImage.duplicateImages(ic);
//        progressImage.createImagePlus("Segmentation progress of " + copy.getTitle());
//        progressImage.showProgressStep();


        // Create a initial state map out of the roi
        StateContainer sc_roi = new StateContainer();
        sc_roi.setROI(roi, ic.getWidth(), ic.getHeight(), ic.getImageCount(), originalImage.getCurrentSlice());

        //For which side to evolve. False implies that it will expand to Outside.
        sc_roi.setExpansionToInside(expandToInside);
        LevelSetImplementation ls = new ActiveContours(ic, progressImage, sc_roi, convergence, advection, curvature, grey_tol);

        for (int iter = 0; iter < max_iteration; iter++) {
            if (!ls.step(step_iteration)) {
                break;
            }
        }
        StateContainer sc_final = ls.getStateContainer();

        // Convert sc_final into binary image ImageContainer and display
        if (sc_final == null) {
            IJ.log("Wow man. sc_final is empty. You lost. Now die.");
        }
        ImageStack stack = new ImageStack(originalImage.getWidth(), originalImage.getHeight());
        for (ImageProcessor bp : sc_final.getIPMask()) {
            stack.addSlice(null, bp);
        }
        ImagePlus seg = originalImage.createImagePlus();
        seg.setStack("Segmentation of " + originalImage.getTitle(), stack);
        seg.setSlice(originalImage.getCurrentSlice());

        return seg;
    }

}