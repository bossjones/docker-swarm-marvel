Role Name
=========

Creates a Digital Ocean droplet and adds it to dynamic inventory

Role Variables
--------------

- DO_API_TOKEN is access token
- name is droplet name
- droplet_groups is ansible groups for this droplet
- `inventory_to_update` inventory

Example Playbook
----------------

Create inventory like this

    [digitalocean]
    locaalhost ansible_connection=local ansible_python_interpreter=python3.6

In file group_vars/all put token

    ---
    # file: group_vars/all
    DO_API_TOKEN: 'put token'

And

    ---
    # file: group_vars/digitalocean
    name: buildbot
    droplet_groups: buildbots
    inventory_to_update: production

How to use role:

    - hosts: digitalocean
      roles:
         - ysz.droplet

Then run

    ansible-playbook -i digitalocean yourplaybook.yml

License
-------

BSD
