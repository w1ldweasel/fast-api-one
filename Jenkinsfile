pipeline {
    agent any

    environment {
        SONARQUBE_ENV = 'sonarqube' // Match SonarQube server name in Jenkins configuration
    }

    stages {
        stage('Clone repository') {
            steps {
                git credentialsId: 'github-credentials-id', url: 'https://github.com/yourusername/yourrepo.git'
            }
        }

        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv(SONARQUBE_ENV) {
                    sh '''
                    sonar-scanner \
                    -Dsonar.projectKey=your_project_key \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://sonarqube:9000 \
                    -Dsonar.login=$SONARQUBE_AUTH_TOKEN
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
}
