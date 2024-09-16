pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/w1ldweasel/fast-api-one.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                // Install dependencies from requirements.txt
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                // Run tests using pytest
                sh 'pytest'
            }
        }
    }
}
