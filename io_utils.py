import os
from collections import OrderedDict


class Sequence:
    def __init__(self, id_, end_time, start_time=0):
        self.id_ = id_
        self.end_time = end_time  # inclusive, i.e. end_time is still in
        self.start_time = start_time


class Detection:
    def __init__(self, det_id, t, class_id, confidence, bbox, rle, mask=None):
        self.det_id = det_id
        self.t = t
        self.class_id = class_id
        self.confidence = confidence
        self.bbox = bbox
        self.rle = rle
        self.mask = mask


def load_seqmap(seqmap_filename):
    seqs = OrderedDict()
    with open(seqmap_filename) as f:
        for l in f:
            sp = l.split()
            assert len(sp) == 4
            id_ = sp[0]
            start_time = int(sp[2])
            end_time = int(sp[3])
            seq = Sequence(id_, start_time, end_time)
            seqs[id_] = seq
    return seqs


# careful: this might consume A LOT of memory. Consider using load_detections_for_seq instead
def load_detections(seqmap, detections_path, decode_masks=True):
    if isinstance(seqmap, str):
        seqmap = load_seqmap(seqmap)
    dets = {}
    for seq_id in seqmap:
        det_fn = os.path.join(detections_path, seq_id + ".txt")
        print("loading detections for sequence", seq_id)
        seq_dets, _ = load_detections_for_seq(det_fn, decode_masks=decode_masks)
        dets[seq_id] = seq_dets
    return dets


def load_detections_for_seq(det_fn, decode_masks=True):
    dets_by_time = OrderedDict()
    dets_by_id = {}
    det_id = 0
    with open(det_fn) as f:
        for l in f:
            sp = l.strip().split()
            assert len(sp) == 10, sp
            t = int(sp[0])
            bbox = [float(x) for x in sp[1:5]]
            confidence = float(sp[5])
            class_id = int(sp[6])
            im_height = int(sp[7])
            im_width = int(sp[8])
            size = [im_height, im_width]
            rle_str = sp[9]
            rle = {"size": size, "counts": rle_str}
            if decode_masks:
                from pycocotools.mask import decode
                mask = decode(rle)
            else:
                mask = None
            det = Detection(det_id, t, class_id, confidence, bbox, rle, mask)
            dets_by_id[det_id] = det
            det_id += 1
            if t not in dets_by_time:
                dets_by_time[t] = []
            dets_by_time[t].append(det)
    return dets_by_time, dets_by_id
