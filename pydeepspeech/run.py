
import argparse
import os
import shutil
import sys

from pydeepspeech.audioTranscript_cmd import transcribe
from pydeepspeech.installModels import installModelsIfNecessary


def check_path(path: str):
    if os.path.exists(path):
        return
    raise OSError(f'Did not find expected path {path}')

def main() -> None:
    parser = argparse.ArgumentParser(description='Transcribe long audio files using webRTC VAD or use the streaming interface')
    #parser.add_argument('--aggressive', type=int, choices=range(4), required=False, default=1,
    #                    help='Determines how aggressive filtering out non-speech is. (Interger between 0-3)')
    parser.add_argument('--wav_file', required=True,
                        help='Path to the audio file to run (WAV format)')
    parser.add_argument('--out_file', default=None)
    parser.add_argument('--model_dir',
                        help='Path to directory that contains all model files (output_graph and scorer)',
                        default=None)
    args = parser.parse_args()
    model_dir = args.model_dir or installModelsIfNecessary()
    expected_txt_file = args.wav_file[:-4] + '.txt'
    check_path(args.wav_file)
    check_path(model_dir)
    #check_path(os.path.join(model_dir,'deepspeech-0.9.3-models.scorer'))
    #check_path(os.path.join(model_dir,'deepspeech-0.9.3-models.pbmm'))
    transcribe(aggressive=1, audio=args.wav_file, model=model_dir, stream=False)
    if not os.path.exists(expected_txt_file):
        print(f'Expected a generated text file at {expected_txt_file} but none appeared.')
        sys.exit(1)
    if args.out_file:
        shutil.move(expected_txt_file, args.out_file)
        expected_txt_file = args.out_file
    print(f'Wrote out subtitle file {expected_txt_file}')
    sys.exit(0)

if __name__ == '__main__':
    main()
