from .logging import notify

path_to_cwltool = 'cwl-runner'
default_server_url = 'http://127.0.0.1:5000'
process_call = [path_to_cwltool]

try:
    import makeitso_local_config

    path_to_cwltool = makeitso_local_config.path_to_cwltool
    default_server_url = makeitso_local_config.default_server_url
    if hasattr(makeitso_local_config, 'process_call'):
        process_call = makeitso_local_config.process_call

except ImportError:
    notify('no local config file (makeitso_local_config cannot be imported)')
