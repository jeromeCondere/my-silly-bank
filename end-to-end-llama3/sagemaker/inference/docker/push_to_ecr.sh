aws ecr get-login-password --region us-east-1 --profile profile-admin | docker login --username AWS --password-stdin 629874083750.dkr.ecr.us-east-1.amazonaws.com
docker build -t inference-pytorch24 . --no-cache
docker tag inference-pytorch24:latest 629874083750.dkr.ecr.us-east-1.amazonaws.com/inference-pytorch24:latest
docker push 629874083750.dkr.ecr.us-east-1.amazonaws.com/inference-pytorch24:latest
