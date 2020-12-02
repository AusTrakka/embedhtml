# embedhtml

Utility to embed/extract HTML content in Anvil YAML files. 

Run `python embedhtml --help` for usage.

The `extract` command searches the yaml file for key-value pairs where the key contains the string "html" (with any case) and saves the corresponding text value to a file. 
This will extract, for instance, `['native_deps']['head_html']` from anvil.yaml, or `['container']['properties']['html']` from a component UI template. 
The extracted html file name will reflect the origin yaml file name as well as the sequence of indices used to locate the node in the yaml tree.

Note this uses yaml's FullLoader, which in principle can execute malicious code if you run it against a malicious yaml file.
