pipeline {
    agent any
    environment {
        SONARQUBE_URL = 'sonarqube'  // Use http://localhost:9000/ or in this case the container name if on same Docker bridge network
        GITHUB_REPO_URL = 'https://github.com/w1ldweasel/fast-api-one.git'
        SONAR_PROJECT_KEY = 'fast-api-one' //project-key
        SONAR_LOGIN_TOKEN = credentials('jenkin-sonar')  // Stored in Jenkins
        GIT_CREDENTIALS_ID = 'PAT'  // GitHub PAT 
        
   stages {
        stage('Checkout Code') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: 'main']],
                    userRemoteConfigs: [[
                        url: GITHUB_REPO_URL,
                        credentialsId: GIT_CREDENTIALS_ID
                    ]]
                ])
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withCredentials([string(credentialsId: 'sonar-token-id', variable: 'SONAR_LOGIN_TOKEN')]) {
                    sh """
                    sonar-scanner \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=${SONARQUBE_URL} \
                        -Dsonar.login=${SONAR_LOGIN_TOKEN}
                    """
                }
            }
        }
    }
}
