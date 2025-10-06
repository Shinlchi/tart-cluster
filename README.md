## tart-lab — Provision Tart VMs with Ansible

Minimal Ansible project to clone and configure macOS/tart VMs from a base image, in order to quickly spin up a small cluster (e.g., Kubernetes master/worker) or utility VMs.

### Prerequisites
- **macOS** with Apple Hypervisor (Apple Silicon recommended)
- **Tart** installed and available in the `PATH`
- **Ansible** 2.13+ (or newer)

### How to
1) Verify Tart and Ansible are installed and that the base image exists:
```bash
tart --version
ansible --version
```
2) Run the playbooks:
```bash
ansible-playbook playbooks/prepare.yml
ansible-playbook playbooks/deploy.yml
ansible-playbook playbooks/configure.yml -i inventory/cluster.yml
ansible-playbook playbooks/stop.yml
ansible-playbook playbooks/remove.yml
```

### To do
- manage the fleet IPs
- cloud-init for the SSH key
- initial test bench