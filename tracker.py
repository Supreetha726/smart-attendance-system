from deep_sort_realtime.deepsort_tracker import DeepSort

tracker = DeepSort(max_age=30)

def track_objects(detections, frame):
    tracks = tracker.update_tracks(detections, frame=frame)
    
    results = []
    for track in tracks:
        if not track.is_confirmed():
            continue
        results.append((track.track_id, track.to_ltrb()))
    
    return results