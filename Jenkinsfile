
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Automated Tests') {
            steps {
                sh 'venv/bin/python -m pytest -v'
            }
        }

        stage('Build Application') {
            steps {
                sh '''
                    mkdir -p build
                    tar --exclude=venv \
                        --exclude=.git \
                        --exclude=build \
                        -czf build/devops-task-manager.tar.gz \
                        app tests requirements.txt
                '''
            }
        }

        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'build/*.tar.gz',
                                 fingerprint: true
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f kubernetes/deployment.yaml
                    kubectl apply -f kubernetes/service.yaml
                    kubectl rollout status deployment/task-manager-deployment
                    kubectl get pods
                    kubectl get services
                '''
            }
        }
    }
}
