"""Script for running perplexity experiment."""

from absl import app, flags

from llama3.eval import Experiment
from llama3.utils.load_utils import load_config, save_config, setup_log_dir

FLAGS = flags.FLAGS
flags.DEFINE_string("base", None, "Path to base config.")
flags.DEFINE_string("devices", None, "Devices to use.")
flags.DEFINE_boolean("verbose", False, "Whether to print non-flag arguments.")


def main(argv):
    """
    Main function for running experiments.
    """
    if FLAGS.verbose:
        print("non-flag arguments:", argv)

    assert FLAGS.base is not None, "Configs not specified, must specify base"
    config = load_config(FLAGS.base)

    experiment_log_dir = setup_log_dir(
        config.get("logs_dir", "experiment_logs"),
        experiment_name=config.get("experiment_name", None),
    )

    config["experiment_config"]["experiment_log_dir"] = experiment_log_dir
    save_config(config.to_dict(), experiment_log_dir + "/config.yaml")

    experiment = Experiment(config["experiment_config"])
    for key, paths in config["dataset_path"].items():
        for path in paths:
            experiment.run(dataset_name=key, dataset_path=path)


if __name__ == "__main__":
    app.run(main)
