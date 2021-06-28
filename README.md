# Genshin Impact Inventory Reader
Playing around with Computer Vision and Genshin Impact Inventories.
Something to read a Genshin Impact Inventory image and output a JSON.

Uses `easyocr` and `opencv-python`

#### Current Limitations:
- Resolution can affect results (built for 16:9 1080p inventory images)
- Not always accurate, and if a material is found, but if quantity can not be read, it can return it with a `-1`.
- Only supporting 36 materials right now, but easily extensible.
<hr/>

## Want to help add materials?
Submit a pull request with the additions and use 124x152 images for the materials. 
See the current images for an example on what they should look like. 
Also add to the items.json and naming.json files.

<hr/>

## Usage:
`python3 genshinreader.py <image_path>`
### Optional arguments:
#### Resolution:
- Resolution of image items relative to actual game resolution.
- Usage:  `-r`/`--res` `<resolution>`
- Default: `1080`
#### Include Failed:
- Whether to include `material: quantity` where the quantity could not be read.
- Usage: `-if`/`--include-failed` `<include_failed>`
- Default: `True`

## What are all the version numbers?:
Engine Version: `name:major.minor.revision`
- Version of the image reading system for Genshin Reader.

List Version: `name:major.minor.revision`
- Version of list of images to pull from for template matching.

Naming Scheme: `scheme:[version]`
- Version: `major.minor.revision`
- Naming scheme and version of output names for materials.

## Example:
### Example Input Image: 
![Example Input Image](https://files.timothyji.com/projects/genshin-reader/ex.png)
### Example Output:
```
{
  "engine-version": "genshinreader:1.0.0",
  "list-version": "genshinreader:0.2.0",
  "naming-scheme": "default:0.2.0",
  "materials": {
    "heros-wit": 286,
    "adventurers-experience": 90,
    "wanderers-advice": 24,
    "slime-concentrate": 56,
    "slime-secretions": 205,
    "slime-condensate": 1002,
    "ominous-mask": 38,
    "stained-mask": 73,
    "damaged-mask": 796,
    "forbidden_curse-scroll": 37,
    "sealed-scroll": 126,
    "divining-scroll": 719,
    "weathered-arrowhead": 30,
    "sharp-arrowhead": 55,
    "firm-arrowhead": 562,
    "black_crystal-horn": 21,
    "black_bronze-horn": 138,
    "heavy-horn": 733,
    "leyline-sprout": -1,
    "dead-leyline-leaves": 66,
    "dead-leyline-branch": 298,
    "chaos-core": 25,
    "chaos-circuit": 72,
    "chaos-device": 328,
    "mistgrass-wick": 21,
    "mistgrass": 80,
    "mistgrass-pollen": 356,
    "inspectors-sacrificial_knife": 10
  }
}
```
