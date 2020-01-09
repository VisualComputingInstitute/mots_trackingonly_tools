import os

MOTS_TOOLS_ROOT = "./mots_tools/"
DET_PATH_ROOT = "./detections/"
RESULT_PATH = "./results/"
DATASET = "KITTI_MOTS"  # either "KITTI_MOTS" or "MOTSChallenge"
#DATASET = "MOTSChallenge"
RUN_ON_TEST_SET = False  # either run on test set or on trainval


#######

if DATASET == "KITTI_MOTS":
    if RUN_ON_TEST_SET:
        seqmap_name = "test"
    else:
        seqmap_name = "fulltrain"
elif DATASET == "MOTSChallenge":
    if RUN_ON_TEST_SET:
        seqmap_name = "test_MOTSchallenge"
    else:
        seqmap_name = "val_MOTSchallenge"
else:
    assert False, ("unknown dataset", DATASET)
seqmap_filename = os.path.join(MOTS_TOOLS_ROOT, "mots_eval", seqmap_name + ".seqmap")
split_str = "test" if RUN_ON_TEST_SET else "trainval"
det_path = os.path.join(DET_PATH_ROOT, DATASET, split_str)
