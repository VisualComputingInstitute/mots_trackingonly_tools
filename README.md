# mots_trackingonly_tools
Tools and example for Challenge 3: Tracking Only (MOT+KITTI) of MOTChallenge 2020 (https://motchallenge.net/workshops/bmtt2020/tracking.html)

In this challenge, you're given strong pre-computed detections with segmentation masks and your task is tracking only, i.e. you are only required to sub-select from the given masks, assign these consistent tracking IDs, and assign a score to each selected mask based on which overlapping masks will be combined (the final reslt must be non-overlapping).

Your tracker has to produce a txt format output. Each line has the following format:
det_id track_id mask_merge_confidence

Where 
det_id is the id of the detection in this sequence (i.e. the line number starting from 0 of the detection file)
track_id is an id of a track, you have to create these ids yourself and multiple detections can be mapped to the same track id
mask_merge_confidence is a float, for overlapping masks, the mask with the higher value will be on top

For an example to create results using a "dummy tracker" and evaluate them, run
./run_demo.sh

For questions please contact Paul Voigtlaender via voigtlaender@vision.rwth-aachen.de
