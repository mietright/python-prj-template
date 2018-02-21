import yaml
from {{cookiecutter.project_slug}}.config import GCONFIG


print(yaml.safe_dump(GCONFIG.settings, indent=2))
