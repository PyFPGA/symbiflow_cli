from symbiflow.symbiflow import SymbiFlow


def gen_file(filename, default, families, packages):
    obj = SymbiFlow(part=default, outdir='_build')
    obj.synthesis('Blink', ['../resources/vhdl/blink.vhdl'])
    with open('{}.txt'.format(filename), 'w') as file:
        for family in families:
            parts = []
            for package in packages:
                part = "{}-{}".format(family, package)
                obj.set_part(part)
                try:
                    obj.pnr()
                    parts.append(part)
                except:
                    print('Unsupported part {}'.format(part))
            parts.sort()
            file.write('* ``{}``\n'.format('`` ``'.join(parts)))

#
# ice40
#

# From <nextpnr>/ice40/main.cc and http://www.clifford.at/icestorm/

families = [
    'lp384', 'lp1k', 'lp4k', 'lp8k', 'hx1k', 'hx4k', 'hx8k',
    'up3k', 'up5k', 'u1k', 'u2k', 'u4k'
]

packages = [
    'swg16tr', 'uwg30', 'cm36', 'cm49', 'cm81', 'cm121', 'cm225', 'qn32',
    'sg48', 'qn84', 'cb81', 'cb121', 'cb132', 'vq100', 'tq144', 'bg121', 'ct256'
]

gen_file('ice40', 'hx8k-ct256', families, packages)

#
# ecp5
#

# From <nextpnr>/ecp5/main.cc and https://github.com/YosysHQ/prjtrellis-db/blob/master/devices.json

families = [
    '12k', '25k', '45k', '85k', 'um-25k', 'um-45k', 'um-85k',
    'um5g-25k', 'um5g-45k', 'um5g-85k'
]

packages = ['csfBGA285', 'caBGA256', 'caBGA381', 'caBGA554', 'caBGA756']

gen_file('ecp5', '12k-csfBGA285', families, packages)
