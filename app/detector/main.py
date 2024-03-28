import cv2
import os

from app.common.broker import Broker
from app.common.config.core import create_and_validate_config
from app.common.context import Context
from app.common.model.model import YOLOModel
from app.detector.pipeline import Pipeline


if __name__ == "__main__":
    broker = Broker()
    config = create_and_validate_config()
    model = YOLOModel(config.mdl_config.weights, config.mdl_config.config, config.mdl_config.classes)    
    context = Context(broker, model, config)
    pipeline = Pipeline(context, config.detector_pipeline_config)

    cap = cv2.VideoCapture(0)
    while True:
        ret, image = cap.read()
        if not ret:
            continue
        pipeline.run(image)