import os
from pathlib import Path

import hydra
from hydra.utils import instantiate
import numpy as np
import matplotlib.pyplot as plt

from navsim.common.dataloader import SceneLoader
from navsim.common.dataclasses import SceneFilter, SensorConfig

SPLIT = "mini"  # ["mini", "test", "trainval"]
FILTER = "all_scenes"

hydra.initialize(config_path="navsim/planning/script/config/common/train_test_split/scene_filter", version_base="1.1")
cfg = hydra.compose(config_name=FILTER)
scene_filter: SceneFilter = instantiate(cfg)
openscene_data_root = Path("download")

scene_loader = SceneLoader(
    openscene_data_root / f"{SPLIT}_navsim_logs/{SPLIT}",
    openscene_data_root / f"{SPLIT}_sensor_blobs/{SPLIT}",
    scene_filter,
    sensor_config=SensorConfig.build_all_sensors(),
)

token = np.random.choice(scene_loader.tokens)
scene = scene_loader.get_scene_from_token(token)