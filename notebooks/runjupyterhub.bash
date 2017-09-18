python3 add_shared_folders.py
python3 public_server.py &
service ssh start &     
jupyterhub -f /opt/notebooks/jupyterhub_config.py
