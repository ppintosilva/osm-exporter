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
    'template',
    required = True,
    nargs = 1,
    type = click.File(mode = 'r')
    #help = "File with overpass query template"
)
@click.argument(
    'values',
    type = click.File(mode = 'r')
    #help = "File with overpass query substitution values"
)
@click.option(
    '-o',
    '--out',
    type = click.STRING,
    default = "map.osm",
    help = "Output filename with the exported osm data"
)
@click.option(
    '-v',
    '--verbose',
    is_flag = True,
    help = "Print the overpass query request"
)
def export(template,
           values,
           out,
           verbose):
    """
    Export OSM data using overpass query templates.

        TEMPLATE is a file containing a template string with '$'-based substitution. Defines the overpass query and substitution keys.

        VALUES is an yaml-file defining the values for each substition key.
    """
    values_dict = yaml.safe_load(values)

    query = Template(template.read())
    query = query.substitute(values_dict)

    # Query time
    url = "http://overpass-api.de/api/interpreter?data=" + query

    if verbose:
        print url
        print "\n"

    print("\nDownloading OSM data to file '{}'\n...".format(out))

    download_file(url, out)

    print("OK")

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
