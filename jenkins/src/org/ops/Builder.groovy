package org.ops

import org.ops.util.PathUtils
import org.ops.util.StringUtils

def exec(Map inputs) {
    def configFiles = []
    def toolMap = [
            java  : {
                env.JAVA_HOME = tool inputs.param_tool_java_version
                env.PATH = "${PATH}:${JAVA_HOME}/bin"
            },
            maven : {
                env.MAVEN_HOME = tool inputs.param_tool_maven_version
                env.PATH = "${PATH}:${MAVEN_HOME}/bin"

                def configId = inputs.param_maven_config_env ? "${inputs.param_maven_config_env}-mvn.config" : 'mvn.config'
                configFiles.add(configFile(fileId: configId, variable: 'CONFIG_FILE_MAVEN'))
            },
            gradle: {
                env.GRADLE_HOME = tool inputs.param_tool_gradle_version
                env.PATH = "${PATH}:${GRADLE_HOME}/bin"

                def configId = inputs.param_gradle_config_env ? "${inputs.param_gradle_config_env}-gradle.config" : 'gradle.config'
                configFiles.add(configFile(fileId: configId, variable: 'CONFIG_FILE_GRADLE'))
            },
            golang: {
                env.GO_HOME = tool inputs.param_tool_golang_version
                env.GOPROXY = inputs.param_go_proxy
                env.GOSUMDB = "off"
                env.CGO_ENABLED = "0"
                env.PATH = "${PATH}:${GO_HOME}/bin"
            },
            nodejs: {
                env.NODEJS_HOME = tool inputs.param_tool_nodejs_version
                env.PATH = "${PATH}:${NODEJS_HOME}/bin"
            },
            dotnet: {
                env.DOTNET_HOME = tool inputs.param_tool_dotnet_version
                env.DOTNET_SYSTEM_GLOBALIZATION_INVARIANT = 1
                env.PATH = "${PATH}:${DOTNET_HOME}"

                def configId = inputs.param_nuget_config_env ? "${inputs.param_nuget_config_env}-nuget.config" : 'nuget.config'
                configFiles.add(configFile(fileId: configId, variable: 'CONFIG_FILE_NUGET'))
            },
            sonarqube: {
                env.SONARQUBE_HOME = tool inputs.param_tool_sonarqube_version
                env.PATH = "${PATH}:${SONARQUBE_HOME}/bin"
            }
    ]

    def sonarCmdPrefix = StringUtils.format(
            "sonar-scanner -Dsonar.projectKey=${inputs.param_sonarqube_project_key} -Dsonar.projectVersion=${inputs.param_release_version} -Dsonar.projectBaseDir={0} -Dsonar.sources=.",
            inputs.param_project_root
    )

    def codeMap = [
        [
            name: 'java',
            func: {
                if ("mvn" == inputs.param_java_build_tool || fileExists("${inputs.param_project_root}/pom.xml")) {
                    inputs.param_java_build_phase = StringUtils.defaultIfEmpty(inputs.param_java_build_phase, "clean install -Dmaven.test.skip=true")
                    
                    sh "mvn -B -U -e -s ${CONFIG_FILE_MAVEN} -f ${inputs.param_project_root}/pom.xml ${inputs.param_java_build_phase}"
                    if (params.param_code_analysis == true) {
                        withSonarQubeEnv(inputs.param_sonarqube_server) {
                            sh "mvn -B -s ${CONFIG_FILE_MAVEN} -f ${inputs.param_project_root}/pom.xml org.sonarsource.scanner.maven:sonar-maven-plugin:sonar -Dsonar.projectKey=${inputs.param_sonarqube_project_key} -Dsonar.projectVersion=${inputs.param_release_version} -Dsonar.host.url=${SONAR_HOST_URL} -Dsonar.token=${SONAR_AUTH_TOKEN}"
                        }
                    }
                } else {
                    inputs.param_java_build_phase = StringUtils.defaultIfEmpty(inputs.param_java_build_phase, "clean build -U -x test")

                    sh "gradle --no-daemon -Pdevelopment=false -I ${CONFIG_FILE_GRADLE} -p ${inputs.param_project_root} ${inputs.param_java_build_phase}"
                    if (params.param_code_analysis == true) {
                        withSonarQubeEnv(inputs.param_sonarqube_server) {
                            sh "gradle --no-daemon -Pdevelopment=false -I ${CONFIG_FILE_GRADLE} -p ${inputs.param_project_root} sonar -Dsonar.projectKey=${inputs.param_sonarqube_project_key} -Dsonar.projectName=${inputs.param_sonarqube_project_key} -Dsonar.projectVersion=${inputs.param_release_version} -Dsonar.host.url=${SONAR_HOST_URL} -Dsonar.token=${SONAR_AUTH_TOKEN}"
                        }
                    }
                }
            },
            tool: {
                return [
                    'java', 
                    "mvn" == inputs.param_java_build_tool || fileExists("${inputs.param_project_root}/pom.xml") ? 'maven' : 'gradle',
                    'nodejs'
                ]
            }
        ],
        [
            name: 'go',
            func: {
                sh "cd ${inputs.param_project_root};go build -o build main.go;"
            },
            tool: {
                return ['golang']
            }
        ],
        [
            name: 'web',
            func: {
                sh "pnpm_config_registry=${inputs.param_npm_repo} pnpm --dir ${inputs.param_project_root} install && pnpm --dir ${inputs.param_project_root} run build"
                if (params.param_code_analysis == true) {
                    withSonarQubeEnv(inputs.param_sonarqube_server) {
                        def cmd = StringUtils.format("{0}", sonarCmdPrefix)
                        sh "${cmd}"
                    }
                }
            },
            tool: {
                return ['nodejs']
            }
        ],
        [
            name: 'dotnet',
            func: {
                if (params.param_code_analysis == true) {
                    withSonarQubeEnv(inputs.param_sonarqube_server) {
                        sh "dotnet new tool-manifest --force"
                        sh "dotnet tool install dotnet-sonarscanner --configfile ${CONFIG_FILE_NUGET}"
                        sh "(cd ${inputs.param_project_root};dotnet tool run dotnet-sonarscanner begin /k:${inputs.param_sonarqube_project_key} /v:${inputs.param_release_version} /d:sonar.host.url=${SONAR_HOST_URL} /d:sonar.token=${SONAR_AUTH_TOKEN} /d:sonar.scanner.scanAll=false)"
                    }
                }
                sh "(cd ${inputs.param_project_root} && rm -rf bin build && dotnet publish --configfile ${CONFIG_FILE_NUGET} -c Release -r linux-x64 -p:DebugType=None -p:DebugSymbols=false)"
                if (params.param_code_analysis == true) {
                    withSonarQubeEnv(inputs.param_sonarqube_server) {
                        sh "(cd ${inputs.param_project_root};dotnet tool run dotnet-sonarscanner end /d:sonar.token=${SONAR_AUTH_TOKEN})"
                    }
                }
            },
            tool: {
                return ['dotnet']
            }
        ],
        [
            name: 'python',
            func: {
                sh "(cd ${inputs.param_project_root} && rm -rf build && mkdir -p build && find app -name '*.py' | xargs -I {} cp -rv --parents {} build/ && cp -rv main.py requirements.txt config/ build/)"
            }
        ],
        [
            name: 'shell',
            func: {
                def sh_file = PathUtils.ofPath(inputs.param_project_root, inputs.param_project_shell_file)
                sh "chmod +x ${sh_file};${sh_file}"
            }
        ]
    ]

    def tools = ["sonarqube"] as Set

    if (StringUtils.isNotEmpty(inputs.param_tools)) {
        tools.addAll(inputs.param_tools.split(","))
    }

    def codeObj = codeMap.find { it.name == inputs.param_code_type }
    if (codeObj) {
        if (codeObj.tool) {
            tools.addAll(codeObj.tool.call())
        }

        tools.each { t -> toolMap[t].call() }
        
        configFileProvider(configFiles) {
            codeObj.func.call()
        }
    }
}

return this