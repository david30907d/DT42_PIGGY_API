import os
import cv2
import sys
import time
import argparse
import logging
from trainer.components import frame_reader
from dt42lab.core import tools
from dt42lab.utility import dict_comparator
from trainer.components import frame_reader
from trainer.pipelines import pipeline as dt42pl
from pynput import keyboard

import sys
import tty
import termios
import threading
import time

from pynput import keyboard

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def monitor(sentinel='q'):

    """reads the stdin until a single char in 'sentinel' is found"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch in sentinel:
                break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def get_args(argv=None):
    """ Prepare auguments for running the script """

    parser = argparse.ArgumentParser(
        description='Pipeline.'
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default='',
        help='Output folder for output_metadata')
    parser.add_argument(
        '-j',
        '--json_list',
        type=str, default=None,
        help="Path to the text file of json lists."
    )
    parser.add_argument(
        '-d',
        '--data_list',
        type=str,
        default='/home/shared/DT42/test_data/'
        'test_auto_labeler_with_tracker/frame_list.txt',
        help="Path to the text file of train images list"
    )
    parser.add_argument(
        '--direct_input', dest='direct_input',
        action='store_true', default=False,
        help="True to use data_list as direct input (i.e. no txt to list)"
    )
    parser.add_argument(
        '--cam_input', dest='cam_input',
        action='store_true', default=False,
        help="True to use usb camera as input"
    )
    parser.add_argument(
        '--rtsp_input', dest='rtsp_input',
        action='store_true', default=False,
        help="True to use rtsp as input"
    )
    parser.add_argument(
        '-ip',
        '--ip',
        type=str,
        default='',
        help="Rtsp ip address"
    )
    parser.add_argument(
        '-m',
        '--repeated_metadata_path',
        type=str,
        default='',
        help="Path of external metadata feed in pipeline repeatedly."
    )
    parser.add_argument(
        '--lab_flag', dest='lab_flag', action='store_true', default=False,
        help='True to enable related lab process.'
    )
    parser.add_argument(
        '--benchmark', dest='benchmark', action='store_true', default=False,
        help='True to enable pipeline benchmark of time used.'
    )
    parser.add_argument(
        '--force_run_skip', dest='force_run_skip',
        action='store_true', default=False,
        help='True to force running skip components.'
    )
    parser.add_argument(
        '--read_frame', dest='read_frame', action='store_true', default=False,
        help='True to read frame before sending input to trainer pipeline.'
    )
    parser.add_argument(
        '-p', '--pipeline_config', type=str,
        help='File contains the definition of pipeline application.',
        default='/home/lab/dt42-trainer/pipeline.config'
    )
    parser.add_argument(
        '--trainer_config_path', type=str,
        help='File of trainer config',
        default=''
    )
    parser.add_argument(
        '--read_meta', dest='read_meta', action='store_true', default=False,
        help='Read metadata',
    )
    parser.add_argument(
        "-v", "--verbosity", action="count", default=0,
        help="increase output verbosity"
    )
    parser.add_argument(
        "--loop_over_input", dest='loop_over_input',
        action='store_true', default=False,
        help="Loop over input data_list"
    )
    parser.add_argument(
        "--force_snapshot", dest='force_snapshot',
        action='store_true', default=False,
        help="Force snapshot components with force_snapshotable on."
    )
    parser.add_argument(
        "--do_not_pack", dest='do_not_pack',
        action='store_true', default=False,
        help="True to send data to pipeline directly without packaging as list"
    )
    parser.add_argument(
        "--multi_channels", dest='multi_channels',
        action='store_true', default=False,
        help="True to input 4 channels to pipeline"
    )
    parser.add_argument(
        "--check_output", dest='check_output',
        action='store_true', default=False,
        help="Check output with reference output list given"
    )
    parser.add_argument(
        '-r',
        '--ref_output',
        type=str,
        default='',
        help="Path to the json file with list of reference output"
    )
    parser.add_argument(
        '-ig',
        '--ignore_key',
        type=str,
        default='',
        help=(
            "Ignore key(s) while checking output."
            "Use , to seperate if you have multiple keys"
        )
    )

    return parser.parse_args(argv)


def main():
    """ main function to run pipeline """

    args = get_args()

    logger = logging.getLogger('launcher')
    log_level = logging.WARNING
    if args.verbosity == 1:
        log_level = logging.INFO
    elif args.verbosity >= 2:
        log_level = logging.DEBUG
    formatter = logging.Formatter('[launcher] %(levelname)s %(message)s')
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.setLevel(log_level)
    logger.addHandler(console)

    logger.info('lab_flag is %r' % args.lab_flag)
    pipeline = dt42pl.Pipeline(
        args.pipeline_config,
        trainer_config_path=args.trainer_config_path,
        parent_result_folder=args.output,
        verbosity=args.verbosity,
        lab_flag=args.lab_flag,
        force_run_skip=args.force_run_skip
    )


    if args.cam_input:

        t = threading.Thread(target=monitor)
        t.start()
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        meta_path = args.repeated_metadata_path
        ext_meta=tools.parse_json(meta_path, 'utf-8')
        while t.isAlive():
            ret, frame = cap.read()
            pipeline.run(
                frame, external_meta=ext_meta, benchmark=False,
                force_snapshot=False
            )
            print('pipeline_output', pipeline.output[0].shape)

    elif args.rtsp_input:

        t = threading.Thread(target=monitor)
        t.start()

        cap = cv2.VideoCapture(args.ip)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        while t.isAlive():
            ret, frame = cap.read()
            pipeline.run(
                frame, external_meta=[], benchmark=False,
                force_snapshot=False
            )

def check_result(tar, ref, input_filename, all_pass, ignore_keys=[]):
    if tar == [] and ref == []:
        pass
    else:
        report = dict_comparator.get_diff(ref, tar, ignore_keys=ignore_keys)
        if report['extra_field'] == [] and \
                report['missing_field'] == []and \
                report['mismatch_val'] == []:
            pass
        else:
            print('[Launcher] Output is different with reference: %s'
                  % input_filename)
            all_pass = False
    return all_pass


def read_meta_single(args, logger, full_path):
    ext_meta = []
    if args.read_meta:
        logger.debug('Reading json for producing binary meta')
        if args.repeated_metadata_path == '':
            meta_path = tools.remove_extension(full_path) + '.json'
        else:
            meta_path = args.repeated_metadata_path
        try:
            ext_meta = tools.parse_json(meta_path, 'utf-8')
        except BaseException:
            logger.error('Fail to parse %s' % meta_path)
            sys.exit(0)
    return ext_meta


if __name__ == "__main__":
    main()
