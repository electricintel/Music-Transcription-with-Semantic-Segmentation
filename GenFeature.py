import os
import argparse

import project.Feature.FeatureProcessor as fp
import project.configuration as conf
from project.configuration import MapsDatasetInfo, MusicNetDatasetInfo, MaestroDatasetInfo, SuDatasetInfo, Bach10DatasetInfo, URMPDatasetInfo
from project.configuration import Su10DatasetInfo, RhythmDatasetInfo


d_conf = {
    "Maps": {
        "dataset_info": conf.MapsDatasetInfo,
        "processor": fp.MapsFeatExt
    },
    "Maestro": {
        "dataset_info": conf.MaestroDatasetInfo,
        "processor": fp.MaestroFeatExt
    },
    "MusicNet": {
        "dataset_info": conf.MusicNetDatasetInfo,
        "processor": fp.MusicNetFeatExt
    },
    "Su": {
        "dataset_info": conf.SuDatasetInfo,
        "processor": fp.SuFeatExt
    },
    "Su-10": {
        "dataset_info": conf.Su10DatasetInfo,
        "processor": fp.SuFeatExt
    },
    "URMP": {
        "dataset_info": conf.URMPDatasetInfo,
        "processor": fp.SuFeatExt
    },
    "Bach": {
        "dataset_info": conf.Bach10DatasetInfo,
        "processor": fp.SuFeatExt
    },
    "Rhythm": {
        "dataset_info": conf.RhythmDatasetInfo,
        "processor": fp.RhythmFeatExt
    }
}


def create_parser():
    parser = argparse.ArgumentParser("Feature Processor")
    parser.add_argument("dataset", help="One of Maps, MusicNet, or Maestro", 
                        type=str, choices=["Maps", "MusicNet", "Maestro", "Su", "Su-10", "URMP", "Bach", "Rhythm"])
    parser.add_argument("dataset_path", help="Path to the downloaded dataset",
                        type=str)
    parser.add_argument("-p", "--phase", help="Generate training feature or testing feature. Default: %(default)s",
                        type=str, default="train", choices=["train", "test"])
    parser.add_argument("-n", "--piece-per-file", help="Number of pieces should be included in one generated file",
                        type=int, default=40)
    parser.add_argument("-s", "--save-path", help="Path to save the generated feature and label files", 
                        type=str, default="./train_feature")
    parser.add_argument("-a", "--harmonic", help="Generate harmonic features",
                        action="store_true")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    dinfo = d_conf[args.dataset]["dataset_info"](args.dataset_path)
    proc_cls = d_conf[args.dataset]["processor"]

    paths = dinfo.train_wavs if args.phase=="train" else dinfo.test_wavs
    wav_paths = [os.path.join(dinfo.base_path, path) for path in paths]
    paths = dinfo.train_labels if args.phase=="train" else dinfo.test_labels
    label_paths = [os.path.join(dinfo.base_path, path) for path in paths] 

    processor = proc_cls(
        wav_paths, 
        label_paths, 
        dinfo.label_ext,
        save_path=args.save_path,
        file_prefix=args.phase,
        piece_per_file=args.piece_per_file,
        harmonic=args.harmonic
    )
    processor.process()


if __name__ == "__main__":
    main()

