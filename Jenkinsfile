pipeline {
    agent {
        docker {
            image 'python:3.11-alpine'
            args '-u root --network jenkins -v jenkins-pip-cache:/root/.cache/pip'
        }
    }

    environment {
        SONARQUBE_ENV = 'sonarserver'
        SCANNER_HOME  = tool 'sonarqube8.0'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                sh 'apk add --no-cache gcc musl-dev'
                sh 'pip install -r requirements.txt pytest pytest-cov flake8'
            }
        }

        stage('Verification') {
            parallel {
                stage('Unit Tests & Coverage') {
                    steps {
                        sh 'pytest --cov=. --cov-report=xml'
                    }
                }
                stage('Code Linting') {
                    steps {
                        sh 'flake8 . --exit-zero'
                    }
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    sh """
                        ${SCANNER_HOME}/sonar-scanner-*/bin/sonar-scanner \
                          -Dsonar.projectKey=ncc-health \
                          -Dsonar.projectName=ncc-health \
                          -Dsonar.sources=. \
                          -Dsonar.python.coverage.reportPaths=coverage.xml
                    """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline Sukses! Check SonarQube for Code Quality.'
        }
        failure {
            echo 'Pipeline Gagal!'
        }
    }
}