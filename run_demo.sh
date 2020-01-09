#!/usr/bin/env bash

# clone mots tools, we'll need it to get sequence maps and to run the evaluation in the end
git clone https://github.com/VisualComputingInstitute/mots_tools

# download and unpack detections (for both KITTI MOTS and MOTSchallenge)
mkdir -p detections
cd detections
wget https://www.vision.rwth-aachen.de/media/resource_files/MOTS20_detections.zip
unzip MOTS20_detections.zip
rm MOTS20_detections.zip
cd ..

# if you want to run on MOTSchallenge instead, you have to set DATASET = "MOTSChallenge" in config.py and do more changes below (see comments)

# run dummy tracker (it just keeps all detections with high confidence and assigns each detection to it's own track)
# it will write out the result as a mapping from detection ids to tracks ids to ./results/
echo "Running dummy tracker..."
python3 dummy_tracker.py

# convert tracking result (the mapping from detection ids to track ids) to the final MOTS result
echo "Converting tracking reslt to final MOTS result..."
python3 convert_tracking_to_final_result.py

# Download ground truth for KITTI_MOTS
mkdir -p mots_data/KITTI_MOTS
cd mots_data/KITTI_MOTS
wget https://www.vision.rwth-aachen.de/media/resource_files/instances_txt.zip
# if you want to run on MOTSChallenge instead, you can find the annotations here: https://www.vision.rwth-aachen.de/media/resource_files/instances_txt_motschallenge.zip
unzip instances_txt.zip
rm instances_txt.zip
cd ../..

# run evaluation on KITTI MOTS validation set
echo "Running evaluation..."
echo "This script uses a dummy tracker, so you'll see that you get many true positives from the strong detections but tons of ID switches from the dummy tracker."
# if you want to run on MOTSChallenge instead, you'll need to change the seqmap to ./mots_tools/mots_eval/val_MOTSchallenge.seqmap
python3 mots_tools/mots_eval/eval.py ./results/KITTI_MOTS/final/trainval/ ./mots_data/KITTI_MOTS/instances_txt/ ./mots_tools/mots_eval/val.seqmap
