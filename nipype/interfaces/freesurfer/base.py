# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""The freesurfer module provides basic functions for interfacing with
freesurfer tools.

Currently these tools are supported:

     * Dicom2Nifti: using mri_convert
     * Resample: using mri_convert

Examples
--------
See the docstrings for the individual classes for 'working' examples.

"""
__docformat__ = 'restructuredtext'

from builtins import object

import os

from ..base import (CommandLine, Directory,
                    CommandLineInputSpec, isdefined)
from ...utils.filemanip import fname_presuffix


class Info(object):
    """ Freesurfer subject directory and version information.

    Examples
    --------

    >>> from nipype.interfaces.freesurfer import Info
    >>> Info.version()  # doctest: +SKIP
    >>> Info.subjectsdir()  # doctest: +SKIP

    """

    @staticmethod
    def version():
        """Check for freesurfer version on system

        Find which freesurfer is being used....and get version from
        /path/to/freesurfer/build-stamp.txt

        Returns
        -------

        version : string
           version number as string
           or None if freesurfer version not found

        """
        fs_home = os.getenv('FREESURFER_HOME')
        if fs_home is None:
            return None
        versionfile = os.path.join(fs_home, 'build-stamp.txt')
        if not os.path.exists(versionfile):
            return None
        fid = open(versionfile, 'rt')
        version = fid.readline()
        fid.close()
        return version

    @classmethod
    def subjectsdir(cls):
        """Check the global SUBJECTS_DIR

        Parameters
        ----------

        subjects_dir :  string
            The system defined subjects directory

        Returns
        -------

        subject_dir : string
            Represents the current environment setting of SUBJECTS_DIR

        """
        if cls.version():
            return os.environ['SUBJECTS_DIR']
        return None


class FSTraitedSpec(CommandLineInputSpec):
    subjects_dir = Directory(exists=True, desc='subjects directory')


class FSCommand(CommandLine):
    """General support for FreeSurfer commands.

       Every FS command accepts 'subjects_dir' input.
    """

    input_spec = FSTraitedSpec

    _subjects_dir = None

    def __init__(self, **inputs):
        super(FSCommand, self).__init__(**inputs)
        self.inputs.on_trait_change(self._subjects_dir_update, 'subjects_dir')
        if not self._subjects_dir:
            self._subjects_dir = Info.subjectsdir()
        if not isdefined(self.inputs.subjects_dir) and self._subjects_dir:
            self.inputs.subjects_dir = self._subjects_dir
        self._subjects_dir_update()

    def _subjects_dir_update(self):
        if self.inputs.subjects_dir:
            self.inputs.environ.update({'SUBJECTS_DIR':
                                        self.inputs.subjects_dir})

    @classmethod
    def set_default_subjects_dir(cls, subjects_dir):
        cls._subjects_dir = subjects_dir

    @property
    def version(self):
        return Info.version()

    def run(self, **inputs):
        if 'subjects_dir' in inputs:
            self.inputs.subjects_dir = inputs['subjects_dir']
        self._subjects_dir_update()
        return super(FSCommand, self).run(**inputs)

    def _gen_fname(self, basename, fname=None, cwd=None, suffix='_fs',
                   use_ext=True):
        '''Define a generic mapping for a single outfile

        The filename is potentially autogenerated by suffixing inputs.infile

        Parameters
        ----------
        basename : string (required)
            filename to base the new filename on
        fname : string
            if not None, just use this fname
        cwd : string
            prefix paths with cwd, otherwise os.getcwd()
        suffix : string
            default suffix
        '''
        if basename == '':
            msg = 'Unable to generate filename for command %s. ' % self.cmd
            msg += 'basename is not set!'
            raise ValueError(msg)
        if cwd is None:
            cwd = os.getcwd()
        fname = fname_presuffix(basename, suffix=suffix,
                                use_ext=use_ext, newpath=cwd)
        return fname

    @property
    def version(self):
        ver = Info.version()
        if ver:
            if 'dev' in ver:
                return ver.rstrip().split('-')[-1] + '.dev'
            else:
                return ver.rstrip().split('-v')[-1]
