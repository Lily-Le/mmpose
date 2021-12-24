# Copyright (c) OpenMMLab. All rights reserved.
from typing import List, Optional, Union

from .builder import NODES
from .node import Node

try:
    from mmdet.apis import inference_detector, init_detector
    has_mmdet = True
except (ImportError, ModuleNotFoundError):
    has_mmdet = False


@NODES.register_module()
class DetectorNode(Node):

    def __init__(self,
                 name: str,
                 model_config: str,
                 model_checkpoint: str,
                 input_buffer: str,
                 output_buffer: Union[str, List[str]],
                 enable_key: Optional[Union[str, int]] = None,
                 device: str = 'cuda:0'):
        # Check mmdetection is installed
        assert has_mmdet, 'Please install mmdet to run the demo.'
        super().__init__(name=name, enable_key=enable_key, enable=True)

        self.model_config = model_config
        self.model_checkpoint = model_checkpoint
        self.device = device.lower()

        # Register buffers
        self.register_input_buffer(input_buffer, 'input', essential=True)
        self.register_output_buffer(output_buffer)

    def on_start(self):
        self.model = init_detector(
            self.model_config,
            self.model_checkpoint,
            device=self.device.lower())

    def bypass(self, input_msgs):
        return input_msgs['input']

    def process(self, input_msgs):
        input_msg = input_msgs['input']

        img = input_msg.get_image()

        preds = inference_detector(self.model, img)
        det_result = self._post_process(preds)

        input_msg.add_detection_result(det_result, tag=self.name)
        return input_msg

    def _post_process(self, preds):
        if isinstance(preds, tuple):
            preds = preds[0]

        assert len(preds) == len(self.model.CLASSES)
        result = {'preds': [], 'model_cfg': self.model.cfg.copy()}

        for i, (cls_name, bboxes) in enumerate(zip(self.model.CLASSES, preds)):
            preds_i = [{
                'cls_id': i,
                'label': cls_name,
                'bbox': bbox
            } for bbox in bboxes]
            result['preds'].extend(preds_i)

        return result