bash runelasticsearch.bash &
python3 add_shared_folders.py
jupyterhub -f /opt/notebooks/jupyterhub_config.py
