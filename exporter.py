import yaml
import click
import os
import sys
import requests
from string import Template

#
#
#

@click.command()
@click.argument(
    'query-values',
    required = False,
    nargs = 1,
    type = click.File(mode = 'r')
)
@click.option(
    '-o',
    '--out_filename',
    type = click.STRING,
    default = "map.osm",
    help = "Output filename containing osm data"
)
@click.option(
    '-v',
    '--verbose',
    is_flag = True,
    help = "Print query"
)
def export(query_values, out_filename, verbose):

    # Load defaults
    try:
        defaults_file = open("query.defaults.yml", "r")
    except IOError:
        print("Can't open the file 'query.defaults.yml'. Have you deleted or moved this file?")
        return
    # Get defaults into dictionary
    values_dict = yaml.safe_load(defaults_file)

    if query_values:
        # Get dictionary from yml file with values necessary for query
        user_vars_dict = yaml.safe_load(query_values)
        values_dict.update(user_vars_dict)

    # Load template file
    try:
        query = open("overpass.query.template", "r")
    except IOError:
        print("Can't open the file 'overpass.query.template'. Have you deleted or moved this file?")
        return

    query = Template(query.read())
    query = query.substitute(values_dict)

    # if verbose:
    #     print query

    url = "http://overpass-api.de/api/interpreter?data=" + query

    if verbose:
        print url

    download_file(url, out_filename)

    print("OSM data downloaded and saved to file {}".format(out_filename))

    return # the end

#
#
#

# Kindly adapted from: https://stackoverflow.com/a/16696317
def download_file(url, out_filename):
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(out_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
#
#
#

if __name__ == "__main__":
    if os.getuid() == 0:
	    sys.exit("Do not run this script as root.")
    export()
