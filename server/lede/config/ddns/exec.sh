# /bin/bash

source {{ param_common_sh }}
role_name={{ param_role_name }}
role_config_types="service"
prune_list_by_types