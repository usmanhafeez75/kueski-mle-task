# coding: utf8
import argparse

from kueski_mle_task.app import app
from kueski_mle_task.core.pipeline import Pipeline


def parse_cli_parameters():
    parser = argparse.ArgumentParser(description='Credit Risk Model')
    parser.add_argument('--preprocess-data', dest='preprocess_data', help='Processes Raw Data', default=False,
                        action='store_true')
    parser.add_argument('--train-model', dest='train_model', help='Train Model', default=False,
                        action='store_true')
    parser.add_argument('--load-model', dest='load_model', help='Load Model', default=False,
                        action='store_true')
    parser.add_argument('--generate-prediction', dest='generate_prediction', help='Generate Prediction', default=False,
                        action='store_true')
    parser.add_argument("--input-file", dest="input_file", help="input csv file with data to be predicted")
    parser.add_argument("--output-file", dest="output_file", help="output csv file with status prediction")
    parser.add_argument('--serve-model', dest='serve_model', help='Serve Model', default=False,
                        action='store_true')

    options = parser.parse_args()

    if options.generate_prediction and not all([options.input_file, options.output_file]):
        raise ValueError("--input-file and --output-file argument must be provided when using --generate-prediction")

    return options


def main():
    cli_parameters = parse_cli_parameters()
    pipeline = Pipeline()
    pipeline.start_pipeline(preprocess_data=cli_parameters.preprocess_data,
                            train_model=cli_parameters.train_model,
                            load_model=cli_parameters.load_model,
                            generate_prediction=cli_parameters.generate_prediction,
                            input_file=cli_parameters.input_file,
                            output_file=cli_parameters.output_file)

    del pipeline
    if cli_parameters.serve_model:
        app.run()


if __name__ == '__main__':
    main()
