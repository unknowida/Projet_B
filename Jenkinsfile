pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sh 'whoami'
                sh 'ls -l'
                sh 'chmod 764 ./cert.sh'
                sh './cert.sh'
                sh 'docker build -f DockerfileA -t microa:microa .'
                sh 'docker build -f DockerfileB -t microb:microb .'
                sh 'docker build -f DockerfileC -t microc:microc .'
                sh 'ls -l'
            }
        }
        stage('Setup Environment') {
            steps {
                // Fetch and place the wordpress.env file
                withCredentials([file(credentialsId: 'wordpress.env', variable: 'WORDPRESS_ENV')]) {
                    sh "cp ${WORDPRESS_ENV} ./wordpress.env"
                    sh "cat wordpress.env"
                }
            }
        }
        stage('Run') {
            steps {
                echo 'Running..'
                sh 'docker-compose -f docker-compose.yml up -d'
            }
        }
        stage('Test') {
            steps {
                echo 'Running..'
                sh 'sleep 10s'
                sh 'python3 ./test/servicetest.py'
                sh 'python3 ./test/waftest.py'
            }
        }
    }
post {
    always {
        sh 'rm -f ./sqldb.env'
        sh 'rm -f ./wordpress.env'
    }
}
}
