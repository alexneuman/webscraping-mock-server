# print("""
# -----------------------------------------------------------------
# ✨ Hello Tilt! This appears in the (Tiltfile) pane whenever Tilt
#    evaluates this file.
# -----------------------------------------------------------------
# """.strip())
# warn('ℹ️ Open {tiltfile_path} in your favorite editor to get started.'.format(
#     tiltfile_path=config.main_path))
# Run local commands

update_settings(
    k8s_upsert_timeout_secs=300,
)


local_resource('install-helm',
               cmd='which helm > /dev/null || brew install helm',
)

settings = {
    'profile': 'dev',
}
# cli_args = config.parse()
settings.update(read_json(
    "tilt_config.json",
    default = {},
))

# k8s_yaml('cluster-config/k8s/ingress-nginx/01-namespace.yaml')

load('ext://helm_resource', 'helm_resource', 'helm_repo')

# Database

k8s_yaml([
    'helm-charts/database/templates/01-namespace.yaml',
    'helm-charts/database/templates/deployment.yaml',
    'helm-charts/database/templates/service.yaml'
])

k8s_resource(
    'database',
    port_forwards=['5432:5432'],
    auto_init=True,
    trigger_mode=TRIGGER_MODE_AUTO
)

k8s_yaml([
    'helm-charts/backend/templates/01-namespace.yaml',
    'helm-charts/backend/templates/deployment.yaml',
    'helm-charts/backend/templates/service.yaml',
    'helm-charts/backend/templates/ingress.yaml',
    ])

docker_build(
    'backend',
    context='./backend',
    dockerfile='./backend/Dockerfile',
    live_update=[
        sync('./backend/', '/app'),
        run('pip install --no-cache-dir -r requirements.txt', trigger=['./backend/requirements.txt']),
    ],
    build_args={
        'DATABASE_URL': 'postgresql+asyncpg://postgres:postgres@database.database.svc.cluster.local:5432/foo'
    }
    )


# Load Kubernetes YAML

k8s_resource('backend',
             # map one or more local ports to ports on your Pod
             port_forwards=['8000:8000', "5678:5678"],
             # change whether the resource is started by default
             auto_init=False,
             # control whether the resource automatically updates
             trigger_mode=TRIGGER_MODE_AUTO,
             # alter envs
            #  resource_deps=['ingress-nginx-controller', 'cert-manager'],
            
)


docker_build(
    'static-file-server',
    context='./static-file-server',
    dockerfile='./static-file-server/Dockerfile',
    # live_update=[
    #     sync('./static', '/usr/share/nginx/html/static')
    # ]
    )
k8s_yaml([
    'helm-charts/static-file-server/templates/01-namespace.yaml',
    'helm-charts/static-file-server/templates/deployment.yaml',
    'helm-charts/static-file-server/templates/service.yaml',
    'helm-charts/static-file-server/templates/ingress.yaml',
    ])
k8s_resource('static-file-server',
             # map one or more local ports to ports on your Pod
             port_forwards=['8080:80'],
             # change whether the resource is started by default
             auto_init=False,
             # control whether the resource automatically updates
             trigger_mode=TRIGGER_MODE_AUTO,
            #  resource_deps=['ingress-nginx-controller', 'cert-manager'],
)

# Ingress Nginx

helm_resource(
    name='ingress-nginx-controller',
    chart='ingress-nginx/ingress-nginx',
    namespace='ingress-nginx',
    flags=[
        '--create-namespace',

        ],
)

k8s_resource('ingress-nginx-controller',
             # map one or more local ports to ports on your Pod
             port_forwards=['8082:80', '8443:443'],
             # change whether the resource is started by default
             auto_init=False,
             # control whether the resource automatically updates
             trigger_mode=TRIGGER_MODE_AUTO,
            #  resource_deps=['cert-manager'],
)