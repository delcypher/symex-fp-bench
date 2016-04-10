import yaml

if hasattr(yaml, 'CLoader'):
  # Use libyaml which is faster
  _loader = yaml.CLoader
else:
  _loader = yaml.Loader

def loadYaml(openFile):
  return yaml.load(openFile, Loader=_loader)

