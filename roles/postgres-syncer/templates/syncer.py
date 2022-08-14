from subprocess import PIPE, Popen
import yaml
from pprint import pprint

config = yaml.loads(open("/etc/postgres-sync/sync.yml").read())

print("Running syncer")
pprint(config)