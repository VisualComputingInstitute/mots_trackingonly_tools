#!/usr/bin/env python3

import os
import pycocotools.mask as cocomask
from io_utils import load_seqmap, load_detections_for_seq
from config import DATASET, RESULT_PATH, seqmap_filename, det_path, split_str


tracking_path = os.path.join(RESULT_PATH, DATASET, "tracking", split_str)
out_path = os.path.join(RESULT_PATH, DATASET, "final", split_str)

seqmap = load_seqmap(seqmap_filename)
os.makedirs(out_path, exist_ok=True)


class Linking:
    def __init__(self, det_id, track_id, mask_merge_confidence):
        self.det_id = det_id
        self.track_id = track_id
        self.mask_merge_confidence = mask_merge_confidence


for seq_id in seqmap:
    print(seq_id)
    det_fn = os.path.join(det_path, seq_id + ".txt")
    _, dets_by_id = load_detections_for_seq(det_fn, decode_masks=False)
    tracking_fn = os.path.join(tracking_path, seq_id + ".txt")
    out_fn = os.path.join(out_path, seq_id + ".txt")

    with open(tracking_fn) as f:
        linkings = []
        for l in f:
            sp = l.strip().split()
            assert len(sp) == 3, sp
            det_id = int(sp[0])
            track_id = int(sp[1])
            conf = float(sp[2])
            lnk = Linking(det_id, track_id, conf)
            linkings.append(lnk)
        linkings.sort(key=lambda x: -x.mask_merge_confidence)

    with open(out_fn, "w") as fout:
        used_pixels = {}
        for lnk in linkings:
            det = dets_by_id[lnk.det_id]
            if det.t in used_pixels:
                if cocomask.area(cocomask.merge([used_pixels[det.t], det.rle], intersect=True)) > 0:
                    det_mask_decoded = cocomask.decode(det.rle)
                    used_pixels_decoded = cocomask.decode(used_pixels[det.t])
                    det_mask_decoded[used_pixels_decoded > 0] = 0
                    if not det_mask_decoded.any():
                        continue
                    rle = cocomask.encode(det_mask_decoded)
                    rle["counts"] = rle["counts"].decode("UTF-8")
                else:
                    rle = det.rle
                used_pixels[det.t] = cocomask.merge([used_pixels[det.t], det.rle], intersect=False)
            else:
                rle = det.rle
                used_pixels[det.t] = det.rle
            print(det.t, lnk.track_id, det.class_id, *rle["size"], rle["counts"], file=fout)
