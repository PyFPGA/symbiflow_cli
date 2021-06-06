import pytest
from pathlib import Path
from symbiflow.oci import OCI


@pytest.mark.parametrize(
    'tool, command', [
        ('yosys', 'docker run --rm -v $HOME:$HOME -w $PWD hdlc/ghdl:yosys yosys'),
        ('ghdl', 'docker run --rm -v $HOME:$HOME -w $PWD hdlc/ghdl:yosys ghdl'),
        ('nextpnr-ice40', 'docker run --rm -v $HOME:$HOME -w $PWD hdlc/nextpnr:ice40 nextpnr-ice40'),
        ('nextpnr-ecp5', 'docker run --rm -v $HOME:$HOME -w $PWD hdlc/nextpnr:ecp5 nextpnr-ecp5'),
        ('icepack', 'docker run --rm -v $HOME:$HOME -w $PWD hdlc/icestorm icepack'),
        ('icetime', 'docker run --rm -v $HOME:$HOME -w $PWD hdlc/icestorm icetime'),
        ('iceprog', 'docker run --rm -v $HOME:$HOME -w $PWD --device /dev/bus/usb hdlc/prog iceprog'),
        ('ecppack', 'docker run --rm -v $HOME:$HOME -w $PWD hdlc/prjtrellis ecppack'),
        ('openocd', 'docker run --rm -v $HOME:$HOME -w $PWD --device /dev/bus/usb hdlc/prog openocd')
    ]
)
def test_defaults(tool, command):
    obj = OCI()
    result = obj.get_command(tool)
    assert result == command


@pytest.mark.parametrize(
    'tool, command', [
        ('test1', 'test run --rm -v path1:path2 -v path3:path4 -w . global-option hdlc/test1 alt-test1'),
        ('test2', 'test run --rm -v path1:path2 -v path3:path4 -w . global-option local-option hdlc/test2 alt-test2')
    ]
)
def test_file(tool, command):
    obj = OCI(Path(__file__).parent / 'test.yml')
    result = obj.get_command(tool)
    assert result == command


def test_methods():
    obj = OCI()
    # Defaults for GHDL:
    assert obj.get_command('ghdl') == 'docker run --rm -v $HOME:$HOME -w $PWD hdlc/ghdl:yosys ghdl'
    # Setting a different engine:
    obj.set_engine('podman')
    assert obj.get_command('ghdl') == 'podman run --rm -v $HOME:$HOME -w $PWD hdlc/ghdl:yosys ghdl'
    # Setting different volumes:
    obj.set_volumes(['v1:v1', 'v2:v2'])
    assert obj.get_command('ghdl') == 'podman run --rm -v v1:v1 -v v2:v2 -w $PWD hdlc/ghdl:yosys ghdl'
    # Setting a different work:
    obj.set_work('/tmp')
    assert obj.get_command('ghdl') == 'podman run --rm -v v1:v1 -v v2:v2 -w /tmp hdlc/ghdl:yosys ghdl'
    # Setting a global options:
    obj.set_global_options('--global-option')
    assert obj.get_command('ghdl') == 'podman run --rm -v v1:v1 -v v2:v2 -w /tmp --global-option hdlc/ghdl:yosys ghdl'
    # Setting a new container:
    obj.set_container('ghdl', 'alt-ghdl-container')
    assert obj.get_command('ghdl') == 'podman run --rm -v v1:v1 -v v2:v2 -w /tmp --global-option alt-ghdl-container ghdl'
    # Setting a new tool name:
    obj.set_name('ghdl', 'alt-ghdl-name')
    assert obj.get_command('ghdl') == 'podman run --rm -v v1:v1 -v v2:v2 -w /tmp --global-option alt-ghdl-container alt-ghdl-name'
    # Setting a local options:
    obj.set_local_options('ghdl', '--local-option')
    assert obj.get_command('ghdl') == 'podman run --rm -v v1:v1 -v v2:v2 -w /tmp --global-option --local-option alt-ghdl-container alt-ghdl-name'
