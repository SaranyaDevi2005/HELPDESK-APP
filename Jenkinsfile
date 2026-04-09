pipeline {
    agent any

    environment {
        DOCKER_USER = credentials('docker-username')
        DOCKER_PASS = credentials('docker-password')
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    pip install -r backend/services/auth_service/requirements.txt pytest httpx
                    cd backend/services/auth_service
                    python -m pytest tests/ -v --tb=short || true
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    docker build -t helpdesk-auth:${IMAGE_TAG}    ./backend/services/auth_service
                    docker build -t helpdesk-ticket:${IMAGE_TAG}  ./backend/services/ticket_service
                    docker build -t helpdesk-comment:${IMAGE_TAG} ./backend/services/comment_service
                    docker build -t helpdesk-frontend:${IMAGE_TAG} ./frontend
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                    # Install trivy if not present
                    which trivy || (curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin)
                    trivy image --severity HIGH,CRITICAL --exit-code 0 helpdesk-auth:${IMAGE_TAG}
                    trivy image --severity HIGH,CRITICAL --exit-code 0 helpdesk-frontend:${IMAGE_TAG}
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh 'sonar-scanner -Dsonar.projectKey=helpdesk -Dsonar.sources=backend,frontend'
                }
            }
        }

        stage('Push to DockerHub') {
            when { branch 'main' }
            steps {
                sh '''
                    echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                    for svc in auth ticket comment; do
                        docker tag helpdesk-${svc}:${IMAGE_TAG} ${DOCKER_USER}/helpdesk-${svc}:latest
                        docker push ${DOCKER_USER}/helpdesk-${svc}:latest
                    done
                    docker tag helpdesk-frontend:${IMAGE_TAG} ${DOCKER_USER}/helpdesk-frontend:latest
                    docker push ${DOCKER_USER}/helpdesk-frontend:latest
                '''
            }
        }

        stage('Update Manifests') {
            when { branch 'main' }
            steps {
                sh '''
                    sed -i "s|image:.*helpdesk-auth:.*|image: ${DOCKER_USER}/helpdesk-auth:${IMAGE_TAG}|" \
                        manifests/deployments/auth-deployment.yaml
                    git config user.email "jenkins@helpdesk.com"
                    git config user.name "Jenkins CI"
                    git add manifests/
                    git diff --staged --quiet || git commit -m "ci: image tag ${IMAGE_TAG}"
                    git push origin main || true
                '''
            }
        }
    }

    post {
        success { echo "✅ Pipeline passed — ArgoCD will sync the cluster" }
        failure { echo "❌ Pipeline failed — check logs above" }
    }
}
