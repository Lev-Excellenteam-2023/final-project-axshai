class LectureParser:
    def __init__(self, lecture_path):
        self._lecture = lecture_path

    def get_lecture_parts(self):
        raise NotImplementedError

    def parse_lecture_part(self, lecture_part) -> str:
        raise NotImplementedError
