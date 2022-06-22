#!/usr/bin/env groovy
package org.ops

def build() {
    // prepare
    configFileProvider([configFile(fileId: "${env.param_global_env_file_id}", targetLocation: '.ci/global.env')]) {
        load ".ci/global.env";
    }
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
    env.JAVA_HOME = "${tool 'jdk-17'}"
    env.GO_HOME = "${tool 'go-v1.18.2'}"
    env.NODEJS_HOME = "${tool 'node-v16.14.0'}"
    env.GOPROXY = env.param_go_proxy
    env.GOCACHE = env.param_go_cache
    env.GOSUMDB = "off"
    env.GOMODCACHE = env.param_go_mod_cache
    env.CGO_ENABLED = "0"
    env.PATH = "${JAVA_HOME}/bin:${GO_HOME}/bin:${NODEJS_HOME}/bin:${PATH}"

    build_cmd = ""
    switch (env.param_code_type) {
        case "java":
            build_cmd = Util.format(
                "chmod +x {0}/gradlew && {0}/gradlew --gradle-user-home {1} --init-script {2} --build-file {0}/build.gradle {3} -x test --refresh-dependencies",
                env.param_project_root,
                env.param_gradle_user_home,
                env.param_gradle_init_file,
                ["clean", "build"].collect { t -> Util.join(":",env.param_project_module, t) }.join(" ")
            )
            break;
        case "go":
            build_cmd = Util.format(
               "cd {0};go build -o build main.go;",
               env.param_project_context
            )
            break;
        case "python":
            break;
        case "web":
            yarn_cmd = Util.format(
                "yarn --cwd {0} --registry {1} --cache-folder {2}",
                env.param_project_context,
                env.param_npm_repo,
                env.param_yarn_cache
            )
            build_cmd = Util.format("{0} install --no-lockfile --update-checksums && {0} --ignore-engines build",yarn_cmd)
            break;
        case "shell":
            build_cmd = Util.format("chmod +x {0};{0}",Util.ofPath(env.param_project_root,env.param_project_shell_file))
        default:
            println(env.param_code_type + " not config" as String);
            return;
    }
    sh "${build_cmd}"
    sh "docker build --tag ${env.param_release_name}:${env.param_release_version} --file ${env.param_docker_file} ${env.param_docker_context}"
    configFileProvider([configFile(fileId: "docker-config", targetLocation: '.ci/docker/config.json')]) {
        sh "docker --config .ci/docker/config.json push ${env.param_release_name}:${env.param_release_version}"
    }
}

return this