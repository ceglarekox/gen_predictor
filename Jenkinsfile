pipeline {
    agent any

    stages {
        stage('clone repo') {
            steps {
                echo 'cloning repo..'
		sh "git clone https://github.com/ceglarekox/gen_predictor.git"
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
		sh "python3 testing/unit_tests.py"
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
