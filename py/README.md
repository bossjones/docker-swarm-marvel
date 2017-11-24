# Help

```
 |2.2.3|  using virtualenv: docker-swarm-marvel2  unifi in ~/dev/bossjones/docker-swarm-marvel
± |feature-inital U:6 ?:7 ✗| →  python py/driver.py --help
usage: driver.py [-h] [--list] [--host HOST] [--all] [--droplets] [--regions]
                 [--images] [--sizes] [--ssh-keys] [--domains] [--tags]
                 [--pretty] [--cache-path CACHE_PATH]
                 [--cache-max_age CACHE_MAX_AGE] [--force-cache]
                 [--refresh-cache] [--env] [--api-token API_TOKEN]

Produce an Ansible Inventory file based on DigitalOcean credentials

optional arguments:
  -h, --help            show this help message and exit
  --list                List all active Droplets as Ansible inventory
                        (default: True)
  --host HOST           Get all Ansible inventory variables about a specific
                        Droplet
  --all                 List all DigitalOcean information as JSON
  --droplets, -d        List Droplets as JSON
  --regions             List Regions as JSON
  --images              List Images as JSON
  --sizes               List Sizes as JSON
  --ssh-keys            List SSH keys as JSON
  --domains             List Domains as JSON
  --tags                List Tags as JSON
  --pretty, -p          Pretty-print results
  --cache-path CACHE_PATH
                        Path to the cache files (default: .)
  --cache-max_age CACHE_MAX_AGE
                        Maximum age of the cached items (default: 0)
  --force-cache         Only use data from the cache
  --refresh-cache, -r   Force refresh of cache by making API requests to
                        DigitalOcean (default: False - use cache files)
  --env, -e             Display DO_API_TOKEN
  --api-token API_TOKEN, -a API_TOKEN
                        DigitalOcean API Token
```
