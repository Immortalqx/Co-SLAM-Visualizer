# Co-SLAM-Visualizer
Visualization tool similar to NICE-SLAM for Co-SLAM.

<p align="center">
  <a href="">
    <img src="./media/replica_room0.gif" alt="replica_room0" width="80%">
  </a>
</p>

## Installation

> Same as [Neural SLAM Evaluation Benchmark](https://github.com/JingwenWang95/neural_slam_eval)

This repo assumes you already configured the environment from [Co-SLAM](https://github.com/HengyiWang/Co-SLAM) main repository. You then also need the following dependencies:

* Open3D
* pyglet
* pyrender

You can install those dependencies by running:

```bash
conda activate coslam
pip install -r requirements.txt
```

## Run Visualizer

> Only tested on Rellica, TUM, Azure datasets.

**Recommend Step**

1. ```shell
   git clone https://github.com/Immortalqx/Co-SLAM-Visualizer.git
   cd Co-SLAM-Visualizer
   ```

2. Copy `configs`, `tools`, `visualizer.py` to the Co-SLAM directory;

3. Co-SLAM saves the mesh every 500 rounds. If you want to save the mesh every 50 rounds like NICE-SLAM, you need to [re-run Co-SLAM](https://github.com/HengyiWang/Co-SLAM?tab=readme-ov-file#run).

4. You can run Co-SLAM Visualizer using the code below:

   ```shell
   python visualizer.py --config './configs/{Dataset}/{scene}.yaml 
   
   # Example
   python visualizer.py --config ./configs/Replica/room0.yaml
   python visualizer.py --config ./configs/Azure/apartment.yaml
   python visualizer.py --config ./configs/Tum/fr1_desk.yaml
   ```
