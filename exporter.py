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
@click.option(
    '--template',
    required = True,
    nargs = 1,
    type = click.File(mode = 'r'),
    help = "File with overpass query template"
)
@click.option(
    '--values',
    type = click.File(mode = 'r'),
    help = "File with overpass query substitution values"
)
@click.option(
    '--defaults',
    type = click.File(mode = 'r'),
    help = "File with default values for overpass query template"
)
@click.option(
    '--bbox',
    type = click.STRING,
    help = "OSM bounding box string"
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
           defaults,
           bbox,
           out,
           verbose):

    # Unfortunate sequence of if/else statements
    if defaults and values:
        values_dict = yaml.safe_load(defaults)
        values_dict.update(yaml.safe_load(values))
    elif values:
        values_dict = yaml.safe_load(values)
    elif defaults:
        values_dict = yaml.safe_load(defaults)
    else:
        print("Substition values for query template required: use the defaults, set your own values or both.")
        return

    if bbox:
        values_dict["bbox"] = bbox

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
