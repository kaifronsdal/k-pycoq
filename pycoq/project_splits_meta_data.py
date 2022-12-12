"""

A data set is made from a collection (list) of coq projs/pkgs.
Each of these coq projs/pkgs has split for their coq .v files.
An example split (see: ~proverbot9001/coqgym_projs_splits.json or ~/iit-term-synthesis/lf_projs_splits.json):
    split: list[dict] =
    [
        {
            "project_name": "constructive-geometry",
            "train_files": [
                "problems.v",
                "affinity.v",
                "basis.v",
                "orthogonality.v",
                "part1.v",
                "part3.v",
                "part2.v"
            ],
            "test_files": [],
            "switch": "coq-8.10"
        },
        ...
        ]
"""
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from pycoq.utils import clean_up_filename
from uutils import load_json


@dataclass()
class CoqProj:
    """ Models a single dict element in the X_projs.json file for a single coq project. """
    project_name: str
    train_files: list[str]
    test_files: list[str]
    switch: str
    #  root path to where this coq proj lives & *all& the rest of them live e.g. ~/proverbot9001/coq-projects/
    path_2_coq_projs: str

    # - other names based on coq-gym
    build_command: str = ''  # e.g.         "build_command": "./configure.sh && make"
    build_partition: str = ''  # e.g.         "build_partition": "long"

    # coq_proj_version ... shoould work for the selected coq ver in (opam) switch

    def get_split(self, split: str) -> list[str]:
        if split == 'train':
            return self.train_files
        else:
            return self.test_files

    def is_filename_in_split(self, filename: str, split: str) -> bool:
        split_files: list[str] = self.get_split(split)
        filename = clean_up_filename(filename)
        in_split: bool = any([split_filename in filename for split_filename in split_files])
        return in_split

    def get_coq_proj_path(self) -> str:
        """
        e.g.
            get_coq_proj_path='/dfs/scratch0/brando9/pycoq/pycoq/test/lf'
        """
        return f"{self.path_2_coq_projs / self.project_name}"


# basically entire benchmark
@dataclass
class CoqProjs:
    """Represents the info & coq projs in a X_projects_splits.json in a dataclass. """
    # the actual split info for each coq project/package -- since for each project we need to specify which files are for train & which are for test
    coq_projs: list[CoqProj]
    # root path to where original/raw all coq projects live e.g. proverbot's coq-projects folder
    path_2_coq_projs: Path
    # path to the splits for each coq project
    path_2_coq_projs_json_splits: Path
    # home root used when generating data set
    home_root: Path = str(Path.home())


def list_dict_splits_2_list_splits(coq_projs: list[dict], path_2_coq_projs: Path) -> list[CoqProj]:
    """
    e.g. use
        coq_projs_splits: list[CoqProj] = list_coq_projs_2_list_coq_projs(coq_projs_splits)
    more advanced: https://stackoverflow.com/questions/53376099/python-dataclass-from-a-nested-dict
    """
    path_2_coq_projs: Path = path_2_coq_projs.expanduser()
    path_2_coq_projs: str = str(path_2_coq_projs)
    coq_proj_splits_: list[CoqProj] = []
    for coq_proj in coq_projs:
        coq_proj_split: CoqProj = CoqProj(**coq_proj, path_2_coq_projs=path_2_coq_projs)
        coq_proj_splits_.append(coq_proj_split)
    return coq_proj_splits_


def get_debug_projprojs_meta_data() -> CoqProjs:
    pass


def get_lf_coq_projs_meta_data() -> CoqProjs:
    pass


def get_compcert_coq_projs_meta_data() -> CoqProjs:
    """
    Get data set coq projs info (i.e. meta data) e.g. path2 coq-proj
    """
    # note: the CompCert path sym links to the CompCert in coq_projects
    path_2_coq_projs: Path = Path('~/proverbot9001/coq-projects/').expanduser()  # todo: move to pycoq location
    path_2_coq_projs_json_splits: Path = Path('~/pycoq/compcert_projs_splits.json').expanduser()
    coq_projs: list[dict] = load_json(path_2_coq_projs_json_splits)
    logging.info(f'{coq_projs[0].keys()=}')
    coq_projs: list[CoqProj] = list_dict_splits_2_list_splits(coq_projs, path_2_coq_projs)
    assert len(coq_projs) == 1
    coq_projs_meta_data: CoqProjs = CoqProjs(path_2_coq_projs=path_2_coq_projs,
                                             path_2_coq_projs_json_splits=path_2_coq_projs_json_splits,
                                             coq_projs=coq_projs)
    return coq_projs_meta_data


def get_coqgym_coq_projs_meta_data() -> CoqProjs:
    pass


def get_proj_splits_based_on_name_of_path2data(path2data: Union[Path, str]) -> CoqProjs:
    # expanduser(path2data)
    name_path2data: str = str(path2data)
    if 'pycoq_lf_debug' in name_path2data:
        data_set_meta_data: CoqProjs = get_lf_coq_projs_meta_data()
    elif 'debug_proj' in name_path2data:
        data_set_meta_data: CoqProjs = get_debug_projprojs_meta_data()
    elif 'compcert' in name_path2data:
        data_set_meta_data: CoqProjs = get_compcert_coq_projs_meta_data()
    elif 'coqgym' in name_path2data:
        data_set_meta_data: CoqProjs = get_coqgym_coq_projs_meta_data()
    else:
        raise ValueError(f'Invalid type of data set/benchmark, got (invalid): {name_path2data=}')
    return data_set_meta_data
