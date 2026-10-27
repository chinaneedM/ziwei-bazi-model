#!/usr/bin/env python3
"""Replay bounded CADAL/1174 image registration; never infer edition identity.

Usage: python scripts/replay-yehuobian-image-registration-12tc.py p121.jpg page-506.jpg
Optional local dependencies: numpy, opencv-python-headless. Never downloads.
This diagnostic is separate from the direct human source-glyph collation.
"""
import hashlib
import json
import sys
from pathlib import Path

CADAL_SHA = "5e4f288f257a83b8f851c53c791dd2d2df52e18bd66276256ef6b64e546894a6"
XUXIU_SHA = "ece3094a332ca5f329a1c21f27f3e65a3412a2ad252452cae5a17fe50fd0ac11"

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: replay-yehuobian-image-registration-12tc.py CADAL_p121.jpg XUXIU_p506.jpg")
    import cv2
    import numpy as np
    paths = [Path(sys.argv[1]), Path(sys.argv[2])]
    for path, expected in zip(paths, [CADAL_SHA, XUXIU_SHA]):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit("SOURCE_JPEG_SHA256_MISMATCH_FAIL_CLOSED " + str(path))
    a = cv2.imread(str(paths[0]), cv2.IMREAD_GRAYSCALE)
    b = cv2.imread(str(paths[1]), cv2.IMREAD_GRAYSCALE)
    if a is None or b is None or a.shape != (1400, 933) or b.shape != (2300, 1645):
        raise SystemExit("SOURCE_PAGE_DIMENSION_MISMATCH_FAIL_CLOSED")
    a = a[185:1220, 75:835]
    b = b[1165:1970, 223:810]
    sift = cv2.SIFT_create(nfeatures=4500)
    pts_a, da = sift.detectAndCompute(a, None)
    pts_b, db = sift.detectAndCompute(b, None)
    if da is None or db is None:
        raise SystemExit("INSUFFICIENT_IMAGE_KEYPOINTS")
    pairs = cv2.BFMatcher().knnMatch(da, db, k=2)
    good = [x for x, y in pairs if x.distance < 0.75 * y.distance]
    if len(good) < 10:
        raise SystemExit("INSUFFICIENT_MATCHED_KEYPOINTS")
    p = np.float32([pts_a[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    q = np.float32([pts_b[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    transform, mask = cv2.findHomography(p, q, cv2.RANSAC, 3.5)
    if transform is None:
        raise SystemExit("SOURCE_REGISTRATION_FAILED")
    inliers = mask.ravel().astype(bool)
    predicted = cv2.perspectiveTransform(p, transform)
    errors = np.linalg.norm(predicted.reshape(-1, 2) - q.reshape(-1, 2), axis=1)[inliers]
    warped = cv2.warpPerspective(a, transform, (b.shape[1], b.shape[0]))
    w = warped[25:-25, 25:-25]
    v = b[25:-25, 25:-25]
    def corr(x, y):
        return float(np.corrcoef(x.ravel(), y.ravel())[0, 1])
    blurry_w = cv2.GaussianBlur(w, (5, 5), 2)
    blurry_v = cv2.GaussianBlur(v, (5, 5), 2)
    result = {
        "schema": "TIANWEN-12TC-IMAGE-REGISTRATION-REPLAY",
        "source_jpeg_sha256_verified": True, "ocr_used": False,
        "opencv": cv2.__version__, "good_matches": len(good),
        "homography_inliers": int(inliers.sum()),
        "inlier_fraction": float(inliers.mean()),
        "inlier_reprojection_error_median_pixels": float(np.median(errors)),
        "inlier_reprojection_error_p90_pixels": float(np.percentile(errors, 90)),
        "registered_gray_pearson": corr(w, v),
        "registered_blur_sigma2_pearson": corr(blurry_w, blurry_v),
        "same_physical_copy_proven": False,
        "same_printing_plate_impression_proven": False,
        "image_similarity_is_not_textual_witness_independence": True,
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
