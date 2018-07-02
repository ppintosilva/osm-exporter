# osm-exporter
Export data from OpenStreetMap using a template overpass query
---

**What is this?** - A small python CLI script to help you export OSM data using pre-defined overpass query templates.

**What osm-exporter is not for:** - Downloading OSM data using a non-template query. If you've already defined a overpass query then you can simply [get the osm data using the command line](http://overpass-api.de/command_line.html). If you think the query can be re-used (e.g. different bbox), turn it into a template instead.

## Installation

Just run ```pip install -r requirements``` in your **virtualenv**.

## Usage

```
python exporter.py --help

Usage: exporter.py [OPTIONS] TEMPLATE VALUES

  Export OSM data using overpass query templates.

      TEMPLATE is a file containing a template string with '$'-based
      substitution. Defines the overpass query and substitution keys.

      VALUES is an yaml-file defining the values for each substitution key.

Options:
  -o, --out TEXT  Output filename with the exported osm data
  -v, --verbose   Print the overpass query request
  --help          Show this message and exit.
```

### Example - Downloading OSM data for the [roads template](templates/roads)

My use case consisted of using OSM data to build the road graph for a region of the U.K. In addition to roads, I wanted to include the location of traffic signals and bus stops. After developing and testing my overpass query on [overpass turbo](https://overpass-turbo.eu/), I came up with the following [query template](templates/roads/query):

```
[bbox:$bbox]
[timeout:$timeout]
[out:$outformat]
;
(
  node
    ["highway"]
    $node_filters
    ;

  way
    ["highway"]
    $way_filters
    ;
);
out;
>;
out skel qt;
```

The default substitution values are defined on the corresponding [defaults file](templates/roads/defaults.yml):
``` yaml
bbox: "54.84,-1.86,55.18,-1.32"
timeout: 120
outformat: json

node_filters: |-
  // Unfortunate but necessary indentation
      ["highway"~"traffic_signals|bus_stop"]

way_filters: |-
  // Unfortunate but necessary indentation
      ["highway"!="track"]
      ["highway"!="bus_guideway"]
      ["highway"!="escape"]
      ["highway"!="raceway"]
      ["highway"!="road"]
      ["highway"!="pedestrian"]
      ["highway"!="footway"]
      ["highway"!="bridleway"]
      ["highway"!="steps"]
      ["highway"!="path"]
      ["highway"!="cycleway"]
      ["highway"!="construction"]
```

Notice that I could have created a template which used the values of $node_filters and $way_filters directly, but instead decided on a more generic template. You can copy the defaults into a new file and redefine any of these variables. Using new values for $timeout and $outformat, and a smaller bounding box, the final query looks like this:
```
[bbox:54.972047139106,-1.625311374664,54.979861000731,-1.6177690029144]
[timeout:15]
[out:xml]
;
(
  node
    ["highway"]
    ["highway"~"traffic_signals|bus_stop"]
    ;

  way
    ["highway"]
    ["highway"!="track"]
    ["highway"!="bus_guideway"]
    ["highway"!="escape"]
    ["highway"!="raceway"]
    ["highway"!="road"]
    ["highway"!="pedestrian"]
    ["highway"!="footway"]
    ["highway"!="bridleway"]
    ["highway"!="steps"]
    ["highway"!="path"]
    ["highway"!="cycleway"]
    ["highway"!="construction"]
    ;
);
out;
>;
out skel qt;
```

You can try the final query at [overpass turbo](https://overpass-turbo.eu/), or use it directly with **osm-exporter**:

```
python exporter.py \
  templates/roads/query \
  templates/roads/defaults.yml \
  --verbose
```

## [Moar](https://www.urbandictionary.com/define.php?term=moar) templates

You can contribute to **osm-exporter** by creating new overpass query templates and adding them to the templates folder:

- **Fork** this repository
- Write your **template** (and defaults.yml)
- Submit a **pull request**
