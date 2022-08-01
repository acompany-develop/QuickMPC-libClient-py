import pkg_resources
from grpc.tools import protoc

protoc.main(
    (
        "",
        "-I{}".format(pkg_resources.resource_filename('grpc_tools', '_proto')),
        "-I.",
        "--python_out=.",
        "--grpc_python_out=.",
        "./libc_to_manage.proto",
    )
)

protoc.main(
    (
        "",
        "-I.",
        "--python_out=.",
        "./common_types/common_types.proto",
    )
)
