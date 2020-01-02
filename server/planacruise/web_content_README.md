# Directory web_content

Notes describing the ``web_content`` directory

* This directory is located on the [Planacruise web server](http://planacruise.online)
* Static web content is served from this directory by the [Lighttpd server](https://www.lighttpd.net/)
* There is a sub-directory with the name of the identifier of a vessel in the fleet (e.g. ``Trilogy``)
* Content is deployed to this directory by the [content deployment script](https://github.com/smr547/cruise-description/blob/master/grammar/deploy_kml.sh)
* Sub-directories are created manually (at this stage)

## Vessel directory

* The vessel sub-directory has the name of the Vessel identifier
* It contains a sub-directory for each Season specified in ``cdl`` deployed to the web server


## Season Directory

* A sub-directory of the Vessel directory
* Named after the cruise season identifier (e.g. ``Steven_2020``)

Contains:

* Source ``cld`` file in which the Season was described (with filename ``<season_id>.cdl``)
* Google maps ``kml`` file providing a detailed chart of the season (with filename ``<season_id>.kml``)
* Season summary ``html`` file providing a summary of all cruises in the season (with filename ``<season_id>_summary.html``)
* Details of all cruises planned for the Season in a ``pdf`` file (with filename ``<season_id>.pdf`)
