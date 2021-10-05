# coding: utf8
import argparse
from kueski_mle_task.core.pipeline import Pipeline


def parse_cli_parameters():
    parser = argparse.ArgumentParser(description='Credit Risk Model')
    parser.add_argument('--preprocess-data', dest='preprocess_data', help='Processes Raw Data', default=False,
                        action='store_true')

    return parser.parse_args()


def main():
    cli_parameters = parse_cli_parameters()
    pipeline = Pipeline('config.yaml')
    pipeline.start_pipeline(preprocess_data=cli_parameters.preprocess_data)


if __name__ == '__main__':
    main()
