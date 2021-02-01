
import click
import yaml
from pathlib import Path
import re
from .version import __version__

@click.version_option(version=__version__, message="%(version)s")

@click.group()
def cli():
  pass

@cli.command()
@click.argument('filename')
def extract(filename):
  """
  Extract any embedded html strings from FILENAME and store in separate files
  """
  with open(filename) as f:
    contents = yaml.full_load(f)
  read_yaml_element(contents, filename, [])

# TODO: if a dict key looks like a number, we will fail as we'll treat it as a number
@cli.command()
@click.argument('htmlfile')
@click.argument('yamlfile')
def embed(htmlfile, yamlfile):
  """
  Read the contents of HTMLFILE and store in the original node of YAMLFILE.
  This will overwrite YAMLFILE with the edited contents!
  """
  # Read files
  html_path = Path(htmlfile)
  html_string = html_path.read_text()
  with open(yamlfile) as f:
    yaml_contents = yaml.full_load(f)

  # Parse node path through yaml file
  match = re.match("(.+)_(.+)__node__(.+)\.html", html_path.name)
  if not match:
    raise ValueError(f"Cannot parse filename {html_path.name}")
  # TODO: warn if filename doesn't appear to match original
  node_path_string = match.group(3)
  node_path = node_path_string.split('--')
  
  # Modify yaml
  node = yaml_contents
  for index in node_path[:-1]:
    try:
      index = int(index)
      node = node[index]
    except ValueError:
      node = node[index]
  node[node_path[-1]] = html_string

  # Write out yaml
  with open(yamlfile, 'w') as f:
    yaml.dump(yaml_contents, f, sort_keys=False, default_flow_style=None)



def read_yaml_element(node, filepath, yaml_path):
  """Recursively handle a subtree of a yaml file, searching for html elements.

  Args:
      node (dict, list, str, numeric, or bool): subtree of the yaml file to read
      file_path (str): path to the input file
      yaml_path (list): list of keys and indices to reach this node
  
  Returns:
      bool: True if any apparent html-containing element was found
  """
  html_found = False
  # isinstance is better than try..except here as the only iterables we want are lists and dicts
  if isinstance(node, dict):
    for (k,childnode) in node.items():
      if 'html' in k.lower():
        extract_html(childnode, filepath, yaml_path+[k])
        html_found = True
      else:
        if read_yaml_element(childnode, filepath, yaml_path+[k]):
          html_found = True
  elif isinstance(node, list):
    for (i,childnode) in enumerate(node):
      if read_yaml_element(childnode, filepath, yaml_path+[i]):
        html_found = True
  else:
    pass
  return html_found

def extract_html(value, filepath, yaml_path):
  """Extract html and write to a separate file in more readable form.

  The output file will be in the same directory as the input yaml file and
  be of the form <inputbasename>_yaml__node__<path-through-yaml-tree>.html .
  Indices of the path through the yaml tree will be separated by '--'.
  This will cause issues if any key in the path contains the string '--'.

  Args:
      value (str): string containing html
      filepath (str): path to the source yaml file
      yaml_path (list): list of indices to look up this value in the yaml tree
  """
  if not isinstance(value, str):
    raise ValueError(f'Node at {yaml_path} does not seem to be a string')
  path = Path(filepath)
  if not path.is_file():
    raise ValueError(f"Cannot read file {filepath}")
  out_dir = path.parent
  out_prefix = path.stem + '_' + path.suffix[1:]
  yaml_path_string = '--'.join([str(x) for x in yaml_path])
  out_path = Path(out_dir).joinpath(f"{out_prefix}__node__{yaml_path_string}.html")
  print(f"Writing to {out_path}")
  out_path.write_text(value)

if __name__ == '__main__':
  cli()
