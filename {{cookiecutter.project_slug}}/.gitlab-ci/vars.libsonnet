local utils = (import "jpy-utils.libsonnet");
{
  images: {
    release: {
      {{cookiecutter.project_slug}}: {
        creds: {
          host: "quay.io",
          password: "$QUAY_TOKEN",
          username: "{{cookiecutter.project_slug}}+gitlabci",
        },
        repo: "{{cookiecutter.docker_registry}}",
        tag: "${CI_COMMIT_REF_SLUG}-${SHA8}",
        name: utils.docker.containerName(self.repo, self.tag),
        get_name(tag):: utils.docker.containerName(self.repo, tag),
      },
    },
    ci: {
      {{cookiecutter.project_slug}}: {
        creds: {
          host: "quay.io",
          password: "$QUAY_TOKEN",
          username: "{{cookiecutter.project_slug}}+gitlabci",
        },
        repo: "{{cookiecutter.docker_registry}}",
        tag: "ci-${CI_COMMIT_REF_SLUG}-${SHA8}",
        name: utils.docker.containerName(self.repo, self.tag),
        get_name(tag):: utils.docker.containerName(self.repo, tag),
      },
    },
  },
}
