def get_landmark_model(saved_model="models/pose_model"):
    try:
        import tensorflow as tf
        from tensorflow import keras
        model = keras.models.load_model(saved_model)
        return model
    except Exception:
        return None

def get_square_box(box):
    left_x = box[0]
    top_y = box[1]
    right_x = box[2]
    bottom_y = box[3]

    box_width = right_x - left_x
    box_height = bottom_y - top_y

    diff = box_height - box_width
    delta = int(abs(diff) / 2)

    if diff == 0:                   # Already a square.
        return box
    elif diff > 0:                  # Height > width, a slim box.
        left_x -= delta
        right_x += delta
        if diff % 2 == 1:
            right_x += 1
    else:                           # Width > height, a short box.
        top_y -= delta
        bottom_y += delta
        if diff % 2 == 1:
            bottom_y += 1

    assert ((right_x - left_x) == (bottom_y - top_y)), 'Box is not square.'

    return [left_x, top_y, right_x, bottom_y]

def move_box(box, offset):
        left_x = box[0] + offset[0]
        top_y = box[1] + offset[1]
        right_x = box[2] + offset[0]
        bottom_y = box[3] + offset[1]
        return [left_x, top_y, right_x, bottom_y]

def detect_marks(img, model, face):
    if model is None:
        x, y, x1, y1 = face
        w = max(1, x1 - x)
        h = max(1, y1 - y)
        marks = np.zeros((68, 2), dtype=int)
        # 30: nose tip
        marks[30] = [x + int(w * 0.5), y + int(h * 0.55)]
        # 8: chin
        marks[8] = [x + int(w * 0.5), y + int(h * 0.95)]
        # 36: left eye left corner
        marks[36] = [x + int(w * 0.28), y + int(h * 0.38)]
        # 45: right eye right corner
        marks[45] = [x + int(w * 0.72), y + int(h * 0.38)]
        # 48: left mouth corner
        marks[48] = [x + int(w * 0.33), y + int(h * 0.75)]
        # 54: right mouth corner
        marks[54] = [x + int(w * 0.67), y + int(h * 0.75)]
        return marks

    try:
        import tensorflow as tf
        offset_y = int(abs((face[3] - face[1]) * 0.1))
        box_moved = move_box(face, [0, offset_y])
        facebox = get_square_box(box_moved)
        
        h, w = img.shape[:2]
        if facebox[0] < 0:
            facebox[0] = 0
        if facebox[1] < 0:
            facebox[1] = 0
        if facebox[2] > w:
            facebox[2] = w
        if facebox[3] > h:
            facebox[3] = h
        
        face_img = img[facebox[1]: facebox[3],
                         facebox[0]: facebox[2]]
        face_img = cv2.resize(face_img, (320, 320))
        face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        
        predictions = model.signatures["predict"](
            tf.constant([face_img], dtype=tf.uint8))

        marks = np.array(predictions['output']).flatten()[:136]
        marks = np.reshape(marks, (-1, 2))
        
        marks *= (facebox[2] - facebox[0])
        marks[:, 0] += facebox[0]
        marks[:, 1] += facebox[1]
        marks = marks.astype(int)

        return marks
    except Exception:
        x, y, x1, y1 = face
        w = max(1, x1 - x)
        h = max(1, y1 - y)
        marks = np.zeros((68, 2), dtype=int)
        marks[30] = [x + int(w * 0.5), y + int(h * 0.55)]
        marks[8] = [x + int(w * 0.5), y + int(h * 0.95)]
        marks[36] = [x + int(w * 0.28), y + int(h * 0.38)]
        marks[45] = [x + int(w * 0.72), y + int(h * 0.38)]
        marks[48] = [x + int(w * 0.33), y + int(h * 0.75)]
        marks[54] = [x + int(w * 0.67), y + int(h * 0.75)]
        return marks