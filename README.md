## tart-lab — Provision de VMs Tart avec Ansible

Projet Ansible minimaliste pour cloner et configurer des VMs macOS/tart à partir d'une image de base, afin de monter rapidement un petit cluster (ex: Kubernetes master/worker) ou des VMs utilitaires.

### Prérequis
- **macOS** avec l'hyperviseur Apple (Apple Silicon recommandé)
- **Tart** installé et accessible dans le `PATH`
- **Ansible** 2.13+ (ou plus récent)

### How to
1) Vérifiez que Tart et Ansible sont installés et que l'image de base existe:
```bash
tart --version
ansible --version
```
2) Lancez le playbook:
```bash
ansible-playbook playbooks/prepare.yml
ansible-playbook playbooks/deploy.yml
ansible-playbook playbooks/configure.yml -i inventory/cluster.yml
ansible-playbook playbooks/stop.yml
ansible-playbook playbooks/remove.yml
```

### To do
gérer les ip du parc
cloud init pour la clef ssh
banc de test initiale