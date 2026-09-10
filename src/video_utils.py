import os
import cv2
import tempfile


def sample_frames(video_bytes: bytes,n_frames: int,extension: str) -> list:
    """
    Writes video_bytes to a temporary file (cv2.VideoCapture needs a
    file path, not an in-memory buffer), samples n_frames evenly-spaced
    frames across the video's duration, and cleans up the temp file.
 
    Returns a list of raw BGR numpy arrays. If the video has fewer
    frames than n_frames, all available frames are returned.
    """

    tmp_path=None
    frames=[]
    cap=None

    try:
        with tempfile.NamedTemporaryFile(delete=False,suffix=extension) as tmp_file:
            tmp_file.write(video_bytes)
            tmp_path=tmp_file.name

        cap = cv2.VideoCapture(tmp_path)
        if not cap.isOpened():
            raise ValueError("Could not open video file -- it may be corrupted "
                              "or in an unsupported format.")
 
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0:
           
            raise ValueError("Video contains no readable frames.")
        n_to_sample=min(total_frames,n_frames)
        frame_indices=[int(i*total_frames/n_to_sample) for i in range(n_to_sample)]
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES,idx)
            success,frame=cap.read()
            if success:
                frames.append(frame)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        if cap is not None:
            cap.release()
        return frames
