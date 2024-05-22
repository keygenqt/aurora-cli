from aurora_cli.src.api.device import (
    device_list_api,
    ssh_device_command_api,
    ssh_device_run_api,
    ssh_device_rpm_install_api,
    ssh_device_upload_api,
    ssh_device_package_remove_api,
)
from aurora_cli.src.api.routes.helper_route import get_route_root, get_arg_bool, get_arg_str, get_arg_int


def search_route_device(route: str) -> bool:
    match get_route_root(route):
        case '/device/list':
            device_list_api(
                verbose=get_arg_bool(route, 'verbose')
            )
        case '/device/ssh/command':
            ssh_device_command_api(
                host=get_arg_str(route, 'host'),
                port=get_arg_int(route, 'port'),
                auth=get_arg_str(route, 'auth'),
                execute=get_arg_str(route, 'execute'),
                verbose=get_arg_bool(route, 'verbose')
            )
        case '/device/ssh/run':
            ssh_device_run_api(
                host=get_arg_str(route, 'host'),
                port=get_arg_int(route, 'port'),
                auth=get_arg_str(route, 'auth'),
                package=get_arg_str(route, 'package'),
                verbose=get_arg_bool(route, 'verbose')
            )
        case '/device/ssh/upload':
            ssh_device_upload_api(
                host=get_arg_str(route, 'host'),
                port=get_arg_int(route, 'port'),
                auth=get_arg_str(route, 'auth'),
                path=get_arg_str(route, 'path'),
                verbose=get_arg_bool(route, 'verbose')
            )
        case '/device/ssh/rpm-install':
            ssh_device_rpm_install_api(
                host=get_arg_str(route, 'host'),
                port=get_arg_int(route, 'port'),
                auth=get_arg_str(route, 'auth'),
                devel_su=get_arg_str(route, 'devel_su'),
                path=get_arg_str(route, 'path'),
                apm=get_arg_bool(route, 'apm'),
                verbose=get_arg_bool(route, 'verbose')
            )
        case '/device/ssh/package-remove':
            ssh_device_package_remove_api(
                host=get_arg_str(route, 'host'),
                port=get_arg_int(route, 'port'),
                auth=get_arg_str(route, 'auth'),
                devel_su=get_arg_str(route, 'devel_su'),
                package=get_arg_str(route, 'package'),
                apm=get_arg_bool(route, 'apm'),
                verbose=get_arg_bool(route, 'verbose')
            )
        case _:
            return False
    return True
