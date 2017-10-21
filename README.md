# docker-swarm-marvel
ansible playbooks, scripts, and docker-compose files based on marvel comics locations. Use with digital ocean. Based on https://github.com/bossjones/docker-swarm-vbox-lab


```
pip install --ignore-installed --pre "https://github.com/pradyunsg/pip/archive/hotfix/9.0.2.zip#egg=pip" \
    && pip install --upgrade setuptools==36.0.1 wheel==0.29.0
```

# Regarding firewalls, remember this!!!

```
# icmp no PORT DEFINED

--outbound-rules "protocol:icmp,address:0.0.0.0/0,address:::/0 protocol:tcp,ports:all,address:0.0.0.0/0,address:::/0 protocol:udp,ports:all,address:0.0.0.0/0,address:::/0"
```
