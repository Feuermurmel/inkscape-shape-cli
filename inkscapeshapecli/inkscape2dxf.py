import argparse
import os
import shutil
import sys
import tempfile

from . import util, dxfexport, inkscape


def regularize_svg_document(path):
    """
    Opens a file with Inkscape and converts all objects to paths.
    """
    command_line = inkscape.InkscapeCommandLine(path)
    layers = command_line.layers

    command_line.apply_to_document('LayerUnlockAll', 'LayerShowAll')

    layer_copies = []

    for i in layers:
        layer_copy = command_line.duplicate_layer(i)
        layer_copies.append(layer_copy)

        command_line.apply_to_layer_content(layer_copy, 'ObjectToPath')
        command_line.apply_to_layer_content(layer_copy, 'SelectionUnGroup')

        if not i.use_paths:
            command_line.apply_to_layer_content(layer_copy, 'StrokeToPath')
            command_line.apply_to_layer_content(layer_copy, 'SelectionUnion')

    for original, copy in zip(layers, layer_copies):
        command_line.clear_layer(original)
        command_line.move_content(copy, original)
        command_line.delete_layer(copy)

    command_line.apply_to_document('FileSave', 'FileClose', 'FileQuit')

    command_line.run()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('in_path')
    parser.add_argument('out_path', nargs='?')
    parser.add_argument('-f', '--flatness', type=float, default=0.2)

    return parser.parse_args()


def main(in_path, out_path, flatness):
    if out_path is None:
        base_name, _ = os.path.splitext(in_path)
        out_path = f'{base_name}.dxf'

    layers = inkscape.get_inkscape_layers(in_path)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_svg_path = os.path.join(temp_dir, os.path.basename(in_path))

        shutil.copyfile(in_path, temp_svg_path)

        regularize_svg_document(temp_svg_path)

        export_effect = dxfexport.DXFExportEffect(layers, flatness)
        export_effect.affect(args=[temp_svg_path], output=False)

    export_effect.write_dxf(out_path)


def script_main():
    try:
        main(**vars(parse_args()))
    except util.UserError as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(2)
