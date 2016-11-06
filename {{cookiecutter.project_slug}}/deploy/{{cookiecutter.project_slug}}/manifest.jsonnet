local kpm = import "kpm.libjsonnet";

function(
  params={}
)

kpm.package({
   package: {
      name: "{{cookiecutter.github_username}}/{{cookiecutter.project_slug}}",
      expander: "jinja2",
      author: "{{cookiecutter.full_name}}",
      version: "{{cookiecutter.version}}-1",
      description: "{{cookiecutter.project_slug}}",
      license: "Apache 2.0",
    },

    variables: {
      namespace: 'default',
      image: "{{cookiecutter.docker_registry}}:v{{cookiecutter.version}}",
      svc_type: "LoadBalancer",
    },

    resources: [
      {
        file: "{{cookiecutter.project_slug}}-dp.yaml",
        template: (importstr "templates/{{cookiecutter.project_slug}}-dp.yaml"),
        name: "{{cookiecutter.project_slug}}",
        type: "deployment",
      },

      {
        file: "{{cookiecutter.project_slug}}-svc.yaml",
        template: (importstr "templates/{{cookiecutter.project_slug}}-svc.yaml"),
        name: "{{cookiecutter.project_slug}}",
        type: "service",
      }
      ],


    deploy: [
      {
        name: "$self",
      },
    ],


  }, params)
