def build_array(tracks, fmt='motchallenge'):
    """
    Saves tracks to a CSV file.
    Args:
        out_path (str): path to output csv file.
        tracks (list): list of tracks to store.
    """
    with open(out_path, "w") as ofile:
        if fmt == 'motchallenge':
            field_names = ['frame', 'id', 'x', 'y', 'w', 'h', 'score', 'wx', 'wy', 'wz']
        else:
            raise ValueError("unknown format type '{}'".format(fmt))

        id_ = 1
        track_array = []
        for track in tracks:
            for i, bbox in enumerate(track['bboxes']):
                row = {'id': id_,
                       'frame': track['start_frame'] + i,
                       'x': bbox[0]+1,
                       'y': bbox[1]+1,
                       'w': bbox[2] - bbox[0],
                       'h': bbox[3] - bbox[1],
                       'score': track['max_score']}
                if fmt == 'motchallenge':
                    row['wx'] = -1
                    row['wy'] = -1
                    row['wz'] = -1
                else:
                    raise ValueError("unknown format type '{}'".format(fmt))
                    
                track_array.append(row)

            id_ += 1
