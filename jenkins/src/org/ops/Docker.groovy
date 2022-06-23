#!/usr/bin/env groovy
package org.ops

def build() {
    sh "echo ${param}"
    env.param_project_context = Util.ofPath(env.param_project_root, env.param_project_module)
    env.param_release_version = params.param_branch
    env.param_release_name = Util.ofPath(
            env.param_registry_repo,
            env.param_registry_dir,
            Util.isEmpty(env.param_release_name)
            ? Util.join("-",env.param_project_name, env.param_project_module)
            : env.param_release_name
    )
    env.param_docker_context = env.param_docker_context == null
                             ? env.param_project_context
                             : Util.ofPath(env.param_project_root,env.param_docker_context)
    env.param_docker_file = Util.ofPath(env.param_docker_context,"Dockerfile")

    tool = [
      java: {
        env.JAVA_HOME = "${tool 'jdk-17'}"
        env.PATH = "${JAVA_HOME}/bin:${PATH}"
      },
      go: {
        env.GO_HOME = "${tool 'go-v1.18.2'}"
        env.GOPROXY = env.param_go_proxy
        env.GOCACHE = env.param_go_cache
        env.GOSUMDB = "off"
        env.GOMODCACHE = env.param_go_mod_cache
        env.CGO_ENABLED = "0"
        env.PATH = "${GO_HOME}/bin:${PATH}"
      },
      web: {
        env.NODEJS_HOME = "${tool 'node-v16.14.0'}"
        env.PATH = "${NODEJS_HOME}/bin:${PATH}"
      }
    ]
    cmd = [
      java: {
        tool.get("java").call()
        return Util.format(
            "chmod +x {0}/gradlew && {0}/gradlew --gradle-user-home {1} --init-script {2} --build-file {0}/build.gradle {3} -x test --refresh-dependencies",
            env.param_project_root,
            env.param_gradle_user_home,
            env.param_gradle_init_file,
            ["clean", "build"].collect { t -> Util.join(":",env.param_project_module, t) }.join(" ")
        )
      },
      go: {
        tool.get("go").call()
        return Util.format(
           "cd {0};go build -o build main.go;",
           env.param_project_context
        )
      },
      web: {
        tool.get("web").call()
        yarn_cmd = Util.format(
            "yarn --cwd {0} --registry {1} --cache-folder {2}",
            env.param_project_context,
            env.param_npm_repo,
            env.param_yarn_cache
        )
        return Util.format("{0} install --no-lockfile --update-checksums && {0} --ignore-engines build",yarn_cmd)
      },
      shell: {
        if (Util.isNotEmpty(env.param_tools)) {
         env.param_tools.split(",").each{ t -> tool.get(t).call() }
        }
        return Util.format("chmod +x {0};{0}",Util.ofPath(env.param_project_root,env.param_project_shell_file))
      }
    ]
    build_cmd = cmd.get(env.param_code_type).call()
    sh "${build_cmd}"
    sh "docker build --tag ${env.param_release_name}:${env.param_release_version} --file ${env.param_docker_file} ${env.param_docker_context}"
    configFileProvider([configFile(fileId: "docker-config", targetLocation: '.jenkins/docker/config.json')]) {
        sh "docker --config .jenkins/docker/ push ${env.param_release_name}:${env.param_release_version}"
    }
}

return this