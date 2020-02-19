import json
import os

from nyaggle.experiment import Experiment
from nyaggle.testing import get_temp_directory


def test_experiment_continue():
    with get_temp_directory() as logging_dir:
        with Experiment(logging_dir, with_mlflow=True) as e:
            e.log_metric('CV', 0.97)

        # appending to exising local & mlflow result
        with Experiment.continue_from(logging_dir) as e:
            e.log_metric('LB', 0.95)

            metric_file = os.path.join(logging_dir, 'metrics.json')

            import mlflow

            client = mlflow.tracking.MlflowClient()
            data = client.get_run(mlflow.active_run().info.run_id).data
            assert data.metrics['CV'] == 0.97
            assert data.metrics['LB'] == 0.95

        with open(metric_file, 'r') as f:
            obj = json.load(f)
            assert obj['CV'] == 0.97
            assert obj['LB'] == 0.95
