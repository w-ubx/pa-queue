import face_recognition
import json
import pytesseract
import io


def encode_photo(path):
    photo_id = face_recognition.load_image_file(path)
    photo_encoding = face_recognition.face_encodings(photo_id)[0]

    return json.dumps(photo_encoding.tolist())

def compare_photo(encoded_id, path_captured):
    id_encoded = json.loads(encoded_id)

    captured_id = face_recognition.load_image_file(path_captured)
    captured_encoding = face_recognition.face_encodings(captured_id)[0]

    results = face_recognition.compare_faces(
        [id_encoded], captured_encoding, tolerance=0.5)

    return results[0]