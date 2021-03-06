# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..convert import VtkStreamlines


def test_VtkStreamlines_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    colourorient=dict(argstr='-colourorient',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    in_file=dict(argstr=' < %s',
    mandatory=True,
    position=-2,
    ),
    inputmodel=dict(argstr='-inputmodel %s',
    usedefault=True,
    ),
    interpolate=dict(argstr='-interpolate',
    ),
    interpolatescalars=dict(argstr='-interpolatescalars',
    ),
    out_file=dict(argstr='> %s',
    genfile=True,
    position=-1,
    ),
    scalar_file=dict(argstr='-scalarfile %s',
    position=3,
    ),
    seed_file=dict(argstr='-seedfile %s',
    position=1,
    ),
    target_file=dict(argstr='-targetfile %s',
    position=2,
    ),
    terminal_output=dict(nohash=True,
    ),
    voxeldims=dict(argstr='-voxeldims %s',
    position=4,
    units='mm',
    ),
    )
    inputs = VtkStreamlines.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value


def test_VtkStreamlines_outputs():
    output_map = dict(vtk=dict(),
    )
    outputs = VtkStreamlines.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
