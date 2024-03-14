import cv2
from pathlib import Path


class YOLOModel:

    data_path: Path = str(Path(__file__).resolve().parent / "data")

    def __init__(self, weights, config, classes):
        self.model = cv2.dnn.readNet(
            f"{self.data_path}/{weights}",
            f"{self.data_path}/{config}"
        )
        with open(f"{self.data_path}/{classes}", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

    def compute_outputs(self, blob):
        self.model.setInput(blob)
        outs = self.model.forward(self.model.getUnconnectedOutLayersNames())
        return outs