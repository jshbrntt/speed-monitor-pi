FROM python:3.10-slim@sha256:f2ee145f3bc4e061f8dfe7e6ebd427a410121495a0bd26e7622136db060c59e0 AS ansible

RUN apt-get update && \
apt-get install --no-install-recommends --yes \
openssh-client=1:8.4p1-5*

RUN python -m pip install ansible \
&& ansible-galaxy collection install \
ansible.posix:1.4.0 \
community.general:5.7.0

WORKDIR /root/playbook

ENTRYPOINT ["ansible-playbook"]
CMD ["-i", "inventory.yaml", "playbook.yaml"]