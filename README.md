## tart-lab — Provision de VMs Tart avec Ansible

Projet Ansible minimaliste pour cloner et configurer des VMs macOS/tart à partir d'une image de base, afin de monter rapidement un petit cluster (ex: Kubernetes master/worker) ou des VMs utilitaires.

### Prérequis
- **macOS** avec l'hyperviseur Apple (Apple Silicon recommandé)
- **Tart** installé et accessible dans le `PATH`
- **Ansible** 2.13+ (ou plus récent)

### Structure du projet
- `ansible.cfg` : configuration d'Ansible (inventaire, rôles, callbacks)
- `inventory/localhost.yml` : inventaire local, exécution sur `localhost`
- `inventory/group_vars/all.yml` : variables globales (image de base `base_image`, liste `vms`)
- `playbooks/create_vms.yml` : playbook principal pour créer/configurer les VMs
- `roles/tart_vm/` : rôle Ansible
  - `tasks/clone.yml` : clonage des VMs depuis l'image de base via `tart clone`
  - `tasks/set.yml` : configuration CPU/Mémoire via `tart set`
  - `tasks/main.yml` : point d'entrée des tâches du rôle
  - `tasks/run.yml` : démarrage des VMs et affichage de leur IP

### Variables
Fichier: `inventory/group_vars/all.yml`

```yaml
base_image: ubuntu-base
vms:
  - { name: "k8s-master",  cpu: 2, memory: 2048 }
  - { name: "k8s-worker1", cpu: 2, memory: 2048 }
  - { name: "k8s-worker2", cpu: 2, memory: 2048 }
  - { name: "root-ca",     cpu: 1, memory: 512  }
```

- **base_image**: nom de l'image Tart source (ex. `tart images`).
- **vms**: liste des VMs à créer avec ressources CPU/Mémoire (MiB).

Note: Les tâches `clone` et `set` conditionnent leur exécution sur `existing_vms` si défini. Par défaut (non fourni), toutes les VMs listées seront traitées.

### Exécution
1) Vérifiez que Tart et Ansible sont installés et que l'image de base existe:
```bash
tart --version
tart list
ansible --version
```

2) Adaptez `inventory/group_vars/all.yml` selon vos besoins (nom d'image, VMs, ressources).

3) Lancez le playbook:
```bash
ansible-playbook -i inventory/localhost.yml playbooks/create_vms.yml
```

Le rôle:
- Clonera chaque VM via `tart clone <base_image> <vm.name>`
- Réglera CPU/Mémoire via `tart set <vm.name> --cpu <cpu> --memory <memory>`
- Démarrera les VMs et affichera leurs adresses IP via `tart ip <vm.name>`

### Inventaire et exécution locale
L'inventaire `inventory/localhost.yml` force l'exécution locale avec Python 3, ce qui convient à un flux où Ansible orchestre des commandes `tart` en local.

### Dépannage
- "command not found: tart": installez Tart et/ou ajoutez-le au `PATH`.
- "image not found": vérifiez `base_image` et la sortie de `tart images`.
- Droits/permissions: exécutez depuis un utilisateur ayant accès à l'hyperviseur.

### Notes Ansible (format de sortie et dépréciations)
- Le projet utilise le callback par défaut avec `result_format=yaml` pour un affichage YAML propre (voir `ansible.cfg`).
- Les avertissements de dépréciation sont désactivés (`deprecation_warnings=False`). Si vous souhaitez les voir, supprimez/ajustez ce paramètre.

### Évolutions possibles
- Détection automatique d'`existing_vms` (ex. via `tart list`) pour éviter de retraiter les VMs déjà présentes.
- Ajout de tâches pour démarrer/arrêter, config réseau, attacher disques, provisioning cloud-init/SSH.

### Licence
MIT (ou à préciser).


