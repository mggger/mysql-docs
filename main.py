import yaml
from rstformat import RstFormat
from scan import Scan


if __name__ == '__main__':
    with open('config.yml', 'rb') as f:
        config = yaml.load(f)

    _scan = Scan(config)
    _scan.process()

    prefix = config['prefix']

    for table in _scan.table_info:
        rst = RstFormat(table, prefix=prefix)
        rst.to_rst()
