#!/usr/bin/env python3

import os
from io_utils import load_seqmap, load_detections_for_seq
from config import DATASET, RESULT_PATH, seqmap_filename, det_path, split_str


out_path = os.path.join(RESULT_PATH, DATASET, "tracking", split_str)
seqmap = load_seqmap(seqmap_filename)
os.makedirs(out_path, exist_ok=True)

for seq_id in seqmap:
    print(seq_id)
    det_fn = os.path.join(det_path, seq_id + ".txt")
    seq_dets, _ = load_detections_for_seq(det_fn, decode_masks=False)
    out_file = os.path.join(out_path, seq_id + ".txt")
    with open(out_file, "w") as f:
        for t, seq_dets_t in seq_dets.items():
            for det in seq_dets_t:
                # only select confident detections
                if det.confidence > 0.7:
                    det_id = det.det_id
                    # dummy tracker: put each detection in its own track
                    track_id = det_id
                    # and use detection confidence as confidence for merging masks
                    # meaning that for two detections overlapping masks, the mask of the detection with higher
                    # confidence will take precedence
                    mask_merge_confidence = det.confidence
                    # write out result as mapping from detection ids to track ids
                    print(det_id, track_id, mask_merge_confidence, file=f)
